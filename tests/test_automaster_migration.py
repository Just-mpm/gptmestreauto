"""
Teste de validação da migração do AutoMaster v4.0 para BaseAgentV2
Verifica funcionalidades de autonomia econômica e robustez
"""

import pytest
import time
from agents.automaster_v2 import AutoMasterV2, PerfilProfissional, FaseVida, TipoDesafio, ModoPrincipal
from agents.base_agent_v2 import BaseAgentV2


def test_automaster_heranca_base_agent():
    """Teste: AutoMaster herda corretamente de BaseAgentV2"""
    automaster = AutoMasterV2()
    
    # Verificar herança
    assert isinstance(automaster, BaseAgentV2)
    assert hasattr(automaster, 'memory')
    assert hasattr(automaster, 'rate_limiter')
    assert hasattr(automaster, 'circuit_breaker')
    assert hasattr(automaster, 'performance_monitor')
    
    print("✅ AutoMaster herda corretamente de BaseAgentV2")


def test_automaster_inicializacao():
    """Teste: Inicialização correta do AutoMaster v4.0"""
    automaster = AutoMasterV2()
    
    # Verificar atributos específicos do AutoMaster
    assert automaster.name == "AutoMaster"
    assert len(automaster.modulos_avancados) == 32
    assert automaster.modo_antifragil_ativo == True
    assert automaster.sistema_backup_ativo == True
    assert automaster.contador_planos == 0
    assert len(automaster.planos_estrategicos) == 0
    
    # Verificar configuração robusta
    assert automaster.config['rate_limit_per_minute'] == 30
    assert automaster.config['cache_ttl_seconds'] == 900  # 15 minutos
    assert automaster.config['timeout_seconds'] == 60  # Mais tempo para processamento complexo
    
    print("✅ AutoMaster inicializado com 32 módulos avançados")


def test_automaster_modulos_avancados():
    """Teste: Sistema de 32 módulos avançados"""
    automaster = AutoMasterV2()
    
    # Verificar que todos os 32 módulos foram criados
    assert len(automaster.modulos_avancados) == 32
    
    # Verificar alguns módulos específicos
    modulos_criticos = [1, 14, 26, 32]  # Narrativa, Gêmeo Pro, Antifrágil, Socorro Total
    
    for modulo_id in modulos_criticos:
        assert modulo_id in automaster.modulos_avancados
        modulo = automaster.modulos_avancados[modulo_id]
        assert modulo.ativo == True
        assert isinstance(modulo.perfis_alvo, list)
        assert len(modulo.funcionalidades) > 0
        assert 1 <= modulo.nivel_complexidade <= 5
    
    # Verificar módulos específicos
    modulo_narrativa = automaster.modulos_avancados[1]
    assert "Narrativa Profissional" in modulo_narrativa.nome
    
    modulo_antifragil = automaster.modulos_avancados[26]
    assert "Antifrágil" in modulo_antifragil.nome
    
    modulo_socorro = automaster.modulos_avancados[32]
    assert "Socorro Total" in modulo_socorro.nome
    
    print("✅ Sistema de 32 módulos avançados funcionando")


def test_automaster_analise_comando():
    """Teste: Análise de comandos específicos"""
    automaster = AutoMasterV2()
    
    # Testar diferentes tipos de comando
    casos_comando = [
        ("Quero criar um curso digital", "curso_digital"),
        ("Preciso viajar trabalhando", "nomade_digital"),
        ("Como me blindar contra crises?", "modo_antifragil"),
        ("Organize minhas finanças", "organizacao_financeira"),
        ("Estou esgotado, preciso otimizar minha energia", "energia_otima"),
        ("Quero criar uma comunidade", "comunidade_propria"),
        ("Preciso de um backup total", "backup_total"),
        ("Simulação de faturamento", "simulacao_faturamento")
    ]
    
    for mensagem, tipo_esperado in casos_comando:
        analise = automaster._analisar_comando_automaster(mensagem)
        assert analise['tipo'] == tipo_esperado
        assert 'parametros' in analise
        print(f"   Comando: '{mensagem}' → {tipo_esperado}")
    
    print("✅ Análise de comandos funcionando")


