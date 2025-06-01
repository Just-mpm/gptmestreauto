"""
🌟 TORRE SHADOW v2.0 - SWARM INTELIGENTE
Sistema avançado de execução paralela silenciosa com múltiplas sombras e aprendizado
"""

import asyncio
import json
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Callable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

# Try psutil first, fallback to mock implementation
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False
    from utils.fallback_psutil import fallback_psutil as psutil

from .base_agent_v2 import BaseAgentV2
from utils.logger import get_logger

logger = get_logger("torre_shadow")


class TipoShadow(Enum):
    """Tipos de shadow disponíveis"""
    PRINCIPAL = "principal"
    ALTERNATIVO = "alternativo"
    CRIATIVO = "criativo"
    CONSERVADOR = "conservador"
    PREDITIVO = "preditivo"
    LEARNING = "learning"


class StatusShadow(Enum):
    """Status de execução do shadow"""
    AGUARDANDO = "aguardando"
    EXECUTANDO = "executando"
    COMPLETADO = "completado"
    ERRO = "erro"
    CANCELADO = "cancelado"


@dataclass
class ShadowExecution:
    """Resultado de uma execução shadow"""
    id: str
    tipo: TipoShadow
    entrada: str
    resultado: str
    confianca: float
    tempo_execucao: float
    recursos_usados: Dict
    timestamp: datetime
    status: StatusShadow
    comparacao_principal: Optional[float] = None
    aprendizados: List[str] = None


@dataclass
class ShadowComparison:
    """Comparação entre shadow e resultado principal"""
    principal_score: float
    shadow_score: float
    diferenca: float
    melhor: str  # "principal" ou "shadow"
    insights: List[str]
    recomendacao: str


@dataclass
class RecursosDisponiveis:
    """Estado atual dos recursos do sistema"""
    cpu_percent: float
    memoria_percent: float
    tokens_disponiveis: int
    threads_ativas: int
    carga_sistema: float
    permite_shadow: bool


class GerenciadorRecursos:
    """Gerencia recursos do sistema para execução de shadows"""
    
    def __init__(self):
        self.limite_cpu = 70.0  # %
        self.limite_memoria = 80.0  # %
        self.limite_threads = 10
        self.tokens_reserva = 1000
        
    def avaliar_recursos(self) -> RecursosDisponiveis:
        """Avalia recursos disponíveis do sistema"""
        cpu = psutil.cpu_percent(interval=0.1)
        memoria = psutil.virtual_memory().percent
        threads = threading.active_count()
        
        # Simular tokens disponíveis (em produção seria baseado na API)
        tokens_estimados = 8000  # Estimativa conservadora
        
        carga = (cpu + memoria) / 2
        
        permite = (
            cpu < self.limite_cpu and
            memoria < self.limite_memoria and
            threads < self.limite_threads and
            tokens_estimados > self.tokens_reserva
        )
        
        return RecursosDisponiveis(
            cpu_percent=cpu,
            memoria_percent=memoria,
            tokens_disponiveis=tokens_estimados,
            threads_ativas=threads,
            carga_sistema=carga,
            permite_shadow=permite
        )
    
    def calcular_shadows_permitidos(self, recursos: RecursosDisponiveis) -> int:
        """Calcula quantos shadows podem ser executados"""
        if not recursos.permite_shadow:
            return 0
        
        # Baseado na carga do sistema
        if recursos.carga_sistema < 30:
            return 3  # Múltiplos shadows
        elif recursos.carga_sistema < 50:
            return 2  # Dois shadows
        elif recursos.carga_sistema < 70:
            return 1  # Um shadow
        else:
            return 0  # Nenhum shadow


