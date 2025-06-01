"""
Sistema de Memória Compartilhada entre Agentes - ETAPA 4
Implementa orquestração eficiente de memória para evitar reprocessamento
Seguindo especificações Gemini AI
"""

import json
import hashlib
import time
import threading
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from pathlib import Path
from abc import ABC, abstractmethod
import pickle

# Logger
try:
    from utils.logger import get_logger
except ImportError:
    class SimpleLogger:
        def __init__(self, name): self.name = name
        def info(self, msg): print(f"[INFO] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
        def debug(self, msg): print(f"[DEBUG] {msg}")
    def get_logger(name): return SimpleLogger(name)

logger = get_logger(__name__)


@dataclass
class MemoryEntry:
    """Entrada de memória compartilhada"""
    key: str                           # Chave única
    value: Any                         # Valor armazenado
    agent_owner: str                   # Agente que criou
    shared_with: Set[str]             # Agentes com acesso
    created_at: datetime              
    accessed_at: datetime             
    access_count: int = 0
    ttl_seconds: int = 3600           # TTL padrão: 1 hora
    is_high_value: bool = False       # Informação de alto valor
    tags: Set[str] = field(default_factory=set)  # Tags para busca
    
    def is_expired(self) -> bool:
        """Verifica se a entrada expirou"""
        return datetime.now() - self.created_at > timedelta(seconds=self.ttl_seconds)
    
    def update_access(self):
        """Atualiza estatísticas de acesso"""
        self.accessed_at = datetime.now()
        self.access_count += 1


@dataclass 
class AgentMemoryIndex:
    """Índice de memórias de um agente específico"""
    agent_name: str
    entries: Dict[str, str] = field(default_factory=dict)  # key -> memory_key
    specialties: Set[str] = field(default_factory=set)     # Especialidades do agente
    last_activity: datetime = field(default_factory=datetime.now)
    
    def add_entry(self, local_key: str, memory_key: str):
        """Adiciona entrada ao índice do agente"""
        self.entries[local_key] = memory_key
        self.last_activity = datetime.now()


class MemorySearchIndex:
    """Índice de busca por tags e palavras-chave"""
    
    def __init__(self):
        self.tag_index: Dict[str, Set[str]] = {}        # tag -> set(memory_keys)
        self.keyword_index: Dict[str, Set[str]] = {}    # keyword -> set(memory_keys)
        self.agent_index: Dict[str, Set[str]] = {}      # agent -> set(memory_keys)
        self.lock = threading.Lock()
    
    def add_entry(self, memory_key: str, entry: MemoryEntry):
        """Adiciona entrada aos índices de busca"""
        with self.lock:
            # Índice de tags
            for tag in entry.tags:
                if tag not in self.tag_index:
                    self.tag_index[tag] = set()
                self.tag_index[tag].add(memory_key)
            
            # Índice de agente
            if entry.agent_owner not in self.agent_index:
                self.agent_index[entry.agent_owner] = set()
            self.agent_index[entry.agent_owner].add(memory_key)
            
            # Índice de palavras-chave (extrair do valor se for string)
            if isinstance(entry.value, str):
                keywords = self._extract_keywords(entry.value)
                for keyword in keywords:
                    if keyword not in self.keyword_index:
                        self.keyword_index[keyword] = set()
                    self.keyword_index[keyword].add(memory_key)
    
    def search_by_tag(self, tag: str) -> Set[str]:
        """Busca entradas por tag"""
        with self.lock:
            return self.tag_index.get(tag, set()).copy()
    
    def search_by_keyword(self, keyword: str) -> Set[str]:
        """Busca entradas por palavra-chave"""
        with self.lock:
            return self.keyword_index.get(keyword.lower(), set()).copy()
    
    def search_by_agent(self, agent_name: str) -> Set[str]:
        """Busca entradas de um agente específico"""
        with self.lock:
            return self.agent_index.get(agent_name, set()).copy()
    
    def _extract_keywords(self, text: str, min_length: int = 4) -> Set[str]:
        """Extrai palavras-chave relevantes de um texto"""
        import re
        
        # Stop words em português
        stop_words = {
            "o", "a", "de", "da", "do", "que", "é", "para", "com", "em", 
            "um", "uma", "por", "se", "no", "na", "os", "as", "dos", "das",
            "este", "esta", "isso", "isso", "seu", "sua", "como", "mais"
        }
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = {
            word for word in words 
            if len(word) >= min_length and word not in stop_words
        }
        
        return keywords


class SharedMemorySystem:
    """
    Sistema de Memória Compartilhada entre Agentes
    Implementa especificações Gemini para evitar reprocessamento
    """
    
    def __init__(self, data_dir: str = "memory/shared", max_memory_items: int = 10000):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.max_memory_items = max_memory_items
        self.memory_store: Dict[str, MemoryEntry] = {}
        self.agent_indices: Dict[str, AgentMemoryIndex] = {}
        self.search_index = MemorySearchIndex()
        
        self.lock = threading.Lock()
        
        # Cache em memória com LRU
        self.memory_cache: Dict[str, Any] = {}
        self.cache_access_order: List[str] = []
        self.max_cache_size = 1000
        
        # Estatísticas
        self.stats = {
            "total_entries": 0,
            "cache_hits": 0,
            "cache_misses": 0,
            "reprocessing_prevented": 0,
            "tokens_saved": 0
        }
        
        # Carregar dados persistentes
        self._load_persistent_data()
        
        logger.info(f"🧠 SharedMemorySystem inicializado - {len(self.memory_store)} entradas")
    
    def store_memory(self, agent_name: str, key: str, value: Any, 
                    share_with: Set[str] = None, ttl_seconds: int = 3600,
                    is_high_value: bool = False, tags: Set[str] = None) -> str:
        """
        Armazena uma memória no sistema compartilhado
        Retorna chave única da memória
        """
        with self.lock:
            # Gerar chave única
            memory_key = self._generate_memory_key(agent_name, key, value)
            
            # Verificar se já existe (evitar duplicação)
            if memory_key in self.memory_store:
                existing = self.memory_store[memory_key]
                existing.update_access()
                if share_with:
                    existing.shared_with.update(share_with)
                return memory_key
            
            # Criar nova entrada
            entry = MemoryEntry(
                key=key,
                value=value,
                agent_owner=agent_name,
                shared_with=share_with or set(),
                created_at=datetime.now(),
                accessed_at=datetime.now(),
                ttl_seconds=ttl_seconds,
                is_high_value=is_high_value,
                tags=tags or set()
            )
            
            # Armazenar
            self.memory_store[memory_key] = entry
            self.search_index.add_entry(memory_key, entry)
            
            # Atualizar índice do agente
            if agent_name not in self.agent_indices:
                self.agent_indices[agent_name] = AgentMemoryIndex(agent_name)
            self.agent_indices[agent_name].add_entry(key, memory_key)
            
            # Adicionar ao cache
            self._add_to_cache(memory_key, value)
            
            self.stats["total_entries"] += 1
            
            # Limpeza periódica
            if len(self.memory_store) % 100 == 0:
                self._cleanup_expired()
            
            logger.debug(f"💾 Memória armazenada: {agent_name}.{key} -> {memory_key[:8]}...")
            
            return memory_key
    
    def retrieve_memory(self, agent_name: str, key: str) -> Optional[Any]:
        """Recupera memória específica de um agente"""
        with self.lock:
            # Verificar índice do agente
            if agent_name not in self.agent_indices:
                return None
            
            agent_index = self.agent_indices[agent_name]
            if key not in agent_index.entries:
                return None
            
            memory_key = agent_index.entries[key]
            return self._get_memory_by_key(memory_key)
    
    def search_shared_memory(self, requesting_agent: str, query: str, 
                           tags: Set[str] = None) -> List[Tuple[str, Any, str]]:
        """
        Busca memórias compartilhadas acessíveis ao agente
        Retorna lista de (key, value, owner_agent)
        """
        with self.lock:
            candidate_keys = set()
            
            # Buscar por tags
            if tags:
                for tag in tags:
                    candidate_keys.update(self.search_index.search_by_tag(tag))
            
            # Buscar por palavras-chave na query
            keywords = self.search_index._extract_keywords(query)
            for keyword in keywords:
                candidate_keys.update(self.search_index.search_by_keyword(keyword))
            
            # Filtrar por permissões de acesso
            accessible_memories = []
            for memory_key in candidate_keys:
                if memory_key not in self.memory_store:
                    continue
                
                entry = self.memory_store[memory_key]
                
                # Verificar se pode acessar
                if (entry.agent_owner == requesting_agent or 
                    requesting_agent in entry.shared_with or
                    not entry.shared_with):  # Compartilhado com todos se empty
                    
                    # Verificar se não expirou
                    if not entry.is_expired():
                        entry.update_access()
                        accessible_memories.append((
                            entry.key, 
                            entry.value, 
                            entry.agent_owner
                        ))
            
            # Ordenar por relevância (alto valor primeiro, depois por acessos)
            accessible_memories.sort(
                key=lambda x: (
                    self.memory_store[self._find_memory_key(x[0], x[2])].is_high_value,
                    self.memory_store[self._find_memory_key(x[0], x[2])].access_count
                ), 
                reverse=True
            )
            
            if accessible_memories:
                self.stats["reprocessing_prevented"] += 1
                self.stats["tokens_saved"] += len(accessible_memories) * 50  # Estimativa
            
            return accessible_memories[:10]  # Limitar a 10 resultados
    
    def check_similar_processing(self, agent_name: str, task_description: str, 
                                context_hash: str = None) -> Optional[Any]:
        """
        Verifica se processamento similar já foi feito
        Implementa Cache Hit Strategy do Gemini
        """
        # Gerar hash da tarefa
        if not context_hash:
            context_hash = hashlib.md5(
                f"{agent_name}:{task_description}".encode()
            ).hexdigest()
        
        # Buscar em cache primeiro
        if context_hash in self.memory_cache:
            self.stats["cache_hits"] += 1
            return self.memory_cache[context_hash]
        
        self.stats["cache_misses"] += 1
        
        # Buscar por similaridade
        similar_memories = self.search_shared_memory(
            agent_name, 
            task_description, 
            tags={"processed_task", "analysis", "research"}
        )
        
        if similar_memories:
            # Retornar resultado mais relevante
            _, result, _ = similar_memories[0]
            self._add_to_cache(context_hash, result)
            return result
        
        return None
    
    def share_memory_with_agents(self, memory_key: str, agent_names: Set[str]):
        """Compartilha memória existente com outros agentes"""
        with self.lock:
            if memory_key in self.memory_store:
                entry = self.memory_store[memory_key]
                entry.shared_with.update(agent_names)
                logger.debug(f"📤 Memória {memory_key[:8]}... compartilhada com {agent_names}")
    
    def get_agent_memory_summary(self, agent_name: str) -> Dict:
        """Retorna resumo da memória de um agente"""
        with self.lock:
            if agent_name not in self.agent_indices:
                return {"entries": 0, "specialties": [], "last_activity": None}
            
            agent_index = self.agent_indices[agent_name]
            
            # Estatísticas das memórias do agente
            agent_memories = self.search_index.search_by_agent(agent_name)
            total_size = 0
            high_value_count = 0
            
            for memory_key in agent_memories:
                if memory_key in self.memory_store:
                    entry = self.memory_store[memory_key]
                    if entry.is_high_value:
                        high_value_count += 1
                    total_size += len(str(entry.value))
            
            return {
                "entries": len(agent_index.entries),
                "specialties": list(agent_index.specialties),
                "last_activity": agent_index.last_activity,
                "total_memory_size": total_size,
                "high_value_entries": high_value_count,
                "shared_memories": len([
                    k for k in agent_memories 
                    if k in self.memory_store and self.memory_store[k].shared_with
                ])
            }
    
    def _generate_memory_key(self, agent_name: str, key: str, value: Any) -> str:
        """Gera chave única para a memória"""
        content_hash = hashlib.sha256(
            f"{agent_name}:{key}:{str(value)[:1000]}".encode()
        ).hexdigest()
        return f"{agent_name}_{content_hash[:16]}"
    
    def _get_memory_by_key(self, memory_key: str) -> Optional[Any]:
        """Obtém memória pela chave, verificando cache primeiro"""
        # Verificar cache
        if memory_key in self.memory_cache:
            self.stats["cache_hits"] += 1
            return self.memory_cache[memory_key]
        
        # Verificar store
        if memory_key in self.memory_store:
            entry = self.memory_store[memory_key]
            if not entry.is_expired():
                entry.update_access()
                self._add_to_cache(memory_key, entry.value)
                return entry.value
        
        self.stats["cache_misses"] += 1
        return None
    
    def _find_memory_key(self, key: str, agent_name: str) -> Optional[str]:
        """Encontra chave de memória baseada em key e agente"""
        if agent_name in self.agent_indices:
            return self.agent_indices[agent_name].entries.get(key)
        return None
    
    def _add_to_cache(self, key: str, value: Any):
        """Adiciona item ao cache LRU"""
        # Remover se já existe
        if key in self.memory_cache:
            self.cache_access_order.remove(key)
        
        # Adicionar no final
        self.memory_cache[key] = value
        self.cache_access_order.append(key)
        
        # Manter tamanho do cache
        while len(self.memory_cache) > self.max_cache_size:
            oldest_key = self.cache_access_order.pop(0)
            del self.memory_cache[oldest_key]
    
    def _cleanup_expired(self):
        """Remove entradas expiradas"""
        expired_keys = []
        
        for memory_key, entry in self.memory_store.items():
            if entry.is_expired() and not entry.is_high_value:
                expired_keys.append(memory_key)
        
        for key in expired_keys:
            del self.memory_store[key]
            if key in self.memory_cache:
                del self.memory_cache[key]
                if key in self.cache_access_order:
                    self.cache_access_order.remove(key)
        
        if expired_keys:
            logger.debug(f"🗑️ Removidas {len(expired_keys)} entradas expiradas")
    
    def _save_persistent_data(self):
        """Salva dados importantes em disco"""
        try:
            # Salvar entradas de alto valor
            high_value_entries = {
                k: v for k, v in self.memory_store.items() 
                if v.is_high_value and not v.is_expired()
            }
            
            with open(self.data_dir / "high_value_memories.pkl", "wb") as f:
                pickle.dump(high_value_entries, f)
            
            # Salvar índices de agentes
            with open(self.data_dir / "agent_indices.json", "w") as f:
                serializable_indices = {}
                for agent_name, index in self.agent_indices.items():
                    serializable_indices[agent_name] = {
                        "entries": index.entries,
                        "specialties": list(index.specialties),
                        "last_activity": index.last_activity.isoformat()
                    }
                json.dump(serializable_indices, f, indent=2)
                
        except Exception as e:
            logger.error(f"Erro ao salvar dados persistentes: {e}")
    
    def _load_persistent_data(self):
        """Carrega dados persistentes do disco"""
        try:
            # Carregar entradas de alto valor
            high_value_file = self.data_dir / "high_value_memories.pkl"
            if high_value_file.exists():
                with open(high_value_file, "rb") as f:
                    high_value_entries = pickle.load(f)
                    self.memory_store.update(high_value_entries)
                    
                    # Reconstruir índices de busca
                    for memory_key, entry in high_value_entries.items():
                        self.search_index.add_entry(memory_key, entry)
            
            # Carregar índices de agentes
            indices_file = self.data_dir / "agent_indices.json"
            if indices_file.exists():
                with open(indices_file, "r") as f:
                    indices_data = json.load(f)
                    
                    for agent_name, data in indices_data.items():
                        self.agent_indices[agent_name] = AgentMemoryIndex(
                            agent_name=agent_name,
                            entries=data["entries"],
                            specialties=set(data["specialties"]),
                            last_activity=datetime.fromisoformat(data["last_activity"])
                        )
                        
        except Exception as e:
            logger.warning(f"Não foi possível carregar dados persistentes: {e}")
    
    def get_system_stats(self) -> Dict:
        """Retorna estatísticas do sistema"""
        with self.lock:
            return {
                **self.stats,
                "total_memory_entries": len(self.memory_store),
                "cache_size": len(self.memory_cache),
                "registered_agents": len(self.agent_indices),
                "cache_hit_rate": (
                    self.stats["cache_hits"] / 
                    (self.stats["cache_hits"] + self.stats["cache_misses"])
                    if (self.stats["cache_hits"] + self.stats["cache_misses"]) > 0 else 0
                )
            }
    
    def shutdown(self):
        """Salva dados e finaliza sistema"""
        self._save_persistent_data()
        logger.info("💾 SharedMemorySystem finalizado - dados salvos")


# Singleton global
_shared_memory_instance = None
_shared_memory_lock = threading.Lock()


def get_shared_memory_system() -> SharedMemorySystem:
    """Retorna instância singleton do SharedMemorySystem"""
    global _shared_memory_instance
    
    with _shared_memory_lock:
        if _shared_memory_instance is None:
            _shared_memory_instance = SharedMemorySystem()
        return _shared_memory_instance


# Teste do sistema
if __name__ == "__main__":
    print("🧪 TESTE DO SISTEMA DE MEMÓRIA COMPARTILHADA")
    print("=" * 60)
    
    # Obter sistema
    memory_system = get_shared_memory_system()
    
    # Simular uso por diferentes agentes
    
    # 1. DeepAgent pesquisa sobre patinhos
    research_result = {
        "topic": "patinhos decorativos",
        "market_size": "R$ 2.5M",
        "competition": "média",
        "demand": "alta"
    }
    
    memory_key1 = memory_system.store_memory(
        agent_name="deepagent",
        key="research_patinhos_shopee",
        value=research_result,
        share_with={"scout", "automaster", "oraculo"},
        is_high_value=True,
        tags={"research", "ecommerce", "market_analysis"}
    )
    
    print(f"✅ DeepAgent armazenou pesquisa: {memory_key1[:8]}...")
    
    # 2. ScoutAI busca informações relacionadas
    found_memories = memory_system.search_shared_memory(
        requesting_agent="scout",
        query="análise mercado patinhos decorativos shopee",
        tags={"research", "market_analysis"}
    )
    
    print(f"🔍 ScoutAI encontrou {len(found_memories)} memórias relacionadas")
    
    if found_memories:
        key, value, owner = found_memories[0]
        print(f"   📋 Usando dados de {owner}: {value}")
    
    # 3. AutoMaster verifica processamento similar
    similar = memory_system.check_similar_processing(
        agent_name="automaster",
        task_description="criar estratégia patinhos decorativos"
    )
    
    if similar:
        print(f"✅ AutoMaster encontrou processamento similar")
    else:
        print(f"❌ AutoMaster não encontrou processamento similar")
        
        # Armazenar nova estratégia
        strategy = {"phase1": "research", "phase2": "prototype", "phase3": "launch"}
        memory_system.store_memory(
            agent_name="automaster",
            key="strategy_patinhos",
            value=strategy,
            share_with={"oraculo", "reflexor"},
            tags={"strategy", "planning"}
        )
        print(f"💡 AutoMaster criou nova estratégia")
    
    # 4. Estatísticas
    stats = memory_system.get_system_stats()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Entradas na memória: {stats['total_memory_entries']}")
    print(f"   Cache hits: {stats['cache_hits']}")
    print(f"   Taxa de acerto: {stats['cache_hit_rate']:.1%}")
    print(f"   Reprocessamento evitado: {stats['reprocessing_prevented']}")
    print(f"   Tokens economizados: {stats['tokens_saved']}")
    
    # 5. Resumo por agente
    for agent in ["deepagent", "scout", "automaster"]:
        summary = memory_system.get_agent_memory_summary(agent)
        print(f"\n🤖 {agent.upper()}:")
        print(f"   Entradas: {summary['entries']}")
        print(f"   Memórias compartilhadas: {summary.get('shared_memories', 0)}")
    
    print(f"\n✅ TESTE CONCLUÍDO!")