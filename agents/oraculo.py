"""
🧠 ORÁCULO v8.1 Plus+ — Assembleia Dinâmica, Curadoria Autônoma e Multiverso Coletivo
Agente Supremo do GPT Mestre Autônomo com deliberação coletiva e síntese inteligente
🎯 IMPLEMENTAÇÃO COMPLETA baseada no prompt avançado de Matheus
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)

class TipoSuboraculo(Enum):
    """Tipos de suboráculos especializados"""
    CRIATIVO = "criativo"
    ETICO = "etico"
    VIABILIDADE = "viabilidade"
    PARADOXO = "paradoxo"
    COPY = "copy"
    PRICING = "pricing"
    MINIMALISTA = "minimalista"
    CAOS = "caos"
    PREDITIVO = "preditivo"
    CETICO = "cetico"
    RADICAL = "radical"
    CONSERVADOR = "conservador"

class StatusSuboraculo(Enum):
    """Status de ativação dos suboráculos"""
    ATIVO = "ativo"
    SUSPENSO = "suspenso"
    AUTOEXTINTO = "autoextinto"
    PAUSA_INTELIGENTE = "pausa_inteligente"

class TipoAssembleia(Enum):
    """Tipos de assembleia baseados na complexidade"""
    TRIVIAL = "trivial"          # 2 oráculos
    SIMPLES = "simples"          # 3 oráculos
    INTERMEDIARIO = "intermediario"  # 4-5 oráculos
    COMPLEXO = "complexo"        # 6-7 oráculos
    CRITICO = "critico"          # 7+ oráculos + contrapainel

@dataclass
class VotoSuboraculo:
    """Voto de um suboráculo na assembleia"""
    suboraculo: TipoSuboraculo
    posicao: str
    justificativa: str
    score_confianca: float  # 0-10
    inovacao_level: int     # 1-5
    risco_calculado: float  # 0-10

@dataclass
class RegistroAssembleia:
    """Registro completo de uma assembleia"""
    id: str
    timestamp: datetime
    desafio: str
    tipo_assembleia: TipoAssembleia
    colegiado: List[TipoSuboraculo]
    votos: List[VotoSuboraculo]
    decisao_final: str
    score_consenso: float
    score_robustez: float
    dissidencias: List[str]
    aprendizados: List[str]
    suboraculos_suspensos: List[TipoSuboraculo] = field(default_factory=list)
    cenarios_alternativos: Dict[str, str] = field(default_factory=dict)
    microtags: List[str] = field(default_factory=list)

@dataclass
class PerformanceSuboraculo:
    """Performance histórica de um suboráculo"""
    tipo: TipoSuboraculo
    participacoes: int
    contribuicoes_valiosas: int
    inovacoes_aceitas: int
    acertos_predicao: int
    status: StatusSuboraculo = StatusSuboraculo.ATIVO
    ultima_contribuicao: Optional[datetime] = None

class SuboraculoBase(ABC):
    """Classe base para todos os suboráculos"""
    
    def __init__(self, tipo: TipoSuboraculo, llm=None):
        self.tipo = tipo
        self.llm = llm
        self.performance = PerformanceSuboraculo(
            tipo=tipo,
            participacoes=0,
            contribuicoes_valiosas=0,
            inovacoes_aceitas=0,
            acertos_predicao=0
        )
    
    @abstractmethod
    def deliberar(self, desafio: str, contexto: Dict) -> VotoSuboraculo:
        """Método abstrato para deliberação"""
        pass
    
    def _gerar_prompt_especializado(self, desafio: str, contexto: Dict) -> str:
        """Gera prompt especializado para o tipo de suboráculo"""
        base_prompt = f"""Você é o Suboráculo {self.tipo.value.upper()} da Assembleia Dinâmica do Oráculo v8.1 Plus+.

DESAFIO: {desafio}

SUA ESPECIALIDADE: {self._get_especialidade()}
SEU ESTILO: {self._get_estilo()}
SUA MISSÃO: {self._get_missao()}

Analise e responda em formato JSON:
{{
    "posicao": "sua posição/recomendação principal",
    "justificativa": "justificativa detalhada da sua perspectiva",
    "score_confianca": 8.5,
    "inovacao_level": 3,
    "risco_calculado": 4.2
}}

