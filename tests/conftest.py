"""
Configuração central do pytest para GPT Mestre Autônomo
Fixtures reutilizáveis e configurações globais
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import MagicMock, AsyncMock, patch
from datetime import datetime
import json
import tempfile
from pathlib import Path

# Adicionar o diretório raiz ao path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Importações necessárias
from agents.carlos import CarlosMaestroV5, criar_carlos_maestro
from agents.base_agent_v2 import BaseAgentV2
from utils.logger import get_logger

# Configuração global para testes
pytest_plugins = ['pytest_asyncio']


@pytest.fixture(scope="session")
def event_loop():
    """Cria event loop para testes assíncronos"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
def mock_llm_response():
    """
    Fixture para mockar a resposta de um LLM.
    Pode ser usado com @pytest.mark.parametrize para diferentes cenários.
    """
    mock_llm = MagicMock()
    
    # Respostas padrão para diferentes tipos de chamada
    def mock_invoke(prompt, **kwargs):
        # Respostas baseadas no conteúdo do prompt
        if "capital da França" in str(prompt):
            return "A capital da França é Paris."
        elif "falha" in str(prompt).lower():
            raise Exception("Simulated LLM API error")
        elif not prompt or str(prompt).strip() == "":
            return "Desculpe, não entendi sua solicitação. Pode reformular?"
        else:
            return f"Resposta mockada para: {str(prompt)[:50]}..."
    
    mock_llm.invoke = MagicMock(side_effect=mock_invoke)
    mock_llm.process_request = MagicMock(side_effect=lambda x: (mock_invoke(x), 10))
    
    return mock_llm


@pytest.fixture(scope="function")
def mock_config():
    """Mock das configurações do sistema"""
    mock_cfg = MagicMock()
    mock_cfg.LLM_PROVIDER = "gemini"
    mock_cfg.GOOGLE_API_KEY = "test-key"
    mock_cfg.GEMINI_MODEL = "gemini-1.5-flash"
    mock_cfg.GEMINI_MAX_TOKENS = 8192
    mock_cfg.GEMINI_TEMPERATURE = 0.7
    mock_cfg.MAX_WORKERS = 4
    mock_cfg.TIMEOUT_SECONDS = 60
    mock_cfg.RATE_LIMIT_PER_MINUTE = 120
    mock_cfg.BURST_ALLOWANCE = 20
    mock_cfg.DEBUG = True
    
    return mock_cfg


@pytest.fixture(scope="function")
def carlos_instance(mock_llm_response, mock_config):
    """
    Fixture para criar uma instância limpa de CarlosMaestroV5 para cada teste.
    Injeta o mock_llm_response no sistema.
    """
    # Patch das configurações
    with patch('config.config', mock_config):
        # Patch do LLM em vários pontos possíveis
        with patch('agents.base_agent_v2.BaseAgentV2._criar_llm', return_value=mock_llm_response):
            with patch('agents.carlos.BaseAgentV2._criar_llm', return_value=mock_llm_response):
                # Criar instância com configurações mínimas para teste
                carlos = criar_carlos_maestro(
                    supervisor_ativo=False,  # Desativar outros agentes para testes unitários
                    reflexor_ativo=False,
                    deepagent_ativo=False,
                    oraculo_ativo=False,
                    automaster_ativo=False,
                    taskbreaker_ativo=False,
                    psymind_ativo=False,
                    promptcrafter_ativo=False,
                    memoria_ativa=False,
                    modo_proativo=False,
                    inovacoes_ativas=False  # Desativar inovações para simplificar
                )
                
                # Injetar o mock diretamente se necessário
                if hasattr(carlos, 'llm'):
                    carlos.llm = mock_llm_response
                
                # Garantir que o LLM está mockado em todos os agentes base
                for attr_name in dir(carlos):
                    attr = getattr(carlos, attr_name)
                    if isinstance(attr, BaseAgentV2) and hasattr(attr, 'llm'):
                        attr.llm = mock_llm_response
                
                yield carlos


