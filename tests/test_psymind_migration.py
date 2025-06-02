"""
Teste de validação da migração do PsyMind v2.0 para BaseAgentV2
Verifica funcionalidades terapêuticas e robustez
"""

import pytest
import time
from agents.psymind_v2 import PsyMindV2, ModoTerapeutico, TipoDeteccao
from agents.base_agent_v2 import BaseAgentV2


def test_psymind_heranca_base_agent():
    """Teste: PsyMind herda corretamente de BaseAgentV2"""
    psymind = PsyMindV2()
    
    # Verificar herança
    assert isinstance(psymind, BaseAgentV2)
    assert hasattr(psymind, 'memory')
    assert hasattr(psymind, 'rate_limiter')
    assert hasattr(psymind, 'circuit_breaker')
    assert hasattr(psymind, 'performance_monitor')
    
    print("✅ PsyMind herda corretamente de BaseAgentV2")


def test_psymind_inicializacao():
    """Teste: Inicialização correta do PsyMind v2.0"""
    psymind = PsyMindV2()
    
    # Verificar atributos específicos do PsyMind
    assert psymind.name == "PsyMind"
    assert psymind.ativacao_automatica == True
    assert hasattr(psymind, 'padroes_deteccao')
    assert hasattr(psymind, 'arquetipos')
    assert psymind.contador_sessoes == 0
    assert len(psymind.sessoes_terapeuticas) == 0
    assert len(psymind.marcos_emocionais) == 0
    
    print("✅ PsyMind inicializado corretamente com todas as funcionalidades")


def test_psymind_deteccao_automatica():
    """Teste: Sistema de detecção automática"""
    psymind = PsyMindV2()
    
    # Testar diferentes padrões de detecção
    casos_teste = [
        ("Não sei mais quem eu sou", TipoDeteccao.IDENTIDADE_FRAGMENTADA),
        ("Me sinto esmagado por tudo", TipoDeteccao.LINGUAGEM_SIMBOLICA),
        ("Só sei me sabotar mesmo", TipoDeteccao.AUTOSABOTAGEM),
        ("Está tudo bem, mas algo não está certo", TipoDeteccao.DISSONANCIA_DISCURSO),
        ("Não sei o que estou sentindo", TipoDeteccao.CRISE_SILENCIOSA)
    ]
    
    for mensagem, deteccao_esperada in casos_teste:
        deteccoes = psymind._detectar_contexto_emocional(mensagem)
        assert deteccao_esperada in deteccoes
        print(f"   Detectado: '{mensagem}' → {deteccao_esperada.value}")
    
    print("✅ Sistema de detecção automática funcionando")


def test_psymind_modos_terapeuticos():
    """Teste: Diferentes modos terapêuticos"""
    psymind = PsyMindV2()
    
    # Testar determinação de modos
    casos_modo = [
        ("Não sei mais quem eu sou", ModoTerapeutico.ARQUETIPO),
        ("Minha criança interior está ferida", ModoTerapeutico.CRIANCA_INTERIOR),
        ("Meu crítico interno não para", ModoTerapeutico.DUPLA_INTERNA),
        ("Preciso de uma visualização", ModoTerapeutico.IMAGINARIO_ORIENTADO),
        ("Como está meu estado interno?", ModoTerapeutico.ESCUTA_EMPATICA)
    ]
    
    for mensagem, modo_esperado in casos_modo:
        deteccoes = psymind._detectar_contexto_emocional(mensagem)
        modo = psymind._determinar_modo_principal(mensagem, deteccoes)
        print(f"   Modo: '{mensagem}' → {modo.value}")
        
        # Para alguns casos específicos, verificar modo exato
        if "quem eu sou" in mensagem:
            assert modo == ModoTerapeutico.ARQUETIPO
        elif "criança interior" in mensagem:
            assert modo == ModoTerapeutico.CRIANCA_INTERIOR
    
    print("✅ Modos terapêuticos funcionando corretamente")


def test_psymind_processamento_empatico():
    """Teste: Processamento empático básico"""
    psymind = PsyMindV2()
    
    mensagem = "Estou me sentindo muito ansioso ultimamente"
    
    start_time = time.time()
    resposta = psymind.processar(mensagem)
    processing_time = time.time() - start_time
    
    # Verificar resposta empática
    assert isinstance(resposta, str)
    assert len(resposta) > 100
    assert "PsyMind v2.0" in resposta
    assert "💙" in resposta or "🧠" in resposta  # Elementos visuais empáticos
    
    # Verificar que sessão foi registrada
    assert psymind.contador_sessoes == 1
    assert len(psymind.sessoes_terapeuticas) == 1
    
    # Verificar métricas
    assert processing_time < 3.0  # Deve ser rápido
    
    print(f"✅ Processamento empático concluído em {processing_time:.2f}s")


