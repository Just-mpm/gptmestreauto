"""
GPT MESTRE AUTÔNOMO - Configurações do Sistema (Fallback)
Versão sem dependência de python-dotenv
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
    VERSION = "3.0"
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
    LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini").lower()
    
    # === API KEYS ===
    # Para testes, usar chave hardcoded temporariamente
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "AIzaSyDHJrNLA3h-LFg4-urvbEd18Vcdzs-1DYE")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    
    # === CONFIGURAÇÕES DO MODELO ===
    if LLM_PROVIDER == "gemini":
        DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-preview-05-20")
        MAX_TOKENS = int(os.getenv("GEMINI_MAX_TOKENS", "8192"))
        TEMPERATURE = float(os.getenv("GEMINI_TEMPERATURE", "0.7"))
        TOP_P = float(os.getenv("GEMINI_TOP_P", "0.95"))
        TOP_K = int(os.getenv("GEMINI_TOP_K", "40"))
    else:
        DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-3-5-haiku-20241022")
        MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "4000"))
        TEMPERATURE = float(os.getenv("CLAUDE_TEMPERATURE", "0.7"))
        TOP_P = 0.95
        TOP_K = 40
    
    # === PERFORMANCE ===
    MAX_WORKERS = int(os.getenv("MAX_WORKERS", "4"))
    TIMEOUT_SECONDS = int(os.getenv("TIMEOUT_SECONDS", "60"))
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", "120"))
    BURST_ALLOWANCE = int(os.getenv("BURST_ALLOWANCE", "20"))
    
    # === MEMÓRIA ===
    MEMORY_ENABLED = os.getenv("MEMORY_ENABLED", "True").lower() == "true"
    CACHE_ENABLED = os.getenv("CACHE_ENABLED", "True").lower() == "true"
    CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))
    
    # === WEB SEARCH ===
    WEB_SEARCH_ENABLED = os.getenv("WEB_SEARCH_ENABLED", "True").lower() == "true"
    WEB_SEARCH_MAX_USES = int(os.getenv("WEB_SEARCH_MAX_USES", "3"))
    WEB_SEARCH_TIMEOUT = int(os.getenv("WEB_SEARCH_TIMEOUT", "30"))
    WEB_SEARCH_MAX_RESULTS = int(os.getenv("WEB_SEARCH_MAX_RESULTS", "10"))
    
    # === CHROMA DB ===
    CHROMA_ENABLED = os.getenv("CHROMA_ENABLED", "True").lower() == "true"
    CHROMA_PERSIST_DIRECTORY = os.getenv("CHROMA_PERSIST_DIRECTORY", "./memory/chroma_db")
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    
    # === LOGGING ===
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT = os.getenv("LOG_FORMAT", "detailed")
    LOG_FILE_ENABLED = os.getenv("LOG_FILE_ENABLED", "True").lower() == "true"
    
    # === CIRCUIT BREAKER ===
    CIRCUIT_BREAKER_ENABLED = os.getenv("CIRCUIT_BREAKER_ENABLED", "True").lower() == "true"
    FAILURE_THRESHOLD = int(os.getenv("FAILURE_THRESHOLD", "3"))
    RECOVERY_TIMEOUT = int(os.getenv("RECOVERY_TIMEOUT", "45"))
    
    # === INOVAÇÕES ===
    CONSCIENCIA_ENABLED = os.getenv("CONSCIENCIA_ENABLED", "True").lower() == "true"
    MASCARAS_ENABLED = os.getenv("MASCARAS_ENABLED", "True").lower() == "true"
    SUBCONSCIENTE_ENABLED = os.getenv("SUBCONSCIENTE_ENABLED", "True").lower() == "true"
    METAMEMORIA_ENABLED = os.getenv("METAMEMORIA_ENABLED", "True").lower() == "true"
    DNA_EVOLUTIVO_ENABLED = os.getenv("DNA_EVOLUTIVO_ENABLED", "True").lower() == "true"
    PERSONALIDADE_ENABLED = os.getenv("PERSONALIDADE_ENABLED", "True").lower() == "true"
    CICLO_VIDA_ENABLED = os.getenv("CICLO_VIDA_ENABLED", "True").lower() == "true"
    SONHOS_ENABLED = os.getenv("SONHOS_ENABLED", "True").lower() == "true"
    EVENTOS_COGNITIVOS_ENABLED = os.getenv("EVENTOS_COGNITIVOS_ENABLED", "True").lower() == "true"
    GPTM_SUPRA_ENABLED = os.getenv("GPTM_SUPRA_ENABLED", "True").lower() == "true"

# Criar instância global
config = Config()