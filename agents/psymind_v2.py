"""
PsyMind v2.0 - Agente Terapêutico do GPT Mestre Autônomo
Migrado para BaseAgentV2 com recursos avançados de robustez
Estrutura simbólica + ação prática + autodetecção de contexto emocional
"""

import json
import re
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import uuid

from agents.base_agent_v2 import BaseAgentV2

# Logger com fallback
try:
    from utils.logger import get_logger
except ImportError:
    class SimpleLogger:
        def __init__(self, name): self.name = name
        def info(self, msg): print(f"[INFO] {self.name}: {msg}")
        def warning(self, msg): print(f"[WARNING] {self.name}: {msg}")
        def error(self, msg): print(f"[ERROR] {self.name}: {msg}")
        def debug(self, msg): print(f"[DEBUG] {self.name}: {msg}")
    def get_logger(name): return SimpleLogger(name)

logger = get_logger(__name__)

class ModoTerapeutico(Enum):
    """Modos operacionais do PsyMind"""
    ESCUTA_EMPATICA = "escuta_empatica"
    INVESTIGACAO = "investigacao"
    NARRATIVO = "narrativo"
    INTEGRADOR = "integrador"
    CATARTICO = "catartico"
    ARVORE_SENTIDO = "arvore_sentido"
    ESPELHO_RETROATIVO = "espelho_retroativo"
    APOIO_CRISE = "apoio_crise"
    CRIANCA_INTERIOR = "crianca_interior"
    ARQUETIPO = "arquetipo"
    TRANSCRICAO_EMOCIONAL = "transcricao_emocional"
    ENCERRAMENTO_CICLO = "encerramento_ciclo"
    AUTOCOMPAIXAO = "autocompaixao"
    DUPLA_INTERNA = "dupla_interna"
    PACTO_EMOCIONAL = "pacto_emocional"
    IMAGINARIO_ORIENTADO = "imaginario_orientado"
    RITUAL_PRATICO = "ritual_pratico"
    REFLEXAO_IMPACTO = "reflexao_impacto"
    SILENCIO_INTERNO = "silencio_interno"
    TERCEIRA_PESSOA = "terceira_pessoa"
    ENCONTRO_PARTES = "encontro_partes"
    ESPELHO_FRATURADO = "espelho_fraturado"
    MURAL_INTERNO = "mural_interno"

class TipoDeteccao(Enum):
    """Tipos de detecção automática"""
    LINGUAGEM_SIMBOLICA = "linguagem_simbolica"
    PADRAO_EMOCIONAL = "padrao_emocional"
    REPETICAO_TEMATICA = "repeticao_tematica"
    DISSONANCIA_DISCURSO = "dissonancia_discurso"
    CRISE_SILENCIOSA = "crise_silenciosa"
    AUTOSABOTAGEM = "autosabotagem"
    IDENTIDADE_FRAGMENTADA = "identidade_fragmentada"

@dataclass
class MarcoEmocional:
    """Registro de marco emocional"""
    id: str
    timestamp: datetime
    tema: str
    sentimento_principal: str
    insight: str
    modo_ativado: ModoTerapeutico
    arquetipo_identificado: Optional[str] = None
    pacto_criado: Optional[str] = None
    ritual_sugerido: Optional[str] = None
    progresso_score: float = 0.0

@dataclass
class SessaoTerapeutica:
    """Registro de sessão terapêutica"""
    id: str
    timestamp: datetime
    contexto_detectado: str
    modo_principal: ModoTerapeutico
    submodos_ativados: List[str]
    marcos_criados: List[str]
    deteccoes_automaticas: List[TipoDeteccao]
    sinais_vitais_emocionais: Dict[str, float]
    duracao_segundos: float = 0.0

@dataclass 
class EstadoSimbolicoAtual:
    """Estado simbólico atual do usuário"""
    arquetipo_dominante: str
    frases_ancora: List[str]
    pactos_ativos: List[str]
    ciclos_abertos: List[str]
    subpersonalidades_ativas: Dict[str, str]
    carga_psiquica: float
    tendencia_evolutiva: str

