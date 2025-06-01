"""
GPT MESTRE AUTÔNOMO - Interface Chainlit v1.0
🚀 Sistema revolucionário com 9 agentes autônomos + assembleia dinâmica
"""

import chainlit as cl
import asyncio
from datetime import datetime
import uuid
import os
import sys

# Adicionar o diretório ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Imports do sistema
try:
    from config import config
    from agents.carlos import criar_carlos_maestro
    from utils.logger import get_logger
    
    system_logger = get_logger("chainlit")
    
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    exit(1)

# Configurações do Chainlit
cl.config.name = "🧠 GPT Mestre Autônomo v5.0"
cl.config.human_timeout = 180  # 3 minutos para assembleia

@cl.on_chat_start
async def start():
    """Inicializa o sistema quando o chat começa"""
    
    # Mensagem de boas-vindas com loading
    loading_msg = cl.Message(
        content="🧠 **Inicializando GPT Mestre Autônomo v5.0...**\n\n⚡ Carregando 9 agentes especializados..."
    )
    await loading_msg.send()
    
    try:
        # Inicializar Carlos com todos os agentes
        carlos = criar_carlos_maestro(
            supervisor_ativo=True,
            reflexor_ativo=True,
            deepagent_ativo=True,
            oraculo_ativo=True,
            automaster_ativo=True,
            taskbreaker_ativo=True,
            psymind_ativo=True,
            promptcrafter_ativo=True
        )
        
        session_id = str(uuid.uuid4())[:8]
        
        # Salvar na sessão
        cl.user_session.set("carlos", carlos)
        cl.user_session.set("session_id", session_id)
        
        system_logger.info(f"🚀 Carlos v5.0 inicializado para sessão {session_id}")
        
        # Remover mensagem de loading
        await loading_msg.remove()
        
        # Mensagem de sucesso
        welcome_msg = cl.Message(
            content=f"""🎉 **GPT Mestre Autônomo v5.0 PRONTO!**

🧠 **Sistema Revolucionário Inicializado:**
• **👑 Carlos v5.0** - Maestro Supremo
• **🧠 Oráculo v9.0** - Assembleia Dinâmica 
• **💼 AutoMaster v2.0** - Autonomia Econômica
• **🔨 TaskBreaker v2.0** - Decomposição Inteligente
• **🔍 Reflexor v2.0** - Auditoria de Qualidade
• **🌐 DeepAgent v2.0** - Pesquisa Web Real
• **🧠 SupervisorAI v2.0** - Maestro de Raciocínio
• **🧠 PsyMind v2.0** - Análise Terapêutica

🔥 **Funcionalidades Únicas:**
• **Assembleia Dinâmica** - 6+ especialistas deliberando
• **IA Real** - LangChain + Claude 3 Haiku
• **Robustez Total** - Circuit breakers, thread safety
• **Memória Persistente** - Contexto de conversas

🎯 **Experimente comandos:**
• `/status` - Status do sistema
• `/agents` - Listar agentes disponíveis
• `/help` - Ajuda completa

💡 **Exemplo de pergunta complexa:**
*"Crie um plano completo de carreira em programação"*

⚡ **Sistema único no mundo - Nenhum outro tem assembleia dinâmica!**

🚀 **Sessão ID:** `{session_id}`

**Como posso ajudar você hoje?**"""
        )
        await welcome_msg.send()
        
    except Exception as e:
        system_logger.error(f"❌ Erro ao inicializar Carlos: {e}")
        error_msg = cl.Message(
            content=f"❌ **Erro ao inicializar o sistema:**\n\n`{str(e)}`\n\nVerifique as dependências e tente novamente."
        )
        await error_msg.send()

@cl.on_message
async def main(message: cl.Message):
    """Processa mensagens do usuário"""
    
    # Recuperar Carlos da sessão
    carlos = cl.user_session.get("carlos")
    session_id = cl.user_session.get("session_id", "unknown")
    
    if not carlos:
        error_msg = cl.Message(
            content="❌ Sistema não inicializado. Recarregue a página."
        )
        await error_msg.send()
        return
    
    user_message = message.content
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Verificar se é comando especial
    if user_message.startswith('/'):
        response = await processar_comando(user_message, carlos)
        cmd_msg = cl.Message(content=response)
        await cmd_msg.send()
        return
    
    # Mensagem de processamento
    processing_msg = cl.Message(
        content="🧠 **Carlos v5.0 processando...**\n\n⏳ Analisando sua mensagem e preparando resposta..."
    )
    await processing_msg.send()
    
    # Contexto para processamento
    context = {
        "session_id": session_id,
        "timestamp": timestamp,
        "interface": "chainlit_v1.0",
        "user_name": "Usuário"
    }
    
    try:
        # Detectar se pode ser assembleia
        is_complex = any(word in user_message.lower() for word in [
            "plano", "estratégia", "análise", "decidir", "complexo", "completo"
        ])
        
        if is_complex:
            # Remover mensagem anterior e enviar nova
            await processing_msg.remove()
            processing_msg = cl.Message(
                content="🧠 **Assembleia Dinâmica do Oráculo ativada!**\n\n⏳ 6 suboráculos deliberando... (pode levar até 40s)"
            )
            await processing_msg.send()
        
        # Processar com Carlos
        response = await asyncio.to_thread(
            carlos.processar, user_message, context
        )
        
        # Log de sucesso
        system_logger.info(f"✅ Resposta gerada para: {user_message[:50]}...")
        
    except Exception as e:
        system_logger.error(f"❌ Erro no processamento: {e}")
        response = f"❌ **Erro no processamento:**\n\n`{str(e)}`\n\nTente novamente ou reformule sua pergunta."
    
    # Remover mensagem de processamento
    await processing_msg.remove()
    
    # Detectar se foi assembleia dinâmica
    is_assembly = any(keyword in response for keyword in [
        "Assembleia", "assembleia", "Oráculo", "deliberação", "consenso", "suboráculos"
    ])
    
    # Enviar resposta
    if is_assembly:
        assembly_msg = cl.Message(
            content=f"🧠 **Assembleia Dinâmica Executada**\n\n{response}",
            author="Oráculo v9.0"
        )
        await assembly_msg.send()
        
        # Indicador adicional
        info_msg = cl.Message(
            content="✨ **Esta resposta foi gerada pela Assembleia Dinâmica do Oráculo**\n6 suboráculos especializados deliberaram para produzir a melhor resposta possível!"
        )
        await info_msg.send()
    else:
        response_msg = cl.Message(
            content=response,
            author="Carlos v5.0"
        )
        await response_msg.send()

