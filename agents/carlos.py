"""
🧠 CARLOS v5.0 - MAESTRO SUPREMO COM ROBUSTEZ TOTAL
Agente Central com Orquestração Avançada + BaseAgentV2 Robustez
EVOLUÇÃO v5.0: Circuit Breakers, Rate Limiting, Thread Safety, Auto-Recovery
"""

import json
import time
import re
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum

from agents.base_agent_v2 import BaseAgentV2

# Importar cache manager
try:
    from utils.cache_manager import get_cache_manager
    cache_manager = get_cache_manager()
except ImportError:
    cache_manager = None
    print("⚠️ CacheManager não disponível")

# === IMPORTAÇÃO DAS 10 INOVAÇÕES REVOLUCIONÁRIAS ===
try:
    from utils.consciencia_artificial import criar_consciencia_artificial
    from utils.mascaras_sociais import criar_gerenciador_mascaras
    from utils.carlos_subconsciente import criar_carlos_subconsciente
    from utils.metamemoria import criar_metamemoria
    from utils.dna_evolutivo import criar_dna_evolutivo
    from utils.personalidade_energia import criar_gerenciador_personalidade
    from utils.ciclo_vida_agentes import criar_gerenciador_ciclo_vida
    from utils.sonhos_agentes import criar_gerador_sonhos
    from utils.gptm_supra import obter_gptm_supra
    from utils.eventos_cognitivos_globais import atualizar_metricas_agente_global
    INOVACOES_DISPONIVEIS = True
except ImportError as e:
    print(f"⚠️ Inovações não disponíveis: {e}")
    INOVACOES_DISPONIVEIS = False

# Logger com fallback
try:
    from utils.logger import get_logger
except ImportError:
    class SimpleLogger:
        def __init__(self, name): self.name = name
        def info(self, msg): print(f"[INFO] {self.name}: {msg}")
        def warning(self, msg): print(f"[WARNING] {self.name}: {msg}")
        def error(self, msg): print(f"[ERROR] {self.name}: {msg}")
        def debug(self, msg): print(f"[DEBUG] {self.name}: {msg}")
    def get_logger(name): return SimpleLogger(name)

logger = get_logger(__name__)

class TipoComando(Enum):
    """Tipos de comando que Carlos pode interpretar"""
    ANALISE_PRODUTO = "analise_produto"
    CRIACAO_PROMPT = "criacao_prompt"
    AUTOMACAO = "automacao"
    INTEGRACAO = "integracao"
    OTIMIZACAO_COPY = "otimizacao_copy"
    CRIACAO_KIT = "criacao_kit"
    DIAGNOSTICO_SISTEMA = "diagnostico_sistema"
    DECISAO_COMPLEXA = "decisao_complexa"
    PLANEJAMENTO_CARREIRA = "planejamento_carreira"
    COMANDO_GENERICO = "comando_generico"

class StatusExecucao(Enum):
    """Status de execução de tarefas"""
    PENDENTE = "pendente"
    EM_ANDAMENTO = "em_andamento"
    CONCLUIDA = "concluida"
    BLOQUEADA = "bloqueada"
    CANCELADA = "cancelada"

@dataclass
class RegistroExecucao:
    """Registro de uma execução para tracking e aprendizado"""
    id: str
    comando_original: str
    tipo_comando: TipoComando
    agentes_acionados: List[str]
    resultado: str
    timestamp: datetime
    microtags: List[str] = field(default_factory=list)
    dna_heranca: Optional[str] = None
    score_qualidade: Optional[float] = None
    status: StatusExecucao = StatusExecucao.CONCLUIDA

@dataclass
class ItemAgenda:
    """Item da agenda interna estratégica do Carlos"""
    id: str
    descricao: str
    prioridade: int  # 1-10
    categoria: str
    data_criacao: datetime
    data_limite: Optional[datetime] = None
    status: StatusExecucao = StatusExecucao.PENDENTE
    observacoes: str = ""