def test_automaster_perfil_usuario():
    """Teste: Sistema de perfil de usuário"""
    automaster = AutoMasterV2()
    
    # Testar inferência de perfil
    casos_perfil = [
        ("Quero criar um curso online", PerfilProfissional.EDUCADOR),
        ("Sou consultor e preciso crescer", PerfilProfissional.CONSULTOR),
        ("Trabalho com conteúdo criativo", PerfilProfissional.CRIADOR),
        ("Atuo como terapeuta", PerfilProfissional.TERAPEUTA)
    ]
    
    for mensagem, perfil_esperado in casos_perfil:
        perfil_inferido = automaster._inferir_perfil_da_mensagem(mensagem)
        assert perfil_inferido['perfil'] == perfil_esperado
        assert perfil_inferido['fase'] in FaseVida
        assert len(perfil_inferido['objetivos']) > 0
        print(f"   Perfil: '{mensagem}' → {perfil_esperado.value}")
    
    # Testar criação de perfil completo
    perfil = automaster._extrair_perfil_usuario({}, "Sou educador iniciante")
    assert isinstance(perfil.perfil_profissional, PerfilProfissional)
    assert isinstance(perfil.fase_vida, FaseVida)
    assert len(perfil.objetivos_principais) > 0
    assert len(perfil.desafios_atuais) > 0
    
    print("✅ Sistema de perfil de usuário funcionando")


def test_automaster_selecao_modulos():
    """Teste: Seleção inteligente de módulos"""
    automaster = AutoMasterV2()
    
    # Criar perfil de teste
    from agents.automaster_v2 import PerfilUsuario
    perfil = PerfilUsuario(
        nome="Teste",
        perfil_profissional=PerfilProfissional.EDUCADOR,
        fase_vida=FaseVida.CRESCIMENTO,
        objetivos_principais=["autonomia financeira"],
        preferencia_exposicao="media",
        tempo_disponivel="parcial",
        conhecimento_acumulado="intermediario",
        desafios_atuais=[TipoDesafio.ESTRATEGICO],
        recursos_disponiveis={"tempo": "limitado"}
    )
    
    # Testar seleção para diferentes tipos
    tipos_teste = ["curso_digital", "nomade_digital", "modo_antifragil"]
    
    for tipo in tipos_teste:
        modulos = automaster._selecionar_modulos_relevantes(tipo, perfil, {})
        
        # Verificar que módulos foram selecionados
        assert len(modulos) > 0
        assert len(modulos) <= 8  # Limitado a 8 módulos
        
        # Verificar que módulos base estão incluídos
        modulos_base = [1, 12, 26, 29, 30]  # Narrativa, Autodiagnóstico, Antifrágil, Finanças, Energia
        for modulo_base in modulos_base:
            assert modulo_base in modulos
        
        print(f"   Tipo '{tipo}': {len(modulos)} módulos selecionados")
    
    print("✅ Seleção inteligente de módulos funcionando")


def test_automaster_processamento_completo():
    """Teste: Processamento completo sem LLM"""
    automaster = AutoMasterV2()
    
    mensagem = "Quero criar um curso digital sobre minha área de expertise"
    
    start_time = time.time()
    resposta = automaster.processar(mensagem)
    processing_time = time.time() - start_time
    
    # Verificar resposta
    assert isinstance(resposta, str)
    assert len(resposta) > 100
    assert "AutoMaster v4.0" in resposta
    assert "Plano Estratégico" in resposta
    
    # Verificar que plano foi criado
    assert automaster.contador_planos == 1
    assert len(automaster.planos_estrategicos) == 1
    
    # Verificar estatísticas
    assert automaster.stats['planos_estrategicos_criados'] == 1
    assert automaster.stats['usuarios_atendidos'] == 1
    
    print(f"✅ Processamento completo em {processing_time:.2f}s")


