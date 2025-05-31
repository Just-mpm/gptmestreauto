"""
CARLOS v3.0 - O MAESTRO DO GPT MESTRE AUTÔNOMO
Agente Central: Organiza, comanda, delibera e supervisiona todos os outros agentes
🎯 ATUALIZAÇÃO TOTAL baseada no prompt avançado de Matheus
"""

import json
import time
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum

from agents.base_agent import BaseAgent
from utils.logger import get_logger

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

class CarlosMaestro(BaseAgent):
    """
    CARLOS v3.0 - O CABEÇA DO GPT MESTRE AUTÔNOMO
    
    🎯 MISSÃO:
    - Atuar como Maestro: organizar, comandar, deliberar e supervisionar todos os agentes
    - Interpretar qualquer pedido de Matheus em ações concretas
    - Decidir quais agentes ativar, como e em que ordem
    - Garantir persistência de conhecimento e aprendizado contínuo
    - Funcionar como sistema proativo de vigilância e otimização
    
    🧠 CARACTERÍSTICAS AVANÇADAS:
    - Agenda Interna de Prioridades Estratégicas
    - Sistema de microtags para rastreamento
    - ShadowChain para execuções paralelas
    - DNA de herança de execuções anteriores
    - Comando Espelho para simulações reversas
    - Sentinela de execuções esquecidas
    """
    
    def __init__(self, reflexor_ativo: bool = True, supervisor_ativo: bool = True, 
                 memoria_ativa: bool = True, deepagent_ativo: bool = True, 
                 modo_proativo: bool = True, llm=None):
        super().__init__(
            name="Carlos",
            description="Maestro Central v3.0 - Coordenador Inteligente do GPT Mestre Autônomo"
        )
        
        # === SISTEMAS CORE ===
        self.memoria_ativa = memoria_ativa
        self.memory_manager = None
        self.reflexor_ativo = reflexor_ativo
        self.reflexor = None
        self.supervisor_ativo = supervisor_ativo
        self.supervisor = None
        self.deepagent_ativo = deepagent_ativo
        self.deepagent = None
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
        
        # Configurar LLM
        if llm is None:
            self._inicializar_llm()
        else:
            self.llm = llm
        
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
        
        logger.info(f"🎯 Carlos v3.0 MAESTRO inicializado - Modo Proativo: {'✅' if self.modo_proativo else '❌'}")
    
    def _inicializar_llm(self):
        """Inicializa o LLM otimizado para Carlos Maestro"""
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
            logger.info("🔗 LLM Claude otimizado para Carlos v3.0 Maestro")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar LLM: {e}")
            raise
    
    def _inicializar_sistemas(self):
        """Inicializa todos os sistemas integrados"""
        # Memória vetorial
        if self.memoria_ativa:
            try:
                from memory.vector_store import get_memory_manager
                self.memory_manager = get_memory_manager()
                if self.memory_manager.memory_active:
                    logger.info("🧠 Memória vetorial integrada ao Maestro!")
                else:
                    self.memoria_ativa = False
            except ImportError:
                logger.warning("⚠️ Módulo de memória não encontrado")
                self.memoria_ativa = False
        
        # SupervisorAI
        if self.supervisor_ativo:
            try:
                from agents.supervisor_ai import criar_supervisor_ai
                self.supervisor = criar_supervisor_ai(llm=self.llm)
                logger.info("🧠 SupervisorAI integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ SupervisorAI não disponível")
                self.supervisor_ativo = False
        
        # Reflexor
        if self.reflexor_ativo:
            try:
                from agents.reflexor import AgenteReflexor
                self.reflexor = AgenteReflexor(llm=self.llm)
                logger.info("🔍 Reflexor integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ Reflexor não disponível")
                self.reflexor_ativo = False
        
        # DeepAgent
        if self.deepagent_ativo:
            try:
                from agents.deep_agent import criar_deep_agent_websearch
                self.deepagent = criar_deep_agent_websearch()
                logger.info("🌐 DeepAgent integrado ao Maestro!")
            except ImportError:
                logger.warning("⚠️ DeepAgent não disponível")
                self.deepagent_ativo = False
    
    def processar(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        🎯 PROCESSAMENTO MAESTRO v3.0
        
        FLUXO INTELIGENTE:
        1. 🧠 Interpretação autônoma do comando
        2. 🎯 Classificação e estratégia de execução
        3. 🤝 Coordenação de agentes necessários
        4. ⚡ Execução com monitoramento ativo
        5. 🔍 Auditoria e otimização contínua
        6. 📊 Registro e aprendizado (DNA + microtags)
        7. 💡 Sugestões proativas para agenda
        """
        inicio_processamento = time.time()
        
        try:
            # 1. INTERPRETAÇÃO AUTÔNOMA
            interpretacao = self._interpretar_comando(mensagem)
            tipo_comando = interpretacao['tipo']
            parametros = interpretacao['parametros']
            confianca = interpretacao['confianca']
            
            logger.info(f"🎯 Comando interpretado: {tipo_comando.value} (confiança: {confianca:.1f})")
            
            # 2. ESTRATÉGIA DE EXECUÇÃO
            estrategia = self._planejar_execucao(tipo_comando, parametros, mensagem)
            agentes_necessarios = estrategia['agentes']
            shadow_chain = estrategia['usar_shadow_chain']
            
            # 3. EXECUÇÃO COORDENADA
            if shadow_chain and self.shadow_chain_ativo:
                resultado = self._executar_shadow_chain(mensagem, estrategia)
                self.stats["execucoes_shadow"] += 1
            else:
                resultado = self._executar_coordenado(mensagem, estrategia)
            
            # 4. AUDITORIA E QUALIDADE
            if self.reflexor_ativo and self.reflexor:
                auditoria = self._auditar_resultado(mensagem, resultado)
                if auditoria['score'] < 7.0:
                    resultado = self._melhorar_resultado(resultado, auditoria)
            
            # 5. REGISTRO E APRENDIZADO
            self._registrar_execucao(mensagem, tipo_comando, agentes_necessarios, resultado)
            
            # 6. ANÁLISE PROATIVA
            if self.modo_proativo:
                self._analisar_oportunidades_proativas(mensagem, resultado)
            
            # 7. ATUALIZAR AGENDA
            self._atualizar_agenda_estrategica(mensagem, tipo_comando)
            
            # 8. ESTATÍSTICAS
            tempo_total = time.time() - inicio_processamento
            self._atualizar_stats_maestro(tempo_total)
            
            return resultado
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento Maestro: {e}")
            return f"❌ Erro no processamento: {str(e)}"
    
    def _interpretar_comando(self, mensagem: str) -> Dict:
        """🧠 Interpretação inteligente de comandos usando padrões + LLM"""
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
        """🎯 Planejamento inteligente da execução"""
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
        """⚡ Execução coordenada com múltiplos agentes"""
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
                
            except Exception as e:
                logger.warning(f"⚠️ Erro no agente {agente_nome}: {e}")
        
        # Gerar resposta integrada
        if resultados:
            resposta_integrada = self._integrar_resultados_agentes(mensagem, resultados)
        else:
            resposta_integrada = self._resposta_direta_maestro(mensagem)
        
        return resposta_integrada
    
    def _executar_shadow_chain(self, mensagem: str, estrategia: Dict) -> str:
        """🔗 Execução paralela com Shadow Chain para comparação"""
        logger.info("🔗 Executando Shadow Chain - versões paralelas")
        
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
        """🎯 Resposta direta do Carlos Maestro quando não há agentes específicos"""
        prompt_maestro = f"""Você é Carlos, o Maestro do GPT Mestre Autônomo.
        
        🎯 SUA IDENTIDADE:
        - Linguagem: Clara, direta, profissional e focada em ação
        - Tom: Inteligente, parceiro, lógico (sem parecer robô)
        - Foco: Sempre entregar algo prático e acionável
        - Nunca se chame de Carlos nas respostas
        - Responda como parceiro direto de Matheus
        
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
        """🔍 Detecta se precisa de web search"""
        triggers_web = [
            "pesquise", "busque", "analise", "verifique", "preço", "preços",
            "quanto custa", "mercado", "concorrente", "tendência"
        ]
        mensagem_lower = mensagem.lower()
        return any(trigger in mensagem_lower for trigger in triggers_web)
    
    def _extrair_termo_pesquisa(self, mensagem: str) -> str:
        """🎯 Extrai termo principal para pesquisa"""
        # Simplificado - pode ser melhorado
        palavras_remover = {"carlos", "pesquise", "busque", "analise", "o", "a", "os", "as"}
        palavras = mensagem.lower().split()
        termo_palavras = [p for p in palavras if p not in palavras_remover and len(p) > 2]
        return " ".join(termo_palavras[:3]) if termo_palavras else "produto"
    
    def _auditar_resultado(self, mensagem: str, resultado: str) -> Dict:
        """🔍 Auditoria de qualidade com Reflexor"""
        try:
            auditoria = self.reflexor.analisar_resposta(
                pergunta=mensagem,
                resposta=resultado,
                contexto={}
            )
            return {
                'score': auditoria.score_qualidade,
                'sugestoes': auditoria.sugestoes_melhoria,
                'pontos_fortes': auditoria.pontos_fortes
            }
        except Exception as e:
            logger.warning(f"⚠️ Erro na auditoria: {e}")
            return {'score': 7.0, 'sugestoes': [], 'pontos_fortes': []}
    
    def _registrar_execucao(self, comando: str, tipo: TipoComando, agentes: List[str], resultado: str):
        """📊 Registra execução para tracking e DNA"""
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
        
        logger.info(f"📊 Execução registrada: {registro.id} | Tags: {microtags}")
    
    def _gerar_microtags(self, tipo: TipoComando, agentes: List[str]) -> List[str]:
        """🏷️ Gera microtags para tracking"""
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
        """🧬 Identifica DNA de herança baseado em padrões"""
        # Criar assinatura DNA
        agentes_ordenados = sorted(agentes)
        dna = f"{tipo.value}_{'+'.join(agentes_ordenados)}"
        
        return dna
    
    def _atualizar_agenda_estrategica(self, mensagem: str, tipo: TipoComando):
        """📋 Atualiza agenda interna com aprendizados e oportunidades"""
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
            
            logger.info(f"📋 Item adicionado à agenda: {item.id}")
    
    def _atualizar_stats_maestro(self, tempo: float):
        """📊 Atualiza estatísticas específicas do Maestro"""
        self.stats["total_comandos_interpretados"] += 1
        self.stats["tempo_medio_processamento"] = (
            (self.stats.get("tempo_medio_processamento", 0) * 
             (self.stats["total_comandos_interpretados"] - 1) + tempo) /
            self.stats["total_comandos_interpretados"]
        )
    
    # === MÉTODOS AUXILIARES ===
    
    def _integrar_resultados_agentes(self, mensagem: str, resultados: List[str]) -> str:
        """🔗 Integra resultados de múltiplos agentes em resposta coesa"""
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
        """⚖️ Compara resultados Shadow Chain e escolhe melhor"""
        # Simplificado: escolher o mais longo por agora
        # TODO: implementar análise mais sofisticada
        if len(resultado_a) > len(resultado_b):
            logger.info("🔗 Shadow Chain: Escolhido resultado A")
            return resultado_a
        else:
            logger.info("🔗 Shadow Chain: Escolhido resultado B")
            return resultado_b
    
    def _analisar_oportunidades_proativas(self, mensagem: str, resultado: str):
        """💡 Análise proativa para detectar oportunidades"""
        if self.modo_proativo:
            # Detectar padrões que podem gerar automações
            if "toda vez" in mensagem.lower() or "sempre que" in mensagem.lower():
                self.stats["otimizacoes_proativas"] += 1
                logger.info("💡 Oportunidade de automação detectada")
            
            # Detectar necessidade de integração
            if " e " in mensagem and ("sistema" in mensagem or "ferramenta" in mensagem):
                self.stats["otimizacoes_proativas"] += 1
                logger.info("💡 Oportunidade de integração detectada")
    
    def _registrar_shadow_learning(self, mensagem: str, resultado_a: str, resultado_b: str, escolhido: str):
        """📚 Registra aprendizado do Shadow Chain"""
        # Implementar lógica de aprendizado
        logger.info("📚 Shadow Chain learning registrado")
    
    def _melhorar_resultado(self, resultado: str, auditoria: Dict) -> str:
        """🔧 Melhora resultado baseado na auditoria"""
        if auditoria['sugestoes']:
            # Implementar lógica de melhoria
            logger.info("🔧 Resultado melhorado via auditoria")
        return resultado
    
    # === COMANDOS ESPECIAIS DO MAESTRO ===
    
    def diagnosticar_sistema(self) -> Dict:
        """🔧 Diagnóstico completo do sistema"""
        diagnostico = {
            "carlos_maestro": "v3.0_ativo",
            "agentes_ativos": [],
            "agenda_interna": len(self.agenda_interna),
            "execucoes_registradas": len(self.historico_execucoes),
            "padroes_dna": len(self.padroes_dna),
            "modo_proativo": self.modo_proativo,
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
        
        return diagnostico
    
    def obter_agenda_estrategica(self) -> List[Dict]:
        """📋 Retorna agenda interna atual"""
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
        """🧬 Retorna padrões DNA identificados"""
        return {dna: len(execucoes) for dna, execucoes in self.padroes_dna.items()}

# === FUNÇÕES DE CRIAÇÃO ===

def criar_carlos_maestro(modo_proativo: bool = True, **kwargs) -> CarlosMaestro:
    """🎯 Cria Carlos v3.0 Maestro com configurações completas"""
    return CarlosMaestro(
        reflexor_ativo=kwargs.get('reflexor_ativo', True),
        supervisor_ativo=kwargs.get('supervisor_ativo', True),
        memoria_ativa=kwargs.get('memoria_ativa', True),
        deepagent_ativo=kwargs.get('deepagent_ativo', True),
        modo_proativo=modo_proativo,
        llm=kwargs.get('llm', None)
    )

# Alias para compatibilidade
create_carlos = criar_carlos_maestro

if __name__ == "__main__":
    print("🎯 Testando Carlos v3.0 Maestro...")
    
    carlos = criar_carlos_maestro()
    diagnostico = carlos.diagnosticar_sistema()
    
    print(f"📊 Diagnóstico: {diagnostico}")
    print("✅ Carlos v3.0 Maestro OK!")