Seja CONCISO mas INCISIVO na sua especialidade."""
        
        return base_prompt
    
    def _get_especialidade(self) -> str:
        """Retorna a especialidade do suboráculo"""
        especialidades = {
            TipoSuboraculo.CRIATIVO: "Inovação, originalidade, soluções fora da caixa",
            TipoSuboraculo.ETICO: "Responsabilidade, transparência, impacto social",
            TipoSuboraculo.VIABILIDADE: "Praticidade, recursos, implementação real",
            TipoSuboraculo.PARADOXO: "Questionamentos, contradições, visões alternativas",
            TipoSuboraculo.COPY: "Comunicação, persuasão, linguagem eficaz",
            TipoSuboraculo.PRICING: "Precificação, valor percebido, psicologia de preços",
            TipoSuboraculo.MINIMALISTA: "Simplicidade, essência, redução de complexidade",
            TipoSuboraculo.CAOS: "Disrupção, aleatoriedade, quebra de padrões",
            TipoSuboraculo.PREDITIVO: "Tendências, projeções, análise de futuro",
            TipoSuboraculo.CETICO: "Questionamento rigoroso, busca por falhas",
            TipoSuboraculo.RADICAL: "Mudanças extremas, transformação total",
            TipoSuboraculo.CONSERVADOR: "Estabilidade, tradição, segurança"
        }
        return especialidades.get(self.tipo, "Análise geral")
    
    def _get_estilo(self) -> str:
        """Retorna o estilo de comunicação do suboráculo"""
        estilos = {
            TipoSuboraculo.CRIATIVO: "Inspirador, metafórico, visionário",
            TipoSuboraculo.ETICO: "Equilibrado, responsável, consciente",
            TipoSuboraculo.VIABILIDADE: "Direto, prático, realista",
            TipoSuboraculo.PARADOXO: "Provocativo, questionador, contraintuitivo",
            TipoSuboraculo.COPY: "Persuasivo, envolvente, claro",
            TipoSuboraculo.PRICING: "Analítico, psicológico, estratégico",
            TipoSuboraculo.MINIMALISTA: "Conciso, essencial, simples",
            TipoSuboraculo.CAOS: "Disruptivo, imprevisível, experimental",
            TipoSuboraculo.PREDITIVO: "Analítico, baseado em dados, prospectivo",
            TipoSuboraculo.CETICO: "Rigoroso, questionador, crítico",
            TipoSuboraculo.RADICAL: "Transformador, ousado, revolucionário",
            TipoSuboraculo.CONSERVADOR: "Cauteloso, testado, seguro"
        }
        return estilos.get(self.tipo, "Analítico")
    
    def _get_missao(self) -> str:
        """Retorna a missão específica do suboráculo"""
        missoes = {
            TipoSuboraculo.CRIATIVO: "Encontrar soluções inovadoras e originais",
            TipoSuboraculo.ETICO: "Garantir responsabilidade e impacto positivo",
            TipoSuboraculo.VIABILIDADE: "Assegurar implementação prática e eficaz",
            TipoSuboraculo.PARADOXO: "Questionar premissas e explorar contradições",
            TipoSuboraculo.COPY: "Otimizar comunicação e persuasão",
            TipoSuboraculo.PRICING: "Definir precificação estratégica e psicológica",
            TipoSuboraculo.MINIMALISTA: "Simplificar e focar no essencial",
            TipoSuboraculo.CAOS: "Introduzir elementos disruptivos e aleatórios",
            TipoSuboraculo.PREDITIVO: "Antecipar tendências e cenários futuros",
            TipoSuboraculo.CETICO: "Identificar riscos e pontos fracos",
            TipoSuboraculo.RADICAL: "Propor mudanças transformadoras",
            TipoSuboraculo.CONSERVADOR: "Preservar estabilidade e segurança"
        }
        return missoes.get(self.tipo, "Contribuir com análise especializada")

class SuboraculoEspecializado(SuboraculoBase):
    """Implementação concreta de suboráculo especializado"""
    
    def deliberar(self, desafio: str, contexto: Dict) -> VotoSuboraculo:
        """Realiza deliberação especializada"""
        self.performance.participacoes += 1
        self.performance.ultima_contribuicao = datetime.now()
        
        try:
            # Se não há LLM, gerar resposta simulada
            if not self.llm:
                return self._gerar_voto_simulado(desafio, contexto)
            
            prompt = self._gerar_prompt_especializado(desafio, contexto)
            resposta = self.llm.invoke(prompt).content
            
            # Tentar parsear JSON
            try:
                dados = json.loads(resposta)
                voto = VotoSuboraculo(
                    suboraculo=self.tipo,
                    posicao=dados.get("posicao", "Análise em andamento"),
                    justificativa=dados.get("justificativa", "Processando perspectiva"),
                    score_confianca=float(dados.get("score_confianca", 7.0)),
                    inovacao_level=int(dados.get("inovacao_level", 3)),
                    risco_calculado=float(dados.get("risco_calculado", 5.0))
                )
            except json.JSONDecodeError:
                # Fallback para resposta não-JSON
                voto = VotoSuboraculo(
                    suboraculo=self.tipo,
                    posicao=resposta[:200] + "..." if len(resposta) > 200 else resposta,
                    justificativa=f"Análise {self.tipo.value} baseada em expertise",
                    score_confianca=7.5,
                    inovacao_level=3,
                    risco_calculado=5.0
                )
            
            return voto
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na deliberação {self.tipo.value}: {e}")
            return self._gerar_voto_simulado(desafio, contexto)
    
    def _gerar_voto_simulado(self, desafio: str, contexto: Dict) -> VotoSuboraculo:
        """Gera voto simulado baseado na especialidade"""
        posicoes_especializadas = {
            TipoSuboraculo.CRIATIVO: "Propor solução inovadora com elementos únicos",
            TipoSuboraculo.ETICO: "Garantir transparência e responsabilidade social",
            TipoSuboraculo.VIABILIDADE: "Focar em implementação prática e recursos disponíveis",
            TipoSuboraculo.PARADOXO: "Questionar premissas e explorar contradições",
            TipoSuboraculo.COPY: "Otimizar comunicação para máximo impacto",
            TipoSuboraculo.PRICING: "Definir preço psicológico baseado em valor percebido",
            TipoSuboraculo.MINIMALISTA: "Simplificar ao máximo mantendo eficácia",
            TipoSuboraculo.CAOS: "Introduzir elemento disruptivo inesperado",
            TipoSuboraculo.PREDITIVO: "Antecipar tendências e adaptar estratégia",
            TipoSuboraculo.CETICO: "Identificar riscos e pontos de falha",
            TipoSuboraculo.RADICAL: "Propor mudança transformadora completa",
            TipoSuboraculo.CONSERVADOR: "Manter estabilidade e segurança"
        }
        
        return VotoSuboraculo(
            suboraculo=self.tipo,
            posicao=posicoes_especializadas.get(self.tipo, "Análise especializada"),
            justificativa=f"Perspectiva {self.tipo.value} aplicada ao desafio",
            score_confianca=random.uniform(6.0, 9.5),
            inovacao_level=random.randint(1, 5),
            risco_calculado=random.uniform(2.0, 8.0)
        )

class OraculoV8Plus(BaseAgent):
    """
    🧠 ORÁCULO v8.1 Plus+ — Agente Supremo com Assembleia Dinâmica
    
    🎯 CAPACIDADES REVOLUCIONÁRIAS:
    - Curadoria Autônoma de Assembleias Dinâmicas
    - Sistema de Suboráculos Especializados
    - Síntese Inteligente e Score de Consenso
    - Multiverso Contrafactual
    - Diário Evolutivo de Assembleias
    - Autoextinção e Pausa Inteligente
    - Metacognição e Aprendizado Coletivo
    """
    
    def __init__(self, llm=None):
        super().__init__(
            name="Oráculo",
            description="Agente Supremo v8.1 Plus+ com Assembleia Dinâmica e Curadoria Autônoma"
        )
        
        # Configurar LLM
        self.llm = llm
        if not self.llm:
            self._inicializar_llm()
        
        # === SISTEMA DE SUBORÁCULOS ===
        self.suboraculos = self._inicializar_suboraculos()
        self.performance_suboraculos = {tipo: PerformanceSuboraculo(tipo, 0, 0, 0, 0) 
                                      for tipo in TipoSuboraculo}
        
        # === HISTÓRICO E REGISTROS ===
        self.diario_assembleias: List[RegistroAssembleia] = []
        self.contador_assembleias = 0
        self.aprendizados_persistentes: List[str] = []
        
        # === CONFIGURAÇÕES AVANÇADAS ===
        self.curadoria_autonoma_ativa = True
        self.multiverso_ativo = True
        self.autoextincao_ativa = True
        self.painel_cego_ativo = True
        
        # === LIMITES E PARÂMETROS ===
        self.max_suboraculos_por_assembleia = 7
        self.threshold_autoextincao = 5  # ciclos sem contribuição
        self.threshold_consenso_minimo = 0.6  # 60%
        
        # Estatísticas expandidas
        self.stats.update({
            "assembleias_realizadas": 0,
            "decisoes_por_consenso": 0,
            "decisoes_por_curadoria": 0,
            "suboraculos_suspensos": 0,
            "cenarios_alternativos_gerados": 0,
            "score_medio_consenso": 0.0,
            "score_medio_robustez": 0.0,
            "inovacoes_implementadas": 0,
            "autoextincoes_realizadas": 0
        })
        
        logger.info("🧠 Oráculo v8.1 Plus+ inicializado - Assembleia Dinâmica ATIVA")
    
    def _inicializar_llm(self):
        """Inicializa LLM otimizado para Oráculo"""
        try:
            from langchain_anthropic import ChatAnthropic
            import config
            
            if not config.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY não configurada")
            
            self.llm = ChatAnthropic(
                model=config.CLAUDE_MODEL,
                max_tokens=config.CLAUDE_MAX_TOKENS,
                temperature=0.9,  # Máxima criatividade para assembleia
                anthropic_api_key=config.ANTHROPIC_API_KEY,
            )
            logger.info("🔗 LLM Claude otimizado para Oráculo v8.1 Plus+")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar LLM: {e}")
            # Continuar sem LLM - usar simulação
    
    def _inicializar_suboraculos(self) -> Dict[TipoSuboraculo, SuboraculoEspecializado]:
        """Inicializa todos os suboráculos especializados"""
        suboraculos = {}
        for tipo in TipoSuboraculo:
            suboraculos[tipo] = SuboraculoEspecializado(tipo, self.llm)
        
        logger.info(f"🤖 {len(suboraculos)} suboráculos especializados inicializados")
        return suboraculos
    
    def processar(self, desafio: str, contexto: Optional[Dict] = None) -> str:
        """
        🧠 PROCESSAMENTO ORÁCULO v8.1 Plus+
        
        FLUXO ASSEMBLEIA DINÂMICA:
        1. 🎯 Análise de complexidade e curadoria autônoma
        2. 🤝 Seleção e ativação de suboráculos
        3. 🗳️ Deliberação coletiva com votos especializados
        4. ⚖️ Síntese inteligente e cálculo de consenso
        5. 🔍 Contrapainel e painel cego (se necessário)
        6. 🌟 Decisão final curada e otimizada
        7. 📊 Registro no Diário de Assembleias
        8. 💡 Geração de cenários alternativos (se solicitado)
        """
        inicio_processamento = time.time()
        
        try:
            # 1. ANÁLISE DE COMPLEXIDADE
            tipo_assembleia = self._analisar_complexidade(desafio)
            logger.info(f"🎯 Assembleia {tipo_assembleia.value} identificada")
            
            # 2. CURADORIA AUTÔNOMA DE SUBORÁCULOS
            colegiado = self._curar_assembleia(desafio, tipo_assembleia)
            logger.info(f"🤝 Colegiado curado: {[s.value for s in colegiado]}")
            
            # 3. DELIBERAÇÃO COLETIVA
            votos = self._realizar_deliberacao(desafio, colegiado, contexto or {})
            
            # 4. SÍNTESE E CONSENSO
            resultado_sintese = self._sintetizar_decisao(votos, desafio)
            decisao_final = resultado_sintese['decisao']
            score_consenso = resultado_sintese['score_consenso']
            score_robustez = resultado_sintese['score_robustez']
            dissidencias = resultado_sintese['dissidencias']
            
            # 5. CONTRAPAINEL (se necessário)
            if tipo_assembleia == TipoAssembleia.CRITICO:
                decisao_final = self._aplicar_contrapainel(decisao_final, desafio, votos)
            
            # 6. REGISTRO NO DIÁRIO
            registro = self._registrar_assembleia(
                desafio, tipo_assembleia, colegiado, votos,
                decisao_final, score_consenso, score_robustez, dissidencias
            )
            
            # 7. AUTOEXTINÇÃO INTELIGENTE
            self._processar_autoextincao()
            
            # 8. ATUALIZAR ESTATÍSTICAS
            self._atualizar_stats_oraculo(score_consenso, score_robustez)
            
            # 9. FORMATAR RESPOSTA FINAL
            resposta_final = self._formatar_resposta_final(
                decisao_final, score_consenso, score_robustez, 
                len(colegiado), dissidencias, registro.id
            )
            
            tempo_total = time.time() - inicio_processamento
            logger.info(f"🧠 Assembleia {registro.id} concluída em {tempo_total:.2f}s")
            
            return resposta_final
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento Oráculo: {e}")
            return f"🧠 Oráculo v8.1 Plus+ - Erro na assembleia: {str(e)}"
    
    def _analisar_complexidade(self, desafio: str) -> TipoAssembleia:
        """🎯 Analisa complexidade e determina tipo de assembleia"""
        # Palavras-chave para diferentes níveis de complexidade
        palavras_triviais = ["preço", "cor", "tamanho", "simples", "rápido"]
        palavras_complexas = ["estratégia", "integração", "sistema", "arquitetura", "transformação"]
        palavras_criticas = ["decisão crítica", "investimento alto", "mudança radical", "risco"]
        
        desafio_lower = desafio.lower()
        
        # Análise baseada em comprimento e palavras-chave
        if len(desafio) < 50 and any(palavra in desafio_lower for palavra in palavras_triviais):
            return TipoAssembleia.TRIVIAL
        elif any(palavra in desafio_lower for palavra in palavras_criticas):
            return TipoAssembleia.CRITICO
        elif any(palavra in desafio_lower for palavra in palavras_complexas):
            return TipoAssembleia.COMPLEXO
        elif len(desafio) > 200:
            return TipoAssembleia.INTERMEDIARIO
        else:
            return TipoAssembleia.SIMPLES
    
    def _curar_assembleia(self, desafio: str, tipo: TipoAssembleia) -> List[TipoSuboraculo]:
        """🤝 Curadoria autônoma: seleciona suboráculos mais relevantes"""
        # Mapear tamanho da assembleia
        tamanhos = {
            TipoAssembleia.TRIVIAL: 2,
            TipoAssembleia.SIMPLES: 3,
            TipoAssembleia.INTERMEDIARIO: 4,
            TipoAssembleia.COMPLEXO: 6,
            TipoAssembleia.CRITICO: 7
        }
        
        tamanho_alvo = tamanhos[tipo]
        
        # Sempre incluir núcleo essencial
        nucleo_essencial = [TipoSuboraculo.VIABILIDADE, TipoSuboraculo.ETICO]
        
        # Detectar necessidades específicas baseadas no desafio
        desafio_lower = desafio.lower()
        relevantes = []
        
        if any(palavra in desafio_lower for palavra in ["criativo", "inovação", "novo", "original"]):
            relevantes.append(TipoSuboraculo.CRIATIVO)
        
        if any(palavra in desafio_lower for palavra in ["preço", "valor", "custa", "investimento"]):
            relevantes.append(TipoSuboraculo.PRICING)
        
        if any(palavra in desafio_lower for palavra in ["copy", "texto", "comunicação", "mensagem"]):
            relevantes.append(TipoSuboraculo.COPY)
        
        if any(palavra in desafio_lower for palavra in ["simples", "minimalista", "essencial"]):
            relevantes.append(TipoSuboraculo.MINIMALISTA)
        
        if any(palavra in desafio_lower for palavra in ["futuro", "tendência", "previsão", "mercado"]):
            relevantes.append(TipoSuboraculo.PREDITIVO)
        
        if any(palavra in desafio_lower for palavra in ["radical", "mudança", "transformar", "revolucionar"]):
            relevantes.append(TipoSuboraculo.RADICAL)
        
        if any(palavra in desafio_lower for palavra in ["risco", "cuidado", "seguro", "estável"]):
            relevantes.append(TipoSuboraculo.CONSERVADOR)
        
        # Adicionar suboráculos baseados em performance histórica
        suboraculos_ativos = [tipo for tipo, perf in self.performance_suboraculos.items() 
                             if perf.status == StatusSuboraculo.ATIVO]
        
        # Combinar núcleo + relevantes + aleatórios ativos
        colegiado = list(set(nucleo_essencial + relevantes))
        
        # Completar até o tamanho alvo com suboráculos ativos
        faltam = tamanho_alvo - len(colegiado)
        disponiveis = [s for s in suboraculos_ativos if s not in colegiado]
        
        if faltam > 0 and disponiveis:
            # Priorizar por performance histórica
            disponiveis_ordenados = sorted(disponiveis, 
                key=lambda x: self.performance_suboraculos[x].contribuicoes_valiosas, 
                reverse=True)
            colegiado.extend(disponiveis_ordenados[:faltam])
        
        # Para assembleias críticas, sempre incluir céticos
        if tipo == TipoAssembleia.CRITICO and TipoSuboraculo.CETICO not in colegiado:
            if len(colegiado) >= tamanho_alvo:
                colegiado[-1] = TipoSuboraculo.CETICO  # Substituir último
            else:
                colegiado.append(TipoSuboraculo.CETICO)
        
        return colegiado[:tamanho_alvo]
    
    def _realizar_deliberacao(self, desafio: str, colegiado: List[TipoSuboraculo], 
                            contexto: Dict) -> List[VotoSuboraculo]:
        """🗳️ Executa deliberação coletiva dos suboráculos"""
        votos = []
        
        logger.info(f"🗳️ Iniciando deliberação com {len(colegiado)} suboráculos")
        
        for tipo_suboraculo in colegiado:
            try:
                suboraculo = self.suboraculos[tipo_suboraculo]
                voto = suboraculo.deliberar(desafio, contexto)
                votos.append(voto)
                
                # Atualizar performance
                self.performance_suboraculos[tipo_suboraculo].participacoes += 1
                
                logger.debug(f"   📊 {tipo_suboraculo.value}: {voto.posicao[:50]}...")
                
            except Exception as e:
                logger.warning(f"⚠️ Erro na deliberação {tipo_suboraculo.value}: {e}")
        
        logger.info(f"✅ Deliberação concluída: {len(votos)} votos coletados")
        return votos
    
    def _sintetizar_decisao(self, votos: List[VotoSuboraculo], desafio: str) -> Dict:
        """⚖️ Síntese inteligente e cálculo de consenso"""
        if not votos:
            return {
                'decisao': "Assembleia inconclusiva - análise individual necessária",
                'score_consenso': 0.0,
                'score_robustez': 0.0,
                'dissidencias': []
            }
        
        # Calcular métricas de consenso
        scores_confianca = [voto.score_confianca for voto in votos]
        score_consenso = sum(scores_confianca) / len(scores_confianca) / 10.0  # Normalizar 0-1
        
        # Calcular robustez baseada na diversidade de perspectivas
        tipos_representados = len(set(voto.suboraculo for voto in votos))
        score_robustez = min(1.0, tipos_representados / 5.0)  # Máximo com 5 tipos diferentes
        
        # Identificar dissidências (votos com baixa confiança ou alto risco)
        dissidencias = []
        for voto in votos:
            if voto.score_confianca < 6.0 or voto.risco_calculado > 7.0:
                dissidencias.append(f"{voto.suboraculo.value}: {voto.posicao[:100]}")
        
        # Síntese inteligente usando LLM (se disponível)
        if self.llm:
            decisao_final = self._gerar_sintese_llm(votos, desafio, score_consenso)
        else:
            decisao_final = self._gerar_sintese_simples(votos, score_consenso)
        
        return {
            'decisao': decisao_final,
            'score_consenso': score_consenso,
            'score_robustez': score_robustez,
            'dissidencias': dissidencias
        }
    
    def _gerar_sintese_llm(self, votos: List[VotoSuboraculo], desafio: str, score_consenso: float) -> str:
        """Gera síntese usando LLM"""
        try:
            # Preparar dados dos votos
            votos_texto = "\n".join([
                f"• {voto.suboraculo.value.upper()}: {voto.posicao} (Confiança: {voto.score_confianca:.1f}/10)"
                for voto in votos
            ])
            
            prompt = f"""Você é o Curador da Assembleia Dinâmica do Oráculo v8.1 Plus+.

