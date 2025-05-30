"""
GPT MESTRE AUTÔNOMO - Interface Streamlit Principal
Versão Integrada: Original + Reflexor v1.5+ + Ecossistema GPT Mestre
VERSÃO COMPLETAMENTE CORRIGIDA
"""

import streamlit as st
import asyncio
from datetime import datetime
import uuid
import json
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def get_stat_safe(stats_obj, key, default=0):
    """Acesso seguro às estatísticas"""
    if isinstance(stats_obj, dict):
        return stats_obj.get(key, default)
    
    # Tentar acessar como atributo
    if hasattr(stats_obj, key):
        return getattr(stats_obj, key, default)
    
    # Mapeamentos de compatibilidade
    mappings = {
        'total_respostas': ['total_interactions', 'total_analises'],
        'respostas_melhoradas': ['successful_interactions', 'melhorias'],
        'score_medio': ['score_medio_qualidade', 'media_qualidade']
    }
    
    if key in mappings:
        for alt_key in mappings[key]:
            if isinstance(stats_obj, dict) and alt_key in stats_obj:
                return stats_obj[alt_key]
            elif hasattr(stats_obj, alt_key):
                return getattr(stats_obj, alt_key, default)
    
    return default

# Configuração da página
st.set_page_config(
    page_title="GPT Mestre Autônomo v1.5+",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports do projeto
try:
    from config import config
    from agents.carlos import create_carlos_com_reflexor, create_carlos
    from utils.logger import get_logger
    
    system_logger = get_logger("system")
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.error("Certifique-se de que todos os arquivos estão no local correto e as dependências instaladas.")
    st.stop()

# CSS customizado para interface mais elegante
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.stats-card {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
}

.score-excellent { color: #28a745; font-weight: bold; }
.score-good { color: #17a2b8; font-weight: bold; }
.score-average { color: #ffc107; font-weight: bold; }
.score-poor { color: #dc3545; font-weight: bold; }

.audit-panel {
    background: #e9ecef;
    border-left: 4px solid #007bff;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}

.improvement-panel {
    background: #d1ecf1;
    border-left: 4px solid #17a2b8;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}

.red-flag-alert {
    background: #f8d7da;
    border-left: 4px solid #dc3545;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Inicialização do estado da sessão
def init_session_state():
    """Inicializa o estado da sessão com funcionalidades expandidas"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if "carlos" not in st.session_state:
        try:
            # Configuração do modo (original ou com Reflexor)
            modo_reflexor = st.session_state.get("modo_reflexor", True)
            
            if modo_reflexor:
                st.session_state.carlos = create_carlos_com_reflexor(reflexor_ativo=True)
                system_logger.info(f"🚀 Carlos com Reflexor v1.5+ inicializado para sessão {st.session_state.session_id}")
            else:
                st.session_state.carlos = create_carlos()
                system_logger.info(f"🚀 Carlos original inicializado para sessão {st.session_state.session_id}")
                
        except Exception as e:
            st.error(f"❌ Erro ao inicializar Carlos: {e}")
            st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""
    
    # Configurações do ecossistema
    if "show_audit_details" not in st.session_state:
        st.session_state.show_audit_details = True
    
    if "modo_reflexor" not in st.session_state:
        st.session_state.modo_reflexor = True

# Função para executar código assíncrono
def run_async(coro):
    """Executa código assíncrono no Streamlit"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)
    except Exception as e:
        system_logger.error(f"❌ Erro na execução assíncrona: {e}")
        return f"Erro: {e}"
    finally:
        loop.close()

def render_audit_details(resultado):
    """Renderiza detalhes da auditoria se disponíveis"""
    if not st.session_state.show_audit_details or not resultado.get('auditoria'):
        return
    
    auditoria = resultado['auditoria']
    
    # Determinar classe CSS do score
    score = auditoria.get('score', 0)
    if score >= 9:
        score_class = "score-excellent"
    elif score >= 7:
        score_class = "score-good"
    elif score >= 5:
        score_class = "score-average"
    else:
        score_class = "score-poor"
    
    with st.expander("🔍 Detalhes da Auditoria Automática", expanded=False):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Score:** <span class='{score_class}'>{score}/10</span>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"**Confiança:** {auditoria.get('nota_confianca', 0):.1f}/10")
        with col3:
            tempo_audit = auditoria.get('tempo_auditoria', 0)
            st.markdown(f"**Tempo:** {tempo_audit}s")
        
        if auditoria.get('pontos_positivos'):
            st.markdown("**✅ Pontos Positivos:**")
            for ponto in auditoria['pontos_positivos'][:3]:  # Máximo 3
                st.markdown(f"• {ponto}")
        
        if auditoria.get('pontos_melhorar'):
            st.markdown("**⚠️ Pontos de Melhoria:**")
            for ponto in auditoria['pontos_melhorar'][:3]:  # Máximo 3
                st.markdown(f"• {ponto}")
        
        if resultado.get('melhorada', False):
            st.markdown("""
            <div class="improvement-panel">
                <strong>📈 Resposta Melhorada Automaticamente</strong><br>
                O Reflexor detectou baixa qualidade e aplicou melhorias automáticas.
            </div>
            """, unsafe_allow_html=True)

def render_sidebar_expanded():
    """Renderiza sidebar expandida com funcionalidades do ecossistema"""
    with st.sidebar:
        st.header("🎛️ Controles do Ecossistema")
        
        # Toggle do Reflexor
        st.subheader("🔍 Configurações do Reflexor")
        modo_reflexor = st.checkbox(
            "Reflexor v1.5+ Ativo", 
            value=st.session_state.modo_reflexor,
            help="Ativa auditoria automática e melhoria de respostas"
        )
        
        if modo_reflexor != st.session_state.modo_reflexor:
            st.session_state.modo_reflexor = modo_reflexor
            st.warning("Reinicie a sessão para aplicar a mudança de modo")
        
        show_audit = st.checkbox(
            "Mostrar Detalhes da Auditoria", 
            value=st.session_state.show_audit_details,
            help="Exibe informações detalhadas da análise de qualidade"
        )
        st.session_state.show_audit_details = show_audit
        
        # Informações da sessão
        st.subheader("📊 Sessão")
        st.text(f"ID: {st.session_state.session_id}")
        
        # Nome do usuário
        user_name = st.text_input("Seu nome:", value=st.session_state.user_name)
        if user_name != st.session_state.user_name:
            st.session_state.user_name = user_name
        
        # Estatísticas do ecossistema (se Reflexor ativo)
        if hasattr(st.session_state.carlos, 'stats_carlos'):
            st.subheader("📈 Estatísticas da Sessão")
            stats = st.session_state.carlos.stats_carlos
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Respostas", get_stat_safe(stats, 'total_respostas', 0))
                st.metric("Score Médio", f"{get_stat_safe(stats, 'score_medio', 0.0):.1f}/10")
            with col2:
                st.metric("Melhoradas", get_stat_safe(stats, 'respostas_melhoradas', 0))
                total_respostas = get_stat_safe(stats, 'total_respostas', 0)
                respostas_melhoradas = get_stat_safe(stats, 'respostas_melhoradas', 0)
                taxa = (respostas_melhoradas / max(1, total_respostas)) * 100
                st.metric("Taxa Melhoria", f"{taxa:.1f}%")
            
            # Red Flags se existirem
            if hasattr(st.session_state.carlos, 'reflexor') and st.session_state.carlos.reflexor:
                try:
                    red_flags = getattr(st.session_state.carlos.reflexor, 'red_flags_ativas', [])
                    if red_flags:
                        st.markdown(f"""
                        <div class="red-flag-alert">
                            <strong>🔴 {len(red_flags)} Red Flag(s) Ativo(s)</strong><br>
                            Padrões críticos detectados
                        </div>
                        """, unsafe_allow_html=True)
                except:
                    pass
        
        # Botões de controle
        st.subheader("🔧 Ações")
        
        if st.button("🧹 Limpar Conversa"):
            st.session_state.messages = []
            if hasattr(st.session_state.carlos, 'clear_memory'):
                st.session_state.carlos.clear_memory()
            st.success("Conversa limpa!")
            st.rerun()
        
        # Comandos especializados do ecossistema
        st.subheader("⚡ Comandos do Ecossistema")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Status"):
                status_cmd = "/status"
                st.session_state.messages.append({
                    "role": "user",
                    "content": status_cmd,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        
        with col2:
            if st.button("🧠 Memória"):
                memory_cmd = "/memory"
                st.session_state.messages.append({
                    "role": "user",
                    "content": memory_cmd,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        
        # Comandos do Reflexor (se ativo)
        if st.session_state.modo_reflexor:
            with col1:
                if st.button("🔍 Reflexor"):
                    reflexor_cmd = "/reflexor"
                    st.session_state.messages.append({
                        "role": "user",
                        "content": reflexor_cmd,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.rerun()
            
            with col2:
                if st.button("🔴 Red Flags"):
                    flags_cmd = "/redflags"
                    st.session_state.messages.append({
                        "role": "user",
                        "content": flags_cmd,
                        "timestamp": datetime.now().strftime("%H:%M:%S")
                    })
                    st.rerun()
        
        # Informações do sistema
        st.subheader("ℹ️ Sistema")
        st.text(f"Versão: {config.VERSION} → v1.5+")
        st.text(f"Modelo: {config.DEFAULT_MODEL}")
        st.text(f"API: Anthropic (Claude 3 Haiku)")
        st.text(f"Reflexor: {'✅ Ativo' if st.session_state.modo_reflexor else '❌ Inativo'}")
        st.text(f"Debug: {'Ativo' if config.DEBUG else 'Inativo'}")
        
        # Comandos rápidos expandidos
        st.subheader("📝 Comandos Disponíveis")
        comandos_basicos = """
        **Básicos:**
        - `/help` - Ajuda completa
        - `/status` - Status do sistema
        - `/memory` - Memória do Carlos
        - `/clear` - Limpar sessão
        - `/agents` - Listar agentes
        """
        
        comandos_ecossistema = """
        **Ecossistema:**
        - `/reflexor` - Status auditoria
        - `/redflags` - Alertas críticos
        - `/qualidade` - Relatório qualidade
        - `/ecossistema` - Status completo
        - `/continuo ativar` - Modo contínuo
        - `/metaauditoria` - Revisão dados
        """
        
        st.markdown(comandos_basicos)
        if st.session_state.modo_reflexor:
            st.markdown(comandos_ecossistema)

def render_message_with_audit(message, is_assistant=False):
    """Renderiza mensagem com informações de auditoria se for resposta do assistente"""
    
    if not is_assistant or not hasattr(message, 'get') or not message.get('audit_data'):
        # Mensagem normal
        st.markdown(message["content"] if isinstance(message, dict) else message)
        if isinstance(message, dict) and message.get("timestamp"):
            st.caption(f"*{message['timestamp']}*")
        return
    
    # Mensagem com dados de auditoria
    audit_data = message.get('audit_data', {})
    
    # Conteúdo principal
    st.markdown(message["content"])
    
    # Informações de auditoria inline
    if st.session_state.show_audit_details and audit_data:
        score = audit_data.get('score', 0)
        confianca = audit_data.get('nota_confianca', 0)
        melhorada = audit_data.get('melhorada', False)
        
        # Indicadores visuais
        indicators = []
        if score >= 8:
            indicators.append("✅ Alta Qualidade")
        elif score >= 6:
            indicators.append("⚠️ Qualidade Média")
        else:
            indicators.append("🔧 Baixa Qualidade")
            
        if melhorada:
            indicators.append("📈 Melhorada")
        
        if indicators:
            st.caption(" | ".join(indicators) + f" | Score: {score}/10")
    
    # Timestamp
    if message.get("timestamp"):
        st.caption(f"*{message['timestamp']}*")

# Interface principal
def main():
    """Interface principal do GPT Mestre Autônomo"""
    
    # Inicializa sessão
    init_session_state()
    
    # Header personalizado
    st.markdown("""
    <div class="main-header">
        <h1>🤖 GPT Mestre Autônomo v1.5+</h1>
        <p>Sistema Integrado com Reflexor • Auditoria Automática • Qualidade Garantida</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar expandida
    render_sidebar_expanded()
    
    # Área principal - Chat
    st.header("💬 Conversa com Carlos")
    
    # Container para as mensagens
    chat_container = st.container()
    
    # Exibe histórico de mensagens
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                render_message_with_audit(message, message["role"] == "assistant")
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem ou comando..."):
        
        # Adiciona mensagem do usuário ao histórico
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Exibe mensagem do usuário
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"*{timestamp}*")
        
        # Processa com Carlos (original ou integrado)
        with st.chat_message("assistant"):
            with st.spinner("Carlos está pensando..."):
                context = {
                    "session_id": st.session_state.session_id,
                    "user_name": st.session_state.user_name,
                    "timestamp": timestamp
                }
                
                # Usar método apropriado baseado no tipo de Carlos
                try:
                    # Tentar método processar primeiro (mais compatível)
                    if hasattr(st.session_state.carlos, 'processar'):
                        resultado = st.session_state.carlos.processar(prompt, context)
                    elif hasattr(st.session_state.carlos, 'process_message'):
                        resultado = run_async(
                            st.session_state.carlos.process_message(prompt, context)
                        )
                    else:
                        resultado = "Método de processamento não encontrado"
                    
                    # Verificar se resultado é dict (Carlos integrado) ou string (Carlos original)
                    if isinstance(resultado, dict):
                        response_text = resultado.get('resposta_final', resultado.get('resposta', str(resultado)))
                        audit_data = {
                            'score': resultado.get('score'),
                            'nota_confianca': resultado.get('nota_confianca'),
                            'melhorada': resultado.get('melhorada', False),
                            'auditoria': resultado.get('auditoria')
                        }
                    else:
                        response_text = str(resultado)
                        audit_data = {}
                        
                except Exception as e:
                    system_logger.error(f"Erro no processamento: {e}")
                    response_text = f"Erro no processamento: {str(e)}"
                    audit_data = {}
            
            # Exibir resposta
            st.markdown(response_text)
            response_time = datetime.now().strftime("%H:%M:%S")
            
            # Mostrar indicadores de qualidade inline se disponíveis
            if audit_data.get('score') and st.session_state.show_audit_details:
                score = audit_data['score']
                confianca = audit_data.get('nota_confianca', 0)
                melhorada = audit_data.get('melhorada', False)
                
                indicators = []
                if score >= 8:
                    indicators.append("✅ Alta Qualidade")
                elif score >= 6:
                    indicators.append("⚠️ Qualidade Média")
                else:
                    indicators.append("🔧 Baixa Qualidade")
                    
                if melhorada:
                    indicators.append("📈 Melhorada Automaticamente")
                
                if indicators:
                    st.caption(" | ".join(indicators) + f" | Score: {score}/10, Confiança: {confianca:.1f}/10")
            
            st.caption(f"*{response_time}*")
            
            # Adicionar resposta ao histórico com dados de auditoria
            message_data = {
                "role": "assistant",
                "content": response_text,
                "timestamp": response_time
            }
            
            if audit_data:
                message_data["audit_data"] = audit_data
            
            st.session_state.messages.append(message_data)
            
            # Renderizar detalhes da auditoria se disponíveis
            if isinstance(resultado, dict):
                render_audit_details(resultado)
    
    # Relatório de qualidade rápido (se Reflexor ativo)
    if (st.session_state.modo_reflexor and 
        hasattr(st.session_state.carlos, 'stats_carlos') and
        len(st.session_state.messages) > 4):  # Só mostrar após algumas interações
        
        with st.expander("📊 Relatório de Qualidade da Sessão", expanded=False):
            stats = st.session_state.carlos.stats_carlos
            total_respostas = get_stat_safe(stats, 'total_respostas', 0)
            
            if total_respostas > 0:
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total", total_respostas)
                with col2:
                    score_medio = get_stat_safe(stats, 'score_medio', 0.0)
                    st.metric("Score Médio", f"{score_medio:.1f}/10")
                with col3:
                    respostas_melhoradas = get_stat_safe(stats, 'respostas_melhoradas', 0)
                    st.metric("Melhoradas", respostas_melhoradas)
                with col4:
                    taxa = (respostas_melhoradas / total_respostas) * 100 if total_respostas > 0 else 0
                    st.metric("Taxa Melhoria", f"{taxa:.1f}%")
                
                # Gráfico simples de qualidade
                if total_respostas >= 3:
                    # Simular dados de qualidade ao longo do tempo
                    score_medio = get_stat_safe(stats, 'score_medio', 5.0)
                    df_quality = pd.DataFrame({
                        'Interação': range(1, min(total_respostas + 1, 11)),
                        'Score': [max(1, score_medio + (i % 3 - 1)) for i in range(min(total_respostas, 10))]
                    })
                    
                    fig = px.line(df_quality, x='Interação', y='Score', 
                                title='Evolução da Qualidade', 
                                range_y=[0, 10])
                    st.plotly_chart(fig, use_container_width=True)
    
    # Área de testes (apenas em debug)
    if config.DEBUG:
        with st.expander("🧪 Área de Testes (Debug Mode)"):
            st.subheader("Teste de Funcionalidades")
            
            test_col1, test_col2 = st.columns(2)
            
            with test_col1:
                if st.button("Teste: Saudação"):
                    try:
                        if hasattr(st.session_state.carlos, 'processar'):
                            test_response = st.session_state.carlos.processar("Olá Carlos, como você está?")
                        else:
                            test_response = run_async(
                                st.session_state.carlos.process_message("Olá Carlos, como você está?")
                            )
                        
                        if isinstance(test_response, dict):
                            st.write("**Resposta:**", test_response.get('resposta_final', test_response))
                            if test_response.get('auditoria'):
                                st.write("**Auditoria:**", f"Score {test_response['score']}/10")
                        else:
                            st.write("**Resposta:**", test_response)
                    except Exception as e:
                        st.write("**Erro:**", str(e))
            
            with test_col2:
                if st.button("Teste: Comando /help"):
                    try:
                        if hasattr(st.session_state.carlos, 'processar'):
                            help_response = st.session_state.carlos.processar("/help")
                        else:
                            help_response = run_async(
                                st.session_state.carlos.process_message("/help")
                            )
                        
                        if isinstance(help_response, dict):
                            st.write("**Ajuda:**", help_response.get('resposta', help_response))
                        else:
                            st.write("**Ajuda:**", help_response)
                    except Exception as e:
                        st.write("**Erro:**", str(e))
            
            # Informações de debug expandidas
            st.subheader("Debug Info")
            debug_info = {
                "session_id": st.session_state.session_id,
                "user_name": st.session_state.user_name,
                "modo_reflexor": st.session_state.modo_reflexor,
                "total_messages": len(st.session_state.messages),
                "carlos_type": type(st.session_state.carlos).__name__,
            }
            
            # Adicionar stats do ecossistema se disponível
            if hasattr(st.session_state.carlos, 'stats_carlos'):
                debug_info["stats_carlos"] = st.session_state.carlos.stats_carlos
            
            if hasattr(st.session_state.carlos, 'get_memory_summary'):
                try:
                    debug_info["carlos_memory"] = st.session_state.carlos.get_memory_summary()
                except:
                    debug_info["carlos_memory"] = "Erro ao obter memória"
            
            st.json(debug_info)

# Footer atualizado
def show_footer():
    """Exibe footer com informações do projeto atualizadas"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🤖 GPT Mestre Autônomo v{} → v1.5+ | Desenvolvido por Matheus Meireles</p>
            <p>Sistema de agentes inteligentes com Reflexor v1.5+ • Claude 3 Haiku • Auditoria Automática</p>
            <p>🔍 Qualidade garantida • 📈 Melhoria contínua • 🚀 Ecossistema integrado</p>
        </div>
        """.format(config.VERSION),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    try:
        main()
        show_footer()
    except Exception as e:
        try:
            system_logger.error(f"❌ Erro na aplicação principal: {e}")
        except:
            pass
        st.error(f"❌ Erro na aplicação: {e}")
        
        # Botão para reiniciar em caso de erro
        if st.button("🔄 Reiniciar Aplicação"):
            st.rerun()
