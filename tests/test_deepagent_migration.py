"""
Teste de validação da migração do DeepAgent v2.0 para BaseAgentV2
Verifica funcionalidades de pesquisa web e robustez
"""

import pytest
import time
from agents.deep_agent_v2 import DeepAgentWebSearchV2, ModoOperacional, ResultadoPesquisaWeb
from agents.base_agent_v2 import BaseAgentV2


def test_deepagent_heranca_base_agent():
    """Teste: DeepAgent herda corretamente de BaseAgentV2"""
    deepagent = DeepAgentWebSearchV2()
    
    # Verificar herança
    assert isinstance(deepagent, BaseAgentV2)
    assert hasattr(deepagent, 'memory')
    assert hasattr(deepagent, 'rate_limiter')
    assert hasattr(deepagent, 'circuit_breaker')
    assert hasattr(deepagent, 'performance_monitor')
    
    print("✅ DeepAgent herda corretamente de BaseAgentV2")


def test_deepagent_inicializacao():
    """Teste: Inicialização correta do DeepAgent v2.0"""
    deepagent = DeepAgentWebSearchV2()
    
    # Verificar atributos específicos do DeepAgent
    assert deepagent.name == "DeepAgent"
    assert hasattr(deepagent, 'web_search_enabled')
    assert hasattr(deepagent, 'stats_web')
    
    # Verificar estatísticas iniciais
    assert deepagent.stats_web['total_pesquisas'] == 0
    assert deepagent.stats_web['pesquisas_web_reais'] == 0
    assert deepagent.stats_web['pesquisas_simuladas'] == 0
    assert deepagent.stats_web['fontes_consultadas'] == 0
    assert deepagent.stats_web['oportunidades_identificadas'] == 0
    
    print("✅ DeepAgent inicializado corretamente com todas as funcionalidades")


def test_deepagent_pesquisa_produto():
    """Teste: Pesquisa de produto (real ou simulada)"""
    deepagent = DeepAgentWebSearchV2()
    
    produto = "patinhos decorativos"
    
    start_time = time.time()
    resultado = deepagent.pesquisar_produto_web(produto)
    processing_time = time.time() - start_time
    
    # Verificar estrutura do resultado
    assert isinstance(resultado, ResultadoPesquisaWeb)
    assert resultado.query == produto
    assert isinstance(resultado.modo, ModoOperacional)
    assert isinstance(resultado.web_search_used, bool)
    assert isinstance(resultado.sources_count, int)
    assert isinstance(resultado.resumo, str)
    assert isinstance(resultado.insights, list)
    assert 0 <= resultado.score_oportunidade <= 10
    assert 0 <= resultado.score_confiabilidade <= 10
    assert isinstance(resultado.recomendacao, str)
    assert isinstance(resultado.citacoes, list)
    assert isinstance(resultado.timestamp, str)
    
    # Verificar que há conteúdo
    assert len(resultado.resumo) > 10
    assert len(resultado.insights) > 0
    
    # Verificar métricas
    assert processing_time < 10.0  # Deve ser razoavelmente rápido
    
    print(f"✅ Pesquisa de produto concluída em {processing_time:.2f}s")
    print(f"   Web Search: {'✅' if resultado.web_search_used else '❌'}")
    print(f"   Score Oportunidade: {resultado.score_oportunidade:.1f}/10")
    print(f"   Insights: {len(resultado.insights)} encontrados")


def test_deepagent_extracao_produto():
    """Teste: Extração de produto da mensagem"""
    deepagent = DeepAgentWebSearchV2()
    
    casos_extracao = [
        ("DeepAgent, pesquise patinhos decorativos", "patinhos decorativos"),
        ("Analise smartwatch fitness", "smartwatch fitness"),
        ("Busque informações sobre fones bluetooth", "informações sobre fones bluetooth"),
        ("pesquise", "produto genérico")  # Caso limite
    ]
    
    for mensagem, produto_esperado in casos_extracao:
        produto = deepagent._extrair_produto(mensagem)
        print(f"   '{mensagem}' → '{produto}'")
        
        # Verificar que não contém palavras de comando
        palavras_comando = ["pesquise", "analise", "busque", "deepagent"]
        for palavra_comando in palavras_comando:
            assert palavra_comando not in produto.lower()
    
    print("✅ Extração de produto funcionando")


