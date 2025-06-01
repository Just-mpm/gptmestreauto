"""
GPT MESTRE AUTÔNOMO - Interface Chainlit SIMPLES
🤖 Apenas Carlos responde - Sistema silencioso e eficiente
"""

import chainlit as cl
import asyncio
from datetime import datetime
import uuid
import os
import sys

# Adicionar o diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports do sistema
try:
    from config import config
    from agents.carlos import criar_carlos_maestro
    from utils.logger import get_logger
    
    system_logger = get_logger("chainlit_simples")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    exit(1)

# Configurações do Chainlit
cl.config.name = "🧠 GPT Mestre Autônomo v5.0"
cl.config.human_timeout = 300  # 5 minutos para operações complexas

# Estado global
carlos_instance = None

@cl.on_chat_start
async def start():
    """Inicializa o sistema de forma simples e rápida"""
    global carlos_instance
    
    session_id = str(uuid.uuid4())[:8]
    
    # Mensagem simples de inicialização
    loading_msg = cl.Message(content="🚀 Inicializando GPT Mestre Autônomo...")
    await loading_msg.send()
    
    try:
        # Inicializar Carlos com todos os sistemas
        carlos_instance = criar_carlos_maestro(
            supervisor_ativo=True,
            reflexor_ativo=True,
            deepagent_ativo=True,
            oraculo_ativo=True,
            automaster_ativo=True,
            taskbreaker_ativo=True,
            psymind_ativo=True,
            promptcrafter_ativo=True,
            memoria_ativa=True,
            modo_proativo=True,
            inovacoes_ativas=True  # Ativar as 10 inovações
        )
        
        # Apagar mensagem de loading
        await loading_msg.remove()
        
        # Mensagem de boas-vindas simples
        welcome_msg = cl.Message(
            content=f"""
🎉 **GPT Mestre Autônomo v5.0 Pronto!**

Olá! Sou Carlos, seu assistente inteligente. Posso ajudar com:

• 💡 Análises e estratégias
• 🎯 Planejamento de projetos e carreira
• 🚀 Automação e otimização
• 🎨 Criação de conteúdo e prompts
• 🔍 Pesquisas e insights
• 🧠 Decisões complexas

**Como posso ajudar você hoje?** 😊
""",
            author="Carlos"
        )
        
        await welcome_msg.send()
        system_logger.info(f"🚀 Sistema inicializado - Sessão {session_id}")
        
    except Exception as e:
        error_msg = cl.Message(
            content=f"❌ Erro na inicialização: {str(e)}\n\nTente recarregar a página."
        )
        await error_msg.send()
        system_logger.error(f"❌ Erro na inicialização: {e}")

