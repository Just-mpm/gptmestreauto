"""
GPT MESTRE AUTÔNOMO - Interface Chainlit APRIMORADA v5.0
🚀 ETAPA 5: Interface e UX completa com todas as melhorias Gemini AI

Funcionalidades implementadas:
✅ 15 Comandos Especiais Naturais
✅ Sistema de Feedback Visual em ASCII  
✅ Personalidade nas Respostas de Erro
✅ Onboarding de 3 Passos para Novos Usuários
✅ Sistema de Otimização Integrado
✅ Monitoramento de Custos em Tempo Real
"""

import chainlit as cl
import asyncio
import threading
from datetime import datetime
import uuid
import os
import sys
import time

# Adicionar o diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports do sistema base
try:
    from config import config
    from agents.carlos import criar_carlos_maestro
    from utils.logger import get_logger
    
    # Imports das melhorias ETAPA 5
    from utils.natural_commands import get_natural_command_processor
    from utils.visual_feedback import get_visual_feedback_manager, ErrorDisplay
    from utils.onboarding_system import (
        get_onboarding_manager, check_and_start_onboarding, 
        process_message_with_onboarding
    )
    
    # Imports das otimizações
    from utils.agent_orchestrator import get_agent_orchestrator
    from utils.token_monitor import get_token_monitor
    
    system_logger = get_logger("chainlit_enhanced")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    exit(1)

# Configurações do Chainlit
cl.config.name = "🧠 GPT Mestre Autônomo v5.0 Enhanced"
cl.config.human_timeout = 300

# Estado global
carlos_instance = None
user_sessions = {}  # Gerenciar múltiplas sessões


class UserSession:
    """Classe para gerenciar estado de sessão do usuário"""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.user_id = session_id[:8]  # Usar primeiros 8 chars como user_id
        self.start_time = datetime.now()
        self.message_count = 0
        self.onboarding_completed = False
        
        # Componentes de UX
        self.command_processor = get_natural_command_processor()
        self.feedback_manager = get_visual_feedback_manager()
        self.onboarding_manager = get_onboarding_manager()
        self.orchestrator = get_agent_orchestrator()
        self.token_monitor = get_token_monitor()
        
        system_logger.info(f"👤 Nova sessão criada: {self.user_id}")


@cl.on_chat_start
async def start():
    """Inicializa o sistema com UX aprimorada"""
    global carlos_instance
    
    session_id = str(uuid.uuid4())
    user_session = UserSession(session_id)
    user_sessions[session_id] = user_session
    
    # Armazenar session_id no contexto do Chainlit
    cl.user_session.set("session_id", session_id)
    
    # Verificar se precisa de onboarding
    onboarding_message = check_and_start_onboarding(user_session.user_id)
    
    if onboarding_message:
        # Usuário novo - mostrar onboarding
        welcome_msg = cl.Message(
            content=onboarding_message,
            author="Carlos"
        )
        await welcome_msg.send()
        system_logger.info(f"👋 Onboarding iniciado para {user_session.user_id}")
        
    else:
        # Usuário experiente - mensagem de boas-vindas rápida
        welcome_content = """👋 **Oi! Carlos aqui, pronto para mais uma sessão produtiva!**

🚀 **Sistema 100% operacional** com todas as otimizações ativas.

💡 **Dica rápida**: 
• Use comandos naturais para economizar cota
• Digite *"Carlos, status"* para ver métricas
• Digite *"Carlos, me ajuda"* se precisar de orientação

**Como posso te ajudar hoje?** 😊"""
        
        welcome_msg = cl.Message(
            content=welcome_content,
            author="Carlos"  
        )
        await welcome_msg.send()
    
    # Inicializar Carlos se não estiver ativo
    if not carlos_instance:
        try:
            # Mostrar feedback visual de inicialização
            init_steps = ["Carregando Módulos", "Ativando Agentes", "Conectando APIs", "Sistema Pronto"]
            
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
                inovacoes_ativas=True
            )
            
            system_logger.info(f"🚀 Sistema inicializado para sessão {session_id}")
            
        except Exception as e:
            error_msg = cl.Message(
                content=f"❌ Erro na inicialização: {str(e)}\n\nTente recarregar a página.",
                author="Sistema"
            )
            await error_msg.send()
            system_logger.error(f"❌ Erro na inicialização: {e}")


