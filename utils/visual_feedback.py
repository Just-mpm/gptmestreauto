"""
Sistema de Feedback Visual em ASCII - ETAPA 5
Implementa indicadores visuais criativos para terminal/console
Seguindo especificações Gemini AI para otimizar percepção de performance
"""

import time
import threading
import sys
import itertools
from typing import List, Dict, Optional, Callable
from datetime import datetime
from enum import Enum

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


class FeedbackType(Enum):
    """Tipos de feedback visual"""
    THINKING = "thinking"                    # Geral/Pensando
    API_CALL = "api_call"                   # Aguardando API LLM
    MEMORY_ACCESS = "memory_access"         # Buscando na memória
    AGENT_WORKING = "agent_working"         # Executando agente
    INITIALIZATION = "initialization"       # Inicialização do sistema
    LONG_OPERATION = "long_operation"       # Operação longa com etapas
    QUICK_RESPONSE = "quick_response"       # Resposta rápida
    ERROR = "error"                         # Erro crítico
    WARNING = "warning"                     # Erro de validação
    SUCCESS = "success"                     # Operação bem-sucedida


class VisualIndicator:
    """
    Indicador visual animado para terminal
    Implementa especificações Gemini de feedback criativo
    """
    
    def __init__(self, feedback_type: FeedbackType, message: str = "", 
                 duration: float = None):
        self.feedback_type = feedback_type
        self.message = message
        self.duration = duration
        self.is_running = False
        self.thread = None
        
        # Configurações de animação por tipo (Gemini specs)
        self.animations = {
            FeedbackType.THINKING: {
                "frames": ["🧠   ", "🧠 . ", "🧠 ..", "🧠 ..."],
                "interval": 0.5,
                "prefix": "🧠 Pensando",
                "suffix": ""
            },
            
            FeedbackType.API_CALL: {
                "frames": ["⚡   API", "⚡ . API", "⚡ ..API", "⚡ ...API"],
                "interval": 0.4,
                "prefix": "⚡ Consultando Claude",
                "suffix": ""
            },
            
            FeedbackType.MEMORY_ACCESS: {
                "frames": ["📖   ", "📖 . ", "📖 ..", "📖 ..."],
                "interval": 0.3,
                "prefix": "📖 Acessando memória",
                "suffix": ""
            },
            
            FeedbackType.AGENT_WORKING: {
                "frames": ["⚙️   ", "⚙️ . ", "⚙️ ..", "⚙️ ..."],
                "interval": 0.4,
                "prefix": "⚙️ Agente trabalhando",
                "suffix": ""
            },
            
            FeedbackType.QUICK_RESPONSE: {
                "frames": ["✨"],
                "interval": 0.1,
                "prefix": "✨",
                "suffix": "",
                "single_shot": True
            },
            
            FeedbackType.SUCCESS: {
                "frames": ["✅"],
                "interval": 0.1,
                "prefix": "✅",
                "suffix": "",
                "single_shot": True
            }
        }
    
    def start(self):
        """Inicia animação"""
        if self.is_running:
            return
        
        self.is_running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Para animação"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=1.0)
        
        # Limpar linha
        self._clear_line()
    
    def _animate(self):
        """Loop de animação"""
        config = self.animations.get(self.feedback_type, self.animations[FeedbackType.THINKING])
        frames = config["frames"]
        interval = config["interval"]
        prefix = config.get("prefix", "")
        is_single_shot = config.get("single_shot", False)
        
        if is_single_shot:
            # Mostrar uma vez e sair
            display_text = f"\r{prefix} {self.message}"
            print(display_text, end="", flush=True)
            time.sleep(interval)
            return
        
        # Animação contínua
        frame_cycle = itertools.cycle(frames)
        start_time = time.time()
        
        while self.is_running:
            if self.duration and (time.time() - start_time) > self.duration:
                break
            
            frame = next(frame_cycle)
            display_text = f"\r{frame} {prefix}"
            if self.message:
                display_text += f": {self.message}"
            
            print(display_text, end="", flush=True)
            time.sleep(interval)
    
    def _clear_line(self):
        """Limpa linha atual"""
        print("\r" + " " * 80 + "\r", end="", flush=True)


