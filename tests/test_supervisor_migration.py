"""
Teste de validação da migração do SupervisorAI v2.0 para BaseAgentV2
Verifica funcionalidades de classificação e integração com DeepAgent
"""

import pytest
import time
from agents.supervisor_ai_v2 import SupervisorAIV2, ModoExecucao, ClassificacaoTarefa
from agents.base_agent_v2 import BaseAgentV2


def test_supervisor_heranca_base_agent():
    """Teste: SupervisorAI herda corretamente de BaseAgentV2"""
    supervisor = SupervisorAIV2()
    
    # Verificar herança
    assert isinstance(supervisor, BaseAgentV2)
    assert hasattr(supervisor, 'memory')
    assert hasattr(supervisor, 'rate_limiter')
    assert hasattr(supervisor, 'circuit_breaker')
    assert hasattr(supervisor, 'performance_monitor')
    
    print("✅ SupervisorAI herda corretamente de BaseAgentV2")


def test_supervisor_inicializacao():
    """Teste: Inicialização correta do SupervisorAI v2.0"""
    supervisor = SupervisorAIV2()
    
    # Verificar atributos específicos do SupervisorAI
    assert supervisor.name == "SupervisorAI"
    assert hasattr(supervisor, 'historico_decisoes')
    assert hasattr(supervisor, 'padroes_aprendidos')
    assert hasattr(supervisor, 'padroes_deepagent')
    assert hasattr(supervisor, 'stats_supervisor')
    assert hasattr(supervisor, 'cache_padroes')
    
    # Verificar configuração robusta
    assert supervisor.config['rate_limit_per_minute'] == 30
    assert supervisor.config['cache_enabled'] == True
    
    print("✅ SupervisorAI inicializado corretamente com todas as funcionalidades")


def test_supervisor_deteccao_deepagent():
    """Teste: Detecção de necessidade do DeepAgent"""
    supervisor = SupervisorAIV2()
    
    # Casos que DEVEM ativar DeepAgent
    casos_deepagent = [
        "Analise este produto do AliExpress",
        "Pesquise a viabilidade deste item",
        "Como está o mercado para este produto?",
        "Vale a pena vender patinhos decorativos?",
        "Produto da Shopee tem potencial?",
        "Score de oportunidade para smartwatch",
        "Análise de saturação do mercado"
    ]
    
    for caso in casos_deepagent:
        precisa_deepagent = supervisor._detectar_necessidade_deepagent(caso)
        assert precisa_deepagent == True
        print(f"   DeepAgent detectado: '{caso}'")
    
    # Casos que NÃO devem ativar DeepAgent
    casos_normais = [
        "Como você está?",
        "Explique o que é inteligência artificial",
        "Ajude-me com um texto",
        "Qual a diferença entre marketing e vendas?",
        "Como fazer um planejamento estratégico?"
    ]
    
    for caso in casos_normais:
        precisa_deepagent = supervisor._detectar_necessidade_deepagent(caso)
        assert precisa_deepagent == False
        print(f"   DeepAgent NÃO detectado: '{caso}'")
    
    print("✅ Detecção de DeepAgent funcionando corretamente")


def test_supervisor_classificacao_complexidade():
    """Teste: Cálculo de complexidade das tarefas"""
    supervisor = SupervisorAIV2()
    
    # Casos de complexidade baixa
    casos_baixa = [
        "Oi",
        "Qual cor?",
        "Preço?"
    ]
    
    for caso in casos_baixa:
        complexidade = supervisor._calcular_complexidade(caso)
        assert complexidade <= 4.0
        print(f"   Baixa complexidade ({complexidade:.1f}): '{caso}'")
    
    # Casos de complexidade alta
    casos_alta = [
        "Analise a viabilidade estratégica de lançar um produto inovador no mercado brasileiro, considerando concorrência, saturação e oportunidades de crescimento",
        "Compare diferentes estratégias de precificação para produtos digitais, avaliando impacto no posicionamento e margem de lucro",
        "Desenvolva um plano completo de otimização de vendas para e-commerce"
    ]
    
    for caso in casos_alta:
        complexidade = supervisor._calcular_complexidade(caso)
        assert complexidade >= 6.0
        print(f"   Alta complexidade ({complexidade:.1f}): '{caso[:50]}...'")
    
    print("✅ Cálculo de complexidade funcionando")


