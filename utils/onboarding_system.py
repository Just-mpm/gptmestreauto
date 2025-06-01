"""
Sistema de Onboarding de 3 Passos - ETAPA 5
Implementa introdução amigável e envolvente para novos usuários
Seguindo especificações Gemini AI para reduzir interações redundantes
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
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


@dataclass
class OnboardingStep:
    """Passo do onboarding"""
    step_number: int
    title: str
    message: str
    feedback_visual: str
    expected_responses: List[str]
    next_step_trigger: List[str]
    help_text: Optional[str] = None


class OnboardingManager:
    """
    Gerenciador de Onboarding para Novos Usuários
    Implementa fluxo de 3 passos seguindo especificações Gemini
    """
    
    def __init__(self, data_dir: str = "data/onboarding"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Estado do onboarding
        self.current_step = 0
        self.is_active = False
        self.user_responses = []
        self.completed_users = set()
        
        # Definir os 3 passos (Gemini specs)
        self.onboarding_steps = self._create_onboarding_steps()
        
        # Carregar usuários que já completaram
        self._load_completed_users()
        
        logger.info("👋 OnboardingManager inicializado com 3 passos Gemini")
    
    def _create_onboarding_steps(self) -> List[OnboardingStep]:
        """Cria os 3 passos do onboarding conforme especificações Gemini"""
        
        return [
            # Passo 1: Bem-Vindo ao GPTMA! (Apresentação do Carlos)
            OnboardingStep(
                step_number=1,
                title="Bem-Vindo ao GPT Mestre Autônomo!",
                message="""👋 **Olá! Eu sou Carlos, o maestro do GPT Mestre Autônomo.**

🎯 **Minha missão** é te ajudar a desvendar o potencial da IA. Estou aqui para te guiar e coordenar nossa equipe de agentes especializados.

🚀 **Juntos, podemos**:
• Analisar mercados e produtos
• Criar conteúdo e estratégias  
• Tomar decisões complexas
• Oferecer suporte personalizado
• E muito mais!

✨ **Pronto para começar essa jornada?**

👇 *Digite "Sim" para continuar ou "Me fale mais" para saber detalhes*""",
                feedback_visual="👋",
                expected_responses=["sim", "s", "yes", "vamos", "pronto", "ok"],
                next_step_trigger=["sim", "s", "yes", "vamos", "pronto", "ok", "me fale mais", "mais detalhes", "explique"],
                help_text="💡 Dica: Você pode responder 'Sim' para começar ou 'Me fale mais' para detalhes"
            ),
            
            # Passo 2: O Que Você Pode Fazer? (Exemplos e Capacidades) 
            OnboardingStep(
                step_number=2,
                title="O Que Você Pode Fazer?",
                message="""💡 **Ótimo! Você pode me pedir para**:

🔍 **Análise e Pesquisa**:
• *"Analise meu produto X"* → Chamo o DeepAgent e ScoutAI para pesquisa completa
• *"Pesquise sobre o mercado Y"* → Busca detalhada com dados atualizados

🎨 **Criação de Conteúdo**:
• *"Crie um prompt de vendas"* → PromptCrafter entra em ação!
• *"Gere uma estratégia de marketing"* → AutoMaster desenvolve plano completo

💭 **Suporte Pessoal**:
• *"Me ajude com um problema pessoal"* → PsyMind está pronto para apoiar
• *"Preciso tomar uma decisão difícil"* → Oráculo oferece análise profunda

⚙️ **Comandos Práticos**:
• *"Carlos, qual o status?"* → Vejo como estou funcionando
• *"Carlos, quem está por aí?"* → Lista todos os agentes disponíveis

🎯 **Para uma visão geral completa, diga**: *"Carlos, quem está por aí?"*

💬 *Agora, que tal tentar um comando? Digite algo que gostaria de fazer!*""",
                feedback_visual="💡",
                expected_responses=["entendi", "ok", "vamos testar", "quero tentar", "carlos, quem está por aí?"],
                next_step_trigger=["entendi", "ok", "vamos", "tentar", "teste", "comando", "carlos"],
                help_text="💡 Dica: Tente algum comando como 'Carlos, quem está por aí?' ou me peça algo específico"
            ),
            
            # Passo 3: Dicas Rápidas e Ajuda (Otimização da Interação)
            OnboardingStep(
                step_number=3,
                title="Dicas Finais para Otimizar sua Experiência",
                message="""📚 **Lembre-se dessas dicas importantes**:

🎯 **Para melhores resultados**:
• **Seja claro e específico** → Quanto mais claro você for, melhor e mais rápido eu te ajudarei
• **Use comandos naturais** → Fale comigo como falaria com um assistente humano
• **Aproveite a economia** → Comandos como "status" e "ajuda" não gastam sua cota!

🆘 **Se precisar de ajuda**:
• Diga *"Carlos, me ajuda!"* → Orientação rápida sobre qualquer tópico
• Diga *"Carlos, me ajuda com comandos"* → Lista completa de comandos especiais

📊 **Monitoramento inteligente**:
• *"Carlos, quanto gastei hoje?"* → Vejo seu uso de cota em tempo real
• *"Carlos, seja mais conciso"* → Ajusto meu estilo para economizar

🌟 **Estou sempre aprendendo!** Seu feedback é muito valioso para minha evolução.

🚀 **Agora me diga: como posso te ajudar hoje?**

*Digite sua primeira pergunta ou tarefa real para começarmos!*""",
                feedback_visual="🚀",
                expected_responses=["entendi", "perfeito", "vamos começar", "preciso de", "me ajude", "analise", "crie"],
                next_step_trigger=["qualquer_resposta"],  # Qualquer resposta finaliza
                help_text="💡 Agora você está pronto! Faça sua primeira pergunta ou tarefa real."
            )
        ]
    
    def should_start_onboarding(self, user_id: str = "default") -> bool:
        """Verifica se deve iniciar onboarding para usuário"""
        if user_id in self.completed_users:
            return False
        
        # Verificar se é primeira execução ou comando explícito
        return not self._has_user_data(user_id)
    
    def start_onboarding(self, user_id: str = "default") -> str:
        """Inicia processo de onboarding"""
        if user_id in self.completed_users:
            return self._get_returning_user_message()
        
        self.is_active = True
        self.current_step = 1
        self.user_responses = []
        
        logger.info(f"👋 Iniciando onboarding para usuário {user_id}")
        
        return self._get_current_step_message()
    
    def process_onboarding_response(self, user_response: str, user_id: str = "default") -> Tuple[str, bool]:
        """
        Processa resposta do usuário no onboarding
        Retorna (mensagem_resposta, onboarding_completo)
        """
        if not self.is_active:
            return "", False
        
        user_response = user_response.lower().strip()
        self.user_responses.append(user_response)
        
        current_step_data = self.onboarding_steps[self.current_step - 1]
        
        # Verificar se resposta pode avançar para próximo passo
        should_advance = self._should_advance_step(user_response, current_step_data)
        
        if should_advance:
            if self.current_step >= len(self.onboarding_steps):
                # Onboarding completo
                self.is_active = False
                self.completed_users.add(user_id)
                self._save_completion(user_id)
                
                completion_message = self._get_completion_message()
                logger.info(f"✅ Onboarding completo para usuário {user_id}")
                
                return completion_message, True
            else:
                # Avançar para próximo passo
                self.current_step += 1
                return self._get_current_step_message(), False
        else:
            # Dar uma resposta de encorajamento ou reorientação
            return self._get_encouragement_message(current_step_data), False
    
    def force_complete_onboarding(self, user_id: str = "default"):
        """Força conclusão do onboarding (para usuários experientes)"""
        self.is_active = False
        self.completed_users.add(user_id)
        self._save_completion(user_id)
        logger.info(f"⏭️ Onboarding pulado para usuário {user_id}")
    
    def reset_onboarding(self, user_id: str = "default"):
        """Reseta onboarding para usuário"""
        self.completed_users.discard(user_id)
        self.is_active = False
        self.current_step = 0
        self.user_responses = []
        
        # Remover arquivo de completion
        completion_file = self.data_dir / f"completed_{user_id}.json"
        if completion_file.exists():
            completion_file.unlink()
        
        logger.info(f"🔄 Onboarding resetado para usuário {user_id}")
    
    def _get_current_step_message(self) -> str:
        """Retorna mensagem do passo atual"""
        if self.current_step > len(self.onboarding_steps):
            return ""
        
        step_data = self.onboarding_steps[self.current_step - 1]
        
        # Formatar mensagem com visual
        message = f"""{step_data.feedback_visual} **Passo {step_data.step_number}/3: {step_data.title}**