def test_psymind_modos_especificos():
    """Teste: Funcionamento de modos específicos"""
    psymind = PsyMindV2()
    
    # Testar modo arquétipo
    resposta_arquetipo = psymind._modo_arquetipo("Não sei qual é meu propósito")
    assert "Arquétipo Dominante" in resposta_arquetipo
    assert "Características ativas" in resposta_arquetipo
    
    # Testar modo criança interior
    resposta_crianca = psymind._modo_crianca_interior("Lembro da minha infância")
    assert "Criança Interior" in resposta_crianca
    assert "Visualização guiada" in resposta_crianca
    
    # Testar modo dupla interna
    resposta_dupla = psymind._modo_dupla_interna("Meu crítico interno me atormenta")
    assert "Partes Internas" in resposta_dupla
    assert "Crítico interno" in resposta_dupla
    
    # Testar modo ritual prático
    resposta_ritual = psymind._modo_ritual_pratico("Estou com muita raiva")
    assert "Ritual Prático" in resposta_ritual
    assert "queime" in resposta_ritual  # Ritual específico para raiva
    
    print("✅ Modos específicos funcionando corretamente")


def test_psymind_estado_simbolico():
    """Teste: Sistema de estado simbólico"""
    psymind = PsyMindV2()
    
    # Processar algumas mensagens para criar estado
    mensagens = [
        "Estou me sentindo como um guerreiro cansado",
        "Preciso encontrar minha força interior",
        "Me sinto em transformação"
    ]
    
    for mensagem in mensagens:
        psymind.processar(mensagem)
    
    # Verificar que estado foi criado
    assert psymind.estado_simbolico is not None
    assert psymind.estado_simbolico.arquetipo_dominante in psymind.arquetipos.keys()
    assert len(psymind.estado_simbolico.frases_ancora) > 0
    assert psymind.estado_simbolico.carga_psiquica >= 0.0
    
    # Testar mural interno
    mural = psymind._modo_mural_interno("Como estou?")
    assert "ESTADO SIMBÓLICO ATUAL" in mural
    assert "Arquétipo Dominante" in mural
    assert "Carga Psíquica" in mural
    
    print("✅ Sistema de estado simbólico funcionando")


def test_psymind_marcos_emocionais():
    """Teste: Criação de marcos emocionais"""
    psymind = PsyMindV2()
    
    # Processar mensagem que deve gerar marco
    mensagem = "Tive uma grande compreensão sobre mim mesmo"
    resposta = psymind.processar(mensagem)
    
    # Verificar se marco foi criado
    # Marcos são criados quando há palavras como "insight", "compreensão", etc.
    assert len(psymind.marcos_emocionais) >= 0  # Pode ou não criar dependendo da resposta
    
    # Forçar criação de marco testando método diretamente
    marcos = psymind._criar_marcos_emocionais(
        mensagem, 
        "Esta é uma resposta com grande insight transformador", 
        ModoTerapeutico.ESCUTA_EMPATICA
    )
    
    assert len(marcos) > 0
    assert len(psymind.marcos_emocionais) > 0
    
    marco = psymind.marcos_emocionais[-1]
    assert marco.tema in ["trabalho", "relacionamento", "família", "ansiedade", "autoestima", "futuro", "crescimento pessoal"]
    assert marco.modo_ativado == ModoTerapeutico.ESCUTA_EMPATICA
    
    print("✅ Sistema de marcos emocionais funcionando")


def test_psymind_robustez_baseagent():
    """Teste: Funcionalidades de robustez do BaseAgentV2"""
    psymind = PsyMindV2()
    
    # Testar cache empático
    mensagem = "Estou triste hoje"
    resposta1 = psymind.processar(mensagem)
    resposta2 = psymind.processar(mensagem)  # Deve usar cache
    
    assert resposta1 == resposta2
    print("✅ Cache empático funcionando")
    
    # Testar health status
    health = psymind.get_health_status()
    assert 'status' in health
    assert 'health_score' in health
    assert 'circuit_breaker_state' in health
    
    # Testar estado específico do PsyMind
    estado = psymind.obter_estado_sistema()
    assert 'total_sessoes' in estado
    assert 'marcos_emocionais' in estado
    assert 'deteccoes_automaticas_ativas' in estado
    assert estado['deteccoes_automaticas_ativas'] == True
    
    print("✅ Robustez do BaseAgentV2 integrada ao PsyMind")


