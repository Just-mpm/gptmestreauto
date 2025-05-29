"""
GPT MESTRE AUTÔNOMO - Interface Streamlit Principal
"""

import streamlit as st
import asyncio
from datetime import datetime
import uuid

# Configuração da página
st.set_page_config(
    page_title="GPT Mestre Autônomo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Imports do projeto
try:
    from config import config
    from agents.carlos import create_carlos
    from utils.logger import system_logger
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.error("Certifique-se de que todos os arquivos estão no local correto e as dependências instaladas.")
    st.stop()

# Inicialização do estado da sessão
def init_session_state():
    """Inicializa o estado da sessão"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if "carlos" not in st.session_state:
        try:
            st.session_state.carlos = create_carlos()
            system_logger.info(f"🚀 Carlos inicializado para sessão {st.session_state.session_id}")
        except Exception as e:
            st.error(f"❌ Erro ao inicializar Carlos: {e}")
            st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

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

# Interface principal
def main():
    """Interface principal do GPT Mestre Autônomo"""
    
    # Inicializa sessão
    init_session_state()
    
    # Header
    st.title("🤖 GPT Mestre Autônomo")
    st.markdown("*Seu assistente inteligente com agentes autônomos*")
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ Controles")
        
        # Informações da sessão
        st.subheader("📊 Sessão")
        st.text(f"ID: {st.session_state.session_id}")
        
        # Nome do usuário
        user_name = st.text_input("Seu nome:", value=st.session_state.user_name)
        if user_name != st.session_state.user_name:
            st.session_state.user_name = user_name
        
        # Botões de controle
        st.subheader("🔧 Ações")
        
        if st.button("🧹 Limpar Conversa"):
            st.session_state.messages = []
            st.session_state.carlos.clear_memory()
            st.success("Conversa limpa!")
            st.experimental_rerun()
        
        if st.button("📊 Status do Sistema"):
            with st.spinner("Consultando status..."):
                status = run_async(
                    st.session_state.carlos.process_message(
                        "/status", 
                        {"session_id": st.session_state.session_id}
                    )
                )
                st.info(status)
        
        if st.button("🧠 Memória do Carlos"):
            with st.spinner("Consultando memória..."):
                memory = run_async(
                    st.session_state.carlos.process_message(
                        "/memory", 
                        {"session_id": st.session_state.session_id}
                    )
                )
                st.info(memory)
        
        # Informações do sistema
        st.subheader("ℹ️ Sistema")
        st.text(f"Versão: {config.VERSION}")
        st.text(f"Modelo: {config.DEFAULT_MODEL}")
        st.text(f"API: OpenRouter (Mistral 7B)")
        st.text(f"Debug: {'Ativo' if config.DEBUG else 'Inativo'}")
        
        # Comandos rápidos
        st.subheader("⚡ Comandos Rápidos")
        st.markdown("""
        **Comandos especiais:**
        - `/help` - Ajuda
        - `/status` - Status
        - `/memory` - Memória
        - `/clear` - Limpar
        - `/agents` - Listar agentes
        """)
    
    # Área principal - Chat
    st.header("💬 Conversa com Carlos")
    
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
    if prompt := st.chat_input("Digite sua mensagem..."):
        
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
        
        # Processa com Carlos
        with st.chat_message("assistant"):
            with st.spinner("Carlos está pensando..."):
                context = {
                    "session_id": st.session_state.session_id,
                    "user_name": st.session_state.user_name,
                    "timestamp": timestamp
                }
                
                response = run_async(
                    st.session_state.carlos.process_message(prompt, context)
                )
            
            st.markdown(response)
            response_time = datetime.now().strftime("%H:%M:%S")
            st.caption(f"*{response_time}*")
            
            # Adiciona resposta ao histórico
            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "timestamp": response_time
            })
    
    # Área de testes (apenas em debug)
    if config.DEBUG:
        with st.expander("🧪 Área de Testes (Debug Mode)"):
            st.subheader("Teste de Funcionalidades")
            
            test_col1, test_col2 = st.columns(2)
            
            with test_col1:
                if st.button("Teste: Saudação"):
                    test_response = run_async(
                        st.session_state.carlos.process_message(
                            "Olá Carlos, como você está?"
                        )
                    )
                    st.write("**Resposta:**", test_response)
            
            with test_col2:
                if st.button("Teste: Comando /help"):
                    help_response = run_async(
                        st.session_state.carlos.process_message("/help")
                    )
                    st.write("**Ajuda:**", help_response)
            
            # Informações de debug
            st.subheader("Debug Info")
            st.json({
                "session_id": st.session_state.session_id,
                "user_name": st.session_state.user_name,
                "total_messages": len(st.session_state.messages),
                "carlos_memory": st.session_state.carlos.get_memory_summary()
            })

# Footer
def show_footer():
    """Exibe footer com informações do projeto"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🤖 GPT Mestre Autônomo v{} | Desenvolvido por Matheus Meireles</p>
            <p>Sistema de agentes inteligentes com LangChain + OpenAI</p>
        </div>
        """.format(config.VERSION),
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    try:
        main()
        show_footer()
    except Exception as e:
        system_logger.error(f"❌ Erro na aplicação principal: {e}")
        st.error(f"❌ Erro na aplicação: {e}")
        
        # Botão para reiniciar em caso de erro
        if st.button("🔄 Reiniciar Aplicação"):
            st.experimental_rerun()