{step_data.message}"""
        
        return message
    
    def _should_advance_step(self, user_response: str, step_data: OnboardingStep) -> bool:
        """Verifica se deve avançar para próximo passo"""
        
        # Passo 3: qualquer resposta finaliza
        if step_data.step_number == 3:
            return True
        
        # Verificar triggers específicos
        for trigger in step_data.next_step_trigger:
            if trigger == "qualquer_resposta":
                return True
            if trigger in user_response:
                return True
        
        # Verificar respostas esperadas
        for expected in step_data.expected_responses:
            if expected in user_response:
                return True
        
        return False
    
    def _get_encouragement_message(self, step_data: OnboardingStep) -> str:
        """Retorna mensagem de encorajamento quando resposta não avança"""
        
        encouragements = {
            1: [
                "😊 Sem pressa! Você pode responder 'Sim' para começar ou 'Me fale mais' se quiser detalhes.",
                "🤔 Que tal responder 'Sim' para continuarmos? Ou diga 'Me fale mais' se tiver dúvidas!",
                "💭 Estou aguardando! Digite 'Sim' para prosseguir ou 'Me fale mais' para saber mais."
            ],
            2: [
                "🎯 Que tal tentar um comando? Digite algo como 'Carlos, quem está por aí?' ou me peça algo que gostaria de fazer!",
                "💡 Experimente! Você pode dizer 'Carlos, status' ou fazer uma pergunta sobre algo que te interessa.",
                "🚀 Vamos praticar! Tente algum comando natural ou me peça para fazer algo específico."
            ],
            3: [
                "🌟 Perfeito! Agora é só me fazer sua primeira pergunta real. O que gostaria de saber ou fazer?",
                "✨ Você está pronto! Me diga: como posso te ajudar hoje?",
                "🎊 Ótimo! Agora me faça qualquer pergunta ou peça qualquer tarefa."
            ]
        }
        
        import random
        step_encouragements = encouragements.get(step_data.step_number, ["😊 Continue seguindo as instruções!"])
        message = random.choice(step_encouragements)
        
        if step_data.help_text:
            message += f"\n\n{step_data.help_text}"
        
        return message
    
    def _get_completion_message(self) -> str:
        """Mensagem de conclusão do onboarding"""
        return """🎉 **Parabéns! Onboarding Completo!**

✅ **Você agora conhece**:
• Como falar comigo naturalmente
• Quais agentes estão disponíveis  
• Como otimizar sua experiência
• Comandos que economizam cota

🚀 **Estou pronto para ser seu assistente de IA!**

🎯 **Vamos começar de verdade? Me diga como posso te ajudar hoje!**

*A partir de agora, todas as suas interações serão processadas normalmente pelos agentes especializados.*"""
    
    def _get_returning_user_message(self) -> str:
        """Mensagem para usuário que já completou onboarding"""
        return """👋 **Oi! Que bom te ver novamente!**

✅ Você já conhece o sistema, então vamos direto ao que interessa.

🚀 **Como posso te ajudar hoje?**