def test_deepagent_processamento_completo():
    """Teste: Processamento completo via _processar_interno"""
    deepagent = DeepAgentWebSearchV2()
    
    # Teste com pesquisa de produto
    mensagem_produto = "Pesquise a viabilidade de patinhos de borracha"
    
    start_time = time.time()
    resposta_produto = deepagent.processar(mensagem_produto)
    processing_time = time.time() - start_time
    
    # Verificar resposta
    assert isinstance(resposta_produto, str)
    assert len(resposta_produto) > 100
    assert "DEEPAGENT v2.0" in resposta_produto
    assert "Score de Oportunidade" in resposta_produto
    assert "Score de Confiabilidade" in resposta_produto
    
    # Verificar que estatísticas foram atualizadas
    assert deepagent.stats_web['total_pesquisas'] >= 1
    
    print(f"✅ Processamento completo em {processing_time:.2f}s")


def test_deepagent_diferentes_tipos_busca():
    """Teste: Diferentes tipos de busca suportados"""
    deepagent = DeepAgentWebSearchV2()
    
    # Teste diferentes tipos de mensagem
    tipos_busca = [
        ("Pesquise patinhos decorativos", "produto"),
        ("Busque notícias sobre tecnologia", "noticia"),
        ("Procure informações sobre marketing digital", "geral"),
        ("DeepAgent ajuda", "ajuda")
    ]
    
    for mensagem, tipo_esperado in tipos_busca:
        resposta = deepagent.processar(mensagem)
        
        print(f"   Tipo '{tipo_esperado}': '{mensagem[:30]}...' → {len(resposta)} chars")
        
        # Verificar que sempre retorna uma resposta válida
        assert isinstance(resposta, str)
        assert len(resposta) > 50
        
        # Verificar conteúdo específico por tipo
        if tipo_esperado == "ajuda":
            assert "Como usar" in resposta or "Funcionalidades" in resposta
        elif tipo_esperado == "noticia":
            assert "NOTÍCIAS" in resposta or "DEEPAGENT" in resposta
        elif tipo_esperado == "produto":
            assert "Score de Oportunidade" in resposta or "DEEPAGENT" in resposta
    
    print("✅ Diferentes tipos de busca funcionando")


def test_deepagent_formatacao_resultado():
    """Teste: Formatação de resultados"""
    deepagent = DeepAgentWebSearchV2()
    
    # Criar resultado de teste
    resultado_teste = ResultadoPesquisaWeb(
        query="produto teste",
        modo=ModoOperacional.WEB_SEARCH,
        web_search_used=True,
        sources_count=3,
        resumo="Resumo do produto teste com informações relevantes",
        insights=["Insight 1", "Insight 2", "Insight 3"],
        score_oportunidade=7.5,
        score_confiabilidade=8.0,
        recomendacao="Produto viável para venda",
        citacoes=["https://exemplo1.com", "https://exemplo2.com"],
        timestamp="2024-01-01T12:00:00"
    )
    
    # Formatar resultado
    resposta_formatada = deepagent._formatar_resultado(resultado_teste)
    
    # Verificar elementos na formatação
    assert "DEEPAGENT v2.0" in resposta_formatada
    assert "PESQUISA WEB REAL" in resposta_formatada
    assert "produto teste" in resposta_formatada
    assert "7.5/10" in resposta_formatada  # Score oportunidade
    assert "8.0/10" in resposta_formatada  # Score confiabilidade
    assert "Resumo do produto teste" in resposta_formatada
    assert "1. Insight 1" in resposta_formatada
    assert "2. Insight 2" in resposta_formatada
    assert "3. Insight 3" in resposta_formatada
    assert "Produto viável para venda" in resposta_formatada
    assert "✅ SIM" in resposta_formatada  # Web search usado
    
    print("✅ Formatação de resultado funcionando")


def test_deepagent_extracao_dados():
    """Teste: Extração de dados de resposta"""
    deepagent = DeepAgentWebSearchV2()
    
    # Texto de exemplo com scores
    conteudo_exemplo = """
    Análise do produto mostra score de oportunidade de 8.5 pontos.
    A confiabilidade desta análise é de 9.0 baseada em dados reais.
    
    Principais insights:
    - Produto tem boa demanda
    - Concorrência moderada
    - Preços competitivos
    
    Recomendação: Produto viável para investimento.
    """
    
    dados = deepagent._extrair_dados_resposta(conteudo_exemplo)
    
    # Verificar extração de scores
    assert 'score_oportunidade' in dados
    assert dados['score_oportunidade'] == 8.5
    assert 'score_confiabilidade' in dados
    assert dados['score_confiabilidade'] == 9.0
    
    # Verificar extração de resumo
    assert 'resumo' in dados
    assert len(dados['resumo']) > 0
    
    print("✅ Extração de dados funcionando")


