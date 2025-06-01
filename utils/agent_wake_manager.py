"""
Sistema de Wake Up e Coordenação de Agentes - ETAPA 4
Implementa estratégia inteligente de ativação com timeouts e dependências
Seguindo especificações Gemini AI
"""

import time
import threading
import asyncio
from typing import Dict, List, Set, Optional, Callable, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime, timedelta
import concurrent.futures
from contextlib import asynccontextmanager

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


class AgentStatus(Enum):
    """Status de um agente no sistema"""
    SLEEPING = "sleeping"        # Agente não ativo
    INITIALIZING = "initializing"  # Iniciando
    ACTIVE = "active"            # Pronto para trabalhar
    BUSY = "busy"                # Processando tarefa
    WAITING = "waiting"          # Aguardando dependência
    TIMEOUT = "timeout"          # Timeout atingido
    ERROR = "error"              # Erro na execução
    COMPLETED = "completed"      # Tarefa concluída


@dataclass
class AgentExecutionResult:
    """Resultado da execução de um agente"""
    agent_name: str
    status: AgentStatus
    result: Any = None
    error: Optional[str] = None
    execution_time: float = 0.0
    tokens_used: int = 0
    memory_used: Dict = field(default_factory=dict)


@dataclass 
class AgentWakeTask:
    """Tarefa de ativação de um agente"""
    agent_name: str
    priority: int                # Prioridade (0 = maior)
    dependencies: Set[str]       # Agentes que devem executar antes
    timeout: int                 # Timeout em segundos
    max_retries: int = 1         # Máximo de tentativas
    callback: Optional[Callable] = None  # Callback pós-execução
    context: Dict = field(default_factory=dict)  # Contexto da tarefa


class CircuitBreakerState(Enum):
    """Estados do Circuit Breaker"""
    CLOSED = "closed"      # Funcionando normalmente
    OPEN = "open"          # Falha detectada, bloqueando
    HALF_OPEN = "half_open"  # Testando recuperação


@dataclass
class CircuitBreaker:
    """Circuit Breaker para agentes com falhas"""
    failure_threshold: int = 3    # Falhas para abrir
    reset_timeout: int = 60      # Segundos para tentar reset
    state: CircuitBreakerState = CircuitBreakerState.CLOSED
    failure_count: int = 0
    last_failure_time: Optional[datetime] = None
    
    def record_success(self):
        """Registra sucesso na execução"""
        self.failure_count = 0
        if self.state == CircuitBreakerState.HALF_OPEN:
            self.state = CircuitBreakerState.CLOSED
    
    def record_failure(self):
        """Registra falha na execução"""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitBreakerState.OPEN
    
    def can_execute(self) -> bool:
        """Verifica se pode executar baseado no circuit breaker"""
        if self.state == CircuitBreakerState.CLOSED:
            return True
        elif self.state == CircuitBreakerState.OPEN:
            # Verificar se é hora de tentar half-open
            if (self.last_failure_time and 
                datetime.now() - self.last_failure_time > timedelta(seconds=self.reset_timeout)):
                self.state = CircuitBreakerState.HALF_OPEN
                return True
            return False
        else:  # HALF_OPEN
            return True


