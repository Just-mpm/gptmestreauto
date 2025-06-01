"""
Módulo de agentes do GPT Mestre Autônomo v5.0
Centraliza todos os imports dos agentes do sistema com BaseAgentV2
"""

# Imports dos agentes base
try:
    from .base_agent_v2 import BaseAgentV2
    BASE_AGENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar BaseAgentV2: {e}")
    BASE_AGENTS_AVAILABLE = False

# === AGENTES V2.0 (BaseAgentV2) - RECOMENDADOS ===

# Carlos v5.0 Maestro (Agente Principal) - JÁ MIGRADO
try:
    from .carlos import CarlosMaestroV5, criar_carlos_maestro_v5, create_carlos
    CARLOS_V5_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Carlos v5.0 Maestro: {e}")
    CARLOS_V5_AVAILABLE = False

# Oráculo v9.0 (Assembleia Dinâmica com BaseAgentV2)
try:
    from .oraculo_v2 import OraculoV9, criar_oraculo_v9, create_oraculo
    ORACULO_V9_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Oráculo v9.0: {e}")
    ORACULO_V9_AVAILABLE = False

# PsyMind v2.0 (Agente Terapêutico com BaseAgentV2)
try:
    from .psymind_v2 import PsyMindV2, criar_psymind_v2, create_psymind
    PSYMIND_V2_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar PsyMind v2.0: {e}")
    PSYMIND_V2_AVAILABLE = False

# AutoMaster v2.0 (Autonomia Econômica com BaseAgentV2)
try:
    from .automaster_v2 import AutoMasterV2, criar_automaster_v2, create_automaster
    AUTOMASTER_V2_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar AutoMaster v2.0: {e}")
    AUTOMASTER_V2_AVAILABLE = False

# DeepAgent v2.0 (Pesquisa Web com BaseAgentV2)
try:
    from .deep_agent_v2 import DeepAgentWebSearchV2, criar_deep_agent_websearch_v2, criar_deep_agent_v2
    DEEPAGENT_V2_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar DeepAgent v2.0: {e}")
    DEEPAGENT_V2_AVAILABLE = False

# SupervisorAI v2.0 (Maestro de Raciocínio com BaseAgentV2)
try:
    from .supervisor_ai_v2 import SupervisorAIV2, criar_supervisor_ai_v2, create_supervisor
    SUPERVISOR_V2_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar SupervisorAI v2.0: {e}")
    SUPERVISOR_V2_AVAILABLE = False

# TaskBreaker v2.0 (Decomposição de Tarefas com BaseAgentV2)
try:
    from .task_breaker_v2 import TaskBreakerV2, criar_task_breaker_v2, create_taskbreaker
    TASKBREAKER_V2_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar TaskBreaker v2.0: {e}")
    TASKBREAKER_V2_AVAILABLE = False

# Reflexor v2.0 (Sistema de Auditoria com BaseAgentV2)
try:
    from .reflexor_v2 import ReflexorV2, criar_reflexor_v2, create_reflexor
    REFLEXOR_V2_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar Reflexor v2.0: {e}")
    REFLEXOR_V2_AVAILABLE = False

# ScoutAI v1.3A (Radar Estratégico de Oportunidades) - NOVO!
try:
    from .scout_ai import ScoutAI, criar_scout_ai, create_scout
    SCOUT_AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Erro ao importar ScoutAI v1.3A: {e}")
    SCOUT_AI_AVAILABLE = False

# === AGENTES LEGADOS - REMOVIDOS ===
# Versões v1.0 foram removidas para manter apenas as versões definitivas v2.0
# Todas as funcionalidades estão disponíveis nas versões v2.0 com robustez superior

CARLOS_LEGADO_AVAILABLE = False
REFLEXOR_LEGADO_AVAILABLE = False
ORACULO_LEGADO_AVAILABLE = False
AUTOMASTER_LEGADO_AVAILABLE = False
TASKBREAKER_LEGADO_AVAILABLE = False
PSYMIND_LEGADO_AVAILABLE = False
DEEPAGENT_LEGADO_AVAILABLE = False
SUPERVISOR_LEGADO_AVAILABLE = False

# Versão do módulo de agentes
__version__ = "5.0.0"

# === SISTEMA DE AGENTES DISPONÍVEIS ===

# Agentes v2.0 (Recomendados)
AGENTES_V2_DISPONIVEIS = []
AGENTES_V2_STATUS = {
    "carlos_v5": CARLOS_V5_AVAILABLE,
    "oraculo_v9": ORACULO_V9_AVAILABLE, 
    "psymind_v2": PSYMIND_V2_AVAILABLE,
    "automaster_v2": AUTOMASTER_V2_AVAILABLE,
    "deepagent_v2": DEEPAGENT_V2_AVAILABLE,
    "supervisor_v2": SUPERVISOR_V2_AVAILABLE,
    "taskbreaker_v2": TASKBREAKER_V2_AVAILABLE,
    "reflexor_v2": REFLEXOR_V2_AVAILABLE,
    "scout_ai": SCOUT_AI_AVAILABLE
}

for agente, disponivel in AGENTES_V2_STATUS.items():
    if disponivel:
        AGENTES_V2_DISPONIVEIS.append(agente)

# Agentes Legados - REMOVIDOS para projeto limpo
AGENTES_LEGADOS_DISPONIVEIS = []  # Lista vazia - todos migrados para v2.0
AGENTES_LEGADOS_STATUS = {}  # Status vazio - versões legadas removidas

