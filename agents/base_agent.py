"""
GPT MESTRE AUTÔNOMO - Classe Base dos Agentes - VERSÃO CORRIGIDA
"""

import asyncio
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# Imports opcionais com fallback
try:
    from langchain_anthropic import ChatAnthropic
    from langchain.schema import HumanMessage, AIMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False

try:
    import config
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False

# Logger com fallback
try:
    from utils.logger import get_agent_logger, log_function_call
except ImportError:
    # Fallback simples para logger
    class SimpleLogger:
        def __init__(self, name): self.name = name
        def info(self, msg): print(f"[INFO] {self.name}: {msg}")
        def warning(self, msg): print(f"[WARNING] {self.name}: {msg}")  
        def error(self, msg): print(f"[ERROR] {self.name}: {msg}")
        def debug(self, msg): print(f"[DEBUG] {self.name}: {msg}")
    
    def get_agent_logger(name): return SimpleLogger(name)
    def log_function_call(*args, **kwargs): pass

@dataclass
class AgentMemory:
    """Estrutura para memória do agente"""
    messages: List[Dict[str, str]]
    context: Dict[str, Any]
    created_at: datetime
    last_updated: datetime

class BaseAgent:
    """
    Classe base para todos os agentes do sistema
    VERSÃO NÃO-ABSTRATA para compatibilidade total
    """
    
    def __init__(self, name: str, role: str = None, personality: str = None, description: str = None, llm=None):
        self.name = name
        self.role = role or description or "Agente Assistente"
        self.description = description or role or "Agente do sistema"
        self.personality = personality or self._default_personality()
        self.logger = get_agent_logger(name)
        self.memory = AgentMemory(
            messages=[],
            context={},
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        # Inicializar LLM
        if llm:
            self.llm = llm
        else:
            self.llm = self._initialize_llm()
        
        # Estatísticas básicas
        self.stats = {
            "total_interactions": 0,
            "successful_interactions": 0,
            "errors": 0,
            "last_interaction": None
        }
        
        self.logger.info(f"🤖 Agente {self.name} ({self.role}) inicializado")
    
    def _default_personality(self) -> str:
        """Define a personalidade padrão do agente"""
        return "Assistente inteligente, prestativo e profissional"
    
    def _initialize_llm(self):
        """Inicializa o LLM com fallback"""
        if not LANGCHAIN_AVAILABLE:
            self.logger.warning("LangChain não disponível - LLM não inicializado")
            return None
        
        if not CONFIG_AVAILABLE:
            self.logger.warning("Config não disponível - usando configurações padrão")
            return None
        
        try:
            return ChatAnthropic(
                model=getattr(config, 'DEFAULT_MODEL', 'claude-3-haiku-20240307'),
                temperature=getattr(config, 'TEMPERATURE', 0.7),
                max_tokens=getattr(config, 'MAX_TOKENS', 4000),
                anthropic_api_key=getattr(config, 'ANTHROPIC_API_KEY', None),
            )
        except Exception as e:
            self.logger.error(f"Erro ao inicializar LLM: {e}")
            return None
    
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """
        Processa uma mensagem e retorna uma resposta
        IMPLEMENTAÇÃO PADRÃO - pode ser sobrescrita
        """
        try:
            # Tentar usar o método síncrono se existir
            if hasattr(self, 'processar'):
                return self.processar(message, context)
            
            # Caso contrário, usar think assíncrono
            return await self.think(message, context)
            
        except Exception as e:
            self.logger.error(f"Erro no process_message: {e}")
            return f"Erro interno: {str(e)}"
    
    def processar(self, message: str, context: Optional[Dict] = None) -> str:
        """
        Método síncrono para processar mensagens
        IMPLEMENTAÇÃO PADRÃO - pode ser sobrescrita
        """
        try:
            self.update_stats(success=True)
            return f"Processado por {self.name}: {message}"
        except Exception as e:
            self.update_stats(success=False)
            return f"Erro: {str(e)}"
    
    @log_function_call
    def get_system_prompt(self) -> str:
        """Constrói o prompt do sistema para o agente"""
        base_prompt = f"""
Você é {self.name}, um agente do sistema GPT Mestre Autônomo.

PAPEL: {self.role}

PERSONALIDADE: {self.personality}

INSTRUÇÕES GERAIS:
- Seja preciso e útil em suas respostas
- Mantenha consistência com sua personalidade
- Use o contexto fornecido para dar respostas mais relevantes
- Registre informações importantes na memória
- Responda sempre em português brasileiro

CONTEXTO ATUAL: {self.memory.context}

Responda sempre no papel de {self.name}.
        """
        
        return base_prompt.strip()
    
    @log_function_call
    async def think(self, prompt: str, context: Dict[str, Any] = None) -> str:
        """Método interno para processamento de pensamento"""
        try:
            if not self.llm:
                return f"{self.name}: {prompt} (LLM não disponível)"
            
            # Atualiza contexto se fornecido
            if context:
                self.memory.context.update(context)
            
            # Constrói mensagens para o LLM
            messages = [
                SystemMessage(content=self.get_system_prompt()),
                HumanMessage(content=prompt)
            ]
            
            # Chama o LLM
            response = await self.llm.ainvoke(messages)
            response_content = response.content if hasattr(response, 'content') else str(response)
            
            # Registra na memória
            self._update_memory(prompt, response_content)
            
            self.logger.debug(f"💭 {self.name} processou: {prompt[:50]}...")
            
            return response_content
            
        except Exception as e:
            self.logger.error(f"❌ Erro no processamento de {self.name}: {e}")
            return f"Desculpe, ocorreu um erro interno: {str(e)[:100]}"
    
    def _update_memory(self, input_msg: str, output_msg: str):
        """Atualiza a memória do agente"""
        self.memory.messages.append({
            "timestamp": datetime.now().isoformat(),
            "input": input_msg,
            "output": output_msg,
            "agent": self.name
        })
        
        self.memory.last_updated = datetime.now()
        
        # Mantém apenas as últimas 50 mensagens
        if len(self.memory.messages) > 50:
            self.memory.messages = self.memory.messages[-50:]
    
    def get_memory_summary(self) -> Dict[str, Any]:
        """Retorna um resumo da memória do agente"""
        return {
            "name": self.name,
            "role": self.role,
            "total_messages": len(self.memory.messages),
            "created_at": self.memory.created_at.isoformat(),
            "last_updated": self.memory.last_updated.isoformat(),
            "context": self.memory.context
        }
    
    def clear_memory(self):
        """Limpa a memória do agente"""
        self.memory.messages.clear()
        self.memory.context.clear()
        self.memory.last_updated = datetime.now()
        self.logger.info(f"🧹 Memória do agente {self.name} limpa")
    
    def update_stats(self, success: bool = True):
        """Atualiza estatísticas do agente"""
        self.stats["total_interactions"] += 1
        self.stats["last_interaction"] = datetime.now().isoformat()
        
        if success:
            self.stats["successful_interactions"] += 1
        else:
            self.stats["errors"] += 1
    
    def get_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o agente"""
        return {
            "name": self.name,
            "role": self.role,
            "description": self.description,
            "personality": self.personality,
            "stats": self.stats,
            "memory_summary": self.get_memory_summary()
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte o agente para dicionário"""
        return self.get_info()
    
    def __str__(self) -> str:
        return f"{self.name} ({self.role})"
    
    def __repr__(self):
        return f"<Agent {self.name} ({self.role})>"

# Função utilitária para criar agentes
def create_agent(agent_class, name: str, **kwargs):
    """Factory function para criar agentes"""
    try:
        agent = agent_class(name=name, **kwargs)
        return agent
    except Exception as e:
        logger = get_agent_logger("system")
        logger.error(f"❌ Erro ao criar agente {name}: {e}")
        raise

# Classe de teste para validação
class TestAgent(BaseAgent):
    """Agente de teste para validar a classe base"""
    
    def _default_personality(self):
        return "Agente de teste amigável e prestativo"
    
    def processar(self, message: str, context: Optional[Dict] = None) -> str:
        """Implementação simples para teste"""
        return f"TestAgent processou: {message}"
    
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """Versão assíncrona para teste"""
        return await self.think(f"Responda: {message}")

# Teste básico
if __name__ == "__main__":
    print("🧪 Testando classe base dos agentes...")
    
    # Teste síncrono
    agent = TestAgent("TestBot", "Agente de Teste")
    response = agent.processar("Olá, como você está?")
    print(f"Resposta síncrona: {response}")
    print(f"Stats: {agent.stats}")
    print(f"Info: {agent.get_info()}")
    
    # Teste assíncrono (descomente se tiver LLM configurado)
    # async def test_async():
    #     response = await agent.process_message("Teste assíncrono")
    #     print(f"Resposta assíncrona: {response}")
    # 
    # asyncio.run(test_async())
    
    print("✅ Classe base testada com sucesso!")