class ShadowPrincipal:
    """Shadow principal que executa abordagem alternativa"""
    
    def __init__(self):
        self.historico = []
        self.padroes_sucesso = {}
        
    async def executar(self, entrada: str, contexto: Dict, metodo_principal: Callable) -> ShadowExecution:
        """Executa shadow principal com abordagem alternativa"""
        inicio = time.time()
        
        try:
            # Criar abordagem alternativa
            entrada_alternativa = self._criar_abordagem_alternativa(entrada, contexto)
            
            # Executar método com abordagem alternativa
            resultado = await self._executar_com_timeout(
                metodo_principal, entrada_alternativa, contexto
            )
            
            tempo = time.time() - inicio
            
            shadow = ShadowExecution(
                id=self._gerar_id(entrada),
                tipo=TipoShadow.PRINCIPAL,
                entrada=entrada_alternativa,
                resultado=resultado,
                confianca=0.8,  # Confiança padrão
                tempo_execucao=tempo,
                recursos_usados=self._capturar_recursos(),
                timestamp=datetime.now(),
                status=StatusShadow.COMPLETADO,
                aprendizados=[]
            )
            
            self.historico.append(shadow)
            return shadow
            
        except Exception as e:
            logger.error(f"❌ Erro no ShadowPrincipal: {e}")
            return ShadowExecution(
                id=self._gerar_id(entrada),
                tipo=TipoShadow.PRINCIPAL,
                entrada=entrada,
                resultado=f"Erro: {str(e)}",
                confianca=0.0,
                tempo_execucao=time.time() - inicio,
                recursos_usados={},
                timestamp=datetime.now(),
                status=StatusShadow.ERRO,
                aprendizados=[]
            )
    
    def _criar_abordagem_alternativa(self, entrada: str, contexto: Dict) -> str:
        """Cria abordagem alternativa para a entrada"""
        # Estratégias alternativas
        estrategias = [
            f"Abordagem inversa: {entrada}",
            f"Perspectiva contrária: {entrada}",
            f"Metodologia diferente: {entrada}",
            f"Foco alternativo: {entrada}"
        ]
        
        # Escolher baseado no hash da entrada para consistência
        indice = hash(entrada) % len(estrategias)
        return estrategias[indice]
    
    async def _executar_com_timeout(self, metodo: Callable, entrada: str, contexto: Dict, timeout: float = 15.0) -> str:
        """Executa método com timeout"""
        try:
            return await asyncio.wait_for(
                metodo(entrada, contexto),
                timeout=timeout
            )
        except asyncio.TimeoutError:
            return "Shadow timeout - execução cancelada"
    
    def _gerar_id(self, entrada: str) -> str:
        """Gera ID único para shadow"""
        return hashlib.md5(f"shadow_{entrada}_{time.time()}".encode()).hexdigest()[:8]
    
    def _capturar_recursos(self) -> Dict:
        """Captura uso atual de recursos"""
        return {
            "cpu": psutil.cpu_percent(),
            "memoria": psutil.virtual_memory().percent,
            "timestamp": time.time()
        }


