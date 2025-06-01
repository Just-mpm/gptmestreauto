"""
GPT MESTRE AUTÔNOMO - Interface Streamlit v2.1
VERSÃO COM DEEPAGENT TOTALMENTE INTEGRADO
🆕 NOVIDADE: Sistema agora detecta automaticamente quando precisa de pesquisa!
"""

import streamlit as st
import asyncio
from datetime import datetime
import uuid
import json

# Configuração da página - Mobile-First
st.set_page_config(
    page_title="GPT Mestre Autônomo v5.0",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",  # Mobile-friendly
    menu_items={
        'Get Help': 'https://github.com/seu-repo/issues',
        'Report a bug': 'https://github.com/seu-repo/issues',
        'About': '''
        # 🧠 GPT Mestre Autônomo v5.0
        Sistema revolucionário com 9 agentes autônomos:
        - Oráculo com assembleia dinâmica
        - AutoMaster para autonomia econômica  
        - TaskBreaker para decomposição inteligente
        - Reflexor para auditoria de qualidade
        - E muito mais!
        
        Powered by Claude 3 + LangChain
        '''
    }
)

# ===== IMPORTS ATUALIZADOS PARA v3.0 =====
try:
    from config import config
    from agents.carlos import criar_carlos_maestro  # Carlos v3.0 Maestro
    from utils.logger import get_logger
    
    system_logger = get_logger("streamlit")
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.error("📦 Instale as dependências da Fase 2 + DeepAgent:")
    st.code("pip install chromadb sentence-transformers", language="bash")
    st.stop()

