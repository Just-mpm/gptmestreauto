"""
GPT MESTRE AUTÔNOMO - Configurações do Sistema
Versão: 1.0.0 - Fase 1 (MVP Básico)
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
    VERSION = "1.0.0"
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
    
    # === CONFIGURAÇÕES DO LLM (Claude 3) ===
    DEFAULT_MODEL = "claude-3-haiku-20240307"  # Claude 3 Haiku (mais barato)
    # DEFAULT_MODEL = "claude-3-sonnet-20240229"  # Claude 3 Sonnet (melhor qualidade)
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    
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
        "oraculo",     # Tomador de decisões
    ]
    
    # === CONFIGURAÇÕES DO STREAMLIT ===
    STREAMLIT_CONFIG = {
        "page_title": PROJECT_NAME,
        "page_icon": "🤖",
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
    
    if errors:
        raise ValueError(f"Configuração inválida: {', '.join(errors)}")
    
    return True

if __name__ == "__main__":
    validate_config()
    print(f"✅ Configuração do {config.PROJECT_NAME} v{config.VERSION} validada com sucesso!")
    print(f"🤖 Usando Claude 3: {config.DEFAULT_MODEL}")

    # ADICIONAR NO FINAL DO ARQUIVO config.py (após a linha do print)

# === COMPATIBILIDADE - Variáveis diretas ===
# Para compatibilidade com imports diretos
ANTHROPIC_API_KEY = config.ANTHROPIC_API_KEY
DEFAULT_MODEL = config.DEFAULT_MODEL
CLAUDE_MODEL = config.DEFAULT_MODEL
MAX_TOKENS = config.MAX_TOKENS
CLAUDE_MAX_TOKENS = config.MAX_TOKENS
TEMPERATURE = config.TEMPERATURE
CLAUDE_TEMPERATURE = config.TEMPERATURE
LOG_LEVEL = config.LOG_LEVEL
LOG_FORMAT = config.LOG_FORMAT

# Telegram e outras APIs
TELEGRAM_BOT_TOKEN = config.TELEGRAM_BOT_TOKEN
NOTION_API_KEY = config.NOTION_API_KEY

# Configurações de memória
CHROMA_DB_PATH = config.CHROMA_PERSIST_DIR
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