@pytest.fixture(scope="function")
def carlos_instance_full(mock_llm_response, mock_config):
    """
    Fixture para criar Carlos com todos os agentes ativos (testes de integração).
    """
    with patch('config.config', mock_config):
        with patch('agents.base_agent_v2.BaseAgentV2._criar_llm', return_value=mock_llm_response):
            carlos = criar_carlos_maestro(
                supervisor_ativo=True,
                reflexor_ativo=True,
                deepagent_ativo=True,
                oraculo_ativo=True,
                automaster_ativo=True,
                taskbreaker_ativo=True,
                psymind_ativo=True,
                promptcrafter_ativo=True,
                memoria_ativa=True,
                modo_proativo=True,
                inovacoes_ativas=True
            )
            
            # Mockar LLM em todos os agentes
            for attr_name in dir(carlos):
                attr = getattr(carlos, attr_name)
                if isinstance(attr, BaseAgentV2) and hasattr(attr, 'llm'):
                    attr.llm = mock_llm_response
            
            yield carlos


@pytest.fixture(scope="function")
def temp_memory_dir():
    """Cria diretório temporário para testes de memória"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def sample_messages():
    """Mensagens de exemplo para testes"""
    return {
        "simple": "Qual a capital da França?",
        "empty": "",
        "none": None,
        "long": "x" * 10000,  # 10k caracteres
        "special_chars": "Olá ✨🤖💥🌎❓✅ teste com emojis!",
        "multi_line": "Primeira linha\nSegunda linha\nTerceira linha",
        "code": "def hello():\n    print('Hello, World!')",
        "complex": "Analise os prós e contras de mudar de carreira de engenharia para gestão, considerando fatores financeiros, satisfação pessoal e impacto familiar.",
        "numbers": "2 + 2 = ?",
        "mixed": "Test123!@# com números e símbolos 🎯"
    }


@pytest.fixture
def sample_contexts():
    """Contextos de exemplo para testes"""
    return {
        "empty": {},
        "user": {"user_id": "test_user", "session_id": "test_session"},
        "full": {
            "user_id": "test_user",
            "session_id": "test_session",
            "timestamp": datetime.now().isoformat(),
            "metadata": {"source": "test", "priority": "high"}
        }
    }


@pytest.fixture
def mock_agent():
    """Mock de um agente genérico"""
    agent = MagicMock(spec=BaseAgentV2)
    agent.processar = MagicMock(return_value="Resposta do agente mock")
    agent.nome = "MockAgent"
    agent.esta_disponivel = MagicMock(return_value=True)
    return agent


# Marcadores customizados
def pytest_configure(config):
    """Registra marcadores customizados"""
    config.addinivalue_line(
        "markers", "slow: marca testes que são lentos (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração"
    )
    config.addinivalue_line(
        "markers", "unit: marca testes unitários"
    )
    config.addinivalue_line(
        "markers", "llm: marca testes que usam LLM real (não mockado)"
    )


# Opções de linha de comando customizadas
def pytest_addoption(parser):
    """Adiciona opções customizadas ao pytest"""
    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )
    parser.addoption(
        "--integration", action="store_true", default=False, help="run integration tests"
    )
    parser.addoption(
        "--llm", action="store_true", default=False, help="run tests with real LLM (expensive!)"
    )


def pytest_collection_modifyitems(config, items):
    """Modifica a coleção de testes baseado nas opções"""
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
    
    if not config.getoption("--integration"):
        skip_integration = pytest.mark.skip(reason="need --integration option to run")
        for item in items:
            if "integration" in item.keywords:
                item.add_marker(skip_integration)
    
    if not config.getoption("--llm"):
        skip_llm = pytest.mark.skip(reason="need --llm option to run (uses real API)")
        for item in items:
            if "llm" in item.keywords:
                item.add_marker(skip_llm)


# Fixture para resetar singletons entre testes
@pytest.fixture(autouse=True)
def reset_singletons():
    """Reseta singletons entre testes para garantir isolamento"""
    yield
    # Aqui você pode adicionar código para resetar qualquer singleton
    # Por exemplo, se TokenMonitor for singleton:
    # TokenMonitor._instance = None