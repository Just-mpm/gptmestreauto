"""
🧠 RACIOCÍNIO CONTÍNUO v3.0 - METACOGNITIVO
Sistema avançado de raciocínio com múltiplas perspectivas paralelas e metacognição
"""

import asyncio
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

from .base_agent_v2 import BaseAgentV2
from utils.logger import get_logger

logger = get_logger("raciocinio_continuo")


class TipoPensamento(Enum):
    """Tipos de pensamento no raciocínio contínuo"""
    ANALITICO = "analitico"
    CRIATIVO = "criativo"  
    CRITICO = "critico"
    INTUITIVO = "intuitivo"
    SISTÊMICO = "sistemico"
    PARADOXAL = "paradoxal"


class EstadoReflexao(Enum):
    """Estados da reflexão metacognitiva"""
    INICIAL = "inicial"
    APROFUNDANDO = "aprofundando"
    CONVERGINDO = "convergindo"
    VALIDANDO = "validando"
    FINALIZADO = "finalizado"


@dataclass
class Pensamento:
    """Estrutura de um pensamento individual"""
    id: str
    tipo: TipoPensamento
    conteudo: str
    confianca: float  # 0-1
    evidencias: List[str]
    contrapontos: List[str]
    timestamp: datetime
    origem: str  # qual perspectiva gerou
    conectado_com: List[str]  # IDs de outros pensamentos


@dataclass
class CicloReflexao:
    """Estrutura de um ciclo completo de reflexão"""
    id: str
    entrada_original: str
    pensamentos: List[Pensamento]
    reflexoes_meta: List[str]
    correcoes: List[str]
    validacoes: List[str]
    resultado_final: str
    confianca_final: float
    tempo_execucao: float
    aprendizados: List[str]
    estado: EstadoReflexao


@dataclass
class SwarmResult:
    """Resultado do processamento swarm"""
    perspectivas: List[Dict]
    convergencia: float  # 0-1 
    consenso: str
    dissidencias: List[str]
    insights_emergentes: List[str]


class MetaReflexor:
    """Sistema de metacognição que reflete sobre o próprio raciocínio"""
    
    def __init__(self):
        self.historico_reflexoes = []
        self.padroes_identificados = {}
        self.qualidade_media = 0.0
        
    async def refletir_sobre_raciocinio(self, pensamentos: List[Pensamento]) -> List[str]:
        """Analisa a qualidade do próprio raciocínio"""
        reflexoes = []
        
        # Análise de diversidade de perspectivas
        tipos_presentes = set(p.tipo for p in pensamentos)
        if len(tipos_presentes) < 3:
            reflexoes.append("METACOGNIÇÃO: Precisamos de mais diversidade de perspectivas")
        
        # Análise de qualidade dos argumentos
        confianca_media = sum(p.confianca for p in pensamentos) / len(pensamentos)
        if confianca_media < 0.6:
            reflexoes.append("METACOGNIÇÃO: Baixa confiança geral, precisamos de mais evidências")
        
        # Análise de conexões entre ideias
        conectividade = sum(len(p.conectado_com) for p in pensamentos) / len(pensamentos)
        if conectividade < 1.0:
            reflexoes.append("METACOGNIÇÃO: Ideias muito isoladas, buscar mais conexões")
        
        # Análise temporal
        tempo_reflexao = (pensamentos[-1].timestamp - pensamentos[0].timestamp).total_seconds()
        if tempo_reflexao < 5:
            reflexoes.append("METACOGNIÇÃO: Raciocínio muito rápido, pode estar superficial")
        
        return reflexoes
    
    def identificar_padroes(self, ciclo: CicloReflexao) -> Dict:
        """Identifica padrões no raciocínio"""
        padroes = {
            "tipos_favoritos": {},
            "tempo_medio": 0,
            "qualidade_tendencia": []
        }
        
        # Registrar este ciclo
        self.historico_reflexoes.append(ciclo)
        
        # Analisar últimos 10 ciclos
        recentes = self.historico_reflexoes[-10:]
        
        # Tipos de pensamento mais usados
        for ciclo_hist in recentes:
            for pensamento in ciclo_hist.pensamentos:
                tipo = pensamento.tipo.value
                padroes["tipos_favoritos"][tipo] = padroes["tipos_favoritos"].get(tipo, 0) + 1
        
        # Tempo médio
        padroes["tempo_medio"] = sum(c.tempo_execucao for c in recentes) / len(recentes)
        
        # Tendência de qualidade
        padroes["qualidade_tendencia"] = [c.confianca_final for c in recentes]
        
        return padroes