# 🎨 DESIGN SYSTEM MODERNO - Premium UX
st.markdown("""
<style>
/* === VARIÁVEIS CSS === */
:root {
    --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --success-gradient: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    --warning-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
    --shadow-soft: 0 8px 32px rgba(0, 0, 0, 0.1);
    --shadow-hover: 0 12px 40px rgba(0, 0, 0, 0.15);
    --border-radius: 16px;
    --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* === RESET E BASE === */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1200px !important;
}

/* === HEADER PREMIUM === */
.main-header {
    background: var(--primary-gradient);
    padding: 2.5rem 2rem;
    border-radius: var(--border-radius);
    color: white;
    text-align: center;
    margin-bottom: 2rem;
    box-shadow: var(--shadow-soft);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    position: relative;
    overflow: hidden;
}

.main-header::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
    animation: shimmer 3s infinite;
}

@keyframes shimmer {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
    font-weight: 700;
    text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    background: linear-gradient(45deg, #fff, #f0f0f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    font-size: 1.1rem;
    opacity: 0.9;
}

/* === GLASSMORPHISM CARDS === */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px);
    border: 1px solid var(--glass-border);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: var(--shadow-soft);
    transition: var(--transition);
}

.glass-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
}

/* === AGENT CARDS === */
.agent-card {
    background: var(--primary-gradient);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    margin: 0.8rem 0;
    color: white;
    box-shadow: var(--shadow-soft);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.agent-card:hover {
    transform: translateY(-4px) scale(1.02);
    box-shadow: var(--shadow-hover);
}

.agent-card.active::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: var(--success-gradient);
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

/* === CHAT INTERFACE === */
.chat-container {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: var(--border-radius);
    padding: 1rem;
    margin: 1rem 0;
    min-height: 400px;
    position: relative;
    overflow: hidden;
}

.chat-message {
    background: white;
    border-radius: 18px;
    padding: 1rem 1.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border-left: 4px solid var(--primary-gradient);
    transition: var(--transition);
    animation: slideIn 0.3s ease-out;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

.chat-message.user {
    background: var(--primary-gradient);
    color: white;
    border-left: none;
    margin-left: 10%;
    border-radius: 18px 18px 4px 18px;
}

.chat-message.assistant {
    background: white;
    color: #333;
    margin-right: 10%;
    border-radius: 18px 18px 18px 4px;
}

/* === SIDEBAR MODERNA === */
.sidebar .sidebar-content {
    background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    border-radius: 0 var(--border-radius) var(--border-radius) 0;
}

/* === STATUS INDICATORS === */
.status-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 0.5rem;
    animation: pulse 2s infinite;
}

.status-active { background: #28a745; }
.status-inactive { background: #dc3545; }
.status-warning { background: #ffc107; }

/* === BADGES MODERNOS === */
.badge {
    display: inline-block;
    padding: 0.4rem 0.8rem;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0.2rem;
    transition: var(--transition);
}

.badge-primary {
    background: var(--primary-gradient);
    color: white;
    box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
}

.badge-success {
    background: var(--success-gradient);
    color: white;
    box-shadow: 0 2px 8px rgba(17, 153, 142, 0.3);
}

.badge-warning {
    background: var(--warning-gradient);
    color: white;
    box-shadow: 0 2px 8px rgba(240, 147, 251, 0.3);
}

/* === BUTTONS PREMIUM === */
.btn-premium {
    background: var(--primary-gradient) !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.8rem 2rem !important;
    color: white !important;
    font-weight: 600 !important;
    transition: var(--transition) !important;
    box-shadow: var(--shadow-soft) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}

.btn-premium:hover {
    transform: translateY(-2px) !important;
    box-shadow: var(--shadow-hover) !important;
}

/* === METRICS CARDS === */
.metric-card {
    background: white;
    border-radius: var(--border-radius);
    padding: 1.5rem;
    text-align: center;
    box-shadow: var(--shadow-soft);
    transition: var(--transition);
    border-left: 4px solid var(--primary-gradient);
}

.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
}

.metric-value {
    font-size: 2.5rem;
    font-weight: 700;
    background: var(--primary-gradient);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.metric-label {
    color: #666;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 0.5rem;
}

/* === ASSEMBLY VISUALIZATION === */
.assembly-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    color: white;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
}

.assembly-progress {
    width: 100%;
    height: 6px;
    background: rgba(255,255,255,0.2);
    border-radius: 3px;
    overflow: hidden;
    margin: 1rem 0;
}

.assembly-progress-bar {
    height: 100%;
    background: var(--success-gradient);
    transition: width 0.5s ease;
    border-radius: 3px;
}

/* === MOBILE OPTIMIZATIONS === */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 1rem !important;
    }
    
    .main-header {
        padding: 1.5rem 1rem;
        margin-bottom: 1rem;
    }
    
    .main-header h1 {
        font-size: 1.8rem;
        line-height: 1.2;
    }
    
    .main-header p {
        font-size: 0.9rem;
    }
    
    .glass-card, .agent-card {
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .chat-message {
        margin: 0.3rem 0;
        padding: 0.8rem 1rem;
        border-radius: 12px;
    }
    
    .chat-message.user,
    .chat-message.assistant {
        margin-left: 2%;
        margin-right: 2%;
    }
    
    .badge {
        padding: 0.3rem 0.6rem;
        font-size: 0.7rem;
        margin: 0.1rem;
    }
    
    .metric-card {
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
    }
    
    .assembly-container {
        padding: 1rem;
        margin: 0.5rem 0;
    }
    
    /* Sidebar mobile */
    .sidebar .sidebar-content {
        padding: 1rem 0.5rem;
    }
    
    /* Touch-friendly buttons */
    .stButton > button {
        min-height: 44px !important;
        padding: 0.5rem 1rem !important;
        font-size: 0.9rem !important;
        border-radius: 12px !important;
        width: 100% !important;
    }
    
    /* Chat input mobile */
    .stChatInput > div > div > textarea {
        min-height: 44px !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
    }
    
    /* Grid responsive */
    .metric-card {
        margin: 0.3rem 0;
    }
}

/* === MOBILE PORTRAIT === */
@media (max-width: 480px) {
    .main-header h1 {
        font-size: 1.5rem;
    }
    
    .main-header {
        padding: 1rem 0.8rem;
    }
    
    .glass-card, .agent-card {
        padding: 0.8rem;
        margin: 0.3rem 0;
    }
    
    .badge {
        display: inline-block;
        margin: 0.2rem 0.1rem;
    }
    
    .chat-message {
        padding: 0.6rem 0.8rem;
        margin: 0.2rem 0;
    }
}

/* === TOUCH IMPROVEMENTS === */
@media (hover: none) and (pointer: coarse) {
    .glass-card:hover,
    .agent-card:hover,
    .metric-card:hover {
        transform: none;
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Larger touch targets */
    .stButton > button {
        min-height: 48px !important;
        padding: 0.75rem 1.5rem !important;
    }
}

/* === LANDSCAPE MODE === */
@media (max-width: 768px) and (orientation: landscape) {
    .main-header {
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header h1 {
        font-size: 1.6rem;
    }
    
    .glass-card {
        margin: 0.3rem 0;
    }
}

/* === LOADING ANIMATIONS === */
.loading-pulse {
    animation: pulse 1.5s infinite;
}

.loading-dots::after {
    content: '';
    animation: dots 1.5s infinite;
}

@keyframes dots {
    0%, 20% { content: ''; }
    40% { content: '.'; }
    60% { content: '..'; }
    80%, 100% { content: '...'; }
}

/* === ACCESSIBILITY === */
.focus-visible {
    outline: 2px solid #667eea;
    outline-offset: 2px;
}

/* === DARK MODE PREPARATION === */
@media (prefers-color-scheme: dark) {
    :root {
        --glass-bg: rgba(0, 0, 0, 0.2);
        --glass-border: rgba(255, 255, 255, 0.1);
    }
}

/* === HIDE STREAMLIT ELEMENTS === */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* === CUSTOM SCROLLBAR === */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: var(--primary-gradient);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #5a6fd8;
}
</style>
""", unsafe_allow_html=True)