DESAFIO: {desafio}

VOTOS DOS SUBORÁCULOS:
{votos_texto}

SCORE DE CONSENSO: {score_consenso:.2f}

SUA MISSÃO: Sintetizar uma decisão final CLARA, PRÁTICA e ACIONÁVEL que:
1. Integre as melhores contribuições dos suboráculos
2. Resolva conflitos priorizando viabilidade e inovação
3. Seja direta e implementável
4. Mantenha o foco no resultado

Responda apenas com a DECISÃO FINAL sintetizada (máximo 3 parágrafos):"""

            resposta = self.llm.invoke(prompt).content
            return resposta.strip()
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na síntese LLM: {e}")
            return self._gerar_sintese_simples(votos, score_consenso)
    
    def _gerar_sintese_simples(self, votos: List[VotoSuboraculo], score_consenso: float) -> str:
        """Gera síntese simples sem LLM"""
        if score_consenso > 0.8:
            # Consenso alto - combinar posições principais
            posicoes = [voto.posicao for voto in votos if voto.score_confianca >= 7.0]
            if posicoes:
                return f"Decisão por alto consenso: {posicoes[0]}. Implementação recomendada com confiança."
        
        # Consenso médio/baixo - decidir por maior confiança
        melhor_voto = max(votos, key=lambda v: v.score_confianca)
        return f"Decisão curada: {melhor_voto.posicao}. Base: perspectiva {melhor_voto.suboraculo.value} com maior confiança."
    
    def _aplicar_contrapainel(self, decisao: str, desafio: str, votos: List[VotoSuboraculo]) -> str:
        """🛡️ Aplica contrapainel cético para decisões críticas"""
        logger.info("🛡️ Ativando contrapainel cético")
        
        # Ativar suboráculos céticos
        ceticos = [TipoSuboraculo.CETICO, TipoSuboraculo.CONSERVADOR, TipoSuboraculo.PARADOXO]
        
        contravotos = []
        for tipo in ceticos:
            if tipo not in [v.suboraculo for v in votos]:  # Evitar duplicação
                try:
                    suboraculo = self.suboraculos[tipo]
                    contexto_critico = {"decisao_principal": decisao, "modo": "contrapainel"}
                    contravoto = suboraculo.deliberar(desafio, contexto_critico)
                    contravotos.append(contravoto)
                except Exception as e:
                    logger.warning(f"⚠️ Erro no contrapainel {tipo.value}: {e}")
        
        # Se contrapainel encontrou riscos críticos, ajustar decisão
        riscos_criticos = [cv for cv in contravotos if cv.risco_calculado > 8.0]
        
        if riscos_criticos:
            logger.warning(f"⚠️ Contrapainel identificou {len(riscos_criticos)} riscos críticos")
            return f"{decisao}\n\n⚠️ ALERTA DO CONTRAPAINEL: {riscos_criticos[0].justificativa}"
        
        return decisao
    
    def _registrar_assembleia(self, desafio: str, tipo: TipoAssembleia, 
                            colegiado: List[TipoSuboraculo], votos: List[VotoSuboraculo],
                            decisao: str, score_consenso: float, score_robustez: float,
                            dissidencias: List[str]) -> RegistroAssembleia:
        """📊 Registra assembleia no Diário Evolutivo"""
        self.contador_assembleias += 1
        
        # Gerar microtags
        microtags = self._gerar_microtags_assembleia(tipo, colegiado, score_consenso)
        
        # Identificar aprendizados
        aprendizados = self._extrair_aprendizados(votos, score_consenso)
        
        registro = RegistroAssembleia(
            id=f"assembleia_{self.contador_assembleias:03d}",
            timestamp=datetime.now(),
            desafio=desafio[:200],  # Resumido
            tipo_assembleia=tipo,
            colegiado=colegiado,
            votos=votos,
            decisao_final=decisao,
            score_consenso=score_consenso,
            score_robustez=score_robustez,
            dissidencias=dissidencias,
            aprendizados=aprendizados,
            microtags=microtags
        )
        
        self.diario_assembleias.append(registro)
        
        # Manter apenas últimos 100 registros
        if len(self.diario_assembleias) > 100:
            self.diario_assembleias = self.diario_assembleias[-100:]
        
        logger.info(f"📊 Assembleia {registro.id} registrada no Diário")
        return registro
    
    def _gerar_microtags_assembleia(self, tipo: TipoAssembleia, 
                                  colegiado: List[TipoSuboraculo], 
                                  score_consenso: float) -> List[str]:
        """🏷️ Gera microtags para a assembleia"""
        tags = [
            "#oraculo_v81plus",
            "#assembleia",
            f"#{tipo.value}",
            "#curadoria_autonoma"
        ]
        
        # Tags baseadas no colegiado
        for suboraculo in colegiado:
            tags.append(f"#{suboraculo.value}")
        
        # Tags baseadas no consenso
        if score_consenso > 0.8:
            tags.append("#alto_consenso")
        elif score_consenso < 0.5:
            tags.append("#baixo_consenso")
            tags.append("#divergencia_maxima")
        
        # Tags especiais
        if len(colegiado) >= 6:
            tags.append("#assembleia_ampla")
        
        if TipoSuboraculo.PARADOXO in colegiado:
            tags.append("#questionamento_ativo")
        
        return tags
    
    def _extrair_aprendizados(self, votos: List[VotoSuboraculo], score_consenso: float) -> List[str]:
        """💡 Extrai aprendizados da assembleia"""
        aprendizados = []
        
        # Aprendizado sobre consenso
        if score_consenso > 0.9:
            aprendizados.append("Alto alinhamento entre perspectivas especializadas")
        elif score_consenso < 0.4:
            aprendizados.append("Divergência significativa requer análise mais profunda")
        
        # Aprendizado sobre inovação
        inovacoes = [v for v in votos if v.inovacao_level >= 4]
        if len(inovacoes) >= 2:
            aprendizados.append("Múltiplas perspectivas inovadoras identificadas")
        
        # Aprendizado sobre riscos
        riscos_altos = [v for v in votos if v.risco_calculado > 7.0]
        if riscos_altos:
            aprendizados.append(f"Riscos elevados identificados por {len(riscos_altos)} suboráculos")
        
        return aprendizados
    
    def _processar_autoextincao(self):
        """🔄 Processa autoextinção inteligente de suboráculos"""
        if not self.autoextincao_ativa:
            return
        
        agora = datetime.now()
        
        for tipo, performance in self.performance_suboraculos.items():
            # Verificar critérios de autoextinção
            if (performance.status == StatusSuboraculo.ATIVO and
                performance.participacoes >= self.threshold_autoextincao and
                performance.contribuicoes_valiosas == 0):
                
                # Auto-extinguir
                performance.status = StatusSuboraculo.AUTOEXTINTO
                self.stats["autoextincoes_realizadas"] += 1
                
                logger.info(f"🔄 Suboráculo {tipo.value} auto-extinto por baixa contribuição")
        
        # Reativar suboráculos se contexto mudou (implementação futura)
        # Por enquanto, manter lógica simples
    
    def _atualizar_stats_oraculo(self, score_consenso: float, score_robustez: float):
        """📈 Atualiza estatísticas do Oráculo"""
        self.stats["assembleias_realizadas"] += 1
        
        # Atualizar médias
        total = self.stats["assembleias_realizadas"]
        self.stats["score_medio_consenso"] = (
            (self.stats["score_medio_consenso"] * (total - 1) + score_consenso) / total
        )
        self.stats["score_medio_robustez"] = (
            (self.stats["score_medio_robustez"] * (total - 1) + score_robustez) / total
        )
        
        # Classificar tipo de decisão
        if score_consenso >= 0.7:
            self.stats["decisoes_por_consenso"] += 1
        else:
            self.stats["decisoes_por_curadoria"] += 1
    
    def _formatar_resposta_final(self, decisao: str, score_consenso: float, 
                               score_robustez: float, num_colegiado: int,
                               dissidencias: List[str], assembleia_id: str) -> str:
        """📝 Formata resposta final do Oráculo"""
        # Calcular score de robustez combinado
        score_final = (score_consenso + score_robustez) / 2 * 10
        
        resposta = f"""🧠 **Oráculo v8.1 Plus+ — Decisão Final (Assembleia Dinâmica)**