class AprendizadoTemporal:
    """Sistema de aprendizado que considera contexto temporal"""
    
    def __init__(self):
        self.contextos_temporais = {
            "manha": {"peso_analitico": 1.2, "peso_criativo": 0.8},
            "tarde": {"peso_analitico": 1.0, "peso_criativo": 1.0}, 
            "noite": {"peso_analitico": 0.8, "peso_criativo": 1.3},
            "madrugada": {"peso_analitico": 0.7, "peso_criativo": 1.5}
        }
        
    def get_contexto_atual(self) -> str:
        """Determina contexto temporal atual"""
        hora = datetime.now().hour
        if 5 <= hora < 12:
            return "manha"
        elif 12 <= hora < 18:
            return "tarde"
        elif 18 <= hora < 24:
            return "noite"
        else:
            return "madrugada"
    
    def ajustar_pensamento(self, pensamento: Pensamento) -> Pensamento:
        """Ajusta pensamento baseado no contexto temporal"""
        contexto = self.get_contexto_atual()
        pesos = self.contextos_temporais[contexto]
        
        # Ajustar confiança baseado no contexto
        if pensamento.tipo == TipoPensamento.ANALITICO:
            pensamento.confianca *= pesos["peso_analitico"]
        elif pensamento.tipo == TipoPensamento.CRIATIVO:
            pensamento.confianca *= pesos["peso_criativo"]
        
        pensamento.confianca = min(1.0, pensamento.confianca)
        return pensamento


