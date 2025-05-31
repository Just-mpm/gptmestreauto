"""
TaskBreaker v1.0 - Agente de Decomposição de Tarefas
Sistema inteligente para quebrar tarefas complexas em subtarefas executáveis
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid

from agents.base_agent import BaseAgent

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

class TipoSubtarefa(Enum):
    """Tipos de subtarefas identificadas"""
    PESQUISA = "pesquisa"
    ANALISE = "analise"
    CRIACAO = "criacao"
    VALIDACAO = "validacao"
    INTEGRACAO = "integracao"
    OTIMIZACAO = "otimizacao"
    DECISAO = "decisao"
    EXECUCAO = "execucao"

class PrioridadeSubtarefa(Enum):
    """Níveis de prioridade"""
    CRITICA = "critica"
    ALTA = "alta"
    MEDIA = "media"
    BAIXA = "baixa"

class StatusSubtarefa(Enum):
    """Status de execução"""
    PENDENTE = "pendente"
    EM_PROGRESSO = "em_progresso"
    CONCLUIDA = "concluida"
    BLOQUEADA = "bloqueada"
    FALHOU = "falhou"

@dataclass
class Subtarefa:
    """Representação de uma subtarefa"""
    id: str
    titulo: str
    descricao: str
    tipo: TipoSubtarefa
    prioridade: PrioridadeSubtarefa
    agentes_sugeridos: List[str]
    dependencias: List[str] = field(default_factory=list)
    tempo_estimado: int = 60  # segundos
    status: StatusSubtarefa = StatusSubtarefa.PENDENTE
    resultado: Optional[str] = None
    tentativas: int = 0
    max_tentativas: int = 3

@dataclass
class PlanoExecucao:
    """Plano completo de execução"""
    id: str
    tarefa_original: str
    subtarefas: List[Subtarefa]
    tempo_total_estimado: int
    complexidade: float
    pode_paralelo: bool
    criado_em: datetime = field(default_factory=datetime.now)
    
    def get_proximas_tarefas(self) -> List[Subtarefa]:
        """Retorna próximas tarefas disponíveis para execução"""
        disponiveis = []
        for subtarefa in self.subtarefas:
            if subtarefa.status == StatusSubtarefa.PENDENTE:
                # Verificar se todas as dependências foram concluídas
                deps_ok = all(
                    self.get_subtarefa_por_id(dep_id).status == StatusSubtarefa.CONCLUIDA
                    for dep_id in subtarefa.dependencias
                )
                if deps_ok:
                    disponiveis.append(subtarefa)
        return disponiveis
    
    def get_subtarefa_por_id(self, id: str) -> Optional[Subtarefa]:
        """Busca subtarefa por ID"""
        for subtarefa in self.subtarefas:
            if subtarefa.id == id:
                return subtarefa
        return None
    
    def get_progresso(self) -> float:
        """Calcula progresso do plano (0-100)"""
        if not self.subtarefas:
            return 0.0
        concluidas = sum(1 for st in self.subtarefas if st.status == StatusSubtarefa.CONCLUIDA)
        return (concluidas / len(self.subtarefas)) * 100

class TaskBreaker(BaseAgent):
    """Agente especialista em quebrar tarefas complexas"""
    
    def __init__(self, **kwargs):
        super().__init__(
            name="TaskBreaker",
            description="Sistema de decomposição inteligente de tarefas"
        )
        
        # Configurações
        self.max_subtarefas = kwargs.get('max_subtarefas', 10)
        self.min_complexidade_quebra = kwargs.get('min_complexidade_quebra', 3.0)
        
        # Mapeamento de capacidades para agentes
        self.capacidades_agentes = {
            "pesquisa_web": ["deepagent"],
            "decisao_complexa": ["oraculo", "supervisor"],
            "analise": ["supervisor", "reflexor"],
            "criacao": ["supervisor"],
            "otimizacao": ["reflexor"],
            "planejamento": ["automaster"],
            "validacao": ["reflexor"],
            "integracao": ["supervisor"]
        }
        
        # Histórico de planos
        self.planos_criados = []
        
        logger.info("🔨 TaskBreaker v1.0 inicializado")
    
    def analisar_tarefa(self, tarefa: str, contexto: Optional[Dict] = None) -> PlanoExecucao:
        """
        Analisa uma tarefa e cria plano de execução
        
        Args:
            tarefa: Descrição da tarefa a ser quebrada
            contexto: Contexto adicional
            
        Returns:
            PlanoExecucao com subtarefas organizadas
        """
        logger.info(f"🔍 Analisando tarefa: {tarefa[:50]}...")
        
        # 1. Avaliar complexidade
        complexidade = self._avaliar_complexidade(tarefa)
        logger.info(f"📊 Complexidade avaliada: {complexidade:.1f}")
        
        # 2. Decidir se precisa quebrar
        if complexidade < self.min_complexidade_quebra:
            # Tarefa simples, não precisa quebrar
            return self._criar_plano_simples(tarefa)
        
        # 3. Identificar componentes da tarefa
        componentes = self._identificar_componentes(tarefa)
        
        # 4. Gerar subtarefas
        subtarefas = self._gerar_subtarefas(tarefa, componentes)
        
        # 5. Estabelecer dependências
        subtarefas = self._estabelecer_dependencias(subtarefas)
        
        # 6. Otimizar ordem de execução
        subtarefas = self._otimizar_ordem(subtarefas)
        
        # 7. Criar plano final
        plano = PlanoExecucao(
            id=f"plano_{uuid.uuid4().hex[:8]}",
            tarefa_original=tarefa,
            subtarefas=subtarefas,
            tempo_total_estimado=sum(st.tempo_estimado for st in subtarefas),
            complexidade=complexidade,
            pode_paralelo=self._verificar_paralelismo(subtarefas)
        )
        
        self.planos_criados.append(plano)
        logger.info(f"✅ Plano criado com {len(subtarefas)} subtarefas")
        
        return plano
    
    def _avaliar_complexidade(self, tarefa: str) -> float:
        """Avalia complexidade da tarefa (0-10)"""
        complexidade = 1.0
        
        # Fatores que aumentam complexidade
        palavras_complexas = [
            'sistema', 'integrar', 'completo', 'múltiplos', 'vários',
            'complexo', 'análise', 'estratégia', 'arquitetura', 'criar'
        ]
        
        for palavra in palavras_complexas:
            if palavra in tarefa.lower():
                complexidade += 1.0
        
        # Tamanho da descrição
        palavras = len(tarefa.split())
        if palavras > 20:
            complexidade += 1.0
        if palavras > 50:
            complexidade += 2.0
        
        # Presença de lista ou múltiplas ações
        if any(sep in tarefa for sep in [',', ';', '\n', ' e ']):
            complexidade += 1.5
        
        # Verbos de ação múltipla
        verbos_acao = ['criar', 'desenvolver', 'implementar', 'analisar', 'otimizar']
        verbos_encontrados = sum(1 for verbo in verbos_acao if verbo in tarefa.lower())
        complexidade += verbos_encontrados * 0.5
        
        return min(complexidade, 10.0)
    
    def _identificar_componentes(self, tarefa: str) -> Dict[str, List[str]]:
        """Identifica componentes principais da tarefa"""
        prompt = f"""Analise esta tarefa e identifique seus componentes principais:

