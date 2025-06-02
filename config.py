"""
GPT MESTRE AUTÔNOMO - Configurações do Sistema
Versão: 3.0 - Com suporte para Google Gemini 2.5 Flash
Autor: Matheus Meireles
"""

import os
from pathlib import Path

# Tentar carregar dotenv, mas não falhar se não estiver disponível
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️ python-dotenv não instalado. Usando variáveis de ambiente do sistema.")

class Config:
    """Configurações centralizadas do sistema"""
    
    # === CONFIGURAÇÕES BÁSICAS ===
    PROJECT_NAME = "GPT Mestre Autônomo"
    VERSION = "3.0"  # 🆕 Versão com Google Gemini
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # === DIRETÓRIOS ===
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    MEMORY_DIR = BASE_DIR / "memory"
    AGENTS_DIR = BASE_DIR / "agents"
    
    # Cria diretórios se não existirem
    for dir_path in [LOGS_DIR, MEMORY_DIR, AGENTS_DIR]:
        dir_path.mkdir(exist_ok=True)
    
    # === CONFIGURAÇÃO DO LLM PROVIDER ===
    # Escolha o provider: "gemini" ou "anthropic"
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    # === API KEYS ===
    # Google Gemini (novo padrão) - sempre usar variável de ambiente
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY and LLM_PROVIDER == "gemini":
        print("⚠️ GOOGLE_API_KEY não configurada! Configure no arquivo .env")
        GOOGLE_API_KEY = None
    
    # Anthropic (mantido para compatibilidade)
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # Validação de API Key baseada no provider
    if LLM_PROVIDER == "gemini":
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY não encontrada! Configure no arquivo .env")
    elif LLM_PROVIDER == "anthropic":
        if not ANTHROPIC_API_KEY:
            raise ValueError("ANTHROPIC_API_KEY não encontrada! Configure no arquivo .env")
    else:
        raise ValueError(f"LLM_PROVIDER inválido: {LLM_PROVIDER}. Use 'gemini' ou 'anthropic'")
    
    # === CONFIGURAÇÕES DO LLM ===
    if LLM_PROVIDER == "gemini":
        # Configurações do Google Gemini 2.5 Flash
        DEFAULT_MODEL = "models/gemini-2.5-flash-preview-05-20"
        MAX_TOKENS = 8192  # Gemini suporta até 8K tokens
        TEMPERATURE = 0.7
        TOP_P = 0.95
        TOP_K = 40
    else:
        # Configurações do Anthropic Claude (compatibilidade)
        DEFAULT_MODEL = "claude-3-5-haiku-20241022"
        MAX_TOKENS = 4000
        TEMPERATURE = 0.7
        TOP_P = None  # Anthropic não usa top_p
        TOP_K = None  # Anthropic não usa top_k
    
    # 🆕 === CONFIGURAÇÕES ESPECÍFICAS DO GEMINI ===
    GEMINI_SAFETY_SETTINGS = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_ONLY_HIGH"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_ONLY_HIGH"
        }
    ]
    
    # === CONFIGURAÇÕES DE WEB SEARCH ===
    WEB_SEARCH_ENABLED = True
    WEB_SEARCH_MAX_USES = 3  # Máximo de buscas por resposta
    WEB_SEARCH_TIMEOUT = 30  # Timeout em segundos
    
    # Domínios permitidos para busca (opcional)
    WEB_SEARCH_ALLOWED_DOMAINS = [
        "shopee.com.br",
        "mercadolivre.com.br", 
        "magazineluiza.com.br",
        "aliexpress.com",
        "amazon.com.br",
        "olx.com.br",
        "google.com",
        "wikipedia.org",
        "g1.globo.com",
        "estadao.com.br",
        "folha.uol.com.br"
    ]
    
    # Domínios bloqueados (opcional)
    WEB_SEARCH_BLOCKED_DOMAINS = [
        "sites-maliciosos.com",
        "spam-sites.com"
    ]
    
    # === INTEGRAÇÕES (Para fases futuras) ===
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    GOOGLE_SHEETS_CREDENTIALS = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    
    # === CONFIGURAÇÕES DA MEMÓRIA VETORIAL ===
    CHROMA_PERSIST_DIR = str(MEMORY_DIR / "chroma_db")
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    
    # === CONFIGURAÇÕES DOS AGENTES ===
    AGENTES_ATIVOS = [
        "carlos",      # Interface principal
        "reflexor",    # Auditor interno
        "deepagent",   # Com web search real!
        "supervisor",  # Classificador inteligente
    ]
    
    # === CONFIGURAÇÕES DO STREAMLIT ===
    STREAMLIT_CONFIG = {
        "page_title": PROJECT_NAME,
        "page_icon": "🤖",  # Ícone atualizado para IA
        "layout": "wide",
        "initial_sidebar_state": "expanded"
    }
    
    # === CONFIGURAÇÕES DE LOGGING ===
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    
    # === CONFIGURAÇÕES DO FASTAPI ===
    API_HOST = "127.0.0.1"
    API_PORT = 8000
    API_RELOAD = DEBUG

