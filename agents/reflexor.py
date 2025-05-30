 
"""
Agente Reflexor v1.5+ - Sistema de Auditoria Avançado
Sistema de análise e melhoria contínua de respostas
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)

class ModoReflexor(Enum):
    """Modos de operação do Reflexor"""
    PONTUAL = "pontual"
    CONTINUO = "continuo"
    META_AUDITORIA = "meta_auditoria"
    TUTOR = "tutor"
    RED_FLAG = "red_flag"

@dataclass
class ReflexaoAnalise:
    """Estrutura de análise do Reflexor"""
    score_qualidade: float  # 1-10
    pontos_positivos: List[str]
    pontos_melhorar: List[str] 
    sugestoes_melhoria: List[str]
    precisa_revisao: bool
    categoria_problema: Optional[str] = None
    red_flags_detectados: List[str] = None
    nota_confianca: float = 0.0
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()
        if self.red_flags_detectados is None:
            self.red_flags_detectados = []

class AgenteReflexor(BaseAgent):
    """
    Reflexor v1.5+ - Sistema de Auditoria Avançado
    
    Funcionalidades:
    - Análise de qualidade de respostas
    - Detecção de red flags
    - Sugestões de melhoria
    - Múltiplos modos de operação
    - Sistema de aprendizado contínuo
    """
    
    def __init__(self, llm=None, modo_inicial: ModoReflexor = ModoReflexor.PONTUAL):
        super().__init__(
            name="Reflexor",
            description="Sistema de auditoria e melhoria contínua"
        )
        
        # Configuração do LLM
        if llm is None:
            self._inicializar_llm()
        else:
            self.llm = llm
        
        # Configurações do Reflexor
        self.modo_atual = modo_inicial
        self.threshold_red_flag = 3
        self.auto_aprendizado = True
        
        # Histórico de análises
        self.historico_analises = []
        
        # Padrões identificados
        self.padroes_problemas = {}
        self.padroes_sucessos = {}
        
        # Red flags ativas
        self.red_flags_ativas = []
        
        logger.info(f"🔍 Reflexor v1.5+ inicializado - Modo: {self.modo_atual.value}")
    
    def _inicializar_llm(self):
        """Inicializa o LLM com configurações padrão"""
        try:
            from langchain_anthropic import ChatAnthropic
            import config
            
            if not config.ANTHROPIC_API_KEY:
                logger.warning("ANTHROPIC_API_KEY não configurada - Reflexor funcionará em modo limitado")
                self.llm = None
                return
            
            self.llm = ChatAnthropic(
                model=config.CLAUDE_MODEL,
                max_tokens=config.CLAUDE_MAX_TOKENS,
                temperature=config.CLAUDE_TEMPERATURE,
                anthropic_api_key=config.ANTHROPIC_API_KEY,
            )
            logger.info("LLM Claude inicializado para Reflexor")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar LLM do Reflexor: {e}")
            self.llm = None
    
    def analisar_resposta(self, pergunta: str, resposta: str, contexto: Dict = None) -> ReflexaoAnalise:
        """
        Analisa uma resposta e gera feedback detalhado
        """
        logger.info("🔍 Iniciando análise de resposta...")
        
        try:
            if self.llm:
                return self._analisar_com_llm(pergunta, resposta, contexto)
            else:
                return self._analisar_heuristica(pergunta, resposta, contexto)
                
        except Exception as e:
            logger.error(f"❌ Erro na análise: {str(e)}")
            return self._criar_analise_fallback(pergunta, resposta)
    
    def _analisar_com_llm(self, pergunta: str, resposta: str, contexto: Dict = None) -> ReflexaoAnalise:
        """Análise usando LLM"""
        prompt = self._criar_prompt_analise(pergunta, resposta, contexto)
        
        try:
            resposta_llm = self.llm.invoke(prompt)
            conteudo = resposta_llm.content if hasattr(resposta_llm, 'content') else str(resposta_llm)
            
            return self._processar_analise_llm(conteudo, pergunta, resposta)
            
        except Exception as e:
            logger.error(f"Erro na análise LLM: {e}")
            return self._analisar_heuristica(pergunta, resposta, contexto)
    
    def _analisar_heuristica(self, pergunta: str, resposta: str, contexto: Dict = None) -> ReflexaoAnalise:
        """Análise usando heurísticas simples"""
        score = 6  # Score padrão
        pontos_positivos = ["Resposta fornecida"]
        pontos_melhorar = []
        sugestoes = []
        precisa_revisao = False
        categoria_problema = None
        
        # Heurísticas básicas
        if len(resposta) < 20:
            score -= 2
            pontos_melhorar.append("Resposta muito curta")
            sugestoes.append("Expandir com mais detalhes")
            categoria_problema = "completude"
            precisa_revisao = True
        
        if len(resposta) > 1000:
            score -= 1
            pontos_melhorar.append("Resposta muito longa")
            sugestoes.append("Ser mais conciso")
        
        if not any(char in resposta for char in '.,!?'):
            score -= 1
            pontos_melhorar.append("Falta de pontuação")
            sugestoes.append("Melhorar estrutura da frase")
        
        if pergunta.lower() in resposta.lower():
            pontos_positivos.append("Resposta relacionada à pergunta")
            score += 1
        
        if score < 5:
            precisa_revisao = True
        
        return ReflexaoAnalise(
            score_qualidade=max(1, min(10, score)),
            pontos_positivos=pontos_positivos,
            pontos_melhorar=pontos_melhorar,
            sugestoes_melhoria=sugestoes,
            precisa_revisao=precisa_revisao,
            categoria_problema=categoria_problema,
            nota_confianca=float(score),
            timestamp=datetime.now().isoformat()
        )
    
    def _criar_prompt_analise(self, pergunta: str, resposta: str, contexto: Dict = None) -> str:
        """Cria prompt para análise crítica"""
        return f"""Você é o Reflexor, um auditor inteligente especializado em análise crítica.

