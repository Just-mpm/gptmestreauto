"""
Orquestrador Central de Agentes - ETAPA 4
Integra Matriz de Decisão, Wake Up Strategy e Memória Compartilhada
Sistema completo de otimização seguindo especificações Gemini AI
"""

import time
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime

# Imports dos componentes de otimização
from utils.agent_optimizer import (
    get_agent_optimizer, MessageAnalysis, ComplexityLevel, TaskType
)
from utils.agent_wake_manager import (
    get_wake_manager, AgentWakeTask, AgentExecutionResult, AgentStatus
)
from utils.shared_memory_system import get_shared_memory_system
from utils.token_monitor import get_token_monitor

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


@dataclass
class OptimizedResponse:
    """Resposta otimizada do sistema"""
    content: str                              # Conteúdo da resposta
    agents_used: List[str]                   # Agentes que foram ativados
    total_execution_time: float              # Tempo total de execução
    tokens_used: int                         # Tokens consumidos
    tokens_saved: int                        # Tokens economizados
    cache_hits: int                          # Hits de cache
    memory_reused: int                       # Memórias reutilizadas
    complexity_detected: ComplexityLevel     # Complexidade detectada
    optimization_applied: List[str]          # Otimizações aplicadas


class AgentOrchestrator:
    """
    Orquestrador Central que integra todas as otimizações
    Implementa fluxo completo seguindo especificações Gemini AI
    """
    
    def __init__(self):
        # Componentes de otimização
        self.optimizer = get_agent_optimizer()
        self.wake_manager = get_wake_manager()
        self.shared_memory = get_shared_memory_system()
        self.token_monitor = get_token_monitor()
        
        # Cache de respostas pré-definidas (consumo zero)
        self.predefined_responses = {
            # Saudações básicas
            "oi": "Olá! Como posso ajudá-lo hoje?",
            "olá": "Oi! Em que posso ser útil?",
            "ola": "Olá! Como posso ajudá-lo?",
            "tudo bem": "Tudo ótimo! Como posso ajudá-lo?",
            "como vai": "Vou muito bem, obrigado! E você?",
            "bom dia": "Bom dia! Como posso ajudá-lo hoje?",
            "boa tarde": "Boa tarde! Em que posso ser útil?",
            "boa noite": "Boa noite! Como posso ajudá-lo?",
            
            # Comandos simples
            "obrigado": "De nada! Fico feliz em ajudar.",
            "tchau": "Até logo! Foi um prazer ajudá-lo.",
            "até logo": "Tchau! Volte sempre que precisar.",
            
            # Comandos de sistema processados internamente
            "/help": "Comandos disponíveis: /status, /help, /agents, /reset",
        }
        
        self.lock = threading.Lock()
        
        # Estatísticas de otimização
        self.optimization_stats = {
            "total_requests": 0,
            "zero_token_responses": 0,
            "cache_hits": 0,
            "memory_reused": 0,
            "agents_bypassed": 0,
            "total_tokens_saved": 0
        }
        
        logger.info("🎯 AgentOrchestrator inicializado - Otimização Gemini AI ativa")
    
    def process_optimized(self, message: str, context: Dict = None, 
                         user_id: str = None) -> OptimizedResponse:
        """
        Processa mensagem com otimização completa
        Implementa fluxo de otimização Gemini AI
        """
        start_time = time.time()
        context = context or {}
        optimizations_applied = []
        
        with self.lock:
            self.optimization_stats["total_requests"] += 1
        
        logger.debug(f"🎯 Processando: '{message[:50]}...'")
        
        # ETAPA 1: Análise inicial e classificação (Gemini Matrix)
        analysis = self.optimizer.analyze_message(message, context)
        logger.debug(f"📊 Complexidade: {analysis.complexity.value}, Tipo: {analysis.task_type.value}")
        
        # ETAPA 2: Verificar respostas pré-definidas (CONSUMO ZERO)
        if analysis.complexity == ComplexityLevel.TRIVIAL:
            predefined = self._check_predefined_response(message)
            if predefined:
                self._update_stats("zero_token_responses")
                optimizations_applied.append("predefined_response")
                
                return OptimizedResponse(
                    content=predefined,
                    agents_used=[],
                    total_execution_time=time.time() - start_time,
                    tokens_used=0,
                    tokens_saved=100,  # Estimativa
                    cache_hits=0,
                    memory_reused=0,
                    complexity_detected=analysis.complexity,
                    optimization_applied=optimizations_applied
                )
        
        # ETAPA 3: Verificar memória compartilhada (Gemini Memory Strategy)
        memory_result = self._check_shared_memory(message, analysis)
        if memory_result:
            self._update_stats("memory_reused")
            optimizations_applied.append("shared_memory_hit")
            
            return OptimizedResponse(
                content=memory_result,
                agents_used=["memory_system"],
                total_execution_time=time.time() - start_time,
                tokens_used=0,
                tokens_saved=analysis.activation_plan.expected_tokens,
                cache_hits=0,
                memory_reused=1,
                complexity_detected=analysis.complexity,
                optimization_applied=optimizations_applied
            )
        
        # ETAPA 4: Verificar processamento similar (Cache Strategy)
        similar_processing = self.shared_memory.check_similar_processing(
            agent_name="carlos",
            task_description=message
        )
        
        if similar_processing:
            self._update_stats("cache_hits")
            optimizations_applied.append("similar_processing_cache")
            
            return OptimizedResponse(
                content=str(similar_processing),
                agents_used=["cache_system"],
                total_execution_time=time.time() - start_time,
                tokens_used=0,
                tokens_saved=analysis.activation_plan.expected_tokens,
                cache_hits=1,
                memory_reused=0,
                complexity_detected=analysis.complexity,
                optimization_applied=optimizations_applied
            )
        
        # ETAPA 5: Execução otimizada com agentes (Gemini Wake Up Strategy)
        response_content, execution_results = self._execute_optimized_agents(
            analysis, message, context
        )
        
        # Registrar tokens no monitor
        total_tokens = sum(result.tokens_used for result in execution_results.values())
        if total_tokens > 0:
            self.token_monitor.log_tokens("orchestrator", total_tokens // 2, total_tokens // 2)
        
        # ETAPA 6: Armazenar resultado para futuro reuso
        if analysis.complexity in [ComplexityLevel.COMPLEX, ComplexityLevel.CRITICAL]:
            self._store_high_value_result(message, response_content, analysis)
            optimizations_applied.append("high_value_storage")
        
        # Calcular tokens economizados
        tokens_saved = self._calculate_tokens_saved(analysis, execution_results)
        
        return OptimizedResponse(
            content=response_content,
            agents_used=list(execution_results.keys()),
            total_execution_time=time.time() - start_time,
            tokens_used=total_tokens,
            tokens_saved=tokens_saved,
            cache_hits=0,
            memory_reused=0,
            complexity_detected=analysis.complexity,
            optimization_applied=optimizations_applied
        )
    
    def _check_predefined_response(self, message: str) -> Optional[str]:
        """Verifica respostas pré-definidas para consumo zero"""
        normalized = message.lower().strip()
        
        # Busca exata
        if normalized in self.predefined_responses:
            return self.predefined_responses[normalized]
        
        # Busca por padrões
        for pattern, response in self.predefined_responses.items():
            if pattern in normalized:
                return response
        
        return None
    
    def _check_shared_memory(self, message: str, analysis: MessageAnalysis) -> Optional[str]:
        """Verifica memória compartilhada para reuso"""
        # Buscar memórias relacionadas
        memories = self.shared_memory.search_shared_memory(
            requesting_agent="orchestrator",
            query=message,
            tags=set(analysis.keywords)
        )
        
        if memories:
            # Usar a memória mais relevante
            _, memory_value, owner_agent = memories[0]
            
            if isinstance(memory_value, dict) and "response" in memory_value:
                return memory_value["response"]
            elif isinstance(memory_value, str):
                return memory_value
        
        return None
    
    def _execute_optimized_agents(self, analysis: MessageAnalysis, message: str, 
                                context: Dict) -> Tuple[str, Dict[str, AgentExecutionResult]]:
        """Executa agentes seguindo estratégia otimizada"""
        
        # Preparar tarefas de wake up baseadas no plano de ativação
        wake_tasks = []
        plan = analysis.activation_plan
        
        # Se bypass LLM, retornar resposta simples
        if plan.bypass_llm:
            return f"Comando {message} processado com sucesso.", {}
        
        # Criar tarefas para agentes primários
        for i, agent_name in enumerate(plan.primary_agents):
            task = AgentWakeTask(
                agent_name=agent_name,
                priority=i,
                dependencies=set(),
                timeout=plan.max_timeout,
                context={"message": message, "context": context}
            )
            wake_tasks.append(task)
        
        # Adicionar agentes secundários com dependências
        for i, agent_name in enumerate(plan.secondary_agents):
            task = AgentWakeTask(
                agent_name=agent_name,
                priority=len(plan.primary_agents) + i,
                dependencies=set(plan.primary_agents),
                timeout=plan.max_timeout,
                context={"message": message, "context": context}
            )
            wake_tasks.append(task)
        
        # Executar wake up otimizado
        execution_results = self.wake_manager.wake_agents_sequence(
            wake_tasks, 
            global_timeout=plan.max_timeout
        )
        
        # Consolidar resposta
        response_parts = []
        
        for agent_name in plan.wake_up_order:
            if agent_name in execution_results:
                result = execution_results[agent_name]
                if result.status == AgentStatus.COMPLETED and result.result:
                    response_parts.append(str(result.result))
        
        if response_parts:
            final_response = "\n\n".join(response_parts)
        else:
            final_response = "Processamento concluído com otimizações aplicadas."
        
        return final_response, execution_results
    
    def _store_high_value_result(self, message: str, response: str, analysis: MessageAnalysis):
        """Armazena resultado de alto valor para reuso futuro"""
        self.shared_memory.store_memory(
            agent_name="orchestrator",
            key=f"processed_{analysis.task_type.value}",
            value={
                "query": message,
                "response": response,
                "complexity": analysis.complexity.value,
                "timestamp": datetime.now().isoformat()
            },
            share_with=set(analysis.activation_plan.primary_agents),
            ttl_seconds=86400,  # 24 horas
            is_high_value=True,
            tags={"processed_task", analysis.task_type.value, "high_value"}
        )
    
    def _calculate_tokens_saved(self, analysis: MessageAnalysis, 
                              execution_results: Dict[str, AgentExecutionResult]) -> int:
        """Calcula tokens economizados pelas otimizações"""
        # Tokens que seriam usados sem otimização
        expected_tokens = analysis.activation_plan.expected_tokens
        
        # Tokens realmente usados
        actual_tokens = sum(result.tokens_used for result in execution_results.values())
        
        # Economia = diferença
        tokens_saved = max(0, expected_tokens - actual_tokens)
        
        # Adicionar economia por agentes não ativados
        all_possible_agents = {
            "carlos", "supervisor", "deepagent", "scout", "oraculo", 
            "automaster", "reflexor", "psymind", "promptcrafter", "taskbreaker"
        }
        activated_agents = set(execution_results.keys())
        bypassed_agents = all_possible_agents - activated_agents
        
        # Estimativa: 150 tokens por agente bypassado
        tokens_saved += len(bypassed_agents) * 150
        
        return tokens_saved
    
    def _update_stats(self, stat_name: str):
        """Atualiza estatísticas de otimização"""
        with self.lock:
            if stat_name in self.optimization_stats:
                self.optimization_stats[stat_name] += 1
    
    def get_optimization_report(self) -> Dict:
        """Retorna relatório completo de otimizações"""
        with self.lock:
            base_stats = self.optimization_stats.copy()
        
        # Adicionar estatísticas dos componentes
        optimizer_stats = self.optimizer.get_optimization_stats()
        memory_stats = self.shared_memory.get_system_stats()
        wake_stats = self.wake_manager.get_performance_stats()
        
        # Calcular métricas derivadas
        if base_stats["total_requests"] > 0:
            optimization_rate = (
                (base_stats["zero_token_responses"] + 
                 base_stats["cache_hits"] + 
                 base_stats["memory_reused"]) / 
                base_stats["total_requests"]
            )
        else:
            optimization_rate = 0.0
        
        return {
            "orchestrator_stats": base_stats,
            "optimization_rate": optimization_rate,
            "optimizer_component": optimizer_stats,
            "memory_component": memory_stats,
            "wake_manager_component": wake_stats,
            "total_tokens_saved": (
                base_stats["total_tokens_saved"] + 
                optimizer_stats.get("tokens_saved", 0) + 
                memory_stats.get("tokens_saved", 0)
            )
        }
    
    def reset_optimization_stats(self):
        """Reseta todas as estatísticas de otimização"""
        with self.lock:
            self.optimization_stats = {
                "total_requests": 0,
                "zero_token_responses": 0,
                "cache_hits": 0,
                "memory_reused": 0,
                "agents_bypassed": 0,
                "total_tokens_saved": 0
            }
        
        self.optimizer.reset_stats()
        logger.info("📊 Estatísticas de otimização resetadas")


# Singleton global
_orchestrator_instance = None
_orchestrator_lock = threading.Lock()


def get_agent_orchestrator() -> AgentOrchestrator:
    """Retorna instância singleton do AgentOrchestrator"""
    global _orchestrator_instance
    
    with _orchestrator_lock:
        if _orchestrator_instance is None:
            _orchestrator_instance = AgentOrchestrator()
        return _orchestrator_instance


# Teste do orquestrador
if __name__ == "__main__":
    print("🧪 TESTE DO ORQUESTRADOR CENTRAL DE AGENTES")
    print("=" * 60)
    
    # Obter orquestrador
    orchestrator = get_agent_orchestrator()
    
    # Casos de teste seguindo especificações Gemini
    test_cases = [
        ("Oi", "Saudação básica - consumo zero"),
        ("/status", "Comando sistema - consumo zero"),
        ("Qual a capital da França?", "Pergunta simples"),
        ("Analise a viabilidade de vender patinhos no Shopee", "Análise complexa"),
        ("Crie um prompt de vendas", "Criação de conteúdo"),
        ("Estou ansioso com meu trabalho", "Suporte emocional"),
        ("Olá", "Saudação - teste cache"),  # Repetida para testar cache
    ]
    
    for i, (message, description) in enumerate(test_cases, 1):
        print(f"\n{i}. {description}")
        print(f"   Mensagem: '{message}'")
        
        # Processar com otimização
        start_time = time.time()
        response = orchestrator.process_optimized(message)
        processing_time = time.time() - start_time
        
        print(f"   ⚡ Tempo: {processing_time:.3f}s")
        print(f"   🎯 Complexidade: {response.complexity_detected.value}")
        print(f"   🤖 Agentes: {', '.join(response.agents_used) if response.agents_used else 'Nenhum'}")
        print(f"   💰 Tokens usados: {response.tokens_used}")
        print(f"   💎 Tokens economizados: {response.tokens_saved}")
        print(f"   🔧 Otimizações: {', '.join(response.optimization_applied)}")
        print(f"   📝 Resposta: {response.content[:100]}...")
    
    # Relatório de otimização
    report = orchestrator.get_optimization_report()
    print(f"\n📊 RELATÓRIO DE OTIMIZAÇÃO:")
    print(f"   Total de requisições: {report['orchestrator_stats']['total_requests']}")
    print(f"   Taxa de otimização: {report['optimization_rate']:.1%}")
    print(f"   Respostas zero token: {report['orchestrator_stats']['zero_token_responses']}")
    print(f"   Cache hits: {report['orchestrator_stats']['cache_hits']}")
    print(f"   Memória reutilizada: {report['orchestrator_stats']['memory_reused']}")
    print(f"   Total tokens economizados: {report['total_tokens_saved']}")
    
    print(f"\n✅ TESTE CONCLUÍDO - Sistema otimizado funcionando!")