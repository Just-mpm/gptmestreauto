"""
Sistema de Otimização de Agentes - ETAPA 4
Matriz de Decisão, Heurísticas de Complexidade e Wake Up Strategy
Implementação seguindo especificações Gemini AI
"""

import re
import time
from typing import Dict, List, Tuple, Set, Optional, Any
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta
import threading
import json
from pathlib import Path

# Logger
try:
    from utils.logger import get_logger
except ImportError:
    class SimpleLogger:
        def __init__(self, name): self.name = name
        def info(self, msg): print(f"[INFO] {msg}")
        def warning(self, msg): print(f"[WARNING] {msg}")
        def error(self, msg): print(f"[ERROR] {msg}")
        def debug(self, msg): print(f"[DEBUG] {msg}")
    def get_logger(name): return SimpleLogger(name)

logger = get_logger(__name__)


class ComplexityLevel(Enum):
    """Níveis de complexidade de mensagens"""
    TRIVIAL = "trivial"          # Respostas pré-definidas, sem LLM
    SIMPLE = "simple"            # Carlos apenas, prompt básico  
    MODERATE = "moderate"        # Carlos + 1-2 agentes específicos
    COMPLEX = "complex"          # Multiple agentes, coordenação
    CRITICAL = "critical"        # Oráculo + assembleia completa


class TaskType(Enum):
    """Tipos de tarefas identificadas"""
    GREETING = "greeting"                    # Saudações básicas
    SYSTEM_COMMAND = "system_command"        # Comandos /status, /help
    FACTUAL_QUERY = "factual_query"         # Perguntas de fato
    RESEARCH = "research"                    # Pesquisa e análise
    CONTENT_CREATION = "content_creation"    # Criação de conteúdo
    STRATEGY_PLANNING = "strategy_planning"  # Planejamento estratégico
    EMOTIONAL_SUPPORT = "emotional_support" # Suporte psicológico
    DECISION_MAKING = "decision_making"      # Decisões críticas
    SYSTEM_OPTIMIZATION = "system_optimization" # Otimização interna
    CREATIVE_EXPLORATION = "creative_exploration" # Inovação/exploração


@dataclass
class AgentActivationPlan:
    """Plano de ativação de agentes para uma tarefa"""
    primary_agents: List[str]      # Agentes principais
    secondary_agents: List[str]    # Agentes de apoio
    validation_agents: List[str]   # Agentes de validação
    wake_up_order: List[str]       # Ordem de ativação
    max_timeout: int               # Timeout máximo em segundos
    expected_tokens: int           # Tokens estimados
    bypass_llm: bool = False       # Se pode pular chamada LLM


@dataclass
class MessageAnalysis:
    """Resultado da análise de uma mensagem"""
    complexity: ComplexityLevel
    task_type: TaskType
    keywords: List[str]
    question_count: int
    word_count: int
    emotional_indicators: List[str]
    activation_plan: AgentActivationPlan
    confidence: float              # Confiança na classificação (0-1)