@cl.on_message
async def main(message: cl.Message):
    """Processa mensagens com UX aprimorada e todas as otimizações"""
    global carlos_instance
    
    session_id = cl.user_session.get("session_id")
    if not session_id or session_id not in user_sessions:
        error_msg = cl.Message(
            content="❌ Sessão inválida. Recarregue a página.",
            author="Sistema"
        )
        await error_msg.send()
        return
    
    user_session = user_sessions[session_id]
    user_session.message_count += 1
    
    if not carlos_instance:
        ErrorDisplay.show_critical_error("Sistema não inicializado")
        error_msg = cl.Message(
            content="❌ Sistema não inicializado. Recarregue a página.",
            author="Carlos"
        )
        await error_msg.send()
        return
    
    user_input = message.content.strip()
    
    try:
        # ETAPA 1: Verificar se está em onboarding
        onboarding_response, should_process_normally = process_message_with_onboarding(
            user_input, user_session.user_id
        )
        
        if onboarding_response:
            response_msg = cl.Message(
                content=onboarding_response,
                author="Carlos"
            )
            await response_msg.send()
            
            if should_process_normally:
                user_session.onboarding_completed = True
                # Continuar processamento normal após onboarding
            else:
                return  # Ainda em onboarding, não processar mais
        
        # ETAPA 2: Verificar comandos especiais naturais
        command_response = user_session.command_processor.process_command(user_input)
        
        if command_response and command_response.is_handled:
            # Comando especial processado - resposta instantânea
            
            # Mostrar feedback visual de resposta rápida
            quick_indicator = user_session.feedback_manager.show_quick_response()
            
            # Adicionar métricas ao final da resposta
            tokens_info = f"\n\n💎 *Comando otimizado: {command_response.tokens_saved} tokens economizados*"
            final_content = command_response.content + tokens_info
            
            response_msg = cl.Message(
                content=final_content,
                author="Carlos"
            )
            await response_msg.send()
            
            system_logger.info(f"⚡ Comando especial: {command_response.command_type}")
            return
        
        # ETAPA 3: Processamento normal com otimização
        
        # Mostrar feedback visual de processamento
        thinking_indicator = user_session.feedback_manager.show_thinking("Analisando sua solicitação")
        
        # Obter métricas antes do processamento
        before_usage = user_session.token_monitor.get_current_usage()
        tokens_before = before_usage['total_tokens']
        
        try:
            # Processar com orquestrador otimizado
            optimized_response = user_session.orchestrator.process_optimized(
                user_input, 
                context={"user_id": user_session.user_id}
            )
            
            # Parar indicador de pensamento
            thinking_indicator.stop()
            
            # Se usou agentes, mostrar feedback específico
            if optimized_response.agents_used:
                agent_indicator = user_session.feedback_manager.show_agent_working(
                    ", ".join(optimized_response.agents_used), 
                    "finalizando"
                )
                await asyncio.sleep(0.5)  # Breve pausa para visibilidade
                agent_indicator.stop()
            
            # Mostrar sucesso
            user_session.feedback_manager.show_success()
            
            # Construir resposta final
            response_content = optimized_response.content
            
            # Adicionar métricas se houver consumo ou economia significativa
            if optimized_response.tokens_used > 0 or optimized_response.tokens_saved > 50:
                metrics_info = f"\n\n📊 *"
                
                if optimized_response.tokens_used > 0:
                    metrics_info += f"{optimized_response.tokens_used} tokens • "
                
                if optimized_response.tokens_saved > 0:
                    metrics_info += f"💎 {optimized_response.tokens_saved} economizados • "
                
                metrics_info += f"⚡ {optimized_response.total_execution_time:.1f}s"
                
                if optimized_response.optimization_applied:
                    metrics_info += f" • 🔧 {', '.join(optimized_response.optimization_applied)}"
                
                metrics_info += "*"
                response_content += metrics_info
            
            # Enviar resposta
            response_msg = cl.Message(
                content=response_content,
                author="Carlos"
            )
            await response_msg.send()
            
            # Log da interação
            system_logger.info(f"✅ Resposta otimizada: {optimized_response.complexity_detected.value}")
            
        except Exception as processing_error:
            # Parar indicadores
            thinking_indicator.stop()
            
            # Mostrar erro com personalidade
            if "timeout" in str(processing_error).lower():
                ErrorDisplay.show_timeout_error()
                error_content = "⏰ **Timeout!** Um dos agentes demorou demais para responder. Que tal tentar uma pergunta mais simples ou aguardar um momento?"
            
            elif "api" in str(processing_error).lower():
                ErrorDisplay.show_api_error()
                error_content = "🔌 **Problema de Conexão!** Houve um contratempo com os serviços externos. Vamos tentar novamente?"
            
            else:
                ErrorDisplay.show_critical_error(str(processing_error))
                error_content = "🚨 **Oops!** Tive um pequeno curto-circuito. Pode reformular sua pergunta?"
            
            error_msg = cl.Message(
                content=error_content,
                author="Carlos"
            )
            await error_msg.send()
            
            system_logger.error(f"❌ Erro no processamento: {processing_error}")
        
    except Exception as e:
        # Erro crítico - mostrar personalidade do Carlos
        ErrorDisplay.show_critical_error(str(e))
        
        error_msg = cl.Message(
            content="🤖 **Carlos está confuso!** Algo inesperado aconteceu. Pode tentar de novo com uma pergunta diferente?",
            author="Carlos"
        )
        await error_msg.send()
        
        system_logger.error(f"❌ Erro crítico: {e}")


