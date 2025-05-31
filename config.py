"""
GPT MESTRE AUTÔNOMO - Configurações do Sistema
Versão: 2.5 - Com Web Search Real
Autor: Matheus Meireles
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

class Config:
    """Configurações centralizadas do sistema"""
    
    # === CONFIGURAÇÕES BÁSICAS ===
    PROJECT_NAME = "GPT Mestre Autônomo"
    VERSION = "2.5"  # 🆕 Versão com Web Search
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # === DIRETÓRIOS ===
    BASE_DIR = Path(__file__).parent
    LOGS_DIR = BASE_DIR / "logs"
    MEMORY_DIR = BASE_DIR / "memory"
    AGENTS_DIR = BASE_DIR / "agents"
    
    # Cria diretórios se não existirem
    for dir_path in [LOGS_DIR, MEMORY_DIR, AGENTS_DIR]:
        dir_path.mkdir(exist_ok=True)
    
    # === API KEYS ===
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY não encontrada! Configure no arquivo .env")
    
    # === CONFIGURAÇÕES DO LLM (Claude 3.5 Haiku com Web Search) ===
    DEFAULT_MODEL = "claude-3-5-haiku-20241022"  # 🆕 Modelo atualizado com web search
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    
    # 🆕 === CONFIGURAÇÕES DE WEB SEARCH ===
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
        "deepagent",   # 🆕 Com web search real!
        "supervisor",  # Classificador inteligente
    ]
    
    # === CONFIGURAÇÕES DO STREAMLIT ===
    STREAMLIT_CONFIG = {
        "page_title": PROJECT_NAME,
        "page_icon": "🌐",  # 🆕 Ícone atualizado para web
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
    
    if not config.ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY não configurada")
    
    # 🆕 Validar configurações de web search
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
    print(f"🌐 Claude 3.5 Haiku: {config.DEFAULT_MODEL}")
    print(f"🔍 Web Search: {'✅ ATIVO' if config.WEB_SEARCH_ENABLED else '❌ Inativo'}")

# === COMPATIBILIDADE - Variáveis diretas ===
ANTHROPIC_API_KEY = config.ANTHROPIC_API_KEY
DEFAULT_MODEL = config.DEFAULT_MODEL
CLAUDE_MODEL = config.DEFAULT_MODEL
MAX_TOKENS = config.MAX_TOKENS
CLAUDE_MAX_TOKENS = config.MAX_TOKENS
TEMPERATURE = config.TEMPERATURE
CLAUDE_TEMPERATURE = config.TEMPERATURE
LOG_LEVEL = config.LOG_LEVEL
LOG_FORMAT = config.LOG_FORMAT

# 🆕 Web Search
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
print(f"🔑 ANTHROPIC_API_KEY: {'✅ Configurada' if ANTHROPIC_API_KEY else '❌ Não encontrada'}")
print(f"🌐 WEB SEARCH: {'✅ Habilitado' if WEB_SEARCH_ENABLED else '❌ Desabilitado'}")