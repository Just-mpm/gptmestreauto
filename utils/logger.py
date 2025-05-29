"""
GPT MESTRE AUTÔNOMO - Sistema de Logging Centralizado
"""

import sys
from pathlib import Path
from loguru import logger
from config import config

class LoggerSetup:
    """Configuração centralizada do sistema de logging"""
    
    def __init__(self):
        self.setup_logger()
    
    def setup_logger(self):
        """Configura o logger com diferentes níveis e saídas"""
        
        # Remove configuração padrão
        logger.remove()
        
        # Console - para desenvolvimento
        logger.add(
            sys.stdout,
            format=config.LOG_FORMAT,
            level=config.LOG_LEVEL,
            colorize=True
        )
        
        # Arquivo geral - todas as mensagens
        logger.add(
            config.LOGS_DIR / "gpt_mestre.log",
            format=config.LOG_FORMAT,
            level="DEBUG",
            rotation="10 MB",
            retention="30 days",
            compression="zip"
        )
        
        # Arquivo de erros - apenas erros críticos
        logger.add(
            config.LOGS_DIR / "errors.log",
            format=config.LOG_FORMAT,
            level="ERROR",
            rotation="5 MB",
            retention="90 days"
        )
        
        # Arquivo específico para agentes
        logger.add(
            config.LOGS_DIR / "agents.log",
            format=config.LOG_FORMAT,
            level="INFO",
            filter=lambda record: "agent" in record["name"].lower(),
            rotation="5 MB",
            retention="15 days"
        )
        
        logger.info(f"🚀 Logger configurado para {config.PROJECT_NAME} v{config.VERSION}")

# Função helper para criar loggers específicos
def get_agent_logger(agent_name: str):
    """Cria um logger específico para um agente"""
    return logger.bind(agent=agent_name)

def get_system_logger():
    """Retorna o logger do sistema"""
    return logger

# Inicializa o sistema de logging
_logger_setup = LoggerSetup()

# Exports principais
system_logger = get_system_logger()

# Decorador para logging automático de funções
def log_function_call(func):
    """Decorador que registra chamadas de função automaticamente"""
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.debug(f"🔄 Chamando função: {func_name}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"✅ Função {func_name} executada com sucesso")
            return result
        except Exception as e:
            logger.error(f"❌ Erro na função {func_name}: {e}")
            raise
    return wrapper

if __name__ == "__main__":
    # Teste do sistema de logging
    test_logger = get_agent_logger("carlos")
    
    system_logger.info("Sistema de logging inicializado")
    test_logger.info("Teste de logging do agente Carlos")
    system_logger.warning("Teste de warning")
    system_logger.error("Teste de error (pode ignorar)")
    
    print("✅ Sistema de logging testado com sucesso!")
