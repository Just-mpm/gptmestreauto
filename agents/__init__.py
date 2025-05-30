"""
Módulo de agentes do GPT Mestre Autônomo
Centraliza todos os imports dos agentes do sistema
"""

# Imports dos agentes base
from .base_agent import BaseAgent

# Imports do Carlos (Agente Principal)
try:
    from .carlos import CarlosAgent, create_carlos, create_carlos_com_reflexor
    CARLOS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Carlos: {e}")
    CARLOS_AVAILABLE = False

# Imports do Reflexor (Sistema de Auditoria)
try:
    from .reflexor import AgenteReflexor, criar_reflexor_gpt_mestre
    REFLEXOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Reflexor: {e}")
    REFLEXOR_AVAILABLE = False

# Versão do módulo de agentes
__version__ = "1.5.1"

# Lista de agentes disponíveis
AGENTES_DISPONIVEIS = []

if CARLOS_AVAILABLE:
    AGENTES_DISPONIVEIS.append("Carlos")
    
if REFLEXOR_AVAILABLE:
    AGENTES_DISPONIVEIS.append("Reflexor")

# Função para verificar status dos agentes
def verificar_agentes():
    """Verifica quais agentes estão disponíveis"""
    status = {
        "carlos": CARLOS_AVAILABLE,
        "reflexor": REFLEXOR_AVAILABLE,
        "total_disponiveis": len(AGENTES_DISPONIVEIS),
        "agentes": AGENTES_DISPONIVEIS
    }
    return status

# Função para criar sistema completo
def criar_sistema_completo():
    """Cria Carlos com Reflexor integrado"""
    if not CARLOS_AVAILABLE:
        raise ImportError("Carlos não está disponível")
    
    if REFLEXOR_AVAILABLE:
        return create_carlos_com_reflexor(reflexor_ativo=True)
    else:
        print("⚠️ Reflexor não disponível - Carlos funcionará sem auditoria")
        return create_carlos()

# Exports principais
__all__ = [
    'BaseAgent',
    'CarlosAgent', 
    'AgenteReflexor',
    'create_carlos',
    'create_carlos_com_reflexor',
    'criar_reflexor_gpt_mestre',
    'verificar_agentes',
    'criar_sistema_completo',
    'AGENTES_DISPONIVEIS'
]

print(f"🤖 Módulo de Agentes v{__version__} carregado")
print(f"📊 Agentes disponíveis: {', '.join(AGENTES_DISPONIVEIS)}")