def test_automaster_plano_estrategico():
    """Teste: Criação de plano estratégico"""
    automaster = AutoMasterV2()
    
    # Criar perfil de teste
    from agents.automaster_v2 import PerfilUsuario
    perfil = PerfilUsuario(
        nome="Teste Educador",
        perfil_profissional=PerfilProfissional.EDUCADOR,
        fase_vida=FaseVida.CRESCIMENTO,
        objetivos_principais=["criar curso digital", "autonomia financeira"],
        preferencia_exposicao="alta",
        tempo_disponivel="integral",
        conhecimento_acumulado="avancado",
        desafios_atuais=[TipoDesafio.ESTRATEGICO, TipoDesafio.TECNICO],
        recursos_disponiveis={"investimento": "medio", "tempo": "adequado"}
    )
    
    modulos = [1, 4, 17, 8, 26]  # Módulos para curso digital
    
    # Criar plano estratégico
    plano = automaster._criar_plano_estrategico_completo(
        perfil, modulos, "curso_digital", {"tema": "expertise"}
    )
    
    # Verificar estrutura do plano
    assert plano.id.startswith("automaster_plano_")
    assert plano.usuario == perfil
    assert plano.modulos_ativados == modulos
    assert len(plano.estrategia_principal) > 50
    assert len(plano.plano_90_dias) > 100
    assert len(plano.plano_1_ano) > 50
    assert len(plano.recursos_necessarios) > 0
    assert len(plano.cronograma) > 0
    
    print("✅ Criação de plano estratégico funcionando")


def test_automaster_simulacao_faturamento():
    """Teste: Simulação de faturamento multicanal"""
    automaster = AutoMasterV2()
    
    # Criar perfil de teste
    from agents.automaster_v2 import PerfilUsuario
    perfil = PerfilUsuario(
        nome="Teste Consultor",
        perfil_profissional=PerfilProfissional.CONSULTOR,
        fase_vida=FaseVida.EXPANSAO,
        objetivos_principais=["aumentar faturamento"],
        preferencia_exposicao="baixa",
        tempo_disponivel="integral",
        conhecimento_acumulado="expert",
        desafios_atuais=[TipoDesafio.FINANCEIRO],
        recursos_disponiveis={"clientes": "poucos", "expertise": "alta"}
    )
    
    # Executar simulação
    simulacao = automaster._executar_simulacao_faturamento(perfil, {"periodo": "anual"})
    
    # Verificar estrutura da simulação
    assert len(simulacao.produtos_servicos) > 0
    assert simulacao.projecao_mensal > 0
    assert simulacao.projecao_anual > 0
    assert simulacao.cenario_conservador < simulacao.projecao_anual
    assert simulacao.cenario_otimista > simulacao.projecao_anual
    assert len(simulacao.pontos_criticos) > 0
    assert len(simulacao.canais_venda) > 0
    
    # Verificar valores específicos para consultor
    assert "consultoria" in simulacao.produtos_servicos
    assert simulacao.produtos_servicos["consultoria"] >= 300
    
    print("✅ Simulação de faturamento funcionando")


def test_automaster_modo_antifragil():
    """Teste: Modo antifrágil"""
    automaster = AutoMasterV2()
    
    # Criar perfil de teste
    from agents.automaster_v2 import PerfilUsuario
    perfil = PerfilUsuario(
        nome="Teste Vulnerável",
        perfil_profissional=PerfilProfissional.AUTONOMO,
        fase_vida=FaseVida.ESTAGNACAO,
        objetivos_principais=["proteção contra crises"],
        preferencia_exposicao="baixa",
        tempo_disponivel="limitado",
        conhecimento_acumulado="intermediario",
        desafios_atuais=[TipoDesafio.FINANCEIRO, TipoDesafio.ESTRATEGICO],
        recursos_disponiveis={"reservas": "baixas"}
    )
    
    # Ativar modo antifrágil
    resposta = automaster._ativar_modo_antifragil(perfil, {"urgencia": "alta"})
    
    # Verificar conteúdo da resposta
    assert "MODO ANTIFRÁGIL ATIVADO" in resposta
    assert "DIVERSIFICAÇÃO DE RISCOS" in resposta
    assert "SISTEMAS DE BACKUP" in resposta
    assert "ADAPTABILIDADE" in resposta
    assert "CRESCIMENTO COM CRISE" in resposta
    assert "PLANO DE AÇÃO IMEDIATO" in resposta
    assert "3 fontes de renda" in resposta
    
    print("✅ Modo antifrágil funcionando")