class ProgressBar:
    """
    Barra de progresso ASCII para inicialização
    Implementa especificação Gemini para operações longas
    """
    
    def __init__(self, total_steps: int, width: int = 20):
        self.total_steps = total_steps
        self.current_step = 0
        self.width = width
        self.start_time = time.time()
        
    def update(self, step: int, message: str = ""):
        """Atualiza progresso"""
        self.current_step = step
        percentage = (step / self.total_steps) * 100
        filled = int(self.width * step / self.total_steps)
        empty = self.width - filled
        
        bar = "=" * filled + " " * empty
        elapsed = time.time() - self.start_time
        
        display = f"\r[{bar}] {percentage:5.1f}% {message}"
        print(display, end="", flush=True)
        
        if step >= self.total_steps:
            print()  # Nova linha ao completar
    
    def complete(self, final_message: str = "Concluído!"):
        """Completa barra de progresso"""
        self.update(self.total_steps, final_message)


class MultiStageProgress:
    """
    Indicador de progresso multi-etapas para operações complexas
    Implementa especificação Gemini para Oráculo e DeepAgent
    """
    
    def __init__(self, stages: List[str]):
        self.stages = stages
        self.current_stage = 0
        self.total_stages = len(stages)
        
    def next_stage(self, custom_message: str = None):
        """Avança para próxima etapa"""
        if self.current_stage < self.total_stages:
            stage_num = self.current_stage + 1
            stage_message = custom_message or self.stages[self.current_stage]
            
            print(f"\r⏳ ({stage_num}/{self.total_stages}) {stage_message}...", end="", flush=True)
            self.current_stage += 1
            
            time.sleep(0.5)  # Pequena pausa para visibilidade
    
    def complete(self, final_message: str = "Processo concluído!"):
        """Finaliza progresso multi-etapas"""
        print(f"\r🌟 {final_message}")


class ErrorDisplay:
    """
    Sistema de exibição de erros com personalidade
    Implementa especificação Gemini para respostas de erro amigáveis
    """
    
    @staticmethod
    def show_critical_error(error_message: str = ""):
        """Erro crítico/inesperado"""
        error_display = """
🚨 OOPS! Algo deu muito errado. 🚨
Carlos: "Sinto muito, tive um pequeno curto-circuito cerebral. 
Por favor, tente novamente ou verifique os logs."
        """.strip()
        
        if error_message:
            error_display += f"\n\n💡 Detalhes técnicos: {error_message}"
        
        print(f"\n{error_display}\n")
    
    @staticmethod
    def show_validation_error(user_input: str = ""):
        """Erro de validação (entrada inválida)"""
        error_display = """
⚠️ Entendi errado. ⚠️
Carlos: "Parece que sua solicitação não está clara. 
Poderia reformular ou me dar mais detalhes?"
        """.strip()
        
        if user_input:
            error_display += f"\n\n💭 Você disse: '{user_input}'"
        
        print(f"\n{error_display}\n")
    
    @staticmethod
    def show_timeout_error(agent_name: str = ""):
        """Timeout com personalidade do Carlos"""
        timeout_messages = [
            "Hmm, parece que um dos meus assistentes está meditando profundamente. Ele vai voltar em breve, por favor, tente novamente em um minuto.",
            "A conexão com o mundo exterior (ou talvez um agente pensador demais) demorou a responder. Tente de novo, a paciência é uma virtude digital!",
            "Ops! Um dos agentes ficou filosofando demais. Vamos tentar de novo?"
        ]
        
        import random
        message = random.choice(timeout_messages)
        
        if agent_name:
            message = message.replace("um dos meus assistentes", f"o {agent_name}")
            message = message.replace("um agente", f"o {agent_name}")
        
        print(f"\n⏰ Carlos: \"{message}\"\n")
    
    @staticmethod  
    def show_api_error():
        """Erro de API com explicação amigável"""
        api_messages = [
            "Oops! Houve um pequeno contratempo na comunicação com meus servidores de conhecimento (API). Pode ser algo temporário, por favor, me dê outra chance.",
            "Parece que a ponte para a internet está com problemas. Não se preocupe, estou investigando! Tente de novo em instantes.",
            "Houston, temos um problema! A conexão com o espaço digital falhou. Mas já estou trabalhando na solução!"
        ]
        
        import random
        message = random.choice(api_messages)
        
        print(f"\n🔌 Carlos: \"{message}\"\n")
    
    @staticmethod
    def show_overload_error():
        """Sistema sobrecarregado"""
        overload_messages = [
            "Puxa, estou com muitos pensamentos na cabeça agora! Minha capacidade está no limite. Poderíamos tentar uma pergunta mais simples ou voltar em alguns minutos?",
            "Estou recebendo muitas requisições neste momento. Para garantir que eu responda com qualidade, sugiro que tente com uma solicitação menos complexa ou espere um pouco.",
            "Meu cérebro digital está no limite! Que tal uma pergunta mais leve enquanto me organizo?"
        ]
        
        import random
        message = random.choice(overload_messages)
        
        print(f"\n🧠💥 Carlos: \"{message}\"\n")