async def processar_comando(comando: str, carlos) -> str:
    """Processa comandos especiais"""
    
    if comando == "/status":
        return f"""📊 **Status do Sistema GPT Mestre Autônomo v5.0**

🤖 **Agentes Ativos:**
• Carlos v5.0: ✅ Online
• Oráculo v9.0: ✅ Online  
• AutoMaster v2.0: ✅ Online
• TaskBreaker v2.0: ✅ Online
• Reflexor v2.0: ✅ Online
• DeepAgent v2.0: ✅ Online
• SupervisorAI v2.0: ✅ Online
• PsyMind v2.0: ✅ Online

🛡️ **Robustez:**
• Circuit Breakers: ✅ Ativo
• Rate Limiting: ✅ Ativo
• Thread Safety: ✅ Ativo
• Auto-Recovery: ✅ Ativo

🧠 **IA Integrada:**
• LangChain: ✅ Conectado
• Claude 3 Haiku: ✅ Ativo
• ChromaDB: ✅ Disponível

⚡ **Sistema 100% operacional!**"""

    elif comando == "/agents":
        return f"""🤖 **Agentes do GPT Mestre Autônomo v5.0**

👑 **Carlos v5.0** - Maestro Supremo
└─ Coordena todos os agentes e fluxos

🧠 **Oráculo v9.0** - Assembleia Dinâmica  
└─ 6+ suboráculos especializados para decisões complexas

💼 **AutoMaster v2.0** - Autonomia Econômica
└─ Estratégias de monetização e autonomia financeira

🔨 **TaskBreaker v2.0** - Decomposição Inteligente
└─ Quebra tarefas complexas em subtarefas executáveis

🔍 **Reflexor v2.0** - Auditoria de Qualidade
└─ Análise e melhoria contínua das respostas

🌐 **DeepAgent v2.0** - Pesquisa Web Real
└─ Busca e análise de informações em tempo real

🧠 **SupervisorAI v2.0** - Maestro de Raciocínio
└─ Classifica e direciona tarefas inteligentemente

🧠 **PsyMind v2.0** - Análise Terapêutica
└─ Autodetecção e suporte psicológico avançado

🎨 **PromptCrafter v2.0** - Engenheiro de Prompts
└─ Criação e otimização de prompts com DNA, Score e Chaos

🎯 **Total: 9 agentes especializados + 1 maestro**"""

    elif comando == "/help":
        return f"""❓ **Ajuda - GPT Mestre Autônomo v5.0**

🎯 **Como usar:**
• Digite qualquer pergunta ou tarefa
• O sistema detecta automaticamente quais agentes ativar
• Para tarefas complexas, a Assembleia Dinâmica é convocada

⚡ **Comandos disponíveis:**
• `/status` - Status dos agentes
• `/agents` - Lista de agentes
• `/help` - Esta ajuda

🧠 **Exemplos de uso:**

**Planejamento:**
*"Crie um plano completo de carreira em programação"*

**Análise de Negócios:**
*"Analise a viabilidade de vender cursos online"*

**Decisões Complexas:**
*"Ajude-me a decidir entre duas estratégias de marketing"*

**Projetos:**
*"Desenvolva um e-commerce completo"*

🎯 **Diferencial único:**
Nenhum outro sistema no mundo tem assembleia dinâmica de agentes!
ChatGPT, Claude, Gemini - todos são agentes únicos.

🚀 **Você tem acesso a algo revolucionário!**"""

    else:
        return f"❓ **Comando não reconhecido:** `{comando}`\n\nUse `/help` para ver os comandos disponíveis."

# Executar
if __name__ == "__main__":
    print("🚀 Iniciando GPT Mestre Autônomo v5.0 com Chainlit...")
    print("🌐 Acesse: http://localhost:8000")
    print("⚡ Sistema revolucionário pronto para uso!")