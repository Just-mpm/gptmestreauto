"""
Sistema de logging avançado para o GPT Mestre Autônomo - VERSÃO COMPLETA
"""

import os
import sys
from datetime import datetime
import functools
import traceback

# Try loguru first, fallback to standard logging
try:
    from loguru import logger
    LOGURU_AVAILABLE = True
except ImportError:
    LOGURU_AVAILABLE = False
    from .fallback_logger import get_fallback_logger
    logger = get_fallback_logger("gpt_mestre")

# Tentar importar config, se não existir, usar valores padrão
try:
    import config
    LOG_LEVEL = getattr(config, 'LOG_LEVEL', 'INFO')
    LOG_FORMAT = getattr(config, 'LOG_FORMAT', "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}")
    LOG_FILE = getattr(config, 'LOG_FILE', "logs/gpt_mestre.log")
    LOG_ROTATION = getattr(config, 'LOG_ROTATION', "100 MB")
    LOG_RETENTION = getattr(config, 'LOG_RETENTION', "30 days")
except ImportError:
    # Valores padrão se config não existir
    LOG_LEVEL = 'INFO'
    LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name} | {message}"
    LOG_FILE = "logs/gpt_mestre.log"
    LOG_ROTATION = "100 MB"
    LOG_RETENTION = "30 days"

# Configure logger only if loguru is available
if LOGURU_AVAILABLE:
    # Remover logger padrão
    logger.remove()

    # Configurar logger para console
    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        colorize=True
    )

    # Criar pasta de logs se não existir
    os.makedirs("logs", exist_ok=True)

    # Configurar logger para arquivo principal
    logger.add(
        LOG_FILE,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        compression="zip"
    )

    # Logger específico para agentes
    logger.add(
        "logs/agents.log",
        format=LOG_FORMAT,
        level="DEBUG",
        rotation="50 MB",
        retention="15 days",
        filter=lambda record: "agent" in record["name"].lower()
    )

    # Logger específico para erros
    logger.add(
        "logs/errors.log",
        format=LOG_FORMAT,
        level="ERROR",
        rotation="10 MB",
        retention="60 days"
    )
else:
    # Fallback configuration
    os.makedirs("logs", exist_ok=True)

# ===== FUNÇÕES PRINCIPAIS =====

def get_logger(name: str):
    """
    Retorna um logger configurado para um módulo específico
    
    Args:
        name: Nome do módulo/classe
    
    Returns:
        Logger configurado
    """
    if LOGURU_AVAILABLE:
        return logger.bind(name=name)
    else:
        return get_fallback_logger(name)

def log_agent_interaction(agent_name: str, input_data: str, output_data: str, success: bool = True):
    """Log específico para interações de agentes"""
    agent_logger = get_logger(f"agent.{agent_name}")
    
    if success:
        agent_logger.info(f"Interação bem-sucedida - Input: {input_data[:100]}... | Output: {output_data[:100]}...")
    else:
        agent_logger.error(f"Erro na interação - Input: {input_data[:100]}...")

def log_system_event(event: str, details: dict = None):
    """Log para eventos do sistema"""
    system_logger = get_logger("system")
    
    if details:
        system_logger.info(f"{event} | Detalhes: {details}")
    else:
        system_logger.info(event)

def log_error(error_msg: str, exception: Exception = None):
    """Log específico para erros"""
    error_logger = get_logger("error")
    
    if exception:
        error_logger.error(f"{error_msg} | Exception: {str(exception)}")
    else:
        error_logger.error(error_msg)

def log_debug(message: str, context: str = "debug"):
    """Log de debug"""
    debug_logger = get_logger(context)
    debug_logger.debug(message)

def log_info(message: str, context: str = "info"):
    """Log de informação"""
    info_logger = get_logger(context)
    info_logger.info(message)

def log_warning(message: str, context: str = "warning"):
    """Log de aviso"""
    warning_logger = get_logger(context)
    warning_logger.warning(message)

# ===== FUNÇÕES ADICIONAIS SOLICITADAS =====

def log_function_call(func_name: str, args: tuple = None, kwargs: dict = None, context: str = "function"):
    """Log de chamadas de função"""
    func_logger = get_logger(context)
    
    args_str = str(args)[:100] if args else "()"
    kwargs_str = str(kwargs)[:100] if kwargs else "{}"
    
    func_logger.debug(f"Chamada de função: {func_name}({args_str}, {kwargs_str})")