class VisualFeedbackManager:
    """
    Gerenciador central de feedback visual
    Coordena todos os tipos de indicadores visuais
    """
    
    def __init__(self):
        self.active_indicators: Dict[str, VisualIndicator] = {}
        self.feedback_history: List[Dict] = []
        
        logger.info("🎨 VisualFeedbackManager inicializado")
    
    def show_thinking(self, message: str = "Analisando sua solicitação"):
        """Mostra indicador de pensamento geral"""
        return self._start_indicator("thinking", FeedbackType.THINKING, message)
    
    def show_api_call(self, message: str = "Consultando inteligência artificial"):
        """Mostra indicador de chamada à API"""
        return self._start_indicator("api_call", FeedbackType.API_CALL, message)
    
    def show_memory_access(self, message: str = "Consultando memória"):
        """Mostra indicador de acesso à memória"""
        return self._start_indicator("memory_access", FeedbackType.MEMORY_ACCESS, message)
    
    def show_agent_working(self, agent_name: str, task: str = "processando"):
        """Mostra indicador de agente trabalhando"""
        message = f"{agent_name} {task}"
        return self._start_indicator("agent_working", FeedbackType.AGENT_WORKING, message)
    
    def show_quick_response(self, message: str = ""):
        """Mostra indicador de resposta rápida"""
        indicator = VisualIndicator(FeedbackType.QUICK_RESPONSE, message)
        indicator.start()
        time.sleep(0.2)
        indicator.stop()
        return indicator
    
    def show_success(self, message: str = ""):
        """Mostra indicador de sucesso"""
        indicator = VisualIndicator(FeedbackType.SUCCESS, message)
        indicator.start() 
        time.sleep(0.3)
        indicator.stop()
        return indicator
    
    def show_initialization(self, steps: List[str]) -> ProgressBar:
        """Mostra barra de progresso de inicialização"""
        print("\nGPTMA V5.0 Inicializando...")
        progress = ProgressBar(len(steps))
        
        for i, step in enumerate(steps):
            progress.update(i + 1, step)
            time.sleep(0.3)  # Simular tempo de carregamento
        
        return progress
    
    def show_long_operation(self, agent_name: str, stages: List[str]) -> MultiStageProgress:
        """Mostra progresso de operação longa com etapas"""
        print(f"\n🌟 {agent_name}: Iniciando processo...")
        return MultiStageProgress(stages)
    
    def stop_indicator(self, indicator_id: str):
        """Para indicador específico"""
        if indicator_id in self.active_indicators:
            self.active_indicators[indicator_id].stop()
            del self.active_indicators[indicator_id]
    
    def stop_all_indicators(self):
        """Para todos os indicadores ativos"""
        for indicator in self.active_indicators.values():
            indicator.stop()
        self.active_indicators.clear()
    
    def _start_indicator(self, indicator_id: str, feedback_type: FeedbackType, 
                        message: str) -> VisualIndicator:
        """Inicia indicador e adiciona ao gerenciamento"""
        # Parar indicador anterior se existir
        if indicator_id in self.active_indicators:
            self.active_indicators[indicator_id].stop()
        
        # Criar e iniciar novo indicador
        indicator = VisualIndicator(feedback_type, message)
        self.active_indicators[indicator_id] = indicator
        indicator.start()
        
        # Adicionar ao histórico
        self.feedback_history.append({
            "timestamp": datetime.now(),
            "type": feedback_type.value,
            "message": message,
            "indicator_id": indicator_id
        })
        
        return indicator
    
    def get_feedback_stats(self) -> Dict:
        """Retorna estatísticas de feedback"""
        type_counts = {}
        for entry in self.feedback_history:
            type_name = entry["type"]
            type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        return {
            "total_feedbacks": len(self.feedback_history),
            "active_indicators": len(self.active_indicators),
            "type_distribution": type_counts
        }