@cl.on_message
async def main(message: cl.Message):
    """Processa mensagens de forma simples e direta"""
    global carlos_instance
    
    if not carlos_instance:
        error_msg = cl.Message(content="❌ Sistema não inicializado. Recarregue a página.")
        await error_msg.send()
        return
    
    user_input = message.content.strip()
    
    # Verificar comandos especiais
    if user_input.lower() == "/status":
        try:
            from utils.dashboard_display import get_dashboard_summary
            from utils.token_monitor import get_token_monitor
            
            monitor = get_token_monitor()
            usage = monitor.get_current_usage()
            prediction = monitor.predict_monthly_cost()
            
            status_content = f"""
📊 **Status do Sistema - GPT Mestre Autônomo**

**💰 Custos e Consumo:**
• Tokens consumidos: {usage['total_tokens']:,}
• Custo atual: R$ {usage['estimated_cost_brl']:.2f}
• % da cota Max 5x: {usage['quota_percentage']:.1f}%
• Velocidade: {usage['tokens_per_minute']:.0f} tokens/min

**📈 Previsões:**
• Custo diário: R$ {prediction['daily_cost_brl']:.2f}
• Custo mensal: R$ {prediction['monthly_cost_brl']:.2f}

**🔥 Top 3 Agentes:**"""
            
            for i, (agent, data) in enumerate(usage['top_consumers'][:3], 1):
                status_content += f"\n{i}. {agent}: {data['total_tokens']:,} tokens (R$ {data['cost_brl']:.2f})"
            
            # Adicionar alertas se houver
            if usage.get('alerts'):
                latest_alert = usage['alerts'][-1]
                status_content += f"\n\n⚠️ **Último Alerta:**\n{latest_alert['message']}"
            
            status_content += f"\n\n💡 {get_dashboard_summary()}"
            
            status_msg = cl.Message(
                content=status_content,
                author="Sistema"
            )
            await status_msg.send()
            return
            
        except Exception as e:
            error_msg = cl.Message(content=f"❌ Erro ao obter status: {str(e)}")
            await error_msg.send()
            return
    
    elif user_input.lower() == "/help":
        help_content = """
🆘 **Comandos Disponíveis:**

• `/status` - Mostra dashboard de monitoramento
• `/help` - Esta mensagem de ajuda

**💡 Como usar:**
Digite suas perguntas normalmente. O sistema tem:
• 🤖 Carlos Maestro - Coordenador principal
• 🔮 Oráculo - Análises profundas
• 🧠 DeepAgent - Raciocínio avançado
• 🪞 Reflexor - Autocrítica e melhoria
• 🎯 Supervisor - Coordenação estratégica
• 🎨 PromptCrafter - Engenharia de prompts
• 💭 PsyMind - Análise comportamental
• ⚡ Cache inteligente - Economia automática

**🚀 Exemplos:**
"Analise esta situação complexa..."
"Crie um plano estratégico para..."
"Me ajude a resolver este problema..."
"""
        help_msg = cl.Message(content=help_content, author="Sistema")
        await help_msg.send()
        return
    
    # Indicador simples de processamento
    thinking_msg = cl.Message(content="🤔 Pensando...")
    await thinking_msg.send()
    
    try:
        # Obter stats antes do processamento
        from utils.token_monitor import get_token_monitor
        monitor = get_token_monitor()
        before_usage = monitor.get_current_usage()
        tokens_before = before_usage['total_tokens']
        
        # Processar com Carlos (ele gerencia tudo internamente)
        response = carlos_instance.processar(user_input, {})
        
        # Obter stats depois
        after_usage = monitor.get_current_usage()
        tokens_after = after_usage['total_tokens']
        tokens_used = tokens_after - tokens_before
        
        # Remover indicador
        await thinking_msg.remove()
        
        # Enviar resposta do Carlos
        response_content = response
        
        # Adicionar métricas se houver consumo
        if tokens_used > 0:
            response_content += f"\n\n📊 *{tokens_used} tokens • R$ {after_usage['cost_per_request']:.2f} • {after_usage['quota_percentage']:.1f}% da cota*"
        
        response_msg = cl.Message(
            content=response_content,
            author="Carlos"
        )
        await response_msg.send()
        
        system_logger.info(f"✅ Resposta gerada para: {user_input[:50]}...")
        
    except Exception as e:
        # Remover indicador
        await thinking_msg.remove()
        
        # Mensagem de erro amigável
        if "timeout" in str(e).lower():
            error_content = "Desculpe, estou temporariamente indisponível. Por favor, tente novamente em alguns momentos."
        else:
            error_content = "Desculpe, não consegui processar sua mensagem. Pode tentar reformular?"
        
        error_msg = cl.Message(
            content=error_content,
            author="Carlos"
        )
        await error_msg.send()
        system_logger.error(f"❌ Erro no processamento: {e}")

@cl.on_stop
async def stop():
    """Limpa recursos quando o chat para"""
    global carlos_instance
    carlos_instance = None
    system_logger.info("🛑 Sessão encerrada")

if __name__ == "__main__":
    cl.run()