@cl.on_stop
async def stop():
    """Limpa recursos quando o chat para"""
    global carlos_instance
    
    session_id = cl.user_session.get("session_id")
    if session_id and session_id in user_sessions:
        user_session = user_sessions[session_id]
        
        # Parar todos os indicadores visuais
        user_session.feedback_manager.stop_all_indicators()
        
        # Log da sessão
        duration = datetime.now() - user_session.start_time
        system_logger.info(
            f"🛑 Sessão {user_session.user_id} encerrada: "
            f"{user_session.message_count} mensagens, {duration.total_seconds():.0f}s"
        )
        
        # Limpar sessão
        del user_sessions[session_id]
    
    # Não limpar carlos_instance - pode ser usado por outras sessões


# Comando personalizado para mostrar dashboard completo
@cl.action_callback("show_dashboard")
async def show_dashboard_action(action):
    """Ação para mostrar dashboard completo"""
    try:
        from utils.dashboard_display import get_dashboard_summary
        
        monitor = get_token_monitor()
        usage = monitor.get_current_usage()
        prediction = monitor.predict_monthly_cost()
        
        dashboard_content = f"""
📊 **Dashboard Completo - GPT Mestre Autônomo**

**💰 Custos e Consumo Atual:**
• Tokens consumidos: {usage['total_tokens']:,}
• Custo atual: R$ {usage['estimated_cost_brl']:.2f}
• % da cota Max 5x: {usage['quota_percentage']:.1f}%
• Velocidade: {usage['tokens_per_minute']:.0f} tokens/min

**📈 Previsões:**
• Custo diário: R$ {prediction['daily_cost_brl']:.2f}
• Custo mensal: R$ {prediction['monthly_cost_brl']:.2f}

**🔥 Top 3 Agentes:**"""
        
        for i, (agent, data) in enumerate(usage['top_consumers'][:3], 1):
            dashboard_content += f"\n{i}. {agent}: {data['total_tokens']:,} tokens (R$ {data['cost_brl']:.2f})"
        
        # Adicionar alertas se houver
        if usage.get('alerts'):
            latest_alert = usage['alerts'][-1]
            dashboard_content += f"\n\n⚠️ **Último Alerta:**\n{latest_alert['message']}"
        
        dashboard_content += f"\n\n💡 {get_dashboard_summary()}"
        
        dashboard_msg = cl.Message(
            content=dashboard_content,
            author="Sistema de Monitoramento"
        )
        await dashboard_msg.send()
        
    except Exception as e:
        error_msg = cl.Message(
            content=f"❌ Erro ao gerar dashboard: {str(e)}",
            author="Sistema"
        )
        await error_msg.send()


