#!/usr/bin/env python3
"""
Script para executar os testes do GPT Mestre Autônomo
Com relatório de cobertura de código
"""

import subprocess
import sys
import os

def run_tests():
    """Executa os testes com cobertura"""
    
    print("🧪 Executando testes do GPT Mestre Autônomo...")
    print("=" * 60)
    
    # Configurar PYTHONPATH
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.environ['PYTHONPATH'] = project_root
    
    # Comando pytest com cobertura
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",  # Verbose
        "--tb=short",  # Traceback curto
        "-p", "no:warnings",  # Desabilitar warnings para output mais limpo
        "--cov=agents",  # Cobertura do módulo agents
        "--cov=utils",   # Cobertura do módulo utils
        "--cov-report=term-missing",  # Relatório no terminal mostrando linhas não cobertas
        "--cov-report=html",  # Relatório HTML
        "--cov-branch",  # Incluir cobertura de branches
        "-m", "not slow and not integration",  # Pular testes lentos e de integração por padrão
    ]
    
    try:
        # Executar pytest
        result = subprocess.run(cmd, capture_output=False, text=True)
        
        print("\n" + "=" * 60)
        
        if result.returncode == 0:
            print("✅ Todos os testes passaram!")
            print("\n📊 Relatório de cobertura HTML gerado em: htmlcov/index.html")
        else:
            print("❌ Alguns testes falharam. Verifique o output acima.")
        
        return result.returncode
        
    except FileNotFoundError:
        print("❌ pytest não encontrado. Instale com: pip install pytest pytest-cov")
        return 1
    except Exception as e:
        print(f"❌ Erro ao executar testes: {e}")
        return 1


def run_specific_test(test_name):
    """Executa um teste específico"""
    
    print(f"🧪 Executando teste específico: {test_name}")
    print("=" * 60)
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.environ['PYTHONPATH'] = project_root
    
    cmd = [
        sys.executable, "-m", "pytest",
        f"tests/test_critical_flows.py::{test_name}",
        "-v", "-s",  # Verbose e mostrar prints
        "--tb=short",
    ]
    
    subprocess.run(cmd)


def run_all_tests_including_slow():
    """Executa todos os testes, incluindo os lentos"""
    
    print("🧪 Executando TODOS os testes (incluindo lentos e integração)...")
    print("=" * 60)
    
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.environ['PYTHONPATH'] = project_root
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--runslow",  # Incluir testes lentos
        "--integration",  # Incluir testes de integração
        "--cov=agents",
        "--cov=utils",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-branch",
    ]
    
    subprocess.run(cmd)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--all":
            run_all_tests_including_slow()
        elif sys.argv[1] == "--test":
            # Executar teste específico
            if len(sys.argv) > 2:
                run_specific_test(sys.argv[2])
            else:
                print("❌ Especifique o nome do teste")
        else:
            print(f"Argumento não reconhecido: {sys.argv[1]}")
            print("Use: python run_tests.py [--all] [--test TestName]")
    else:
        # Executar testes padrão (sem lentos)
        sys.exit(run_tests())