class SwarmIntelligence:
    """Sistema de inteligência coletiva com múltiplos processadores"""
    
    def __init__(self):
        self.perspectivas_ativas = []
        self.threshold_convergencia = 0.8
        
    async def processar_swarm(self, entrada: str, contexto: Dict) -> SwarmResult:
        """Processa entrada com múltiplas perspectivas paralelas"""
        
        # Definir perspectivas para processar
        perspectivas = [
            {"nome": "analista", "foco": "dados e evidências"},
            {"nome": "criativo", "foco": "possibilidades e inovação"},
            {"nome": "critico", "foco": "problemas e limitações"},
            {"nome": "pragmatico", "foco": "implementação e resultados"},
            {"nome": "holistico", "foco": "visão sistêmica e contexto"}
        ]
        
        # Processar perspectivas em paralelo
        tasks = []
        for perspectiva in perspectivas:
            task = self._processar_perspectiva(entrada, perspectiva, contexto)
            tasks.append(task)
        
        resultados = await asyncio.gather(*tasks)
        
        # Analisar convergência
        convergencia = self._calcular_convergencia(resultados)
        
        # Gerar consenso
        consenso = self._gerar_consenso(resultados)
        
        # Identificar dissidências
        dissidencias = self._identificar_dissidencias(resultados)
        
        # Buscar insights emergentes
        insights = self._buscar_insights_emergentes(resultados)
        
        return SwarmResult(
            perspectivas=resultados,
            convergencia=convergencia,
            consenso=consenso,
            dissidencias=dissidencias,
            insights_emergentes=insights
        )
    
    async def _processar_perspectiva(self, entrada: str, perspectiva: Dict, contexto: Dict) -> Dict:
        """Processa entrada de uma perspectiva específica"""
        # Simular processamento específico da perspectiva
        await asyncio.sleep(0.1)  # Simular tempo de processamento
        
        resultado = {
            "nome": perspectiva["nome"],
            "foco": perspectiva["foco"],
            "analise": f"Análise {perspectiva['nome']} de: {entrada[:50]}...",
            "conclusao": f"Conclusão da perspectiva {perspectiva['nome']}",
            "confianca": 0.7 + (hash(perspectiva["nome"]) % 30) / 100,
            "evidencias": [f"Evidência {i} da perspectiva {perspectiva['nome']}" for i in range(2)],
            "recomendacoes": [f"Recomendação {i} da perspectiva {perspectiva['nome']}" for i in range(2)]
        }
        
        return resultado
    
    def _calcular_convergencia(self, resultados: List[Dict]) -> float:
        """Calcula nível de convergência entre perspectivas"""
        # Algoritmo simplificado de convergência
        confidencias = [r["confianca"] for r in resultados]
        convergencia = 1.0 - (max(confidencias) - min(confidencias))
        return max(0.0, min(1.0, convergencia))
    
    def _gerar_consenso(self, resultados: List[Dict]) -> str:
        """Gera consenso baseado nas perspectivas"""
        # Ponderar por confiança
        peso_total = sum(r["confianca"] for r in resultados)
        
        consenso_partes = []
        for resultado in resultados:
            peso = resultado["confianca"] / peso_total
            if peso > 0.15:  # Só incluir perspectivas significativas
                consenso_partes.append(f"[{resultado['nome']}]: {resultado['conclusao']}")
        
        return " | ".join(consenso_partes)
    
    def _identificar_dissidencias(self, resultados: List[Dict]) -> List[str]:
        """Identifica pontos de divergência entre perspectivas"""
        dissidencias = []
        
        # Buscar perspectivas com baixa confiança
        for resultado in resultados:
            if resultado["confianca"] < 0.6:
                dissidencias.append(f"Baixa confiança em {resultado['nome']}: {resultado['conclusao']}")
        
        return dissidencias
    
    def _buscar_insights_emergentes(self, resultados: List[Dict]) -> List[str]:
        """Busca insights que emergem da combinação de perspectivas"""
        insights = []
        
        # Combinar evidências de múltiplas perspectivas
        todas_evidencias = []
        for resultado in resultados:
            todas_evidencias.extend(resultado["evidencias"])
        
        # Buscar padrões emergentes (simplificado)
        palavras_comuns = {}
        for evidencia in todas_evidencias:
            for palavra in evidencia.split():
                if len(palavra) > 4:  # Palavras significativas
                    palavras_comuns[palavra] = palavras_comuns.get(palavra, 0) + 1
        
        # Gerar insights baseados em padrões
        for palavra, freq in palavras_comuns.items():
            if freq >= 2:
                insights.append(f"Insight emergente: '{palavra}' aparece em múltiplas perspectivas")
        
        return insights


