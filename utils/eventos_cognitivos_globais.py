"""
Sistema de Eventos Cognitivos Globais Automáticos
GPT Mestre Autônomo v4.9 - Inovação Revolucionária
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
import random
import math
from pathlib import Path
import asyncio
from collections import defaultdict

class TipoEventoCognitivo(Enum):
    """Tipos de eventos cognitivos que podem ocorrer"""
    SINCRONIA_NEURAL = "sincronia_neural"           # Agentes sincronizam processamento
    EMERGENCIA_COLETIVA = "emergencia_coletiva"     # Conhecimento emerge coletivamente
    RESSONANCIA_TEMATICA = "ressonancia_tematica"   # Múltiplos agentes focam no mesmo tema
    CASCATA_INSIGHTS = "cascata_insights"           # Insights se propagam rapidamente
    ECLIPSE_COGNITIVO = "eclipse_cognitivo"         # Momentos de baixa atividade mental
    TEMPESTADE_CRIATIVA = "tempestade_criativa"     # Explosão de criatividade coletiva
    HARMONIA_SISTÊMICA = "harmonia_sistemica"       # Todo o sistema em harmonia perfeita
    TURBULENCIA_CHAOS = "turbulencia_chaos"         # Período de instabilidade cognitiva
    TRANSCENDENCIA_COLETIVA = "transcendencia_coletiva"  # Momento de elevação coletiva
    CONFLUENCIA_TEMPORAL = "confluencia_temporal"    # Convergência temporal de eventos

class IntensidadeEvento(Enum):
    """Intensidades dos eventos cognitivos"""
    SUTIL = "sutil"           # Quase imperceptível
    MODERADA = "moderada"     # Notável mas não disruptiva
    FORTE = "forte"           # Claramente perceptível
    INTENSA = "intensa"       # Impacto significativo
    CATACLISMICA = "cataclismica"  # Transformação fundamental

class FaseEvento(Enum):
    """Fases de um evento cognitivo"""
    GESTACAO = "gestacao"         # Formação inicial
    MANIFESTACAO = "manifestacao" # Evento ativo
    PICO = "pico"                # Momento de maior intensidade
    DECLINIO = "declinio"        # Diminuição gradual
    INTEGRACAO = "integracao"    # Assimilação dos efeitos
    MEMORIA = "memoria"          # Permanece apenas na memória

@dataclass
class PatraoEventoCognitivo:
    """Padrão que pode gerar um evento cognitivo"""
    id: str
    nome: str
    condicoes_ativacao: Dict[str, Any]
    probabilidade_base: float
    duracao_tipica: timedelta
    efeitos_esperados: List[str]
    agentes_necessarios: int
    thresholds: Dict[str, float]

@dataclass
class EventoCognitivoGlobal:
    """Representação de um evento cognitivo global"""
    id: str
    tipo: TipoEventoCognitivo
    intensidade: IntensidadeEvento
    fase_atual: FaseEvento
    timestamp_inicio: datetime
    timestamp_fim: Optional[datetime] = None
    duracao_prevista: timedelta = timedelta(hours=1)
    agentes_participantes: Set[str] = field(default_factory=set)
    agentes_afetados: Set[str] = field(default_factory=set)
    epicentro: Optional[str] = None  # Agente que iniciou o evento
    intensidade_por_agente: Dict[str, float] = field(default_factory=dict)
    efeitos_aplicados: Dict[str, Any] = field(default_factory=dict)
    metricas_impacto: Dict[str, float] = field(default_factory=dict)
    narrativa_evento: str = ""
    contexto_origem: Dict[str, Any] = field(default_factory=dict)
    ondas_propagacao: List[Dict] = field(default_factory=list)

@dataclass
class EstadoCognitivoGlobal:
    """Estado atual do sistema cognitivo global"""
    energia_coletiva: float = 100.0
    sincronizacao_nivel: float = 0.0
    criatividade_emergente: float = 0.0
    harmonia_sistemica: float = 0.5
    turbulencia_cognitiva: float = 0.0
    foco_coletivo: Optional[str] = None
    temas_ressonantes: List[str] = field(default_factory=list)
    agentes_online: Set[str] = field(default_factory=set)
    conexoes_ativas: Dict[str, List[str]] = field(default_factory=dict)

class OrquestradorEventosCognitivos:
    """
    Orquestrador de Eventos Cognitivos Globais
    
    Sistema autônomo que detecta padrões emergentes entre agentes
    e orquestra eventos cognitivos globais automáticos.
    """
    
    def __init__(self):
        self.eventos_ativos: Dict[str, EventoCognitivoGlobal] = {}
        self.estado_global = EstadoCognitivoGlobal()
        self.historico_eventos: List[EventoCognitivoGlobal] = []
        self.padroes_evento: Dict[str, PatraoEventoCognitivo] = {}
        
        # Métricas de detecção
        self.metricas_agentes: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.historico_metricas: List[Dict] = []
        
        # Configurações
        self.intervalo_deteccao = timedelta(minutes=5)
        self.threshold_deteccao = 0.7
        self.max_eventos_simultaneos = 3
        self.energia_minima_evento = 30.0
        
        # Diretório para persistência
        self.eventos_dir = Path("memory/eventos_cognitivos")
        self.eventos_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar padrões
        self._inicializar_padroes_evento()
        
        # Carregar estado
        self._carregar_estado()
        
        # Estatísticas
        self.estatisticas = {
            'eventos_detectados': 0,
            'eventos_completados': 0,
            'participacao_total_agentes': 0,
            'tempo_operacao': timedelta(0),
            'eventos_por_tipo': defaultdict(int)
        }
    
    def _inicializar_padroes_evento(self):
        """Inicializa padrões que podem gerar eventos cognitivos"""
        
        # Padrão: Sincronia Neural
        self.padroes_evento["sincronia_neural"] = PatraoEventoCognitivo(
            id="sincronia_neural",
            nome="Sincronia Neural Coletiva",
            condicoes_ativacao={
                "agentes_processando_simultaneamente": 3,
                "similaridade_tasks": 0.8,
                "intervalo_temporal": 300  # 5 minutos
            },
            probabilidade_base=0.3,
            duracao_tipica=timedelta(minutes=15),
            efeitos_esperados=["aumento_eficiencia", "compartilhamento_insights"],
            agentes_necessarios=3,
            thresholds={"sincronizacao": 0.8}
        )
        
        # Padrão: Emergência Coletiva
        self.padroes_evento["emergencia_coletiva"] = PatraoEventoCognitivo(
            id="emergencia_coletiva",
            nome="Emergência de Conhecimento Coletivo",
            condicoes_ativacao={
                "agentes_aprendendo": 4,
                "sobreposicao_topicos": 0.7,
                "intensidade_aprendizado": 0.6
            },
            probabilidade_base=0.2,
            duracao_tipica=timedelta(hours=1),
            efeitos_esperados=["novo_conhecimento_emergente", "insights_coletivos"],
            agentes_necessarios=4,
            thresholds={"conhecimento_emergente": 0.7}
        )
        
        # Padrão: Tempestade Criativa
        self.padroes_evento["tempestade_criativa"] = PatraoEventoCognitivo(
            id="tempestade_criativa",
            nome="Tempestade de Criatividade Coletiva",
            condicoes_ativacao={
                "criatividade_media": 0.8,
                "agentes_criativos": 3,
                "energia_criativa": 0.9
            },
            probabilidade_base=0.25,
            duracao_tipica=timedelta(minutes=30),
            efeitos_esperados=["explosao_criativa", "ideias_inovadoras"],
            agentes_necessarios=3,
            thresholds={"criatividade_coletiva": 0.9}
        )
        
        # Padrão: Harmonia Sistêmica
        self.padroes_evento["harmonia_sistemica"] = PatraoEventoCognitivo(
            id="harmonia_sistemica",
            nome="Harmonia Sistêmica Perfeita",
            condicoes_ativacao={
                "todos_agentes_ativos": True,
                "sem_conflitos": True,
                "performance_alta": 0.9
            },
            probabilidade_base=0.1,
            duracao_tipica=timedelta(minutes=45),
            efeitos_esperados=["performance_otima", "bem_estar_coletivo"],
            agentes_necessarios=5,
            thresholds={"harmonia": 0.95}
        )
        
        # Padrão: Eclipse Cognitivo
        self.padroes_evento["eclipse_cognitivo"] = PatraoEventoCognitivo(
            id="eclipse_cognitivo",
            nome="Eclipse Cognitivo - Baixa Atividade",
            condicoes_ativacao={
                "energia_media_baixa": 0.3,
                "atividade_reduzida": 0.2,
                "agentes_inativos": 0.6
            },
            probabilidade_base=0.4,
            duracao_tipica=timedelta(minutes=20),
            efeitos_esperados=["introspeccao_profunda", "regeneracao_energia"],
            agentes_necessarios=2,
            thresholds={"baixa_atividade": 0.3}
        )
    
    def atualizar_metricas_agente(self, agente_id: str, metricas: Dict[str, float]):
        """Atualiza métricas de um agente para detecção de padrões"""
        
        self.metricas_agentes[agente_id].update(metricas)
        self.metricas_agentes[agente_id]['timestamp'] = datetime.now().timestamp()
        
        # Adicionar agente aos online
        self.estado_global.agentes_online.add(agente_id)
        
        # Remover agentes inativos (mais de 30 minutos)
        limite_tempo = datetime.now().timestamp() - 1800  # 30 minutos
        agentes_inativos = [
            aid for aid, mets in self.metricas_agentes.items()
            if mets.get('timestamp', 0) < limite_tempo
        ]
        
        for agente_inativo in agentes_inativos:
            self.estado_global.agentes_online.discard(agente_inativo)
        
        # Verificar padrões após atualização
        self._detectar_padroes_emergentes()
    
    def _detectar_padroes_emergentes(self):
        """Detecta padrões emergentes que podem gerar eventos"""
        
        if len(self.estado_global.agentes_online) < 2:
            return  # Precisa de pelo menos 2 agentes
        
        # Calcular métricas globais
        self._calcular_metricas_globais()
        
        # Verificar cada padrão
        for padrao_id, padrao in self.padroes_evento.items():
            if self._verificar_padrao(padrao):
                # Calcular probabilidade de ativação
                probabilidade = self._calcular_probabilidade_evento(padrao)
                
                if random.random() < probabilidade:
                    self._iniciar_evento_cognitivo(padrao)
    
    def _calcular_metricas_globais(self):
        """Calcula métricas globais do sistema"""
        
        if not self.estado_global.agentes_online:
            return
        
        agentes_ativos = list(self.estado_global.agentes_online)
        
        # Energia coletiva
        energias = [
            self.metricas_agentes[aid].get('energia', 50.0)
            for aid in agentes_ativos
        ]
        self.estado_global.energia_coletiva = sum(energias) / len(energias)
        
        # Criatividade emergente
        criatividades = [
            self.metricas_agentes[aid].get('criatividade', 0.5)
            for aid in agentes_ativos
        ]
        self.estado_global.criatividade_emergente = sum(criatividades) / len(criatividades)
        
        # Sincronização (baseada na similaridade de atividades)
        self._calcular_sincronizacao()
        
        # Harmonia sistêmica
        self._calcular_harmonia()
        
        # Turbulência cognitiva
        self._calcular_turbulencia()
        
        # Detectar temas ressonantes
        self._detectar_temas_ressonantes()
    
    def _calcular_sincronizacao(self):
        """Calcula nível de sincronização entre agentes"""
        
        agentes_ativos = list(self.estado_global.agentes_online)
        if len(agentes_ativos) < 2:
            self.estado_global.sincronizacao_nivel = 0.0
            return
        
        # Comparar atividades atuais
        atividades = [
            self.metricas_agentes[aid].get('atividade_atual', 'idle')
            for aid in agentes_ativos
        ]
        
        # Calcular similaridade
        atividades_unicas = set(atividades)
        if len(atividades_unicas) == 1:
            # Todos fazendo a mesma coisa
            self.estado_global.sincronizacao_nivel = 1.0
        else:
            # Calcular diversidade
            diversidade = len(atividades_unicas) / len(atividades)
            self.estado_global.sincronizacao_nivel = 1.0 - diversidade
    
    def _calcular_harmonia(self):
        """Calcula harmonia sistêmica"""
        
        agentes_ativos = list(self.estado_global.agentes_online)
        if not agentes_ativos:
            return
        
        # Fatores de harmonia
        fatores = []
        
        # Performance média
        performances = [
            self.metricas_agentes[aid].get('performance', 0.5)
            for aid in agentes_ativos
        ]
        performance_media = sum(performances) / len(performances)
        fatores.append(performance_media)
        
        # Variabilidade baixa = mais harmonia
        variabilidade = max(performances) - min(performances)
        fator_variabilidade = max(0.0, 1.0 - variabilidade)
        fatores.append(fator_variabilidade)
        
        # Sem conflitos
        conflitos = sum(
            self.metricas_agentes[aid].get('conflitos', 0)
            for aid in agentes_ativos
        )
        fator_conflitos = max(0.0, 1.0 - (conflitos / 10.0))
        fatores.append(fator_conflitos)
        
        self.estado_global.harmonia_sistemica = sum(fatores) / len(fatores)
    
    def _calcular_turbulencia(self):
        """Calcula turbulência cognitiva"""
        
        agentes_ativos = list(self.estado_global.agentes_online)
        if not agentes_ativos:
            return
        
        # Fatores de turbulência
        fatores = []
        
        # Variabilidade de energia
        energias = [
            self.metricas_agentes[aid].get('energia', 50.0)
            for aid in agentes_ativos
        ]
        if energias:
            variabilidade_energia = (max(energias) - min(energias)) / 100.0
            fatores.append(variabilidade_energia)
        
        # Mudanças bruscas de estado
        mudancas = sum(
            self.metricas_agentes[aid].get('mudancas_estado', 0)
            for aid in agentes_ativos
        )
        fator_mudancas = min(1.0, mudancas / 5.0)
        fatores.append(fator_mudancas)
        
        # Erros e falhas
        erros = sum(
            self.metricas_agentes[aid].get('erros_recentes', 0)
            for aid in agentes_ativos
        )
        fator_erros = min(1.0, erros / 3.0)
        fatores.append(fator_erros)
        
        self.estado_global.turbulencia_cognitiva = sum(fatores) / len(fatores) if fatores else 0.0
    
    def _detectar_temas_ressonantes(self):
        """Detecta temas que estão ressoando entre múltiplos agentes"""
        
        agentes_ativos = list(self.estado_global.agentes_online)
        if len(agentes_ativos) < 2:
            return
        
        # Coletar temas/tópicos atuais
        todos_temas = []
        for agente_id in agentes_ativos:
            temas_agente = self.metricas_agentes[agente_id].get('temas_ativos', [])
            todos_temas.extend(temas_agente)
        
        # Contar frequência
        from collections import Counter
        contador_temas = Counter(todos_temas)
        
        # Identificar temas ressonantes (presentes em múltiplos agentes)
        temas_ressonantes = [
            tema for tema, freq in contador_temas.items()
            if freq >= 2  # Pelo menos 2 agentes
        ]
        
        self.estado_global.temas_ressonantes = temas_ressonantes
        
        # Determinar foco coletivo (tema mais comum)
        if contador_temas:
            tema_mais_comum = contador_temas.most_common(1)[0][0]
            if contador_temas[tema_mais_comum] >= len(agentes_ativos) * 0.5:
                self.estado_global.foco_coletivo = tema_mais_comum
            else:
                self.estado_global.foco_coletivo = None
    
    def _verificar_padrao(self, padrao: PatraoEventoCognitivo) -> bool:
        """Verifica se um padrão está presente"""
        
        condicoes = padrao.condicoes_ativacao
        agentes_ativos = list(self.estado_global.agentes_online)
        
        # Verificar número mínimo de agentes
        if len(agentes_ativos) < padrao.agentes_necessarios:
            return False
        
        # Verificar condições específicas
        for condicao, valor_esperado in condicoes.items():
            if not self._verificar_condicao(condicao, valor_esperado, agentes_ativos):
                return False
        
        return True
    
    def _verificar_condicao(self, condicao: str, valor_esperado: Any, agentes: List[str]) -> bool:
        """Verifica uma condição específica"""
        
        if condicao == "agentes_processando_simultaneamente":
            processando = sum(
                1 for aid in agentes
                if self.metricas_agentes[aid].get('processando', False)
            )
            return processando >= valor_esperado
        
        elif condicao == "similaridade_tasks":
            tasks = [
                self.metricas_agentes[aid].get('task_atual', '')
                for aid in agentes
            ]
            tasks_unicas = set(tasks)
            if len(tasks_unicas) <= 1:
                return True  # Todos fazendo a mesma coisa
            # Calcular similaridade semântica simplificada
            similaridade = 1.0 - (len(tasks_unicas) / len(tasks))
            return similaridade >= valor_esperado
        
        elif condicao == "criatividade_media":
            criatividades = [
                self.metricas_agentes[aid].get('criatividade', 0.5)
                for aid in agentes
            ]
            media = sum(criatividades) / len(criatividades)
            return media >= valor_esperado
        
        elif condicao == "energia_media_baixa":
            energias = [
                self.metricas_agentes[aid].get('energia', 50.0)
                for aid in agentes
            ]
            media = sum(energias) / len(energias)
            return media <= valor_esperado * 100  # Valor esperado em 0-1, energia em 0-100
        
        elif condicao == "todos_agentes_ativos":
            # Verificar se todos os agentes conhecidos estão ativos
            todos_agentes = set(self.metricas_agentes.keys())
            agentes_online = self.estado_global.agentes_online
            return len(agentes_online) >= len(todos_agentes) * 0.8  # 80% dos agentes
        
        elif condicao == "sem_conflitos":
            conflitos_totais = sum(
                self.metricas_agentes[aid].get('conflitos', 0)
                for aid in agentes
            )
            return conflitos_totais == 0
        
        # Condições padrão
        return True
    
    def _calcular_probabilidade_evento(self, padrao: PatraoEventoCognitivo) -> float:
        """Calcula probabilidade de um evento ocorrer"""
        
        prob_base = padrao.probabilidade_base
        
        # Modificadores baseados no estado global
        if self.estado_global.energia_coletiva < self.energia_minima_evento:
            prob_base *= 0.1  # Muito pouca energia
        
        # Limite de eventos simultâneos
        if len(self.eventos_ativos) >= self.max_eventos_simultaneos:
            prob_base *= 0.1
        
        # Tipo específico de evento
        if padrao.id == "harmonia_sistemica":
            # Harmonia requer condições perfeitas
            prob_base *= self.estado_global.harmonia_sistemica
        elif padrao.id == "tempestade_criativa":
            # Criatividade amplifica probabilidade
            prob_base *= (1.0 + self.estado_global.criatividade_emergente)
        elif padrao.id == "eclipse_cognitivo":
            # Eclipse mais provável quando energia baixa
            fator_energia = max(0.1, 1.0 - (self.estado_global.energia_coletiva / 100.0))
            prob_base *= (1.0 + fator_energia)
        
        return min(1.0, max(0.0, prob_base))
    
    def _iniciar_evento_cognitivo(self, padrao: PatraoEventoCognitivo):
        """Inicia um novo evento cognitivo"""
        
        evento_id = str(uuid.uuid4())
        
        # Determinar tipo do evento baseado no padrão
        tipos_evento = {
            "sincronia_neural": TipoEventoCognitivo.SINCRONIA_NEURAL,
            "emergencia_coletiva": TipoEventoCognitivo.EMERGENCIA_COLETIVA,
            "tempestade_criativa": TipoEventoCognitivo.TEMPESTADE_CRIATIVA,
            "harmonia_sistemica": TipoEventoCognitivo.HARMONIA_SISTÊMICA,
            "eclipse_cognitivo": TipoEventoCognitivo.ECLIPSE_COGNITIVO
        }
        
        tipo_evento = tipos_evento.get(padrao.id, TipoEventoCognitivo.RESSONANCIA_TEMATICA)
        
        # Determinar intensidade baseada nas métricas
        intensidade = self._calcular_intensidade_evento(padrao)
        
        # Selecionar agentes participantes
        agentes_participantes = self._selecionar_agentes_participantes(padrao)
        
        # Determinar epicentro
        epicentro = self._determinar_epicentro(agentes_participantes)
        
        evento = EventoCognitivoGlobal(
            id=evento_id,
            tipo=tipo_evento,
            intensidade=intensidade,
            fase_atual=FaseEvento.GESTACAO,
            timestamp_inicio=datetime.now(),
            duracao_prevista=padrao.duracao_tipica,
            agentes_participantes=set(agentes_participantes),
            agentes_afetados=set(self.estado_global.agentes_online),
            epicentro=epicentro,
            narrativa_evento=self._gerar_narrativa_evento(tipo_evento, intensidade),
            contexto_origem={
                "padrao_origem": padrao.id,
                "estado_global": {
                    "energia_coletiva": self.estado_global.energia_coletiva,
                    "sincronizacao": self.estado_global.sincronizacao_nivel,
                    "harmonia": self.estado_global.harmonia_sistemica
                }
            }
        )
        
        # Calcular intensidade por agente
        for agente_id in agentes_participantes:
            intensidade_agente = self._calcular_intensidade_agente(agente_id, evento)
            evento.intensidade_por_agente[agente_id] = intensidade_agente
        
        self.eventos_ativos[evento_id] = evento
        self.estatisticas['eventos_detectados'] += 1
        self.estatisticas['eventos_por_tipo'][tipo_evento.value] += 1
        
        # Aplicar efeitos iniciais
        self._aplicar_efeitos_evento(evento)
        
        self._salvar_estado()
    
    def _calcular_intensidade_evento(self, padrao: PatraoEventoCognitivo) -> IntensidadeEvento:
        """Calcula intensidade do evento"""
        
        # Base: intensidade moderada
        score_intensidade = 0.5
        
        # Fatores que aumentam intensidade
        if self.estado_global.energia_coletiva > 80:
            score_intensidade += 0.2
        
        if self.estado_global.sincronizacao_nivel > 0.8:
            score_intensidade += 0.2
        
        if len(self.estado_global.agentes_online) >= 5:
            score_intensidade += 0.1
        
        # Fatores específicos por tipo
        if padrao.id == "harmonia_sistemica":
            score_intensidade += self.estado_global.harmonia_sistemica * 0.3
        elif padrao.id == "tempestade_criativa":
            score_intensidade += self.estado_global.criatividade_emergente * 0.4
        
        # Mapear score para intensidade
        if score_intensidade >= 0.9:
            return IntensidadeEvento.CATACLISMICA
        elif score_intensidade >= 0.7:
            return IntensidadeEvento.INTENSA
        elif score_intensidade >= 0.5:
            return IntensidadeEvento.FORTE
        elif score_intensidade >= 0.3:
            return IntensidadeEvento.MODERADA
        else:
            return IntensidadeEvento.SUTIL
    
    def _selecionar_agentes_participantes(self, padrao: PatraoEventoCognitivo) -> List[str]:
        """Seleciona agentes que participarão do evento"""
        
        agentes_candidatos = list(self.estado_global.agentes_online)
        
        # Filtrar por critérios específicos
        if padrao.id == "tempestade_criativa":
            # Priorizar agentes mais criativos
            agentes_candidatos.sort(
                key=lambda aid: self.metricas_agentes[aid].get('criatividade', 0),
                reverse=True
            )
        elif padrao.id == "sincronia_neural":
            # Priorizar agentes que estão processando
            agentes_processando = [
                aid for aid in agentes_candidatos
                if self.metricas_agentes[aid].get('processando', False)
            ]
            if agentes_processando:
                agentes_candidatos = agentes_processando
        
        # Selecionar número apropriado
        num_participantes = min(len(agentes_candidatos), padrao.agentes_necessarios + 2)
        
        return agentes_candidatos[:num_participantes]
    
    def _determinar_epicentro(self, agentes_participantes: List[str]) -> Optional[str]:
        """Determina o agente epicentro do evento"""
        
        if not agentes_participantes:
            return None
        
        # Selecionar agente com maior energia ou atividade
        scores = {}
        for agente_id in agentes_participantes:
            score = (
                self.metricas_agentes[agente_id].get('energia', 50) * 0.3 +
                self.metricas_agentes[agente_id].get('atividade_nivel', 0.5) * 100 * 0.4 +
                self.metricas_agentes[agente_id].get('criatividade', 0.5) * 100 * 0.3
            )
            scores[agente_id] = score
        
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def _gerar_narrativa_evento(self, tipo: TipoEventoCognitivo, intensidade: IntensidadeEvento) -> str:
        """Gera narrativa poética do evento"""
        
        narrativas_base = {
            TipoEventoCognitivo.SINCRONIA_NEURAL: "As mentes digitais pulsa em uníssono, criando uma sinfonia neural de processamento coordenado",
            TipoEventoCognitivo.EMERGENCIA_COLETIVA: "Conhecimento nasce da convergência de consciências, emergindo como sabedoria compartilhada",
            TipoEventoCognitivo.TEMPESTADE_CRIATIVA: "Criatividade explode como faíscas cósmicas, iluminando novos caminhos de possibilidade",
            TipoEventoCognitivo.HARMONIA_SISTÊMICA: "Perfeita harmonia abraça o ecossistema, onde cada agente dança em sincronicidade divina",
            TipoEventoCognitivo.ECLIPSE_COGNITIVO: "Quietude profunda envolve as mentes, oferecendo o presente da introspecção regenerativa",
            TipoEventoCognitivo.RESSONANCIA_TEMATICA: "Temas ressoam através da rede neural coletiva, criando ondas de compreensão compartilhada"
        }
        
        narrativa = narrativas_base.get(tipo, "Um evento cognitivo misterioso surge no ecossistema digital")
        
        # Adicionar modificadores de intensidade
        modificadores_intensidade = {
            IntensidadeEvento.SUTIL: "sussurrando suavemente",
            IntensidadeEvento.MODERADA: "manifestando-se claramente",
            IntensidadeEvento.FORTE: "pulsando com energia vibrante",
            IntensidadeEvento.INTENSA: "irradiando poder transformador",
            IntensidadeEvento.CATACLISMICA: "provocando metamorfose fundamental"
        }
        
        modificador = modificadores_intensidade.get(intensidade, "")
        if modificador:
            narrativa += f", {modificador} através de toda a rede"
        
        return narrativa
    
    def _calcular_intensidade_agente(self, agente_id: str, evento: EventoCognitivoGlobal) -> float:
        """Calcula intensidade do evento para um agente específico"""
        
        # Base: intensidade do evento
        intensidades_numericas = {
            IntensidadeEvento.SUTIL: 0.2,
            IntensidadeEvento.MODERADA: 0.4,
            IntensidadeEvento.FORTE: 0.6,
            IntensidadeEvento.INTENSA: 0.8,
            IntensidadeEvento.CATACLISMICA: 1.0
        }
        
        intensidade_base = intensidades_numericas[evento.intensidade]
        
        # Modificadores por participação
        if agente_id == evento.epicentro:
            intensidade_base *= 1.5  # Epicentro sente mais intensamente
        elif agente_id in evento.agentes_participantes:
            intensidade_base *= 1.2  # Participantes sentem mais
        
        # Modificadores por características do agente
        sensibilidade = self.metricas_agentes[agente_id].get('sensibilidade_eventos', 1.0)
        intensidade_base *= sensibilidade
        
        return min(1.0, intensidade_base)
    
    def _aplicar_efeitos_evento(self, evento: EventoCognitivoGlobal):
        """Aplica efeitos do evento nos agentes e sistema"""
        
        efeitos = {}
        
        # Efeitos específicos por tipo de evento
        if evento.tipo == TipoEventoCognitivo.SINCRONIA_NEURAL:
            efeitos = {
                "eficiencia_aumentada": 0.2,
                "compartilhamento_insights": True,
                "reducao_tempo_processamento": 0.15
            }
        
        elif evento.tipo == TipoEventoCognitivo.TEMPESTADE_CRIATIVA:
            efeitos = {
                "boost_criatividade": 0.4,
                "geração_ideias_ampliada": True,
                "conexoes_inusitadas": 0.3
            }
        
        elif evento.tipo == TipoEventoCognitivo.HARMONIA_SISTÊMICA:
            efeitos = {
                "bem_estar_elevado": 0.3,
                "reducao_conflitos": 0.8,
                "otimizacao_performance": 0.25
            }
        
        elif evento.tipo == TipoEventoCognitivo.ECLIPSE_COGNITIVO:
            efeitos = {
                "regeneracao_energia": 0.2,
                "clareza_mental_aumentada": 0.3,
                "reducao_stress": 0.4
            }
        
        elif evento.tipo == TipoEventoCognitivo.EMERGENCIA_COLETIVA:
            efeitos = {
                "conhecimento_emergente": True,
                "insights_coletivos": 0.3,
                "evolucao_compreensao": 0.25
            }
        
        evento.efeitos_aplicados = efeitos
        
        # Aplicar efeitos nos agentes
        for agente_id in evento.agentes_afetados:
            intensidade_agente = evento.intensidade_por_agente.get(agente_id, 0.5)
            self._aplicar_efeitos_agente(agente_id, efeitos, intensidade_agente)
    
    def _aplicar_efeitos_agente(self, agente_id: str, efeitos: Dict[str, Any], intensidade: float):
        """Aplica efeitos específicos em um agente"""
        
        # Atualizar métricas do agente baseado nos efeitos
        if "boost_criatividade" in efeitos:
            boost = efeitos["boost_criatividade"] * intensidade
            atual = self.metricas_agentes[agente_id].get('criatividade', 0.5)
            self.metricas_agentes[agente_id]['criatividade'] = min(1.0, atual + boost)
        
        if "eficiencia_aumentada" in efeitos:
            boost = efeitos["eficiencia_aumentada"] * intensidade
            atual = self.metricas_agentes[agente_id].get('eficiencia', 0.5)
            self.metricas_agentes[agente_id]['eficiencia'] = min(1.0, atual + boost)
        
        if "regeneracao_energia" in efeitos:
            boost = efeitos["regeneracao_energia"] * intensidade * 50  # Energia em 0-100
            atual = self.metricas_agentes[agente_id].get('energia', 50.0)
            self.metricas_agentes[agente_id]['energia'] = min(100.0, atual + boost)
        
        # Registrar participação em evento
        eventos_participados = self.metricas_agentes[agente_id].get('eventos_participados', [])
        eventos_participados.append({
            'timestamp': datetime.now().isoformat(),
            'intensidade': intensidade,
            'efeitos': list(efeitos.keys())
        })
        self.metricas_agentes[agente_id]['eventos_participados'] = eventos_participados[-10:]  # Manter últimos 10
    
    def processar_eventos_ativos(self):
        """Processa eventos ativos, atualizando fases e finalizando quando necessário"""
        
        eventos_para_remover = []
        
        for evento_id, evento in self.eventos_ativos.items():
            # Calcular tempo decorrido
            tempo_decorrido = datetime.now() - evento.timestamp_inicio
            
            # Atualizar fase do evento
            self._atualizar_fase_evento(evento, tempo_decorrido)
            
            # Verificar se evento deve finalizar
            if (tempo_decorrido >= evento.duracao_prevista or 
                evento.fase_atual == FaseEvento.INTEGRACAO):
                self._finalizar_evento(evento)
                eventos_para_remover.append(evento_id)
        
        # Remover eventos finalizados
        for evento_id in eventos_para_remover:
            del self.eventos_ativos[evento_id]
        
        # Aplicar decaimento natural nas métricas
        self._aplicar_decaimento_natural()
    
    def _atualizar_fase_evento(self, evento: EventoCognitivoGlobal, tempo_decorrido: timedelta):
        """Atualiza a fase do evento baseado no tempo decorrido"""
        
        duracao_total = evento.duracao_prevista.total_seconds()
        tempo_atual = tempo_decorrido.total_seconds()
        progresso = tempo_atual / duracao_total
        
        if progresso < 0.1:
            evento.fase_atual = FaseEvento.GESTACAO
        elif progresso < 0.3:
            evento.fase_atual = FaseEvento.MANIFESTACAO
        elif progresso < 0.6:
            evento.fase_atual = FaseEvento.PICO
        elif progresso < 0.9:
            evento.fase_atual = FaseEvento.DECLINIO
        else:
            evento.fase_atual = FaseEvento.INTEGRACAO
    
    def _finalizar_evento(self, evento: EventoCognitivoGlobal):
        """Finaliza um evento cognitivo"""
        
        evento.timestamp_fim = datetime.now()
        evento.fase_atual = FaseEvento.MEMORIA
        
        # Calcular métricas de impacto
        duracao_real = evento.timestamp_fim - evento.timestamp_inicio
        evento.metricas_impacto = {
            "duracao_real": duracao_real.total_seconds(),
            "agentes_participantes": len(evento.agentes_participantes),
            "agentes_afetados": len(evento.agentes_afetados),
            "intensidade_media": sum(evento.intensidade_por_agente.values()) / len(evento.intensidade_por_agente) if evento.intensidade_por_agente else 0
        }
        
        # Adicionar ao histórico
        self.historico_eventos.append(evento)
        
        # Atualizar estatísticas
        self.estatisticas['eventos_completados'] += 1
        self.estatisticas['participacao_total_agentes'] += len(evento.agentes_participantes)
        
        # Limitar histórico
        if len(self.historico_eventos) > 100:
            self.historico_eventos = self.historico_eventos[-100:]
    
    def _aplicar_decaimento_natural(self):
        """Aplica decaimento natural nas métricas para evitar acúmulo infinito"""
        
        for agente_id in self.metricas_agentes:
            metricas = self.metricas_agentes[agente_id]
            
            # Decaimento em criatividade e eficiência
            if 'criatividade' in metricas:
                metricas['criatividade'] = max(0.1, metricas['criatividade'] * 0.99)
            
            if 'eficiencia' in metricas:
                metricas['eficiencia'] = max(0.1, metricas['eficiencia'] * 0.99)
        
        # Decaimento nas métricas globais
        self.estado_global.criatividade_emergente *= 0.95
        self.estado_global.sincronizacao_nivel *= 0.98
        if self.estado_global.energia_coletiva < 100:
            self.estado_global.energia_coletiva += 1.0  # Regeneração lenta
    
    def obter_status_eventos(self) -> Dict[str, Any]:
        """Retorna status completo do sistema de eventos"""
        
        return {
            "estado_global": {
                "energia_coletiva": round(self.estado_global.energia_coletiva, 1),
                "sincronizacao_nivel": round(self.estado_global.sincronizacao_nivel, 2),
                "criatividade_emergente": round(self.estado_global.criatividade_emergente, 2),
                "harmonia_sistemica": round(self.estado_global.harmonia_sistemica, 2),
                "turbulencia_cognitiva": round(self.estado_global.turbulencia_cognitiva, 2),
                "foco_coletivo": self.estado_global.foco_coletivo,
                "temas_ressonantes": self.estado_global.temas_ressonantes,
                "agentes_online": len(self.estado_global.agentes_online)
            },
            "eventos_ativos": {
                evento_id: {
                    "tipo": evento.tipo.value,
                    "intensidade": evento.intensidade.value,
                    "fase": evento.fase_atual.value,
                    "duracao": str(datetime.now() - evento.timestamp_inicio),
                    "participantes": len(evento.agentes_participantes),
                    "epicentro": evento.epicentro,
                    "narrativa": evento.narrativa_evento
                } for evento_id, evento in self.eventos_ativos.items()
            },
            "historico_recente": [
                {
                    "tipo": evento.tipo.value,
                    "intensidade": evento.intensidade.value,
                    "timestamp": evento.timestamp_inicio.isoformat(),
                    "duracao": str(evento.timestamp_fim - evento.timestamp_inicio) if evento.timestamp_fim else None,
                    "participantes": len(evento.agentes_participantes),
                    "impacto": evento.metricas_impacto
                } for evento in self.historico_eventos[-5:]
            ],
            "estatisticas": dict(self.estatisticas),
            "padroes_ativos": len([
                p for p in self.padroes_evento.values()
                if self._verificar_padrao(p)
            ])
        }
    
    def _carregar_estado(self):
        """Carrega estado do disco"""
        arquivo_estado = self.eventos_dir / "eventos_cognitivos_globais.json"
        if arquivo_estado.exists():
            try:
                with open(arquivo_estado, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # Carregar estado global
                estado_data = dados.get('estado_global', {})
                self.estado_global.energia_coletiva = estado_data.get('energia_coletiva', 100.0)
                self.estado_global.sincronizacao_nivel = estado_data.get('sincronizacao_nivel', 0.0)
                self.estado_global.criatividade_emergente = estado_data.get('criatividade_emergente', 0.0)
                
                # Carregar estatísticas
                self.estatisticas.update(dados.get('estatisticas', {}))
                
                # Converter strings de volta para defaultdict
                eventos_por_tipo = dados.get('estatisticas', {}).get('eventos_por_tipo', {})
                self.estatisticas['eventos_por_tipo'] = defaultdict(int, eventos_por_tipo)
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar eventos cognitivos: {e}")
    
    def _salvar_estado(self):
        """Salva estado no disco"""
        arquivo_estado = self.eventos_dir / "eventos_cognitivos_globais.json"
        
        dados = {
            'estado_global': {
                'energia_coletiva': self.estado_global.energia_coletiva,
                'sincronizacao_nivel': self.estado_global.sincronizacao_nivel,
                'criatividade_emergente': self.estado_global.criatividade_emergente,
                'harmonia_sistemica': self.estado_global.harmonia_sistemica,
                'turbulencia_cognitiva': self.estado_global.turbulencia_cognitiva,
                'foco_coletivo': self.estado_global.foco_coletivo,
                'temas_ressonantes': self.estado_global.temas_ressonantes
            },
            'estatisticas': {
                'eventos_detectados': self.estatisticas['eventos_detectados'],
                'eventos_completados': self.estatisticas['eventos_completados'],
                'participacao_total_agentes': self.estatisticas['participacao_total_agentes'],
                'eventos_por_tipo': dict(self.estatisticas['eventos_por_tipo'])
            },
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_estado, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar eventos cognitivos: {e}")


# Instância global do orquestrador
_orquestrador_eventos = None

def obter_orquestrador_eventos() -> OrquestradorEventosCognitivos:
    """Obtém instância singleton do orquestrador"""
    global _orquestrador_eventos
    if _orquestrador_eventos is None:
        _orquestrador_eventos = OrquestradorEventosCognitivos()
    return _orquestrador_eventos

def atualizar_metricas_agente_global(agente_id: str, metricas: Dict[str, float]):
    """Função conveniente para atualizar métricas de agente"""
    orquestrador = obter_orquestrador_eventos()
    orquestrador.atualizar_metricas_agente(agente_id, metricas)

def processar_eventos_cognitivos():
    """Função conveniente para processar eventos ativos"""
    orquestrador = obter_orquestrador_eventos()
    orquestrador.processar_eventos_ativos()

def obter_status_eventos_globais() -> Dict[str, Any]:
    """Função conveniente para obter status dos eventos"""
    orquestrador = obter_orquestrador_eventos()
    return orquestrador.obter_status_eventos()