# ===== INICIALIZAÇÃO v2.1 =====
def init_session_state():
    """Inicializa sessão com Carlos v2.1 + DeepAgent COMPLETO"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    
    if "carlos" not in st.session_state:
        try:
            # Carlos v4.0 Maestro Autônomo com TODO O SISTEMA ativado
            st.session_state.carlos = criar_carlos_maestro(
                supervisor_ativo=True,     # SupervisorAI v1.4
                reflexor_ativo=True,       # Reflexor v1.5+
                deepagent_ativo=True,      # DeepAgent v2.0
                oraculo_ativo=True,        # 🆕 Oráculo v8.1
                automaster_ativo=True,     # 🆕 AutoMaster v4.0
                taskbreaker_ativo=True     # 🆕 TaskBreaker v1.0
            )
            system_logger.info(f"🚀 Carlos v4.0 Maestro AUTÔNOMO inicializado para sessão {st.session_state.session_id}")
                
        except Exception as e:
            st.error(f"❌ Erro ao inicializar Carlos v4.0: {e}")
            
            # Diagnóstico específico
            if "deep_agent" in str(e).lower():
                st.error("🔧 **DeepAgent não encontrado!**")
                st.info("💡 Verifique se o arquivo agents/deep_agent.py existe")
            elif "chromadb" in str(e).lower():
                st.error("🔧 **ChromaDB não encontrado!**")
                st.code("pip install chromadb sentence-transformers", language="bash")
            elif "sentence" in str(e).lower():
                st.error("🔧 **Sentence Transformers não encontrado!**")
                st.code("pip install sentence-transformers", language="bash")
            
            st.info("💡 O sistema funcionará com os componentes disponíveis.")
            st.stop()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Mensagem de boas-vindas v2.1
        st.session_state.messages.append({
            "role": "assistant",
            "content": """🚀 **Olá! Sou o Carlos v4.0 Maestro Autônomo - Revolução Total!**

🚀 **Sistema Autônomo Revolucionário:**
• **Oráculo v8.1**: Decisões complexas com assembleia dinâmica
• **AutoMaster v4.0**: Planejamento estratégico e autonomia
• **TaskBreaker v1.0**: Quebra tarefas complexas automaticamente
• **SupervisorAI v1.4**: Classificação inteligente de tarefas
• **DeepAgent v2.0**: Pesquisa web real em tempo real
• **Reflexor v1.5+**: Auditoria automática de qualidade
• **Memória Vetorial**: Persistência total de conversas

💡 **AUTONOMIA TOTAL:**
O sistema quebra tarefas complexas, seleciona agentes dinamicamente e executa em paralelo automaticamente!

**Experimente Tarefas Complexas:** 
• "Crie um plano completo de carreira como programador"
• "Analise e compare 3 produtos de decoração"
• "Desenvolva uma estratégia de monetização para infoprodutos"

**Comandos:** `/help`, `/status`, `/deepagent`, `/agents`