def log_method_call(method_name: str, instance_name: str = None, args: tuple = None, context: str = "method"):
    """Log de chamadas de método"""
    method_logger = get_logger(context)
    
    instance_str = f"{instance_name}." if instance_name else ""
    args_str = str(args)[:100] if args else "()"
    
    method_logger.debug(f"Chamada de método: {instance_str}{method_name}({args_str})")

def log_performance(operation: str, duration: float, context: str = "performance"):
    """Log de performance"""
    perf_logger = get_logger(context)
    perf_logger.info(f"Performance - {operation}: {duration:.4f}s")

def log_api_call(endpoint: str, method: str, status_code: int = None, response_time: float = None):
    """Log de chamadas de API"""
    api_logger = get_logger("api")
    
    status_str = f" [{status_code}]" if status_code else ""
    time_str = f" ({response_time:.3f}s)" if response_time else ""
    
    api_logger.info(f"API {method} {endpoint}{status_str}{time_str}")

def log_database_query(query: str, execution_time: float = None, context: str = "database"):
    """Log de queries de database"""
    db_logger = get_logger(context)
    
    query_short = query[:200] + "..." if len(query) > 200 else query
    time_str = f" ({execution_time:.3f}s)" if execution_time else ""
    
    db_logger.debug(f"Query{time_str}: {query_short}")

def log_exception(exception: Exception, context: str = "exception", include_traceback: bool = True):
    """Log detalhado de exceções"""
    exc_logger = get_logger(context)
    
    if include_traceback:
        exc_logger.error(f"Exception: {str(exception)}\n{traceback.format_exc()}")
    else:
        exc_logger.error(f"Exception: {str(exception)}")

def log_memory_usage(memory_mb: float, context: str = "memory"):
    """Log de uso de memória"""
    mem_logger = get_logger(context)
    mem_logger.info(f"Uso de memória: {memory_mb:.2f} MB")

def log_startup(component: str, version: str = None):
    """Log de inicialização de componentes"""
    startup_logger = get_logger("startup")
    version_str = f" v{version}" if version else ""
    startup_logger.info(f"🚀 {component}{version_str} inicializado")

def log_shutdown(component: str):
    """Log de encerramento de componentes"""
    shutdown_logger = get_logger("shutdown")
    shutdown_logger.info(f"⏹️ {component} encerrado")

def log_config_change(setting: str, old_value: str, new_value: str):
    """Log de mudanças de configuração"""
    config_logger = get_logger("config")
    config_logger.info(f"Configuração alterada - {setting}: {old_value} → {new_value}")

def log_security_event(event: str, details: dict = None, level: str = "warning"):
    """Log de eventos de segurança"""
    security_logger = get_logger("security")
    
    log_func = getattr(security_logger, level.lower(), security_logger.warning)
    
    if details:
        log_func(f"🔒 Evento de segurança: {event} | Detalhes: {details}")
    else:
        log_func(f"🔒 Evento de segurança: {event}")

def log_user_action(user_id: str, action: str, details: dict = None):
    """Log de ações do usuário"""
    user_logger = get_logger("user_action")
    
    if details:
        user_logger.info(f"👤 Usuário {user_id}: {action} | {details}")
    else:
        user_logger.info(f"👤 Usuário {user_id}: {action}")

# ===== DECORADORES DE LOG =====