class AgentOptimizer:
    """
    Sistema Central de Otimização de Agentes
    Implementa Matriz de Decisão e Heurísticas do Gemini
    """
    
    def __init__(self):
        self.lock = threading.Lock()
        
        # Palavras-chave para detecção de complexidade (Gemini specs)
        self.complexity_keywords = {
            ComplexityLevel.CRITICAL: {
                "analise profunda", "estratégia completa", "plano de negócios", 
                "viabilidade", "cenários", "otimizar sistema", "meta-análise", 
                "dilema", "crítico", "inovação", "transformação", "arquitetura",
                "decisão crítica", "investir", "melhor opção", "complexo"
            },
            ComplexityLevel.COMPLEX: {
                "explicar detalhadamente", "comparar", "sugerir opções", 
                "pesquisar", "melhorar", "criar", "planejar", "analisar",
                "estratégia", "mercado", "produto", "planejamento"
            },
            ComplexityLevel.MODERATE: {
                "o que é", "me explique", "resumo", "lista", "exemplo", 
                "como fazer", "definir", "mostrar", "ensinar"
            },
            ComplexityLevel.SIMPLE: {
                "oi", "olá", "tudo bem", "como vai", "bom dia", "boa tarde",
                "obrigado", "tchau", "até logo"
            }
        }
        
        # Indicadores emocionais (Gemini specs)
        self.emotional_indicators = {
            "me sinto", "estou", "ansiedade", "problema pessoal", 
            "preciso de ajuda emocional", "triste", "feliz", "preocupado",
            "estressado", "confuso", "perdido", "desesperado"
        }
        
        # Comandos do sistema
        self.system_commands = {
            "/status", "/help", "/agents", "/reset", "/resumo", "/alertas",
            "/agentes", "/cache", "/config", "/debug"
        }
        
        # Matriz de Decisão [Tipo de Pergunta] x [Agentes Necessários]
        self.decision_matrix = self._build_decision_matrix()
        
        # Estatísticas de otimização
        self.stats = {
            "total_analyses": 0,
            "llm_bypassed": 0,
            "tokens_saved": 0,
            "avg_agents_activated": 0,
            "cache_hits": 0
        }
        
        logger.info("🚀 AgentOptimizer inicializado com Matriz de Decisão Gemini")
    
    def _build_decision_matrix(self) -> Dict[TaskType, AgentActivationPlan]:
        """
        Constrói a Matriz de Decisão seguindo especificações Gemini
        [Tipo de Pergunta] x [Agentes Necessários]
        """
        matrix = {
            # Básico/Saudação - Consumo ZERO de cota
            TaskType.GREETING: AgentActivationPlan(
                primary_agents=["carlos"],
                secondary_agents=[],
                validation_agents=[],
                wake_up_order=["carlos"],
                max_timeout=5,
                expected_tokens=0,
                bypass_llm=True
            ),
            
            # Comandos do Sistema - Consumo ZERO de cota  
            TaskType.SYSTEM_COMMAND: AgentActivationPlan(
                primary_agents=["carlos"],
                secondary_agents=[],
                validation_agents=[],
                wake_up_order=["carlos"],
                max_timeout=10,
                expected_tokens=0,
                bypass_llm=True
            ),
            
            # Informação Simples/Fato - Cache primeiro, LLM mínimo
            TaskType.FACTUAL_QUERY: AgentActivationPlan(
                primary_agents=["carlos"],
                secondary_agents=["deepagent"],
                validation_agents=[],
                wake_up_order=["carlos", "deepagent"],
                max_timeout=15,
                expected_tokens=100,
                bypass_llm=False
            ),
            
            # Análise de Produto/Mercado - Fluxo coordenado
            TaskType.RESEARCH: AgentActivationPlan(
                primary_agents=["supervisor", "deepagent", "scout"],
                secondary_agents=["reflexor"],
                validation_agents=["reflexor"],
                wake_up_order=["supervisor", "deepagent", "scout", "reflexor"],
                max_timeout=45,
                expected_tokens=800,
                bypass_llm=False
            ),
            
            # Criação/Otimização de Conteúdo
            TaskType.CONTENT_CREATION: AgentActivationPlan(
                primary_agents=["promptcrafter"],
                secondary_agents=["reflexor"],
                validation_agents=["reflexor"],
                wake_up_order=["promptcrafter", "reflexor"],
                max_timeout=30,
                expected_tokens=400,
                bypass_llm=False
            ),
            
            # Planejamento/Estratégia
            TaskType.STRATEGY_PLANNING: AgentActivationPlan(
                primary_agents=["taskbreaker", "automaster"],
                secondary_agents=["oraculo", "reflexor"],
                validation_agents=["oraculo", "reflexor"],
                wake_up_order=["taskbreaker", "automaster", "oraculo", "reflexor"],
                max_timeout=60,
                expected_tokens=1200,
                bypass_llm=False
            ),
            
            # Suporte Emocional/Psicológico - Rota direta
            TaskType.EMOTIONAL_SUPPORT: AgentActivationPlan(
                primary_agents=["psymind"],
                secondary_agents=[],
                validation_agents=[],
                wake_up_order=["psymind"],
                max_timeout=25,
                expected_tokens=300,
                bypass_llm=False
            ),
            
            # Decisão Crítica/Dilema Complexo - Assembleia completa
            TaskType.DECISION_MAKING: AgentActivationPlan(
                primary_agents=["supervisor", "oraculo"],
                secondary_agents=["deepagent", "automaster"],
                validation_agents=["reflexor"],
                wake_up_order=["supervisor", "oraculo", "reflexor"],
                max_timeout=90,
                expected_tokens=1500,
                bypass_llm=False
            ),
            
            # Otimização Interna
            TaskType.SYSTEM_OPTIMIZATION: AgentActivationPlan(
                primary_agents=["carlos"],
                secondary_agents=["reflexor"],
                validation_agents=["reflexor"],
                wake_up_order=["carlos", "reflexor"],
                max_timeout=30,
                expected_tokens=200,
                bypass_llm=False
            ),
            
            # Exploração/Inovação Aberta
            TaskType.CREATIVE_EXPLORATION: AgentActivationPlan(
                primary_agents=["raciocinio_continuo", "promptcrafter"],
                secondary_agents=["oraculo"],
                validation_agents=[],
                wake_up_order=["raciocinio_continuo", "promptcrafter", "oraculo"],
                max_timeout=60,
                expected_tokens=1000,
                bypass_llm=False
            )
        }
        
        return matrix
    
    def analyze_message(self, message: str, context: Dict = None) -> MessageAnalysis:
        """
        Analisa mensagem e determina estratégia de ativação
        Implementa Heurísticas de Complexidade do Gemini
        """
        with self.lock:
            self.stats["total_analyses"] += 1
            
            # Normalizar mensagem
            normalized = message.lower().strip()
            words = normalized.split()
            word_count = len(words)
            
            # 1. Detectar comandos do sistema (Gemini: consumo zero)
            if any(cmd in normalized for cmd in self.system_commands):
                return self._create_analysis(
                    complexity=ComplexityLevel.TRIVIAL,
                    task_type=TaskType.SYSTEM_COMMAND,
                    message=message,
                    word_count=word_count,
                    confidence=1.0
                )
            
            # 2. Detectar saudações básicas (Gemini: consumo zero)
            if self._is_greeting(normalized):
                return self._create_analysis(
                    complexity=ComplexityLevel.TRIVIAL,
                    task_type=TaskType.GREETING,
                    message=message,
                    word_count=word_count,
                    confidence=1.0
                )
            
            # 3. Detectar contexto emocional (Gemini: rota direta PsyMind)
            emotional_indicators = self._detect_emotional_context(normalized)
            if emotional_indicators:
                return self._create_analysis(
                    complexity=ComplexityLevel.MODERATE,
                    task_type=TaskType.EMOTIONAL_SUPPORT,
                    message=message,
                    word_count=word_count,
                    emotional_indicators=emotional_indicators,
                    confidence=0.9
                )
            
            # 4. Análise por comprimento (Gemini specs)
            if word_count <= 5:
                # Muito curta - provável simples
                complexity = ComplexityLevel.SIMPLE
            elif word_count <= 15:
                # Curta - analisar palavras-chave
                complexity = self._analyze_keywords(normalized)
            elif word_count <= 50:
                # Média - provável moderada a alta
                complexity = max(self._analyze_keywords(normalized), ComplexityLevel.MODERATE)
            else:
                # Longa - quase sempre complexa
                complexity = max(self._analyze_keywords(normalized), ComplexityLevel.COMPLEX)
            
            # 5. Detectar múltiplas perguntas/instruções
            question_count = self._count_questions(message)
            if question_count > 1:
                complexity = max(complexity, ComplexityLevel.COMPLEX)
            
            # 6. Determinar tipo de tarefa
            task_type = self._classify_task_type(normalized, complexity)
            
            # 7. Gerar análise final
            return self._create_analysis(
                complexity=complexity,
                task_type=task_type,
                message=message,
                word_count=word_count,
                question_count=question_count,
                confidence=self._calculate_confidence(complexity, task_type, word_count)
            )
    
    def _is_greeting(self, normalized: str) -> bool:
        """Detecta saudações básicas"""
        greetings = {"oi", "olá", "ola", "hey", "tudo bem", "como vai", "bom dia", 
                    "boa tarde", "boa noite", "tchau", "até logo", "obrigado", "obrigada"}
        return any(greeting in normalized for greeting in greetings)
    
    def _detect_emotional_context(self, normalized: str) -> List[str]:
        """Detecta indicadores emocionais na mensagem"""
        found_indicators = []
        for indicator in self.emotional_indicators:
            if indicator in normalized:
                found_indicators.append(indicator)
        return found_indicators
    
    def _analyze_keywords(self, normalized: str) -> ComplexityLevel:
        """Analisa palavras-chave para determinar complexidade"""
        # Ordem de prioridade: CRITICAL > COMPLEX > MODERATE > SIMPLE
        for complexity in [ComplexityLevel.CRITICAL, ComplexityLevel.COMPLEX, 
                          ComplexityLevel.MODERATE, ComplexityLevel.SIMPLE]:
            keywords = self.complexity_keywords.get(complexity, set())
            if any(keyword in normalized for keyword in keywords):
                return complexity
        
        return ComplexityLevel.SIMPLE
    
    def _count_questions(self, message: str) -> int:
        """Conta número de perguntas na mensagem"""
        # Contar pontos de interrogação
        question_marks = message.count('?')
        
        # Detectar múltiplas instruções
        enumerations = len(re.findall(r'\d+\.', message))
        bullet_points = len(re.findall(r'[-•*]', message))
        
        return max(question_marks, enumerations, bullet_points, 1)
    
    def _classify_task_type(self, normalized: str, complexity: ComplexityLevel) -> TaskType:
        """Classifica o tipo de tarefa baseado no conteúdo"""
        # Palavras-chave para tipos específicos
        task_indicators = {
            TaskType.RESEARCH: ["analise", "pesquise", "mercado", "produto", "dados", "informações"],
            TaskType.CONTENT_CREATION: ["crie", "escreva", "gere", "prompt", "texto", "conteúdo"],
            TaskType.STRATEGY_PLANNING: ["plano", "estratégia", "planejamento", "objetivos"],
            TaskType.DECISION_MAKING: ["decida", "escolha", "melhor opção", "viabilidade", "investir"],
            TaskType.SYSTEM_OPTIMIZATION: ["otimize", "melhore performance", "limpeza"],
            TaskType.CREATIVE_EXPLORATION: ["surpreenda", "inovação", "criativo", "explore"]
        }
        
        for task_type, keywords in task_indicators.items():
            if any(keyword in normalized for keyword in keywords):
                return task_type
        
        # Fallback baseado na complexidade
        if complexity == ComplexityLevel.TRIVIAL:
            return TaskType.GREETING
        elif complexity == ComplexityLevel.SIMPLE:
            return TaskType.FACTUAL_QUERY
        else:
            return TaskType.RESEARCH
    
    def _create_analysis(self, complexity: ComplexityLevel, task_type: TaskType, 
                        message: str, word_count: int, question_count: int = 1,
                        emotional_indicators: List[str] = None, 
                        confidence: float = 0.8) -> MessageAnalysis:
        """Cria análise completa da mensagem"""
        
        # Obter plano de ativação da matriz
        activation_plan = self.decision_matrix.get(task_type, self.decision_matrix[TaskType.FACTUAL_QUERY])
        
        # Extrair palavras-chave relevantes
        keywords = self._extract_keywords(message.lower())
        
        # Atualizar estatísticas
        if activation_plan.bypass_llm:
            self.stats["llm_bypassed"] += 1
            self.stats["tokens_saved"] += 100  # Estimativa de tokens salvos
        
        return MessageAnalysis(
            complexity=complexity,
            task_type=task_type,
            keywords=keywords,
            question_count=question_count,
            word_count=word_count,
            emotional_indicators=emotional_indicators or [],
            activation_plan=activation_plan,
            confidence=confidence
        )
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrai palavras-chave relevantes do texto"""
        # Palavras irrelevantes (stop words em português)
        stop_words = {"o", "a", "de", "da", "do", "que", "é", "para", "com", "em", 
                     "um", "uma", "por", "se", "no", "na", "os", "as", "dos", "das"}
        
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if len(word) > 3 and word not in stop_words]
        
        return keywords[:10]  # Limitar a 10 palavras-chave
    
    def _calculate_confidence(self, complexity: ComplexityLevel, task_type: TaskType, 
                            word_count: int) -> float:
        """Calcula confiança na classificação"""
        base_confidence = 0.7
        
        # Maior confiança para casos claros
        if complexity == ComplexityLevel.TRIVIAL:
            base_confidence = 0.95
        elif task_type == TaskType.SYSTEM_COMMAND:
            base_confidence = 1.0
        elif word_count > 50:  # Mensagens longas geralmente são complexas
            base_confidence = 0.9
        
        return min(base_confidence, 1.0)
    
    def get_optimization_stats(self) -> Dict:
        """Retorna estatísticas de otimização"""
        with self.lock:
            stats = self.stats.copy()
            
            if stats["total_analyses"] > 0:
                stats["bypass_rate"] = stats["llm_bypassed"] / stats["total_analyses"]
                stats["avg_tokens_saved"] = stats["tokens_saved"] / stats["total_analyses"]
            else:
                stats["bypass_rate"] = 0.0
                stats["avg_tokens_saved"] = 0.0
                
            return stats
    
    def reset_stats(self):
        """Reseta estatísticas"""
        with self.lock:
            self.stats = {
                "total_analyses": 0,
                "llm_bypassed": 0,
                "tokens_saved": 0,
                "avg_agents_activated": 0,
                "cache_hits": 0
            }
            logger.info("📊 Estatísticas de otimização resetadas")


# Singleton global
_optimizer_instance = None
_optimizer_lock = threading.Lock()


def get_agent_optimizer() -> AgentOptimizer:
    """Retorna instância singleton do AgentOptimizer"""
    global _optimizer_instance
    
    with _optimizer_lock:
        if _optimizer_instance is None:
            _optimizer_instance = AgentOptimizer()
        return _optimizer_instance


# Exemplo de uso e teste
if __name__ == "__main__":
    # Teste do sistema de otimização
    optimizer = get_agent_optimizer()
    
    # Casos de teste conforme especificações Gemini
    test_cases = [
        "Oi, tudo bem?",  # TRIVIAL - Saudação
        "/status",        # TRIVIAL - Comando sistema
        "Qual a capital da França?",  # SIMPLE - Fato
        "Analise a viabilidade de vender patinhos no Shopee",  # COMPLEX - Pesquisa
        "Crie um prompt de vendas para meu produto",  # MODERATE - Criação
        "Estou me sentindo ansioso com meu trabalho",  # MODERATE - Emocional
        "Preciso decidir entre investir em X ou Y para minha empresa. Analise cenários, viabilidade econômica, riscos e oportunidades de cada opção.",  # CRITICAL - Decisão
    ]
    
    print("🧪 TESTE DO SISTEMA DE OTIMIZAÇÃO DE AGENTES")
    print("=" * 60)
    
    for i, message in enumerate(test_cases, 1):
        analysis = optimizer.analyze_message(message)
        
        print(f"\n{i}. Mensagem: '{message}'")
        print(f"   Complexidade: {analysis.complexity.value}")
        print(f"   Tipo: {analysis.task_type.value}")
        print(f"   Agentes: {', '.join(analysis.activation_plan.primary_agents)}")
        print(f"   Tokens estimados: {analysis.activation_plan.expected_tokens}")
        print(f"   Bypass LLM: {'Sim' if analysis.activation_plan.bypass_llm else 'Não'}")
        print(f"   Confiança: {analysis.confidence:.1%}")
    
    # Estatísticas
    stats = optimizer.get_optimization_stats()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Análises: {stats['total_analyses']}")
    print(f"   LLM bypassed: {stats['llm_bypassed']} ({stats['bypass_rate']:.1%})")
    print(f"   Tokens economizados: {stats['tokens_saved']}")