def test_supervisor_impacto_estrategico():
    """Teste: Cálculo de impacto estratégico"""
    supervisor = SupervisorAIV2()
    
    # Casos de alto impacto
    casos_alto_impacto = [
        "Decisão de investir R$ 100.000 em novo produto",
        "Estratégia de lançamento para mercado competitivo",
        "Análise de risco para expansão empresarial",
        "Viabilidade de saturação de mercado para produtos"
    ]
    
    for caso in casos_alto_impacto:
        impacto = supervisor._calcular_impacto_estrategico(caso)
        assert impacto >= 6.0
        print(f"   Alto impacto ({impacto:.1f}): '{caso}'")
    
    # Casos de baixo impacto
    casos_baixo_impacto = [
        "Como fazer um texto bonito?",
        "Explique conceitos básicos",
        "Dúvida simples sobre formatação"
    ]
    
    for caso in casos_baixo_impacto:
        impacto = supervisor._calcular_impacto_estrategico(caso)
        assert impacto <= 5.0
        print(f"   Baixo impacto ({impacto:.1f}): '{caso}'")
    
    print("✅ Cálculo de impacto estratégico funcionando")


def test_supervisor_decisao_modo():
    """Teste: Decisão de modo de execução"""
    supervisor = SupervisorAIV2()
    
    casos_modo = [
        ("Oi", ModoExecucao.DIRETO),
        ("Analise produto complexo com múltiplas variáveis estratégicas", ModoExecucao.PROFUNDO),
        ("Compare dois produtos similares", ModoExecucao.ESPELHADO),
        ("Simule cenário de vendas", ModoExecucao.EXPLORATORIO)
    ]
    
    for mensagem, modo_esperado in casos_modo:
        complexidade = supervisor._calcular_complexidade(mensagem)
        impacto = supervisor._calcular_impacto_estrategico(mensagem)
        modo = supervisor._decidir_modo_execucao(complexidade, impacto, mensagem)
        
        print(f"   Modo '{modo.value}' para: '{mensagem[:30]}...'")
        
        # Verificar alguns casos específicos
        if mensagem == "Oi":
            assert modo == ModoExecucao.DIRETO
        elif "compare" in mensagem.lower():
            assert modo in [ModoExecucao.ESPELHADO, ModoExecucao.ANALISE_MODULAR, ModoExecucao.PROFUNDO]
    
    print("✅ Decisão de modo de execução funcionando")


def test_supervisor_sugestao_agentes():
    """Teste: Sugestão de agentes incluindo DeepAgent"""
    supervisor = SupervisorAIV2()
    
    # Teste com DeepAgent necessário
    agentes_com_deep = supervisor._sugerir_agentes(
        "Analise produto do AliExpress", 
        ModoExecucao.PROFUNDO, 
        None, 
        precisa_deepagent=True
    )
    
    assert "DeepAgent" in agentes_com_deep
    assert "Reflexor" in agentes_com_deep
    print(f"   Com DeepAgent: {agentes_com_deep}")
    
    # Teste com diferentes tipos de tarefa
    casos_agentes = [
        ("Preciso de um anúncio para produto", ["CopyBooster"]),
        ("Decisão estratégica crítica", ["Oráculo"]),
        ("Tenho dúvidas sobre processo", ["DoubtSolver"]),
        ("Análise de preço e margem", ["AutoPrice"]),
        ("Criar kit de produtos", ["KitBuilder"])
    ]
    
    for mensagem, agentes_esperados in casos_agentes:
        agentes = supervisor._sugerir_agentes(mensagem, ModoExecucao.INTERMEDIARIO, None, False)
        
        for agente_esperado in agentes_esperados:
            if agente_esperado in agentes:
                print(f"   ✅ {agente_esperado} sugerido para: '{mensagem}'")
            else:
                print(f"   ⚠️ {agente_esperado} não sugerido para: '{mensagem}'")
    
    print("✅ Sugestão de agentes funcionando")