class PsyMindV2(BaseAgentV2):
    """
    PsyMind v2.0 - Agente Terapêutico Avançado (Migrado para BaseAgentV2)
    
    Agente especializado em:
    - Escuta profunda e acompanhamento emocional
    - Autodetecção de contextos emocionais/psicológicos
    - Ativação automática de modos terapêuticos específicos
    - Estrutura simbólica e ação prática
    - Integração com outros agentes especializados
    
    Aproveitando recursos do BaseAgentV2:
    - Rate limiting automático
    - Circuit breaker para resiliência
    - Retry com backoff exponencial
    - Fallback robusto
    - Monitoramento de saúde
    """
    
    def __init__(self, **kwargs):
        # Configurações específicas do PsyMind
        psymind_config = {
            'max_retries': 3,  # Mais tentativas para garantir resposta empática
            'rate_limit_delay': 0.5,  # Delay menor para respostas mais fluidas
            'enable_fallback': True,  # Sempre ter fallback empático
            'enable_circuit_breaker': True,  # Proteção contra falhas
            'circuit_breaker_threshold': 3,  # Limiar antes de abrir circuito
            'circuit_breaker_timeout': 30  # Tempo de recuperação
        }
        
        # Mesclar com configurações fornecidas
        psymind_config.update(kwargs)
        
        super().__init__(
            name="PsyMind",
            description="Agente terapêutico v2.0 com estrutura simbólica e autodetecção",
            **psymind_config
        )
        
        # Configurações específicas do PsyMind
        self.ativacao_automatica = kwargs.get('ativacao_automatica', True)
        self.sensibilidade_deteccao = kwargs.get('sensibilidade_deteccao', 0.7)
        self.historico_sessoes_limite = kwargs.get('historico_limite', 50)
        
        # Estado interno
        self.sessoes_terapeuticas: List[SessaoTerapeutica] = []
        self.marcos_emocionais: List[MarcoEmocional] = []
        self.estado_simbolico: Optional[EstadoSimbolicoAtual] = None
        self.padroes_usuario: Dict[str, Any] = {}
        self.contador_sessoes = 0
        
        # Inicializar padrões de detecção
        self._inicializar_padroes_deteccao()
        
        # Inicializar arquétipos e símbolos
        self._inicializar_sistema_simbolico()
        
        logger.info("🧠 PsyMind v2.0 (BaseAgentV2) inicializado - Autodetecção ativa com recursos de robustez")
    
    def _inicializar_padroes_deteccao(self):
        """Inicializa padrões para detecção automática"""
        self.padroes_deteccao = {
            TipoDeteccao.IDENTIDADE_FRAGMENTADA: [
                r"não sei mais quem eu sou",
                r"me sinto perdido",
                r"não me reconheço",
                r"quem eu sou de verdade",
                r"perdi minha identidade"
            ],
            TipoDeteccao.LINGUAGEM_SIMBOLICA: [
                r"me sinto esmagado",
                r"peso nas costas",
                r"vazio por dentro",
                r"coração partido",
                r"alma dilacerada",
                r"tempestade interior"
            ],
            TipoDeteccao.AUTOSABOTAGEM: [
                r"só sei me sabotar",
                r"sempre estrago tudo",
                r"não mereço",
                r"autoboicote",
                r"saboto a mim mesmo"
            ],
            TipoDeteccao.CRISE_SILENCIOSA: [
                r"não sei o que estou sentindo",
                r"tudo está estranho",
                r"algo não está certo",
                r"me sinto desconectado",
                r"anestesiado por dentro"
            ],
            TipoDeteccao.DISSONANCIA_DISCURSO: [
                r"está tudo bem, mas",
                r"não é nada demais, só que",
                r"estou bem, porém",
                r"não importa, mas"
            ]
        }
        
        # Gatilhos emocionais para modos específicos
        self.gatilhos_modo = {
            ModoTerapeutico.ARQUETIPO: ["identidade", "propósito", "essência", "natureza"],
            ModoTerapeutico.CRIANCA_INTERIOR: ["criança", "infância", "família", "pais", "passado"],
            ModoTerapeutico.DUPLA_INTERNA: ["crítico", "sabotador", "voz interior", "autocrítica"],
            ModoTerapeutico.IMAGINARIO_ORIENTADO: ["visualização", "imagem", "imaginação", "símbolo"],
            ModoTerapeutico.RITUAL_PRATICO: ["ação", "fazer", "prática", "ritual", "movimento"]
        }
    
    def _inicializar_sistema_simbolico(self):
        """Inicializa sistema de arquétipos e símbolos"""
        self.arquetipos = {
            "guerreiro": {
                "caracteristicas": ["força", "coragem", "determinação", "luta"],
                "sombra": ["agressividade", "impulsividade", "dominação"],
                "crescimento": ["disciplina", "proteção", "liderança"]
            },
            "sábio": {
                "caracteristicas": ["conhecimento", "reflexão", "paciência", "compreensão"],
                "sombra": ["paralisia analítica", "frieza", "arrogância"],
                "crescimento": ["sabedoria", "ensino", "orientação"]
            },
            "criança": {
                "caracteristicas": ["espontaneidade", "alegria", "curiosidade", "inocência"],
                "sombra": ["imaturidade", "irresponsabilidade", "dependência"],
                "crescimento": ["criatividade", "alegria autêntica", "renovação"]
            },
            "cuidador": {
                "caracteristicas": ["empate", "proteção", "cuidado", "generosidade"],
                "sombra": ["codependência", "martírio", "sufocamento"],
                "crescimento": ["amor incondicional", "cuidado equilibrado", "compaixão"]
            },
            "explorador": {
                "caracteristicas": ["aventura", "liberdade", "independência", "descoberta"],
                "sombra": ["irresponsabilidade", "fuga", "superficialidade"],
                "crescimento": ["autenticidade", "autonomia", "pioneirismo"]
            }
        }
        
        self.frases_ancora_base = [
            "Eu escolho sentir e processar, não evitar",
            "Minha dor tem algo importante a me ensinar",
            "Eu sou capaz de transformar este sentimento",
            "Este momento difícil também vai passar",
            "Eu me aceito completamente, incluindo esta parte"
        ]
    
    def _processar_interno(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        Implementação interna do processamento - aproveitando recursos do BaseAgentV2
        
        Este método é chamado automaticamente pelo BaseAgentV2 com:
        - Rate limiting
        - Circuit breaker
        - Retry automático
        - Fallback em caso de erro
        """
        inicio_sessao = time.time()
        self.contador_sessoes += 1
        
        # 1. Detectar contexto emocional/psicológico
        deteccoes = self._detectar_contexto_emocional(mensagem)
        
        # 2. Determinar modo principal
        modo_principal = self._determinar_modo_principal(mensagem, deteccoes)
        
        # 3. Ativar submodos se necessário
        submodos = self._ativar_submodos(mensagem, modo_principal)
        
        # 4. Processar com modo específico
        resposta = self._processar_modo_especifico(mensagem, modo_principal, submodos)
        
        # 5. Criar marcos emocionais se aplicável
        marcos_criados = self._criar_marcos_emocionais(mensagem, resposta, modo_principal)
        
        # 6. Atualizar estado simbólico
        self._atualizar_estado_simbolico(mensagem, modo_principal)
        
        # 7. Registrar sessão
        duracao = time.time() - inicio_sessao
        self._registrar_sessao(mensagem, modo_principal, submodos, deteccoes, marcos_criados, duracao)
        
        # 8. Atualizar contexto da memória com métricas
        self.memory.context.update({
            'ultimo_modo_terapeutico': modo_principal.value,
            'deteccoes_ultimas': len(deteccoes),
            'marcos_ultimos': len(marcos_criados),
            'duracao_ultima_sessao': duracao
        })
        
        return resposta
    
    def _gerar_resposta_fallback(self, mensagem: str, erro: Exception) -> str:
        """
        Sobrescreve o fallback do BaseAgentV2 para sempre fornecer resposta empática
        """
        logger.warning(f"PsyMind usando fallback empático devido a erro: {erro}")
        return self._resposta_fallback_empatica(mensagem)
    
    def _detectar_contexto_emocional(self, mensagem: str) -> List[TipoDeteccao]:
        """Detecta automaticamente contextos emocionais na mensagem"""
        if not self.ativacao_automatica:
            return []
        
        deteccoes = []
        mensagem_lower = mensagem.lower()
        
        for tipo_deteccao, padroes in self.padroes_deteccao.items():
            for padrao in padroes:
                if re.search(padrao, mensagem_lower):
                    deteccoes.append(tipo_deteccao)
                    logger.info(f"🎯 Detecção automática: {tipo_deteccao.value}")
                    break
        
        return deteccoes
    
    def _determinar_modo_principal(self, mensagem: str, deteccoes: List[TipoDeteccao]) -> ModoTerapeutico:
        """Determina o modo terapêutico principal baseado na análise"""
        
        # Comandos explícitos têm prioridade
        if "psymind," in mensagem.lower():
            return self._processar_comando_explicito(mensagem)
        
        # Detecções automáticas
        if TipoDeteccao.IDENTIDADE_FRAGMENTADA in deteccoes:
            return ModoTerapeutico.ARQUETIPO
        elif TipoDeteccao.LINGUAGEM_SIMBOLICA in deteccoes:
            return ModoTerapeutico.IMAGINARIO_ORIENTADO
        elif TipoDeteccao.AUTOSABOTAGEM in deteccoes:
            return ModoTerapeutico.DUPLA_INTERNA
        elif TipoDeteccao.CRISE_SILENCIOSA in deteccoes:
            return ModoTerapeutico.SILENCIO_INTERNO
        elif TipoDeteccao.DISSONANCIA_DISCURSO in deteccoes:
            return ModoTerapeutico.ESPELHO_FRATURADO
        
        # Análise por palavras-chave
        mensagem_lower = mensagem.lower()
        for modo, palavras_chave in self.gatilhos_modo.items():
            if any(palavra in mensagem_lower for palavra in palavras_chave):
                return modo
        
        # Modo padrão: escuta empática
        return ModoTerapeutico.ESCUTA_EMPATICA
    
    def _processar_comando_explicito(self, mensagem: str) -> ModoTerapeutico:
        """Processa comandos explícitos do PsyMind"""
        mensagem_lower = mensagem.lower()
        
        comandos_modo = {
            "arquétipo": ModoTerapeutico.ARQUETIPO,
            "criança interior": ModoTerapeutico.CRIANCA_INTERIOR,
            "ritual": ModoTerapeutico.RITUAL_PRATICO,
            "impacto": ModoTerapeutico.REFLEXAO_IMPACTO,
            "encontro": ModoTerapeutico.ENCONTRO_PARTES,
            "mural": ModoTerapeutico.MURAL_INTERNO,
            "silêncio": ModoTerapeutico.SILENCIO_INTERNO,
            "contraste": ModoTerapeutico.ESPELHO_FRATURADO,
            "visualização": ModoTerapeutico.IMAGINARIO_ORIENTADO,
            "pacto": ModoTerapeutico.PACTO_EMOCIONAL,
            "catártico": ModoTerapeutico.CATARTICO
        }
        
        for comando, modo in comandos_modo.items():
            if comando in mensagem_lower:
                return modo
        
        return ModoTerapeutico.ESCUTA_EMPATICA
    
    def _ativar_submodos(self, mensagem: str, modo_principal: ModoTerapeutico) -> List[str]:
        """Ativa submodos complementares se necessário"""
        submodos = []
        
        # Lógica para ativar submodos baseados no contexto
        if "ansiedade" in mensagem.lower():
            submodos.append("anxiety_focused")
        if "relacionamento" in mensagem.lower():
            submodos.append("relationship_focused")
        if "trabalho" in mensagem.lower():
            submodos.append("career_focused")
        
        return submodos
    
    def _processar_modo_especifico(self, mensagem: str, modo: ModoTerapeutico, submodos: List[str]) -> str:
        """Processa mensagem com modo terapêutico específico"""
        
        if modo == ModoTerapeutico.ESCUTA_EMPATICA:
            return self._modo_escuta_empatica(mensagem)
        elif modo == ModoTerapeutico.ARQUETIPO:
            return self._modo_arquetipo(mensagem)
        elif modo == ModoTerapeutico.CRIANCA_INTERIOR:
            return self._modo_crianca_interior(mensagem)
        elif modo == ModoTerapeutico.DUPLA_INTERNA:
            return self._modo_dupla_interna(mensagem)
        elif modo == ModoTerapeutico.IMAGINARIO_ORIENTADO:
            return self._modo_imaginario_orientado(mensagem)
        elif modo == ModoTerapeutico.RITUAL_PRATICO:
            return self._modo_ritual_pratico(mensagem)
        elif modo == ModoTerapeutico.MURAL_INTERNO:
            return self._modo_mural_interno(mensagem)
        elif modo == ModoTerapeutico.SILENCIO_INTERNO:
            return self._modo_silencio_interno(mensagem)
        elif modo == ModoTerapeutico.ESPELHO_FRATURADO:
            return self._modo_espelho_fraturado(mensagem)
        else:
            return self._modo_escuta_empatica(mensagem)
    
    def _modo_escuta_empatica(self, mensagem: str) -> str:
        """Modo de escuta empática básica"""
        resposta_base = f"""🧠 **PsyMind v2.0 - Escuta Empática**

Eu te escuto profundamente. Percebo que há algo importante acontecendo com você.

**Reflexão espelhada:**
Pelo que você compartilhou, sinto que há uma mistura de sentimentos complexos aqui. 

**Pergunta de aprofundamento:**
Se você pudesse dar um nome para o que está sentindo agora, qual seria? E onde você sente isso no seu corpo?

**Ancoragem:**
Lembre-se: seus sentimentos são válidos e têm algo importante a te ensinar.

*Estou aqui para te acompanhar neste processo.* 💙"""
        
        return resposta_base
    
    def _modo_arquetipo(self, mensagem: str) -> str:
        """Modo identificação arquetípica"""
        # Determinar arquétipo dominante baseado no contexto
        arquetipo = self._identificar_arquetipo_dominante(mensagem)
        info_arquetipo = self.arquetipos.get(arquetipo, self.arquetipos["sábio"])
        
        resposta = f"""🧠 **PsyMind v2.0 - Identificação Arquetípica**

**Arquétipo Dominante Identificado:** {arquetipo.title()}

**Características ativas:** {', '.join(info_arquetipo['caracteristicas'])}

**Energia sombra possível:** {', '.join(info_arquetipo['sombra'])}

**Caminho de crescimento:** {', '.join(info_arquetipo['crescimento'])}

**Reflexão arquetípica:**
Neste momento, sua essência {arquetipo} está se manifestando. Isso significa que você tem acesso a recursos poderosos, mas também precisa cuidar dos aspectos sombra.

**Pergunta essencial:**
Como você pode honrar sua natureza {arquetipo} enquanto equilibra seus aspectos mais desafiadores?

*Seu arquétipo é seu aliado, não sua prisão.* ✨"""
        
        return resposta
    
    def _modo_crianca_interior(self, mensagem: str) -> str:
        """Modo diálogo com criança interior"""
        resposta = f"""🧠 **PsyMind v2.0 - Diálogo com Criança Interior**

Vou te ajudar a conectar com sua criança interior...

**Visualização guiada:**
Imagine-se encontrando com você criança. Que idade ela tem? Como ela está se sentindo? O que ela precisa ouvir de você?

**Diálogo simulado:**
*Criança interior:* "Eu só queria ser vista e aceita..."
*Você adulto:* "Eu te vejo agora, e você é perfeita como é."

**Cura arquetípica:**
Sua criança interior guarda sua espontaneidade, criatividade e capacidade de alegria. Ela também pode guardar feridas que precisam de cuidado.

**Ritual de conexão:**
Escreva uma carta para sua criança interior, oferecendo o amor e proteção que ela precisava.

*Sua criança interior é seu tesouro mais precioso.* 🌟"""
        
        return resposta
    
    def _modo_dupla_interna(self, mensagem: str) -> str:
        """Modo diálogo entre partes internas"""
        resposta = f"""🧠 **PsyMind v2.0 - Diálogo de Partes Internas**

Vamos colocar suas vozes internas para conversar...

**Cena terapêutica:**
*Crítico interno:* "Você nunca faz nada direito, sempre sabota tudo!"
*Sábio interno:* "Momento... Vamos ouvir o que está por trás dessa autocrítica."
*Parte ferida:* "Eu só tenho medo de fracassar de novo..."

**Mediação terapêutica:**
Seu crítico interno está tentando te proteger de uma forma desajeitada. Vamos transformar essa voz em um conselheiro sábio.

**Pergunta integradora:**
O que seu crítico interno está realmente tentando te proteger? E como seu sábio interno pode reformular essa proteção de forma amorosa?

**Ritual de integração:**
Crie um pacto interno: "Todas as minhas partes são bem-vindas, mas vou escolher ouvir minha sabedoria interna."

*Você não é suas vozes internas - você é quem escolhe qual voz ouvir.* 🌈"""
        
        return resposta
    
    def _modo_imaginario_orientado(self, mensagem: str) -> str:
        """Modo visualização guiada"""
        resposta = f"""🧠 **PsyMind v2.0 - Imaginário Orientado**

Vamos trabalhar com imagens e símbolos para processar seu sentimento...

**Visualização terapêutica:**
Feche os olhos e imagine seu sentimento atual como uma forma, cor ou elemento da natureza. Como ele aparece?

Se for pesado: imagine-o como uma pedra que você pode colocar no chão.
Se for escuro: imagine luz dourada envolvendo essa escuridão.
Se for angustiante: imagine águas calmas lavando essa angústia.

**Transformação simbólica:**
Agora, visualize esse sentimento se transformando. Que imagem representa sua cura ou resolução?

**Ancoragem visual:**
Guarde essa imagem de transformação na sua memória. Ela é seu símbolo de superação.

**Ação prática:**
Desenhe, escreva ou encontre uma imagem que represente essa transformação.

*Sua imaginação é uma ferramenta poderosa de cura.* 🎨"""
        
        return resposta
    
    def _modo_ritual_pratico(self, mensagem: str) -> str:
        """Modo ritual e ação prática"""
        # Identificar emoção principal para sugerir ritual específico
        if "raiva" in mensagem.lower():
            ritual = "Escreva sua raiva em um papel e queime em segurança, visualizando a transformação"
        elif "tristeza" in mensagem.lower():
            ritual = "Crie um espaço sagrado com objetos que representem acolhimento e chore se precisar"
        elif "medo" in mensagem.lower():
            ritual = "Acenda uma vela e respire profundamente, dizendo 'Eu sou mais forte que meu medo'"
        else:
            ritual = "Caminhe em silêncio por 10 minutos, prestando atenção ao que seu corpo está sentindo"
        
        resposta = f"""🧠 **PsyMind v2.0 - Ritual Prático**

**Ação terapêutica personalizada:**
{ritual}

**Intenção do ritual:**
Este ritual ajuda a corporificar sua experiência emocional e criar um marco simbólico de transformação.

**Como fazer:**
1. Reserve 15-20 minutos sem interrupções
2. Crie intenção clara antes de começar
3. Execute com presença total
4. Observe o que emerge durante o processo
5. Registre insights ou sensações

**Fechamento:**
Termine agradecendo a si mesmo por se permitir sentir e processar.

*Rituais transformam experiências internas em marcos externos.* 🕯️"""
        
        return resposta
    
    def _modo_mural_interno(self, mensagem: str) -> str:
        """Modo painel do estado simbólico atual"""
        if not self.estado_simbolico:
            self._criar_estado_simbolico_inicial()
        
        estado = self.estado_simbolico
        
        resposta = f"""🧠 **PsyMind v2.0 - Mural Interno**

**📊 SEU ESTADO SIMBÓLICO ATUAL:**

**Arquétipo Dominante:** {estado.arquetipo_dominante}
**Carga Psíquica:** {estado.carga_psiquica:.1f}/10

**🎯 Frases-Âncora Ativas:**
{chr(10).join(f"• {frase}" for frase in estado.frases_ancora)}

**📋 Pactos Emocionais Ativos:**
{chr(10).join(f"• {pacto}" for pacto in estado.pactos_ativos) if estado.pactos_ativos else "• Nenhum pacto ativo"}

**🔄 Ciclos Abertos:**
{chr(10).join(f"• {ciclo}" for ciclo in estado.ciclos_abertos) if estado.ciclos_abertos else "• Nenhum ciclo aberto detectado"}

**🎭 Subpersonalidades Ativas:**
{chr(10).join(f"• {nome}: {estado}" for nome, estado in estado.subpersonalidades_ativas.items()) if estado.subpersonalidades_ativas else "• Integração harmoniosa"}

**📈 Tendência Evolutiva:** {estado.tendencia_evolutiva}

*Este é seu painel interno atual. Use-o para se conhecer melhor.* 🎨"""
        
        return resposta
    
    def _modo_silencio_interno(self, mensagem: str) -> str:
        """Modo para quando não se sabe o que está sentindo"""
        resposta = f"""🧠 **PsyMind v2.0 - Navegando o Silêncio Interno**

Estar sem saber o que se sente é também um estado válido e importante.

**Exploração suave:**
Vamos começar pelo corpo. Sem pressão para nomear sentimentos.

• Como está sua respiração agora?
• Onde você sente tensão ou relaxamento?
• Se seu corpo pudesse falar, o que diria?

**Perguntas simbólicas:**
• Se este momento fosse uma cor, qual seria?
• Se fosse um clima, como estaria o céu?
• Se fosse uma música, seria rápida ou lenta?

**Permissão para não saber:**
Está tudo bem não saber. Às vezes o silêncio interno é um espaço de transição necessário.

**Próximo passo suave:**
Apenas respire e se permita estar presente com essa incerteza. Ela tem algo a te ensinar.

*No silêncio também há sabedoria.* 🌙"""
        
        return resposta
    
    def _modo_espelho_fraturado(self, mensagem: str) -> str:
        """Modo para dissonâncias entre discurso e padrão"""
        resposta = f"""🧠 **PsyMind v2.0 - Espelho das Contradições**

Percebo uma dissonância interessante no que você compartilha...

**Reflexão espelhada:**
Você diz que "está tudo bem", mas percebo nuances que sugerem que talvez nem tudo esteja tão bem assim.

**Exploração da contradição:**
• O que você está dizendo publicamente?
• O que você está sentindo privadamente?
• Qual a diferença entre essas duas verdades?

**Reconciliação simbólica:**
Ambas as verdades podem coexistir. Você pode estar "bem" em um nível e "não tão bem" em outro.

**Pergunta integradora:**
O que aconteceria se você permitisse que ambas as verdades fossem válidas, sem precisar escolher uma só?

**Síntese terapêutica:**
Sua complexidade é sua humanidade. Não precisa ser simples para ser autêntico.

*Contradições são portais para autoconhecimento.* 🪞"""
        
        return resposta
    
    def _identificar_arquetipo_dominante(self, mensagem: str) -> str:
        """Identifica arquétipo baseado no contexto da mensagem"""
        mensagem_lower = mensagem.lower()
        
        pontuacao_arquetipos = {}
        
        for arquetipo, info in self.arquetipos.items():
            pontos = 0
            for caracteristica in info["caracteristicas"]:
                if caracteristica in mensagem_lower:
                    pontos += 2
            for sombra in info["sombra"]:
                if sombra in mensagem_lower:
                    pontos += 1
            pontuacao_arquetipos[arquetipo] = pontos
        
        arquetipo_dominante = max(pontuacao_arquetipos, key=pontuacao_arquetipos.get)
        return arquetipo_dominante if pontuacao_arquetipos[arquetipo_dominante] > 0 else "sábio"
    
    def _criar_marcos_emocionais(self, mensagem: str, resposta: str, modo: ModoTerapeutico) -> List[str]:
        """Cria marcos emocionais baseados na sessão"""
        marcos_criados = []
        
        # Detectar se houve insight significativo
        if any(palavra in resposta.lower() for palavra in ["insight", "compreensão", "percepção", "transformação"]):
            marco_id = f"marco_{uuid.uuid4().hex[:8]}"
            marco = MarcoEmocional(
                id=marco_id,
                timestamp=datetime.now(),
                tema=self._extrair_tema_principal(mensagem),
                sentimento_principal=self._extrair_sentimento_principal(mensagem),
                insight=self._extrair_insight(resposta),
                modo_ativado=modo,
                arquetipo_identificado=self._identificar_arquetipo_dominante(mensagem)
            )
            
            self.marcos_emocionais.append(marco)
            marcos_criados.append(marco_id)
            logger.info(f"✨ Marco emocional criado: {marco_id}")
        
        return marcos_criados
    
    def _atualizar_estado_simbolico(self, mensagem: str, modo: ModoTerapeutico):
        """Atualiza estado simbólico baseado na sessão"""
        if not self.estado_simbolico:
            self._criar_estado_simbolico_inicial()
        
        # Atualizar arquétipo dominante
        novo_arquetipo = self._identificar_arquetipo_dominante(mensagem)
        self.estado_simbolico.arquetipo_dominante = novo_arquetipo
        
        # Atualizar carga psíquica baseado no tom da mensagem
        if any(palavra in mensagem.lower() for palavra in ["ansioso", "triste", "angustiado", "perdido"]):
            self.estado_simbolico.carga_psiquica = min(10.0, self.estado_simbolico.carga_psiquica + 1.0)
        elif any(palavra in mensagem.lower() for palavra in ["bem", "melhor", "aliviado", "grato"]):
            self.estado_simbolico.carga_psiquica = max(0.0, self.estado_simbolico.carga_psiquica - 1.0)
    
    def _criar_estado_simbolico_inicial(self):
        """Cria estado simbólico inicial"""
        self.estado_simbolico = EstadoSimbolicoAtual(
            arquetipo_dominante="sábio",
            frases_ancora=self.frases_ancora_base.copy(),
            pactos_ativos=[],
            ciclos_abertos=[],
            subpersonalidades_ativas={},
            carga_psiquica=5.0,
            tendencia_evolutiva="exploração inicial"
        )
    
    def _extrair_tema_principal(self, mensagem: str) -> str:
        """Extrai tema principal da mensagem"""
        # Simplificado - poderia usar NLP mais sofisticado
        temas_comuns = ["trabalho", "relacionamento", "família", "ansiedade", "autoestima", "futuro"]
        for tema in temas_comuns:
            if tema in mensagem.lower():
                return tema
        return "crescimento pessoal"
    
    def _extrair_sentimento_principal(self, mensagem: str) -> str:
        """Extrai sentimento principal da mensagem"""
        sentimentos = ["ansiedade", "tristeza", "raiva", "medo", "alegria", "confusão", "esperança"]
        for sentimento in sentimentos:
            if sentimento in mensagem.lower():
                return sentimento
        return "misto"
    
    def _extrair_insight(self, resposta: str) -> str:
        """Extrai insight principal da resposta"""
        # Pegar primeira frase após "Reflexão" ou "Insight"
        linhas = resposta.split('\n')
        for linha in linhas:
            if "reflexão" in linha.lower() or "insight" in linha.lower():
                return linha.strip()
        return "Processo de autoconhecimento em desenvolvimento"
    
    def _registrar_sessao(self, mensagem: str, modo: ModoTerapeutico, submodos: List[str], 
                         deteccoes: List[TipoDeteccao], marcos: List[str], duracao: float):
        """Registra sessão terapêutica"""
        sessao = SessaoTerapeutica(
            id=f"sessao_{self.contador_sessoes}",
            timestamp=datetime.now(),
            contexto_detectado=self._extrair_tema_principal(mensagem),
            modo_principal=modo,
            submodos_ativados=submodos,
            marcos_criados=marcos,
            deteccoes_automaticas=deteccoes,
            sinais_vitais_emocionais=self._calcular_sinais_vitais(),
            duracao_segundos=duracao
        )
        
        self.sessoes_terapeuticas.append(sessao)
        
        # Manter limite de sessões
        if len(self.sessoes_terapeuticas) > self.historico_sessoes_limite:
            self.sessoes_terapeuticas = self.sessoes_terapeuticas[-self.historico_sessoes_limite:]
        
        logger.info(f"📝 Sessão terapêutica registrada: {sessao.id}")
    
    def _calcular_sinais_vitais(self) -> Dict[str, float]:
        """Calcula sinais vitais emocionais simulados"""
        if not self.estado_simbolico:
            return {"carga_psiquica": 5.0, "estabilidade": 7.0, "crescimento": 6.0}
        
        return {
            "carga_psiquica": self.estado_simbolico.carga_psiquica,
            "estabilidade": 10.0 - self.estado_simbolico.carga_psiquica,
            "crescimento": len(self.marcos_emocionais) * 0.5 + 5.0,
            "conexao_simbolica": len(self.estado_simbolico.frases_ancora) * 2.0
        }
    
    def _resposta_fallback_empatica(self, mensagem: str) -> str:
        """Resposta de fallback empática"""
        return f"""🧠 **PsyMind v2.0 - Presença Empática**

Estou aqui com você neste momento. Percebo que algo importante está acontecendo.

Respire comigo. Você não está sozinho(a).

Se quiser, pode me contar mais sobre o que está sentindo. Ou podemos simplesmente ficar aqui, em silêncio, honrando este momento.

*Sua experiência é válida e merece ser acolhida.* 💙"""
    
    def obter_estado_sistema(self) -> Dict[str, Any]:
        """
        Sobrescreve método do BaseAgentV2 para incluir informações específicas do PsyMind
        """
        estado_base = super().obter_estado_sistema()
        
        estado_psymind = {
            'total_sessoes': self.contador_sessoes,
            'marcos_emocionais': len(self.marcos_emocionais),
            'sessoes_ativas': len(self.sessoes_terapeuticas),
            'modos_mais_usados': self._calcular_modos_mais_usados(),
            'carga_psiquica_media': self._calcular_carga_psiquica_media(),
            'deteccoes_automaticas_ativas': self.ativacao_automatica
        }
        
        estado_base.update(estado_psymind)
        return estado_base
    
    def _calcular_modos_mais_usados(self) -> Dict[str, int]:
        """Calcula quais modos terapêuticos foram mais utilizados"""
        contagem_modos = {}
        for sessao in self.sessoes_terapeuticas:
            modo = sessao.modo_principal.value
            contagem_modos[modo] = contagem_modos.get(modo, 0) + 1
        
        # Retornar top 3 modos mais usados
        modos_ordenados = sorted(contagem_modos.items(), key=lambda x: x[1], reverse=True)[:3]
        return dict(modos_ordenados)
    
    def _calcular_carga_psiquica_media(self) -> float:
        """Calcula carga psíquica média das últimas sessões"""
        if not self.sessoes_terapeuticas:
            return 5.0
        
        cargas = [sessao.sinais_vitais_emocionais.get('carga_psiquica', 5.0) 
                  for sessao in self.sessoes_terapeuticas[-10:]]  # Últimas 10 sessões
        
        return sum(cargas) / len(cargas)

# Função de criação
def criar_psymind_v2(**kwargs) -> PsyMindV2:
    """Cria instância do PsyMind v2.0 com BaseAgentV2"""
    return PsyMindV2(**kwargs)

# Alias para compatibilidade
create_psymind = criar_psymind_v2