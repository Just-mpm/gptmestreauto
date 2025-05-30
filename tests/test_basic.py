#!/usr/bin/env python3
"""
GPT MESTRE AUTÔNOMO - Testes Básicos do Sistema
Testa componentes fundamentais sem necessidade de API key
"""

import sys
import os
from pathlib import Path

# Adiciona o diretório raiz ao PATH
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Testa se todos os módulos podem ser importados"""
    print("🧪 Testando imports...")
    
    try:
        # Testa imports básicos
        import config
        print("  ✅ config.py")
        
        from utils.logger import system_logger, get_agent_logger
        print("  ✅ utils.logger")
        
        from agents.base_agent import BaseAgent
        print("  ✅ agents.base_agent")
        
        from agents.carlos import CarlosAgent, create_carlos
        print("  ✅ agents.carlos")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Erro de import: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Erro geral: {e}")
        return False

def test_config():
    """Testa configurações básicas"""
    print("🧪 Testando configurações...")
    
    try:
        from config import config
        
        # Testa propriedades básicas
        assert hasattr(config, 'PROJECT_NAME')
        assert hasattr(config, 'VERSION')
        assert hasattr(config, 'BASE_DIR')
        
        print(f"  ✅ Projeto: {config.PROJECT_NAME}")
        print(f"  ✅ Versão: {config.VERSION}")
        print(f"  ✅ Diretório base: {config.BASE_DIR}")
        
        # Testa se diretórios existem
        dirs_to_check = [config.LOGS_DIR, config.MEMORY_DIR, config.AGENTS_DIR]
        for dir_path in dirs_to_check:
            assert dir_path.exists(), f"Diretório {dir_path} não existe"
            print(f"  ✅ Diretório: {dir_path.name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na configuração: {e}")
        return False

def test_logger():
    """Testa sistema de logging"""
    print("🧪 Testando sistema de logging...")
    
    try:
        from utils.logger import system_logger, get_agent_logger
        
        # Testa logger do sistema
        system_logger.info("Teste do logger do sistema")
        print("  ✅ Logger do sistema")
        
        # Testa logger de agente
        test_logger = get_agent_logger("test_agent")
        test_logger.info("Teste do logger de agente")
        print("  ✅ Logger de agente")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro no logger: {e}")
        return False

def test_base_agent():
    """Testa classe base dos agentes (sem LLM)"""
    print("🧪 Testando classe base dos agentes...")
    
    try:
        from agents.base_agent import BaseAgent
        from datetime import datetime
        
        # Cria agente de teste
        class TestAgent(BaseAgent):
            def _default_personality(self):
                return "Agente de teste"
            
            async def process_message(self, message, context=None):
                # Simula processamento sem chamar LLM
                return f"Teste processado: {message}"
        
        # Testa inicialização
        agent = TestAgent("TestAgent", "Teste")
        assert agent.name == "TestAgent"
        assert agent.role == "Teste"
        print("  ✅ Inicialização do agente")
        
        # Testa memória
        memory_summary = agent.get_memory_summary()
        assert 'name' in memory_summary
        assert 'total_messages' in memory_summary
        print("  ✅ Sistema de memória")
        
        # Testa prompt do sistema
        system_prompt = agent.get_system_prompt()
        assert "TestAgent" in system_prompt
        print("  ✅ Geração de prompt do sistema")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na classe base: {e}")
        return False

def test_carlos_basic():
    """Testa agente Carlos (inicialização apenas)"""
    print("🧪 Testando agente Carlos (básico)...")
    
    try:
        from agents.carlos import CarlosAgent, create_carlos
        
        # Testa factory function
        carlos = create_carlos()
        assert carlos.name == "Carlos"
        assert "Interface Principal" in carlos.role
        print("  ✅ Criação do Carlos")
        
        # Testa comandos especiais
        assert "/help" in carlos.special_commands
        assert "/status" in carlos.special_commands
        print("  ✅ Comandos especiais registrados")
        
        # Testa personalidade
        personality = carlos._default_personality()
        assert "Carlos" in personality
        print("  ✅ Personalidade definida")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro no Carlos: {e}")
        return False

def test_file_structure():
    """Testa estrutura de arquivos"""
    print("🧪 Testando estrutura de arquivos...")
    
    required_files = [
        "config.py",
        "run.py", 
        "app.py",
        "requirements.txt",
        ".env.example"
    ]
    
    required_dirs = [
        "agents",
        "utils",
        "logs",
        "memory"
    ]
    
    try:
        # Testa arquivos
        for file_name in required_files:
            file_path = Path(file_name)
            assert file_path.exists(), f"Arquivo {file_name} não encontrado"
            print(f"  ✅ Arquivo: {file_name}")
        
        # Testa diretórios
        for dir_name in required_dirs:
            dir_path = Path(dir_name)
            assert dir_path.exists(), f"Diretório {dir_name} não encontrado"
            print(f"  ✅ Diretório: {dir_name}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Erro na estrutura: {e}")
        return False

def test_dependencies():
    """Testa se dependências principais estão disponíveis"""
    print("🧪 Testando dependências...")
    
    deps = [
        "streamlit",
        "langchain", 
        "openai",  # Usado para compatibilidade com OpenRouter
        "chromadb",
        "loguru",
        "fastapi",
        "pandas"
    ]
    
    missing_deps = []
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"  ✅ {dep}")
        except ImportError:
            missing_deps.append(dep)
            print(f"  ❌ {dep} (não instalado)")
    
    if missing_deps:
        print(f"\n⚠️  Dependências faltando: {', '.join(missing_deps)}")
        print("Execute: pip install -r requirements.txt")
        return False
    
    return True

def run_all_tests():
    """Executa todos os testes"""
    print("🚀 INICIANDO TESTES DO GPT MESTRE AUTÔNOMO")
    print("=" * 50)
    
    tests = [
        ("Dependências", test_dependencies),
        ("Estrutura de Arquivos", test_file_structure),
        ("Imports", test_imports),
        ("Configurações", test_config),
        ("Sistema de Logging", test_logger),
        ("Classe Base dos Agentes", test_base_agent),
        ("Agente Carlos", test_carlos_basic),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro crítico no teste {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumo final
    print("\n" + "="*50)
    print("📊 RESUMO DOS TESTES")
    print("="*50)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print(f"\n📈 Resultados: {passed} passou(ram), {failed} falhou(aram)")
    
    if failed == 0:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema pronto para uso básico")
        print("\n💡 Próximos passos:")
        print("1. Configure OPENAI_API_KEY no .env")
        print("2. Execute: python run.py")
    else:
        print("⚠️  ALGUNS TESTES FALHARAM")
        print("🔧 Verifique os erros acima e corrija antes de prosseguir")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