TAREFA: Analise a resposta abaixo e forneça feedback estruturado.

PERGUNTA: {pergunta}

RESPOSTA: {resposta}

CRITÉRIOS: Relevância, Completude, Clareza, Precisão, Utilidade, Estrutura, Tom

FORMATO (JSON):
{{
    "score_qualidade": 8,
    "pontos_positivos": ["aspecto1", "aspecto2"],
    "pontos_melhorar": ["problema1", "problema2"],
    "sugestoes_melhoria": ["sugestao1", "sugestao2"],
    "precisa_revisao": false,
    "categoria_problema": null,
    "justificativa": "explicação do score"
}}

Seja crítico mas construtivo. Score 1-10."""
    
    def _processar_analise_llm(self, resposta_llm: str, pergunta: str, resposta: str) -> ReflexaoAnalise:
        """Processa resposta do LLM"""
        try:
            # Extrair JSON
            inicio = resposta_llm.find('{')
            fim = resposta_llm.rfind('}') + 1
            
            if inicio != -1 and fim > inicio:
                json_str = resposta_llm[inicio:fim]
                dados = json.loads(json_str)
                
                return ReflexaoAnalise(
                    score_qualidade=float(dados.get("score_qualidade", 5)),
                    pontos_positivos=dados.get("pontos_positivos", []),
                    pontos_melhorar=dados.get("pontos_melhorar", []),
                    sugestoes_melhoria=dados.get("sugestoes_melhoria", []),
                    precisa_revisao=dados.get("precisa_revisao", False),
                    categoria_problema=dados.get("categoria_problema"),
                    nota_confianca=float(dados.get("score_qualidade", 5)),
                    timestamp=datetime.now().isoformat()
                )
            else:
                return self._analisar_heuristica(pergunta, resposta)
                
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            logger.warning(f"Erro ao processar JSON do LLM: {e}")
            return self._analisar_heuristica(pergunta, resposta)
    
    def _criar_analise_fallback(self, pergunta: str, resposta: str) -> ReflexaoAnalise:
        """Cria análise de fallback em caso de erro"""
        return ReflexaoAnalise(
            score_qualidade=5.0,
            pontos_positivos=["Resposta fornecida"],
            pontos_melhorar=["Erro na análise automática"],
            sugestoes_melhoria=["Revisar sistema de análise"],
            precisa_revisao=True,
            categoria_problema="sistema",
            nota_confianca=3.0,
            timestamp=datetime.now().isoformat()
        )
    
    def melhorar_resposta(self, pergunta: str, resposta_original: str) -> Optional[str]:
        """Tenta melhorar resposta com base na análise"""
        if not self.llm:
            return None
            
        try:
            prompt = f"""Melhore a resposta abaixo:

PERGUNTA: {pergunta}
RESPOSTA ORIGINAL: {resposta_original}

TAREFA: Reescreva de forma mais clara, completa e útil.

RESPOSTA MELHORADA:"""
            
            resposta_llm = self.llm.invoke(prompt)
            return resposta_llm.content if hasattr(resposta_llm, 'content') else str(resposta_llm)
            
        except Exception as e:
            logger.error(f"Erro ao melhorar resposta: {e}")
            return None
    
    def obter_relatorio_qualidade(self) -> Dict:
        """Gera relatório de qualidade"""
        if not self.historico_analises:
            return {
                "status": "Nenhuma análise realizada",
                "total_analises": 0
            }
        
        scores = [a.score_qualidade for a in self.historico_analises]
        score_medio = sum(scores) / len(scores)
        
        revisoes = sum(1 for a in self.historico_analises if a.precisa_revisao)
        taxa_revisao = (revisoes / len(self.historico_analises)) * 100
        
        return {
            "resumo": {
                "total_analises": len(self.historico_analises),
                "score_medio": round(score_medio, 2),
                "taxa_revisao": round(taxa_revisao, 2)
            },
            "qualidade": {
                "excelente": sum(1 for s in scores if s >= 9),
                "boa": sum(1 for s in scores if 7 <= s < 9), 
                "regular": sum(1 for s in scores if 5 <= s < 7),
                "ruim": sum(1 for s in scores if s < 5)
            },
            "recomendacoes": self._gerar_recomendacoes(score_medio, taxa_revisao)
        }
    
    def _gerar_recomendacoes(self, score_medio: float, taxa_revisao: float) -> List[str]:
        """Gera recomendações baseadas nas métricas"""
        recomendacoes = []
        
        if score_medio < 6:
            recomendacoes.append("Score médio baixo - Revisar qualidade das respostas")
        
        if taxa_revisao > 50:
            recomendacoes.append("Alta taxa de revisão - Otimizar respostas iniciais")
        
        if score_medio >= 8 and taxa_revisao < 30:
            recomendacoes.append("Sistema funcionando bem - Manter padrão")
        
        return recomendacoes

# Funções auxiliares
def criar_reflexor_gpt_mestre(llm=None) -> AgenteReflexor:
    """Cria instância do Reflexor para GPT Mestre"""
    return AgenteReflexor(llm=llm)

def AgenteReflexor_criar(llm=None) -> AgenteReflexor:
    """Alias para compatibilidade"""
    return AgenteReflexor(llm=llm)

# Teste básico
if __name__ == "__main__":
    print("🧪 Testando Reflexor...")
    reflexor = criar_reflexor_gpt_mestre()
    
    # Teste simples
    analise = reflexor.analisar_resposta(
        "Como está o tempo?",
        "O tempo está bom hoje."
    )
    
    print(f"Score: {analise.score_qualidade}/10")
    print(f"Pontos positivos: {analise.pontos_positivos}")
    print("✅ Reflexor OK!")