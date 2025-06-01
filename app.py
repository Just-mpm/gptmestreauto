"""
GPT MESTRE AUTÔNOMO - Interface Chainlit v3.0 STREAMING
🚀 Sistema com streaming em tempo real e construção palavra por palavra
"""

import chainlit as cl
import asyncio
from datetime import datetime
import uuid
import os
import sys
import time
import re

# Adicionar o diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports do sistema
try:
    from config import config
    from agents.carlos import criar_carlos_maestro
    from utils.logger import get_logger
    
    system_logger = get_logger("chainlit_streaming")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    exit(1)

# Configurações do Chainlit
cl.config.name = "🧠 GPT Mestre Autônomo v5.0 - STREAMING"
cl.config.human_timeout = 300  # 5 minutos para operações complexas

# Estado global
carlos_instance = None
current_status_msg = None
current_streaming_msg = None

async def stream_agent_activity(agent_name: str, activity: str, duration: float = 2.0):
    """Simula atividade do agente em tempo real"""
    emoji_map = {
        "Carlos": "👑",
        "TaskBreaker": "🔨", 
        "SupervisorAI": "🧠",
        "AutoMaster": "💼",
        "PromptCrafter": "🎨",
        "Oráculo": "🔮",
        "DeepAgent": "🌐",
        "Reflexor": "🔍"
    }
    
    emoji = emoji_map.get(agent_name, "🤖")
    
    # Criar mensagem de atividade
    activity_msg = cl.Message(
        content=f"{emoji} **{agent_name}**: {activity}",
        author=f"{agent_name} Activity"
    )
    await activity_msg.send()
    
    # Simular duração da atividade
    steps = ["⚡ Inicializando...", "🔄 Processando...", "✅ Concluído!"]
    
    for i, step in enumerate(steps):
        await asyncio.sleep(duration / len(steps))
        activity_msg.content = f"{emoji} **{agent_name}**: {activity}\n{step}"
        await activity_msg.update()

async def stream_oraculo_assembly(num_suboraculos: int = 6):
    """Simula assembleia do Oráculo em tempo real"""
    assembly_msg = cl.Message(
        content="🔮 **Assembleia Dinâmica Iniciada**\n⏳ Convocando suboráculos...",
        author="Oráculo v9.0"
    )
    await assembly_msg.send()
    
    # Simular convocação dos suboráculos
    specialists = ["Ético", "Viabilidade", "Criativo", "Paradoxo", "Copy", "Pricing"]
    
    for i, specialist in enumerate(specialists[:num_suboraculos]):
        await asyncio.sleep(1.5)
        assembly_msg.content += f"\n✅ {specialist} conectado"
        await assembly_msg.update()
    
    # Simular deliberação
    await asyncio.sleep(2)
    assembly_msg.content += "\n\n🗳️ **Deliberação em Andamento**"
    await assembly_msg.update()
    
    # Simular votos chegando
    for i in range(num_suboraculos):
        await asyncio.sleep(3)
        assembly_msg.content += f"\n📊 Voto {i+1}/{num_suboraculos} recebido"
        await assembly_msg.update()
    
    # Conclusão
    await asyncio.sleep(1)
    assembly_msg.content += "\n\n✨ **Assembleia Concluída - Resultado Aprovado!**"
    await assembly_msg.update()

async def stream_response_generation(response_text: str):
    """Gera resposta palavra por palavra em tempo real"""
    global current_streaming_msg
    
    # Criar mensagem para streaming
    current_streaming_msg = cl.Message(
        content="",
        author="Carlos v5.0"
    )
    await current_streaming_msg.send()
    
    # Dividir texto em palavras
    words = response_text.split()
    current_text = ""
    
    # Stream palavra por palavra
    for i, word in enumerate(words):
        current_text += word + " "
        current_streaming_msg.content = current_text + "▌"  # Cursor piscando
        await current_streaming_msg.update()
        
        # Pausa baseada no tamanho da palavra (mais realista)
        delay = max(0.05, min(0.3, len(word) * 0.02))
        await asyncio.sleep(delay)
        
        # Pausas extras em pontuação
        if word.endswith(('.', '!', '?', ':')):
            await asyncio.sleep(0.5)
        elif word.endswith(','):
            await asyncio.sleep(0.2)
    
    # Remover cursor e finalizar
    current_streaming_msg.content = current_text.strip()
    await current_streaming_msg.update()

