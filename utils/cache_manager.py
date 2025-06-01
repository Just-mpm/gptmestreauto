"""
Sistema de Cache Inteligente para GPT Mestre Autônomo
Implementa cache hierárquico com similaridade semântica
"""

import sqlite3
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, Tuple, Optional, List, Set
from collections import OrderedDict
from pathlib import Path
import re
from threading import Lock

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


class CacheManager:
    """
    Gerenciador de Cache Hierárquico
    
    Nível 1: Cache Exato (Hash)
    Nível 2: Cache por Similaridade (Jaccard)
    """
    
    def __init__(self, 
                 cache_dir: str = "data",
                 max_memory_items: int = 1000,
                 ttl_seconds: int = 3600,
                 similarity_threshold: float = 0.8):
        """
        Inicializa o gerenciador de cache
        
        Args:
            cache_dir: Diretório para armazenar o cache persistente
            max_memory_items: Número máximo de itens em memória (LRU)
            ttl_seconds: Time-to-live padrão em segundos
            similarity_threshold: Threshold para similaridade Jaccard
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.max_memory_items = max_memory_items
        self.ttl_seconds = ttl_seconds
        self.similarity_threshold = similarity_threshold
        
        # Cache em memória (Nível 1) - OrderedDict para LRU
        self.memory_cache: OrderedDict[str, Dict] = OrderedDict()
        
        # Índice de similaridade (Nível 2)
        self.similarity_index: Dict[str, Set[str]] = {}
        self.similarity_cache: Dict[str, Dict] = {}
        
        # Lock para thread safety
        self._lock = Lock()
        
        # Estatísticas
        self.stats = {
            'hits_exact': 0,
            'hits_similarity': 0,
            'misses': 0,
            'tokens_saved': 0,
            'invalidations': 0
        }
        
        # Inicializar banco de dados
        self._init_db()
        
        # Carregar cache do disco
        self._load_from_disk()
        
        logger.info("🚀 CacheManager inicializado")
        
    def _init_db(self):
        """Inicializa o banco de dados SQLite"""
        db_path = self.cache_dir / "cache.db"
        
        with sqlite3.connect(str(db_path)) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    query_hash TEXT PRIMARY KEY,
                    query_normalized TEXT,
                    response TEXT,
                    tokens_used INTEGER,
                    timestamp REAL,
                    access_count INTEGER DEFAULT 1,
                    last_accessed REAL
                )
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp ON cache(timestamp)
            """)
            
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_last_accessed ON cache(last_accessed)
            """)
            
            conn.commit()
    
    def _normalize_query(self, query: str) -> str:
        """Normaliza a pergunta para cache"""
        if not query:
            return ""
        
        # Converter para minúsculas
        normalized = query.lower()
        
        # Remover pontuação extra e espaços múltiplos
        normalized = re.sub(r'[^\w\s]', ' ', normalized)
        normalized = re.sub(r'\s+', ' ', normalized)
        normalized = normalized.strip()
        
        return normalized
    
    def _hash_query(self, query: str) -> str:
        """Gera hash SHA256 da query normalizada"""
        normalized = self._normalize_query(query)
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()
    
    def _tokenize_query(self, query: str) -> Set[str]:
        """Tokeniza a query para cálculo de similaridade"""
        normalized = self._normalize_query(query)
        
        # Palavras comuns em português para remover (stopwords simplificadas)
        stopwords = {
            'o', 'a', 'os', 'as', 'um', 'uma', 'de', 'do', 'da', 'dos', 'das',
            'em', 'no', 'na', 'nos', 'nas', 'para', 'por', 'com', 'sem',
            'e', 'ou', 'mas', 'que', 'qual', 'quais', 'como', 'onde', 'quando',
            'é', 'são', 'foi', 'será', 'seria', 'eu', 'você', 'ele', 'ela',
            'nós', 'eles', 'elas', 'meu', 'sua', 'seu', 'nosso', 'me', 'te'
        }
        
        # Tokenizar e remover stopwords
        tokens = set(normalized.split())
        tokens = tokens - stopwords
        
        # Adicionar bigramas para melhor captura de contexto
        words = normalized.split()
        for i in range(len(words) - 1):
            if words[i] not in stopwords and words[i+1] not in stopwords:
                tokens.add(f"{words[i]}_{words[i+1]}")
        
        return tokens
    
    def _calculate_jaccard_similarity(self, tokens1: Set[str], tokens2: Set[str]) -> float:
        """Calcula similaridade Jaccard entre dois conjuntos de tokens"""
        if not tokens1 or not tokens2:
            return 0.0
        
        intersection = tokens1.intersection(tokens2)
        union = tokens1.union(tokens2)
        
        if not union:
            return 0.0
        
        return len(intersection) / len(union)
    
    def _is_expired(self, timestamp: float) -> bool:
        """Verifica se um item está expirado"""
        return (time.time() - timestamp) > self.ttl_seconds
    
    def get(self, query: str) -> Tuple[Optional[str], int]:
        """
        Busca resposta no cache
        
        Returns:
            Tuple[resposta, tokens_economizados] ou (None, 0) se não encontrar
        """
        with self._lock:
            # Nível 1: Cache Exato
            query_hash = self._hash_query(query)
            
            # Verificar memória primeiro
            if query_hash in self.memory_cache:
                item = self.memory_cache[query_hash]
                
                if not self._is_expired(item['timestamp']):
                    # Atualizar LRU (mover para o final)
                    self.memory_cache.move_to_end(query_hash)
                    
                    # Atualizar estatísticas
                    self.stats['hits_exact'] += 1
                    self.stats['tokens_saved'] += item['tokens_used']
                    
                    logger.info(f"✅ Cache hit (exato): {item['tokens_used']} tokens economizados")
                    return item['response'], item['tokens_used']
                else:
                    # Expirado - remover
                    del self.memory_cache[query_hash]
                    self._remove_from_disk(query_hash)
            
            # Verificar disco se não está na memória
            disk_result = self._get_from_disk(query_hash)
            if disk_result:
                response, tokens_used = disk_result
                
                # Adicionar à memória (LRU cuidará do limite)
                self._add_to_memory(query_hash, self._normalize_query(query), 
                                  response, tokens_used)
                
                self.stats['hits_exact'] += 1
                self.stats['tokens_saved'] += tokens_used
                
                logger.info(f"✅ Cache hit (disco): {tokens_used} tokens economizados")
                return response, tokens_used
            
            # Nível 2: Cache por Similaridade
            query_tokens = self._tokenize_query(query)
            best_match = None
            best_similarity = 0.0
            
            for cached_query, cached_tokens in self.similarity_index.items():
                similarity = self._calculate_jaccard_similarity(query_tokens, cached_tokens)
                
                if similarity > best_similarity and similarity >= self.similarity_threshold:
                    best_similarity = similarity
                    best_match = cached_query
            
            if best_match and best_match in self.similarity_cache:
                item = self.similarity_cache[best_match]
                
                if not self._is_expired(item['timestamp']):
                    self.stats['hits_similarity'] += 1
                    self.stats['tokens_saved'] += item['tokens_used']
                    
                    logger.info(f"✅ Cache hit (similaridade {best_similarity:.2f}): "
                              f"{item['tokens_used']} tokens economizados")
                    return item['response'], item['tokens_used']
            
            # Cache miss
            self.stats['misses'] += 1
            logger.debug("❌ Cache miss")
            return None, 0
    
    def put(self, query: str, response: str, tokens_used: int):
        """Adiciona ou atualiza item no cache"""
        with self._lock:
            query_hash = self._hash_query(query)
            normalized_query = self._normalize_query(query)
            
            # Adicionar ao cache em memória
            self._add_to_memory(query_hash, normalized_query, response, tokens_used)
            
            # Adicionar ao índice de similaridade
            query_tokens = self._tokenize_query(query)
            self.similarity_index[normalized_query] = query_tokens
            self.similarity_cache[normalized_query] = {
                'response': response,
                'tokens_used': tokens_used,
                'timestamp': time.time()
            }
            
            # Persistir no disco
            self._save_to_disk(query_hash, normalized_query, response, tokens_used)
            
            logger.info(f"💾 Cache atualizado: {tokens_used} tokens")
    
    def _add_to_memory(self, query_hash: str, normalized_query: str, 
                      response: str, tokens_used: int):
        """Adiciona item ao cache em memória com política LRU"""
        # Remover itens mais antigos se necessário (LRU)
        while len(self.memory_cache) >= self.max_memory_items:
            oldest = next(iter(self.memory_cache))
            del self.memory_cache[oldest]
            logger.debug(f"LRU: Removido item mais antigo do cache")
        
        # Adicionar novo item
        self.memory_cache[query_hash] = {
            'response': response,
            'tokens_used': tokens_used,
            'timestamp': time.time(),
            'normalized_query': normalized_query
        }
    
    def _save_to_disk(self, query_hash: str, normalized_query: str, 
                     response: str, tokens_used: int):
        """Salva item no banco de dados"""
        db_path = self.cache_dir / "cache.db"
        
        try:
            with sqlite3.connect(str(db_path)) as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO cache 
                    (query_hash, query_normalized, response, tokens_used, 
                     timestamp, last_accessed)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (query_hash, normalized_query, response, tokens_used, 
                     time.time(), time.time()))
                conn.commit()
        except Exception as e:
            logger.error(f"Erro ao salvar no disco: {e}")
    
    def _get_from_disk(self, query_hash: str) -> Optional[Tuple[str, int]]:
        """Busca item no banco de dados"""
        db_path = self.cache_dir / "cache.db"
        
        try:
            with sqlite3.connect(str(db_path)) as conn:
                cursor = conn.execute("""
                    SELECT response, tokens_used, timestamp 
                    FROM cache 
                    WHERE query_hash = ?
                """, (query_hash,))
                
                row = cursor.fetchone()
                if row:
                    response, tokens_used, timestamp = row
                    
                    # Verificar expiração
                    if not self._is_expired(timestamp):
                        # Atualizar último acesso
                        conn.execute("""
                            UPDATE cache 
                            SET last_accessed = ?, access_count = access_count + 1
                            WHERE query_hash = ?
                        """, (time.time(), query_hash))
                        conn.commit()
                        
                        return response, tokens_used
                    else:
                        # Expirado - remover
                        self._remove_from_disk(query_hash)
                        
        except Exception as e:
            logger.error(f"Erro ao buscar no disco: {e}")
        
        return None
    
    def _remove_from_disk(self, query_hash: str):
        """Remove item do banco de dados"""
        db_path = self.cache_dir / "cache.db"
        
        try:
            with sqlite3.connect(str(db_path)) as conn:
                conn.execute("DELETE FROM cache WHERE query_hash = ?", (query_hash,))
                conn.commit()
        except Exception as e:
            logger.error(f"Erro ao remover do disco: {e}")
    
    def _load_from_disk(self):
        """Carrega cache recente do disco para memória"""
        db_path = self.cache_dir / "cache.db"
        
        try:
            with sqlite3.connect(str(db_path)) as conn:
                # Carregar itens mais recentes e não expirados
                cursor = conn.execute("""
                    SELECT query_hash, query_normalized, response, tokens_used, timestamp
                    FROM cache
                    WHERE timestamp > ?
                    ORDER BY last_accessed DESC
                    LIMIT ?
                """, (time.time() - self.ttl_seconds, self.max_memory_items))
                
                for row in cursor:
                    query_hash, normalized_query, response, tokens_used, timestamp = row
                    
                    self.memory_cache[query_hash] = {
                        'response': response,
                        'tokens_used': tokens_used,
                        'timestamp': timestamp,
                        'normalized_query': normalized_query
                    }
                    
                    # Reconstruir índice de similaridade
                    query_tokens = self._tokenize_query(normalized_query)
                    self.similarity_index[normalized_query] = query_tokens
                    self.similarity_cache[normalized_query] = {
                        'response': response,
                        'tokens_used': tokens_used,
                        'timestamp': timestamp
                    }
                
                logger.info(f"📂 Carregados {len(self.memory_cache)} itens do cache")
                
        except Exception as e:
            logger.error(f"Erro ao carregar cache do disco: {e}")
    
    def invalidate(self, query: Optional[str] = None):
        """Invalida um item específico ou todo o cache"""
        with self._lock:
            if query:
                # Invalidar item específico
                query_hash = self._hash_query(query)
                
                if query_hash in self.memory_cache:
                    del self.memory_cache[query_hash]
                
                normalized = self._normalize_query(query)
                if normalized in self.similarity_index:
                    del self.similarity_index[normalized]
                if normalized in self.similarity_cache:
                    del self.similarity_cache[normalized]
                
                self._remove_from_disk(query_hash)
                
                self.stats['invalidations'] += 1
                logger.info(f"🗑️ Item invalidado: {query[:50]}...")
            else:
                # Invalidar todo o cache
                self.memory_cache.clear()
                self.similarity_index.clear()
                self.similarity_cache.clear()
                
                # Limpar banco de dados
                db_path = self.cache_dir / "cache.db"
                try:
                    with sqlite3.connect(str(db_path)) as conn:
                        conn.execute("DELETE FROM cache")
                        conn.commit()
                except Exception as e:
                    logger.error(f"Erro ao limpar banco de dados: {e}")
                
                self.stats['invalidations'] += len(self.memory_cache)
                logger.info("🗑️ Cache completamente invalidado")
    
    def cleanup(self):
        """Remove itens expirados"""
        with self._lock:
            # Limpar memória
            expired_keys = []
            for key, item in self.memory_cache.items():
                if self._is_expired(item['timestamp']):
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.memory_cache[key]
            
            # Limpar índice de similaridade
            expired_queries = []
            for query, item in self.similarity_cache.items():
                if self._is_expired(item['timestamp']):
                    expired_queries.append(query)
            
            for query in expired_queries:
                if query in self.similarity_index:
                    del self.similarity_index[query]
                del self.similarity_cache[query]
            
            # Limpar disco
            db_path = self.cache_dir / "cache.db"
            try:
                with sqlite3.connect(str(db_path)) as conn:
                    conn.execute("""
                        DELETE FROM cache 
                        WHERE timestamp < ?
                    """, (time.time() - self.ttl_seconds,))
                    conn.commit()
            except Exception as e:
                logger.error(f"Erro ao limpar disco: {e}")
            
            if expired_keys or expired_queries:
                logger.info(f"🧹 Limpeza: {len(expired_keys)} itens expirados removidos")
    
    def get_stats(self) -> Dict[str, int]:
        """Retorna estatísticas do cache"""
        total_hits = self.stats['hits_exact'] + self.stats['hits_similarity']
        total_requests = total_hits + self.stats['misses']
        
        hit_rate = (total_hits / total_requests * 100) if total_requests > 0 else 0
        
        return {
            **self.stats,
            'total_hits': total_hits,
            'total_requests': total_requests,
            'hit_rate': round(hit_rate, 2),
            'memory_items': len(self.memory_cache),
            'similarity_items': len(self.similarity_index)
        }
    
    def __del__(self):
        """Cleanup ao destruir o objeto"""
        try:
            self.cleanup()
        except:
            pass


# Singleton global
_cache_instance: Optional[CacheManager] = None


def get_cache_manager(**kwargs) -> CacheManager:
    """Retorna instância singleton do CacheManager"""
    global _cache_instance
    
    if _cache_instance is None:
        _cache_instance = CacheManager(**kwargs)
    
    return _cache_instance


if __name__ == "__main__":
    # Teste básico
    print("🧪 Testando CacheManager...")
    
    cache = CacheManager()
    
    # Teste 1: Cache exato
    cache.put("Qual a capital da França?", "A capital da França é Paris.", 50)
    response, tokens = cache.get("Qual a capital da França?")
    print(f"✅ Cache exato: {response[:30]}... ({tokens} tokens economizados)")
    
    # Teste 2: Cache por similaridade
    response, tokens = cache.get("Me diga a capital da França")
    print(f"✅ Cache similaridade: {response[:30]}... ({tokens} tokens economizados)")
    
    # Estatísticas
    print(f"\n📊 Estatísticas: {cache.get_stats()}")