"""
GPT MESTRE AUTÔNOMO - Sistema de Memória Vetorial Integrado
Versão simplificada e otimizada para Fase 2
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

try:
    import chromadb
    from chromadb.config import Settings
    from sentence_transformers import SentenceTransformer
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False

from utils.logger import get_logger

logger = get_logger(__name__)

@dataclass
class MemoryDocument:
    """Estrutura de documento na memória vetorial"""
    id: str
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    agent_source: str

class MemoryManager:
    """
    Gerenciador de Memória Vetorial - Versão Integrada
    Sistema inteligente que lembra de tudo que o Carlos conversa
    """
    
    def __init__(self, persist_directory: str = "memory/chroma_db"):
        self.persist_directory = persist_directory
        self.session_memory = {}  # Memória temporária da sessão
        
        # Verificar se ChromaDB está disponível
        if not CHROMADB_AVAILABLE:
            logger.warning("⚠️ ChromaDB não disponível - Memória vetorial DESATIVADA")
            self.memory_active = False
            self.client = None
            self.embedding_model = None
            return
        
        try:
            # Criar diretório se não existir
            os.makedirs(persist_directory, exist_ok=True)
            
            # Inicializar modelo de embedding (leve e eficiente)
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Inicializar ChromaDB
            self.client = chromadb.PersistentClient(
                path=persist_directory,
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Coleções por tipo de conteúdo
            self.conversations = self._get_or_create_collection("conversations")
            self.learnings = self._get_or_create_collection("learnings") 
            
            self.memory_active = True
            logger.info(f"🧠 MemoryManager inicializado: {persist_directory}")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar memória: {e}")
            self.memory_active = False
            self.client = None
    
    def _get_or_create_collection(self, name: str):
        """Obtém ou cria uma coleção"""
        try:
            return self.client.get_collection(name)
        except:
            return self.client.create_collection(
                name=name,
                metadata={"hnsw:space": "cosine"}
            )
    
    def remember_conversation(self, user_input: str, assistant_response: str, 
                            agent_name: str = "Carlos", session_id: str = None):
        """Salva conversa na memória permanente"""
        if not self.memory_active:
            return None
            
        try:
            doc_id = f"conv_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{agent_name}"
            
            # Combinar input e response para busca
            full_text = f"Pergunta: {user_input}\nResposta: {assistant_response}"
            
            metadata = {
                "type": "conversation",
                "agent": agent_name,
                "timestamp": datetime.now().isoformat(),
                "user_input": user_input,
                "assistant_response": assistant_response,
                "session_id": session_id or "default"
            }
            
            # Gerar embedding
            embedding = self.embedding_model.encode(full_text).tolist()
            
            self.conversations.add(
                documents=[full_text],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.debug(f"💬 Conversa salva: {doc_id}")
            return doc_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar conversa: {e}")
            return None
    
    def remember_learning(self, text: str, category: str, agent: str = "system"):
        """Salva aprendizado na memória"""
        if not self.memory_active:
            return None
            
        try:
            doc_id = f"learn_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{category}"
            
            metadata = {
                "type": "learning",
                "category": category,
                "agent_source": agent,
                "timestamp": datetime.now().isoformat()
            }
            
            embedding = self.embedding_model.encode(text).tolist()
            
            self.learnings.add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
            
            logger.info(f"🧠 Aprendizado salvo: {category}")
            return doc_id
            
        except Exception as e:
            logger.error(f"❌ Erro ao salvar aprendizado: {e}")
            return None
    
    def recall_context(self, query: str, max_results: int = 3) -> str:
        """Recupera contexto relevante como texto formatado"""
        if not self.memory_active:
            return "CONTEXTO RELEVANTE: Memória vetorial não disponível.\n\n"
            
        try:
            # Buscar conversas similares
            query_embedding = self.embedding_model.encode(query).tolist()
            
            results = self.conversations.query(
                query_embeddings=[query_embedding],
                n_results=max_results,
                include=["documents", "metadatas", "distances"]
            )
            
            formatted_context = "CONTEXTO RELEVANTE:\n\n"
            
            # Conversas similares
            if results["documents"][0]:
                formatted_context += "CONVERSAS ANTERIORES SIMILARES:\n"
                for i, doc in enumerate(results["documents"][0]):
                    similarity = (1 - results["distances"][0][i]) * 100
                    if similarity > 50:  # Só mostrar se similaridade > 50%
                        formatted_context += f"• [{similarity:.1f}% similar] {doc[:150]}...\n"
                formatted_context += "\n"
            
            return formatted_context
            
        except Exception as e:
            logger.error(f"❌ Erro ao recuperar contexto: {e}")
            return "CONTEXTO RELEVANTE: Erro na busca.\n\n"
    
    def save_memory(self, user_input: str, assistant_response: str, 
                   agent_name: str = "Carlos", session_id: str = None):
        """Método de compatibilidade para salvar memória (alias para remember_conversation)"""
        return self.remember_conversation(user_input, assistant_response, agent_name, session_id)
    
    def get_stats(self) -> Dict[str, Any]:
        """Estatísticas completas da memória"""
        if not self.memory_active:
            return {
                "memory_active": False,
                "error": "ChromaDB não disponível"
            }
            
        try:
            conv_count = self.conversations.count()
            learn_count = self.learnings.count()
            
            return {
                "memory_active": True,
                "vector_memory": {
                    "conversations": conv_count,
                    "learnings": learn_count,
                    "total_documents": conv_count + learn_count,
                    "storage_path": self.persist_directory,
                    "embedding_model": "all-MiniLM-L6-v2"
                },
                "session_memory": {
                    "active_sessions": len(self.session_memory),
                    "session_keys": list(self.session_memory.keys())
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "memory_active": False,
                "error": str(e)
            }

# Instância global para uso nos agentes
_memory_manager = None

def get_memory_manager() -> MemoryManager:
    """Retorna o gerenciador de memória global"""
    global _memory_manager
    if _memory_manager is None:
        _memory_manager = MemoryManager()
    return _memory_manager

# Funções de conveniência
def remember_conversation(user_input: str, response: str, agent: str = "Carlos", session_id: str = None):
    """Função de conveniência para salvar conversas"""
    return get_memory_manager().remember_conversation(user_input, response, agent, session_id)

def recall_context(query: str) -> str:
    """Função de conveniência para recuperar contexto"""
    return get_memory_manager().recall_context(query)

# Teste básico
if __name__ == "__main__":
    print("🧪 Testando sistema de memória...")
    
    mem = get_memory_manager()
    
    if mem.memory_active:
        # Testar salvamento
        mem.remember_conversation(
            "Como calcular preço?",
            "Para calcular preço, considere custo + margem + impostos",
            "Carlos"
        )
        
        # Testar busca
        context = mem.recall_context("precificar produto")
        print("📋 Contexto recuperado:")
        print(context)
        
        print("✅ Memória testada com sucesso!")
    else:
        print("⚠️ Memória não disponível - instale: pip install chromadb sentence-transformers")
