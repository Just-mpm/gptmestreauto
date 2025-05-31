"""
BaseAgent v2.0 - Fundação Robusta para GPT Mestre Autônomo
Inclui: Persistência, Rate Limiting, Thread Safety, Auto-Recovery, Performance Monitoring
"""

import asyncio
import json
import threading
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import deque
import os
import pickle
import hashlib

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

@dataclass
class PerformanceMetrics:
    """Métricas de performance detalhadas"""
    response_time_avg: float = 0.0
    response_time_p95: float = 0.0
    success_rate: float = 100.0
    error_rate: float = 0.0
    requests_per_minute: int = 0
    tokens_consumed: int = 0
    memory_usage_mb: float = 0.0
    total_requests: int = 0
    total_errors: int = 0
    last_request_time: Optional[datetime] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "response_time_avg": self.response_time_avg,
            "response_time_p95": self.response_time_p95,
            "success_rate": self.success_rate,
            "error_rate": self.error_rate,
            "requests_per_minute": self.requests_per_minute,
            "tokens_consumed": self.tokens_consumed,
            "memory_usage_mb": self.memory_usage_mb,
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "last_request_time": self.last_request_time.isoformat() if self.last_request_time else None
        }

@dataclass
class AgentMemoryV2:
    """Estrutura de memória avançada com persistência"""
    messages: deque = field(default_factory=lambda: deque(maxlen=100))
    context: Dict[str, Any] = field(default_factory=dict)
    user_preferences: Dict[str, Any] = field(default_factory=dict)
    session_id: str = ""
    last_interaction: Optional[datetime] = None
    interaction_count: int = 0
    
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None):
        """Adiciona mensagem à memória"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now(),
            "metadata": metadata or {}
        })
        self.last_interaction = datetime.now()
        self.interaction_count += 1
    
    def get_context_window(self, max_messages: int = 10) -> List[Dict]:
        """Obtém janela de contexto limitada"""
        return list(self.messages)[-max_messages:]
    
    def to_dict(self) -> Dict[str, Any]:
        """Serializa memória para persistência"""
        return {
            "messages": list(self.messages),
            "context": self.context,
            "user_preferences": self.user_preferences,
            "session_id": self.session_id,
            "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None,
            "interaction_count": self.interaction_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AgentMemoryV2':
        """Deserializa memória da persistência"""
        memory = cls()
        memory.messages = deque(data.get("messages", []), maxlen=100)
        memory.context = data.get("context", {})
        memory.user_preferences = data.get("user_preferences", {})
        memory.session_id = data.get("session_id", "")
        memory.interaction_count = data.get("interaction_count", 0)
        
        if data.get("last_interaction"):
            memory.last_interaction = datetime.fromisoformat(data["last_interaction"])
        
        return memory

class RateLimiter:
    """Rate limiter inteligente com burst allowance"""
    
    def __init__(self, max_requests: int = 60, window_seconds: int = 60, burst_allowance: int = 10):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.burst_allowance = burst_allowance
        self.requests = deque()
        self.burst_used = 0
        self.lock = threading.Lock()
    
    def can_proceed(self) -> bool:
        """Verifica se pode prosseguir com a requisição"""
        with self.lock:
            now = datetime.now()
            cutoff = now - timedelta(seconds=self.window_seconds)
            
            # Remove requisições antigas
            while self.requests and self.requests[0] < cutoff:
                self.requests.popleft()
            
            # Verifica limite normal
            if len(self.requests) < self.max_requests:
                self.requests.append(now)
                return True
            
            # Verifica burst allowance
            if self.burst_used < self.burst_allowance:
                self.burst_used += 1
                self.requests.append(now)
                logger.warning(f"Using burst allowance: {self.burst_used}/{self.burst_allowance}")
                return True
            
            return False
    
    def wait_time(self) -> float:
        """Calcula tempo de espera necessário"""
        with self.lock:
            if not self.requests:
                return 0.0
            
            oldest_request = self.requests[0]
            wait_until = oldest_request + timedelta(seconds=self.window_seconds)
            wait_seconds = (wait_until - datetime.now()).total_seconds()
            
            return max(0.0, wait_seconds)

class CircuitBreaker:
    """Circuit breaker para proteção contra falhas"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 30, half_open_requests: int = 3):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_requests = half_open_requests
        
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN
        self.half_open_attempts = 0
        self.lock = threading.Lock()
    
    def can_execute(self) -> bool:
        """Verifica se pode executar operação"""
        with self.lock:
            if self.state == "CLOSED":
                return True
            elif self.state == "OPEN":
                # Verifica se deve tentar abrir
                if self.last_failure_time and \
                   (datetime.now() - self.last_failure_time).total_seconds() > self.recovery_timeout:
                    self.state = "HALF_OPEN"
                    self.half_open_attempts = 0
                    logger.info("Circuit breaker moving to HALF_OPEN state")
                    return True
                return False
            elif self.state == "HALF_OPEN":
                return self.half_open_attempts < self.half_open_requests
    
    def record_success(self):
        """Registra sucesso"""
        with self.lock:
            if self.state == "HALF_OPEN":
                self.half_open_attempts += 1
                if self.half_open_attempts >= self.half_open_requests:
                    self.state = "CLOSED"
                    self.failure_count = 0
                    logger.info("Circuit breaker CLOSED - recovered")
            elif self.state == "CLOSED":
                self.failure_count = max(0, self.failure_count - 1)
    
    def record_failure(self):
        """Registra falha"""
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = datetime.now()
            
            if self.state == "HALF_OPEN":
                self.state = "OPEN"
                logger.warning("Circuit breaker OPEN - half-open failed")
            elif self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                logger.warning(f"Circuit breaker OPEN - {self.failure_count} failures")