# Instância global de configuração
config = Config()

# Função para validar configuração
def validate_config():
    """Valida se todas as configurações necessárias estão presentes"""
    errors = []
    
    if config.LLM_PROVIDER == "gemini":
        if not config.GOOGLE_API_KEY:
            errors.append("GOOGLE_API_KEY não configurada")
    elif config.LLM_PROVIDER == "anthropic":
        if not config.ANTHROPIC_API_KEY:
            errors.append("ANTHROPIC_API_KEY não configurada")
    
    # Validar configurações de web search
    if config.WEB_SEARCH_ENABLED:
        if config.WEB_SEARCH_MAX_USES < 1 or config.WEB_SEARCH_MAX_USES > 10:
            errors.append("WEB_SEARCH_MAX_USES deve estar entre 1 e 10")
        
        if config.WEB_SEARCH_TIMEOUT < 5 or config.WEB_SEARCH_TIMEOUT > 60:
            errors.append("WEB_SEARCH_TIMEOUT deve estar entre 5 e 60 segundos")
    
    if errors:
        raise ValueError(f"Configuração inválida: {', '.join(errors)}")
    
    return True

if __name__ == "__main__":
    validate_config()
    print(f"✅ Configuração do {config.PROJECT_NAME} v{config.VERSION} validada com sucesso!")
    print(f"🤖 LLM Provider: {config.LLM_PROVIDER.upper()}")
    print(f"🤖 Modelo: {config.DEFAULT_MODEL}")
    print(f"🔍 Web Search: {'✅ ATIVO' if config.WEB_SEARCH_ENABLED else '❌ Inativo'}")

# === COMPATIBILIDADE - Variáveis diretas ===
# Mantidas para compatibilidade com código existente
LLM_PROVIDER = config.LLM_PROVIDER
GOOGLE_API_KEY = config.GOOGLE_API_KEY
ANTHROPIC_API_KEY = config.ANTHROPIC_API_KEY
DEFAULT_MODEL = config.DEFAULT_MODEL
CLAUDE_MODEL = config.DEFAULT_MODEL  # Alias para compatibilidade
MAX_TOKENS = config.MAX_TOKENS
CLAUDE_MAX_TOKENS = config.MAX_TOKENS  # Alias para compatibilidade
TEMPERATURE = config.TEMPERATURE
CLAUDE_TEMPERATURE = config.TEMPERATURE  # Alias para compatibilidade
TOP_P = config.TOP_P
TOP_K = config.TOP_K
LOG_LEVEL = config.LOG_LEVEL
LOG_FORMAT = config.LOG_FORMAT

# Web Search
WEB_SEARCH_ENABLED = config.WEB_SEARCH_ENABLED
WEB_SEARCH_MAX_USES = config.WEB_SEARCH_MAX_USES
WEB_SEARCH_ALLOWED_DOMAINS = config.WEB_SEARCH_ALLOWED_DOMAINS
WEB_SEARCH_BLOCKED_DOMAINS = config.WEB_SEARCH_BLOCKED_DOMAINS

# Telegram e outras APIs
TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
NOTION_API_KEY = config.NOTION_API_KEY

# Configurações de memória
CHROMA_DB_PATH = config.CHROMA_PERSIST_DIR
CHROMA_PERSIST_DIR = config.CHROMA_PERSIST_DIR  # Adicionar para compatibilidade
MEMORY_COLLECTION = "gpt_mestre_memory"

# Configurações de interface
STREAMLIT_THEME = "dark"
PAGE_TITLE = config.PROJECT_NAME
PAGE_ICON = config.STREAMLIT_CONFIG["page_icon"]

# Configurações de logs
LOG_FILE = str(config.LOGS_DIR / "gpt_mestre.log")
LOG_ROTATION = "100 MB"
LOG_RETENTION = "30 days"

print(f"🔧 Variáveis de compatibilidade configuradas")
print(f"🤖 LLM Provider: {LLM_PROVIDER}")
if LLM_PROVIDER == "gemini":
    print(f"🔑 GOOGLE_API_KEY: {'✅ Configurada' if GOOGLE_API_KEY else '❌ Não encontrada'}")
else:
    print(f"🔑 ANTHROPIC_API_KEY: {'✅ Configurada' if ANTHROPIC_API_KEY else '❌ Não encontrada'}")
print(f"🌐 WEB SEARCH: {'✅ Habilitado' if WEB_SEARCH_ENABLED else '❌ Desabilitado'}")