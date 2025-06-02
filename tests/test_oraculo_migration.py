"""
Teste de validação da migração do Oráculo v9.0 para BaseAgentV2
Verifica funcionalidades básicas e robustez
"""

import pytest
import time
from agents.oraculo_v2 import OraculoV9, TipoAssembleia, StatusSuboraculo, TipoSuboraculo
from agents.base_agent_v2 import BaseAgentV2


def test_oraculo_heranca_base_agent():
    """Teste: Oráculo herda corretamente de BaseAgentV2"""
    oraculo = OraculoV9()
    
    # Verificar herança
    assert isinstance(oraculo, BaseAgentV2)
    assert hasattr(oraculo, 'memory')
    assert hasattr(oraculo, 'rate_limiter')
    assert hasattr(oraculo, 'circuit_breaker')
    assert hasattr(oraculo, 'performance_monitor')
    
    print("✅ Oráculo herda corretamente de BaseAgentV2")


def test_oraculo_inicializacao():
    """Teste: Inicialização correta do Oráculo v9.0"""
    oraculo = OraculoV9()
    
    # Verificar atributos específicos do Oráculo
    assert oraculo.name == "Oráculo"
    assert len(oraculo.suboraculos) == len(TipoSuboraculo)
    assert len(oraculo.performance_suboraculos) == len(TipoSuboraculo)
    assert oraculo.curadoria_autonoma_ativa == True
    assert oraculo.multiverso_ativo == True
    assert oraculo.contador_assembleias == 0
    
    # Verificar configuração robusta
    assert oraculo.config['rate_limit_per_minute'] == 120
    assert oraculo.config['burst_allowance'] == 20
    
    print("✅ Oráculo inicializado corretamente com todas as funcionalidades")


def test_oraculo_processamento_simples():
    """Teste: Processamento básico sem LLM"""
    oraculo = OraculoV9()
    
    # Testar processamento simples
    desafio = "Qual a melhor cor para um botão?"
    
    start_time = time.time()
    resposta = oraculo.processar(desafio)
    processing_time = time.time() - start_time
    
    # Verificar resposta
    assert isinstance(resposta, str)
    assert len(resposta) > 50
    assert "Oráculo v9.0" in resposta
    assert "Decisão Final" in resposta
    
    # Verificar métricas
    assert oraculo.stats['assembleias_realizadas'] == 1
    assert oraculo.stats['comandos_processados'] == 1
    assert processing_time < 5.0  # Deve ser rápido
    
    print(f"✅ Processamento simples concluído em {processing_time:.2f}s")


def test_oraculo_assembleia_dinamica():
    """Teste: Sistema de assembleia dinâmica"""
    oraculo = OraculoV9()
    
    # Teste com diferentes complexidades
    casos_teste = [
        ("Cor do botão", TipoAssembleia.TRIVIAL),
        ("Estratégia de marketing digital para startup", TipoAssembleia.COMPLEXO),
        ("Decisão crítica de investimento de 1 milhão", TipoAssembleia.CRITICO)
    ]
    
    for desafio, tipo_esperado in casos_teste:
        tipo_detectado = oraculo._analisar_complexidade(desafio)
        print(f"   Desafio: '{desafio}' → {tipo_detectado.value}")
        
        # Testar curadoria
        colegiado = oraculo._curar_assembleia(desafio, tipo_detectado)
        assert len(colegiado) >= 2
        assert TipoSuboraculo.VIABILIDADE in colegiado  # Núcleo essencial
        assert TipoSuboraculo.ETICO in colegiado  # Núcleo essencial
        
        print(f"   Colegiado: {[s.value for s in colegiado]}")
    
    print("✅ Sistema de assembleia dinâmica funcionando")


def test_oraculo_suboraculos():
    """Teste: Funcionamento dos suboráculos"""
    oraculo = OraculoV9()
    
    # Testar alguns suboráculos específicos
    tipos_teste = [TipoSuboraculo.CRIATIVO, TipoSuboraculo.VIABILIDADE, TipoSuboraculo.CETICO]
    
    for tipo in tipos_teste:
        suboraculo = oraculo.suboraculos[tipo]
        
        # Testar deliberação
        voto = suboraculo.deliberar("Teste de funcionalidade", {})
        
        assert voto.suboraculo == tipo
        assert isinstance(voto.posicao, str)
        assert len(voto.posicao) > 10
        assert 0 <= voto.score_confianca <= 10
        assert 1 <= voto.inovacao_level <= 5
        assert 0 <= voto.risco_calculado <= 10
        
        print(f"   {tipo.value}: {voto.posicao[:50]}...")
    
    print("✅ Suboráculos funcionando corretamente")