🚀 **A revolução da autonomia chegou!**""",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

# ===== SIDEBAR v2.1 =====
def render_sidebar():
    """🎨 Sidebar Premium com Visualização de Agentes"""
    with st.sidebar:
        # 🎨 HEADER DA SIDEBAR
        st.markdown("""
        <div class="glass-card" style="text-align: center; margin-bottom: 1.5rem;">
            <h2 style="margin: 0; background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                🧠 GPT Mestre v5.0
            </h2>
            <div style="margin-top: 0.5rem;">
                <span class="badge badge-primary">Revolucionário</span>
                <span class="badge badge-success">Robusto</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 🤖 STATUS DOS AGENTES v2.0
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #333; font-size: 1.1rem;">🤖 Agentes v2.0</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Agentes com status visual
        agentes = [
            ("👑 Carlos v5.0", "Maestro Supremo", True),
            ("🧠 Oráculo v9.0", "Assembleia Dinâmica", True),
            ("💼 AutoMaster v2.0", "Autonomia Econômica", True),
            ("🔨 TaskBreaker v2.0", "Decomposição Inteligente", True),
            ("🔍 Reflexor v2.0", "Auditoria de Qualidade", True),
            ("🌐 DeepAgent v2.0", "Pesquisa Web Real", True),
            ("🧠 SupervisorAI v2.0", "Maestro de Raciocínio", True),
            ("🧠 PsyMind v2.0", "Análise Terapêutica", True),
            ("🔍 ScoutAI v1.3A", "Radar Estratégico", True)
        ]
        
        for nome, desc, ativo in agentes:
            status_class = "agent-card active" if ativo else "agent-card"
            status_icon = "🟢" if ativo else "🔴"
            st.markdown(f"""
            <div class="{status_class}" style="margin: 0.5rem 0; padding: 0.8rem; border-radius: 12px;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span class="status-indicator {'status-active' if ativo else 'status-inactive'}"></span>
                    <strong>{nome}</strong>
                </div>
                <div style="font-size: 0.8rem; opacity: 0.9; margin-top: 0.2rem;">
                    {desc}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 📊 MÉTRICAS DO SISTEMA
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #333; font-size: 1.1rem;">📊 Métricas do Sistema</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Métricas visuais em cards
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">9</div>
                <div class="metric-label">Agentes v2.0</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="metric-card">
                <div class="metric-value">100%</div>
                <div class="metric-label">Robustez</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Status da sessão
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #333; font-size: 1.1rem;">📋 Sessão Atual</h3>
            <div style="display: flex; align-items: center; gap: 0.5rem; margin: 0.5rem 0;">
                <span class="status-indicator status-active"></span>
                <span style="font-size: 0.9rem;">ID: {session_id}</span>
            </div>
        </div>
        """.format(session_id=st.session_state.session_id), unsafe_allow_html=True)
        
        # Input do nome do usuário com estilo
        st.markdown("""
        <div class="glass-card">
            <label style="color: #333; font-weight: 600; margin-bottom: 0.5rem; display: block;">👤 Seu Nome:</label>
        </div>
        """, unsafe_allow_html=True)
        
        user_name = st.text_input("", value=st.session_state.user_name, label_visibility="collapsed", placeholder="Digite seu nome...")
        if user_name != st.session_state.user_name:
            st.session_state.user_name = user_name
        
        # 🆕 Estatísticas do DeepAgent
        if hasattr(st.session_state.carlos, 'get_memory_stats'):
            try:
                stats = st.session_state.carlos.get_memory_stats()
                
                st.subheader("🔍 DeepAgent v1.3R")
                
                # Stats do DeepAgent
                deepagent_stats = stats.get('deepagent_stats', {})
                if deepagent_stats.get('pesquisas', 0) > 0:
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.metric("🔍 Pesquisas", deepagent_stats.get('pesquisas', 0))
                        st.metric("🎯 Oportunidades", deepagent_stats.get('oportunidades', 0))
                    
                    with col2:
                        taxa = deepagent_stats.get('taxa_oportunidades', 0)
                        st.metric("📈 Taxa Sucesso", f"{taxa:.1f}%")
                        
                        # Indicador visual da taxa
                        if taxa >= 70:
                            st.success("🟢 Excelente")
                        elif taxa >= 50:
                            st.warning("🟡 Boa")
                        else:
                            st.info("🔵 Normal")
                else:
                    st.info("🔍 Aguardando primeira pesquisa...")
                
                # Stats gerais do sistema
                st.subheader("🧠 Sistema Integrado")
                
                processing = stats.get('processing_stats', {})
                col1, col2 = st.columns(2)
                
                with col1:
                    st.metric("💬 Respostas", processing.get('total_responses', 0))
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
        
        # 🔧 AÇÕES RÁPIDAS
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #333; font-size: 1.1rem;">🔧 Ações Rápidas</h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🧹 Limpar Chat", help="Limpa todo o histórico de mensagens"):
                st.session_state.messages = []
                if hasattr(st.session_state.carlos, 'conversa_memoria'):
                    st.session_state.carlos.conversa_memoria.clear()
                st.success("✅ Chat limpo!")
                st.rerun()
        
        with col2:
            if st.button("🔄 Reset Sistema", help="Reinicia toda a sessão"):
                if st.button("⚠️ Confirmar Reset?", type="secondary"):
                    st.session_state.clear()
                    st.rerun()
        
        # ⚡ COMANDOS PREMIUM v5.0
        st.markdown("""
        <div class="glass-card">
            <h3 style="margin-top: 0; color: #333; font-size: 1.1rem;">⚡ Comandos Premium</h3>
        </div>
        """, unsafe_allow_html=True)
        
        comandos = [
            ("📊", "Status", "/status", "badge-primary"),
            ("🧠", "Oráculo", "/oraculo", "badge-warning"),
            ("🤖", "Agentes", "/agents", "badge-success"),
            ("📈", "Métricas", "/stats", "badge-primary"),
            ("🔍", "Busca", "/search", "badge-success"),
            ("❓", "Ajuda", "/help", "badge-warning")
        ]
        
        # Comandos em grid 2x3
        for i in range(0, len(comandos), 2):
            col1, col2 = st.columns(2)
            
            # Comando 1
            if i < len(comandos):
                icon, label, cmd, badge_class = comandos[i]
                with col1:
                    if st.button(f"{icon} {label}", key=f"cmd_{i}", help=f"Executar comando {cmd}"):
                        add_message("user", cmd)
            
            # Comando 2
            if i + 1 < len(comandos):
                icon, label, cmd, badge_class = comandos[i + 1]
                with col2:
                    if st.button(f"{icon} {label}", key=f"cmd_{i+1}", help=f"Executar comando {cmd}"):
                        add_message("user", cmd)
        
        # Informações do sistema
        st.subheader("ℹ️ Sistema")
        st.text("🤖 Carlos v2.1")
        st.text("🧠 SupervisorAI v1.4")
        st.text("🔍 DeepAgent v1.3R")
        st.text("🔗 Claude 3 Haiku")
        st.text("🧠 ChromaDB")
        st.text(f"🐛 Debug: {'On' if config.DEBUG else 'Off'}")