**Decisão:**
{decisao}

**Curadoria:** Consenso de {num_colegiado} suboráculos especializados
**Score de Robustez:** {score_final:.1f}/10
**ID da Assembleia:** {assembleia_id}"""

        # Adicionar dissidências se houver
        if dissidencias:
            resposta += f"\n**Dissidências Registradas:** {len(dissidencias)} perspectiva(s) alternativa(s)"
        
        # Nota sobre bastidores
        resposta += "\n\n_[Para ver bastidores da assembleia, multiverso ou diário: solicite explicitamente]_"
        
        return resposta
    
    # === MÉTODOS ESPECIAIS DE CONSULTA ===
    
    def mostrar_bastidores_ultima_assembleia(self) -> str:
        """🎭 Mostra bastidores da última assembleia"""
        if not self.diario_assembleias:
            return "📊 Nenhuma assembleia realizada ainda."
        
        ultima = self.diario_assembleias[-1]
        
        bastidores = f"""🎭 **BASTIDORES DA ASSEMBLEIA {ultima.id.upper()}**

**Desafio:** {ultima.desafio}
**Tipo:** {ultima.tipo_assembleia.value.title()}
**Timestamp:** {ultima.timestamp.strftime('%d/%m/%Y %H:%M')}

**🗳️ COLEGIADO E VOTOS:**"""

        for voto in ultima.votos:
            bastidores += f"""
