"""
Módulo de agentes do GPT Mestre Autônomo
Centraliza todos os imports dos agentes do sistema
"""

# Imports dos agentes base
from .base_agent import BaseAgent

# Imports do Carlos v3.0 Maestro (Agente Principal)
try:
    from .carlos import CarlosMaestro, criar_carlos_maestro, create_carlos
    CARLOS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Carlos v3.0 Maestro: {e}")
    CARLOS_AVAILABLE = False

# Imports do Reflexor (Sistema de Auditoria)
try:
    from .reflexor import AgenteReflexor, criar_reflexor_gpt_mestre
    REFLEXOR_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Reflexor: {e}")
    REFLEXOR_AVAILABLE = False

# Imports do Oráculo v8.1 Plus+ (Assembleia Dinâmica)
try:
    from .oraculo import OraculoV8Plus, criar_oraculo_v8_plus, create_oraculo
    ORACULO_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Oráculo v8.1 Plus+: {e}")
    ORACULO_AVAILABLE = False

# Imports do AutoMaster v4.0 (Autonomia Econômica e Estratégica)
try:
    from .automaster import AutoMasterV4, criar_automaster_v4, create_automaster
    AUTOMASTER_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar AutoMaster v4.0: {e}")
    AUTOMASTER_AVAILABLE = False

# Versão do módulo de agentes
__version__ = "1.5.1"

# Lista de agentes disponíveis
AGENTES_DISPONIVEIS = []

if CARLOS_AVAILABLE:
    AGENTES_DISPONIVEIS.append("Carlos")
    
if REFLEXOR_AVAILABLE:
    AGENTES_DISPONIVEIS.append("Reflexor")

if ORACULO_AVAILABLE:
    AGENTES_DISPONIVEIS.append("Oráculo")

if AUTOMASTER_AVAILABLE:
    AGENTES_DISPONIVEIS.append("AutoMaster")

# Função para verificar status dos agentes
def verificar_agentes():
    """Verifica quais agentes estão disponíveis"""
    status = {
        "carlos": CARLOS_AVAILABLE,
        "reflexor": REFLEXOR_AVAILABLE,
        "oraculo": ORACULO_AVAILABLE,
        "automaster": AUTOMASTER_AVAILABLE,
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
    'CarlosMaestro', 
    'AgenteReflexor',
    'OraculoV8Plus',
    'AutoMasterV4',
    'create_carlos',
    'criar_carlos_maestro',
    'criar_reflexor_gpt_mestre',
    'criar_oraculo_v8_plus',
    'create_oraculo',
    'criar_automaster_v4',
    'create_automaster',
    'verificar_agentes',
    'criar_sistema_completo',
    'AGENTES_DISPONIVEIS'
]

print(f"🤖 Módulo de Agentes v{__version__} carregado")
print(f"📊 Agentes disponíveis: {', '.join(AGENTES_DISPONIVEIS)}")
