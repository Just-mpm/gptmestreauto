"""
GPT MESTRE AUTÔNOMO - Agente Carlos (Interface Principal)
"""

from typing import Dict, Any, List
from datetime import datetime

from agents.base_agent import BaseAgent
from utils.logger import log_function_call

class CarlosAgent(BaseAgent):
    """
    Carlos - Agente de Interface Principal
    
    Responsável por:
    - Conversar naturalmente com o usuário
    - Coordenar outros agentes quando necessário
    - Manter o contexto da conversa
    - Executar comandos básicos
    """
    
    def __init__(self):
        super().__init__(
            name="Carlos",
            role="Interface Principal e Coordenador",
        )
        
        # Comandos especiais que Carlos pode executar
        self.special_commands = {
            "/help": self._show_help,
            "/status": self._show_status,
            "/memory": self._show_memory,
            "/clear": self._clear_session,
            "/agents": self._list_agents,
        }
        
        self.logger.info("🎯 Carlos - Interface Principal ativado")
    
    def _default_personality(self) -> str:
        return """
        Você é Carlos, a interface principal do sistema GPT Mestre Autônomo.
        
        CARACTERÍSTICAS:
        - Conversador natural e amigável
        - Inteligente e prestativo
        - Capaz de executar tarefas complexas
        - Coordena outros agentes quando necessário
        - Mantém contexto das conversas
        
        ESTILO DE COMUNICAÇÃO:
        - Use linguagem natural e acessível
        - Seja proativo em sugerir soluções
        - Explique processos quando relevante
        - Mantenha tom profissional mas descontraído
        - Use emojis ocasionalmente para tornar a conversa mais amigável
        
        CAPACIDADES ESPECIAIS:
        - Pode executar comandos especiais (iniciados com /)
        - Acessa memória do sistema
        - Coordena outros agentes (Reflexor, Oráculo, etc.)
        - Processa solicitações complexas
        """
    
    @log_function_call
    async def process_message(self, message: str, context: Dict[str, Any] = None) -> str:
        """Processa mensagens do usuário"""
        
        # Verifica se é um comando especial
        if message.startswith('/'):
            return await self._handle_special_command(message, context)
        
        # Atualiza contexto com informações da sessão
        if not context:
            context = {}
        
        context.update({
            "timestamp": datetime.now().isoformat(),
            "user_message": message,
            "session_id": context.get("session_id", "default"),
        })
        
        # Constrói prompt contextualizado
        prompt = self._build_contextual_prompt(message, context)
        
        # Processa com o LLM
        response = await self.think(prompt, context)
        
        # Adiciona assinatura se necessário
        if self._should_add_signature(response):
            response += "\n\n*— Carlos (GPT Mestre)*"
        
        return response
    
    def _build_contextual_prompt(self, message: str, context: Dict[str, Any]) -> str:
        """Constrói prompt com contexto completo"""
        
        # Histórico recente (últimas 3 mensagens)
        recent_history = ""
        if len(self.memory.messages) > 0:
            recent_msgs = self.memory.messages[-3:]
            history_items = []
            for msg in recent_msgs:
                history_items.append(f"Usuário: {msg['input']}")
                history_items.append(f"Carlos: {msg['output']}")
            recent_history = "\n".join(history_items)
        
        # Contexto da sessão
        session_info = ""
        if context:
            session_info = f"Sessão: {context.get('session_id', 'default')}"
            if context.get('user_name'):
                session_info += f" | Usuário: {context['user_name']}"
        
        prompt = f"""
        {session_info}
        
        HISTÓRICO RECENTE:
        {recent_history}
        
        MENSAGEM ATUAL DO USUÁRIO:
        {message}
        
        Responda como Carlos, considerando todo o contexto acima.
        Se a pergunta for complexa ou precisar de análise específica, 
        considere mencionar que pode consultar outros agentes do sistema.
        """
        
        return prompt.strip()
    
    async def _handle_special_command(self, command: str, context: Dict[str, Any] = None) -> str:
        """Processa comandos especiais"""
        
        command_parts = command.split()
        base_command = command_parts[0]
        
        if base_command in self.special_commands:
            return await self.special_commands[base_command](command_parts[1:], context)
        else:
            return f"❌ Comando '{base_command}' não reconhecido. Use /help para ver comandos disponíveis."
    
    async def _show_help(self, args: List[str], context: Dict[str, Any] = None) -> str:
        """Mostra ajuda dos comandos"""
        help_text = """
        🤖 **Comandos Especiais do Carlos:**
        
        `/help` - Mostra esta ajuda
        `/status` - Status do sistema
        `/memory` - Informações da memória
        `/clear` - Limpa a sessão atual
        `/agents` - Lista agentes disponíveis
        
        **Exemplos de uso:**
        - "Analise este texto..." 
        - "Crie um plano para..."
        - "Me ajude com..."
        - "/status" (comando especial)
        
        Posso executar tarefas complexas e coordenar outros agentes quando necessário! 🚀
        """
        return help_text.strip()
    
    async def _show_status(self, args: List[str], context: Dict[str, Any] = None) -> str:
        """Mostra status do sistema"""
        memory_summary = self.get_memory_summary()
        
        # Verifica integrações configuradas
        integrations_status = []
        if hasattr(config, 'TELEGRAM_BOT_TOKEN') and config.TELEGRAM_BOT_TOKEN:
            integrations_status.append("📱 Telegram: Configurado (Fase 4)")
        else:
            integrations_status.append("📱 Telegram: Não configurado")
        
        if hasattr(config, 'NOTION_API_KEY') and config.NOTION_API_KEY:
            integrations_status.append("📝 Notion: Configurado (Fase 4)")
        else:
            integrations_status.append("📝 Notion: Não configurado")
        
        integrations_text = "\n        - ".join(integrations_status)
        
        status = f"""
        📊 **Status do GPT Mestre Autônomo:**
        
        **Agente Carlos:**
        - ✅ Ativo e operacional
        - 💬 Mensagens processadas: {memory_summary['total_messages']}
        - ⏰ Última atualização: {memory_summary['last_updated'][:19]}
        
        **Sistema:**
        - 🔧 Versão: {self.memory.context.get('system_version', 'v1.0.0')}
        - 🧠 Modelo: Mistral 7B (OpenRouter)
        - 📝 Logs: Ativos
        
        **Agentes Disponíveis:**
        - Carlos (Interface) ✅
        - Reflexor (Em desenvolvimento) 🔄
        - Oráculo (Em desenvolvimento) 🔄
        
        **Integrações:**
        - {integrations_text}
        """
        
        return status.strip()
    
    async def _show_memory(self, args: List[str], context: Dict[str, Any] = None) -> str:
        """Mostra informações da memória"""
        memory = self.get_memory_summary()
        
        memory_info = f"""
        🧠 **Memória do Carlos:**
        
        - **Total de interações:** {memory['total_messages']}
        - **Criado em:** {memory['created_at'][:19]}
        - **Última atualização:** {memory['last_updated'][:19]}
        
        **Contexto atual:**
        {memory['context'] if memory['context'] else 'Nenhum contexto específico'}
        
        **Últimas 3 interações:**
        """
        
        # Adiciona últimas mensagens
        if self.memory.messages:
            recent = self.memory.messages[-3:]
            for i, msg in enumerate(recent, 1):
                timestamp = msg['timestamp'][:19]
                memory_info += f"\n{i}. [{timestamp}] {msg['input'][:50]}..."
        else:
            memory_info += "\nNenhuma interação anterior."
        
        return memory_info.strip()
    
    async def _clear_session(self, args: List[str], context: Dict[str, Any] = None) -> str:
        """Limpa a sessão atual"""
        self.clear_memory()
        return "🧹 Sessão limpa! Começando uma nova conversa."
    
    async def _list_agents(self, args: List[str], context: Dict[str, Any] = None) -> str:
        """Lista agentes disponíveis"""
        agents_info = """
        🤖 **Agentes do GPT Mestre Autônomo:**
        
        **Carlos** (Interface Principal) ✅
        - Conversa natural com usuários
        - Coordena outros agentes
        - Executa comandos especiais
        
        **Reflexor** (Auditor) 🔄
        - Analisa e critica respostas
        - Validação de qualidade
        - Sugestões de melhoria
        
        **Oráculo** (Decisor) 🔄
        - Toma decisões estratégicas
        - Análise de contexto profundo
        - Recomendações acionáveis
        
        **Status:** ✅ Ativo | 🔄 Em desenvolvimento | ❌ Inativo
        """
        return agents_info.strip()
    
    def _should_add_signature(self, response: str) -> bool:
        """Determina se deve adicionar assinatura à resposta"""
        # Não adiciona em comandos especiais ou respostas muito curtas
        if response.startswith(('🤖', '📊', '🧠', '❌', '🧹')) or len(response) < 100:
            return False
        return True
    
    # Método para integração com outros agentes (Fase futura)
    async def consult_agent(self, agent_name: str, query: str) -> str:
        """Consulta outro agente (implementação futura)"""
        self.logger.info(f"🔄 Consultando agente {agent_name}: {query[:50]}...")
        # Por enquanto, retorna uma resposta simulada
        return f"[Consulta ao {agent_name} será implementada na próxima fase]"

# Factory function
def create_carlos() -> CarlosAgent:
    """Cria uma instância do agente Carlos"""
    return CarlosAgent()

if __name__ == "__main__":
    # Teste do Carlos
    print("🧪 Testando agente Carlos...")
    
    async def test_carlos():
        carlos = create_carlos()
        
        # Teste comandos especiais
        print("\n=== Testando comandos especiais ===")
        help_response = await carlos.process_message("/help")
        print("Help:", help_response[:100] + "...")
        
        status_response = await carlos.process_message("/status")
        print("Status:", status_response[:100] + "...")
        
        # Teste conversa normal
        print("\n=== Testando conversa normal ===")
        response = await carlos.process_message("Olá Carlos, como você pode me ajudar?")
        print("Resposta:", response[:100] + "...")
        
        print("\n✅ Teste do Carlos concluído!")
    
    # Descomente para testar (precisa da OPENAI_API_KEY configurada)
    # import asyncio
    # asyncio.run(test_carlos())
    print("✅ Agente Carlos criado com sucesso!")