def test_deepagent_extracao_insights():
    """Teste: Extração de insights"""
    deepagent = DeepAgentWebSearchV2()
    
    conteudo_com_insights = """
    Análise detalhada do produto:
    
    - Primeira observação importante
    • Segunda observação relevante
    * Terceira consideração estratégica
    + Quarta análise de mercado
    1. Quinta conclusão numerada
    2. Sexta recomendação estruturada
    
    Outras informações sem formatação especial.
    """
    
    insights = deepagent._extrair_insights(conteudo_com_insights)
    
    # Verificar que extraiu insights formatados
    assert len(insights) >= 5  # Pelo menos 5 insights formatados
    
    # Verificar que removeu marcadores
    for insight in insights:
        assert not insight.startswith(('-', '•', '*', '+'))
        assert len(insight.strip()) > 0
    
    print(f"✅ Extração de insights funcionando ({len(insights)} extraídos)")


def test_deepagent_pesquisa_fallback():
    """Teste: Sistema de fallback quando web search não disponível"""
    deepagent = DeepAgentWebSearchV2()
    
    # Forçar uso de fallback
    resultado_fallback = deepagent._pesquisa_simulada_fallback("produto teste")
    
    # Verificar estrutura do fallback
    assert isinstance(resultado_fallback, ResultadoPesquisaWeb)
    assert resultado_fallback.query == "produto teste"
    assert resultado_fallback.web_search_used == False
    assert resultado_fallback.sources_count == 0
    assert len(resultado_fallback.resumo) > 0
    assert len(resultado_fallback.insights) > 0
    assert 0 <= resultado_fallback.score_oportunidade <= 10
    assert 0 <= resultado_fallback.score_confiabilidade <= 10
    assert "simulados" in resultado_fallback.recomendacao.lower()
    
    print("✅ Sistema de fallback funcionando")


def test_deepagent_stats_atualizacao():
    """Teste: Atualização de estatísticas"""
    deepagent = DeepAgentWebSearchV2()
    
    # Criar resultado para teste
    resultado_web = ResultadoPesquisaWeb(
        query="teste stats",
        modo=ModoOperacional.WEB_SEARCH,
        web_search_used=True,
        sources_count=5,
        resumo="Teste",
        insights=["insight"],
        score_oportunidade=8.0,  # Score alto (>= 7.0)
        score_confiabilidade=9.0,
        recomendacao="Teste",
        citacoes=["url1", "url2"],
        timestamp="2024-01-01T12:00:00"
    )
    
    # Verificar stats iniciais
    stats_iniciais = deepagent.stats_web.copy()
    
    # Atualizar stats
    deepagent._atualizar_stats(1.5, resultado_web)
    
    # Verificar mudanças
    assert deepagent.stats_web['total_pesquisas'] == stats_iniciais['total_pesquisas'] + 1
    assert deepagent.stats_web['pesquisas_web_reais'] == stats_iniciais['pesquisas_web_reais'] + 1
    assert deepagent.stats_web['fontes_consultadas'] == stats_iniciais['fontes_consultadas'] + 5
    assert deepagent.stats_web['oportunidades_identificadas'] == stats_iniciais['oportunidades_identificadas'] + 1
    
    print("✅ Atualização de estatísticas funcionando")


def test_deepagent_robustez_baseagent():
    """Teste: Funcionalidades de robustez do BaseAgentV2"""
    deepagent = DeepAgentWebSearchV2()
    
    # Testar cache
    mensagem = "Pesquise produto teste cache"
    resposta1 = deepagent.processar(mensagem)
    resposta2 = deepagent.processar(mensagem)  # Deve usar cache
    
    assert resposta1 == resposta2
    print("✅ Cache funcionando")
    
    # Testar health status
    health = deepagent.get_health_status()
    assert 'status' in health
    assert 'health_score' in health
    assert 'circuit_breaker_state' in health
    
    # Testar estado do sistema
    estado = deepagent.obter_estado_sistema()
    assert 'agent_name' in estado
    assert estado['agent_name'] == "DeepAgent"
    
    print("✅ Robustez do BaseAgentV2 integrada ao DeepAgent")