class PersistentMemoryManager:
    """Gerenciador de memória persistente"""
    
    def __init__(self, storage_dir: str = "memory/agents", compression: bool = True):
        self.storage_dir = storage_dir
        self.compression = compression
        os.makedirs(storage_dir, exist_ok=True)
    
    def _get_storage_path(self, agent_id: str, session_id: str = "") -> str:
        """Gera caminho para armazenamento"""
        filename = f"{agent_id}_{session_id}.pkl" if session_id else f"{agent_id}.pkl"
        return os.path.join(self.storage_dir, filename)
    
    def save_memory(self, agent_id: str, memory: AgentMemoryV2, session_id: str = "") -> bool:
        """Salva memória no storage"""
        try:
            storage_path = self._get_storage_path(agent_id, session_id)
            data = memory.to_dict()
            
            with open(storage_path, 'wb') as f:
                pickle.dump(data, f)
            
            logger.debug(f"Memory saved for agent {agent_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to save memory for {agent_id}: {e}")
            return False
    
    def load_memory(self, agent_id: str, session_id: str = "") -> Optional[AgentMemoryV2]:
        """Carrega memória do storage"""
        try:
            storage_path = self._get_storage_path(agent_id, session_id)
            
            if not os.path.exists(storage_path):
                return None
            
            with open(storage_path, 'rb') as f:
                data = pickle.load(f)
            
            memory = AgentMemoryV2.from_dict(data)
            logger.debug(f"Memory loaded for agent {agent_id}")
            return memory
        except Exception as e:
            logger.error(f"Failed to load memory for {agent_id}: {e}")
            return None
    
    def cleanup_old_memories(self, max_age_days: int = 30):
        """Remove memórias antigas"""
        try:
            cutoff_time = datetime.now() - timedelta(days=max_age_days)
            
            for filename in os.listdir(self.storage_dir):
                if filename.endswith('.pkl'):
                    file_path = os.path.join(self.storage_dir, filename)
                    file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                    
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        logger.debug(f"Removed old memory file: {filename}")
        except Exception as e:
            logger.error(f"Failed to cleanup old memories: {e}")