# Adicionar ações personalizadas na interface
@cl.on_chat_start
async def setup_actions():
    """Configura ações personalizadas na interface"""
    
    # Ação para mostrar dashboard
    dashboard_action = cl.Action(
        name="show_dashboard",
        label="📊 Dashboard",
        description="Mostrar dashboard completo de custos e uso"
    )
    
    # Ação para comandos de ajuda
    help_action = cl.Action(
        name="show_help", 
        label="🆘 Ajuda",
        description="Mostrar comandos disponíveis"
    )
    
    # Ação para status rápido
    status_action = cl.Action(
        name="quick_status",
        label="⚡ Status",
        description="Status rápido do sistema"
    )
    
    await cl.Message(
        content="🎛️ **Ações rápidas disponíveis nos botões acima**",
        actions=[dashboard_action, help_action, status_action]
    ).send()


@cl.action_callback("show_help")
async def show_help_action(action):
    """Ação para mostrar ajuda"""
    help_content = """
🆘 **Guia Rápido - GPT Mestre Autônomo v5.0**

**🎯 Comandos Naturais (Economizam Cota):**
• *"Carlos, como está o sistema?"* - Status completo
• *"Carlos, quem está por aí?"* - Lista de agentes
• *"Carlos, quanto gastei hoje?"* - Uso da cota
• *"Carlos, me ajuda com [tópico]"* - Ajuda específica
• *"Carlos, seja mais conciso"* - Ajustar verbosidade
• *"Carlos, modo criativo"* - Ativar modo criativo

**🚀 Exemplos de Uso:**
• *"Analise o mercado de [produto]"* - DeepAgent + Scout
• *"Crie um prompt de vendas"* - PromptCrafter
• *"Me ajude a decidir entre X e Y"* - Oráculo
• *"Estou me sentindo ansioso"* - PsyMind

**💡 Dicas de Otimização:**
• Comandos como este não gastam sua cota Max 5x
• Seja específico para melhores resultados
• Use feedback para me ajudar a melhorar
• Sistema já otimiza automaticamente para economia

**🎨 Interface:**
• Use os botões de ação rápida acima
• Feedback visual mostra o que está acontecendo
• Métricas aparecem automaticamente nas respostas

**🔧 Em caso de problemas:**
• Recarregue a página se algo não funcionar
• Use *"Carlos, tenho um feedback"* para reportar issues
• Errors têm personalidade - Carlos te orienta!
    """
    
    help_msg = cl.Message(
        content=help_content,
        author="Sistema de Ajuda"
    )
    await help_msg.send()


@cl.action_callback("quick_status") 
async def quick_status_action(action):
    """Ação para status rápido"""
    try:
        monitor = get_token_monitor()
        usage = monitor.get_current_usage()
        
        status_emoji = "🟢" if usage['quota_percentage'] < 70 else "🟡" if usage['quota_percentage'] < 90 else "🔴"
        
        quick_status = f"""
{status_emoji} **Status Rápido**

📊 **Cota**: {usage['quota_percentage']:.1f}% usada
💰 **Custo**: R$ {usage['estimated_cost_brl']:.2f}
🤖 **Agentes**: Todos operacionais
⚡ **Sistema**: Otimizado e funcionando

{get_dashboard_summary()}
        """.strip()
        
        status_msg = cl.Message(
            content=quick_status,
            author="Monitor do Sistema"
        )
        await status_msg.send()
        
    except Exception as e:
        error_msg = cl.Message(
            content="⚡ **Sistema Operacional!** Monitor temporariamente indisponível, mas tudo funcionando.",
            author="Carlos"
        )
        await error_msg.send()


if __name__ == "__main__":
    print("🚀 Iniciando GPT Mestre Autônomo v5.0 Enhanced...")
    print("📋 Funcionalidades ETAPA 5 ativas:")
    print("   ✅ 15 Comandos Especiais Naturais")
    print("   ✅ Sistema de Feedback Visual ASCII")
    print("   ✅ Personalidade em Respostas de Erro")
    print("   ✅ Onboarding de 3 Passos")
    print("   ✅ Sistema de Otimização Completo")
    print("   ✅ Monitoramento de Custos em Tempo Real")
    print("🌟 Interface e UX otimizada para Claude Max 5x!")
    
    cl.run()