💡 *Dica: Se quiser revisar os comandos, diga "Carlos, me ajuda com comandos"*"""
    
    def _has_user_data(self, user_id: str) -> bool:
        """Verifica se usuário já tem dados salvos"""
        completion_file = self.data_dir / f"completed_{user_id}.json"
        return completion_file.exists()
    
    def _save_completion(self, user_id: str):
        """Salva conclusão do onboarding"""
        try:
            completion_data = {
                "user_id": user_id,
                "completed_at": datetime.now().isoformat(),
                "steps_completed": len(self.onboarding_steps),
                "responses": self.user_responses
            }
            
            completion_file = self.data_dir / f"completed_{user_id}.json"
            with open(completion_file, "w") as f:
                json.dump(completion_data, f, indent=2)
                
        except Exception as e:
            logger.error(f"Erro ao salvar completion do onboarding: {e}")
    
    def _load_completed_users(self):
        """Carrega lista de usuários que completaram onboarding"""
        try:
            for file_path in self.data_dir.glob("completed_*.json"):
                try:
                    with open(file_path, "r") as f:
                        data = json.load(f)
                        self.completed_users.add(data["user_id"])
                except Exception as e:
                    logger.warning(f"Erro ao carregar {file_path}: {e}")
                    
        except Exception as e:
            logger.debug(f"Erro ao carregar usuários completados: {e}")
    
    def get_onboarding_stats(self) -> Dict:
        """Retorna estatísticas do onboarding"""
        return {
            "total_steps": len(self.onboarding_steps),
            "current_step": self.current_step,
            "is_active": self.is_active,
            "completed_users": len(self.completed_users),
            "responses_this_session": len(self.user_responses)
        }


# Singleton global
_onboarding_manager_instance = None


def get_onboarding_manager() -> OnboardingManager:
    """Retorna instância singleton do OnboardingManager"""
    global _onboarding_manager_instance
    
    if _onboarding_manager_instance is None:
        _onboarding_manager_instance = OnboardingManager()
    
    return _onboarding_manager_instance


# Função helper para integração fácil
def check_and_start_onboarding(user_id: str = "default") -> Optional[str]:
    """
    Verifica se deve iniciar onboarding e retorna mensagem inicial
    Retorna None se não precisa de onboarding
    """
    manager = get_onboarding_manager()
    
    if manager.should_start_onboarding(user_id):
        return manager.start_onboarding(user_id)
    
    return None


def process_message_with_onboarding(message: str, user_id: str = "default") -> Tuple[Optional[str], bool]:
    """
    Processa mensagem considerando onboarding ativo
    Retorna (resposta_onboarding, deve_processar_normalmente)
    """
    manager = get_onboarding_manager()
    
    if manager.is_active:
        response, completed = manager.process_onboarding_response(message, user_id)
        return response, completed  # Se completed=True, pode processar normalmente depois
    
    # Verificar se é comando para iniciar onboarding
    if any(keyword in message.lower() for keyword in ["me ajude a começar", "como usar", "tutorial", "onboarding"]):
        return manager.start_onboarding(user_id), False
    
    return None, True  # Não está em onboarding, processar normalmente


# Teste do sistema
if __name__ == "__main__":
    print("🧪 TESTE DO SISTEMA DE ONBOARDING")
    print("=" * 60)
    
    manager = get_onboarding_manager()
    test_user = "test_user"
    
    # Reset para teste
    manager.reset_onboarding(test_user)
    
    print("1. 👋 Iniciando onboarding...")
    initial_message = manager.start_onboarding(test_user)
    print(f"\n{initial_message}\n")
    
    # Simular respostas do usuário
    test_responses = [
        "sim",  # Passo 1 -> 2
        "vamos testar",  # Passo 2 -> 3  
        "entendi, me ajude com análise de mercado"  # Passo 3 -> Completo
    ]
    
    for i, response in enumerate(test_responses, 1):
        print(f"👤 Usuário responde: '{response}'")
        
        reply, completed = manager.process_onboarding_response(response, test_user)
        print(f"\n🤖 Carlos: {reply}\n")
        
        if completed:
            print("✅ ONBOARDING CONCLUÍDO!")
            break
        else:
            print(f"➡️ Avançando para próximo passo...")
    
    # Teste com usuário que já completou
    print("\n2. 🔄 Testando usuário que já completou...")
    returning_message = manager.start_onboarding(test_user)
    print(f"\n{returning_message}\n")
    
    # Teste de helpers
    print("3. 🔧 Testando funções helper...")
    
    new_user = "new_user"
    onboarding_check = check_and_start_onboarding(new_user)
    if onboarding_check:
        print(f"✅ Onboarding necessário para {new_user}")
        print(f"📝 Mensagem: {onboarding_check[:100]}...")
    
    # Estadísticas
    stats = manager.get_onboarding_stats()
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de passos: {stats['total_steps']}")
    print(f"   Usuários completos: {stats['completed_users']}")
    print(f"   Onboarding ativo: {stats['is_active']}")
    
    print(f"\n✅ TESTE CONCLUÍDO - Sistema de onboarding funcionando!")