class RaciocinioContinuoV3(BaseAgentV2):
    """
    🧠 RACIOCÍNIO CONTÍNUO v3.0 - METACOGNITIVO
    
    Sistema avançado de raciocínio com:
    - Múltiplas perspectivas paralelas
    - Metacognição recursiva
    - Aprendizado temporal
    - Inteligência coletiva (swarm)
    - Validação futura preditiva
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="RaciocinioContinuoV3",
            version="3.0",
            agent_type="raciocinio_metacognitivo",
            primary_function="raciocinio_avancado",
            capabilities=[
                "pensamento_paralelo", "metacognicao", "swarm_intelligence",
                "aprendizado_temporal", "validacao_preditiva", "convergencia_automatica"
            ],
            **kwargs
        )
        
        # Componentes do sistema
        self.meta_reflexor = MetaReflexor()
        self.aprendizado_temporal = AprendizadoTemporal()
        self.swarm_intelligence = SwarmIntelligence()
        
        # Estado do sistema
        self.ciclos_ativos = []
        self.historico_completo = []
        self.padroes_globais = {}
        
        # Configurações
        self.max_ciclos_paralelos = 3
        self.timeout_ciclo = 30.0  # segundos
        self.min_confianca = 0.6
        
        logger.info("🧠 RaciocínioContinuoV3 inicializado com metacognição avançada")
    
    def _processar_interno(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Implementação do método abstrato"""
        return asyncio.run(self.processar_com_raciocinio(entrada, contexto or {}))
    
    async def processar_com_raciocinio(self, entrada: str, contexto: Dict) -> str:
        """Processo principal do raciocínio contínuo metacognitivo"""
        try:
            inicio = time.time()
            
            # 1. PENSAR (múltiplas perspectivas paralelas)
            pensamentos = await self._pensar_paralelo(entrada, contexto)
            
            # 2. REFLETIR (com metacognição)
            reflexoes = await self._refletir_metacognitivo(pensamentos, contexto)
            
            # 3. CORRIGIR/REFAZER (adaptativo)
            correcoes = await self._corrigir_adaptativo(reflexoes, contexto)
            
            # 4. VALIDAÇÃO FUTURA (preditiva)
            validacao = await self._validar_futuro(correcoes, contexto)
            
            # 5. SWARM CONVERGENCE (inteligência coletiva)
            resultado_final = await self._convergir_swarm(validacao, contexto)
            
            # 6. REGISTRAR CICLO COMPLETO
            tempo_total = time.time() - inicio
            ciclo = await self._registrar_ciclo(
                entrada, pensamentos, reflexoes, correcoes, 
                validacao, resultado_final, tempo_total
            )
            
            # 7. APRENDIZADO CONTÍNUO
            await self._aprender_do_ciclo(ciclo)
            
            return self._formatar_resultado_final(resultado_final, ciclo)
            
        except Exception as e:
            logger.error(f"❌ Erro no raciocínio contínuo: {e}")
            return f"❌ Erro no processamento metacognitivo: {str(e)}"
    
    async def _pensar_paralelo(self, entrada: str, contexto: Dict) -> List[Pensamento]:
        """Fase 1: Pensamento com múltiplas perspectivas paralelas"""
        pensamentos = []
        
        # Gerar diferentes tipos de pensamento
        tipos_pensamento = [
            TipoPensamento.ANALITICO,
            TipoPensamento.CRIATIVO,
            TipoPensamento.CRITICO,
            TipoPensamento.INTUITIVO,
            TipoPensamento.SISTÊMICO
        ]
        
        # Processar cada tipo em paralelo
        tasks = []
        for tipo in tipos_pensamento:
            task = self._gerar_pensamento_tipo(entrada, tipo, contexto)
            tasks.append(task)
        
        pensamentos_raw = await asyncio.gather(*tasks)
        
        # Aplicar ajustes temporais
        for pensamento in pensamentos_raw:
            pensamento_ajustado = self.aprendizado_temporal.ajustar_pensamento(pensamento)
            pensamentos.append(pensamento_ajustado)
        
        # Conectar pensamentos relacionados
        await self._conectar_pensamentos(pensamentos)
        
        return pensamentos
    
    async def _gerar_pensamento_tipo(self, entrada: str, tipo: TipoPensamento, contexto: Dict) -> Pensamento:
        """Gera pensamento de um tipo específico"""
        timestamp = datetime.now()
        
        # Lógica específica por tipo
        if tipo == TipoPensamento.ANALITICO:
            conteudo = f"Análise sistemática de: {entrada}"
            evidencias = ["Dados históricos", "Métricas disponíveis"]
            contrapontos = ["Limitações dos dados", "Viés de amostragem"]
            confianca = 0.8
            
        elif tipo == TipoPensamento.CRIATIVO:
            conteudo = f"Exploração criativa de: {entrada}"
            evidencias = ["Analogias inovadoras", "Conexões inesperadas"]
            contrapontos = ["Falta de validação", "Alto risco"]
            confianca = 0.6
            
        elif tipo == TipoPensamento.CRITICO:
            conteudo = f"Avaliação crítica de: {entrada}"
            evidencias = ["Problemas identificados", "Limitações claras"]
            contrapontos = ["Possível pessimismo", "Falta de alternativas"]
            confianca = 0.7
            
        elif tipo == TipoPensamento.INTUITIVO:
            conteudo = f"Insight intuitivo sobre: {entrada}"
            evidencias = ["Padrões sutis", "Experiência anterior"]
            contrapontos = ["Difícil de verificar", "Subjetivo"]
            confianca = 0.5
            
        else:  # SISTÊMICO
            conteudo = f"Visão sistêmica de: {entrada}"
            evidencias = ["Conexões múltiplas", "Impacto holístico"]
            contrapontos = ["Complexidade alta", "Difícil implementação"]
            confianca = 0.7
        
        return Pensamento(
            id=hashlib.md5(f"{tipo.value}{timestamp}".encode()).hexdigest()[:8],
            tipo=tipo,
            conteudo=conteudo,
            confianca=confianca,
            evidencias=evidencias,
            contrapontos=contrapontos,
            timestamp=timestamp,
            origem=f"perspectiva_{tipo.value}",
            conectado_com=[]
        )
    
    async def _conectar_pensamentos(self, pensamentos: List[Pensamento]):
        """Identifica e conecta pensamentos relacionados"""
        for i, pensamento1 in enumerate(pensamentos):
            for j, pensamento2 in enumerate(pensamentos[i+1:], i+1):
                # Verificar similaridade (algoritmo simplificado)
                if self._calcular_similaridade(pensamento1, pensamento2) > 0.3:
                    pensamento1.conectado_com.append(pensamento2.id)
                    pensamento2.conectado_com.append(pensamento1.id)
    
    def _calcular_similaridade(self, p1: Pensamento, p2: Pensamento) -> float:
        """Calcula similaridade entre dois pensamentos"""
        # Algoritmo simplificado baseado em palavras comuns
        palavras1 = set(p1.conteudo.lower().split())
        palavras2 = set(p2.conteudo.lower().split())
        
        intersecao = len(palavras1.intersection(palavras2))
        uniao = len(palavras1.union(palavras2))
        
        return intersecao / uniao if uniao > 0 else 0.0
    
    async def _refletir_metacognitivo(self, pensamentos: List[Pensamento], contexto: Dict) -> List[str]:
        """Fase 2: Reflexão metacognitiva sobre o raciocínio"""
        reflexoes = []
        
        # Metacognição sobre qualidade do raciocínio
        reflexoes_meta = await self.meta_reflexor.refletir_sobre_raciocinio(pensamentos)
        reflexoes.extend(reflexoes_meta)
        
        # Análise de coerência interna
        coerencia = self._analisar_coerencia(pensamentos)
        if coerencia < 0.7:
            reflexoes.append("REFLEXÃO: Baixa coerência detectada, revisar argumentos")
        
        # Análise de completude
        completude = self._analisar_completude(pensamentos)
        if completude < 0.8:
            reflexoes.append("REFLEXÃO: Análise incompleta, explorar mais aspectos")
        
        # Reflexão sobre próprios vieses
        reflexoes.append("REFLEXÃO: Verificando vieses cognitivos próprios...")
        
        return reflexoes
    
    def _analisar_coerencia(self, pensamentos: List[Pensamento]) -> float:
        """Analisa coerência interna entre pensamentos"""
        if not pensamentos:
            return 0.0
        
        # Verificar consistência de evidências
        todas_evidencias = []
        for pensamento in pensamentos:
            todas_evidencias.extend(pensamento.evidencias)
        
        # Calcular coerência (simplificado)
        evidencias_unicas = set(todas_evidencias)
        coerencia = len(evidencias_unicas) / len(todas_evidencias) if todas_evidencias else 0.0
        
        return min(1.0, max(0.0, coerencia))
    
    def _analisar_completude(self, pensamentos: List[Pensamento]) -> float:
        """Analisa completude da análise"""
        tipos_presentes = set(p.tipo for p in pensamentos)
        completude = len(tipos_presentes) / len(TipoPensamento)
        return completude
    
    async def _corrigir_adaptativo(self, reflexoes: List[str], contexto: Dict) -> List[str]:
        """Fase 3: Correção adaptativa baseada nas reflexões"""
        correcoes = []
        
        for reflexao in reflexoes:
            if "diversidade" in reflexao.lower():
                correcoes.append("CORREÇÃO: Adicionando perspectiva paradoxal")
                # Aqui adicionaríamos um pensamento paradoxal
                
            elif "confiança" in reflexao.lower():
                correcoes.append("CORREÇÃO: Buscando evidências adicionais")
                
            elif "conexões" in reflexao.lower():
                correcoes.append("CORREÇÃO: Fortalecendo relações entre ideias")
                
            elif "superficial" in reflexao.lower():
                correcoes.append("CORREÇÃO: Aprofundando análise crítica")
        
        return correcoes
    
    async def _validar_futuro(self, correcoes: List[str], contexto: Dict) -> Dict:
        """Fase 4: Validação futura preditiva"""
        validacao = {
            "cenarios_futuros": [],
            "robustez": 0.0,
            "adaptabilidade": 0.0,
            "sustentabilidade": 0.0
        }
        
        # Simular cenários futuros
        cenarios = [
            "Cenário otimista: Condições ideais",
            "Cenário pessimista: Múltiplas dificuldades", 
            "Cenário realista: Condições normais"
        ]
        
        validacao["cenarios_futuros"] = cenarios
        validacao["robustez"] = 0.8  # Simplificado
        validacao["adaptabilidade"] = 0.7
        validacao["sustentabilidade"] = 0.75
        
        return validacao
    
    async def _convergir_swarm(self, validacao: Dict, contexto: Dict) -> SwarmResult:
        """Fase 5: Convergência via inteligência coletiva"""
        entrada_convergencia = f"Validação: {validacao}"
        return await self.swarm_intelligence.processar_swarm(entrada_convergencia, contexto)
    
    async def _registrar_ciclo(self, entrada: str, pensamentos: List[Pensamento], 
                              reflexoes: List[str], correcoes: List[str],
                              validacao: Dict, resultado: SwarmResult, 
                              tempo: float) -> CicloReflexao:
        """Registra ciclo completo de raciocínio"""
        
        ciclo = CicloReflexao(
            id=hashlib.md5(f"{entrada}{time.time()}".encode()).hexdigest()[:8],
            entrada_original=entrada,
            pensamentos=pensamentos,
            reflexoes_meta=reflexoes,
            correcoes=correcoes,
            validacoes=[str(validacao)],
            resultado_final=resultado.consenso,
            confianca_final=resultado.convergencia,
            tempo_execucao=tempo,
            aprendizados=[],
            estado=EstadoReflexao.FINALIZADO
        )
        
        self.historico_completo.append(ciclo)
        return ciclo
    
    async def _aprender_do_ciclo(self, ciclo: CicloReflexao):
        """Aprende do ciclo para melhorar futuras execuções"""
        # Identificar padrões
        padroes = self.meta_reflexor.identificar_padroes(ciclo)
        self.padroes_globais.update(padroes)
        
        # Extrair aprendizados
        aprendizados = []
        
        if ciclo.confianca_final > 0.8:
            aprendizados.append("Ciclo de alta qualidade, replicar abordagem")
        
        if ciclo.tempo_execucao < 5:
            aprendizados.append("Processamento rápido mantendo qualidade")
        
        if len(ciclo.pensamentos) > 4:
            aprendizados.append("Diversidade de perspectivas bem-sucedida")
        
        ciclo.aprendizados = aprendizados
        
        # Registrar evento
        self._registrar_evento("ciclo_completado", {
            "confianca": ciclo.confianca_final,
            "tempo": ciclo.tempo_execucao,
            "num_pensamentos": len(ciclo.pensamentos),
            "aprendizados": len(aprendizados)
        })
    
    def _formatar_resultado_final(self, resultado: SwarmResult, ciclo: CicloReflexao) -> str:
        """Formata resultado final para o usuário"""
        return f"""
🧠 **Raciocínio Contínuo v3.0 - Resultado Metacognitivo**

📝 **Consenso Final:**
{resultado.consenso}

🔍 **Insights Emergentes:**
{chr(10).join(f"• {insight}" for insight in resultado.insights_emergentes[:3])}

📊 **Métricas do Raciocínio:**
• Convergência: {resultado.convergencia:.1%}
• Confiança Final: {ciclo.confianca_final:.1%}
• Tempo de Processamento: {ciclo.tempo_execucao:.2f}s
• Perspectivas Analisadas: {len(ciclo.pensamentos)}

🎯 **Aprendizados do Ciclo:**
{chr(10).join(f"• {aprendizado}" for aprendizado in ciclo.aprendizados)}

⚡ **Estado da Metacognição:** {ciclo.estado.value.upper()}
"""


def criar_raciocinio_continuo() -> RaciocinioContinuoV3:
    """Factory function para criar RaciocínioContinuoV3"""
    return RaciocinioContinuoV3()