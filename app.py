"""
GPT MESTRE AUTÔNOMO - Interface Streamlit SIMPLES v5.0
Interface limpa focada na funcionalidade
"""

import streamlit as st
import asyncio
from datetime import datetime
import uuid

# Configuração da página
st.set_page_config(
    page_title="GPT Mestre Autônomo v5.0",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Imports do sistema
try:
    from config import config
    from agents.carlos import criar_carlos_maestro
    from utils.logger import get_logger
    
    system_logger = get_logger("streamlit")
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.error("📦 Instale as dependências:")
    st.code("pip install -r requirements.txt", language="bash")
    st.stop()

# Inicialização da sessão
def init_session_state():
    """Inicializa sessão com Carlos v5.0"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if "carlos" not in st.session_state:
        try:
            st.session_state.carlos = criar_carlos_maestro(
                supervisor_ativo=True,
                reflexor_ativo=True,
                deepagent_ativo=True,
                oraculo_ativo=True,
                automaster_ativo=True,
                taskbreaker_ativo=True
            )
            system_logger.info(f"🚀 Carlos v5.0 inicializado para sessão {st.session_state.session_id}")
                
        except Exception as e:
            st.error(f"❌ Erro ao inicializar Carlos v5.0: {e}")
            st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

# Interface principal
def main():
    init_session_state()
    
    # Header simples
    st.title("🧠 GPT Mestre Autônomo v5.0")
    st.markdown("*Sistema Revolucionário com 9 Agentes Autônomos*")
    
    # Status dos agentes
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🛡️ BaseAgentV2")
    with col2:
        st.success("🧠 LangChain + Claude 3")
    with col3:
        st.warning("⚡ 9 Agentes v2.0")
    with col4:
        st.info("🔍 ScoutAI v1.3A")
    
    st.divider()
    
    # Sidebar simples
    with st.sidebar:
        st.header("🤖 Sistema")
        st.metric("Agentes", "9/9")
        st.metric("Sessão", st.session_state.session_id)
        
        if st.button("🧹 Limpar Chat"):
            st.session_state.messages = []
            st.rerun()
    
    # Área de chat
    st.subheader("💬 Chat com Carlos v5.0")
    
    # Container para mensagens
    chat_container = st.container()
    
    # Histórico de mensagens
    with chat_container:
        for i, message in enumerate(st.session_state.messages):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "timestamp" in message:
                    st.caption(f"*{message['timestamp']}*")
    
    # Mostrar indicador se Carlos está processando
    if "processing" in st.session_state and st.session_state.processing:
        st.info("🧠 Carlos está processando... (Assembleia dinâmica pode levar até 40s)")
        st.balloons()
    
    # Input do usuário
    if prompt := st.chat_input("Digite sua mensagem..."):
        
        # Marcar como processando
        st.session_state.processing = True
        
        # Adicionar mensagem do usuário
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        # Contexto para processamento
        context = {
            "session_id": st.session_state.session_id,
            "timestamp": timestamp,
            "interface": "streamlit_v5.0"
        }
        
        # Processar resposta
        try:
            resposta = st.session_state.carlos.processar(prompt, context)
            system_logger.info(f"Resposta gerada com sucesso para: {prompt[:50]}...")
                
        except Exception as e:
            system_logger.error(f"Erro no processamento: {e}")
            resposta = f"❌ Erro no processamento: {str(e)}"
        
        # Adicionar resposta ao histórico
        response_time = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "assistant", 
            "content": resposta,
            "timestamp": response_time
        })
        
        # Marcar como não processando
        st.session_state.processing = False
        
        # Forçar rerun para mostrar as mensagens
        st.rerun()

# Footer simples
def show_footer():
    st.divider()
    st.markdown("## 🧠 GPT Mestre Autônomo v5.0")
    st.markdown("*Sistema Revolucionário com Assembleia Dinâmica*")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.info("🛡️ BaseAgentV2")
    with col2:
        st.success("🧠 LangChain + Claude 3")
    with col3:
        st.warning("⚡ 9 Agentes v2.0")
    with col4:
        st.info("🔍 ScoutAI v1.3A")
    
    st.divider()
    st.markdown("✨ **Desenvolvido por Matheus Meireles** com arquitetura revolucionária")
    st.caption("🚀 O futuro da autonomia artificial • Único sistema com assembleia dinâmica no mundo")

# Execução
if __name__ == "__main__":
    try:
        main()
        show_footer()
    except Exception as e:
        st.error(f"❌ Erro na aplicação: {e}")
        
        if st.button("🚨 Reiniciar Sistema"):
            st.session_state.clear()
            st.rerun()