class ShadowSwarm:
    """Swarm de múltiplos shadows trabalhando em paralelo"""
    
    def __init__(self, max_shadows: int = 3):
        self.max_shadows = max_shadows
        self.shadows_ativos = []
        self.resultados = []
        
    async def executar_swarm(self, entrada: str, contexto: Dict, metodos: List[Callable]) -> List[ShadowExecution]:
        """Executa múltiplos shadows em paralelo"""
        # Limitar número de shadows baseado em recursos
        gerenciador = GerenciadorRecursos()
        recursos = gerenciador.avaliar_recursos()
        max_permitido = gerenciador.calcular_shadows_permitidos(recursos)
        
        num_shadows = min(self.max_shadows, max_permitido, len(metodos))
        
        if num_shadows == 0:
            logger.warning("⚠️ Recursos insuficientes para execução de shadows")
            return []
        
        # Criar tasks para execução paralela
        tasks = []
        for i in range(num_shadows):
            metodo = metodos[i % len(metodos)]
            task = self._executar_shadow_individual(entrada, contexto, metodo, i)
            tasks.append(task)
        
        # Executar em paralelo
        resultados = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar resultados
        shadows_validos = []
        for resultado in resultados:
            if isinstance(resultado, ShadowExecution):
                shadows_validos.append(resultado)
            else:
                logger.error(f"❌ Erro em shadow: {resultado}")
        
        self.resultados.extend(shadows_validos)
        return shadows_validos
    
    async def _executar_shadow_individual(self, entrada: str, contexto: Dict, metodo: Callable, indice: int) -> ShadowExecution:
        """Executa um shadow individual"""
        inicio = time.time()
        
        try:
            # Criar variação da entrada para este shadow
            entrada_variada = self._criar_variacao(entrada, indice)
            
            # Executar método
            resultado = await metodo(entrada_variada, contexto)
            
            tempo = time.time() - inicio
            
            return ShadowExecution(
                id=f"swarm_{indice}_{int(time.time())}",
                tipo=TipoShadow.ALTERNATIVO,
                entrada=entrada_variada,
                resultado=resultado,
                confianca=0.7,
                tempo_execucao=tempo,
                recursos_usados={"indice": indice},
                timestamp=datetime.now(),
                status=StatusShadow.COMPLETADO,
                aprendizados=[]
            )
            
        except Exception as e:
            return ShadowExecution(
                id=f"swarm_erro_{indice}",
                tipo=TipoShadow.ALTERNATIVO,
                entrada=entrada,
                resultado=f"Erro: {str(e)}",
                confianca=0.0,
                tempo_execucao=time.time() - inicio,
                recursos_usados={},
                timestamp=datetime.now(),
                status=StatusShadow.ERRO,
                aprendizados=[]
            )
    
    def _criar_variacao(self, entrada: str, indice: int) -> str:
        """Cria variação da entrada para shadow específico"""
        variacoes = [
            f"Primeira abordagem: {entrada}",
            f"Segunda perspectiva: {entrada}",
            f"Terceira análise: {entrada}",
            f"Quarta metodologia: {entrada}"
        ]
        
        return variacoes[indice % len(variacoes)]


class PredictiveShadow:
    """Shadow que antecipa próximas necessidades do usuário"""
    
    def __init__(self):
        self.padroes_usuario = {}
        self.predicoes_ativas = []
        
    async def prever_proximas_tarefas(self, contexto: Dict, historico: List) -> List[str]:
        """Prevê próximas tarefas baseado em padrões"""
        predicoes = []
        
        # Analisar padrões no histórico
        if len(historico) >= 3:
            ultimas_tarefas = [item.get("tipo", "") for item in historico[-3:]]
            
            # Padrões comuns identificados
            if "pesquisa" in ultimas_tarefas:
                predicoes.append("Usuário pode precisar de análise dos dados pesquisados")
            
            if "analise" in ultimas_tarefas:
                predicoes.append("Usuário pode querer implementação das recomendações")
            
            if "planejamento" in ultimas_tarefas:
                predicoes.append("Usuário pode precisar de execução do plano")
        
        # Padrões temporais
        hora_atual = datetime.now().hour
        if 9 <= hora_atual <= 11:
            predicoes.append("Horário típico de planejamento estratégico")
        elif 14 <= hora_atual <= 16:
            predicoes.append("Horário típico de execução de tarefas")
        
        return predicoes[:3]  # Limitar a 3 predições
    
    async def pre_carregar_recursos(self, predicoes: List[str]) -> Dict:
        """Pré-carrega recursos baseado nas predições"""
        recursos_pre_carregados = {}
        
        for predicao in predicoes:
            if "análise" in predicao.lower():
                recursos_pre_carregados["templates_analise"] = "carregado"
            elif "planejamento" in predicao.lower():
                recursos_pre_carregados["frameworks_planejamento"] = "carregado"
            elif "execução" in predicao.lower():
                recursos_pre_carregados["checklists_execucao"] = "carregado"
        
        return recursos_pre_carregados