# Total de agentes (apenas v2.0)
TODOS_AGENTES = AGENTES_V2_DISPONIVEIS

# === FUNÇÕES DE VERIFICAÇÃO ===

def verificar_agentes():
    """Verifica quais agentes estão disponíveis"""
    status = {
        "versao_modulo": __version__,
        "base_agents_available": BASE_AGENTS_AVAILABLE,
        "agentes_v2": {
            "disponiveis": AGENTES_V2_DISPONIVEIS,
            "total": len(AGENTES_V2_DISPONIVEIS),
            "status_detalhado": AGENTES_V2_STATUS
        },
        "agentes_legados": {
            "disponiveis": AGENTES_LEGADOS_DISPONIVEIS,
            "total": len(AGENTES_LEGADOS_DISPONIVEIS),
            "status_detalhado": AGENTES_LEGADOS_STATUS
        },
        "total_agentes": len(TODOS_AGENTES),
        "recomendacao": "Use agentes v2.0 para máxima robustez e performance"
    }
    return status

def listar_agentes_v2():
    """Lista apenas agentes v2.0 (recomendados)"""
    return {
        "agentes_v2_disponiveis": AGENTES_V2_DISPONIVEIS,
        "total": len(AGENTES_V2_DISPONIVEIS),
        "descricoes": {
            "carlos_v5": "Agente Central - Maestro Supremo v5.0",
            "oraculo_v9": "Assembleia Dinâmica - Oráculo v9.0", 
            "psymind_v2": "Agente Terapêutico - PsyMind v2.0",
            "automaster_v2": "Autonomia Econômica - AutoMaster v2.0",
            "deepagent_v2": "Pesquisa Web Real - DeepAgent v2.0",
            "supervisor_v2": "Maestro de Raciocínio - SupervisorAI v2.0",
            "taskbreaker_v2": "Decomposição de Tarefas - TaskBreaker v2.0",
            "reflexor_v2": "Sistema de Auditoria - Reflexor v2.0",
            "scout_ai": "Radar Estratégico - ScoutAI v1.3A"
        }
    }

# === FUNÇÕES DE CRIAÇÃO DO SISTEMA ===

def criar_sistema_v5_completo():
    """Cria sistema completo v5.0 com agentes v2.0"""
    if not CARLOS_V5_AVAILABLE:
        raise ImportError("Carlos v5.0 não está disponível")
    
    agentes_criados = {}
    
    # Carlos v5.0 (Principal)
    agentes_criados["carlos"] = criar_carlos_maestro_v5()
    
    # Agentes complementares v2.0
    if ORACULO_V9_AVAILABLE:
        agentes_criados["oraculo"] = criar_oraculo_v9()
    
    if PSYMIND_V2_AVAILABLE:
        agentes_criados["psymind"] = criar_psymind_v2()
    
    if AUTOMASTER_V2_AVAILABLE:
        agentes_criados["automaster"] = criar_automaster_v2()
    
    if DEEPAGENT_V2_AVAILABLE:
        agentes_criados["deepagent"] = criar_deep_agent_v2()
    
    if SUPERVISOR_V2_AVAILABLE:
        agentes_criados["supervisor"] = criar_supervisor_ai_v2()
    
    if TASKBREAKER_V2_AVAILABLE:
        agentes_criados["taskbreaker"] = criar_task_breaker_v2()
    
    if REFLEXOR_V2_AVAILABLE:
        agentes_criados["reflexor"] = criar_reflexor_v2()
    
    if SCOUT_AI_AVAILABLE:
        agentes_criados["scout"] = criar_scout_ai()
    
    return agentes_criados

def criar_sistema_completo():
    """Cria sistema completo (compatibilidade - redireciona para v5.0)"""
    return criar_sistema_v5_completo()

# === EXPORTS PRINCIPAIS ===

__all__ = [
    # Agentes base
    'BaseAgentV2',
    
    # Agentes v2.0 disponíveis
    'CarlosMaestroV5', 'criar_carlos_maestro_v5', 'create_carlos',
    
    # Funções de verificação
    'verificar_agentes',
    'listar_agentes_v2',
    
    # Listas de agentes
    'AGENTES_V2_DISPONIVEIS',
    'TODOS_AGENTES'
]

# === INICIALIZAÇÃO ===

print(f"🚀 GPT Mestre Autônomo v{__version__} - Sistema LIMPO e Robusto")
print(f"⚡ BaseAgentV2: {'✅ Disponível' if BASE_AGENTS_AVAILABLE else '❌ Indisponível'}")
print(f"🤖 Agentes v2.0: {len(AGENTES_V2_DISPONIVEIS)}/9 disponíveis")
print(f"🧹 Projeto Limpo: Apenas versões definitivas v2.0")
print(f"🎯 Total de Agentes: {len(TODOS_AGENTES)}")

if AGENTES_V2_DISPONIVEIS:
    print(f"✨ Agentes v2.0 Ativos: {', '.join(AGENTES_V2_DISPONIVEIS)}")
else:
    print("⚠️ Nenhum agente v2.0 disponível - verifique as dependências")

if SCOUT_AI_AVAILABLE:
    print("🔍 NOVO: ScoutAI v1.3A - Radar Estratégico Ativo!")

print("💡 Use 'verificar_agentes()' para diagnóstico completo")
print("🔧 Use 'criar_sistema_v5_completo()' para sistema completo")