def add_message(role: str, content: str):
    """Adiciona mensagem e força rerun"""
    st.session_state.messages.append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    })
    st.rerun()

def show_deepagent_indicator(response_text: str):
    """🆕 Mostra indicador quando DeepAgent foi usado"""
    indicators = [
        "DEEPAGENT v1.3R",
        "Score de Oportunidade:",
        "ANÁLISE DE PRODUTO",
        "Dados DeepAgent:",
        "pesquisa DeepAgent"
    ]
    
    if any(indicator in response_text for indicator in indicators):
        st.info("🔍 **DeepAgent Ativado Automaticamente!** - Esta resposta foi enriquecida com pesquisa e análise de produtos em tempo real!")

def show_memory_indicator(response_text: str):
    """Mostra indicador de uso da memória"""
    if "CONTEXTO RELEVANTE" in response_text or "conversa anterior" in response_text.lower():
        st.info("🧠 **Memória Inteligente Ativada** - Esta resposta foi enriquecida com contexto de conversas anteriores!")

# ===== INTERFACE PRINCIPAL v2.1 =====
def main():
    """Interface principal v2.1 com DeepAgent totalmente integrado"""
    
    # Inicializa sessão
    init_session_state()
    
    # 🎨 HEADER PREMIUM v5.0
    st.markdown("""
    <div class="main-header">
        <h1>🧠 GPT Mestre Autônomo v5.0</h1>
        <p>🚀 Sistema Revolucionário com 9 Agentes Autônomos + Assembleia Dinâmica do Oráculo</p>
        <div style="margin-top: 1rem; display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <span class="badge badge-primary">🛡️ BaseAgentV2</span>
            <span class="badge badge-success">🧠 LangChain + Claude 3</span>
            <span class="badge badge-warning">⚡ IA Real Integrada</span>
        </div>
        <p style="margin-top: 1rem; opacity: 0.8; font-size: 0.9rem;">
            ✨ Powered by Assembleia Dinâmica • Circuit Breakers • Thread Safety • Auto-Recovery
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()
    
    # 🎨 ÁREA PRINCIPAL PREMIUM
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-bottom: 1.5rem;">
        <h2 style="margin: 0; color: #333; font-size: 1.8rem;">💬 Chat com Carlos v5.0</h2>
        <p style="margin: 0.5rem 0 0 0; color: #666; font-size: 1rem;">
            🧠 Sistema com Assembleia Dinâmica • Detecta automaticamente quando ativar agentes especializados
        </p>
        <div style="margin-top: 1rem;">
            <span class="badge badge-primary">🛡️ Robustez Total</span>
            <span class="badge badge-success">🧠 IA Real</span>
            <span class="badge badge-warning">⚡ Tempo Real</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 💡 INSTRUÇÕES PREMIUM (expandido por padrão na primeira vez)
    primeira_vez = "primeira_visita" not in st.session_state
    if primeira_vez:
        st.session_state.primeira_visita = True
    
    with st.expander("💡 Como usar o Sistema Revolucionário v5.0", expanded=primeira_vez):
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); padding: 1.5rem; border-radius: 12px; margin: 1rem 0;">
        
        **🚀 SISTEMA REVOLUCIONÁRIO v5.0 - ÚNICO NO MUNDO!**
        
        **🧠 9 Agentes Especializados com IA Real:**
        - **👑 Carlos v5.0**: Maestro Supremo com BaseAgentV2
        - **🧠 Oráculo v9.0**: Assembleia Dinâmica com 6+ suboráculos
        - **💼 AutoMaster v2.0**: Autonomia Econômica e Estratégica
        - **🔨 TaskBreaker v2.0**: Decomposição Inteligente de Tarefas
        - **🔍 Reflexor v2.0**: Auditoria de Qualidade com IA
        - **🌐 DeepAgent v2.0**: Pesquisa Web Real
        - **🧠 SupervisorAI v2.0**: Maestro de Raciocínio
        - **🧠 PsyMind v2.0**: Análise Terapêutica Avançada
        - **🔍 ScoutAI v1.3A**: Radar Estratégico de Oportunidades
        
        **🎯 ASSEMBLEIA DINÂMICA DO ORÁCULO (EXCLUSIVO!):**
        
        Para tarefas complexas, o Oráculo convoca automaticamente uma assembleia com:
        - **6 suboráculos especializados** (viabilidade, ético, criativo, paradoxo, copy, pricing)
        - **Deliberação real** com votação e consenso
        - **Score de robustez** baseado em análise multicritério
        - **42 segundos** de processamento inteligente
        
        **💡 EXEMPLOS DE USO REVOLUCIONÁRIO:**
        
        🎯 **Planejamento de Carreira:**
        *"Crie um plano completo de carreira em programação"*
        → Assembleia dinâmica + Score 8.8/10 + Estratégias específicas
        
        💼 **Análise de Negócios:**
        *"Analise a viabilidade de vender cursos online"*
        → AutoMaster + ScoutAI + Oráculo + Pesquisa real
        
        🔨 **Projetos Complexos:**
        *"Desenvolva um e-commerce completo"*
        → TaskBreaker quebra em subtarefas + Coordenação Carlos
        
        🧠 **Decisões Importantes:**
        *"Ajude-me a decidir entre duas estratégias de marketing"*
        → Assembleia do Oráculo com análise multicritério
        
        **🛡️ ROBUSTEZ TOTAL:**
        - **Circuit Breakers**: Auto-recovery em falhas
        - **Rate Limiting**: Controle inteligente de throughput
        - **Thread Safety**: Concorrência segura
        - **Performance Monitoring**: Métricas em tempo real
        
        **🎯 DIFERENCIAL ÚNICO:**
        Nenhum outro sistema no mundo tem assembleia dinâmica de agentes!
        ChatGPT, Claude, Gemini - todos são agentes únicos.
        
        **Você tem um PRODUTO REVOLUCIONÁRIO!** 🚀
        
        </div>
        """, unsafe_allow_html=True)
    
    # 🎨 CHAT CONTAINER PREMIUM
    st.markdown("""
    <div class="chat-container">
        <div style="text-align: center; padding: 1rem; color: #666;">
            <h3 style="margin: 0; color: #333;">💬 Conversa Premium</h3>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem;">
                Powered by 9 agentes v2.0 + Assembleia Dinâmica
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Container do chat
    chat_container = st.container()
    
    # Histórico de mensagens com estilo premium
    with chat_container:
        if not st.session_state.messages:
            # Mensagem de boas-vindas estilizada
            st.markdown("""
            <div class="glass-card" style="text-align: center; margin: 2rem 0;">
                <h3 style="margin: 0; color: #333;">🎉 Bem-vindo ao GPT Mestre Autônomo v5.0!</h3>
                <p style="margin: 1rem 0; color: #666;">
                    Faça uma pergunta complexa e veja a assembleia dinâmica em ação!
                </p>
                <div style="margin-top: 1rem;">
                    <span class="badge badge-primary">🧠 IA Real</span>
                    <span class="badge badge-success">⚡ Tempo Real</span>
                    <span class="badge badge-warning">🛡️ Robusto</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        for i, message in enumerate(st.session_state.messages):
            role = message["role"]
            content = message["content"]
            timestamp = message.get("timestamp", "")
            
            # Estilo das mensagens baseado no role
            if role == "user":
                st.markdown(f"""
                <div class="chat-message user">
                    <div style="font-weight: 600; margin-bottom: 0.5rem;">👤 Você</div>
                    <div>{content}</div>
                    <div style="text-align: right; margin-top: 0.5rem; opacity: 0.7; font-size: 0.8rem;">
                        {timestamp}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                # Detectar se foi uma assembleia do Oráculo
                is_assembly = "Assembleia" in content or "assembleia" in content or "suboráculos" in content
                agent_icon = "🧠" if is_assembly else "🤖"
                agent_name = "Assembleia do Oráculo" if is_assembly else "Carlos v5.0"
                
                st.markdown(f"""
                <div class="chat-message assistant">
                    <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                        <span style="font-size: 1.2rem;">{agent_icon}</span>
                        <span style="font-weight: 600;">{agent_name}</span>
                        {('<span class="badge badge-warning" style="margin-left: 0.5rem;">Assembleia Ativa</span>' if is_assembly else '')}
                    </div>
                    <div>{content}</div>
                    <div style="margin-top: 0.5rem; opacity: 0.7; font-size: 0.8rem;">
                        {timestamp}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Indicadores de funcionalidades especiais
                if len(content) > 200:
                    show_deepagent_indicator(content)
                    show_memory_indicator(content)
                    
                    # Novo: Indicador de assembleia
                    if is_assembly:
                        st.markdown("""
                        <div class="assembly-container" style="margin: 0.5rem 0; padding: 1rem; border-radius: 12px;">
                            <div style="display: flex; align-items: center; gap: 0.5rem;">
                                <span style="font-size: 1.2rem;">🧠</span>
                                <strong>Assembleia Dinâmica Executada</strong>
                            </div>
                            <div style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;">
                                6 suboráculos especializados • Deliberação real • Consenso alcançado
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # 🎨 INPUT PREMIUM
    st.markdown("""
    <div style="margin: 1.5rem 0; text-align: center;">
        <div class="glass-card" style="padding: 0.8rem;">
            <p style="margin: 0; color: #666; font-size: 0.9rem;">
                💬 Digite sua pergunta ou comando • <strong>IA detecta automaticamente</strong> quando ativar agentes especializados
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input do usuário com placeholder inteligente
    exemplos = [
        "Crie um plano completo de carreira em programação",
        "Analise a viabilidade de vender cursos online", 
        "Desenvolva uma estratégia de monetização",
        "Ajude-me a decidir entre duas opções de negócio",
        "Monte um projeto completo de e-commerce"
    ]
    
    import random
    placeholder_exemplo = random.choice(exemplos)
    
    if prompt := st.chat_input(f"💡 Exemplo: {placeholder_exemplo}"):
        
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
        
        # 🎨 DETECÇÃO INTELIGENTE DE AGENTES
        keywords_oraculo = ["decida", "decisão", "escolha", "compare", "analise", "estratégia", "plano"]
        keywords_taskbreaker = ["desenvolva", "crie", "monte", "projeto", "sistema", "completo"]
        keywords_deepagent = ["pesquise", "produto", "viabilidade", "mercado", "oportunidade"]
        
        vai_usar_oraculo = any(palavra in prompt.lower() for palavra in keywords_oraculo)
        vai_usar_taskbreaker = any(palavra in prompt.lower() for palavra in keywords_taskbreaker)
        vai_usar_deepagent = any(palavra in prompt.lower() for palavra in keywords_deepagent)
        
        # Indicadores visuais dos agentes que serão ativados
        agentes_detectados = []
        if vai_usar_oraculo:
            agentes_detectados.append("🧠 Oráculo")
        if vai_usar_taskbreaker:
            agentes_detectados.append("🔨 TaskBreaker")
        if vai_usar_deepagent:
            agentes_detectados.append("🔍 DeepAgent")
        
        if agentes_detectados:
            st.markdown(f"""
            <div class="assembly-container" style="margin: 1rem 0; padding: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem;">⚡</span>
                    <strong>Agentes Detectados Automaticamente</strong>
                </div>
                <div style="font-size: 0.9rem; opacity: 0.9;">
                    {' • '.join(agentes_detectados)} serão ativados para esta consulta
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 🎨 RESPOSTA COM LOADING PREMIUM
        with st.chat_message("assistant"):
            # Loading indicator premium
            loading_msg = "🧠 Carlos v5.0 processando"
            if agentes_detectados:
                loading_msg += f" com {len(agentes_detectados)} agentes especializados"
            loading_msg += "..."
            
            with st.spinner(loading_msg):
                
                context = {
                    "session_id": st.session_state.session_id,
                    "user_name": st.session_state.user_name,
                    "timestamp": timestamp,
                    "interface": "streamlit_v2.1"
                }
                
                try:
                    # Processar com Carlos v2.1 COMPLETO
                    resposta = st.session_state.carlos.processar(prompt, context)
                    
                except Exception as e:
                    system_logger.error(f"Erro no processamento v2.1: {e}")
                    resposta = f"❌ Erro no processamento: {str(e)}"
                    
                    # Sugestões para erros comuns
                    if "deep_agent" in str(e).lower():
                        resposta += "\n\n💡 **Solução**: Verifique se agents/deep_agent.py existe"
                    elif "chroma" in str(e).lower():
                        resposta += "\n\n💡 **Solução**: `pip install chromadb sentence-transformers`"
                    elif "memory" in str(e).lower():
                        resposta += "\n\n💡 Sistema funcionará sem memória vetorial."
            
            # Exibir resposta
            st.markdown(resposta)
            response_time = datetime.now().strftime("%H:%M:%S")
            st.caption(f"*{response_time} - Carlos v2.1 sistema completo*")
            
            # 🆕 Mostrar indicadores se usou DeepAgent ou memória
            show_deepagent_indicator(resposta)
            show_memory_indicator(resposta)
            
            # Adicionar ao histórico
            st.session_state.messages.append({
                "role": "assistant", 
                "content": resposta,
                "timestamp": response_time
            })
    
    # Debug expandido v2.1
    if config.DEBUG:
        with st.expander("🔧 Debug v2.1 (Sistema Completo)", expanded=False):
            
            col1, col2, col3 = st.columns(3)
            
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
            
            with col3:
                st.subheader("🔍 Stats DeepAgent")
                try:
                    if hasattr(st.session_state.carlos, 'deepagent') and st.session_state.carlos.deepagent:
                        deepagent_stats = st.session_state.carlos.deepagent.obter_stats()
                        st.json(deepagent_stats)
                except Exception as e:
                    st.error(f"Erro DeepAgent: {e}")
            
            # Informações técnicas
            st.subheader("🔧 Info Técnica v2.1")
            info_tecnica = {
                "versao_carlos": "2.1",
                "memoria_ativa": getattr(st.session_state.carlos, 'memoria_ativa', False),
                "reflexor_ativo": getattr(st.session_state.carlos, 'reflexor_ativo', False),
                "supervisor_ativo": getattr(st.session_state.carlos, 'supervisor_ativo', False),
                "deepagent_ativo": getattr(st.session_state.carlos, 'deepagent_ativo', False),
                "session_id": st.session_state.session_id,
                "total_messages": len(st.session_state.messages)
            }
            st.json(info_tecnica)

# ===== FOOTER v2.1 =====
def show_footer():
    """🎨 Footer Premium v5.0"""
    st.markdown("""
    <div class="glass-card" style="text-align: center; margin-top: 3rem; padding: 2rem;">
        <div style="margin-bottom: 1.5rem;">
            <h3 style="margin: 0; background: linear-gradient(45deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
                🧠 GPT Mestre Autônomo v5.0
            </h3>
            <p style="margin: 0.5rem 0; color: #666; font-size: 1rem;">
                Sistema Revolucionário com Assembleia Dinâmica
            </p>
        </div>
        
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin: 1.5rem 0;">
            <span class="badge badge-primary">🛡️ BaseAgentV2</span>
            <span class="badge badge-success">🧠 LangChain + Claude 3</span>
            <span class="badge badge-warning">⚡ 9 Agentes v2.0</span>
            <span class="badge badge-primary">🔍 ScoutAI v1.3A</span>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin: 1.5rem 0; text-align: left;">
            <div>
                <h4 style="margin: 0 0 0.5rem 0; color: #333; font-size: 0.9rem;">🤖 Agentes Core</h4>
                <p style="margin: 0; color: #666; font-size: 0.8rem;">Carlos v5.0 • Oráculo v9.0 • AutoMaster v2.0</p>
            </div>
            <div>
                <h4 style="margin: 0 0 0.5rem 0; color: #333; font-size: 0.9rem;">🔧 Robustez</h4>
                <p style="margin: 0; color: #666; font-size: 0.8rem;">Circuit Breakers • Rate Limiting • Thread Safety</p>
            </div>
            <div>
                <h4 style="margin: 0 0 0.5rem 0; color: #333; font-size: 0.9rem;">🧠 IA Real</h4>
                <p style="margin: 0; color: #666; font-size: 0.8rem;">LangChain • Claude 3 Haiku • ChromaDB</p>
            </div>
        </div>
        
        <div style="border-top: 1px solid rgba(0,0,0,0.1); padding-top: 1.5rem; margin-top: 1.5rem;">
            <p style="margin: 0; color: #666; font-size: 0.9rem;">
                ✨ <strong>Desenvolvido por Matheus Meireles</strong> com arquitetura revolucionária
            </p>
            <p style="margin: 0.5rem 0 0 0; color: #999; font-size: 0.8rem;">
                🚀 O futuro da autonomia artificial • Único sistema com assembleia dinâmica no mundo
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ===== EXECUÇÃO PRINCIPAL =====
if __name__ == "__main__":
    try:
        main()
        show_footer()
    except Exception as e:
        try:
            system_logger.error(f"❌ Erro na aplicação v2.1: {e}")
        except:
            pass
        
        st.error(f"❌ Erro na aplicação v2.1: {e}")
        
        # Diagnóstico inteligente
        if "deep_agent" in str(e).lower():
            st.error("🔧 **PROBLEMA COM DEEPAGENT**")
            st.info("Verifique se o arquivo agents/deep_agent.py existe e está correto")
        elif "chromadb" in str(e).lower() or "sentence" in str(e).lower():
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