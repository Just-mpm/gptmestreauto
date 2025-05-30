"""
GPT MESTRE AUTÔNOMO - Módulo de Memória
Inicialização do sistema de memória vetorial
"""

# Imports principais do módulo de memória
try:
    from .vector_store import (
        MemoryManager,
        get_memory_manager,
        remember_conversation,
        recall_context
    )
    MEMORY_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Memória vetorial não disponível: {e}")
    MEMORY_AVAILABLE = False

# Versão do módulo
__version__ = "2.0"

# Exports principais
__all__ = [
    'MemoryManager',
    'get_memory_manager', 
    'remember_conversation',
    'recall_context',
    'MEMORY_AVAILABLE'
]

print(f"🧠 Módulo de Memória v{__version__} {'✅ carregado' if MEMORY_AVAILABLE else '❌ indisponível'}")
