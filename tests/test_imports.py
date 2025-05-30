#!/usr/bin/env python3
"""
Script de teste para verificar se todos os imports estão funcionando
Execute: python test_imports.py
"""

import sys
import os

def testar_estrutura_basica():
    """Testa se a estrutura básica existe"""
    print("🔍 Verificando estrutura de pastas...")
    
    pastas_necessarias = ['agents', 'utils', 'logs']
    for pasta in pastas_necessarias:
        if os.path.exists(pasta):
            print(f"✅ {pasta}/ existe")
        else:
            print(f"❌ {pasta}/ NÃO existe")
            return False
    
    arquivos_necessarios = [
        'agents/__init__.py',
        'agents/base_agent.py', 
        'agents/carlos.py',
        'config.py',
        'app.py'
    ]
    
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"✅ {arquivo} existe")
        else:
            print(f"❌ {arquivo} NÃO existe")
            return False
    
    return True

def testar_imports():
    """Testa todos os imports principais"""
    print("\n🧪 Testando imports...")
    
    # Teste 1: BaseAgent
    try:
        from agents.base_agent import BaseAgent
        print("✅ BaseAgent importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar BaseAgent: {e}")
        return False
    
    # Teste 2: Módulo agents
    try:
        import agents
        status = agents.verificar_agentes()
        print(f"✅ Módulo agents importado: {status}")
    except Exception as e:
        print(f"❌ Erro ao importar módulo agents: {e}")
        return False
    
    # Teste 3: Carlos
    try:
        from agents.carlos import CarlosAgent, create_carlos
        print("✅ Carlos importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar Carlos: {e}")
        return False
    
    # Teste 4: Reflexor (opcional)
    try:
        from agents.reflexor import AgenteReflexor
        print("✅ Reflexor importado com sucesso")
    except Exception as e:
        print(f"⚠️ Reflexor não disponível: {e}")
    
    # Teste 5: Config
    try:
        import config
        print("✅ Config importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar config: {e}")
        return False
    
    return True

def testar_criacao_carlos():
    """Testa se consegue criar uma instância do Carlos"""
    print("\n🤖 Testando criação do Carlos...")
    
    try:
        from agents import create_carlos, verificar_agentes
        
        # Verificar agentes disponíveis
        status = verificar_agentes()
        print(f"📊 Status dos agentes: {status}")
        
        # Criar Carlos
        carlos = create_carlos()
        print("✅ Carlos criado com sucesso!")
        
        # Testar resposta básica
        resposta = carlos.processar("Olá, como você está?")
        print(f"💬 Resposta do Carlos: {resposta[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar Carlos: {e}")
        return False

def testar_sistema_completo():
    """Testa se o sistema completo funciona"""
    print("\n🎯 Testando sistema completo...")
    
    try:
        from agents import criar_sistema_completo
        
        sistema = criar_sistema_completo()
        print("✅ Sistema completo criado!")
        
        # Teste de funcionalidade
        resposta = sistema.processar("/status")
        print(f"📊 Status: {resposta[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no sistema completo: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes do GPT Mestre Autônomo...\n")
    
    # Teste 1: Estrutura
    if not testar_estrutura_basica():
        print("\n❌ FALHOU: Estrutura básica")
        return False
    
    # Teste 2: Imports
    if not testar_imports():
        print("\n❌ FALHOU: Imports")
        return False
    
    # Teste 3: Carlos
    if not testar_criacao_carlos():
        print("\n❌ FALHOU: Criação do Carlos")
        return False
    
    # Teste 4: Sistema completo
    if not testar_sistema_completo():
        print("\n⚠️ AVISO: Sistema completo com problemas")
    
    print("\n🎉 SUCESSO: Todos os testes principais passaram!")
    print("\n📋 Próximos passos:")
    print("1. Execute: streamlit run app.py")
    print("2. Acesse: http://localhost:8501")
    print("3. Teste o Carlos funcionando!")
    
    return True

if __name__ == "__main__":
    main()