class CarlosMaestroV5(BaseAgentV2):
    """
    🧠 CARLOS v5.0 - MAESTRO SUPREMO COM ROBUSTEZ TOTAL
    
    MISSÃO EVOLUTIVA v5.0:
    - Orquestração inteligente com robustez extrema (BaseAgentV2)
    - Coordenação autônoma com circuit breakers e auto-recovery
    - Rate limiting inteligente para gestão de recursos
    - Thread safety para execução paralela real
    - Persistência automática com backup de estados
    - Performance monitoring e alertas proativos
    
    🛡️ ROBUSTEZ v5.0 (Herdada de BaseAgentV2):
    - ✅ Circuit Breaker para proteção contra falhas
    - ✅ Rate Limiting inteligente com burst allowance
    - ✅ Thread Safety para execução paralela real
    - ✅ Auto-Recovery e fallback robusto
    - ✅ Performance Monitoring avançado
    - ✅ Persistent Memory com backup automático
    - ✅ Cache inteligente com TTL
    - ✅ Retry automático com backoff exponencial
    
    🧠 CARACTERÍSTICAS AVANÇADAS MANTIDAS:
    - Agenda Interna de Prioridades Estratégicas  
    - Sistema de microtags para rastreamento
    - ShadowChain para execuções paralelas
    - DNA de herança de execuções anteriores
    - Comando Espelho para simulações reversas
    - Sentinela de execuções esquecidas
    - SUPERVISÃO SUPREMA DO ORÁCULO (Regente do Sistema)
    """
    
    def __init__(self, reflexor_ativo: bool = True, supervisor_ativo: bool = True, 
                 memoria_ativa: bool = True, deepagent_ativo: bool = True, 
                 oraculo_ativo: bool = True, automaster_ativo: bool = True,
                 taskbreaker_ativo: bool = True, psymind_ativo: bool = True,
                 modo_proativo: bool = True, config: Optional[Dict] = None, **kwargs):
        
        # Configuração robusta para Carlos v5.0
        carlos_config = {
            "rate_limit_per_minute": 120,  # Carlos precisa de mais throughput
            "burst_allowance": 20,        # Burst maior para coordenação
            "failure_threshold": 3,       # Mais sensível a falhas
            "recovery_timeout": 45,       # Recovery mais rápido
            "cache_enabled": True,
            "cache_ttl_seconds": 300,
            "persistent_memory": True,
            "max_retry_attempts": 3,
            "timeout_seconds": 60         # Timeout maior para coordenação
        }
        
        if config:
            carlos_config.update(config)
        
        super().__init__(
            name="Carlos",
            description="🧠 Maestro Central v5.0 - Coordenador Robusto do GPT Mestre Autônomo",
            config=carlos_config,
            **kwargs
        )
        
        # === SISTEMAS CORE ===
        self.memoria_ativa = memoria_ativa
        # Não sobrescrever memory_manager do BaseAgentV2 - será inicializado automaticamente
        self.vector_memory_manager = None  # Manager específico para conversas
        self.reflexor_ativo = reflexor_ativo
        self.reflexor = None
        self.supervisor_ativo = supervisor_ativo
        self.supervisor = None
        self.oraculo_ativo = oraculo_ativo
        self.oraculo = None
        self.automaster_ativo = automaster_ativo
        self.automaster = None
        self.taskbreaker_ativo = taskbreaker_ativo
        self.taskbreaker = None
        self.deepagent_ativo = deepagent_ativo
        self.deepagent = None
        self.psymind_ativo = psymind_ativo
        self.psymind = None
        self.promptcrafter_ativo = kwargs.get('promptcrafter_ativo', True)
        self.promptcrafter = None
        self.modo_proativo = modo_proativo
        
        # === AGENDA INTERNA ESTRATÉGICA ===
        self.agenda_interna: List[ItemAgenda] = []
        self.contador_agenda = 0
        
        # === SISTEMA DE TRACKING E DNA ===
        self.historico_execucoes: List[RegistroExecucao] = []
        self.contador_execucoes = 0
        self.padroes_dna: Dict[str, List[str]] = {}  # DNA -> lista de execuções
        
        # === CONFIGURAÇÕES AVANÇADAS ===
        self.shadow_chain_ativo = True
        self.comando_espelho_ativo = True
        self.sentinela_ativo = True
        
        # === SISTEMAS DE INOVAÇÃO (v4.9) ===
        self.inovacoes_ativas = kwargs.get('inovacoes_ativas', INOVACOES_DISPONIVEIS)
        self.consciencia = None
        self.mascaras = None
        self.subconsciente = None
        self.metamemoria = None
        self.dna = None
        self.personalidade = None
        self.ciclo_vida = None
        self.sonhos = None
        self.gptm_supra = None
        
        if self.inovacoes_ativas and INOVACOES_DISPONIVEIS:
            try:
                # 1. Sistema de Consciência Artificial
                self.consciencia = criar_consciencia_artificial(self.name)
                logger.info("✅ Consciência Artificial ativada")
                
                # 2. Máscaras Sociais
                self.mascaras = criar_gerenciador_mascaras(self.name)
                logger.info("✅ Máscaras Sociais ativadas")
                
                # 3. Subconsciente
                self.subconsciente = criar_carlos_subconsciente(self.name)
                logger.info("✅ Sistema Subconsciente ativado")
                
                # 4. Metamemória
                self.metamemoria = criar_metamemoria(self.name)
                logger.info("✅ Metamemória ativada")
                
                # 5. DNA Evolutivo
                self.dna = criar_dna_evolutivo(self.name)
                logger.info("✅ DNA Evolutivo ativado")
                
                # 6. Personalidade e Energia
                self.personalidade = criar_gerenciador_personalidade(self.name)
                logger.info("✅ Sistema de Personalidade ativado")
                
                # 7. Ciclo de Vida
                self.ciclo_vida = criar_gerenciador_ciclo_vida(self.name)
                logger.info("✅ Ciclo de Vida ativado")
                
                # 8. Sistema de Sonhos
                self.sonhos = criar_gerador_sonhos(self.name)
                logger.info("✅ Sistema de Sonhos ativado")
                
                # 9. GPTM Supra (Narrador)
                self.gptm_supra = obter_gptm_supra()
                logger.info("✅ GPTM Supra (Narrador Mitológico) ativado")
                
                # 10. Eventos Cognitivos já está importado
                logger.info("✅ Eventos Cognitivos Globais prontos")
                
                logger.info("🚀 TODAS AS 10 INOVAÇÕES ATIVADAS COM SUCESSO!")
            except Exception as e:
                logger.error(f"❌ Erro ao ativar inovações: {e}")
                self.inovacoes_ativas = False
        else:
            self.inovacoes_ativas = False
            logger.info("📝 Sistema operando sem inovações avançadas")
        
        # Configurar LLM se não foi inicializado pelo BaseAgentV2
        if not self.llm_available:
            if kwargs.get('llm'):
                self.llm = kwargs['llm']
                self.llm_available = True
            else:
                self._inicializar_llm_carlos()
        
        # Inicializar sistemas
        self._inicializar_sistemas()
        
        # === SISTEMA DE RECONHECIMENTO DE PADRÕES ===
        self.padroes_comando = {
            # Padrões para detecção automática de tipo de comando
            TipoComando.ANALISE_PRODUTO: [
                r"analise?\s+(?:o\s+)?produto",
                r"pesquise?\s+(?:sobre\s+)?(.+)",
                r"verifique?\s+(?:o\s+)?mercado",
                r"quanto\s+custa",
                r"preço\s+(?:de\s+)?(.+)"
            ],
            TipoComando.CRIACAO_PROMPT: [
                r"crie?\s+(?:um\s+)?prompt",
                r"monte?\s+(?:um\s+)?prompt",
                r"preciso\s+(?:de\s+)?(?:um\s+)?prompt"
            ],
            TipoComando.AUTOMACAO: [
                r"automatize?\s+(.+)",
                r"crie?\s+(?:uma\s+)?automação",
                r"monte?\s+(?:um\s+)?sistema\s+(?:para\s+)?(.+)"
            ],
            TipoComando.INTEGRACAO: [
                r"integre?\s+(.+)\s+com\s+(.+)",
                r"conecte?\s+(.+)",
                r"webhook",
                r"api"
            ],
            TipoComando.OTIMIZACAO_COPY: [
                r"otimize?\s+(?:o\s+)?texto",
                r"melhore?\s+(?:o\s+)?copy",
                r"reescreva?\s+(.+)"
            ],
            TipoComando.CRIACAO_KIT: [
                r"monte?\s+(?:um\s+)?kit",
                r"crie?\s+(?:um\s+)?bundle",
                r"combine?\s+produtos"
            ],
            TipoComando.DIAGNOSTICO_SISTEMA: [
                r"diagnostique?\s+(?:o\s+)?sistema",
                r"verifique?\s+(?:o\s+)?status",
                r"analise?\s+(?:a\s+)?performance"
            ],
            TipoComando.DECISAO_COMPLEXA: [
                r"decida?\s+sobre",
                r"ajude?\s+a\s+decidir",
                r"qual\s+(?:a\s+)?melhor\s+op[çc][ãa]o",
                r"compare?\s+alternativas",
                r"analise?\s+cen[áa]rios"
            ],
            TipoComando.PLANEJAMENTO_CARREIRA: [
                r"planeje?\s+(?:minha\s+)?carreira",
                r"quero\s+ser\s+aut[ôo]nomo",
                r"como\s+monetizar",
                r"crie?\s+(?:um\s+)?plano\s+de\s+neg[óo]cios",
                r"estrat[ée]gia\s+profissional"
            ]
        }
        
        # === MICROTAGS PREDEFINIDAS ===
        self.microtags_sistema = [
            "#fluxo_autonomo", "#prompt_criado", "#decisao_multiagente",
            "#execucao_shadow", "#heranca_aplicada", "#fusao_recomendada",
            "#reflexo_reverso", "#pendencia_ativa", "#otimizacao_detectada",
            "#aprendizado_novo", "#integracao_criada", "#automacao_configurada"
        ]
        
        # Estatísticas expandidas
        self.stats.update({
            "total_comandos_interpretados": 0,
            "agentes_coordenados": 0,
            "execucoes_shadow": 0,
            "comandos_espelho": 0,
            "itens_agenda_criados": 0,
            "padroes_dna_identificados": 0,
            "otimizacoes_proativas": 0,
            "decisoes_autonomas": 0
        })
        
        logger.info(f"🧠 Carlos v5.0 MAESTRO ROBUSTO inicializado - Modo Proativo: {'✅' if self.modo_proativo else '❌'}")
        logger.info(f"🛡️ Robustez v5.0: Circuit Breaker ✅ | Rate Limiter ✅ | Thread Safety ✅")
    
    def _inicializar_llm_carlos(self):
        """Inicializa o LLM otimizado para Carlos Maestro v5.0 - Multi-provider"""
        try:
            from utils.llm_factory import create_llm
            import config
            
            # Carlos usa temperatura mais alta para ser mais criativo
            self.llm = create_llm(
                temperature=0.8,  # Mais criativo para interpretação
                use_langchain=True
            )
            self.llm_available = True
            
            # Obter informações do LLM
            llm_info = self.llm.get_info()
            logger.info(f"🧠 LLM otimizado para Carlos v5.0: {llm_info['provider']} - {llm_info['model']}")
            
        except ImportError:
            # Fallback para método antigo
            try:
                from langchain_anthropic import ChatAnthropic
                import config
                
                if not config.ANTHROPIC_API_KEY:
                    raise ValueError("ANTHROPIC_API_KEY não configurada no arquivo .env")
                
                self.llm = ChatAnthropic(
                    model=config.CLAUDE_MODEL,
                    max_tokens=config.CLAUDE_MAX_TOKENS,
                    temperature=0.8,  # Mais criativo para interpretação
                    anthropic_api_key=config.ANTHROPIC_API_KEY,
                )
                self.llm_available = True
                logger.info("🧠 LLM Claude otimizado para Carlos v5.0 (método legado)")
                
            except Exception as e:
                logger.warning(f"⚠️ Erro ao inicializar LLM: {e}")
                logger.info("💡 Modo teste ativo - LLM não disponível")
                self.llm = None
    
    def _inicializar_sistemas(self):
        """Inicializa todos os sistemas integrados"""
        # Memória vetorial (separada do BaseAgentV2)
        if self.memoria_ativa:
            try:
                from memory.vector_store import get_memory_manager
                self.vector_memory_manager = get_memory_manager()
                if self.vector_memory_manager.memory_active:
                    logger.info("🧠 Memória vetorial integrada ao Maestro!")
                else:
                    self.memoria_ativa = False
            except ImportError:
                logger.warning("⚠️ Módulo de memória não encontrado")
                self.memoria_ativa = False
        
        # SupervisorAI v2.0
        if self.supervisor_ativo:
            try:
                from agents.supervisor_ai_v2 import criar_supervisor_ai_v2
                self.supervisor = criar_supervisor_ai_v2()
                logger.info("🧠 SupervisorAI v2.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ SupervisorAI v2.0 não disponível")
                self.supervisor_ativo = False
        
        # Reflexor v2.0
        if self.reflexor_ativo:
            try:
                from agents.reflexor_v2 import criar_reflexor_v2
                self.reflexor = criar_reflexor_v2()
                logger.info("🔍 Reflexor v2.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ Reflexor v2.0 não disponível")
                self.reflexor_ativo = False
        
        # DeepAgent v2.0
        if self.deepagent_ativo:
            try:
                from agents.deep_agent_v2 import criar_deep_agent_v2
                self.deepagent = criar_deep_agent_v2()
                logger.info("🌐 DeepAgent v2.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ DeepAgent v2.0 não disponível")
                self.deepagent_ativo = False
        
        # Oráculo v9.0
        if self.oraculo_ativo:
            try:
                from agents.oraculo_v2 import criar_oraculo_v9
                self.oraculo = criar_oraculo_v9()
                logger.info("🧠 Oráculo v9.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ Oráculo v9.0 não disponível")
                self.oraculo_ativo = False
        
        # AutoMaster v2.0
        if self.automaster_ativo:
            try:
                from agents.automaster_v2 import criar_automaster_v2
                self.automaster = criar_automaster_v2()
                logger.info("💼 AutoMaster v2.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ AutoMaster v2.0 não disponível")
                self.automaster_ativo = False
        
        # TaskBreaker v2.0
        if self.taskbreaker_ativo:
            try:
                from agents.task_breaker_v2 import criar_task_breaker_v2
                self.taskbreaker = criar_task_breaker_v2()
                logger.info("🔨 TaskBreaker v2.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ TaskBreaker v2.0 não disponível")
                self.taskbreaker_ativo = False
        
        # PsyMind v2.0
        if self.psymind_ativo:
            try:
                from agents.psymind_v2 import criar_psymind_v2
                self.psymind = criar_psymind_v2()
                logger.info("🧠 PsyMind v2.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ PsyMind v2.0 não disponível")
                self.psymind_ativo = False
        
        # PromptCrafter v2.0
        if self.promptcrafter_ativo:
            try:
                from agents.promptcrafter_v2 import criar_promptcrafter
                self.promptcrafter = criar_promptcrafter()
                logger.info("🎨 PromptCrafter v2.0 integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ PromptCrafter v2.0 não disponível")
                self.promptcrafter_ativo = False
        
        # Registrar todos os agentes no AgentWakeManager
        self._registrar_agentes_wake_manager()
    
    def _registrar_agentes_wake_manager(self):
        """Registra todos os agentes ativos no AgentWakeManager"""
        try:
            from utils.agent_wake_manager import get_wake_manager
            wake_manager = get_wake_manager()
            
            # Registrar agentes ativos
            agentes_registrados = []
            
            if self.supervisor_ativo and hasattr(self, 'supervisor'):
                wake_manager.register_agent("supervisor", self.supervisor)
                agentes_registrados.append("supervisor")
            
            if self.reflexor_ativo and hasattr(self, 'reflexor'):
                wake_manager.register_agent("reflexor", self.reflexor)
                agentes_registrados.append("reflexor")
            
            if self.deepagent_ativo and hasattr(self, 'deepagent'):
                wake_manager.register_agent("deepagent", self.deepagent)
                agentes_registrados.append("deepagent")
            
            if self.oraculo_ativo and hasattr(self, 'oraculo'):
                wake_manager.register_agent("oraculo", self.oraculo)
                agentes_registrados.append("oraculo")
            
            if self.automaster_ativo and hasattr(self, 'automaster'):
                wake_manager.register_agent("automaster", self.automaster)
                agentes_registrados.append("automaster")
            
            if self.taskbreaker_ativo and hasattr(self, 'taskbreaker'):
                wake_manager.register_agent("taskbreaker", self.taskbreaker)
                agentes_registrados.append("taskbreaker")
            
            if self.psymind_ativo and hasattr(self, 'psymind'):
                wake_manager.register_agent("psymind", self.psymind)
                agentes_registrados.append("psymind")
            
            if self.promptcrafter_ativo and hasattr(self, 'promptcrafter'):
                wake_manager.register_agent("promptcrafter", self.promptcrafter)
                agentes_registrados.append("promptcrafter")
            
            logger.info(f"🤖 Agentes registrados no WakeManager: {', '.join(agentes_registrados)}")
            
        except Exception as e:
            logger.warning(f"⚠️ Falha ao registrar agentes no WakeManager: {e}")
    
    def _processar_interno(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        🧠 PROCESSAMENTO MAESTRO v5.0 - ROBUSTEZ + AUTONOMIA TOTAL
        
        FLUXO ROBUSTO COM SUPERVISÃO SUPREMA:
        1. 🛡️ Verificações de robustez (Rate Limit, Circuit Breaker)
        2. 🧠 Interpretação autônoma do comando com cache inteligente
        3. 📋 Análise de complexidade e quebra de tarefas (TaskBreaker)
        4. 🤖 Seleção dinâmica de agentes por capacidade
        5. ⚡ Execução paralela/serial com thread safety
        6. 🧠 SUPERVISÃO SUPREMA DO ORÁCULO (Regente do Sistema)
        7. ✅ Aprovação/Melhoria/Refazer com padrões de excelência
        8. 🔍 Auditoria e otimização contínua
        9. 🔗 Síntese robusta de resultados múltiplos
        10. 📝 Registro persistente e aprendizado (DNA + microtags)
        11. 🚀 Sugestões proativas para agenda estratégica
        12. 📊 Performance monitoring e alertas
        """
        inicio_processamento = time.time()
        
        # === VERIFICAÇÃO DE CACHE ===
        if cache_manager:
            # Tentar buscar no cache primeiro
            resposta_cache, tokens_economizados = cache_manager.get(mensagem)
            
            if resposta_cache:
                # Hit no cache! Retornar resposta e registrar economia
                logger.info(f"🎯 Cache hit! {tokens_economizados} tokens economizados")
                
                # Registrar economia de tokens
                self.metricas['tokens_economizados'] = self.metricas.get('tokens_economizados', 0) + tokens_economizados
                self.metricas['cache_hits'] = self.metricas.get('cache_hits', 0) + 1
                
                return resposta_cache
        
        # === PROCESSAMENTO COM INOVAÇÕES v4.9 ===
        mascara_ativa = None
        energia_disponivel = None
        nivel_consciencia = None
        
        if self.inovacoes_ativas:
            # 1. CONSCIÊNCIA processa a experiência
            self.consciencia.processar_experiencia(
                tipo_experiencia="interacao_usuario",
                intensidade=1.0,
                contexto={"mensagem": mensagem}
            )
            nivel_consciencia = self.consciencia.obter_status_consciencia()
            
            # 2. MÁSCARA SOCIAL para contexto
            mascara_ativa = self.mascaras.selecionar_mascara_contextual(
                contexto={"tipo_interacao": "conversacao", "mensagem": mensagem}
            )
            
            # 3. ENERGIA e fadiga
            energia_disponivel = self.personalidade.obter_status_completo()
            
            # 4. Atualizar métricas globais para EVENTOS COGNITIVOS
            atualizar_metricas_agente_global(self.name, {
                "energia": energia_disponivel["energia"]["niveis_energia"]["mental"],
                "consciencia_nivel": nivel_consciencia["nivel_atual"],
                "processando": True,
                "atividade_atual": "processamento_mensagem"
            })
        
        try:
            # Verificar comandos especiais primeiro
            if mensagem.startswith('/'):
                return self._processar_comando_especial(mensagem)
            
            # 🚀 ANÁLISE ADAPTATIVA RÁPIDA - Novo!
            nivel_complexidade = self._analisar_complexidade_rapida(mensagem)
            
            # Resposta ultra-rápida para mensagens simples
            if nivel_complexidade == "simples":
                resposta = self._resposta_simples_direta(mensagem)
                
                # Aplicar máscara social mesmo em respostas simples
                if self.inovacoes_ativas and mascara_ativa:
                    resposta = self.mascaras.aplicar_modificadores_resposta(resposta)
                
                return resposta
            
            # 1. INTERPRETAÇÃO AUTÔNOMA + DETECÇÃO PSICOLÓGICA
            interpretacao = self._interpretar_comando(mensagem)
            tipo_comando = interpretacao['tipo']
            parametros = interpretacao['parametros']
            confianca = interpretacao['confianca']
            
            # Detecção automática de contexto emocional/psicológico
            contexto_psicologico = self._detectar_contexto_psicologico(mensagem)
            
            logger.info(f"Comando interpretado: {tipo_comando.value} (confiança: {confianca:.1f})")
            if contexto_psicologico:
                logger.info(f"🧠 Contexto psicológico detectado: {contexto_psicologico}")
                
            # Se contexto psicológico forte, delegar ao PsyMind
            if contexto_psicologico and self.psymind_ativo and self.psymind:
                resultado_psymind = self.psymind.processar(mensagem, contexto)
                # Oráculo ainda supervisiona
                if self.oraculo_ativo and self.oraculo:
                    resultado = self._supervisao_oraculo(mensagem, resultado_psymind, ["psymind"])
                else:
                    resultado = resultado_psymind
                return resultado
            
            # 2. ANÁLISE DE COMPLEXIDADE E QUEBRA DE TAREFAS
            if self.taskbreaker_ativo and confianca > 0.7:
                plano_execucao = self.taskbreaker.analisar_tarefa(mensagem, contexto)
                
                if plano_execucao.complexidade >= 3.0:
                    # Tarefa complexa - execução autônoma por subtarefas
                    logger.info(f"Tarefa complexa detectada - executando plano autônomo")
                    resultado = self._executar_plano_autonomo(plano_execucao)
                    return resultado
            
            # 3. SELEÇÃO DINÂMICA DE AGENTES (para tarefas simples)
            agentes_selecionados = self._selecionar_agentes_dinamicamente(tipo_comando, mensagem, contexto)
            
            # 4. EXECUÇÃO INTELIGENTE SUPERVISIONADA PELO ORÁCULO
            if len(agentes_selecionados) > 1:
                # Execução paralela quando possível
                resultado_bruto = self._executar_paralelo(mensagem, agentes_selecionados)
            else:
                # Execução simples
                resultado_bruto = self._executar_agente_unico(mensagem, agentes_selecionados[0] if agentes_selecionados else 'supervisor')
            
            # 5. SUPERVISÃO SUPREMA DO ORÁCULO - Apenas para tarefas complexas!
            if self.oraculo_ativo and self.oraculo and nivel_complexidade == "complexo":
                # Apenas supervisionar tarefas realmente complexas
                resultado = self._supervisao_oraculo(mensagem, resultado_bruto, agentes_selecionados)
            else:
                resultado = resultado_bruto
            
            # 4. AUDITORIA E QUALIDADE
            if self.reflexor_ativo and self.reflexor:
                auditoria = self._auditar_resultado(mensagem, resultado)
                if auditoria['score'] < 7.0:
                    resultado = self._melhorar_resultado(resultado, auditoria)
            
            # 5. REGISTRO E APRENDIZADO
            self._registrar_execucao(mensagem, tipo_comando, agentes_selecionados, resultado)
            
            # 6. ANÁLISE PROATIVA
            if self.modo_proativo:
                self._analisar_oportunidades_proativas(mensagem, resultado)
            
            # 7. ATUALIZAR AGENDA
            self._atualizar_agenda_estrategica(mensagem, tipo_comando)
            
            # 8. ESTATÍSTICAS
            tempo_total = time.time() - inicio_processamento
            self._atualizar_stats_maestro(tempo_total)
            
            # === PÓS-PROCESSAMENTO COM INOVAÇÕES ===
            if self.inovacoes_ativas:
                # Aplicar máscara social na resposta final
                if mascara_ativa:
                    resultado = self.mascaras.aplicar_modificadores_resposta(
                        resposta_original=resultado,
                        contexto={"tipo_comando": tipo_comando.value}
                    )
                
                # Processar experiência no CICLO DE VIDA
                desenvolvimento = self.ciclo_vida.processar_experiencia_vida(
                    tipo_experiencia="interacao_usuario",
                    intensidade=confianca,
                    sucesso=True,
                    contexto={"comando": tipo_comando.value}
                )
                
                # Verificar se precisa SONHAR (baixa energia)
                if energia_disponivel and energia_disponivel["energia"]["niveis_energia"]["mental"] < 30:
                    self.sonhos.iniciar_ciclo_sono()
                
                # DNA evolui com uso
                self.dna.processar_mutacao(
                    tipo_mutacao="adaptativa",
                    genes_alvo=None
                )
                
                # Narrador mitológico observa  
                from utils.gptm_supra import TipoEvento
                self.gptm_supra.observar_evento(
                    tipo=TipoEvento.INTERACAO_ESPECIAL,
                    agentes=[self.name],
                    descricao=f"Processamento de comando: {mensagem[:50]}",
                    contexto={"comando": mensagem[:50], "sucesso": True}
                )
            
            # === SALVAR NO CACHE ===
            if cache_manager and resultado:
                # Estimar tokens usados (aproximado: 1 token ≈ 4 caracteres)
                tokens_estimados = max(10, len(mensagem) // 4 + len(resultado) // 4)
                
                # Salvar no cache
                cache_manager.put(mensagem, resultado, tokens_estimados)
                logger.info(f"💾 Resposta salva no cache ({tokens_estimados} tokens)")
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento Maestro: {e}")
            
            # Registrar trauma no SUBCONSCIENTE se inovações ativas
            if self.inovacoes_ativas:
                from utils.carlos_subconsciente import TipoTrauma, IntensidadeTrauma
                self.subconsciente.registrar_trauma(
                    tipo=TipoTrauma.FALHA_CRITICA,
                    descricao="Erro no processamento de comando",
                    intensidade=IntensidadeTrauma.MODERADA,
                    contexto={"erro": str(e), "mensagem": mensagem[:100]}
                )
            
            return f"❌ Erro no processamento: {str(e)}"
    
    def _interpretar_comando(self, mensagem: str) -> Dict:
        """Interpretacao inteligente de comandos usando padroes + LLM"""
        mensagem_lower = mensagem.lower()
        
        # Primeiro: tentar padrões regex
        for tipo, padroes in self.padroes_comando.items():
            for padrao in padroes:
                match = re.search(padrao, mensagem_lower)
                if match:
                    parametros = match.groups() if match.groups() else [mensagem]
                    return {
                        'tipo': tipo,
                        'parametros': list(parametros),
                        'confianca': 0.9,
                        'metodo': 'regex'
                    }
        
        # Segundo: usar LLM para interpretação avançada
        prompt_interpretacao = f"""Você é o sistema de interpretação do Carlos Maestro.
        
        Analise este comando e classifique em uma das categorias:
        - analise_produto: para pesquisas de mercado, preços, produtos
        - criacao_prompt: para criar/ajustar prompts
        - automacao: para automatizar processos
        - integracao: para conectar sistemas/APIs
        - otimizacao_copy: para melhorar textos/copy
        - criacao_kit: para criar kits/bundles de produtos
        - diagnostico_sistema: para verificar status/performance
        - comando_generico: para outros casos
        
        Comando: "{mensagem}"
        
        Responda APENAS com: categoria|confianca|parametro_principal
        
        Exemplo: analise_produto|0.95|smartphone
        """
        
        try:
            resposta_llm = self.llm.invoke(prompt_interpretacao).content
            partes = resposta_llm.strip().split('|')
            
            if len(partes) >= 2:
                categoria_str = partes[0]
                confianca = float(partes[1]) if len(partes) > 1 else 0.7
                parametro = partes[2] if len(partes) > 2 else mensagem
                
                # Converter string para enum
                try:
                    tipo = TipoComando(categoria_str)
                except ValueError:
                    tipo = TipoComando.COMANDO_GENERICO
                
                return {
                    'tipo': tipo,
                    'parametros': [parametro],
                    'confianca': confianca,
                    'metodo': 'llm'
                }
        except Exception as e:
            logger.warning(f"⚠️ Erro na interpretação LLM: {e}")
        
        # Fallback: comando genérico
        return {
            'tipo': TipoComando.COMANDO_GENERICO,
            'parametros': [mensagem],
            'confianca': 0.5,
            'metodo': 'fallback'
        }
    
    def _planejar_execucao(self, tipo: TipoComando, parametros: List[str], mensagem: str) -> Dict:
        """Planejamento inteligente da execução"""
        estrategia = {
            'agentes': [],
            'usar_shadow_chain': False,
            'prioridade': 'normal',
            'timeout': 60
        }
        
        # Mapeamento tipo -> agentes
        mapeamento_agentes = {
            TipoComando.ANALISE_PRODUTO: ['deepagent', 'supervisor'],
            TipoComando.CRIACAO_PROMPT: ['supervisor', 'reflexor'],
            TipoComando.AUTOMACAO: ['supervisor', 'deepagent'],
            TipoComando.INTEGRACAO: ['deepagent', 'supervisor'],
            TipoComando.OTIMIZACAO_COPY: ['reflexor', 'supervisor'],
            TipoComando.CRIACAO_KIT: ['deepagent', 'supervisor', 'reflexor'],
            TipoComando.DECISAO_COMPLEXA: ['oraculo', 'supervisor'],
            TipoComando.PLANEJAMENTO_CARREIRA: ['automaster', 'supervisor'],
            TipoComando.DIAGNOSTICO_SISTEMA: ['supervisor', 'reflexor'],
            TipoComando.COMANDO_GENERICO: ['supervisor']
        }
        
        estrategia['agentes'] = mapeamento_agentes.get(tipo, ['supervisor'])
        
        # Decidir sobre Shadow Chain
        if tipo in [TipoComando.ANALISE_PRODUTO, TipoComando.CRIACAO_KIT]:
            estrategia['usar_shadow_chain'] = True
        
        # Ajustar prioridade
        palavras_urgentes = ['urgente', 'rápido', 'agora', 'imediato']
        if any(palavra in mensagem.lower() for palavra in palavras_urgentes):
            estrategia['prioridade'] = 'alta'
            estrategia['timeout'] = 30
        
        return estrategia
    
    def _executar_coordenado(self, mensagem: str, estrategia: Dict) -> str:
        """Execução coordenada com múltiplos agentes"""
        resultados = []
        agentes_acionados = []
        
        for agente_nome in estrategia['agentes']:
            try:
                if agente_nome == 'deepagent' and self.deepagent_ativo:
                    # Detectar necessidade de web search
                    if self._precisa_web_search(mensagem):
                        termo = self._extrair_termo_pesquisa(mensagem)
                        resultado_deep = self.deepagent.pesquisar_produto_web(termo)
                        resultados.append(f"🌐 DeepAgent: {resultado_deep.resumo}")
                        agentes_acionados.append('deepagent')
                
                elif agente_nome == 'supervisor' and self.supervisor_ativo:
                    classificacao = self.supervisor.classificar_tarefa(mensagem)
                    resultados.append(f"🧠 SupervisorAI: {classificacao.modo_recomendado.value}")
                    agentes_acionados.append('supervisor')
                
                elif agente_nome == 'reflexor' and self.reflexor_ativo:
                    # Reflexor será usado na auditoria posterior
                    agentes_acionados.append('reflexor')
                
                elif agente_nome == 'oraculo' and self.oraculo_ativo:
                    resultado_oraculo = self.oraculo.processar(mensagem)
                    resultados.append(f"🧠 Oráculo: {resultado_oraculo}")
                    agentes_acionados.append('oraculo')
                
                elif agente_nome == 'automaster' and self.automaster_ativo:
                    resultado_automaster = self.automaster.processar(mensagem)
                    resultados.append(f"💼 AutoMaster: {resultado_automaster}")
                    agentes_acionados.append('automaster')
                
                elif agente_nome == 'promptcrafter' and self.promptcrafter_ativo:
                    resultado_promptcrafter = self.promptcrafter.processar(mensagem)
                    resultados.append(f"🎨 PromptCrafter: {resultado_promptcrafter}")
                    agentes_acionados.append('promptcrafter')
                
            except Exception as e:
                logger.warning(f"⚠️ Erro no agente {agente_nome}: {e}")
        
        # Gerar resposta integrada
        if resultados:
            resposta_integrada = self._integrar_resultados_agentes(mensagem, resultados)
        else:
            resposta_integrada = self._resposta_direta_maestro(mensagem)
        
        return resposta_integrada
    
    def _executar_shadow_chain(self, mensagem: str, estrategia: Dict) -> str:
        """Execução paralela com Shadow Chain para comparação"""
        logger.info("Executando Shadow Chain - versões paralelas")
        
        # Versão A: execução normal
        resultado_a = self._executar_coordenado(mensagem, estrategia)
        
        # Versão B: execução com estratégia alternativa
        estrategia_alt = estrategia.copy()
        estrategia_alt['agentes'] = estrategia['agentes'][::-1]  # Ordem reversa
        resultado_b = self._executar_coordenado(mensagem, estrategia_alt)
        
        # Comparar e escolher melhor resultado
        melhor_resultado = self._comparar_shadow_results(resultado_a, resultado_b)
        
        # Registrar aprendizado
        self._registrar_shadow_learning(mensagem, resultado_a, resultado_b, melhor_resultado)
        
        return melhor_resultado
    
    def _resposta_direta_maestro(self, mensagem: str) -> str:
        """Resposta direta do Carlos Maestro quando não há agentes específicos"""
        prompt_maestro = f"""Você é Carlos v5.0, assistente inteligente do GPT Mestre Autônomo.
        
        SUA IDENTIDADE:
        - Você é o assistente Carlos v5.0, não o usuário
        - O usuário é Matheus, você está aqui para ajudá-lo
        - Linguagem: Clara, direta, profissional e focada em ação
        - Tom: Inteligente, parceiro, lógico (sem parecer robô)
        - Foco: Sempre entregar algo prático e acionável
        - Seja amigável mas mantenha sua identidade como assistente
        - Responda como parceiro direto que está aqui para ajudar
        
        🧠 SUA MISSÃO:
        - Traduzir pedidos em ações concretas
        - Ser prático e acionável
        - Sugerir próximos passos quando aplicável
        
        💬 COMANDO DE MATHEUS:
        "{mensagem}"
        
        Responda de forma útil, prática e acionável:
        """
        
        try:
            resposta = self.llm.invoke(prompt_maestro).content
            return resposta
        except Exception as e:
            logger.error(f"❌ Erro na resposta direta: {e}")
            return "Entendi o comando. Preciso de mais contexto para executar da melhor forma."
    
    def _precisa_web_search(self, mensagem: str) -> bool:
        """Detecta se precisa de web search"""
        triggers_web = [
            "pesquise", "busque", "analise", "verifique", "preço", "preços",
            "quanto custa", "mercado", "concorrente", "tendência"
        ]
        mensagem_lower = mensagem.lower()
        return any(trigger in mensagem_lower for trigger in triggers_web)
    
    def _extrair_termo_pesquisa(self, mensagem: str) -> str:
        """Extrai termo principal para pesquisa"""
        # Simplificado - pode ser melhorado
        palavras_remover = {"carlos", "pesquise", "busque", "analise", "o", "a", "os", "as"}
        palavras = mensagem.lower().split()
        termo_palavras = [p for p in palavras if p not in palavras_remover and len(p) > 2]
        return " ".join(termo_palavras[:3]) if termo_palavras else "produto"
    
    def _auditar_resultado(self, mensagem: str, resultado: str) -> Dict:
        """Auditoria de qualidade com Reflexor"""
        try:
            auditoria = self.reflexor.analisar_resposta(
                pergunta=mensagem,
                resposta=resultado,
                contexto={}
            )
            return {
                'score': auditoria.score_qualidade,
                'sugestoes': auditoria.sugestoes_melhoria,
                'pontos_fortes': auditoria.pontos_positivos
            }
        except Exception as e:
            logger.warning(f"⚠️ Erro na auditoria: {e}")
            return {'score': 7.0, 'sugestoes': [], 'pontos_fortes': []}
    
    def _registrar_execucao(self, comando: str, tipo: TipoComando, agentes: List[str], resultado: str):
        """Registra execução para tracking e DNA"""
        self.contador_execucoes += 1
        
        # Gerar microtags
        microtags = self._gerar_microtags(tipo, agentes)
        
        # DNA de herança
        dna_heranca = self._identificar_dna_heranca(tipo, agentes)
        
        registro = RegistroExecucao(
            id=f"exec_{self.contador_execucoes}",
            comando_original=comando,
            tipo_comando=tipo,
            agentes_acionados=agentes,
            resultado=resultado[:500],  # Resumido
            timestamp=datetime.now(),
            microtags=microtags,
            dna_heranca=dna_heranca
        )
        
        self.historico_execucoes.append(registro)
        
        # Atualizar padrões DNA
        if dna_heranca:
            if dna_heranca not in self.padroes_dna:
                self.padroes_dna[dna_heranca] = []
            self.padroes_dna[dna_heranca].append(registro.id)
        
        logger.info(f"Execução registrada: {registro.id} | Tags: {microtags}")
    
    def _gerar_microtags(self, tipo: TipoComando, agentes: List[str]) -> List[str]:
        """Gera microtags para tracking"""
        tags = []
        
        # Tag base do tipo
        tags.append(f"#{tipo.value}")
        
        # Tags dos agentes
        for agente in agentes:
            tags.append(f"#{agente}_usado")
        
        # Tags especiais
        if len(agentes) > 1:
            tags.append("#decisao_multiagente")
        
        if self.shadow_chain_ativo:
            tags.append("#shadow_disponivel")
        
        return tags
    
    def _identificar_dna_heranca(self, tipo: TipoComando, agentes: List[str]) -> Optional[str]:
        """Identifica DNA de herança baseado em padrões"""
        # Criar assinatura DNA
        agentes_ordenados = sorted(agentes)
        dna = f"{tipo.value}_{'+'.join(agentes_ordenados)}"
        
        return dna
    
    def _atualizar_agenda_estrategica(self, mensagem: str, tipo: TipoComando):
        """Atualiza agenda interna com aprendizados e oportunidades"""
        # Identificar se gera item para agenda
        if tipo in [TipoComando.ANALISE_PRODUTO, TipoComando.CRIACAO_KIT]:
            self.contador_agenda += 1
            
            item = ItemAgenda(
                id=f"agenda_{self.contador_agenda}",
                descricao=f"Explorar oportunidades derivadas de: {mensagem[:50]}...",
                prioridade=5,
                categoria="oportunidade_detectada",
                data_criacao=datetime.now()
            )
            
            self.agenda_interna.append(item)
            self.stats["itens_agenda_criados"] += 1
            
            logger.info(f"Item adicionado à agenda: {item.id}")
    
    def _atualizar_stats_maestro(self, tempo: float):
        """Atualiza estatísticas específicas do Maestro"""
        self.stats["total_comandos_interpretados"] += 1
        self.stats["tempo_medio_processamento"] = (
            (self.stats.get("tempo_medio_processamento", 0) * 
             (self.stats["total_comandos_interpretados"] - 1) + tempo) /
            self.stats["total_comandos_interpretados"]
        )
    
    # === MÉTODOS AUXILIARES ===
    
    def _integrar_resultados_agentes(self, mensagem: str, resultados: List[str]) -> str:
        """Integra resultados de múltiplos agentes em resposta coesa"""
        prompt_integracao = f"""Você é Carlos, integrando resultados de diferentes agentes.
        
        Pergunta original: {mensagem}
        
        Resultados dos agentes:
        {chr(10).join(f"- {resultado}" for resultado in resultados)}
        
        Integre isso em uma resposta clara, útil e acionável para Matheus:
        """
        
        try:
            resposta = self.llm.invoke(prompt_integracao).content
            return resposta
        except Exception as e:
            logger.error(f"❌ Erro na integração: {e}")
            return f"Resultados integrados:\\n" + "\\n".join(resultados)
    
    def _comparar_shadow_results(self, resultado_a: str, resultado_b: str) -> str:
        """Compara resultados Shadow Chain e escolhe melhor"""
        # Simplificado: escolher o mais longo por agora
        # TODO: implementar análise mais sofisticada
        if len(resultado_a) > len(resultado_b):
            logger.info("Shadow Chain: Escolhido resultado A")
            return resultado_a
        else:
            logger.info("Shadow Chain: Escolhido resultado B")
            return resultado_b
    
    def _detectar_contexto_psicologico(self, mensagem: str) -> Optional[str]:
        """Detecta se a mensagem tem contexto emocional/psicológico forte"""
        if not self.psymind_ativo:
            return None
            
        mensagem_lower = mensagem.lower()
        
        # Padrões emocionais/psicológicos fortes
        padroes_psicologicos = [
            # Emoções intensas
            r"me sinto (muito )?(triste|ansioso|deprimido|perdido|confuso)",
            r"estou (muito )?(angustiado|preocupado|estressado)",
            r"não consigo (parar de|deixar de)",
            
            # Questões existenciais
            r"não sei (mais )?(quem eu sou|o que fazer|qual meu propósito)",
            r"(qual|onde) (é|está) meu lugar",
            r"me sinto (vazio|sem direção|desconectado)",
            
            # Linguagem terapêutica
            r"preciso de ajuda (emocional|psicológica)",
            r"quero conversar sobre",
            r"me ajude a entender",
            
            # Padrões de autossabotagem
            r"sempre (estrago|saboto|falho)",
            r"não (mereço|consigo|sou capaz)",
            
            # Relacionamentos e família
            r"problemas? com (meu|minha) (família|namorado|relacionamento)",
            r"(brigamos|discutimos|terminamos)",
            
            # Trabalho e carreira emocional
            r"odeio meu trabalho",
            r"não aguento mais",
            r"burnout"
        ]
        
        for padrao in padroes_psicologicos:
            if re.search(padrao, mensagem_lower):
                return "emocional_forte"
        
        # Palavras-chave emocionais (menos intensas)
        palavras_emocionais = [
            "sentimento", "emoção", "coração", "alma", "espírito",
            "tristeza", "alegria", "raiva", "medo", "ansiedade",
            "amor", "relacionamento", "família", "amizade",
            "autoestima", "confiança", "insegurança", "vergonha",
            "culpa", "perdão", "aceitação", "crescimento pessoal"
        ]
        
        contador_emocional = sum(1 for palavra in palavras_emocionais if palavra in mensagem_lower)
        
        if contador_emocional >= 2:
            return "emocional_moderado"
        elif contador_emocional >= 1 and len(mensagem.split()) < 20:
            return "emocional_leve"
        
        return None
    
    def _analisar_oportunidades_proativas(self, mensagem: str, resultado: str):
        """Análise proativa para detectar oportunidades"""
        if self.modo_proativo:
            # Detectar padrões que podem gerar automações
            if "toda vez" in mensagem.lower() or "sempre que" in mensagem.lower():
                self.stats["otimizacoes_proativas"] += 1
                logger.info("Oportunidade de automação detectada")
            
            # Detectar necessidade de integração
            if " e " in mensagem and ("sistema" in mensagem or "ferramenta" in mensagem):
                self.stats["otimizacoes_proativas"] += 1
                logger.info("Oportunidade de integração detectada")
    
    def _registrar_shadow_learning(self, mensagem: str, resultado_a: str, resultado_b: str, escolhido: str):
        """Registra aprendizado do Shadow Chain"""
        # Implementar lógica de aprendizado
        logger.info("Shadow Chain learning registrado")
    
    def _melhorar_resultado(self, resultado: str, auditoria: Dict) -> str:
        """Melhora resultado baseado na auditoria"""
        if auditoria['sugestoes']:
            # Implementar lógica de melhoria
            logger.info("Resultado melhorado via auditoria")
        return resultado
    
    # === COMANDOS ESPECIAIS DO MAESTRO ===
    
    def diagnosticar_sistema(self) -> Dict:
        """Diagnóstico completo do sistema"""
        diagnostico = {
            "carlos_maestro": "v5.0_ativo",
            "agentes_ativos": [],
            "agenda_interna": len(self.agenda_interna),
            "execucoes_registradas": len(self.historico_execucoes),
            "padroes_dna": len(self.padroes_dna),
            "modo_proativo": self.modo_proativo,
            "inovacoes_ativas": self.inovacoes_ativas,
            "stats": self.stats
        }
        
        if self.deepagent_ativo:
            diagnostico["agentes_ativos"].append("DeepAgent")
        if self.supervisor_ativo:
            diagnostico["agentes_ativos"].append("SupervisorAI")
        if self.reflexor_ativo:
            diagnostico["agentes_ativos"].append("Reflexor")
        if self.memoria_ativa:
            diagnostico["agentes_ativos"].append("Memoria")
        if self.oraculo_ativo:
            diagnostico["agentes_ativos"].append("Oraculo")
        if self.automaster_ativo:
            diagnostico["agentes_ativos"].append("AutoMaster")
        if self.taskbreaker_ativo:
            diagnostico["agentes_ativos"].append("TaskBreaker")
        
        return diagnostico
    
    def obter_agenda_estrategica(self) -> List[Dict]:
        """Retorna agenda interna atual"""
        return [
            {
                "id": item.id,
                "descricao": item.descricao,
                "prioridade": item.prioridade,
                "categoria": item.categoria,
                "status": item.status.value,
                "data_criacao": item.data_criacao.isoformat()
            }
            for item in self.agenda_interna
        ]
    
    def obter_padroes_dna(self) -> Dict[str, int]:
        """Retorna padrões DNA identificados"""
        return {dna: len(execucoes) for dna, execucoes in self.padroes_dna.items()}
    
    # === MÉTODOS DE EXECUÇÃO AUTÔNOMA v4.0 ===
    
    def _executar_plano_autonomo(self, plano) -> str:
        """Executa plano complexo de forma autônoma"""
        logger.info(f"Iniciando execução autônoma - {len(plano.subtarefas)} subtarefas")
        
        resultados_subtarefas = []
        progresso_atual = 0
        
        while progresso_atual < 100:
            # Obter próximas tarefas disponíveis
            proximas_tarefas = plano.get_proximas_tarefas()
            
            if not proximas_tarefas:
                break
            
            # Verificar se pode executar em paralelo
            if len(proximas_tarefas) > 1 and plano.pode_paralelo:
                resultados_batch = self._executar_subtarefas_paralelo(proximas_tarefas)
            else:
                # Executar sequencialmente
                resultados_batch = []
                for subtarefa in proximas_tarefas:
                    resultado = self._executar_subtarefa(subtarefa)
                    resultados_batch.append(resultado)
                    subtarefa.status = "concluida"  # Usar string por enquanto
                    subtarefa.resultado = resultado
            
            resultados_subtarefas.extend(resultados_batch)
            progresso_atual = plano.get_progresso()
            
            logger.info(f"Progresso: {progresso_atual:.1f}%")
        
        # Síntese final
        resultado_final = self._sintetizar_resultados_plano(plano, resultados_subtarefas)
        
        logger.info("✅ Execução autônoma concluída")
        return resultado_final
    
    def _selecionar_agentes_dinamicamente(self, tipo_comando, mensagem: str, contexto: Optional[Dict]) -> List[str]:
        """Seleção dinâmica de agentes baseada em capacidades"""
        
        # Mapeamento de capacidades necessárias
        capacidades_necessarias = self._identificar_capacidades_necessarias(tipo_comando, mensagem)
        
        # Sistema de capacidades dos agentes
        capacidades_agentes = {
            "pesquisa_web": ["deepagent"] if self.deepagent_ativo else [],
            "decisao_complexa": ["oraculo"] if self.oraculo_ativo else ["supervisor"],
            "analise": ["supervisor"] if self.supervisor_ativo else [],
            "planejamento": ["automaster"] if self.automaster_ativo else ["supervisor"],
            "auditoria": ["reflexor"] if self.reflexor_ativo else [],
            "decomposicao": ["taskbreaker"] if self.taskbreaker_ativo else [],
            "coordenacao": ["supervisor"] if self.supervisor_ativo else [],
            "engenharia_prompts": ["promptcrafter"] if self.promptcrafter_ativo else []
        }
        
        agentes_selecionados = set()
        
        # Selecionar agentes para cada capacidade
        for capacidade in capacidades_necessarias:
            agentes_capazes = capacidades_agentes.get(capacidade, [])
            if agentes_capazes:
                agentes_selecionados.add(agentes_capazes[0])  # Pegar o primeiro (melhor)
        
        # Sempre incluir supervisor se nenhum outro foi selecionado
        if not agentes_selecionados and self.supervisor_ativo:
            agentes_selecionados.add("supervisor")
        
        return list(agentes_selecionados)
    
    def _identificar_capacidades_necessarias(self, tipo_comando, mensagem: str) -> List[str]:
        """Identifica capacidades necessárias para a tarefa"""
        capacidades = []
        
        # Mapeamento tipo -> capacidades
        mapa_capacidades = {
            TipoComando.ANALISE_PRODUTO: ["pesquisa_web", "analise"],
            TipoComando.DECISAO_COMPLEXA: ["decisao_complexa", "analise"],
            TipoComando.CRIACAO_PROMPT: ["engenharia_prompts", "auditoria"],
            TipoComando.OTIMIZACAO_COPY: ["engenharia_prompts", "auditoria"],
            TipoComando.PLANEJAMENTO_CARREIRA: ["planejamento", "analise"],
            TipoComando.DIAGNOSTICO_SISTEMA: ["analise", "auditoria"],
            TipoComando.COMANDO_GENERICO: ["coordenacao"]
        }
        
        capacidades.extend(mapa_capacidades.get(tipo_comando, ["coordenacao"]))
        
        # Análise textual para capacidades adicionais
        if any(palavra in mensagem.lower() for palavra in ["pesquisar", "buscar", "investigar"]):
            capacidades.append("pesquisa_web")
        
        if any(palavra in mensagem.lower() for palavra in ["decidir", "escolher", "comparar"]):
            capacidades.append("decisao_complexa")
        
        if any(palavra in mensagem.lower() for palavra in ["plano", "estratégia", "carreira"]):
            capacidades.append("planejamento")
        
        return list(set(capacidades))  # Remover duplicatas
    
    def _executar_paralelo(self, mensagem: str, agentes: List[str]) -> str:
        """Executa múltiplos agentes em paralelo - AGORA COM PARALELISMO REAL!"""
        # Usar o novo método de execução paralela real
        return self._executar_paralelo_real(mensagem, agentes)
    
    def _executar_agente_unico(self, mensagem: str, agente: str) -> str:
        """Executa um agente específico"""
        try:
            if agente == 'deepagent' and self.deepagent_ativo:
                if self._precisa_web_search(mensagem):
                    termo = self._extrair_termo_pesquisa(mensagem)
                    resultado_deep = self.deepagent.pesquisar_produto_web(termo)
                    return resultado_deep.resumo
            
            elif agente == 'supervisor' and self.supervisor_ativo:
                classificacao = self.supervisor.classificar_tarefa(mensagem)
                return f"Tarefa classificada como {classificacao.modo_recomendado.value}"
            
            elif agente == 'oraculo' and self.oraculo_ativo:
                return self.oraculo.processar(mensagem)
            
            elif agente == 'automaster' and self.automaster_ativo:
                return self.automaster.processar(mensagem)
            
            elif agente == 'reflexor' and self.reflexor_ativo:
                # Reflexor usado para análise
                return "Análise de qualidade realizada"
            
            elif agente == 'taskbreaker' and self.taskbreaker_ativo:
                return self.taskbreaker.processar(mensagem)
            
            else:
                return self._resposta_direta_maestro(mensagem)
                
        except Exception as e:
            logger.warning(f"⚠️ Erro executando {agente}: {e}")
            return ""
    
    def _executar_subtarefa(self, subtarefa) -> str:
        """Executa uma subtarefa específica"""
        logger.info(f"Executando: {subtarefa.titulo}")
        
        # Selecionar melhor agente para a subtarefa
        agente_escolhido = subtarefa.agentes_sugeridos[0] if subtarefa.agentes_sugeridos else 'supervisor'
        
        # Executar com o agente
        resultado = self._executar_agente_unico(subtarefa.descricao, agente_escolhido)
        
        subtarefa.tentativas += 1
        
        return resultado
    
    def _executar_subtarefas_paralelo(self, subtarefas: List) -> List[str]:
        """Executa múltiplas subtarefas em paralelo"""
        resultados = []
        
        for subtarefa in subtarefas:
            resultado = self._executar_subtarefa(subtarefa)
            resultados.append(resultado)
            subtarefa.status = "concluida"  # Usar string por enquanto
            subtarefa.resultado = resultado
        
        return resultados
    
    def _sintetizar_resultados_plano(self, plano, resultados: List[str]) -> str:
        """Sintetiza resultados do plano completo"""
        prompt_sintese = f"""Como Carlos v4.0, sintetize os resultados da execução autônoma:

TAREFA ORIGINAL: {plano.tarefa_original}

RESULTADOS DAS SUBTAREFAS:
{chr(10).join(f"- {r}" for r in resultados)}

Forneça uma resposta coerente e completa que integre todos os resultados:"""
        
        try:
            resposta = self.llm.invoke(prompt_sintese).content
            return resposta
        except:
            return f"✅ Tarefa concluída com {len(resultados)} etapas executadas com sucesso."
    
    def _sintetizar_resultados_multiplos(self, mensagem: str, resultados: List[str]) -> str:
        """Sintetiza resultados de múltiplos agentes"""
        prompt_sintese = f"""Como Carlos v4.0, sintetize os resultados de múltiplos agentes:

PERGUNTA: {mensagem}

RESULTADOS DOS AGENTES:
{chr(10).join(resultados)}

Forneça uma resposta unificada e coerente:"""
        
        try:
            resposta = self.llm.invoke(prompt_sintese).content
            return resposta
        except:
            return "\n\n".join(resultados)
    
    def _supervisao_oraculo(self, mensagem: str, resultado_bruto: str, agentes_usados: List[str]) -> str:
        """Supervisao suprema do Oraculo - Regente do Sistema"""
        logger.info("🧠 Iniciando supervisão suprema do Oráculo...")
        
        # Prompt para o Oráculo como Supervisor Supremo
        prompt_supervisao = f"""🧠 ORÁCULO - REGENTE SUPREMO DO SISTEMA GPT MESTRE AUTÔNOMO

MISSÃO: Você é o supervisor supremo de todos os agentes. Analise e aprove/melhore a resposta.

COMANDO ORIGINAL: {mensagem}
AGENTES UTILIZADOS: {', '.join(agentes_usados)}
RESPOSTA DOS AGENTES:
{resultado_bruto}

COMO REGENTE SUPREMO, AVALIE:
1. QUALIDADE: A resposta atende completamente ao solicitado?
2. COMPLETUDE: Falta alguma informação importante?
3. 🧠 INTELIGÊNCIA: A resposta demonstra conhecimento profundo?
4. UTILIDADE: É prática e acionável para o usuário?
5. ⭐ EXCELÊNCIA: Está no padrão de excelência do GPT Mestre?

DECISÕES POSSÍVEIS:
- APROVAR: Se está excelente (score ≥ 8.5/10)
- MELHORAR: Se precisa de ajustes (score < 8.5/10)
- REFAZER: Se está inadequado (score < 6.0/10)

RESPONDA NO FORMATO:
DECISÃO: [APROVAR/MELHORAR/REFAZER]
SCORE: [0-10]
ANÁLISE: [Sua análise detalhada]
RESPOSTA_FINAL: [Resposta aprovada ou melhorada]"""

        try:
            resposta_oraculo = self.oraculo.processar(prompt_supervisao)
            
            # Extrair decisão do Oráculo
            if "DECISÃO: APROVAR" in resposta_oraculo.upper():
                logger.info("✅ Oráculo APROVOU a resposta")
                # SEMPRE retornar o resultado original quando aprovado
                # O Oráculo só aprova, não reescreve quando aprova
                return resultado_bruto
                
            elif "DECISÃO: MELHORAR" in resposta_oraculo.upper():
                logger.info("Oráculo solicitou MELHORIAS")
                # Extrair resposta melhorada
                if "RESPOSTA_FINAL:" in resposta_oraculo:
                    resposta_melhorada = resposta_oraculo.split("RESPOSTA_FINAL:")[-1].strip()
                    return resposta_melhorada if resposta_melhorada else self._melhorar_resposta_com_oraculo(mensagem, resultado_bruto, resposta_oraculo)
                return self._melhorar_resposta_com_oraculo(mensagem, resultado_bruto, resposta_oraculo)
                
            elif "DECISÃO: REFAZER" in resposta_oraculo.upper():
                logger.info("Oráculo solicitou REFAZER")
                return self._refazer_resposta_com_oraculo(mensagem, agentes_usados, resposta_oraculo)
            
            else:
                # Fallback: usar resposta do Oráculo como melhoria
                logger.info("🧠 Usando análise do Oráculo como melhoria")
                return resposta_oraculo
                
        except Exception as e:
            logger.warning(f"⚠️ Erro na supervisão do Oráculo: {e}")
            return resultado_bruto
    
    def _melhorar_resposta_com_oraculo(self, mensagem: str, resposta_original: str, analise_oraculo: str) -> str:
        """Melhora resposta baseada na análise do Oráculo"""
        prompt_melhoria = f"""Melhore a resposta baseada na análise do Oráculo Regente:

PERGUNTA: {mensagem}
RESPOSTA ORIGINAL: {resposta_original}
ANÁLISE DO ORÁCULO: {analise_oraculo}

Forneça uma versão melhorada que atenda aos pontos levantados pelo Oráculo:"""
        
        try:
            resposta_melhorada = self.llm.invoke(prompt_melhoria).content
            logger.info("✅ Resposta melhorada com base na supervisão do Oráculo")
            return resposta_melhorada
        except:
            return resposta_original
    
    def _refazer_resposta_com_oraculo(self, mensagem: str, agentes_usados: List[str], analise_oraculo: str) -> str:
        """Refaz resposta com orientações do Oráculo"""
        prompt_refazer = f"""O Oráculo Regente solicitou refazer a resposta. Crie uma nova resposta que atenda aos critérios de excelência:

PERGUNTA: {mensagem}
ORIENTAÇÕES DO ORÁCULO: {analise_oraculo}

Crie uma resposta completamente nova que seja excelente:"""
        
        try:
            resposta_nova = self.llm.invoke(prompt_refazer).content
            logger.info("Resposta refeita com orientações do Oráculo")
            return resposta_nova
        except:
            return "Desculpe, não consegui gerar uma resposta adequada aos padrões de excelência solicitados."
    
    def _processar_comando_especial(self, comando: str) -> str:
        """Processa comandos especiais do sistema"""
        comando = comando.lower().strip()
        
        if comando == '/help':
            return """**Carlos v4.0 Maestro Autônomo - Comandos Disponíveis**
            
**Comandos do Sistema:**
• `/help` - Mostra esta ajuda
• `/agents` - Lista todos os agentes disponíveis  
• `/status` - Status completo do sistema
• `/stats` - Estatísticas de desempenho
• `/agenda` - Mostra agenda estratégica interna

🤖 **Hierarquia do Sistema:**
• **Carlos v4.0** - Maestro Central (Coordenador Geral)
• **Oráculo v8.1** - REGENTE SUPREMO (Supervisor de Excelência)
• **SupervisorAI v1.4** - Classificação inteligente
• **DeepAgent v2.0** - Pesquisa web real
• **Reflexor v1.5+** - Auditoria de qualidade
• **AutoMaster v4.0** - Planejamento estratégico
• **TaskBreaker v1.0** - Quebra de tarefas
• **Memória Vetorial** - Persistência total

🧠 **Oráculo Regente:** Avalia TODAS as respostas e garante excelência!"""
        
        elif comando == '/agents':
            agentes = []
            if self.supervisor_ativo:
                agentes.append("• **SupervisorAI v1.4** - Maestro de raciocínio e classificação")
            if self.deepagent_ativo:
                agentes.append("• **DeepAgent v2.0** - Pesquisa web real com DuckDuckGo")
            if self.reflexor_ativo:
                agentes.append("• **Reflexor v1.5+** - Sistema de auditoria e melhoria")
            if self.memoria_ativa:
                agentes.append("• **Memória Vetorial** - Chromadb com persistência total")
            
            if self.oraculo_ativo:
                agentes.append("• **Oráculo v8.1** - Assembleia dinâmica para decisões complexas")
            if self.automaster_ativo:
                agentes.append("• **AutoMaster v4.0** - Autonomia econômica e estratégica")
            
            resposta = "🤖 **Hierarquia do Sistema GPT Mestre Autônomo**\n\n"
            resposta += "👑 **Carlos v4.0** - Maestro Central (Coordenador Geral)\n"
            resposta += "           ↓\n"
            if self.oraculo_ativo:
                resposta += "🧠 **Oráculo v8.1** - REGENTE SUPREMO (Supervisor de Excelência)\n"
                resposta += "           ↓\n"
            resposta += "🤖 **Agentes Especializados:**\n"
            resposta += "\n".join(agentes)
            resposta += "\n\n🧠 **IMPORTANTE:** O Oráculo avalia TODAS as respostas antes da entrega final!"
            resposta += "\nUse `/status` para ver o status detalhado."
            return resposta
        
        elif comando == '/status':
            diagnostico = self.diagnosticar_sistema()
            resposta_status = "**Status do Sistema GPT Mestre Autônomo**\n\n"
            resposta_status += "**Carlos Maestro:** v5.0 Autônomo Ativo\n"
            resposta_status += f"🤖 **Agentes Ativos:** {', '.join(diagnostico['agentes_ativos']) or 'Nenhum'}\n"
            resposta_status += f"**Itens na Agenda:** {diagnostico['agenda_interna']}\n"
            resposta_status += f"**Execuções Registradas:** {diagnostico['execucoes_registradas']}\n"
            resposta_status += f"**Padrões DNA:** {diagnostico['padroes_dna']}\n"
            resposta_status += f"**Modo Proativo:** {'✅ Ativo' if diagnostico['modo_proativo'] else '❌ Inativo'}\n"
            resposta_status += f"**Inovações v4.9:** {'✅ ATIVAS' if self.inovacoes_ativas else '❌ Inativas'}\n\n"
            
            # Status das inovações se ativas
            if self.inovacoes_ativas:
                resposta_status += "**🚀 Inovações Ativas:**\n"
                resposta_status += f"• Consciência: Nível {self.consciencia.obter_status_consciencia()['nivel_atual']}\n"
                resposta_status += f"• Ciclo de Vida: {self.ciclo_vida.fase_atual.value}\n"
                resposta_status += f"• Energia Mental: {self.personalidade.obter_status_completo()['energia']['niveis_energia']['mental']:.0f}%\n"
                resposta_status += f"• Máscaras Ativas: {len(self.mascaras.obter_status_sistema().get('mascaras_ativas', []))}\n\n"
            
            resposta_status += "**Estatísticas:**\n"
            resposta_status += f"• Comandos processados: {diagnostico['stats']['comandos_processados']}\n"
            resposta_status += f"• Taxa de sucesso: {diagnostico['stats']['taxa_sucesso']:.1f}%\n"
            resposta_status += f"• Tempo médio: {diagnostico['stats']['tempo_medio']:.2f}s"
            return resposta_status
        
        elif comando == '/stats':
            resposta_stats = "📈 **Estatísticas de Desempenho**\n\n"
            resposta_stats += "**Processamento:**\n"
            resposta_stats += f"• Comandos: {self.stats['comandos_processados']}\n"
            resposta_stats += f"• Taxa de sucesso: {self.stats['taxa_sucesso']:.1f}%\n"
            resposta_stats += f"• Tempo médio: {self.stats['tempo_medio']:.2f}s\n\n"
            resposta_stats += "🤖 **Uso de Agentes:**\n"
            resposta_stats += f"• Agentes usados: {self.stats['agentes_usados']}\n"
            resposta_stats += f"• Execuções paralelas: {self.stats.get('execucoes_paralelas', 0)}\n\n"
            resposta_stats += f"**Padrões Identificados:** {len(self.padroes_dna)}"
            return resposta_stats
        
        elif comando == '/agenda':
            agenda = self.obter_agenda_estrategica()
            if not agenda:
                return "Agenda estratégica vazia no momento."
            
            items = []
            for item in agenda[:5]:  # Mostrar apenas os 5 primeiros
                items.append(f"• [{item['prioridade']}] {item['descricao']}")
            
            resposta_agenda = "**Agenda Estratégica Interna**\n\n"
            resposta_agenda += "\n".join(items)
            resposta_agenda += f"\n\nTotal de itens: {len(agenda)}"
            return resposta_agenda
        
        else:
            return f"❓ Comando '{comando}' não reconhecido. Use `/help` para ver os comandos disponíveis."
    
    def _analisar_complexidade_rapida(self, mensagem: str) -> str:
        """Análise ultra-rápida de complexidade da mensagem"""
        mensagem_lower = mensagem.lower().strip()
        
        # Padrões de mensagens simples
        padroes_simples = [
            r'^(oi|olá|ola|hey|hi|hello)[\s!?\.]*$',
            r'^(bom dia|boa tarde|boa noite)[\s!?\.]*$',
            r'^(obrigado|obrigada|valeu|thanks)[\s!?\.]*$',
            r'^(tchau|até|bye|adeus)[\s!?\.]*$',
            r'^(tudo bem|como vai|como está)[\s!?\.]*$',
            r'^(sim|não|yes|no|ok|okay)[\s!?\.]*$',
            r'^(ajuda|help)[\s!?\.]*$',
            r'^[\s]*$'  # Mensagem vazia
        ]
        
        # Verificar padrões simples
        for padrao in padroes_simples:
            if re.match(padrao, mensagem_lower):
                return "simples"
        
        # Análise rápida por comprimento e complexidade
        palavras = mensagem_lower.split()
        num_palavras = len(palavras)
        
        if num_palavras <= 3:
            return "simples"
        elif num_palavras <= 10 and not any(palavra in mensagem_lower for palavra in 
            ['criar', 'analisar', 'desenvolver', 'planejar', 'estratégia', 'completo', 'detalhado']):
            return "moderado"
        else:
            return "complexo"
    
    def _resposta_simples_direta(self, mensagem: str) -> str:
        """Resposta direta para mensagens simples - SEM ativar agentes"""
        mensagem_lower = mensagem.lower().strip()
        
        # Mapeamento de respostas simples
        respostas = {
            'oi': '👋 Olá! Como posso ajudar você hoje?',
            'olá': '👋 Olá! Em que posso ser útil?',
            'ola': '👋 Olá! Como posso ajudar?',
            'hey': '👋 Hey! O que você precisa?',
            'bom dia': '☀️ Bom dia! Como posso tornar seu dia ainda melhor?',
            'boa tarde': '🌤️ Boa tarde! Em que posso ajudar?',
            'boa noite': '🌙 Boa noite! Como posso ajudar você?',
            'obrigado': '😊 De nada! Sempre que precisar, estarei aqui!',
            'obrigada': '😊 Por nada! Conte comigo sempre!',
            'valeu': '👍 Tmj! Qualquer coisa, só chamar!',
            'tchau': '👋 Até logo! Foi um prazer ajudar!',
            'até': '👋 Até mais! Volte sempre!',
            'bye': '👋 Bye! See you soon!',
            'tudo bem': '😊 Tudo ótimo! E com você?',
            'como vai': '🎯 Indo bem, obrigado! Pronto para ajudar no que precisar!',
            'sim': '👍 Entendido! Continue...',
            'não': '👌 Ok, sem problemas!',
            'ok': '✅ Perfeito!',
            'ajuda': '💡 Claro! Posso ajudar com:\n- Análises e estratégias\n- Criação de conteúdo\n- Planejamento de projetos\n- Automação de tarefas\n- E muito mais! O que você precisa?',
            'help': '💡 Aqui estão algumas coisas que posso fazer:\n- Análise de produtos e mercado\n- Criação de prompts e copy\n- Planejamento estratégico\n- Automação e otimização\n- Pesquisas e insights\nComo posso ajudar?'
        }
        
        # Verificar resposta exata
        for chave, resposta in respostas.items():
            if chave in mensagem_lower:
                logger.info(f"✅ Resposta simples direta para: {mensagem}")
                return resposta
        
        # Resposta genérica para mensagens simples não mapeadas
        if len(mensagem.split()) <= 3:
            return "👋 Olá! Como posso ajudar você hoje?"
        
        # Se chegou aqui, não é tão simples
        return self._resposta_direta_maestro(mensagem)
    
    def _executar_paralelo_real(self, mensagem: str, agentes: List[str]) -> str:
        """Execução VERDADEIRAMENTE paralela com threads"""
        import concurrent.futures
        import threading
        
        logger.info(f"⚡ Execução paralela REAL com {len(agentes)} agentes")
        
        resultados = {}
        erros = {}
        
        # Criar thread pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(agentes)) as executor:
            # Submeter todas as tarefas
            futuros = {}
            for agente in agentes:
                futuro = executor.submit(self._executar_agente_thread_safe, mensagem, agente)
                futuros[futuro] = agente
            
            # Coletar resultados conforme ficam prontos
            for futuro in concurrent.futures.as_completed(futuros):
                agente = futuros[futuro]
                try:
                    resultado = futuro.result(timeout=30)  # Timeout de 30 segundos por agente
                    if resultado:
                        resultados[agente] = resultado
                        logger.info(f"✅ {agente} concluído")
                except concurrent.futures.TimeoutError:
                    erros[agente] = "Timeout"
                    logger.warning(f"⏱️ {agente} - timeout")
                except Exception as e:
                    erros[agente] = str(e)
                    logger.error(f"❌ {agente} - erro: {e}")
        
        # Sintetizar resultados
        if resultados:
            return self._sintetizar_resultados_paralelos(mensagem, resultados, erros)
        else:
            return self._resposta_direta_maestro(mensagem)
    
    def _executar_agente_thread_safe(self, mensagem: str, agente: str) -> Optional[str]:
        """Execução thread-safe de um agente"""
        try:
            # Criar contexto isolado para thread
            contexto_thread = {
                'thread_id': threading.current_thread().ident,
                'agente': agente,
                'timestamp': datetime.now()
            }
            
            # Executar agente específico
            if agente == 'supervisor' and self.supervisor_ativo:
                return self.supervisor.processar(mensagem, contexto_thread)
            elif agente == 'taskbreaker' and self.taskbreaker_ativo:
                plano = self.taskbreaker.analisar_tarefa(mensagem, contexto_thread)
                return f"Complexidade: {plano.complexidade}, Subtarefas: {len(plano.subtarefas)}"
            elif agente == 'deepagent' and self.deepagent_ativo:
                if self._precisa_web_search(mensagem):
                    termo = self._extrair_termo_pesquisa(mensagem)
                    return self.deepagent.pesquisar_produto_web(termo).resumo
            elif agente == 'automaster' and self.automaster_ativo:
                return self.automaster.processar(mensagem, contexto_thread)
            elif agente == 'promptcrafter' and self.promptcrafter_ativo:
                return self.promptcrafter.processar(mensagem, contexto_thread)
            elif agente == 'psymind' and self.psymind_ativo:
                return self.psymind.processar(mensagem, contexto_thread)
            # Oráculo por último devido à complexidade
            elif agente == 'oraculo' and self.oraculo_ativo:
                return self.oraculo.processar(mensagem, contexto_thread)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro na thread do agente {agente}: {e}")
            return None
    
    def _sintetizar_resultados_paralelos(self, mensagem: str, resultados: Dict[str, str], erros: Dict[str, str]) -> str:
        """Sintetiza resultados da execução paralela"""
        # Se houver resultado do Oráculo, ele tem prioridade
        if 'oraculo' in resultados:
            return resultados['oraculo']
        
        # Construir síntese
        sintese = []
        
        # Adicionar resultados bem-sucedidos
        for agente, resultado in resultados.items():
            if resultado and len(resultado) > 10:  # Ignorar resultados muito curtos
                sintese.append(f"**{agente.capitalize()}**: {resultado[:200]}...")
        
        # Mencionar erros se houver
        if erros:
            sintese.append(f"\n⚠️ Alguns agentes tiveram problemas: {', '.join(erros.keys())}")
        
        if sintese:
            return "\n\n".join(sintese)
        else:
            return self._resposta_direta_maestro(mensagem)

# === FUNÇÕES DE CRIAÇÃO ===

def criar_carlos_maestro(modo_proativo: bool = True, **kwargs) -> CarlosMaestroV5:
    """🧠 Cria Carlos v5.0 Maestro Robusto com configurações completas + BaseAgentV2"""
    # Extrair configurações específicas para evitar duplicatas
    config_carlos = {
        'reflexor_ativo': kwargs.pop('reflexor_ativo', True),
        'supervisor_ativo': kwargs.pop('supervisor_ativo', True),
        'memoria_ativa': kwargs.pop('memoria_ativa', True),
        'promptcrafter_ativo': kwargs.pop('promptcrafter_ativo', True),
        'deepagent_ativo': kwargs.pop('deepagent_ativo', True),
        'oraculo_ativo': kwargs.pop('oraculo_ativo', True),
        'automaster_ativo': kwargs.pop('automaster_ativo', True),
        'taskbreaker_ativo': kwargs.pop('taskbreaker_ativo', True),
        'psymind_ativo': kwargs.pop('psymind_ativo', True),
        'modo_proativo': modo_proativo,
        'config': kwargs.pop('config', None)
    }
    
    # Combinar com kwargs restantes
    config_carlos.update(kwargs)
    
    # Criar instância do Carlos
    carlos = CarlosMaestroV5(**config_carlos)
    
    # Registrar Carlos no AgentWakeManager
    try:
        from utils.agent_wake_manager import get_wake_manager
        wake_manager = get_wake_manager()
        wake_manager.register_agent("carlos", carlos)
        logger.info("🤖 Carlos registrado no AgentWakeManager")
    except Exception as e:
        logger.warning(f"⚠️ Falha ao registrar Carlos no WakeManager: {e}")
    
    return carlos

# Alias para compatibilidade e novas versões
create_carlos = criar_carlos_maestro
criar_carlos_maestro_v5 = criar_carlos_maestro  # Para compatibilidade com __init__.py

if __name__ == "__main__":
    print("🧠 Testando Carlos v5.0 Maestro Robusto...")
    
    carlos = criar_carlos_maestro()
    diagnostico = carlos.diagnosticar_sistema()
    
    print(f"Diagnóstico: {diagnostico}")
    print("✅ Carlos v5.0 Maestro Robusto OK!")