class AgentWakeManager:
    """
    Gerenciador de Wake Up de Agentes
    Implementa Strategy Pattern do Gemini com timeouts adaptativos
    """
    
    def __init__(self, max_concurrent_agents: int = 5):
        self.max_concurrent_agents = max_concurrent_agents
        self.active_agents: Dict[str, AgentStatus] = {}
        self.agent_registry: Dict[str, Any] = {}  # Instâncias dos agentes
        self.circuit_breakers: Dict[str, CircuitBreaker] = {}
        self.execution_history: List[AgentExecutionResult] = []
        
        # Timeouts específicos por tipo de agente (Gemini specs)
        self.agent_timeouts = {
            "carlos": 15,              # Maestro central - rápido
            "supervisor": 20,          # Classificação rápida
            "taskbreaker": 25,         # Decomposição de tarefas
            "deepagent": 45,           # Busca externa - maior latência
            "scout": 45,               # Pesquisa com APIs externas  
            "oraculo": 60,             # Assembleia dinâmica - complexo
            "automaster": 30,          # Estratégia e planejamento
            "promptcrafter": 25,       # Criação de prompts
            "psymind": 30,             # Análise psicológica
            "reflexor": 20,            # Auditoria e validação
            "raciocinio_continuo": 40  # Raciocínio multi-perspectiva
        }
        
        # Dependências entre agentes (Gemini specs)
        self.agent_dependencies = {
            "scout": {"deepagent"},           # Scout precisa de dados do DeepAgent
            "oraculo": {"supervisor"},        # Oráculo precisa de classificação
            "reflexor": {"automaster", "deepagent", "promptcrafter"}  # Reflexor audita outros
        }
        
        self.lock = threading.Lock()
        
        logger.info("🚀 AgentWakeManager inicializado com timeouts Gemini")
    
    def register_agent(self, agent_name: str, agent_instance: Any):
        """Registra um agente no sistema"""
        with self.lock:
            self.active_agents[agent_name] = AgentStatus.SLEEPING
            self.agent_registry[agent_name] = agent_instance
            self.circuit_breakers[agent_name] = CircuitBreaker()
            
            logger.debug(f"🤖 Agente {agent_name} registrado")
    
    def wake_agents_sequence(self, wake_tasks: List[AgentWakeTask], 
                           global_timeout: int = 120) -> Dict[str, AgentExecutionResult]:
        """
        Ativa agentes em sequência inteligente respeitando dependências
        Implementa Strategy Pattern do Gemini
        """
        start_time = time.time()
        results: Dict[str, AgentExecutionResult] = {}
        
        logger.info(f"🎯 Iniciando wake up de {len(wake_tasks)} agentes")
        
        # Ordenar tarefas por prioridade e dependências
        sorted_tasks = self._sort_tasks_by_dependencies(wake_tasks)
        
        # Executor para paralelismo controlado
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_concurrent_agents) as executor:
            futures: Dict[concurrent.futures.Future, AgentWakeTask] = {}
            
            for task in sorted_tasks:
                # Verificar timeout global
                if time.time() - start_time > global_timeout:
                    logger.warning(f"⏰ Timeout global atingido ({global_timeout}s)")
                    break
                
                # Aguardar dependências
                if not self._wait_for_dependencies(task, results):
                    logger.warning(f"⚠️ Dependências não satisfeitas para {task.agent_name}")
                    continue
                
                # Verificar circuit breaker
                circuit_breaker = self.circuit_breakers.get(task.agent_name)
                if circuit_breaker and not circuit_breaker.can_execute():
                    logger.warning(f"🔴 Circuit breaker aberto para {task.agent_name}")
                    results[task.agent_name] = AgentExecutionResult(
                        agent_name=task.agent_name,
                        status=AgentStatus.ERROR,
                        error="Circuit breaker open"
                    )
                    continue
                
                # Submeter execução
                future = executor.submit(self._execute_agent_task, task)
                futures[future] = task
                
                logger.debug(f"🚀 {task.agent_name} submetido para execução")
            
            # Coletar resultados
            for future in concurrent.futures.as_completed(futures, timeout=global_timeout):
                task = futures[future]
                try:
                    result = future.result()
                    results[task.agent_name] = result
                    
                    # Atualizar circuit breaker
                    circuit_breaker = self.circuit_breakers.get(task.agent_name)
                    if circuit_breaker:
                        if result.status == AgentStatus.COMPLETED:
                            circuit_breaker.record_success()
                        else:
                            circuit_breaker.record_failure()
                    
                    logger.debug(f"✅ {task.agent_name} concluído: {result.status.value}")
                    
                except Exception as e:
                    logger.error(f"❌ Erro na execução de {task.agent_name}: {e}")
                    results[task.agent_name] = AgentExecutionResult(
                        agent_name=task.agent_name,
                        status=AgentStatus.ERROR,
                        error=str(e)
                    )
        
        total_time = time.time() - start_time
        logger.info(f"🏁 Wake up concluído em {total_time:.2f}s - {len(results)} agentes")
        
        return results
    
    def _sort_tasks_by_dependencies(self, tasks: List[AgentWakeTask]) -> List[AgentWakeTask]:
        """Ordena tarefas respeitando dependências e prioridades"""
        # Criar grafo de dependências
        task_map = {task.agent_name: task for task in tasks}
        sorted_tasks = []
        completed = set()
        
        def can_execute(task: AgentWakeTask) -> bool:
            """Verifica se todas as dependências foram satisfeitas"""
            return task.dependencies.issubset(completed)
        
        # Algoritmo de ordenação topológica com prioridades
        while len(sorted_tasks) < len(tasks):
            # Encontrar tarefas executáveis
            executable = [
                task for task in tasks 
                if task.agent_name not in completed and can_execute(task)
            ]
            
            if not executable:
                # Deadlock ou dependência circular
                remaining = [task for task in tasks if task.agent_name not in completed]
                logger.warning(f"⚠️ Possível deadlock detectado: {[t.agent_name for t in remaining]}")
                # Adicionar pelo menos uma tarefa para evitar loop infinito
                if remaining:
                    sorted_tasks.append(remaining[0])
                    completed.add(remaining[0].agent_name)
                continue
            
            # Ordenar por prioridade (menor número = maior prioridade)
            executable.sort(key=lambda t: t.priority)
            
            # Executar a de maior prioridade
            next_task = executable[0]
            sorted_tasks.append(next_task)
            completed.add(next_task.agent_name)
        
        return sorted_tasks
    
    def _wait_for_dependencies(self, task: AgentWakeTask, 
                              results: Dict[str, AgentExecutionResult],
                              max_wait: int = 30) -> bool:
        """Aguarda dependências serem satisfeitas"""
        if not task.dependencies:
            return True
        
        start_wait = time.time()
        
        while time.time() - start_wait < max_wait:
            satisfied = True
            for dep in task.dependencies:
                if dep not in results or results[dep].status != AgentStatus.COMPLETED:
                    satisfied = False
                    break
            
            if satisfied:
                return True
            
            time.sleep(0.5)  # Aguardar um pouco
        
        logger.warning(f"⏰ Timeout aguardando dependências para {task.agent_name}")
        return False
    
    def _execute_agent_task(self, task: AgentWakeTask) -> AgentExecutionResult:
        """Executa uma tarefa de agente com timeout"""
        start_time = time.time()
        agent_name = task.agent_name
        
        # Atualizar status
        with self.lock:
            self.active_agents[agent_name] = AgentStatus.INITIALIZING
        
        try:
            # Obter instância do agente
            agent_instance = self.agent_registry.get(agent_name)
            if not agent_instance:
                raise ValueError(f"Agente {agent_name} não registrado")
            
            # Atualizar status para ativo
            with self.lock:
                self.active_agents[agent_name] = AgentStatus.ACTIVE
            
            # Executar com timeout
            timeout = self.agent_timeouts.get(agent_name, task.timeout)
            
            result = self._execute_with_timeout(
                agent_instance, 
                task.context, 
                timeout
            )
            
            execution_time = time.time() - start_time
            
            # Criar resultado de sucesso
            agent_result = AgentExecutionResult(
                agent_name=agent_name,
                status=AgentStatus.COMPLETED,
                result=result,
                execution_time=execution_time,
                tokens_used=getattr(result, 'tokens_used', 0)
            )
            
            # Callback se definido
            if task.callback:
                try:
                    task.callback(agent_result)
                except Exception as e:
                    logger.warning(f"⚠️ Erro no callback de {agent_name}: {e}")
            
            return agent_result
            
        except TimeoutError:
            logger.warning(f"⏰ Timeout de {agent_name} ({timeout}s)")
            return AgentExecutionResult(
                agent_name=agent_name,
                status=AgentStatus.TIMEOUT,
                error=f"Timeout após {timeout}s",
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"❌ Erro na execução de {agent_name}: {e}")
            return AgentExecutionResult(
                agent_name=agent_name,
                status=AgentStatus.ERROR,
                error=str(e),
                execution_time=time.time() - start_time
            )
        
        finally:
            # Voltar para sleeping
            with self.lock:
                self.active_agents[agent_name] = AgentStatus.SLEEPING
    
    def _execute_with_timeout(self, agent_instance: Any, context: Dict, timeout: int) -> Any:
        """Executa agente com timeout usando threads"""
        result = [None]
        exception = [None]
        
        def target():
            try:
                # Assumir que agente tem método 'processar'
                if hasattr(agent_instance, 'processar'):
                    result[0] = agent_instance.processar(
                        context.get('message', ''), 
                        context.get('context', {})
                    )
                else:
                    result[0] = f"Agente {agent_instance.__class__.__name__} ativado"
            except Exception as e:
                exception[0] = e
        
        thread = threading.Thread(target=target)
        thread.daemon = True
        thread.start()
        thread.join(timeout)
        
        if thread.is_alive():
            # Thread ainda executando - timeout
            raise TimeoutError(f"Execução excedeu {timeout}s")
        
        if exception[0]:
            raise exception[0]
        
        return result[0]
    
    def get_agent_status(self, agent_name: str) -> AgentStatus:
        """Retorna status atual de um agente"""
        with self.lock:
            return self.active_agents.get(agent_name, AgentStatus.SLEEPING)
    
    def get_all_status(self) -> Dict[str, AgentStatus]:
        """Retorna status de todos os agentes"""
        with self.lock:
            return self.active_agents.copy()
    
    def get_circuit_breaker_status(self) -> Dict[str, Dict]:
        """Retorna status dos circuit breakers"""
        status = {}
        for agent_name, cb in self.circuit_breakers.items():
            status[agent_name] = {
                "state": cb.state.value,
                "failure_count": cb.failure_count,
                "can_execute": cb.can_execute()
            }
        return status
    
    def reset_circuit_breaker(self, agent_name: str):
        """Reseta circuit breaker de um agente"""
        if agent_name in self.circuit_breakers:
            self.circuit_breakers[agent_name] = CircuitBreaker()
            logger.info(f"🔄 Circuit breaker resetado para {agent_name}")
    
    def get_performance_stats(self) -> Dict:
        """Retorna estatísticas de performance"""
        if not self.execution_history:
            return {"total_executions": 0}
        
        successful = [r for r in self.execution_history if r.status == AgentStatus.COMPLETED]
        failed = [r for r in self.execution_history if r.status == AgentStatus.ERROR]
        timeouts = [r for r in self.execution_history if r.status == AgentStatus.TIMEOUT]
        
        avg_execution_time = sum(r.execution_time for r in successful) / len(successful) if successful else 0
        
        return {
            "total_executions": len(self.execution_history),
            "successful": len(successful),
            "failed": len(failed),
            "timeouts": len(timeouts),
            "success_rate": len(successful) / len(self.execution_history) if self.execution_history else 0,
            "avg_execution_time": avg_execution_time,
            "total_tokens_used": sum(r.tokens_used for r in self.execution_history)
        }