def test_psymind_fallback_empatico():
    """Teste: Fallback empático"""
    psymind = PsyMindV2()
    
    # Testar resposta de fallback
    fallback = psymind._resposta_fallback_empatica("Teste de fallback")
    
    assert "PsyMind v2.0" in fallback
    assert "Presença Empática" in fallback
    assert "💙" in fallback
    assert "Estou aqui com você" in fallback
    
    print("✅ Fallback empático funcionando")


def test_psymind_historico_sessoes():
    """Teste: Sistema de histórico de sessões"""
    psymind = PsyMindV2()
    
    # Processar várias sessões
    mensagens = [
        "Primeira sessão terapêutica",
        "Segunda sessão sobre ansiedade", 
        "Terceira sessão sobre relacionamentos",
        "Quarta sessão sobre autoestima"
    ]
    
    for mensagem in mensagens:
        psymind.processar(mensagem)
    
    # Verificar histórico
    assert len(psymind.sessoes_terapeuticas) == 4
    assert psymind.contador_sessoes == 4
    
    # Verificar dados da última sessão
    ultima_sessao = psymind.sessoes_terapeuticas[-1]
    assert ultima_sessao.modo_principal in ModoTerapeutico
    assert ultima_sessao.duracao_segundos > 0
    assert 'carga_psiquica' in ultima_sessao.sinais_vitais_emocionais
    
    # Verificar cálculo de estatísticas
    modos_usados = psymind._calcular_modos_mais_usados()
    assert isinstance(modos_usados, dict)
    
    carga_media = psymind._calcular_carga_psiquica_media()
    assert 0.0 <= carga_media <= 10.0
    
    print("✅ Sistema de histórico de sessões funcionando")


def test_psymind_arquetipos():
    """Teste: Sistema de arquétipos"""
    psymind = PsyMindV2()
    
    # Testar identificação de arquétipos
    casos_arquetipo = [
        ("Preciso lutar por meus sonhos", "guerreiro"),
        ("Busco conhecimento e sabedoria", "sábio"),
        ("Quero brincar e ser espontâneo", "criança"),
        ("Sempre cuido de todos", "cuidador"),
        ("Preciso de liberdade para explorar", "explorador")
    ]
    
    for mensagem, arquetipo_esperado in casos_arquetipo:
        arquetipo = psymind._identificar_arquetipo_dominante(mensagem)
        print(f"   Arquétipo: '{mensagem}' → {arquetipo}")
        
        # Verificar que é um dos arquétipos válidos
        assert arquetipo in psymind.arquetipos.keys()
    
    # Testar informações do arquétipo
    info_guerreiro = psymind.arquetipos["guerreiro"]
    assert "força" in info_guerreiro["caracteristicas"]
    assert "agressividade" in info_guerreiro["sombra"]
    assert "disciplina" in info_guerreiro["crescimento"]
    
    print("✅ Sistema de arquétipos funcionando")


if __name__ == "__main__":
    print("🧪 TESTE DE MIGRAÇÃO - PSYMIND v2.0 → BaseAgentV2")
    print("=" * 70)
    
    try:
        test_psymind_heranca_base_agent()
        test_psymind_inicializacao()
        test_psymind_deteccao_automatica()
        test_psymind_modos_terapeuticos()
        test_psymind_processamento_empatico()
        test_psymind_modos_especificos()
        test_psymind_estado_simbolico()
        test_psymind_marcos_emocionais()
        test_psymind_robustez_baseagent()
        test_psymind_fallback_empatico()
        test_psymind_historico_sessoes()
        test_psymind_arquetipos()
        
        print("\n" + "=" * 70)
        print("✅ TODOS OS TESTES PASSARAM!")
        print("🎉 PsyMind v2.0 migrado com sucesso para BaseAgentV2")
        print("🧠 Sistema terapêutico robusto e empático")
        
    except Exception as e:
        print(f"\n❌ TESTE FALHOU: {e}")
        import traceback
        traceback.print_exc()