Tarefa: {tarefa}

Identifique:
1. AÇÕES necessárias (verbos: criar, analisar, pesquisar, etc)
2. OBJETOS a serem trabalhados (sistema, produto, relatório, etc)
3. REQUISITOS específicos mencionados
4. RESULTADOS esperados

Responda em JSON:
{{
    "acoes": ["acao1", "acao2"],
    "objetos": ["objeto1", "objeto2"],
    "requisitos": ["req1", "req2"],
    "resultados": ["resultado1", "resultado2"]
}}"""
        
        try:
            resposta = self.llm.invoke(prompt).content
            return json.loads(resposta)
        except Exception as e:
            logger.warning(f"⚠️ Erro na análise LLM: {e}")
            # Fallback: análise simples mas robusta
            verbos = self._extrair_verbos(tarefa)
            objetos = self._extrair_substantivos(tarefa)
            logger.info(f"🔧 Fallback: {len(verbos)} verbos, {len(objetos)} objetos")
            return {
                "acoes": verbos if verbos else ["criar", "implementar"],
                "objetos": objetos if objetos else ["aplicativo", "sistema"],
                "requisitos": self._extrair_requisitos(tarefa),
                "resultados": []
            }
    
    def _gerar_subtarefas(self, tarefa: str, componentes: Dict) -> List[Subtarefa]:
        """Gera subtarefas baseadas nos componentes"""
        subtarefas = []
        acoes = componentes.get('acoes', [])
        objetos = componentes.get('objetos', [])
        
        # Se não temos componentes, gerar subtarefas padrão
        if not acoes and not objetos:
            logger.info("🔧 Gerando subtarefas padrão - sem componentes específicos")
            return self._gerar_subtarefas_padrao(tarefa)
        
        # Sempre começar com análise/pesquisa se necessário
        if any(palavra in tarefa.lower() for palavra in ['analisar', 'pesquisar', 'investigar']):
            subtarefas.append(self._criar_subtarefa_pesquisa(componentes))
        
        # Criar subtarefas para cada ação principal
        if acoes and objetos:
            for acao in acoes:
                for objeto in objetos:
                    subtarefa = self._criar_subtarefa_acao(acao, objeto, componentes)
                    if subtarefa:
                        subtarefas.append(subtarefa)
        elif acoes:
            # Apenas ações, sem objetos específicos
            for acao in acoes:
                subtarefa = self._criar_subtarefa_acao(acao, "sistema", componentes)
                if subtarefa:
                    subtarefas.append(subtarefa)
        elif objetos:
            # Apenas objetos, ação padrão
            for objeto in objetos:
                subtarefa = self._criar_subtarefa_acao("desenvolver", objeto, componentes)
                if subtarefa:
                    subtarefas.append(subtarefa)
        
        # Se ainda não temos subtarefas, usar padrão
        if not subtarefas:
            logger.info("🔧 Fallback: Gerando subtarefas padrão")
            return self._gerar_subtarefas_padrao(tarefa)
        
        # Adicionar validação no final se necessário
        if len(subtarefas) > 1:
            subtarefas.append(self._criar_subtarefa_validacao(tarefa))
        
        # Limitar número de subtarefas
        if len(subtarefas) > self.max_subtarefas:
            subtarefas = self._consolidar_subtarefas(subtarefas)
        
        return subtarefas
    
    def _criar_subtarefa_pesquisa(self, componentes: Dict) -> Subtarefa:
        """Cria subtarefa de pesquisa"""
        return Subtarefa(
            id=f"st_{uuid.uuid4().hex[:8]}",
            titulo="Pesquisa e Análise Inicial",
            descricao=f"Pesquisar informações sobre {', '.join(componentes.get('objetos', ['o tema']))}",
            tipo=TipoSubtarefa.PESQUISA,
            prioridade=PrioridadeSubtarefa.ALTA,
            agentes_sugeridos=["deepagent", "supervisor"],
            tempo_estimado=120
        )
    
    def _criar_subtarefa_acao(self, acao: str, objeto: str, componentes: Dict) -> Optional[Subtarefa]:
        """Cria subtarefa para uma ação específica"""
        # Mapear ação para tipo de subtarefa
        mapa_tipos = {
            'criar': TipoSubtarefa.CRIACAO,
            'analisar': TipoSubtarefa.ANALISE,
            'integrar': TipoSubtarefa.INTEGRACAO,
            'otimizar': TipoSubtarefa.OTIMIZACAO,
            'decidir': TipoSubtarefa.DECISAO,
            'executar': TipoSubtarefa.EXECUCAO,
            'validar': TipoSubtarefa.VALIDACAO
        }
        
        tipo = TipoSubtarefa.EXECUCAO  # default
        for palavra, tipo_sub in mapa_tipos.items():
            if palavra in acao.lower():
                tipo = tipo_sub
                break
        
        # Determinar agentes apropriados
        agentes = self._selecionar_agentes_para_tipo(tipo)
        
        return Subtarefa(
            id=f"st_{uuid.uuid4().hex[:8]}",
            titulo=f"{acao.capitalize()} {objeto}",
            descricao=f"Executar ação: {acao} no contexto de {objeto}",
            tipo=tipo,
            prioridade=PrioridadeSubtarefa.MEDIA,
            agentes_sugeridos=agentes,
            tempo_estimado=180
        )
    
    def _criar_subtarefa_validacao(self, tarefa: str) -> Subtarefa:
        """Cria subtarefa de validação final"""
        return Subtarefa(
            id=f"st_{uuid.uuid4().hex[:8]}",
            titulo="Validação e Integração Final",
            descricao="Validar resultados e garantir que todos os objetivos foram alcançados",
            tipo=TipoSubtarefa.VALIDACAO,
            prioridade=PrioridadeSubtarefa.ALTA,
            agentes_sugeridos=["reflexor", "supervisor"],
            tempo_estimado=90
        )
    
    def _estabelecer_dependencias(self, subtarefas: List[Subtarefa]) -> List[Subtarefa]:
        """Estabelece dependências entre subtarefas"""
        if not subtarefas:
            return subtarefas
        
        # Regras básicas de dependência
        for i, subtarefa in enumerate(subtarefas):
            # Pesquisa sempre vem primeiro
            if subtarefa.tipo == TipoSubtarefa.PESQUISA:
                continue
            
            # Validação depende de tudo anterior
            if subtarefa.tipo == TipoSubtarefa.VALIDACAO:
                subtarefa.dependencias = [st.id for st in subtarefas[:i]]
            
            # Integração depende de criação
            elif subtarefa.tipo == TipoSubtarefa.INTEGRACAO:
                for j in range(i):
                    if subtarefas[j].tipo in [TipoSubtarefa.CRIACAO, TipoSubtarefa.EXECUCAO]:
                        subtarefa.dependencias.append(subtarefas[j].id)
            
            # Análise geralmente vem depois de pesquisa
            elif subtarefa.tipo == TipoSubtarefa.ANALISE:
                for j in range(i):
                    if subtarefas[j].tipo == TipoSubtarefa.PESQUISA:
                        subtarefa.dependencias.append(subtarefas[j].id)
        
        return subtarefas
    
    def _otimizar_ordem(self, subtarefas: List[Subtarefa]) -> List[Subtarefa]:
        """Otimiza ordem de execução considerando dependências"""
        # Ordenação topológica simples
        ordenadas = []
        restantes = subtarefas.copy()
        
        while restantes:
            # Encontrar tarefas sem dependências pendentes
            prontas = []
            for subtarefa in restantes:
                deps_satisfeitas = all(
                    any(st.id == dep_id for st in ordenadas)
                    for dep_id in subtarefa.dependencias
                )
                if not subtarefa.dependencias or deps_satisfeitas:
                    prontas.append(subtarefa)
            
            if not prontas:
                # Ciclo detectado ou erro, retornar como está
                logger.warning("⚠️ Ciclo de dependências detectado")
                return subtarefas
            
            # Adicionar prontas priorizando por prioridade
            prontas.sort(key=lambda x: x.prioridade.value)
            ordenadas.extend(prontas)
            
            # Remover prontas das restantes
            for subtarefa in prontas:
                restantes.remove(subtarefa)
        
        return ordenadas
    
    def _verificar_paralelismo(self, subtarefas: List[Subtarefa]) -> bool:
        """Verifica se algumas subtarefas podem ser executadas em paralelo"""
        # Se houver subtarefas sem dependências mútuas, podem ser paralelas
        for i, st1 in enumerate(subtarefas):
            for j, st2 in enumerate(subtarefas[i+1:], i+1):
                # Se não há dependência mútua, podem ser paralelas
                if (st1.id not in st2.dependencias and 
                    st2.id not in st1.dependencias):
                    return True
        return False
    
    def _selecionar_agentes_para_tipo(self, tipo: TipoSubtarefa) -> List[str]:
        """Seleciona agentes apropriados para o tipo de subtarefa"""
        mapa_tipo_capacidade = {
            TipoSubtarefa.PESQUISA: "pesquisa_web",
            TipoSubtarefa.ANALISE: "analise",
            TipoSubtarefa.CRIACAO: "criacao",
            TipoSubtarefa.VALIDACAO: "validacao",
            TipoSubtarefa.INTEGRACAO: "integracao",
            TipoSubtarefa.OTIMIZACAO: "otimizacao",
            TipoSubtarefa.DECISAO: "decisao_complexa",
            TipoSubtarefa.EXECUCAO: "criacao"
        }
        
        capacidade = mapa_tipo_capacidade.get(tipo, "criacao")
        return self.capacidades_agentes.get(capacidade, ["supervisor"])
    
    def _criar_plano_simples(self, tarefa: str) -> PlanoExecucao:
        """Cria plano simples para tarefa não complexa"""
        subtarefa_unica = Subtarefa(
            id=f"st_{uuid.uuid4().hex[:8]}",
            titulo="Executar tarefa",
            descricao=tarefa,
            tipo=TipoSubtarefa.EXECUCAO,
            prioridade=PrioridadeSubtarefa.MEDIA,
            agentes_sugeridos=["supervisor"],
            tempo_estimado=120
        )
        
        return PlanoExecucao(
            id=f"plano_{uuid.uuid4().hex[:8]}",
            tarefa_original=tarefa,
            subtarefas=[subtarefa_unica],
            tempo_total_estimado=120,
            complexidade=1.0,
            pode_paralelo=False
        )
    
    def _consolidar_subtarefas(self, subtarefas: List[Subtarefa]) -> List[Subtarefa]:
        """Consolida subtarefas similares quando há muitas"""
        # Agrupar por tipo
        grupos = {}
        for st in subtarefas:
            if st.tipo not in grupos:
                grupos[st.tipo] = []
            grupos[st.tipo].append(st)
        
        # Consolidar grupos grandes
        consolidadas = []
        for tipo, grupo in grupos.items():
            if len(grupo) > 3:
                # Criar uma subtarefa consolidada
                consolidada = Subtarefa(
                    id=f"st_{uuid.uuid4().hex[:8]}",
                    titulo=f"{tipo.value.capitalize()} - Consolidado",
                    descricao=f"Executar {len(grupo)} ações de {tipo.value}",
                    tipo=tipo,
                    prioridade=PrioridadeSubtarefa.ALTA,
                    agentes_sugeridos=self._selecionar_agentes_para_tipo(tipo),
                    tempo_estimado=sum(st.tempo_estimado for st in grupo)
                )
                consolidadas.append(consolidada)
            else:
                consolidadas.extend(grupo)
        
        return consolidadas[:self.max_subtarefas]
    
    def _extrair_verbos(self, texto: str) -> List[str]:
        """Extrai verbos principais do texto"""
        verbos_comuns = [
            'criar', 'fazer', 'desenvolver', 'implementar', 'analisar',
            'pesquisar', 'otimizar', 'integrar', 'validar', 'testar'
        ]
        encontrados = []
        for verbo in verbos_comuns:
            if verbo in texto.lower():
                encontrados.append(verbo)
        return encontrados[:3]  # Limitar a 3 verbos
    
    def _extrair_substantivos(self, texto: str) -> List[str]:
        """Extrai substantivos principais do texto"""
        # Simplificado - em produção usaria NLP
        palavras = texto.lower().split()
        substantivos_comuns = [
            'sistema', 'produto', 'aplicação', 'projeto', 'relatório',
            'análise', 'estratégia', 'plano', 'código', 'documento',
            'aplicativo', 'mobile', 'app', 'login', 'perfil', 'chat',
            'notificações', 'push', 'usuário', 'interface'
        ]
        encontrados = []
        for palavra in palavras:
            palavra_clean = palavra.replace(',', '').replace('.', '')
            if palavra_clean in substantivos_comuns:
                encontrados.append(palavra_clean)
        return encontrados[:3]  # Limitar a 3 substantivos
    
    def _extrair_requisitos(self, texto: str) -> List[str]:
        """Extrai requisitos mencionados no texto"""
        requisitos = []
        palavras_requisito = ['com', 'incluindo', 'precisa', 'deve', 'ter']
        
        for palavra in palavras_requisito:
            if palavra in texto.lower():
                # Buscar o que vem depois da palavra
                partes = texto.lower().split(palavra)
                if len(partes) > 1:
                    requisito = partes[1].split()[0:3]  # Pegar algumas palavras
                    requisitos.append(' '.join(requisito))
        
        return requisitos[:3]
    
    def _gerar_subtarefas_padrao(self, tarefa: str) -> List[Subtarefa]:
        """Gera subtarefas padrão quando a análise automática falha"""
        subtarefas = []
        
        # Análise inicial sempre
        st1 = Subtarefa(
            id=f"st_{uuid.uuid4().hex[:8]}",
            titulo="Análise e Planejamento",
            descricao=f"Analisar requisitos e planejar execução: {tarefa[:100]}...",
            tipo=TipoSubtarefa.ANALISE,
            prioridade=PrioridadeSubtarefa.ALTA,
            agentes_sugeridos=["supervisor", "oraculo"],
            tempo_estimado=120
        )
        subtarefas.append(st1)
        
        # Execução principal
        st2 = Subtarefa(
            id=f"st_{uuid.uuid4().hex[:8]}",
            titulo="Execução Principal",
            descricao=f"Executar tarefa principal: {tarefa}",
            tipo=TipoSubtarefa.EXECUCAO,
            prioridade=PrioridadeSubtarefa.ALTA,
            agentes_sugeridos=["supervisor"],
            tempo_estimado=180,
            dependencias=[st1.id]
        )
        subtarefas.append(st2)
        
        # Validação final
        st3 = Subtarefa(
            id=f"st_{uuid.uuid4().hex[:8]}",
            titulo="Validação e Entrega",
            descricao="Validar resultados e preparar entrega final",
            tipo=TipoSubtarefa.VALIDACAO,
            prioridade=PrioridadeSubtarefa.MEDIA,
            agentes_sugeridos=["reflexor", "supervisor"],
            tempo_estimado=90,
            dependencias=[st2.id]
        )
        subtarefas.append(st3)
        
        logger.info(f"✅ Criadas {len(subtarefas)} subtarefas padrão")
        return subtarefas
    
    def processar(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Interface padrão do agente - cria e retorna plano"""
        plano = self.analisar_tarefa(mensagem, contexto)
        
        # Formatar resposta
        resposta = f"""📋 **Plano de Execução Criado**

**Tarefa Original:** {plano.tarefa_original}
**Complexidade:** {plano.complexidade:.1f}/10
**Subtarefas:** {len(plano.subtarefas)}
**Tempo Estimado:** {plano.tempo_total_estimado // 60} minutos
**Execução Paralela:** {'✅ Possível' if plano.pode_paralelo else '❌ Sequencial'}

**📝 Subtarefas:**
"""
        
        for i, subtarefa in enumerate(plano.subtarefas, 1):
            deps = f" (depende de: {', '.join(subtarefa.dependencias)})" if subtarefa.dependencias else ""
            resposta += f"""
{i}. **{subtarefa.titulo}**
   - Tipo: {subtarefa.tipo.value}
   - Prioridade: {subtarefa.prioridade.value}
   - Agentes: {', '.join(subtarefa.agentes_sugeridos)}
   - Tempo: {subtarefa.tempo_estimado}s{deps}
"""
        
        return resposta

# Função de criação
def criar_task_breaker(**kwargs) -> TaskBreaker:
    """Cria instância do TaskBreaker"""
    return TaskBreaker(**kwargs)