# Singleton global
_feedback_manager_instance = None


def get_visual_feedback_manager() -> VisualFeedbackManager:
    """Retorna instância singleton do VisualFeedbackManager"""
    global _feedback_manager_instance
    
    if _feedback_manager_instance is None:
        _feedback_manager_instance = VisualFeedbackManager()
    
    return _feedback_manager_instance


# Context manager para feedback automático
class FeedbackContext:
    """Context manager para feedback visual automático"""
    
    def __init__(self, feedback_type: str, message: str = ""):
        self.feedback_type = feedback_type
        self.message = message
        self.manager = get_visual_feedback_manager()
        self.indicator = None
    
    def __enter__(self):
        # Mapear tipos para métodos
        method_map = {
            "thinking": self.manager.show_thinking,
            "api_call": self.manager.show_api_call,
            "memory_access": self.manager.show_memory_access,
            "agent_working": self.manager.show_agent_working
        }
        
        method = method_map.get(self.feedback_type, self.manager.show_thinking)
        self.indicator = method(self.message)
        return self.indicator
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.indicator:
            self.indicator.stop()


# Teste do sistema
if __name__ == "__main__":
    print("🧪 TESTE DO SISTEMA DE FEEDBACK VISUAL")
    print("=" * 60)
    
    manager = get_visual_feedback_manager()
    
    # Teste 1: Indicadores básicos
    print("\n1. 🧠 Teste de Pensamento (3s)")
    indicator = manager.show_thinking("Analisando sua solicitação")
    time.sleep(3)
    indicator.stop()
    
    print("\n2. ⚡ Teste de API Call (2s)")
    indicator = manager.show_api_call("Consultando Claude")
    time.sleep(2)
    indicator.stop()
    
    print("\n3. 📖 Teste de Memória (2s)")
    indicator = manager.show_memory_access("Buscando informações anteriores")
    time.sleep(2)
    indicator.stop()
    
    print("\n4. ⚙️ Teste de Agente (2s)")
    indicator = manager.show_agent_working("Oráculo", "deliberando")
    time.sleep(2)
    indicator.stop()
    
    # Teste 2: Respostas rápidas
    print("\n5. ✨ Teste de Resposta Rápida")
    manager.show_quick_response("Comando processado")
    
    print("\n6. ✅ Teste de Sucesso")
    manager.show_success("Operação concluída")
    
    # Teste 3: Barra de progresso
    print("\n7. 📊 Teste de Inicialização")
    steps = ["Carregando Módulos", "Ativando Agentes", "Conectando APIs", "Sistema Pronto"]
    progress = manager.show_initialization(steps)
    
    # Teste 4: Operação multi-etapas
    print("\n8. 🌟 Teste de Operação Longa")
    stages = ["Coletando informações", "Analisando dados", "Chegando a uma conclusão"]
    multi_progress = manager.show_long_operation("Oráculo", stages)
    
    for stage in stages:
        multi_progress.next_stage()
        time.sleep(1)
    
    multi_progress.complete("Deliberação concluída!")
    
    # Teste 5: Erros com personalidade
    print("\n9. 🚨 Teste de Erros")
    
    print("\n📌 Erro Crítico:")
    ErrorDisplay.show_critical_error("Conexão perdida")
    
    print("📌 Erro de Validação:")
    ErrorDisplay.show_validation_error("comando inválido")
    
    print("📌 Timeout:")
    ErrorDisplay.show_timeout_error("Oráculo")
    
    print("📌 Erro de API:")
    ErrorDisplay.show_api_error()
    
    print("📌 Sistema Sobrecarregado:")
    ErrorDisplay.show_overload_error()
    
    # Teste 6: Context Manager
    print("\n10. 🔄 Teste de Context Manager")
    with FeedbackContext("thinking", "Processando com context manager"):
        time.sleep(2)
        print("\r✅ Processamento concluído com context manager!")
    
    # Estatísticas
    stats = manager.get_feedback_stats()
    print(f"\n📊 ESTATÍSTICAS DE FEEDBACK:")
    print(f"   Total de feedbacks: {stats['total_feedbacks']}")
    print(f"   Indicadores ativos: {stats['active_indicators']}")
    print(f"   Distribuição por tipo: {stats['type_distribution']}")
    
    print(f"\n✅ TESTE CONCLUÍDO - Sistema de feedback visual funcionando!")