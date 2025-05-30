"""
GPT MESTRE AUTÔNOMO - Interface Streamlit Principal
VERSÃO CORRIGIDA PARA USAR carlos.py
"""

import streamlit as st
import asyncio
from datetime import datetime
import uuid
import json

# Configuração da página
st.set_page_config(
    page_title="GPT Mestre Autônomo v2.0",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== IMPORTS CORRIGIDOS PARA carlos.py =====
try:
    from config import config
    # CORRIGIDO: Importar do carlos.py (não mais carlos_v2.py)
    from agents.carlos import criar_carlos_integrado
    from utils.logger import get_logger
    
    system_logger = get_logger("system")
    
    # Usar sempre Carlos v2.0 integrado
    USE_CARLOS_V2 = True
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.error("Certifique-se de que todos os arquivos estão no local correto.")
    st.stop()

# CSS customizado
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

.agent-active { color: #28a745; font-weight: bold; }
.agent-inactive { color: #dc3545; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# ===== INICIALIZAÇÃO =====
def init_session_state():
    """Inicializa o estado da sessão com Carlos v2.0"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if "carlos" not in st.session_state:
        try:
            # CORRIGIDO: Usar função do carlos.py
            st.session_state.carlos = criar_carlos_integrado(
                supervisor_ativo=True,
                reflexor_ativo=True
            )
            system_logger.info(f"🚀 Carlos v2.0 + SupervisorAI inicializado para sessão {st.session_state.session_id}")
                
        except Exception as e:
            st.error(f"❌ Erro ao inicializar Carlos: {e}")
            st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

# ===== SIDEBAR =====
def render_sidebar():
    """Renderiza sidebar com informações do Carlos v2.0"""
    with st.sidebar:
        st.header("🎛️ GPT Mestre v2.0")
        
        # Status do sistema
        st.subheader("📊 Status do Sistema")
        st.markdown("**Carlos:** <span class='agent-active'>v2.0 ativo</span>", unsafe_allow_html=True)
        st.markdown("**SupervisorAI:** <span class='agent-active'>✅ Ativo</span>", unsafe_allow_html=True)
        st.markdown("**Reflexor:** <span class='agent-active'>✅ Ativo</span>", unsafe_allow_html=True)
        
        # Informações da sessão
        st.subheader("📋 Sessão")
        st.text(f"ID: {st.session_state.session_id}")
        
        # Nome do usuário
        user_name = st.text_input("Seu nome:", value=st.session_state.user_name)
        if user_name != st.session_state.user_name:
            st.session_state.user_name = user_name
        
        # Estatísticas do Carlos v2.0
        if hasattr(st.session_state.carlos, 'stats_integrado'):
            st.subheader("📈 Estatísticas v2.0")
            stats = st.session_state.carlos.stats_integrado
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Processamentos", stats.get('total_processamentos', 0))
                st.metric("Tempo Médio", f"{stats.get('tempo_medio_processamento', 0):.2f}s")
            with col2:
                st.metric("Auto-ativações", stats.get('ativacoes_automaticas', 0))
                st.metric("Score Médio", f"{stats.get('score_medio_qualidade', 0):.1f}/10")
        
        # Botões de controle
        st.subheader("🔧 Ações")
        
        if st.button("🧹 Limpar Conversa"):
            st.session_state.messages = []
            if hasattr(st.session_state.carlos, 'conversa_memoria'):
                st.session_state.carlos.conversa_memoria.clear()
            st.success("Conversa limpa!")
            st.rerun()
        
        # Comandos rápidos
        st.subheader("⚡ Comandos Rápidos")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Status"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "/status",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        
        with col2:
            if st.button("🤖 Agentes"):
                st.session_state.messages.append({
                    "role": "user", 
                    "content": "/agents",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        
        # Mais comandos
        col3, col4 = st.columns(2)
        with col3:
            if st.button("🧠 SupervisorAI"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "/supervisor",
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        
        with col4:
            if st.button("📈 Stats"):
                st.session_state.messages.append({
                    "role": "user",
                    "content": "/stats", 
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
                st.rerun()
        
        # Informações do sistema
        st.subheader("ℹ️ Sistema")
        st.text(f"Versão: Carlos v2.0")
        st.text(f"LLM: Claude 3 Haiku")
        st.text(f"SupervisorAI: ✅ Ativo")
        st.text(f"Reflexor: ✅ Ativo")
        st.text(f"Debug: {'Ativo' if config.DEBUG else 'Inativo'}")

# ===== FUNÇÃO PRINCIPAL =====
def main():
    """Interface principal do GPT Mestre Autônomo v2.0"""
    
    # Inicializa sessão
    init_session_state()
    
    # Header personalizado
    st.markdown("""
    <div class="main-header">
        <h1>🤖 GPT Mestre Autônomo v2.0</h1>
        <p>Sistema com SupervisorAI • Ativação Automática de Agentes • Conversa Natural</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()
    
    # Área principal - Chat
    st.header("💬 Conversa com Carlos v2.0")
    
    # Instruções rápidas
    with st.expander("💡 Como usar o Carlos v2.0", expanded=False):
        st.markdown("""
        **🚀 Novidade: Conversa 100% Natural!**
        
        Simplesmente fale comigo normalmente. Eu ativo automaticamente os agentes necessários:
        
        **Exemplos:**
        - *"Analise este produto do AliExpress"* → Ativa DeepAgent + ScoutAI + AutoPrice
        - *"Preciso de uma decisão estratégica"* → Ativa Oráculo + Assembleia  
        - *"Crie um anúncio otimizado"* → Ativa CopyBooster + PromptCrafter
        - *"Oi Carlos, como você está?"* → Resposta direta, sem agentes
        
        **Comandos especiais:** /help, /status, /agents, /supervisor, /memory, /clear, /stats
        """)
    
    # Container para as mensagens
    chat_container = st.container()
    
    # Exibe histórico de mensagens
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("timestamp"):
                    st.caption(f"*{message['timestamp']}*")
    
    # Input do usuário
    if prompt := st.chat_input("Fale naturalmente comigo... (Carlos v2.0 ativa agentes automaticamente)"):
        
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
        
        # Processa com Carlos v2.0
        with st.chat_message("assistant"):
            with st.spinner("Carlos v2.0 processando (SupervisorAI analisando e ativando agentes)..."):
                context = {
                    "session_id": st.session_state.session_id,
                    "user_name": st.session_state.user_name,
                    "timestamp": timestamp
                }
                
                try:
                    # CORRIGIDO: Usar método processar do Carlos v2.0
                    resposta = st.session_state.carlos.processar(prompt, context)
                    
                except Exception as e:
                    system_logger.error(f"Erro no processamento: {e}")
                    resposta = f"❌ Erro no processamento: {str(e)}"
            
            # Exibir resposta
            st.markdown(resposta)
            response_time = datetime.now().strftime("%H:%M:%S")
            st.caption(f"*{response_time}*")
            
            # Adicionar resposta ao histórico
            st.session_state.messages.append({
                "role": "assistant",
                "content": resposta,
                "timestamp": response_time
            })
    
    # Painel de debug (se ativo)
    if config.DEBUG:
        with st.expander("🔧 Debug Info (Carlos v2.0)", expanded=False):
            try:
                if hasattr(st.session_state.carlos, 'obter_status_completo'):
                    debug_info = st.session_state.carlos.obter_status_completo()
                    st.json(debug_info)
                else:
                    st.write("Método obter_status_completo não disponível")
            except Exception as e:
                st.write(f"Erro no debug: {e}")

# Footer
def show_footer():
    """Exibe footer atualizado"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🤖 GPT Mestre Autônomo v2.0 | Desenvolvido por Matheus Meireles</p>
            <p>Sistema com SupervisorAI • Ativação Automática • Claude 3 Haiku • Conversa Natural</p>
            <p>🧠 SupervisorAI v1.3 • 🤖 Carlos v2.0 • 🔍 Reflexor Integrado</p>
        </div>
        """,
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