#!/usr/bin/env python3
"""
GPT MESTRE AUTÔNOMO - Script de Execução Principal
"""

import os
import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Verifica se os requisitos estão instalados"""
    print("🔍 Verificando dependências...")
    
    try:
        import streamlit
        import anthropic
        import langchain
        import langchain_anthropic
        import chromadb
        import loguru
        print("✅ Dependências principais encontradas")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("📦 Execute: pip install -r requirements.txt")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe e está configurado"""
    print("🔍 Verificando configuração...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Arquivo .env não encontrado!")
        print("📝 Copie .env.example para .env e configure suas chaves de API")
        return False
    
    # Verifica se tem ANTHROPIC_API_KEY
    with open(env_file, 'r') as f:
        content = f.read()
        if "ANTHROPIC_API_KEY=sk-ant-" not in content:
            print("❌ ANTHROPIC_API_KEY não configurada no arquivo .env")
            print("🔑 Configure sua chave da Anthropic no arquivo .env")
            return False
    
    print("✅ Configuração encontrada")
    return True

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios...")
    
    dirs = ["logs", "memory", "agents", "utils"]
    for dir_name in dirs:
        Path(dir_name).mkdir(exist_ok=True)
    
    print("✅ Diretórios criados")

def run_streamlit():
    """Executa a aplicação Streamlit"""
    print("🚀 Iniciando GPT Mestre Autônomo...")
    print("🌐 A aplicação será aberta no navegador em http://localhost:8501")
    print("⏹️  Pressione Ctrl+C para parar")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app.py",
            "--server.port=8501",
            "--server.address=0.0.0.0",
            "--theme.base=dark"
        ])
    except KeyboardInterrupt:
        print("\n👋 GPT Mestre Autônomo finalizado!")
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")

def show_help():
    """Mostra informações de ajuda"""
    help_text = """
    🤖 GPT MESTRE AUTÔNOMO - Sistema de Agentes Inteligentes
    
    COMANDOS:
    python run.py          - Executa a aplicação
    python run.py --help   - Mostra esta ajuda
    python run.py --check  - Verifica configuração
    python run.py --setup  - Configuração inicial
    
    REQUISITOS:
    1. Python 3.8+
    2. pip install -r requirements.txt
    3. Arquivo .env com ANTHROPIC_API_KEY configurada
    
    PRIMEIRA EXECUÇÃO:
    1. python run.py --setup
    2. Configure seu .env com a chave da Anthropic
    3. python run.py
    
    ESTRUTURA DO PROJETO:
    📁 agents/       - Agentes do sistema (Carlos, Reflexor, etc.)
    📁 utils/        - Utilitários (logger, etc.)
    📁 memory/       - Sistema de memória vetorial
    📁 logs/         - Logs do sistema
    📄 config.py     - Configurações centralizadas
    📄 app.py        - Interface Streamlit principal
    
    PROBLEMAS COMUNS:
    - "Module not found": Execute pip install -r requirements.txt
    - "API key missing": Configure ANTHROPIC_API_KEY no .env
    - "Permission denied": Execute como administrador/sudo
    
    SUPORTE:
    - Logs disponíveis em logs/gpt_mestre.log
    - Debug mode: configure DEBUG=True no .env
    """
    print(help_text)

def setup_initial():
    """Configuração inicial do projeto"""
    print("🔧 Configuração inicial do GPT Mestre Autônomo...")
    
    # Cria diretórios
    create_directories()
    
    # Verifica se .env.example existe
    if not Path(".env.example").exists():
        print("❌ Arquivo .env.example não encontrado!")
        return False
    
    # Copia .env.example para .env se não existir
    env_file = Path(".env")
    if not env_file.exists():
        import shutil
        shutil.copy(".env.example", ".env")
        print("📝 Arquivo .env criado a partir do .env.example")
        print("🔑 CONFIGURE sua ANTHROPIC_API_KEY no arquivo .env antes de continuar!")
    else:
        print("✅ Arquivo .env já existe")
    
    # Verifica dependências
    if not check_requirements():
        print("📦 Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Configuração inicial concluída!")
    print("🔑 Próximo passo: Configure ANTHROPIC_API_KEY no arquivo .env")
    print("🚀 Depois execute: python run.py")
    
    return True

def main():
    """Função principal"""
    print("🤖 GPT MESTRE AUTÔNOMO v1.0.0")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "--help":
            show_help()
            return
        elif command == "--check":
            print("🔍 Verificando sistema...")
            deps_ok = check_requirements()
            env_ok = check_env_file()
            if deps_ok and env_ok:
                print("✅ Sistema pronto para execução!")
            else:
                print("❌ Sistema não está pronto. Verifique os erros acima.")
            return
        elif command == "--setup":
            setup_initial()
            return
        else:
            print(f"❌ Comando desconhecido: {command}")
            print("Use --help para ver comandos disponíveis")
            return
    
    # Execução normal
    if not check_requirements():
        print("Execute: python run.py --setup")
        return
    
    if not check_env_file():
        print("Configure o arquivo .env antes de continuar")
        return
    
    create_directories()
    run_streamlit()

if __name__ == "__main__":
    main()