def test_automaster_robustez_baseagent():
    """Teste: Funcionalidades de robustez do BaseAgentV2"""
    automaster = AutoMasterV2()
    
    # Testar cache estratégico
    mensagem = "Quero criar um negócio sustentável"
    resposta1 = automaster.processar(mensagem)
    resposta2 = automaster.processar(mensagem)  # Deve usar cache
    
    assert resposta1 == resposta2
    print("✅ Cache estratégico funcionando")
    
    # Testar health status
    health = automaster.get_health_status()
    assert 'status' in health
    assert 'health_score' in health
    assert 'circuit_breaker_state' in health
    
    # Testar diagnóstico específico do AutoMaster
    diagnostico = automaster.diagnosticar_automaster()
    assert 'version' in diagnostico
    assert '4.0_Autonomia_Economica_Estrategica_V2' in diagnostico['version']
    assert diagnostico['modulos_disponiveis'] == 32
    assert diagnostico['modulos_ativos'] == 32
    assert 'robustez' in diagnostico
    assert 'integracoes' in diagnostico
    
    print("✅ Robustez do BaseAgentV2 integrada ao AutoMaster")


def test_automaster_historico_persistente():
    """Teste: Sistema de histórico persistente"""
    automaster = AutoMasterV2()
    
    # Processar alguns planos
    mensagens = [
        "Quero criar um curso digital",
        "Preciso de simulação de faturamento",
        "Como me blindar contra crises?"
    ]
    
    for mensagem in mensagens:
        automaster.processar(mensagem)
    
    # Verificar histórico
    assert len(automaster.planos_estrategicos) >= 2  # Alguns comandos criam planos
    assert automaster.contador_planos >= 2
    
    # Testar salvamento persistente
    automaster._salvar_historico_persistente()
    assert 'historico_automaster' in automaster.memory.context
    
    # Testar obtenção de histórico
    historico = automaster.obter_historico_planos(2)
    assert "HISTÓRICO DOS ÚLTIMOS" in historico
    assert "automaster_plano_" in historico
    
    print("✅ Sistema de histórico persistente funcionando")


def test_automaster_listagem_modulos():
    """Teste: Listagem de módulos disponíveis"""
    automaster = AutoMasterV2()
    
    # Testar listagem
    lista = automaster.listar_modulos_disponiveis()
    
    assert "32 MÓDULOS AVANÇADOS" in lista
    assert "Narrativa Profissional" in lista
    assert "Modo Antifrágil" in lista
    assert "Modo Socorro Total" in lista
    assert "⭐" in lista  # Indicadores de complexidade
    
    # Verificar que todos os 32 módulos estão listados
    linhas = lista.split('\n')
    modulos_listados = [l for l in linhas if l.strip().startswith('✅') or l.strip().startswith('❌')]
    assert len(modulos_listados) == 32
    
    print("✅ Listagem de módulos funcionando")


def test_automaster_cleanup():
    """Teste: Limpeza de recursos"""
    automaster = AutoMasterV2()
    
    # Criar alguns dados
    automaster.processar("Teste de limpeza")
    
    # Verificar que há dados
    assert len(automaster.planos_estrategicos) > 0
    
    # Testar cleanup
    automaster.cleanup_resources()
    
    # Verificar que dados foram salvos na memória persistente
    assert 'historico_automaster' in automaster.memory.context
    
    print("✅ Limpeza de recursos funcionando")


if __name__ == "__main__":
    print("🧪 TESTE DE MIGRAÇÃO - AUTOMASTER v4.0 → BaseAgentV2")
    print("=" * 70)
    
    try:
        test_automaster_heranca_base_agent()
        test_automaster_inicializacao()
        test_automaster_modulos_avancados()
        test_automaster_analise_comando()
        test_automaster_perfil_usuario()
        test_automaster_selecao_modulos()
        test_automaster_processamento_completo()
        test_automaster_plano_estrategico()
        test_automaster_simulacao_faturamento()
        test_automaster_modo_antifragil()
        test_automaster_robustez_baseagent()
        test_automaster_historico_persistente()
        test_automaster_listagem_modulos()
        test_automaster_cleanup()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 AutoMaster v4.0 migrado com sucesso para BaseAgentV2")
        print("🚀 Sistema de autonomia econômica robusto e escalável")
        print("💼 32 módulos avançados operacionais")
        
    except Exception as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        import traceback
        traceback.print_exc()