def test_oraculo_robustez_baseagent():
    """Teste: Funcionalidades de robustez do BaseAgentV2"""
    oraculo = OraculoV9()
    
    # Testar cache
    desafio = "Teste de cache"
    resposta1 = oraculo.processar(desafio)
    resposta2 = oraculo.processar(desafio)  # Deve usar cache
    
    # Verificar que é a mesma resposta (cache hit)
    assert resposta1 == resposta2
    print("✅ Cache funcionando")
    
    # Testar health status
    health = oraculo.get_health_status()
    assert 'status' in health
    assert 'health_score' in health
    assert 'circuit_breaker_state' in health
    assert 'assembleias_realizadas' in health
    print("✅ Health status disponível")
    
    # Testar diagnóstico específico
    diagnostico = oraculo.diagnosticar_oraculo()
    assert 'version' in diagnostico
    assert 'suboraculos_ativos' in diagnostico
    assert diagnostico['suboraculos_ativos'] == len(TipoSuboracula)
    print("✅ Diagnóstico específico funcionando")


def test_oraculo_historico_assembleia():
    """Teste: Sistema de histórico e diário"""
    oraculo = OraculoV9()
    
    # Processar algumas assembleias
    desafios = [
        "Primeira decisão",
        "Segunda decisão", 
        "Terceira decisão"
    ]
    
    for desafio in desafios:
        oraculo.processar(desafio)
    
    # Verificar histórico
    assert len(oraculo.diario_assembleias) == 3
    assert oraculo.contador_assembleias == 3
    
    # Testar diário
    diario = oraculo.obter_diario_assembleias(2)
    assert "DIÁRIO DE ASSEMBLEIAS" in diario
    assert "assembleia_003" in diario
    
    # Testar bastidores
    bastidores = oraculo.mostrar_bastidores_ultima_assembleia()
    assert "BASTIDORES DA ASSEMBLEIA" in bastidores
    assert "COLEGIADO E VOTOS" in bastidores
    
    print("✅ Sistema de histórico e diário funcionando")


def test_oraculo_performance():
    """Teste: Performance e métricas"""
    oraculo = OraculoV9()
    
    # Processar múltiplas assembleias e medir performance
    start_time = time.time()
    
    for i in range(5):
        desafio = f"Decisão de teste {i+1}"
        resposta = oraculo.processar(desafio)
        assert len(resposta) > 0
    
    total_time = time.time() - start_time
    avg_time = total_time / 5
    
    # Verificar métricas
    assert oraculo.stats['assembleias_realizadas'] == 5
    assert oraculo.stats['score_medio_consenso'] >= 0.0
    assert oraculo.stats['score_medio_robustez'] >= 0.0
    
    print(f"✅ Performance: {avg_time:.2f}s por assembleia em média")
    print(f"   Consenso médio: {oraculo.stats['score_medio_consenso']:.2f}")
    print(f"   Robustez média: {oraculo.stats['score_medio_robustez']:.2f}")


def test_oraculo_multiverso():
    """Teste: Sistema de multiverso contrafactual"""
    oraculo = OraculoV9()
    
    # Testar geração de cenários alternativos
    cenarios = oraculo.gerar_cenarios_alternativos("Teste de multiverso")
    
    assert "MULTIVERSO CONTRAFACTUAL" in cenarios
    assert "Otimista" in cenarios
    assert "Pessimista" in cenarios
    assert "Radical" in cenarios
    assert "Minimalista" in cenarios
    assert "Contrafactual" in cenarios
    
    assert oraculo.stats['cenarios_alternativos_gerados'] == 5
    
    print("✅ Sistema de multiverso funcionando")


if __name__ == "__main__":
    print("🧪 TESTE DE MIGRAÇÃO - ORÁCULO v9.0 → BaseAgentV2")
    print("=" * 70)
    
    try:
        test_oraculo_heranca_base_agent()
        test_oraculo_inicializacao()
        test_oraculo_processamento_simples()
        test_oraculo_assembleia_dinamica()
        test_oraculo_suboraculos()
        test_oraculo_robustez_baseagent()
        test_oraculo_historico_assembleia()
        test_oraculo_performance()
        test_oraculo_multiverso()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 Oráculo v9.0 migrado com sucesso para BaseAgentV2")
        print("🚀 Sistema robusto e funcional")
        
    except Exception as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        import traceback
        traceback.print_exc()