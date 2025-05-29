"""
GPT MESTRE AUTÔNOMO - Classe Base dos Agentes
"""

import asyncio
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, AIMessage, SystemMessage

from config import config
from utils.logger import get_agent_logger, log_function_call

@dataclass
class AgentMemory:
    """Estrutura para memória do agente"""
    messages: List[Dict[str, str]]
    context: Dict[str, Any]
    created_at: datetime
    last_updated: datetime

class BaseAgent(ABC):
    """Classe base para todos os agentes do sistema"""
    
    def __init__(self, name: str, role: str, personality: str = None):
        self.name = name
        self.role = role
        self.personality = personality or self._default_personality()
        self.logger = get_agent_logger(name)
        self.memory = AgentMemory(
            messages=[],
            context={},
            created_at=datetime.now(),
            last_updated=datetime.now()
        )
        
        # Inicializa o LLM (Claude 3)
        self.llm = ChatAnthropic(
            model=config.DEFAULT_MODEL,
            temperature=config.TEMPERATURE,
            max_tokens=config.MAX_TOKENS,
            anthropic_api_key=config.ANTHROPIC_API_KEY,
        )
        
        self.logger.info(f"🤖 Agente {self.name} ({self.role}) inicializado com Claude 3")
    
    @abstractmethod
    def _default_personality(self) -> str:
        """Define a personalidade padrão do agente"""
        pass
    
    @abstractmethod
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """Processa uma mensagem e retorna uma resposta"""
        pass
    
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
            
            # Registra na memória
            self._update_memory(prompt, response.content)
            
            self.logger.debug(f"💭 {self.name} processou: {prompt[:50]}...")
            
            return response.content
            
        except Exception as e:
            self.logger.error(f"❌ Erro no processamento de {self.name}: {e}")
            return f"Desculpe, ocorreu um erro interno. ({str(e)[:100]})"
    
    def _update_memory(self, input_msg: str, output_msg: str):
        """Atualiza a memória do agente"""
        self.memory.messages.append({
            "timestamp": datetime.now().isoformat(),
            "input": input_msg,
            "output": output_msg,
            "agent": self.name
        })
        
        self.memory.last_updated = datetime.now()
        
        # Mantém apenas as últimas 50 mensagens para não sobrecarregar
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

if __name__ == "__main__":
    # Teste da classe base
    print("🧪 Testando classe base dos agentes...")
    
    class TestAgent(BaseAgent):
        def _default_personality(self):
            return "Agente de teste amigável e prestativo"
        
        async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
            return await self.think(f"Responda: {message}")
    
    # Teste básico
    async def test():
        agent = TestAgent("TestBot", "Agente de Teste")
        response = await agent.process_message("Olá, como você está?")
        print(f"Resposta: {response}")
        print(f"Memória: {agent.get_memory_summary()}")
    
    # Descomente para testar (precisa da ANTHROPIC_API_KEY configurada)
    # asyncio.run(test())
    print("✅ Classe base dos agentes criada com Claude 3!")