# Singleton global
_wake_manager_instance = None
_wake_manager_lock = threading.Lock()


def get_wake_manager() -> AgentWakeManager:
    """Retorna instância singleton do AgentWakeManager"""
    global _wake_manager_instance
    
    with _wake_manager_lock:
        if _wake_manager_instance is None:
            _wake_manager_instance = AgentWakeManager()
        return _wake_manager_instance


# Teste do sistema
if __name__ == "__main__":
    # Teste básico do wake manager
    wake_manager = get_wake_manager()
    
    # Simular agentes
    class MockAgent:
        def __init__(self, name, sleep_time=1):
            self.name = name
            self.sleep_time = sleep_time
        
        def processar(self, message, context):
            time.sleep(self.sleep_time)
            return f"{self.name} processou: {message}"
    
    # Registrar agentes mock
    agents = ["carlos", "supervisor", "deepagent", "reflexor"]
    for agent_name in agents:
        mock_agent = MockAgent(agent_name, sleep_time=0.5)
        wake_manager.register_agent(agent_name, mock_agent)
    
    # Criar tarefas de teste
    tasks = [
        AgentWakeTask(
            agent_name="carlos",
            priority=0,
            dependencies=set(),
            timeout=10,
            context={"message": "Teste Carlos"}
        ),
        AgentWakeTask(
            agent_name="supervisor", 
            priority=1,
            dependencies={"carlos"},
            timeout=15,
            context={"message": "Teste Supervisor"}
        ),
        AgentWakeTask(
            agent_name="deepagent",
            priority=2,
            dependencies={"supervisor"},
            timeout=20,
            context={"message": "Teste DeepAgent"}
        ),
        AgentWakeTask(
            agent_name="reflexor",
            priority=3,
            dependencies={"deepagent"},
            timeout=15,
            context={"message": "Teste Reflexor"}
        )
    ]
    
    print("🧪 TESTE DO SISTEMA DE WAKE UP")
    print("=" * 50)
    
    # Executar wake up
    results = wake_manager.wake_agents_sequence(tasks)
    
    # Mostrar resultados
    for agent_name, result in results.items():
        print(f"\n🤖 {agent_name}:")
        print(f"   Status: {result.status.value}")
        print(f"   Tempo: {result.execution_time:.2f}s")
        if result.result:
            print(f"   Resultado: {result.result}")
        if result.error:
            print(f"   Erro: {result.error}")
    
    # Estatísticas
    stats = wake_manager.get_performance_stats()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Execuções: {stats['total_executions']}")
    print(f"   Sucessos: {stats['successful']}")
    print(f"   Taxa de sucesso: {stats['success_rate']:.1%}")
    print(f"   Tempo médio: {stats['avg_execution_time']:.2f}s")