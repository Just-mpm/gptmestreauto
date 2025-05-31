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

# Configuração da página
st.set_page_config(
    page_title="GPT Mestre Autônomo v2.1 - Sistema Completo com DeepAgent",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== IMPORTS ATUALIZADOS PARA v2.1 =====
try:
    from config import config
    from agents.carlos import criar_carlos_integrado  # Carlos v2.1 com DeepAgent
    from utils.logger import get_logger
    
    system_logger = get_logger("streamlit")
    
except ImportError as e:
    st.error(f"❌ Erro ao importar módulos: {e}")
    st.error("📦 Instale as dependências da Fase 2 + DeepAgent:")
    st.code("pip install chromadb sentence-transformers", language="bash")
    st.stop()

# CSS atualizado com tema DeepAgent
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

.deepagent-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    color: white;
}

.pesquisa-ativa {
    background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
    border-radius: 8px;
    padding: 0.8rem;
    margin: 0.5rem 0;
    color: white;
    font-weight: bold;
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
.deepagent-active { color: #17a2b8; font-weight: bold; }

.version-badge {
    background: #007bff;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}

.deepagent-badge {
    background: #17a2b8;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
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
            # Carlos v2.1 com TODO O SISTEMA ativado
            st.session_state.carlos = criar_carlos_integrado(
                supervisor_ativo=True,   # SupervisorAI v1.4
                reflexor_ativo=True,     # Reflexor v1.5+
                deepagent_ativo=True     # 🆕 DeepAgent v1.3R
            )
            system_logger.info(f"🔍 Carlos v2.1 COMPLETO inicializado para sessão {st.session_state.session_id}")
                
        except Exception as e:
            st.error(f"❌ Erro ao inicializar Carlos v2.1: {e}")
            
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
            "content": """🔍 **Olá! Sou o Carlos v2.1 com DeepAgent Integrado!**

🚀 **Sistema Completo Ativo:**
• **SupervisorAI v1.4**: Classifica tarefas automaticamente
• **DeepAgent v1.3R**: Pesquisa e análise de produtos 🆕  
• **Memória Vetorial**: Lembro de TODAS as nossas conversas
• **Reflexor v1.5+**: Auditoria automática de qualidade
• **Detecção Inteligente**: Ativo o DeepAgent automaticamente!

💬 **Como funciona a detecção automática:**
Quando você menciona produtos, análises ou pesquisas, o sistema detecta automaticamente e ativa o DeepAgent para dar respostas mais completas!

**Experimente:** 
• "Analise patinhos decorativos" 
• "Este produto tem potencial?"
• "Pesquise viabilidade de produtos de casa"

**Comandos:** `/help`, `/status`, `/deepagent`, `/agents`

🎯 **O sistema mais inteligente até agora!**""",
            "timestamp": datetime.now().strftime("%H:%M:%S")
        })
    
    if "user_name" not in st.session_state:
        st.session_state.user_name = ""

# ===== SIDEBAR v2.1 =====
def render_sidebar():
    """Sidebar atualizada com DeepAgent integrado"""
    with st.sidebar:
        st.header("🔍 GPT Mestre v2.1")
        st.markdown('<span class="version-badge">SISTEMA COMPLETO</span> <span class="deepagent-badge">DEEPAGENT</span>', unsafe_allow_html=True)
        
        # Status do sistema
        st.subheader("📊 Status do Sistema")
        st.markdown("**Carlos:** <span class='agent-active'>v2.1 ativo</span>", unsafe_allow_html=True)
        st.markdown("**SupervisorAI:** <span class='agent-active'>✅ v1.4</span>", unsafe_allow_html=True)
        st.markdown("**Reflexor:** <span class='agent-active'>✅ v1.5+</span>", unsafe_allow_html=True)
        
        # 🆕 Status do DeepAgent
        if hasattr(st.session_state.carlos, 'deepagent_ativo'):
            if st.session_state.carlos.deepagent_ativo:
                st.markdown("**DeepAgent:** <span class='deepagent-active'>🔍 v1.3R Ativo</span>", unsafe_allow_html=True)
            else:
                st.markdown("**DeepAgent:** <span class='agent-inactive'>❌ Inativo</span>", unsafe_allow_html=True)
        
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
        
        # 🆕 Comandos rápidos v2.1 com DeepAgent
        st.subheader("⚡ Comandos v2.1")
        
        comandos = [
            ("📊", "Status", "/status"),
            ("🔍", "DeepAgent", "/deepagent"),
            ("🧠", "Memória", "/memory"),
            ("🤖", "Agentes", "/agents"),
            ("📈", "Stats", "/stats"),
            ("❓", "Ajuda", "/help")
        ]
        
        col1, col2 = st.columns(2)
        for i, (icon, label, cmd) in enumerate(comandos):
            col = col1 if i % 2 == 0 else col2
            with col:
                if st.button(f"{icon} {label}"):
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
    
    # Header v2.1
    st.markdown("""
    <div class="main-header">
        <h1>🔍 GPT Mestre Autônomo v2.1</h1>
        <p>Sistema Completo com DeepAgent • Pesquisa Automática • Análise Inteligente</p>
        <small>✨ Powered by SupervisorAI v1.4 + DeepAgent v1.3R + ChromaDB + Claude 3</small>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    render_sidebar()
    
    # Área principal
    st.header("💬 Conversa com Carlos v2.1")
    st.caption("🔍 Sistema com DeepAgent integrado - Detecta automaticamente quando precisa pesquisar!")
    
    # Instruções v2.1
    with st.expander("💡 Como usar o Sistema Completo v2.1", expanded=False):
        st.markdown("""
        **🔍 NOVIDADE: DeepAgent Integrado!**
        
        **🧠 Sistema Completo v2.1:**
        - **SupervisorAI v1.4**: Classifica tarefas e detecta quando usar DeepAgent
        - **DeepAgent v1.3R**: Pesquisa e análise automática de produtos
        - **Memória Vetorial**: Lembro de TODAS as conversas
        - **Reflexor v1.5+**: Auditoria e melhoria contínua
        
        **🔍 Detecção Automática do DeepAgent:**
        O sistema detecta automaticamente quando você quer:
        - Analisar produtos
        - Pesquisar viabilidade
        - Investigar mercado
        - Calcular score de oportunidade
        
        **💡 Exemplos de Ativação Automática:**
        - *"Analise patinhos decorativos"* → DeepAgent + Modo profundo
        - *"Este produto tem potencial?"* → DeepAgent + Análise automática
        - *"Pesquise viabilidade de produtos de casa"* → DeepAgent ativo
        - *"Como está o mercado de decoração?"* → DeepAgent + SupervisorAI
        
        **🎯 Fluxo Inteligente:**
        1. Você faz uma pergunta
        2. SupervisorAI detecta se precisa de pesquisa
        3. DeepAgent é ativado automaticamente (se necessário)
        4. Sistema busca contexto na memória
        5. Resposta integrada com todos os dados
        6. Reflexor audita e melhora
        7. Tudo salvo na memória permanente
        
        **📚 Sistema Verdadeiramente Inteligente:**
        - Não precisa pedir para ativar o DeepAgent
        - Detecção automática por palavras-chave
        - Integração perfeita entre todos os agentes
        - Respostas sempre contextualizadas
        
        **💾 Persistência Total:**
        - Todas as pesquisas ficam salvas
        - Análises anteriores são reutilizadas
        - Conhecimento cresce automaticamente
        - Funciona offline (ChromaDB local)
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
                
                # 🆕 Indicador de DeepAgent para respostas do assistente
                if message["role"] == "assistant" and len(message["content"]) > 200:
                    show_deepagent_indicator(message["content"])
                    show_memory_indicator(message["content"])
    
    # Input do usuário
    if prompt := st.chat_input("💬 Converse comigo... Pesquiso automaticamente quando necessário! 🔍"):
        
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
        
        # 🆕 Detectar se vai usar DeepAgent (preview para usuário)
        vai_usar_deepagent = any(palavra in prompt.lower() for palavra in [
            "analise", "pesquise", "produto", "viabilidade", "mercado", "oportunidade"
        ])
        
        # Resposta do Carlos v2.1
        with st.chat_message("assistant"):
            with st.spinner("🧠 Carlos v2.1 processando..." + (" (🔍 DeepAgent detectado!)" if vai_usar_deepagent else "")):
                
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
    """Footer atualizado para v2.1 com DeepAgent"""
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <p>🔍 <strong>GPT Mestre Autônomo v2.1</strong> | Desenvolvido por Matheus Meireles</p>
            <p>✨ Sistema Completo • SupervisorAI v1.4 • DeepAgent v1.3R • ChromaDB • Claude 3</p>
            <p>🤖 Carlos v2.1 • 🧠 SupervisorAI • 🔍 DeepAgent • 🔍 Reflexor v1.5+ • 💾 Memória Permanente</p>
            <p><small>🚀 Fase 2+ Concluída - Sistema Inteligente com Pesquisa Automática</small></p>
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