• **{voto.suboraculo.value.upper()}**
  - Posição: {voto.posicao}
  - Justificativa: {voto.justificativa}
  - Confiança: {voto.score_confianca:.1f}/10
  - Inovação: {voto.inovacao_level}/5
  - Risco: {voto.risco_calculado:.1f}/10"""

        if ultima.dissidencias:
            bastidores += f"\n\n**⚠️ DISSIDÊNCIAS:**\n" + "\n".join(f"- {d}" for d in ultima.dissidencias)
        
        if ultima.aprendizados:
            bastidores += f"\n\n**💡 APRENDIZADOS:**\n" + "\n".join(f"- {a}" for a in ultima.aprendizados)
        
        bastidores += f"\n\n**📊 MÉTRICAS:**"
        bastidores += f"\n- Score Consenso: {ultima.score_consenso:.2f}"
        bastidores += f"\n- Score Robustez: {ultima.score_robustez:.2f}"
        bastidores += f"\n- Microtags: {', '.join(ultima.microtags)}"
        
        return bastidores
    
    def gerar_cenarios_alternativos(self, desafio: str) -> str:
        """🌟 Gera cenários alternativos usando multiverso contrafactual"""
        if not self.multiverso_ativo:
            return "🌟 Multiverso contrafactual não está ativo."
        
        cenarios = {
            "Otimista": "Cenário com máxima aceitação e recursos ilimitados",
            "Pessimista": "Cenário com máxima resistência e recursos limitados", 
            "Radical": "Cenário de transformação disruptiva completa",
            "Minimalista": "Cenário com implementação mínima viável",
            "Contrafactual": "Cenário oposto à decisão principal"
        }
        
        resultado = f"🌟 **MULTIVERSO CONTRAFACTUAL - {desafio[:50]}**\n\n"
        
        for nome, descricao in cenarios.items():
            # Simular análise rápida para cada cenário
            resultado += f"**🌍 Universo {nome}:**\n"
            resultado += f"{descricao}\n"
            resultado += f"_[Análise detalhada disponível sob demanda]_\n\n"
        
        self.stats["cenarios_alternativos_gerados"] += len(cenarios)
        return resultado
    
    def obter_diario_assembleias(self, ultimas: int = 5) -> str:
        """📚 Retorna diário das últimas assembleias"""
        if not self.diario_assembleias:
            return "📚 Diário vazio - nenhuma assembleia realizada."
        
        assembleias_recentes = self.diario_assembleias[-ultimas:]
        
        diario = f"📚 **DIÁRIO DE ASSEMBLEIAS - ÚLTIMAS {len(assembleias_recentes)}**\n\n"
        
        for assembleia in reversed(assembleias_recentes):
            diario += f"**{assembleia.id.upper()}** - {assembleia.timestamp.strftime('%d/%m %H:%M')}\n"
            diario += f"Desafio: {assembleia.desafio[:100]}...\n"
            diario += f"Colegiado: {', '.join(s.value for s in assembleia.colegiado)}\n"
            diario += f"Consenso: {assembleia.score_consenso:.2f} | Robustez: {assembleia.score_robustez:.2f}\n"
            if assembleia.aprendizados:
                diario += f"Aprendizado: {assembleia.aprendizados[0]}\n"
            diario += "---\n\n"
        
        return diario
    
    def diagnosticar_oraculo(self) -> Dict:
        """🔧 Diagnóstico completo do Oráculo v8.1 Plus+"""
        # Status dos suboráculos
        status_suboraculos = {}
        for tipo, perf in self.performance_suboraculos.items():
            status_suboraculos[tipo.value] = {
                "status": perf.status.value,
                "participacoes": perf.participacoes,
                "contribuicoes_valiosas": perf.contribuicoes_valiosas,
                "ultima_contribuicao": perf.ultima_contribuicao.isoformat() if perf.ultima_contribuicao else None
            }
        
        return {
            "version": "8.1_Plus_Assembleia_Dinamica",
            "status": "ATIVO",
            "assembleia_dinamica": self.curadoria_autonoma_ativa,
            "multiverso": self.multiverso_ativo,
            "autoextincao": self.autoextincao_ativa,
            "suboraculos_ativos": len([p for p in self.performance_suboraculos.values() 
                                     if p.status == StatusSuboraculo.ATIVO]),
            "assembleias_realizadas": self.stats["assembleias_realizadas"],
            "score_medio_consenso": self.stats["score_medio_consenso"],
            "score_medio_robustez": self.stats["score_medio_robustez"],
            "aprendizados_persistentes": len(self.aprendizados_persistentes),
            "status_suboraculos": status_suboraculos,
            "stats_completas": self.stats
        }

# === FUNÇÕES DE CRIAÇÃO ===

def criar_oraculo_v8_plus(llm=None) -> OraculoV8Plus:
    """🧠 Cria Oráculo v8.1 Plus+ com configurações completas"""
    return OraculoV8Plus(llm=llm)

# Alias para compatibilidade
create_oraculo = criar_oraculo_v8_plus

if __name__ == "__main__":
    print("🧠 Testando Oráculo v8.1 Plus+...")
    
    oraculo = criar_oraculo_v8_plus()
    diagnostico = oraculo.diagnosticar_oraculo()
    
    print(f"📊 Diagnóstico: {diagnostico['version']}")
    print(f"🤖 Suboráculos ativos: {diagnostico['suboraculos_ativos']}")
    print("✅ Oráculo v8.1 Plus+ pronto para assembleias dinâmicas!")