"""
SupervisorAI v1.3 - Maestro de Raciocínio do GPT Mestre Autônomo
Classifica tarefas e decide automaticamente o modo de execução ideal
"""

import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)

class ModoExecucao(Enum):
    """Modos de execução disponíveis"""
    DIRETO = "direto"
    INTERMEDIARIO = "intermediario" 
    ANALISE_MODULAR = "analise_modular"
    PROFUNDO = "profundo"
    REATIVO = "reativo"
    EXPLORATORIO = "exploratorio"
    ESPELHADO = "espelhado"
    SHADOW = "shadow"
    METACOGNITIVO = "metacognitivo"

@dataclass
class ClassificacaoTarefa:
    """Resultado da classificação de uma tarefa"""
    complexidade: float  # 0-10
    impacto_estrategico: float  # 0-10
    modo_recomendado: ModoExecucao
    agentes_sugeridos: List[str]
    justificativa: str
    tolerancia_erro: str  # baixa, media, alta
    historico_relevante: bool
    tags_detectadas: List[str]
    tempo_estimado: int  # segundos
    confianca_classificacao: float  # 0-10

class SupervisorAI(BaseAgent):
    """
    SupervisorAI v1.3 - Maestro lógico-adaptativo do sistema GPT Mestre
    
    Funcionalidades:
    - Classifica automaticamente qualquer tarefa recebida
    - Decide o modo de execução ideal (direto até profundo)
    - Ativa agentes complementares conforme necessário
    - Aprende padrões e melhora decisões ao longo do tempo
    - Monitora qualidade e ajusta estratégias
    """
    
    def __init__(self, llm=None):
        super().__init__(
            name="SupervisorAI",
            description="Maestro de raciocínio - classifica tarefas e decide execução"
        )
        
        if llm:
            self.llm = llm
        else:
            self._inicializar_llm()
        
        # Histórico de decisões para aprendizado
        self.historico_decisoes = []
        self.padroes_aprendidos = {}
        
        # Métricas de performance
        self.stats_supervisor = {
            "total_classificacoes": 0,
            "acertos_modo": 0,
            "score_medio_reflexor": 0.0,
            "tempo_medio_classificacao": 0.0,
            "ultima_metacognicao": None
        }
        
        # Cache de padrões por tipo de tarefa
        self.cache_padroes = {}
        
        logger.info("🧠 SupervisorAI v1.3 inicializado - Modo adaptativo ativo")
    
    def _inicializar_llm(self):
        """Inicializa o LLM com configurações padrão"""
        try:
            from langchain_anthropic import ChatAnthropic
            import config
            
            self.llm = ChatAnthropic(
                model=config.CLAUDE_MODEL,
                max_tokens=config.CLAUDE_MAX_TOKENS,
                temperature=0.3,  # Baixa temperature para classificação consistente
                anthropic_api_key=config.ANTHROPIC_API_KEY,
            )
            logger.info("LLM Claude inicializado para SupervisorAI")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar LLM do SupervisorAI: {e}")
            self.llm = None
    
    def classificar_tarefa(self, mensagem: str, contexto: Optional[Dict] = None) -> ClassificacaoTarefa:
        """
        Classifica uma tarefa e decide o modo de execução ideal
        
        Args:
            mensagem: Mensagem/tarefa do usuário
            contexto: Contexto adicional da conversa
            
        Returns:
            ClassificacaoTarefa com modo recomendado e agentes
        """
        inicio = time.time()
        
        try:
            # Análise rápida de padrões conhecidos
            classificacao_cache = self._verificar_cache_padroes(mensagem)
            if classificacao_cache:
                logger.info(f"🚀 Classificação via cache: {classificacao_cache.modo_recomendado.value}")
                return classificacao_cache
            
            # Análise completa
            complexidade = self._calcular_complexidade(mensagem, contexto)
            impacto = self._calcular_impacto_estrategico(mensagem, contexto)
            modo = self._decidir_modo_execucao(complexidade, impacto, mensagem)
            agentes = self._sugerir_agentes(mensagem, modo, contexto)
            
            classificacao = ClassificacaoTarefa(
                complexidade=complexidade,
                impacto_estrategico=impacto,
                modo_recomendado=modo,
                agentes_sugeridos=agentes,
                justificativa=self._gerar_justificativa(complexidade, impacto, modo),
                tolerancia_erro=self._avaliar_tolerancia_erro(impacto),
                historico_relevante=self._verificar_historico_relevante(mensagem),
                tags_detectadas=self._detectar_tags(mensagem),
                tempo_estimado=self._estimar_tempo(modo, len(agentes)),
                confianca_classificacao=self._calcular_confianca(complexidade, impacto)
            )
            
            # Salvar para aprendizado
            self._salvar_decisao(mensagem, classificacao)
            
            # Atualizar estatísticas
            tempo_total = time.time() - inicio
            self._atualizar_stats(tempo_total)
            
            logger.info(f"📊 Tarefa classificada: {modo.value} (C:{complexidade:.1f}, I:{impacto:.1f})")
            
            return classificacao
            
        except Exception as e:
            logger.error(f"Erro na classificação: {e}")
            # Fallback seguro
            return self._classificacao_fallback(mensagem)
    
    def _calcular_complexidade(self, mensagem: str, contexto: Optional[Dict] = None) -> float:
        """Calcula complexidade da tarefa (0-10)"""
        complexidade = 2.0  # Base
        
        # Análise textual
        palavras = len(mensagem.split())
        if palavras > 50:
            complexidade += 1.0
        if palavras > 100:
            complexidade += 1.0
            
        # Palavras-chave de complexidade
        indicadores_alta = [
            'análise', 'compare', 'estratégia', 'decisão', 'avaliar',
            'otimizar', 'calcular', 'simular', 'prever', 'planejar'
        ]
        indicadores_media = [
            'explicar', 'resumir', 'listar', 'sugerir', 'recomendar'
        ]
        
        mensagem_lower = mensagem.lower()
        for indicador in indicadores_alta:
            if indicador in mensagem_lower:
                complexidade += 1.5
                
        for indicador in indicadores_media:
            if indicador in mensagem_lower:
                complexidade += 0.8
        
        # Indicadores de múltiplas etapas
        if any(palavra in mensagem_lower for palavra in ['depois', 'então', 'primeiro', 'segundo']):
            complexidade += 1.0
            
        # Perguntas abertas vs específicas
        if mensagem.endswith('?') and len(palavras) < 10:
            complexidade -= 0.5
            
        return min(10.0, max(1.0, complexidade))
    
    def _calcular_impacto_estrategico(self, mensagem: str, contexto: Optional[Dict] = None) -> float:
        """Calcula impacto estratégico (0-10)"""
        impacto = 3.0  # Base
        
        mensagem_lower = mensagem.lower()
        
        # Palavras de alto impacto
        alto_impacto = [
            'investir', 'comprar', 'vender', 'lançar', 'decisão crítica',
            'estratégia', 'plano', 'orçamento', 'receita', 'lucro',
            'risco', 'oportunidade', 'mercado', 'concorrência'
        ]
        
        medio_impacto = [
            'produto', 'cliente', 'anúncio', 'preço', 'marketing',
            'tendência', 'análise', 'otimizar'
        ]
        
        for palavra in alto_impacto:
            if palavra in mensagem_lower:
                impacto += 2.0
                
        for palavra in medio_impacto:
            if palavra in mensagem_lower:
                impacto += 1.0
        
        # Valores monetários mencionados
        if 'r$' in mensagem_lower or 'reais' in mensagem_lower:
            impacto += 1.5
            
        # URLs ou links (análise de produto)
        if 'http' in mensagem_lower or 'aliexpress' in mensagem_lower:
            impacto += 1.0
            
        return min(10.0, max(1.0, impacto))
    
    def _decidir_modo_execucao(self, complexidade: float, impacto: float, mensagem: str) -> ModoExecucao:
        """Decide o modo de execução baseado em complexidade e impacto"""
        
        # Score combinado (peso maior no impacto)
        score = (complexidade * 0.4) + (impacto * 0.6)
        
        # Casos especiais primeiro
        if 'como você está' in mensagem.lower() or mensagem.lower().startswith('oi'):
            return ModoExecucao.DIRETO
            
        if 'compare' in mensagem.lower() and score > 6:
            return ModoExecucao.ESPELHADO
            
        if 'simule' in mensagem.lower() or 'cenário' in mensagem.lower():
            return ModoExecucao.EXPLORATORIO
            
        # Decisão por score
        if score >= 8.0:
            return ModoExecucao.PROFUNDO
        elif score >= 6.5:
            return ModoExecucao.ANALISE_MODULAR
        elif score >= 4.0:
            return ModoExecucao.INTERMEDIARIO
        else:
            return ModoExecucao.DIRETO
    
    def _sugerir_agentes(self, mensagem: str, modo: ModoExecucao, contexto: Optional[Dict] = None) -> List[str]:
        """Sugere agentes complementares baseado na mensagem e modo"""
        agentes = []
        mensagem_lower = mensagem.lower()
        
        # Sempre incluir Reflexor em modos não-diretos
        if modo != ModoExecucao.DIRETO:
            agentes.append("Reflexor")
        
        # Análise de produto/mercado
        if any(palavra in mensagem_lower for palavra in ['produto', 'aliexpress', 'shopee', 'mercado']):
            agentes.extend(["DeepAgent", "ScoutAI"])
            
        # Preço/financeiro
        if any(palavra in mensagem_lower for palavra in ['preço', 'custo', 'margem', 'lucro', 'r$']):
            agentes.append("AutoPrice")
            
        # Kit/combo
        if any(palavra in mensagem_lower for palavra in ['kit', 'combo', 'conjunto']):
            agentes.append("KitBuilder")
            
        # Copy/anúncio
        if any(palavra in mensagem_lower for palavra in ['anúncio', 'título', 'descrição', 'copy']):
            agentes.append("CopyBooster")
            
        # Decisão estratégica
        if any(palavra in mensagem_lower for palavra in ['decisão', 'estratégia', 'dilema', 'escolher']):
            agentes.append("Oráculo")
            
        # Dúvidas/ambiguidade
        if any(palavra in mensagem_lower for palavra in ['dúvida', 'confuso', 'não entendi']):
            agentes.append("DoubtSolver")
            
        # Modo profundo sempre inclui múltiplos agentes
        if modo == ModoExecucao.PROFUNDO and len(agentes) < 3:
            agentes.extend(["Oráculo", "DeepAgent"])
            
        return list(set(agentes))  # Remove duplicatas
    
    def _gerar_justificativa(self, complexidade: float, impacto: float, modo: ModoExecucao) -> str:
        """Gera justificativa da decisão"""
        score = (complexidade * 0.4) + (impacto * 0.6)
        
        if modo == ModoExecucao.PROFUNDO:
            return f"Alta complexidade ({complexidade:.1f}) e impacto crítico ({impacto:.1f}) exigem análise profunda"
        elif modo == ModoExecucao.ANALISE_MODULAR:
            return f"Complexidade moderada ({complexidade:.1f}) requer análise estruturada"
        elif modo == ModoExecucao.INTERMEDIARIO:
            return f"Tarefa padrão ({score:.1f}) com raciocínio básico"
        else:
            return f"Resposta direta adequada para tarefa simples ({score:.1f})"
    
    def _avaliar_tolerancia_erro(self, impacto: float) -> str:
        """Avalia tolerância a erro baseado no impacto"""
        if impacto >= 8:
            return "baixa"
        elif impacto >= 5:
            return "media"
        else:
            return "alta"
    
    def _verificar_historico_relevante(self, mensagem: str) -> bool:
        """Verifica se há histórico relevante para a tarefa"""
        # Buscar em histórico de decisões similares
        for decisao in self.historico_decisoes[-10:]:  # Últimas 10
            if self._similaridade_mensagens(mensagem, decisao['mensagem']) > 0.7:
                return True
        return False
    
    def _detectar_tags(self, mensagem: str) -> List[str]:
        """Detecta tags relevantes na mensagem"""
        tags = []
        mensagem_lower = mensagem.lower()
        
        categorias = {
            '#PRODUTO': ['produto', 'item', 'artigo'],
            '#FINANCEIRO': ['preço', 'custo', 'lucro', 'margem', 'r$'],
            '#ESTRATEGICO': ['estratégia', 'decisão', 'plano'],
            '#ANALISE': ['analisar', 'avaliar', 'comparar'],
            '#MARKETING': ['anúncio', 'copy', 'marketing'],
            '#URGENTE': ['urgente', 'rápido', 'agora'],
            '#DECISAO_CRITICA': ['crítico', 'importante', 'decisão']
        }
        
        for tag, palavras in categorias.items():
            if any(palavra in mensagem_lower for palavra in palavras):
                tags.append(tag)
                
        return tags
    
    def _estimar_tempo(self, modo: ModoExecucao, num_agentes: int) -> int:
        """Estima tempo de processamento em segundos"""
        tempos_base = {
            ModoExecucao.DIRETO: 5,
            ModoExecucao.INTERMEDIARIO: 15,
            ModoExecucao.ANALISE_MODULAR: 30,
            ModoExecucao.PROFUNDO: 60,
            ModoExecucao.EXPLORATORIO: 45,
            ModoExecucao.ESPELHADO: 90
        }
        
        tempo_base = tempos_base.get(modo, 20)
        tempo_agentes = num_agentes * 10
        
        return tempo_base + tempo_agentes
    
    def _calcular_confianca(self, complexidade: float, impacto: float) -> float:
        """Calcula confiança na classificação"""
        # Maior confiança em extremos claros
        if complexidade <= 2 and impacto <= 2:
            return 9.5  # Claramente simples
        elif complexidade >= 8 and impacto >= 8:
            return 9.0  # Claramente complexo
        elif 3 <= complexidade <= 7 and 3 <= impacto <= 7:
            return 6.5  # Zona cinzenta
        else:
            return 8.0  # Casos intermediários
    
    def _verificar_cache_padroes(self, mensagem: str) -> Optional[ClassificacaoTarefa]:
        """Verifica se existe padrão conhecido em cache"""
        # Implementação simplificada - pode ser expandida
        hash_mensagem = hash(mensagem.lower().strip())
        
        if hash_mensagem in self.cache_padroes:
            padrao = self.cache_padroes[hash_mensagem]
            if (datetime.now() - padrao['timestamp']).days < 7:  # Cache válido por 7 dias
                return padrao['classificacao']
                
        return None
    
    def _salvar_decisao(self, mensagem: str, classificacao: ClassificacaoTarefa):
        """Salva decisão para aprendizado futuro"""
        decisao = {
            'timestamp': datetime.now(),
            'mensagem': mensagem,
            'classificacao': classificacao,
            'hash': hash(mensagem.lower().strip())
        }
        
        self.historico_decisoes.append(decisao)
        
        # Manter apenas últimas 100 decisões
        if len(self.historico_decisoes) > 100:
            self.historico_decisoes = self.historico_decisoes[-100:]
        
        # Atualizar cache se confiança alta
        if classificacao.confianca_classificacao >= 8.0:
            self.cache_padroes[decisao['hash']] = {
                'timestamp': datetime.now(),
                'classificacao': classificacao
            }
    
    def _atualizar_stats(self, tempo_processamento: float):
        """Atualiza estatísticas do SupervisorAI"""
        self.stats_supervisor['total_classificacoes'] += 1
        
        # Média móvel do tempo
        total = self.stats_supervisor['total_classificacoes']
        tempo_anterior = self.stats_supervisor['tempo_medio_classificacao']
        self.stats_supervisor['tempo_medio_classificacao'] = \
            ((tempo_anterior * (total - 1)) + tempo_processamento) / total
    
    def _classificacao_fallback(self, mensagem: str) -> ClassificacaoTarefa:
        """Classificação de fallback em caso de erro"""
        return ClassificacaoTarefa(
            complexidade=5.0,
            impacto_estrategico=5.0,
            modo_recomendado=ModoExecucao.INTERMEDIARIO,
            agentes_sugeridos=["Reflexor"],
            justificativa="Classificação de segurança devido a erro no processamento",
            tolerancia_erro="media",
            historico_relevante=False,
            tags_detectadas=["#FALLBACK"],
            tempo_estimado=30,
            confianca_classificacao=3.0
        )
    
    def _similaridade_mensagens(self, msg1: str, msg2: str) -> float:
        """Calcula similaridade simples entre mensagens"""
        # Implementação básica - pode ser melhorada
        palavras1 = set(msg1.lower().split())
        palavras2 = set(msg2.lower().split())
        
        if not palavras1 or not palavras2:
            return 0.0
            
        intersecao = palavras1.intersection(palavras2)
        uniao = palavras1.union(palavras2)
        
        return len(intersecao) / len(uniao)
    
    def modo_metacognitivo(self) -> Dict[str, Any]:
        """Executa autoavaliação das decisões passadas"""
        logger.info("🔍 Executando modo metacognitivo...")
        
        if not self.historico_decisoes:
            return {"status": "Sem histórico suficiente para análise"}
        
        # Análise das últimas decisões
        ultimas_30 = self.historico_decisoes[-30:]
        
        # Distribuição de modos
        distribuicao_modos = {}
        for decisao in ultimas_30:
            modo = decisao['classificacao'].modo_recomendado.value
            distribuicao_modos[modo] = distribuicao_modos.get(modo, 0) + 1
        
        # Confiança média
        confianca_media = sum(d['classificacao'].confianca_classificacao for d in ultimas_30) / len(ultimas_30)
        
        relatorio = {
            "periodo_analisado": f"Últimas {len(ultimas_30)} decisões",
            "distribuicao_modos": distribuicao_modos,
            "confianca_media": round(confianca_media, 2),
            "total_classificacoes": self.stats_supervisor['total_classificacoes'],
            "tempo_medio": round(self.stats_supervisor['tempo_medio_classificacao'], 3),
            "recomendacoes": self._gerar_recomendacoes_metacognitivas(distribuicao_modos, confianca_media)
        }
        
        self.stats_supervisor['ultima_metacognicao'] = datetime.now()
        
        return relatorio
    
    def _gerar_recomendacoes_metacognitivas(self, distribuicao: Dict, confianca: float) -> List[str]:
        """Gera recomendações baseadas na autoavaliação"""
        recomendacoes = []
        
        if confianca < 7.0:
            recomendacoes.append("Ajustar critérios de classificação - confiança baixa")
        
        total_decisoes = sum(distribuicao.values())
        if distribuicao.get('direto', 0) / total_decisoes > 0.6:
            recomendacoes.append("Muitas tarefas classificadas como diretas - revisar sensibilidade")
            
        if distribuicao.get('profundo', 0) / total_decisoes > 0.3:
            recomendacoes.append("Muitas tarefas profundas - otimizar para reduzir custos")
        
        if not recomendacoes:
            recomendacoes.append("Performance adequada - manter padrões atuais")
            
        return recomendacoes
    
    def obter_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas detalhadas do SupervisorAI"""
        return {
            "stats_gerais": self.stats_supervisor,
            "cache_size": len(self.cache_padroes),
            "historico_size": len(self.historico_decisoes),
            "ultima_metacognicao": self.stats_supervisor.get('ultima_metacognicao'),
            "agente_info": self.get_info()
        }

# Função de criação para uso no sistema
def criar_supervisor_ai(llm=None) -> SupervisorAI:
    """Cria instância do SupervisorAI"""
    return SupervisorAI(llm=llm)

# Teste básico
if __name__ == "__main__":
    print("🧪 Testando SupervisorAI...")
    
    supervisor = criar_supervisor_ai()
    
    # Testes de classificação
    testes = [
        "Oi Carlos, como você está?",
        "Analise este produto do AliExpress para revenda",
        "Preciso tomar uma decisão estratégica sobre investir R$ 10.000 neste nicho",
        "Explique como funciona o dropshipping"
    ]
    
    for teste in testes:
        print(f"\n📝 Teste: {teste}")
        classificacao = supervisor.classificar_tarefa(teste)
        print(f"🎯 Modo: {classificacao.modo_recomendado.value}")
        print(f"📊 Complexidade: {classificacao.complexidade:.1f}, Impacto: {classificacao.impacto_estrategico:.1f}")
        print(f"🤖 Agentes: {classificacao.agentes_sugeridos}")
    
    print("\n✅ SupervisorAI testado com sucesso!")
