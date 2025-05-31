"""
Reflexor v2.0 - Migrado para BaseAgentV2
Sistema de Auditoria Avançado com Robustez Total
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

from agents.base_agent_v2 import BaseAgentV2

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

class ReflexorV2(BaseAgentV2):
    """
    Reflexor v2.0 - Sistema de Auditoria Avançado com BaseAgentV2
    
    Mantém todas as funcionalidades originais:
    - Análise de qualidade de respostas
    - Detecção de red flags
    - Sugestões de melhoria
    - Múltiplos modos de operação
    - Sistema de aprendizado contínuo
    - ✅ Agora com robustez total do BaseAgentV2
    """
    
    def __init__(self, modo_inicial: ModoReflexor = ModoReflexor.PONTUAL, **kwargs):
        # Configuração robusta para Reflexor
        config_robusta = {
            "rate_limit_per_minute": 40,  # Reflexor pode precisar de mais chamadas
            "burst_allowance": 8,
            "failure_threshold": 4,
            "recovery_timeout": 45,
            "cache_enabled": True,
            "cache_ttl_seconds": 300,  # 5 minutos
            "persistent_memory": True,
            "max_retry_attempts": 3
        }
        
        # Merge com config fornecida
        if 'config' in kwargs:
            config_robusta.update(kwargs['config'])
        kwargs['config'] = config_robusta
        
        super().__init__(
            name="Reflexor",
            description="Sistema de auditoria e melhoria contínua v2.0",
            **kwargs
        )
        
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
        
        logger.info(f"🔍 Reflexor v2.0 (BaseAgentV2) inicializado - Modo: {self.modo_atual.value}")
    
    def _processar_interno(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        Processamento interno - análise de qualidade
        """
        # Extrair pergunta e resposta do contexto ou mensagem
        pergunta = contexto.get('pergunta', '') if contexto else ''
        resposta = contexto.get('resposta', mensagem) if contexto else mensagem
        
        if not pergunta and ':' in mensagem:
            # Tentar extrair pergunta e resposta da mensagem
            partes = mensagem.split(':', 1)
            if len(partes) == 2:
                pergunta = partes[0].strip()
                resposta = partes[1].strip()
        
        # Realizar análise
        analise = self.analisar_resposta(pergunta, resposta, contexto)
        
        # Formatar resposta
        resposta_formatada = f"""🔍 **Análise do Reflexor v2.0**

**Score de Qualidade:** {analise.score_qualidade:.1f}/10
**Confiança na Análise:** {analise.nota_confianca:.1f}/10
**Precisa Revisão:** {'⚠️ SIM' if analise.precisa_revisao else '✅ NÃO'}

**✅ Pontos Positivos:**
{self._formatar_lista(analise.pontos_positivos)}

**📋 Pontos a Melhorar:**
{self._formatar_lista(analise.pontos_melhorar)}

**💡 Sugestões de Melhoria:**
{self._formatar_lista(analise.sugestoes_melhoria)}
"""
        
        if analise.categoria_problema:
            resposta_formatada += f"\n**🏷️ Categoria do Problema:** {analise.categoria_problema}"
        
        if analise.red_flags_detectados:
            resposta_formatada += f"\n\n**🚨 Red Flags Detectados:**\n{self._formatar_lista(analise.red_flags_detectados)}"
        
        # Se modo contínuo, adicionar sugestão de melhoria
        if self.modo_atual == ModoReflexor.CONTINUO and analise.precisa_revisao:
            melhoria = self.melhorar_resposta(pergunta, resposta)
            if melhoria:
                resposta_formatada += f"\n\n**📝 Versão Melhorada Sugerida:**\n{melhoria}"
        
        return resposta_formatada
    
    def analisar_resposta(self, pergunta: str, resposta: str, contexto: Dict = None) -> ReflexaoAnalise:
        """
        Analisa uma resposta e gera feedback detalhado
        """
        logger.info("🔍 Iniciando análise de resposta...")
        
        try:
            if self.llm_available and self.llm:
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
            
            analise = self._processar_analise_llm(conteudo, pergunta, resposta)
            
            # Adicionar ao histórico
            self.historico_analises.append(analise)
            
            # Aprendizado contínuo
            if self.auto_aprendizado:
                self._aprender_com_analise(analise, pergunta, resposta)
            
            return analise
            
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
        red_flags = []
        
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
        
        # Verificar red flags
        if any(palavra in resposta.lower() for palavra in ['erro', 'falha', 'problema']):
            red_flags.append("Possível indicação de problema não resolvido")
        
        if score < 5:
            precisa_revisao = True
        
        analise = ReflexaoAnalise(
            score_qualidade=max(1, min(10, score)),
            pontos_positivos=pontos_positivos,
            pontos_melhorar=pontos_melhorar,
            sugestoes_melhoria=sugestoes,
            precisa_revisao=precisa_revisao,
            categoria_problema=categoria_problema,
            red_flags_detectados=red_flags,
            nota_confianca=float(score),
            timestamp=datetime.now().isoformat()
        )
        
        # Adicionar ao histórico
        self.historico_analises.append(analise)
        
        return analise
    
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
    "red_flags_detectados": [],
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
                    red_flags_detectados=dados.get("red_flags_detectados", []),
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
        if not self.llm_available or not self.llm:
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
    
    def _formatar_lista(self, items: List[str]) -> str:
        """Formata lista para exibição"""
        if not items:
            return "- Nenhum item"
        return '\n'.join(f"- {item}" for item in items)
    
    def _aprender_com_analise(self, analise: ReflexaoAnalise, pergunta: str, resposta: str):
        """Sistema de aprendizado contínuo"""
        # Identificar padrões de problemas
        if analise.categoria_problema:
            if analise.categoria_problema not in self.padroes_problemas:
                self.padroes_problemas[analise.categoria_problema] = []
            self.padroes_problemas[analise.categoria_problema].append({
                'score': analise.score_qualidade,
                'timestamp': analise.timestamp
            })
        
        # Identificar padrões de sucesso
        if analise.score_qualidade >= 8:
            chave_sucesso = f"score_{int(analise.score_qualidade)}"
            if chave_sucesso not in self.padroes_sucessos:
                self.padroes_sucessos[chave_sucesso] = []
            self.padroes_sucessos[chave_sucesso].append({
                'pontos_positivos': analise.pontos_positivos,
                'timestamp': analise.timestamp
            })
    
    def obter_relatorio_qualidade(self) -> Dict:
        """Gera relatório de qualidade avançado"""
        if not self.historico_analises:
            return {
                "status": "Nenhuma análise realizada",
                "total_analises": 0
            }
        
        scores = [a.score_qualidade for a in self.historico_analises]
        score_medio = sum(scores) / len(scores)
        
        revisoes = sum(1 for a in self.historico_analises if a.precisa_revisao)
        taxa_revisao = (revisoes / len(self.historico_analises)) * 100
        
        # Análise de red flags
        total_red_flags = sum(len(a.red_flags_detectados) for a in self.historico_analises)
        
        return {
            "resumo": {
                "total_analises": len(self.historico_analises),
                "score_medio": round(score_medio, 2),
                "taxa_revisao": round(taxa_revisao, 2),
                "total_red_flags": total_red_flags
            },
            "qualidade": {
                "excelente": sum(1 for s in scores if s >= 9),
                "boa": sum(1 for s in scores if 7 <= s < 9), 
                "regular": sum(1 for s in scores if 5 <= s < 7),
                "ruim": sum(1 for s in scores if s < 5)
            },
            "padroes": {
                "problemas_frequentes": list(self.padroes_problemas.keys()),
                "categorias_sucesso": list(self.padroes_sucessos.keys())
            },
            "recomendacoes": self._gerar_recomendacoes(score_medio, taxa_revisao, total_red_flags),
            "health_status": self.get_health_status()  # Incluir status do BaseAgentV2
        }
    
    def _gerar_recomendacoes(self, score_medio: float, taxa_revisao: float, total_red_flags: int) -> List[str]:
        """Gera recomendações baseadas nas métricas"""
        recomendacoes = []
        
        if score_medio < 6:
            recomendacoes.append("Score médio baixo - Revisar qualidade das respostas")
        
        if taxa_revisao > 50:
            recomendacoes.append("Alta taxa de revisão - Otimizar respostas iniciais")
        
        if total_red_flags > len(self.historico_analises) * 0.3:
            recomendacoes.append("Muitos red flags - Investigar problemas recorrentes")
        
        if score_medio >= 8 and taxa_revisao < 30:
            recomendacoes.append("Sistema funcionando bem - Manter padrão")
        
        return recomendacoes
    
    def definir_modo(self, novo_modo: ModoReflexor):
        """Define novo modo de operação"""
        self.modo_atual = novo_modo
        logger.info(f"🔄 Reflexor mudou para modo: {novo_modo.value}")
    
    def verificar_red_flags(self, limite: int = 3) -> List[str]:
        """Verifica red flags acumulados"""
        red_flags_recentes = []
        
        for analise in self.historico_analises[-10:]:  # Últimas 10 análises
            red_flags_recentes.extend(analise.red_flags_detectados)
        
        # Contar frequência
        frequencia = {}
        for flag in red_flags_recentes:
            frequencia[flag] = frequencia.get(flag, 0) + 1
        
        # Retornar flags que aparecem mais que o limite
        return [flag for flag, count in frequencia.items() if count >= limite]


# Funções de criação
def criar_reflexor_v2(**kwargs) -> ReflexorV2:
    """Cria instância do Reflexor v2.0 com BaseAgentV2"""
    return ReflexorV2(**kwargs)

def criar_reflexor_gpt_mestre_v2(**kwargs) -> ReflexorV2:
    """Alias para compatibilidade"""
    return ReflexorV2(**kwargs)

# Aliases adicionais
create_reflexor_v2 = criar_reflexor_v2
create_reflexor = criar_reflexor_v2