class LearningShadow:
    """Shadow que aprende com diferenças e melhora o agente principal"""
    
    def __init__(self):
        self.aprendizados = []
        self.padroes_melhorias = {}
        self.score_historico = []
        
    def comparar_resultados(self, resultado_principal: str, shadows: List[ShadowExecution]) -> ShadowComparison:
        """Compara resultado principal com shadows"""
        melhor_shadow = self._encontrar_melhor_shadow(shadows)
        
        if not melhor_shadow:
            return ShadowComparison(
                principal_score=1.0,
                shadow_score=0.0,
                diferenca=1.0,
                melhor="principal",
                insights=["Nenhum shadow válido para comparação"],
                recomendacao="Manter abordagem principal"
            )
        
        # Calcular scores (simplificado)
        principal_score = self._calcular_score_resultado(resultado_principal)
        shadow_score = melhor_shadow.confianca
        
        diferenca = abs(principal_score - shadow_score)
        melhor = "shadow" if shadow_score > principal_score else "principal"
        
        # Gerar insights
        insights = self._gerar_insights(resultado_principal, melhor_shadow)
        
        # Gerar recomendação
        recomendacao = self._gerar_recomendacao(principal_score, shadow_score, diferenca)
        
        comparacao = ShadowComparison(
            principal_score=principal_score,
            shadow_score=shadow_score,
            diferenca=diferenca,
            melhor=melhor,
            insights=insights,
            recomendacao=recomendacao
        )
        
        # Registrar para aprendizado
        self._registrar_aprendizado(comparacao)
        
        return comparacao
    
    def _encontrar_melhor_shadow(self, shadows: List[ShadowExecution]) -> Optional[ShadowExecution]:
        """Encontra o shadow com melhor performance"""
        shadows_validos = [s for s in shadows if s.status == StatusShadow.COMPLETADO]
        
        if not shadows_validos:
            return None
        
        return max(shadows_validos, key=lambda s: s.confianca)
    
    def _calcular_score_resultado(self, resultado: str) -> float:
        """Calcula score de qualidade do resultado"""
        # Algoritmo simplificado baseado em características do resultado
        score = 0.5  # Base
        
        if len(resultado) > 100:
            score += 0.2  # Resultados mais detalhados
        
        if "análise" in resultado.lower():
            score += 0.1
        
        if "recomendação" in resultado.lower():
            score += 0.1
        
        if "dados" in resultado.lower():
            score += 0.1
        
        return min(1.0, score)
    
    def _gerar_insights(self, principal: str, shadow: ShadowExecution) -> List[str]:
        """Gera insights da comparação"""
        insights = []
        
        if len(shadow.resultado) > len(principal):
            insights.append("Shadow gerou resultado mais detalhado")
        
        if shadow.tempo_execucao < 5.0:
            insights.append("Shadow foi mais eficiente em tempo")
        
        if shadow.confianca > 0.8:
            insights.append("Shadow demonstrou alta confiança")
        
        return insights
    
    def _gerar_recomendacao(self, principal_score: float, shadow_score: float, diferenca: float) -> str:
        """Gera recomendação baseada na comparação"""
        if diferenca < 0.1:
            return "Resultados similares, manter abordagem atual"
        elif shadow_score > principal_score:
            return "Shadow superior, considerar integração da abordagem"
        else:
            return "Principal superior, continuar com abordagem atual"
    
    def _registrar_aprendizado(self, comparacao: ShadowComparison):
        """Registra aprendizado para futuras melhorias"""
        aprendizado = {
            "timestamp": datetime.now().isoformat(),
            "melhor": comparacao.melhor,
            "diferenca": comparacao.diferenca,
            "insights": comparacao.insights,
            "recomendacao": comparacao.recomendacao
        }
        
        self.aprendizados.append(aprendizado)
        self.score_historico.append((comparacao.principal_score, comparacao.shadow_score))
        
        # Limitar histórico
        if len(self.aprendizados) > 100:
            self.aprendizados = self.aprendizados[-50:]
        
        if len(self.score_historico) > 100:
            self.score_historico = self.score_historico[-50:]