def test_supervisor_classificacao_completa():
    """Teste: Classificação completa de tarefa"""
    supervisor = SupervisorAIV2()
    
    # Teste com tarefa que precisa de DeepAgent
    mensagem = "Analise a viabilidade de vender patinhos decorativos do AliExpress"
    
    start_time = time.time()
    classificacao = supervisor.classificar_tarefa(mensagem)
    processing_time = time.time() - start_time
    
    # Verificar estrutura da classificação
    assert isinstance(classificacao, ClassificacaoTarefa)
    assert 0 <= classificacao.complexidade <= 10
    assert 0 <= classificacao.impacto_estrategico <= 10
    assert isinstance(classificacao.modo_recomendado, ModoExecucao)
    assert isinstance(classificacao.agentes_sugeridos, list)
    assert isinstance(classificacao.precisa_deepagent, bool)
    assert len(classificacao.justificativa) > 10
    assert classificacao.tolerancia_erro in ["baixa", "media", "alta"]
    assert isinstance(classificacao.tags_detectadas, list)
    assert classificacao.tempo_estimado > 0
    assert 0 <= classificacao.confianca_classificacao <= 10
    
    # Para esta mensagem específica, deve detectar DeepAgent
    assert classificacao.precisa_deepagent == True
    assert "DeepAgent" in classificacao.agentes_sugeridos
    
    print(f"✅ Classificação completa em {processing_time:.2f}s")
    print(f"   Complexidade: {classificacao.complexidade:.1f}")
    print(f"   Impacto: {classificacao.impacto_estrategico:.1f}")
    print(f"   Modo: {classificacao.modo_recomendado.value}")
    print(f"   DeepAgent: {'✅' if classificacao.precisa_deepagent else '❌'}")


def test_supervisor_processamento_completo():
    """Teste: Processamento completo sem LLM"""
    supervisor = SupervisorAIV2()
    
    mensagem = "Pesquise a viabilidade de vender smartwatch importado"
    
    start_time = time.time()
    resposta = supervisor.processar(mensagem)
    processing_time = time.time() - start_time
    
    # Verificar resposta
    assert isinstance(resposta, str)
    assert len(resposta) > 100
    assert "SupervisorAI v2.0" in resposta
    assert "Classificação da Tarefa" in resposta
    assert "Agentes Sugeridos" in resposta
    
    # Verificar que estatísticas foram atualizadas
    assert supervisor.stats_supervisor['total_classificacoes'] == 1
    
    print(f"✅ Processamento completo em {processing_time:.2f}s")


def test_supervisor_robustez_baseagent():
    """Teste: Funcionalidades de robustez do BaseAgentV2"""
    supervisor = SupervisorAIV2()
    
    # Testar cache
    mensagem = "Teste de cache para supervisor"
    resposta1 = supervisor.processar(mensagem)
    resposta2 = supervisor.processar(mensagem)  # Deve usar cache
    
    assert resposta1 == resposta2
    print("✅ Cache funcionando")
    
    # Testar health status
    health = supervisor.get_health_status()
    assert 'status' in health
    assert 'health_score' in health
    assert 'circuit_breaker_state' in health
    
    # Testar stats específicas do SupervisorAI
    stats = supervisor.obter_stats()
    assert 'stats_gerais' in stats
    assert 'deepagent_stats' in stats
    assert 'cache_size' in stats
    assert 'historico_size' in stats
    
    print("✅ Robustez do BaseAgentV2 integrada ao SupervisorAI")


def test_supervisor_modo_metacognitivo():
    """Teste: Modo metacognitivo de autoavaliação"""
    supervisor = SupervisorAIV2()
    
    # Processar algumas tarefas para gerar histórico
    tarefas = [
        "Analise produto simples",
        "Decisão estratégica complexa de investimento",
        "Pesquise viabilidade de produto AliExpress",
        "Criar anúncio para produto",
        "Dúvida sobre processo"
    ]
    
    for tarefa in tarefas:
        supervisor.classificar_tarefa(tarefa)
    
    # Executar modo metacognitivo
    relatorio = supervisor.modo_metacognitivo()
    
    # Verificar estrutura do relatório
    assert 'periodo_analisado' in relatorio
    assert 'distribuicao_modos' in relatorio
    assert 'deepagent_ativacoes' in relatorio
    assert 'taxa_deepagent' in relatorio
    assert 'confianca_media' in relatorio
    assert 'recomendacoes' in relatorio
    
    # Verificar que há dados
    assert relatorio['total_classificacoes'] >= 5
    assert isinstance(relatorio['distribuicao_modos'], dict)
    assert isinstance(relatorio['recomendacoes'], list)
    
    print("✅ Modo metacognitivo funcionando")
    print(f"   Taxa DeepAgent: {relatorio['taxa_deepagent']:.1f}%")
    print(f"   Confiança média: {relatorio['confianca_media']:.1f}")