def log_function_decorator(func):
    """Decorator para log automático de funções"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_logger = get_logger(f"func.{func.__name__}")
        
        start_time = datetime.now()
        func_logger.debug(f"Iniciando {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            func_logger.debug(f"Concluído {func.__name__} em {duration:.4f}s")
            return result
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            func_logger.error(f"Erro em {func.__name__} após {duration:.4f}s: {str(e)}")
            raise
    
    return wrapper

# ===== UTILITÁRIOS =====

def set_log_level(level: str):
    """
    Configura o nível de log dinamicamente
    
    Args:
        level: Nível do log (DEBUG, INFO, WARNING, ERROR)
    """
    global LOG_LEVEL
    LOG_LEVEL = level.upper()
    
    # Reconfigurar loggers
    logger.remove()
    logger.add(
        sys.stdout,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        colorize=True
    )
    
    logger.add(
        LOG_FILE,
        format=LOG_FORMAT,
        level=LOG_LEVEL,
        rotation=LOG_ROTATION,
        retention=LOG_RETENTION,
        compression="zip"
    )

def get_log_stats():
    """Retorna estatísticas dos logs"""
    try:
        if os.path.exists(LOG_FILE):
            size = os.path.getsize(LOG_FILE)
            return {
                "log_file": LOG_FILE,
                "size_mb": round(size / (1024 * 1024), 2),
                "level": LOG_LEVEL,
                "format": LOG_FORMAT
            }
    except Exception as e:
        return {"error": str(e)}
    
    return {"status": "log file not found"}

def test_logging():
    """Testa todas as funções de logging"""
    test_logger = get_logger("test")
    
    print("🧪 Testando sistema de logging completo...")
    
    # Testes básicos
    test_logger.debug("Teste de debug")
    test_logger.info("Teste de info")
    test_logger.warning("Teste de warning")
    test_logger.error("Teste de error")
    
    # Testes avançados
    log_system_event("Sistema inicializado", {"timestamp": datetime.now().isoformat()})
    log_agent_interaction("TestAgent", "pergunta teste", "resposta teste", True)
    log_function_call("test_function", ("arg1", "arg2"), {"key": "value"})
    log_api_call("/api/test", "GET", 200, 0.123)
    log_performance("operacao_teste", 1.234)
    log_startup("TestComponent", "1.0.0")
    
    print("✅ Sistema de logging testado com sucesso!")

# ===== ALIASES PARA COMPATIBILIDADE =====

# Aliases principais
get_agent_logger = get_logger
agent_logger = get_logger
create_logger = get_logger
setup_logger = get_logger
logger_for = get_logger

# Aliases para funções específicas
log_func_call = log_function_call
log_func = log_function_call
log_method = log_method_call
log_perf = log_performance
log_api = log_api_call
log_db = log_database_query
log_exc = log_exception
log_mem = log_memory_usage
log_start = log_startup
log_stop = log_shutdown
log_cfg = log_config_change
log_sec = log_security_event
log_user = log_user_action

# ===== INICIALIZAÇÃO =====

# Inicialização do sistema de logging
system_logger = get_logger("system")
if LOGURU_AVAILABLE:
    system_logger.info("🚀 Sistema de logging GPT Mestre Autônomo v2.0 inicializado (loguru)")
else:
    system_logger.info("🚀 Sistema de logging GPT Mestre Autônomo v2.0 inicializado (fallback)")

# Lista completa de exports
__all__ = [
    # Funções principais
    'get_logger', 'get_agent_logger', 'agent_logger', 'create_logger', 'setup_logger', 'logger_for',
    
    # Funções de log específicas
    'log_agent_interaction', 'log_system_event', 'log_error', 'log_debug', 'log_info', 'log_warning',
    'log_function_call', 'log_method_call', 'log_performance', 'log_api_call', 'log_database_query',
    'log_exception', 'log_memory_usage', 'log_startup', 'log_shutdown', 'log_config_change',
    'log_security_event', 'log_user_action',
    
    # Aliases
    'log_func_call', 'log_func', 'log_method', 'log_perf', 'log_api', 'log_db', 'log_exc',
    'log_mem', 'log_start', 'log_stop', 'log_cfg', 'log_sec', 'log_user',
    
    # Utilitários
    'log_function_decorator', 'set_log_level', 'get_log_stats', 'test_logging'
]

# Exemplo de uso para documentação
if __name__ == "__main__":
    test_logging()
    
    # Testar aliases
    print("🧪 Testando aliases...")
    
    logger1 = get_logger("test1")
    logger2 = get_agent_logger("test2")  
    logger3 = create_logger("test3")
    
    logger1.info("✅ get_logger OK")
    logger2.info("✅ get_agent_logger OK")
    logger3.info("✅ create_logger OK")
    
    # Testar função solicitada
    log_function_call("test_function", ("arg1",), {"key": "value"})
    
    print("✅ Todos os testes funcionando!")
    print(f"📊 Stats: {get_log_stats()}")