class TorreShadowV2(BaseAgentV2):
    """
    🌟 TORRE SHADOW v2.0 - SWARM INTELIGENTE
    
    Sistema avançado de execução paralela silenciosa:
    - Shadow Principal com abordagens alternativas
    - Shadow Swarm com múltiplas perspectivas paralelas
    - Predictive Shadow que antecipa necessidades
    - Learning Shadow que aprende e melhora o sistema
    - Controle inteligente de recursos
    - Comparação automática e aprendizado contínuo
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="TorreShadowV2",
            version="2.0",
            agent_type="shadow_execution",
            primary_function="execucao_paralela_silenciosa",
            capabilities=[
                "shadow_principal", "shadow_swarm", "predictive_shadow",
                "learning_shadow", "resource_management", "auto_comparison"
            ],
            **kwargs
        )
        
        # Componentes do sistema
        self.shadow_principal = ShadowPrincipal()
        self.shadow_swarm = ShadowSwarm(max_shadows=3)
        self.predictive_shadow = PredictiveShadow()
        self.learning_shadow = LearningShadow()
        self.gerenciador_recursos = GerenciadorRecursos()
        
        # Estado do sistema
        self.shadows_executados = []
        self.comparacoes_historico = []
        self.predicoes_ativas = []
        
        # Configurações
        self.modo_ativo = True
        self.limite_shadows_por_minuto = 10
        self.auto_learning = True
        
        logger.info("🌟 TorreShadowV2 inicializada com swarm inteligente")
    
    def _processar_interno(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Implementação do método abstrato"""
        return asyncio.run(self.executar_com_shadow(entrada, contexto or {}, None))
    
    async def executar_com_shadow(self, entrada: str, contexto: Dict, metodo_principal: Optional[Callable] = None) -> Tuple[str, Dict]:
        """Executa tarefa principal com shadows paralelos"""
        try:
            inicio = time.time()
            
            # 1. Avaliar recursos disponíveis
            recursos = self.gerenciador_recursos.avaliar_recursos()
            
            if not recursos.permite_shadow:
                logger.warning("⚠️ Recursos insuficientes para shadows")
                if metodo_principal:
                    resultado_principal = await metodo_principal(entrada, contexto)
                    return resultado_principal, {"shadow_executado": False, "motivo": "recursos_insuficientes"}
                else:
                    return "Shadow: recursos insuficientes", {"shadow_executado": False}
            
            # 2. Executar principal + shadows em paralelo
            resultados = await self._executar_paralelo(entrada, contexto, metodo_principal)
            
            # 3. Comparar e aprender
            if self.auto_learning and len(resultados["shadows"]) > 0:
                comparacao = self.learning_shadow.comparar_resultados(
                    resultados["principal"], resultados["shadows"]
                )
                resultados["comparacao"] = asdict(comparacao)
            
            # 4. Predizer próximas necessidades
            predicoes = await self.predictive_shadow.prever_proximas_tarefas(contexto, self.shadows_executados)
            resultados["predicoes"] = predicoes
            
            # 5. Registrar execução
            tempo_total = time.time() - inicio
            await self._registrar_execucao(entrada, resultados, tempo_total)
            
            return resultados["principal"], resultados
            
        except Exception as e:
            logger.error(f"❌ Erro na TorreShadow: {e}")
            return f"Erro na execução shadow: {str(e)}", {"erro": str(e)}
    
    async def _executar_paralelo(self, entrada: str, contexto: Dict, metodo_principal: Optional[Callable]) -> Dict:
        """Executa método principal e shadows em paralelo"""
        resultados = {
            "principal": "",
            "shadows": [],
            "tempo_execucao": 0,
            "recursos_utilizados": {}
        }
        
        inicio = time.time()
        
        # Criar tasks para execução paralela
        tasks = []
        
        # Task principal
        if metodo_principal:
            tasks.append(self._executar_principal(entrada, contexto, metodo_principal))
        
        # Tasks de shadows
        tasks.append(self._executar_shadows(entrada, contexto, metodo_principal))
        
        # Executar em paralelo
        resultados_paralelos = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Processar resultados
        if metodo_principal and len(resultados_paralelos) >= 2:
            resultados["principal"] = resultados_paralelos[0] if not isinstance(resultados_paralelos[0], Exception) else "Erro no principal"
            resultados["shadows"] = resultados_paralelos[1] if not isinstance(resultados_paralelos[1], Exception) else []
        elif len(resultados_paralelos) >= 1:
            resultados["shadows"] = resultados_paralelos[0] if not isinstance(resultados_paralelos[0], Exception) else []
            resultados["principal"] = "Shadow apenas - sem principal"
        
        resultados["tempo_execucao"] = time.time() - inicio
        return resultados
    
    async def _executar_principal(self, entrada: str, contexto: Dict, metodo: Callable) -> str:
        """Executa método principal"""
        try:
            return await metodo(entrada, contexto)
        except Exception as e:
            logger.error(f"❌ Erro no método principal: {e}")
            return f"Erro: {str(e)}"
    
    async def _executar_shadows(self, entrada: str, contexto: Dict, metodo_principal: Optional[Callable]) -> List[ShadowExecution]:
        """Executa todos os tipos de shadows"""
        shadows = []
        
        # Shadow Principal
        if metodo_principal:
            try:
                shadow_principal = await self.shadow_principal.executar(entrada, contexto, metodo_principal)
                shadows.append(shadow_principal)
            except Exception as e:
                logger.error(f"❌ Erro no ShadowPrincipal: {e}")
        
        # Shadow Swarm (se temos múltiplos métodos simulados)
        if metodo_principal:
            try:
                metodos_swarm = [metodo_principal]  # Em produção, seria lista de métodos diferentes
                shadows_swarm = await self.shadow_swarm.executar_swarm(entrada, contexto, metodos_swarm)
                shadows.extend(shadows_swarm)
            except Exception as e:
                logger.error(f"❌ Erro no ShadowSwarm: {e}")
        
        return shadows
    
    async def _registrar_execucao(self, entrada: str, resultados: Dict, tempo: float):
        """Registra execução para histórico e aprendizado"""
        execucao = {
            "timestamp": datetime.now().isoformat(),
            "entrada": entrada[:100],  # Truncar para economia de espaço
            "num_shadows": len(resultados.get("shadows", [])),
            "tempo_total": tempo,
            "teve_comparacao": "comparacao" in resultados,
            "predicoes": len(resultados.get("predicoes", []))
        }
        
        self.shadows_executados.append(execucao)
        
        # Limitar histórico
        if len(self.shadows_executados) > 1000:
            self.shadows_executados = self.shadows_executados[-500:]
        
        # Registrar evento
        self._registrar_evento("shadow_executado", execucao)
    
    def get_estatisticas_shadow(self) -> Dict:
        """Retorna estatísticas de performance dos shadows"""
        if not self.shadows_executados:
            return {"mensagem": "Nenhum shadow executado ainda"}
        
        recentes = self.shadows_executados[-50:]  # Últimos 50
        
        estatisticas = {
            "total_execucoes": len(self.shadows_executados),
            "tempo_medio": sum(e["tempo_total"] for e in recentes) / len(recentes),
            "shadows_medio_por_execucao": sum(e["num_shadows"] for e in recentes) / len(recentes),
            "taxa_comparacao": sum(1 for e in recentes if e["teve_comparacao"]) / len(recentes),
            "predicoes_medio": sum(e["predicoes"] for e in recentes) / len(recentes),
            "ultima_execucao": recentes[-1]["timestamp"] if recentes else None
        }
        
        return estatisticas
    
    def configurar_shadow(self, **kwargs):
        """Configura parâmetros do sistema shadow"""
        if "modo_ativo" in kwargs:
            self.modo_ativo = kwargs["modo_ativo"]
        
        if "limite_shadows" in kwargs:
            self.limite_shadows_por_minuto = kwargs["limite_shadows"]
        
        if "auto_learning" in kwargs:
            self.auto_learning = kwargs["auto_learning"]
        
        if "max_shadows_swarm" in kwargs:
            self.shadow_swarm.max_shadows = kwargs["max_shadows_swarm"]
        
        logger.info(f"🔧 TorreShadow configurada: {kwargs}")


def criar_torre_shadow() -> TorreShadowV2:
    """Factory function para criar TorreShadowV2"""
    return TorreShadowV2()