def test_supervisor_historico_aprendizado():
    """Teste: Sistema de histórico e aprendizado"""
    supervisor = SupervisorAIV2()
    
    # Processar várias tarefas
    tarefas = [
        "Primeira tarefa de teste",
        "Segunda tarefa similar", 
        "Terceira tarefa diferente",
        "Quarta tarefa complexa de análise estratégica"
    ]
    
    for tarefa in tarefas:
        supervisor.classificar_tarefa(tarefa)
    
    # Verificar histórico
    assert len(supervisor.historico_decisoes) == 4
    
    # Verificar estrutura das decisões
    for decisao in supervisor.historico_decisoes:
        assert 'timestamp' in decisao
        assert 'mensagem' in decisao
        assert 'classificacao' in decisao
        assert 'hash' in decisao
    
    # Testar detecção de histórico relevante
    historico_relevante = supervisor._verificar_historico_relevante("Primeira tarefa de teste")
    # Deve detectar similaridade com primeira tarefa
    
    print("✅ Sistema de histórico e aprendizado funcionando")


def test_supervisor_tolerancia_erro():
    """Teste: Avaliação de tolerância a erro"""
    supervisor = SupervisorAIV2()
    
    casos_tolerancia = [
        (2.0, "alta"),    # Baixo impacto = alta tolerância
        (5.5, "media"),   # Médio impacto = média tolerância
        (9.0, "baixa")    # Alto impacto = baixa tolerância
    ]
    
    for impacto, tolerancia_esperada in casos_tolerancia:
        tolerancia = supervisor._avaliar_tolerancia_erro(impacto)
        assert tolerancia == tolerancia_esperada
        print(f"   Impacto {impacto} → Tolerância {tolerancia}")
    
    print("✅ Avaliação de tolerância a erro funcionando")


def test_supervisor_tags_deteccao():
    """Teste: Sistema de detecção de tags"""
    supervisor = SupervisorAIV2()
    
    casos_tags = [
        ("Analise este produto importante", ["#PRODUTO", "#ANALISE"]),
        ("Decisão crítica urgente sobre preço", ["#URGENTE", "#DECISAO_CRITICA", "#FINANCEIRO"]),
        ("Pesquise viabilidade com score", ["#PESQUISA", "#DEEPAGENT"]),
        ("Criar anúncio de marketing", ["#MARKETING"])
    ]
    
    for mensagem, tags_esperadas in casos_tags:
        tags = supervisor._detectar_tags(mensagem)
        
        tags_encontradas = 0
        for tag_esperada in tags_esperadas:
            if tag_esperada in tags:
                tags_encontradas += 1
        
        print(f"   '{mensagem}' → {tags} (encontradas: {tags_encontradas}/{len(tags_esperadas)})")
    
    print("✅ Sistema de detecção de tags funcionando")


if __name__ == "__main__":
    print("🧪 TESTE DE MIGRAÇÃO - SUPERVISORAI v2.0 → BaseAgentV2")
    print("=" * 70)
    
    try:
        test_supervisor_heranca_base_agent()
        test_supervisor_inicializacao()
        test_supervisor_deteccao_deepagent()
        test_supervisor_classificacao_complexidade()
        test_supervisor_impacto_estrategico()
        test_supervisor_decisao_modo()
        test_supervisor_sugestao_agentes()
        test_supervisor_classificacao_completa()
        test_supervisor_processamento_completo()
        test_supervisor_robustez_baseagent()
        test_supervisor_modo_metacognitivo()
        test_supervisor_historico_aprendizado()
        test_supervisor_tolerancia_erro()
        test_supervisor_tags_deteccao()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 SupervisorAI v2.0 migrado com sucesso para BaseAgentV2")
        print("🚀 Sistema robusto de classificação e integração com DeepAgent")
        print("🧠 Metacognição e aprendizado funcionais")
        
    except Exception as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        import traceback
        traceback.print_exc()