class PerformanceMonitor:
    """Monitor de performance avançado"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.metrics = PerformanceMetrics()
        self.response_times = deque(maxlen=100)  # Últimos 100 tempos
        self.lock = threading.Lock()
    
    def record_request(self, response_time: float, success: bool, tokens_used: int = 0):
        """Registra requisição"""
        with self.lock:
            self.response_times.append(response_time)
            self.metrics.total_requests += 1
            self.metrics.tokens_consumed += tokens_used
            self.metrics.last_request_time = datetime.now()
            
            if not success:
                self.metrics.total_errors += 1
            
            # Atualizar métricas derivadas
            self._update_derived_metrics()
    
    def _update_derived_metrics(self):
        """Atualiza métricas derivadas"""
        if self.response_times:
            self.metrics.response_time_avg = sum(self.response_times) / len(self.response_times)
            sorted_times = sorted(self.response_times)
            p95_index = int(len(sorted_times) * 0.95)
            self.metrics.response_time_p95 = sorted_times[p95_index] if sorted_times else 0.0
        
        if self.metrics.total_requests > 0:
            self.metrics.success_rate = ((self.metrics.total_requests - self.metrics.total_errors) / 
                                       self.metrics.total_requests) * 100
            self.metrics.error_rate = (self.metrics.total_errors / self.metrics.total_requests) * 100
        
        # Calcular RPM baseado nos últimos timestamps
        if self.metrics.last_request_time:
            minute_ago = datetime.now() - timedelta(minutes=1)
            recent_requests = sum(1 for _ in self.response_times)  # Simplificado
            self.metrics.requests_per_minute = recent_requests
    
    def get_health_status(self) -> Dict[str, Any]:
        """Retorna status de saúde"""
        with self.lock:
            health_score = 100.0
            issues = []
            
            # Verificar tempo de resposta
            if self.metrics.response_time_avg > 5.0:
                health_score -= 20
                issues.append("High response time")
            
            # Verificar taxa de erro
            if self.metrics.error_rate > 5.0:
                health_score -= 30
                issues.append("High error rate")
            
            # Verificar se está responsivo
            if (self.metrics.last_request_time and 
                (datetime.now() - self.metrics.last_request_time).total_seconds() > 300):
                health_score -= 10
                issues.append("No recent activity")
            
            status = "healthy" if health_score >= 80 else "degraded" if health_score >= 50 else "unhealthy"
            
            return {
                "status": status,
                "health_score": health_score,
                "issues": issues,
                "metrics": self.metrics.to_dict()
            }

class BaseAgentV2(ABC):
    """
    Classe base avançada para todos os agentes do GPT Mestre Autônomo v5.0
    
    Melhorias v2.0:
    - ✅ Persistência automática de memória
    - ✅ Rate limiting inteligente
    - ✅ Thread safety
    - ✅ Circuit breaker para auto-recovery
    - ✅ Performance monitoring avançado
    - ✅ Configuração flexível
    - ✅ Cache inteligente
    - ✅ Retry automático com backoff
    """
    
    def __init__(self, name: str, description: str = "", config: Optional[Dict] = None, **kwargs):
        # Identificação
        self.name = name
        self.description = description
        self.agent_id = f"{name}_{uuid.uuid4().hex[:8]}"
        self.session_id = kwargs.get("session_id", str(uuid.uuid4()))
        
        # Configuração
        self.config = self._load_config(config or {})
        
        # Sistemas robustos
        self.rate_limiter = RateLimiter(
            max_requests=self.config.get("rate_limit_per_minute", 60),
            burst_allowance=self.config.get("burst_allowance", 10)
        )
        
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=self.config.get("failure_threshold", 5),
            recovery_timeout=self.config.get("recovery_timeout", 30)
        )
        
        self.performance_monitor = PerformanceMonitor(self.name)
        
        # Memória persistente
        self.persistent_memory = self.config.get("persistent_memory", True)
        if self.persistent_memory:
            self.memory_manager = PersistentMemoryManager(
                storage_dir=self.config.get("memory_storage_dir", "memory/agents")
            )
            # Tentar carregar memória existente
            self.memory = self.memory_manager.load_memory(self.agent_id, self.session_id)
            if not self.memory:
                self.memory = AgentMemoryV2(session_id=self.session_id)
        else:
            self.memory = AgentMemoryV2(session_id=self.session_id)
            self.memory_manager = None
        
        # Thread safety
        self.execution_lock = threading.RLock()
        
        # LLM e configuração
        self.llm = None
        self.llm_available = False
        
        # Cache
        self.cache_enabled = self.config.get("cache_enabled", True)
        self.cache = {} if self.cache_enabled else None
        self.cache_ttl = self.config.get("cache_ttl_seconds", 300)  # 5 minutos
        
        # Estatísticas
        self.stats = {
            "agent_name": self.name,
            "agent_id": self.agent_id,
            "created_at": datetime.now(),
            "comandos_processados": 0,
            "tempo_medio": 0.0,
            "taxa_sucesso": 100.0,
            "agentes_usados": 0,
            "ultima_atividade": None
        }
        
        # Inicializar LLM se disponível
        self._inicializar_llm(**kwargs)
        
        logger.info(f"🤖 Agente {self.name} (Robustez v2.0) inicializado - ID: {self.agent_id}")
    
    def _load_config(self, config: Dict) -> Dict:
        """Carrega configuração com defaults"""
        default_config = {
            "rate_limit_per_minute": 60,
            "burst_allowance": 10,
            "failure_threshold": 5,
            "recovery_timeout": 30,
            "cache_enabled": True,
            "cache_ttl_seconds": 300,
            "persistent_memory": True,
            "memory_storage_dir": "memory/agents",
            "max_retry_attempts": 3,
            "retry_backoff_base": 2.0,
            "timeout_seconds": 30
        }
        
        # Merge com configuração fornecida
        merged_config = default_config.copy()
        merged_config.update(config)
        
        return merged_config
    
    def _inicializar_llm(self, **kwargs):
        """Inicializa LLM com fallback robusto"""
        try:
            # Tentar imports opcionais
            try:
                from langchain_anthropic import ChatAnthropic
                from langchain.schema import HumanMessage, AIMessage, SystemMessage
                LANGCHAIN_AVAILABLE = True
            except ImportError:
                LANGCHAIN_AVAILABLE = False
                logger.warning("LangChain não disponível - LLM não inicializado")
                return
            
            try:
                import config
                CONFIG_AVAILABLE = True
            except ImportError:
                CONFIG_AVAILABLE = False
                logger.warning("Config não disponível")
                return
            
            if LANGCHAIN_AVAILABLE and CONFIG_AVAILABLE and hasattr(config, 'ANTHROPIC_API_KEY'):
                self.llm = ChatAnthropic(
                    model=getattr(config, 'CLAUDE_MODEL', 'claude-3-sonnet-20241022'),
                    max_tokens=getattr(config, 'CLAUDE_MAX_TOKENS', 4096),
                    temperature=kwargs.get('temperature', 0.7),
                    anthropic_api_key=config.ANTHROPIC_API_KEY,
                )
                self.llm_available = True
                logger.info(f"LLM inicializado para {self.name}")
            else:
                logger.warning(f"LLM não configurado para {self.name}")
                
        except Exception as e:
            logger.error(f"Erro ao inicializar LLM para {self.name}: {e}")
            self.llm = None
            self.llm_available = False
    
    def _cache_key(self, input_text: str, context: Optional[Dict] = None) -> str:
        """Gera chave de cache"""
        cache_input = f"{input_text}_{json.dumps(context or {}, sort_keys=True)}"
        return hashlib.md5(cache_input.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Obtém item do cache"""
        if not self.cache_enabled or not self.cache:
            return None
        
        cache_item = self.cache.get(cache_key)
        if cache_item:
            cached_time, cached_data = cache_item
            if (datetime.now() - cached_time).total_seconds() < self.cache_ttl:
                logger.debug(f"Cache hit for {self.name}")
                return cached_data
            else:
                # Remove item expirado
                del self.cache[cache_key]
        
        return None
    
    def _set_cache(self, cache_key: str, data: Any):
        """Salva item no cache"""
        if self.cache_enabled and self.cache is not None:
            self.cache[cache_key] = (datetime.now(), data)
            logger.debug(f"Cache set for {self.name}")
    
    def _execute_with_retry(self, func: Callable, *args, **kwargs) -> Any:
        """Executa função com retry automático"""
        max_attempts = self.config.get("max_retry_attempts", 3)
        backoff_base = self.config.get("retry_backoff_base", 2.0)
        
        for attempt in range(max_attempts):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < max_attempts - 1:
                    wait_time = backoff_base ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed for {self.name}, retrying in {wait_time}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {max_attempts} attempts failed for {self.name}: {e}")
                    raise
    
    def processar(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        Método principal de processamento com robustez completa
        """
        start_time = time.time()
        success = False
        
        try:
            with self.execution_lock:
                # 1. Rate limiting
                if not self.rate_limiter.can_proceed():
                    wait_time = self.rate_limiter.wait_time()
                    logger.warning(f"Rate limit exceeded for {self.name}, waiting {wait_time:.1f}s")
                    time.sleep(min(wait_time, 10))  # Max 10s wait
                    
                    if not self.rate_limiter.can_proceed():
                        raise Exception("Rate limit still exceeded after waiting")
                
                # 2. Circuit breaker
                if not self.circuit_breaker.can_execute():
                    raise Exception("Circuit breaker is OPEN")
                
                # 3. Cache check
                cache_key = self._cache_key(mensagem, contexto)
                cached_result = self._get_from_cache(cache_key)
                if cached_result:
                    success = True
                    self.circuit_breaker.record_success()
                    return cached_result
                
                # 4. Adicionar à memória
                self.memory.add_message("user", mensagem, {"context": contexto})
                
                # 5. Processar com retry
                try:
                    resultado = self._execute_with_retry(self._processar_interno, mensagem, contexto)
                    success = True
                    
                    # 6. Salvar no cache
                    self._set_cache(cache_key, resultado)
                    
                    # 7. Adicionar resposta à memória
                    self.memory.add_message("assistant", resultado)
                    
                    # 8. Circuit breaker success
                    self.circuit_breaker.record_success()
                    
                    return resultado
                
                except Exception as e:
                    self.circuit_breaker.record_failure()
                    logger.error(f"Erro no processamento de {self.name}: {e}")
                    
                    # Fallback
                    resultado_fallback = self._fallback_response(mensagem, contexto)
                    self.memory.add_message("assistant", resultado_fallback, {"fallback": True})
                    return resultado_fallback
        
        finally:
            # 9. Métricas de performance
            response_time = time.time() - start_time
            self.performance_monitor.record_request(response_time, success)
            
            # 10. Atualizar estatísticas
            self._atualizar_stats(response_time, success)
            
            # 11. Salvar memória persistente
            if self.persistent_memory and self.memory_manager:
                self.memory_manager.save_memory(self.agent_id, self.memory, self.session_id)
    
    @abstractmethod
    def _processar_interno(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Método interno de processamento - deve ser implementado pelas subclasses"""
        pass
    
    def _fallback_response(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Resposta de fallback quando há erro"""
        return f"Desculpe, estou temporariamente indisponível. Por favor, tente novamente em alguns momentos."
    
    def _atualizar_stats(self, tempo_resposta: float, sucesso: bool):
        """Atualiza estatísticas do agente"""
        self.stats["comandos_processados"] += 1
        self.stats["ultima_atividade"] = datetime.now()
        
        # Tempo médio
        if self.stats["comandos_processados"] == 1:
            self.stats["tempo_medio"] = tempo_resposta
        else:
            self.stats["tempo_medio"] = (
                (self.stats["tempo_medio"] * (self.stats["comandos_processados"] - 1) + tempo_resposta) /
                self.stats["comandos_processados"]
            )
        
        # Taxa de sucesso
        if not sucesso:
            total_sucessos = (self.stats["comandos_processados"] - 1) * (self.stats["taxa_sucesso"] / 100)
            self.stats["taxa_sucesso"] = (total_sucessos / self.stats["comandos_processados"]) * 100
    
    def get_health_status(self) -> Dict[str, Any]:
        """Retorna status de saúde completo do agente"""
        health_data = self.performance_monitor.get_health_status()
        
        # Adicionar informações específicas do agente
        health_data.update({
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "circuit_breaker_state": self.circuit_breaker.state,
            "memory_items": len(self.memory.messages),
            "cache_items": len(self.cache) if self.cache else 0,
            "llm_available": self.llm_available,
            "stats": self.stats
        })
        
        return health_data
    
    def cleanup_resources(self):
        """Limpa recursos do agente"""
        if self.persistent_memory and self.memory_manager:
            self.memory_manager.save_memory(self.agent_id, self.memory, self.session_id)
            self.memory_manager.cleanup_old_memories()
        
        if self.cache:
            self.cache.clear()
        
        logger.info(f"Resources cleaned up for agent {self.name}")
    
    def reset_circuit_breaker(self):
        """Reset manual do circuit breaker"""
        with self.circuit_breaker.lock:
            self.circuit_breaker.state = "CLOSED"
            self.circuit_breaker.failure_count = 0
            self.circuit_breaker.last_failure_time = None
            logger.info(f"Circuit breaker reset for {self.name}")
    
    def update_config(self, new_config: Dict):
        """Atualiza configuração em runtime"""
        self.config.update(new_config)
        
        # Recriar rate limiter se necessário
        if any(key in new_config for key in ["rate_limit_per_minute", "burst_allowance"]):
            self.rate_limiter = RateLimiter(
                max_requests=self.config.get("rate_limit_per_minute", 60),
                burst_allowance=self.config.get("burst_allowance", 10)
            )
        
        logger.info(f"Configuration updated for {self.name}")

# Função utilitária para criar agente base robusto
def create_robust_agent(agent_class, name: str, description: str = "", **kwargs):
    """Cria agente com configuração robusta padrão"""
    robust_config = {
        "rate_limit_per_minute": 30,  # Conservador
        "burst_allowance": 5,
        "failure_threshold": 3,
        "recovery_timeout": 60,
        "cache_enabled": True,
        "cache_ttl_seconds": 600,  # 10 minutos
        "persistent_memory": True,
        "max_retry_attempts": 3
    }
    
    robust_config.update(kwargs.get("config", {}))
    kwargs["config"] = robust_config
    
    return agent_class(name=name, description=description, **kwargs)