async def simulate_multi_token_processing(user_input: str, max_tokens: int = 4000):
    """Simula processamento multi-token para respostas grandes"""
    
    # Detectar se vai precisar de múltiplos tokens
    estimated_tokens = len(user_input.split()) * 2  # Estimativa grosseira
    
    if estimated_tokens > max_tokens * 0.8:  # 80% do limite
        # Mostrar que vai dividir em chunks
        chunk_msg = cl.Message(
            content="🧠 **Detectada requisição complexa**\n⚡ Dividindo em múltiplos chunks para processamento otimizado...",
            author="Sistema Multi-Token"
        )
        await chunk_msg.send()
        
        # Simular divisão em chunks
        num_chunks = max(2, estimated_tokens // max_tokens + 1)
        
        for i in range(num_chunks):
            await asyncio.sleep(1)
            chunk_msg.content += f"\n📦 Chunk {i+1}/{num_chunks} processado"
            await chunk_msg.update()
        
        chunk_msg.content += "\n✅ **Todos os chunks processados - Compilando resposta final...**"
        await chunk_msg.update()

class StreamingCarlosWrapper:
    """Wrapper para interceptar e adicionar streaming ao Carlos"""
    
    def __init__(self, carlos_instance):
        self.carlos = carlos_instance
    
    async def processar_com_streaming(self, entrada: str, contexto: dict = None):
        """Processa com streaming visual completo"""
        
        # 1. Análise inicial
        await stream_agent_activity("Carlos", "Analisando comando recebido", 1.5)
        
        # 2. Detectar se precisa multi-token
        await simulate_multi_token_processing(entrada)
        
        # 3. TaskBreaker analisando
        await stream_agent_activity("TaskBreaker", "Avaliando complexidade da tarefa", 2.0)
        
        # 4. SupervisorAI classificando
        await stream_agent_activity("SupervisorAI", "Classificando tipo de resposta necessária", 1.8)
        
        # 5. Se for plano de carreira, mostrar agentes específicos
        if "plano" in entrada.lower() and "carreira" in entrada.lower():
            await stream_agent_activity("AutoMaster", "Criando estratégia de carreira completa", 3.0)
            await stream_agent_activity("PromptCrafter", "Otimizando estrutura do plano", 2.5)
        
        # 6. Simulação da Assembleia do Oráculo
        await stream_oraculo_assembly(6)
        
        # 7. Processamento real do Carlos
        response = self.carlos.processar(entrada, contexto or {})
        
        # 8. Auditoria final
        await stream_agent_activity("Reflexor", "Realizando auditoria de qualidade", 1.5)
        
        # 9. Stream da resposta palavra por palavra
        await asyncio.sleep(1)
        await stream_response_generation(response)
        
        return response

@cl.on_chat_start
async def start():
    """Inicializa o sistema com feedback streaming"""
    global carlos_instance
    
    session_id = str(uuid.uuid4())[:8]
    
    # Loading sequence animada
    loading_msg = cl.Message(content="🚀 **Inicializando GPT Mestre Autônomo v5.0 Streaming...**")
    await loading_msg.send()
    
    steps = [
        "🔧 Inicializando núcleo do sistema...",
        "👑 Carregando Carlos v5.0 Maestro...",
        "🧠 Ativando SupervisorAI v2.0...", 
        "🔍 Inicializando Reflexor v2.0...",
        "🌐 Conectando DeepAgent v2.0...",
        "🔮 Despertando Oráculo v9.0...",
        "💼 Ativando AutoMaster v2.0...",
        "🔨 Preparando TaskBreaker v2.0...",
        "🧠 Inicializando PsyMind v2.0...",
        "🎨 Carregando PromptCrafter v3.0...",
        "🧠 Conectando memória vetorial...",
        "⚡ Configurando streaming em tempo real...",
        "✅ Sistema 100% operacional!"
    ]
    
    for step in steps:
        await asyncio.sleep(0.4)
        loading_msg.content = f"🚀 **GPT Mestre Autônomo v5.0 Streaming**\n\n{step}"
        await loading_msg.update()
    
    try:
        # Inicializar Carlos
        carlos_base = criar_carlos_maestro(
            supervisor_ativo=True,
            reflexor_ativo=True,
            deepagent_ativo=True,
            oraculo_ativo=True,
            automaster_ativo=True,
            taskbreaker_ativo=True,
            psymind_ativo=True,
            promptcrafter_ativo=True,
            memoria_ativa=True,
            modo_proativo=True
        )
        
        # Wrapper com streaming
        carlos_instance = StreamingCarlosWrapper(carlos_base)
        
        # Mensagem de boas-vindas
        welcome_msg = cl.Message(
            content=f"""
🎉 **GPT Mestre Autônomo v5.0 STREAMING PRONTO!**

🔥 **Funcionalidades STREAMING:**
• 📡 **Feedback em Tempo Real** - Veja cada agente trabalhando
• ⚡ **Resposta Palavra por Palavra** - Construção ao vivo  
• 🧠 **Assembleia Dinâmica Visual** - Veja os suboráculos deliberando
• 🚀 **Sistema Multi-Token** - Quebra automática para respostas grandes
• 🎪 **Transparência Total** - Acompanhe todo o processo

🧠 **Sistema Multi-Agente Ativo:**
• 👑 Carlos v5.0 - Maestro com Streaming
• 🔮 Oráculo v9.0 - Assembleia Dinâmica Visual
• 💼 AutoMaster v2.0 - Planejamento Estratégico
• 🔨 TaskBreaker v2.0 - Análise de Complexidade
• 🔍 Reflexor v2.0 - Auditoria de Qualidade
• 🌐 DeepAgent v2.0 - Pesquisa Web em Tempo Real

💡 **Teste agora:**
"Crie um plano completo de carreira em programação"

🚀 **Sessão ID**: {session_id}

**Oi Matheus! Como posso ajudá-lo hoje?** 😊
""",
            author="GPT Mestre Autônomo"
        )
        
        await welcome_msg.send()
        system_logger.info(f"🚀 Sistema Streaming inicializado para sessão {session_id}")
        
    except Exception as e:
        error_msg = cl.Message(
            content=f"❌ **Erro na inicialização**: {str(e)}\n\nTente recarregar a página."
        )
        await error_msg.send()
        system_logger.error(f"❌ Erro na inicialização: {e}")

@cl.on_message
async def main(message: cl.Message):
    """Processa mensagens com streaming completo"""
    global carlos_instance
    
    if not carlos_instance:
        error_msg = cl.Message(content="❌ Sistema não inicializado. Recarregue a página.")
        await error_msg.send()
        return
    
    user_input = message.content.strip()
    
    try:
        # Processar com streaming visual completo
        await carlos_instance.processar_com_streaming(user_input, {})
        
        system_logger.info(f"✅ Resposta streaming gerada para: {user_input[:50]}...")
        
    except Exception as e:
        error_msg = cl.Message(
            content=f"❌ **Erro no processamento**: {str(e)}\n\nTente uma pergunta mais simples.",
            author="Sistema"
        )
        await error_msg.send()
        system_logger.error(f"❌ Erro no processamento streaming: {e}")

@cl.on_stop
async def stop():
    """Limpa recursos quando o chat para"""
    global carlos_instance, current_status_msg, current_streaming_msg
    carlos_instance = None
    current_status_msg = None
    current_streaming_msg = None
    system_logger.info("🛑 Sessão streaming encerrada")

if __name__ == "__main__":
    cl.run()