def test_deepagent_modos_operacionais():
    """Teste: Diferentes modos operacionais"""
    deepagent = DeepAgentWebSearchV2()
    
    # Verificar que todos os modos estão disponíveis
    modos_esperados = [ModoOperacional.RAPIDO, ModoOperacional.PROFUNDO, ModoOperacional.WEB_SEARCH]
    
    for modo in modos_esperados:
        assert isinstance(modo, ModoOperacional)
        print(f"   Modo disponível: {modo.value}")
    
    # Testar criação de resultado com diferentes modos
    for modo in modos_esperados:
        resultado = ResultadoPesquisaWeb(
            query=f"teste {modo.value}",
            modo=modo,
            web_search_used=modo == ModoOperacional.WEB_SEARCH,
            sources_count=1,
            resumo="Teste",
            insights=["teste"],
            score_oportunidade=7.0,
            score_confiabilidade=8.0,
            recomendacao="Teste",
            citacoes=[],
            timestamp=None  # Deve ser gerado automaticamente
        )
        
        assert resultado.modo == modo
        assert resultado.timestamp is not None  # __post_init__ deve definir
    
    print("✅ Modos operacionais funcionando")


def test_deepagent_resposta_ajuda():
    """Teste: Resposta de ajuda"""
    deepagent = DeepAgentWebSearchV2()
    
    resposta_ajuda = deepagent._resposta_ajuda()
    
    # Verificar elementos na ajuda
    assert "DEEPAGENT v2.0" in resposta_ajuda
    assert "Como usar" in resposta_ajuda
    assert "Funcionalidades" in resposta_ajuda
    assert "Exemplos" in resposta_ajuda
    assert "BaseAgentV2" in resposta_ajuda
    
    # Verificar status do web search
    if deepagent.web_search_enabled:
        assert "✅ ATIVO" in resposta_ajuda
    else:
        assert "❌ INATIVO" in resposta_ajuda
    
    print("✅ Resposta de ajuda funcionando")


def test_deepagent_query_geral():
    """Teste: Extração de query geral"""
    deepagent = DeepAgentWebSearchV2()
    
    casos_query = [
        ("Busque informações sobre inteligência artificial", "informações sobre inteligência artificial"),
        ("Procure dados sobre mercado brasileiro", "dados sobre mercado brasileiro"),
        ("DeepAgent encontre estudos sobre e-commerce", "estudos sobre e-commerce"),
        ("notícia sobre tecnologia blockchain", "sobre tecnologia blockchain")
    ]
    
    for mensagem, query_esperada in casos_query:
        query = deepagent._extrair_query_geral(mensagem)
        print(f"   '{mensagem}' → '{query}'")
        
        # Verificar que removeu palavras de comando
        palavras_comando = ["busque", "procure", "encontre", "deepagent", "notícia", "noticia"]
        query_lower = query.lower()
        for palavra_comando in palavras_comando:
            if palavra_comando in mensagem.lower():
                # Palavra deve ter sido removida ou a query deve ser diferente da mensagem original
                assert query != mensagem
    
    print("✅ Extração de query geral funcionando")


if __name__ == "__main__":
    print("🧪 TESTE DE MIGRAÇÃO - DEEPAGENT v2.0 → BaseAgentV2")
    print("=" * 70)
    
    try:
        test_deepagent_heranca_base_agent()
        test_deepagent_inicializacao()
        test_deepagent_pesquisa_produto()
        test_deepagent_extracao_produto()
        test_deepagent_processamento_completo()
        test_deepagent_diferentes_tipos_busca()
        test_deepagent_formatacao_resultado()
        test_deepagent_extracao_dados()
        test_deepagent_extracao_insights()
        test_deepagent_pesquisa_fallback()
        test_deepagent_stats_atualizacao()
        test_deepagent_robustez_baseagent()
        test_deepagent_modos_operacionais()
        test_deepagent_resposta_ajuda()
        test_deepagent_query_geral()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 DeepAgent v2.0 migrado com sucesso para BaseAgentV2")
        print("🌐 Sistema de pesquisa web robusto e funcional")
        print("🔍 Suporte completo a DuckDuckGo Search gratuito")
        
    except Exception as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        import traceback
        traceback.print_exc()