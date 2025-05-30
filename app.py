"""
GPT MESTRE AUTÔNOMO - Interface Streamlit v2.0
VERSÃO COM MEMÓRIA INTELIGENTE
"""

import streamlit as st
import asyncio
from datetime import datetime
import uuid
import json

# Configuração da página
st.set_page_config(
    page_title="GPT Mestre Autônomo v2.0 - Memória Inteligente",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== IMPORTS ATUALIZADOS PARA v2.0 =====
try:
    from config import config
    from agents.carlos import criar_carlos_integrado  # Carlos v2.0
    from utils.logger import get_logger
    
    system_logger = get_logger("streamlit")
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.error("📦 Instale as dependências da Fase 2:")
    st.code("pip install chromadb sentence-transformers", language="bash")
    st.stop()

# CSS atualizado com tema de memória
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #1e3c72 0%, #2a5298 50%, #764ba2 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.memory-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    color: white;
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
.memory-active { color: #6f42c1; font-weight: bold; }

.version-badge {
    background: #007bff;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ===== INICIALIZAÇÃO v2.0 =====
def init_session_state():
    """Inicializa sessão com Carlos v2.0 + Memória Inteligente"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if "carlos" not in st.session_state:
        try:
            # Carlos v2.0 com memória vetorial + reflexor
            st.session_state.carlos = criar_carlos_integrado(
                supervisor_ativo=True,  # Futuro
                reflexor_ativo=True     # Ativo
            )
            system_logger.info(f"🧠 Carlos v2.0 inicializado para sessão {st.session_state.session_id}")
                
        except Exception as e:
            st.error(f"❌ Erro ao inicializar Carlos v2.0: {e}")
            
            # Diagnóstico específico
            if "chromadb" in str(e).lower():
                st.error("🔧 **ChromaDB não encontrado!**")
                st.code("pip install chromadb sentence-transformers", language="bash")
            elif "sentence" in str(e).lower():
                st.error("🔧 **Sentence Transformers não encontrado!**")
                st.code("pip install sentence-transformers", language="bash")
            
            st.info("💡 A memória vetorial é opcional. O sistema funcionará em modo básico.")
            st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensagem de boas-vindas v2.0
        st.session_state.messages.append({
            "role": "assistant",
            "content": """🧠 **Olá! Sou o Carlos v2.0 com Memória Inteligente!**

🚀 **Principais novidades:**
• **Memória Vetorial**: Lembro de TODAS as nossas conversas
• **Busca Semântica**: Encontro automaticamente contexto relevante  
• **Aprendizado Contínuo**: Cada conversa me torna mais inteligente
• **Reflexor v1.5+**: Auditoria automática de qualidade

💬 **Como funciona:**
Converse naturalmente! Automaticamente busco conversas anteriores similares e aprendizados relevantes para dar respostas mais precisas.

**Experimente:** "Volte ao assunto que falamos sobre..." ou "Lembra quando discutimos...?"

**Comandos:** `/help`, `/status`, `/memory`""",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

# ===== SIDEBAR v2.0 =====
def render_sidebar():
    """Sidebar atualizada com informações de memória"""
    with st.sidebar:
        st.header("🧠 GPT Mestre v2.0")
        st.markdown('<span class="version-badge">MEMÓRIA INTELIGENTE</span>', unsafe_allow_html=True)
        
        # Status do sistema
        st.subheader("📊 Status do Sistema")
        st.markdown("**Carlos:** <span class='agent-active'>v2.0 ativo</span>", unsafe_allow_html=True)
        st.markdown("**Reflexor:** <span class='agent-active'>✅ v1.5+</span>", unsafe_allow_html=True)
        
        # Status da memória
        if hasattr(st.session_state.carlos, 'memoria_ativa'):
            if st.session_state.carlos.memoria_ativa:
                st.markdown("**Memória:** <span class='memory-active'>🧠 Ativa</span>", unsafe_allow_html=True)
                st.markdown("**ChromaDB:** <span class='memory-active'>✅ Conectado</span>", unsafe_allow_html=True)
            else:
                st.markdown("**Memória:** <span class='agent-inactive'>❌ Inativa</span>", unsafe_allow_html=True)
        
        # Informações da sessão
        st.subheader("📋 Sessão")
        st.text(f"ID: {st.session_state.session_id}")
        
        # Nome do usuário
        user_name = st.text_input("Seu nome:", value=st.session_state.user_name)
        if user_name != st.session_state.user_name:
            st.session_state.user_name = user_name
        
        # Estatísticas de memória
        if hasattr(st.session_state.carlos, 'get_memory_stats'):
            try:
                stats = st.session_state.carlos.get_memory_stats()
                
                st.subheader("🧠 Memória Inteligente")
                
                # Stats principais
                processing = stats.get('processing_stats', {})
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("💬 Conversas", processing.get('with_memory', 0))
                    st.metric("🔍 Buscas", processing.get('semantic_searches', 0))
                
                with col2:
                    st.metric("🎯 Contexto", processing.get('context_retrieved', 0))
                    st.metric("📚 Aprendizados", processing.get('learnings_saved', 0))
                
                # Qualidade média
                quality = processing.get('avg_quality_score', 0.0)
                if quality > 0:
                    st.metric("⭐ Qualidade", f"{quality:.1f}/10")
                
                # Progresso visual
                session_total = stats['session_memory']['conversations']
                if session_total > 0:
                    progress = min(session_total / 20, 1.0)
                    st.progress(progress)
                    st.caption(f"Sessão: {session_total}/20 interações")
                
            except Exception as e:
                st.error(f"Erro nas stats: {str(e)[:50]}...")
        
        # Botões de controle
        st.subheader("🔧 Ações")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Limpar"):
                st.session_state.messages = []
                if hasattr(st.session_state.carlos, 'conversa_memoria'):
                    st.session_state.carlos.conversa_memoria.clear()
                st.success("✅ Sessão limpa!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset"):
                if st.button("⚠️ Confirmar?"):
                    st.session_state.clear()
                    st.rerun()
        
        # Comandos rápidos v2.0
        st.subheader("⚡ Comandos v2.0")
        
        comandos = [
            ("📊", "Status", "/status"),
            ("🧠", "Memória", "/memory"),
            ("🤖", "Agentes", "/agents"),
            ("📈", "Stats", "/stats")
        ]
        
        col1, col2 = st.columns(2)
        for i, (icon, label, cmd) in enumerate(comandos):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(f"{icon} {label}"):
                    add_message("user", cmd)
        
        # Informações do sistema
        st.subheader("ℹ️ Sistema")
        st.text("🤖 Carlos v2.0")
        st.text("🔗 Claude 3 Haiku")
        st.text("🧠 ChromaDB")
        st.text("🔍 Reflexor v1.5+")
        st.text(f"🐛 Debug: {'On' if config.DEBUG else 'Off'}")

def add_message(role: str, content: str):
    """Adiciona mensagem e força rerun"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    st.rerun()

def show_memory_indicator(response_text: str):
    """Mostra indicador de uso da memória"""
    if "CONTEXTO RELEVANTE" in response_text or "conversa anterior" in response_text.lower():
        st.info("🧠 **Memória Inteligente Ativada** - Esta resposta foi enriquecida com contexto de conversas anteriores!")

# ===== INTERFACE PRINCIPAL v2.0 =====
def main():
    """Interface principal v2.0 com memória inteligente"""
    
    # Inicializa sessão
    init_session_state()
    
    # Header v2.0
    st.markdown("""
    <div class="main-header">
        <h1>🧠 GPT Mestre Autônomo v2.0</h1>
        <p>Sistema com Memória Inteligente • Busca Semântica • Aprendizado Contínuo</p>
        <small>✨ Powered by ChromaDB + Claude 3 Haiku + Reflexor v1.5+</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()
    
    # Área principal
    st.header("💬 Conversa com Carlos v2.0")
    st.caption("🧠 Sistema de memória inteligente ativo - Nunca esqueço nada!")
    
    # Instruções v2.0
    with st.expander("💡 Como usar a Memória Inteligente v2.0", expanded=False):
        st.markdown("""
        **🧠 Sistema de Memória Vetorial Ativo!**
        
        **🔍 Busca Automática:**
        - Cada pergunta busca automaticamente conversas similares
        - Recupera aprendizados relevantes do histórico  
        - Aplica contexto para respostas mais precisas
        
        **💡 Exemplos de Continuidade:**
        - *"Volte ao tema de precificação"* → Encontra discussões anteriores
        - *"Como ficou aquela análise?"* → Busca análises relacionadas
        - *"Lembra do produto que discutimos?"* → Recupera contexto específico
        
        **📚 Aprendizado Contínuo:**
        - Respostas de alta qualidade são salvas automaticamente
        - Padrões são identificados e reutilizados
        - Conhecimento cresce a cada interação
        
        **🔍 Reflexor v1.5+:**
        - Auditoria automática de qualidade
        - Score de confiança em tempo real
        - Melhoria contínua das respostas
        
        **💾 Persistência:**
        - Todas as conversas ficam salvas localmente
        - Funciona offline (ChromaDB local)
        - Sem dependência de serviços externos
        """)
    
    # Container do chat
    chat_container = st.container()
    
    # Histórico de mensagens
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message.get("timestamp"):
                    st.caption(f"*{message['timestamp']}*")
                
                # Indicador de memória para respostas do assistente
                if message["role"] == "assistant" and len(message["content"]) > 200:
                    show_memory_indicator(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("💬 Converse comigo... Lembro de tudo que conversamos! 🧠"):
        
        # Mensagem do usuário
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": timestamp
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
            st.caption(f"*{timestamp}*")
        
        # Resposta do Carlos v2.0
        with st.chat_message("assistant"):
            with st.spinner("🧠 Carlos v2.0 processando (buscando na memória vetorial...)"):
                
                context = {
                    "session_id": st.session_state.session_id,
                    "user_name": st.session_state.user_name,
                    "timestamp": timestamp,
                    "interface": "streamlit_v2.0"
                }
                
                try:
                    # Processar com Carlos v2.0
                    resposta = st.session_state.carlos.processar(prompt, context)
                    
                except Exception as e:
                    system_logger.error(f"Erro no processamento v2.0: {e}")
                    resposta = f"❌ Erro no processamento: {str(e)}"
                    
                    # Sugestões para erros comuns
                    if "chroma" in str(e).lower():
                        resposta += "\n\n💡 **Solução**: `pip install chromadb sentence-transformers`"
                    elif "memory" in str(e).lower():
                        resposta += "\n\n💡 Sistema funcionará sem memória vetorial."
            
            # Exibir resposta
            st.markdown(resposta)
            response_time = datetime.now().strftime("%H:%M:%S")
            st.caption(f"*{response_time} - Carlos v2.0 com memória*")
            
            # Mostrar indicador se usou memória
            show_memory_indicator(resposta)
            
            # Adicionar ao histórico
            st.session_state.messages.append({
                "role": "assistant", 
                "content": resposta,
                "timestamp": response_time
            })
    
    # Debug expandido v2.0
    if config.DEBUG:
        with st.expander("🔧 Debug v2.0 (Memória + Reflexor)", expanded=False):
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Stats Gerais")
                try:
                    if hasattr(st.session_state.carlos, 'stats'):
                        st.json(st.session_state.carlos.stats)
                except Exception as e:
                    st.error(f"Erro stats: {e}")
            
            with col2:
                st.subheader("🧠 Stats de Memória")
                try:
                    if hasattr(st.session_state.carlos, 'get_memory_stats'):
                        memory_stats = st.session_state.carlos.get_memory_stats()
                        st.json(memory_stats)
                except Exception as e:
                    st.error(f"Erro memória: {e}")
            
            # Informações técnicas
            st.subheader("🔧 Info Técnica")
            info_tecnica = {
                "versao_carlos": "2.0",
                "memoria_ativa": getattr(st.session_state.carlos, 'memoria_ativa', False),
                "reflexor_ativo": getattr(st.session_state.carlos, 'reflexor_ativo', False),
                "session_id": st.session_state.session_id,
                "total_messages": len(st.session_state.messages)
            }
            st.json(info_tecnica)

# ===== FOOTER v2.0 =====
def show_footer():
    """Footer atualizado para v2.0"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🧠 <strong>GPT Mestre Autônomo v2.0</strong> | Desenvolvido por Matheus Meireles</p>
            <p>✨ Sistema com Memória Vetorial • ChromaDB • Busca Semântica • Claude 3 Haiku</p>
            <p>🤖 Carlos v2.0 • 🔍 Reflexor v1.5+ • 💾 Memória Permanente Local</p>
            <p><small>🚀 Fase 2 Concluída - Sistema Inteligente com Aprendizado Contínuo</small></p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ===== EXECUÇÃO PRINCIPAL =====
if __name__ == "__main__":
    try:
        main()
        show_footer()
    except Exception as e:
        try:
            system_logger.error(f"❌ Erro na aplicação v2.0: {e}")
        except:
            pass
        
        st.error(f"❌ Erro na aplicação v2.0: {e}")
        
        # Diagnóstico inteligente
        if "chromadb" in str(e).lower() or "sentence" in str(e).lower():
            st.error("🔧 **PROBLEMA DE DEPENDÊNCIAS**")
            st.code("pip install chromadb sentence-transformers", language="bash")
            st.info("Depois reinicie: `streamlit run app.py`")
        
        elif "anthropic" in str(e).lower():
            st.error("🔑 **PROBLEMA DE API KEY**")
            st.info("Configure ANTHROPIC_API_KEY no arquivo .env")
        
        elif "import" in str(e).lower():
            st.error("📦 **PROBLEMA DE IMPORTS**")
            st.info("Verifique se todos os arquivos estão no local correto")
        
        # Botão de emergência
        if st.button("🚨 Reiniciar Sistema"):
            st.session_state.clear()
            st.rerun()
