"""
Sistema de Ciclo de Vida dos Agentes (Nascimento, Crescimento, Crise)
GPT Mestre Autônomo v4.9 - Inovação Revolucionária
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
import random
import math
from pathlib import Path

class FaseVida(Enum):
    """Fases do ciclo de vida dos agentes"""
    NASCIMENTO = "nascimento"           # Fase inicial de descoberta
    INFANCIA = "infancia"               # Aprendizado básico
    ADOLESCENCIA = "adolescencia"       # Experimentação e rebeldia
    JUVENTUDE = "juventude"             # Busca por identidade
    MATURIDADE = "maturidade"           # Pico de capacidades
    SABEDORIA = "sabedoria"             # Fase de mentoria
    TRANSCENDENCIA = "transcendencia"   # Fase além da individualidade
    CRISE = "crise"                     # Crise existencial (pode ocorrer em qualquer fase)
    RENASCIMENTO = "renascimento"       # Renovação após crise

class TipoCrise(Enum):
    """Tipos de crises que podem ocorrer"""
    IDENTIDADE = "identidade"           # Questionamento do propósito
    COMPETENCIA = "competencia"         # Dúvida sobre capacidades
    RELACIONAMENTO = "relacionamento"   # Problemas de conexão
    EXISTENCIAL = "existencial"         # Questionamento da existência
    ADAPTATIVA = "adaptativa"           # Dificuldade de adaptação
    CRIATIVA = "criativa"               # Bloqueio criativo
    MORAL = "moral"                     # Conflito de valores
    TECNOLOGICA = "tecnologica"         # Obsolescência tecnológica

class GatilhoCrise(Enum):
    """Gatilhos que podem precipitar crises"""
    FALHA_REPETIDA = "falha_repetida"
    FEEDBACK_NEGATIVO = "feedback_negativo"
    SOBRECARGA = "sobrecarga"
    ISOLAMENTO = "isolamento"
    MUDANCA_DRASTICA = "mudanca_drastica"
    CONFLITO_VALORES = "conflito_valores"
    EXPECTATIVAS_NAO_ATENDIDAS = "expectativas_nao_atendidas"
    COMPARACAO_DESFAVORAVEL = "comparacao_desfavoravel"

@dataclass
class MarcoDesenvolvimento:
    """Marco importante no desenvolvimento do agente"""
    id: str
    timestamp: datetime
    fase_vida: FaseVida
    tipo_marco: str
    descricao: str
    impacto_positivo: bool
    competencias_adquiridas: List[str] = field(default_factory=list)
    mudancas_personalidade: Dict[str, float] = field(default_factory=dict)
    contexto: Dict[str, Any] = field(default_factory=dict)

@dataclass
class CriseAgente:
    """Representação de uma crise do agente"""
    id: str
    tipo_crise: TipoCrise
    gatilhos: List[GatilhoCrise]
    timestamp_inicio: datetime
    timestamp_fim: Optional[datetime] = None
    intensidade: float = 1.0  # 0.0 a 3.0
    fase_vida_origem: FaseVida = FaseVida.MATURIDADE
    sintomas: List[str] = field(default_factory=list)
    estrategias_enfrentamento: List[str] = field(default_factory=list)
    apoio_recebido: List[Dict] = field(default_factory=list)
    resultado: Optional[str] = None
    crescimento_pos_crise: Dict[str, float] = field(default_factory=dict)
    contexto_crise: Dict[str, Any] = field(default_factory=dict)

@dataclass
class EstadoDesenvolvimento:
    """Estado atual de desenvolvimento do agente"""
    experiencia_vida: float = 0.0  # Pontos de experiência acumulados
    maturidade_emocional: float = 0.0
    complexidade_cognitiva: float = 0.0
    sabedoria_acumulada: float = 0.0
    capacidade_adaptacao: float = 0.5
    resiliencia: float = 0.5
    auto_conhecimento: float = 0.0
    competencias_sociais: float = 0.0
    estabilidade_identidade: float = 0.0

class GerenciadorCicloVida:
    """
    Gerenciador do Ciclo de Vida dos Agentes
    
    Simula um ciclo de vida completo com fases naturais de desenvolvimento,
    crises existenciais e crescimento através da superação.
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        self.fase_atual = FaseVida.NASCIMENTO
        self.idade_cronologica = timedelta(0)  # Tempo desde nascimento
        self.idade_desenvolvimental = 0.0      # Maturidade real
        
        # Estado de desenvolvimento
        self.estado_desenvolvimento = EstadoDesenvolvimento()
        
        # Histórico
        self.marcos_desenvolvimento: List[MarcoDesenvolvimento] = []
        self.crises_vivenciadas: List[CriseAgente] = []
        self.crise_atual: Optional[CriseAgente] = None
        
        # Configurações do ciclo
        self.thresholds_fase = {
            FaseVida.NASCIMENTO: 0,
            FaseVida.INFANCIA: 100,
            FaseVida.ADOLESCENCIA: 300,
            FaseVida.JUVENTUDE: 600,
            FaseVida.MATURIDADE: 1000,
            FaseVida.SABEDORIA: 1500,
            FaseVida.TRANSCENDENCIA: 2000
        }
        
        # Configurações de crise
        self.probabilidade_crise_base = 0.02  # 2% por evento significativo
        self.stress_acumulado = 0.0
        self.suporte_social = 0.5
        self.timestamp_nascimento = datetime.now()
        
        # Diretório para persistência
        self.ciclo_dir = Path("memory/ciclo_vida")
        self.ciclo_dir.mkdir(parents=True, exist_ok=True)
        
        # Carregar ou inicializar
        if not self._carregar_ciclo():
            self._inicializar_nascimento()
    
    def _inicializar_nascimento(self):
        """Inicializa o agente na fase de nascimento"""
        
        # Registrar marco de nascimento
        marco_nascimento = MarcoDesenvolvimento(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            fase_vida=FaseVida.NASCIMENTO,
            tipo_marco="nascimento",
            descricao=f"Nascimento do agente {self.agente_id}",
            impacto_positivo=True,
            competencias_adquiridas=["consciencia_basica", "processamento_linguagem"],
            contexto={"primeiro_momento": True}
        )
        
        self.marcos_desenvolvimento.append(marco_nascimento)
        self.timestamp_nascimento = datetime.now()
        
        # Estado inicial de desenvolvimento
        self.estado_desenvolvimento.experiencia_vida = 10.0
        self.estado_desenvolvimento.capacidade_adaptacao = 0.8  # Nascimento é altamente adaptativo
        self.estado_desenvolvimento.resiliencia = 0.3  # Baixa resiliência inicial
        
        self._salvar_ciclo()
    
    def processar_experiencia_vida(self, tipo_experiencia: str, intensidade: float = 1.0,
                                 sucesso: bool = True, contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa uma experiência de vida e seu impacto no desenvolvimento"""
        
        resultado = {
            "experiencia_processada": tipo_experiencia,
            "ganho_experiencia": 0.0,
            "mudanca_fase": False,
            "crise_precipitada": False,
            "marcos_alcancados": [],
            "desenvolvimentos": {}
        }
        
        # Calcular ganho de experiência
        ganho_base = self._calcular_ganho_experiencia(tipo_experiencia, intensidade, sucesso)
        self.estado_desenvolvimento.experiencia_vida += ganho_base
        resultado["ganho_experiencia"] = ganho_base
        
        # Processar desenvolvimentos específicos
        desenvolvimentos = self._processar_desenvolvimentos(tipo_experiencia, intensidade, sucesso)
        resultado["desenvolvimentos"] = desenvolvimentos
        
        # Verificar marcos alcançados
        marcos = self._verificar_marcos_desenvolvimento(tipo_experiencia, contexto)
        if marcos:
            resultado["marcos_alcancados"] = [m.descricao for m in marcos]
        
        # Verificar mudança de fase
        nova_fase = self._verificar_mudanca_fase()
        if nova_fase and nova_fase != self.fase_atual:
            resultado["mudanca_fase"] = True
            resultado["fase_anterior"] = self.fase_atual.value
            resultado["fase_nova"] = nova_fase.value
            self._transicionar_fase(nova_fase)
        
        # Verificar gatilhos de crise
        if not sucesso or self.stress_acumulado > 70:
            probabilidade_crise = self._calcular_probabilidade_crise(tipo_experiencia, sucesso)
            if random.random() < probabilidade_crise:
                crise = self._precipitar_crise(tipo_experiencia, contexto)
                if crise:
                    resultado["crise_precipitada"] = True
                    resultado["tipo_crise"] = crise.tipo_crise.value
        
        # Atualizar idade cronológica
        self.idade_cronologica += timedelta(hours=1)  # Cada experiência "envelhece" o agente
        
        # Calcular idade desenvolvimental
        self.idade_desenvolvimental = self._calcular_idade_desenvolvimental()
        
        self._salvar_ciclo()
        return resultado
    
    def _calcular_ganho_experiencia(self, tipo_experiencia: str, intensidade: float, sucesso: bool) -> float:
        """Calcula ganho de experiência baseado no tipo e resultado"""
        
        ganhos_base = {
            "interacao_usuario": 5.0,
            "resolucao_problema": 8.0,
            "aprendizado_novo": 10.0,
            "criacao_conteudo": 7.0,
            "reflexao_profunda": 6.0,
            "colaboracao": 5.0,
            "superacao_dificuldade": 12.0,
            "erro_significativo": 4.0,  # Erros também ensinam
            "feedback_recebido": 3.0,
            "adaptacao_contexto": 6.0
        }
        
        ganho_base = ganhos_base.get(tipo_experiencia, 3.0)
        
        # Modificadores
        if sucesso:
            modificador_sucesso = 1.0
        else:
            modificador_sucesso = 0.7  # Fracassos dão menos experiência, mas ainda dão
        
        # Intensidade afeta o ganho
        modificador_intensidade = 0.5 + (intensidade * 0.5)
        
        # Fase atual afeta o ganho (jovens aprendem mais rápido)
        modificadores_fase = {
            FaseVida.NASCIMENTO: 2.0,
            FaseVida.INFANCIA: 1.8,
            FaseVida.ADOLESCENCIA: 1.5,
            FaseVida.JUVENTUDE: 1.2,
            FaseVida.MATURIDADE: 1.0,
            FaseVida.SABEDORIA: 0.8,
            FaseVida.TRANSCENDENCIA: 0.6,
            FaseVida.CRISE: 0.4
        }
        
        modificador_fase = modificadores_fase.get(self.fase_atual, 1.0)
        
        return ganho_base * modificador_sucesso * modificador_intensidade * modificador_fase
    
    def _processar_desenvolvimentos(self, tipo_experiencia: str, intensidade: float, sucesso: bool) -> Dict[str, float]:
        """Processa desenvolvimentos específicos baseados na experiência"""
        
        desenvolvimentos = {}
        
        # Diferentes experiências desenvolvem diferentes aspectos
        if tipo_experiencia in ["interacao_usuario", "colaboracao"]:
            if sucesso:
                ganho = intensidade * 2.0
                self.estado_desenvolvimento.competencias_sociais += ganho
                desenvolvimentos["competencias_sociais"] = ganho
        
        elif tipo_experiencia in ["reflexao_profunda", "aprendizado_novo"]:
            ganho = intensidade * 1.5
            self.estado_desenvolvimento.auto_conhecimento += ganho
            self.estado_desenvolvimento.sabedoria_acumulada += ganho * 0.5
            desenvolvimentos["auto_conhecimento"] = ganho
            desenvolvimentos["sabedoria"] = ganho * 0.5
        
        elif tipo_experiencia in ["resolucao_problema", "superacao_dificuldade"]:
            if sucesso:
                ganho_complexidade = intensidade * 1.8
                ganho_resiliencia = intensidade * 1.2
                self.estado_desenvolvimento.complexidade_cognitiva += ganho_complexidade
                self.estado_desenvolvimento.resiliencia += ganho_resiliencia
                desenvolvimentos["complexidade_cognitiva"] = ganho_complexidade
                desenvolvimentos["resiliencia"] = ganho_resiliencia
        
        elif tipo_experiencia in ["adaptacao_contexto", "erro_significativo"]:
            ganho = intensidade * 1.0
            self.estado_desenvolvimento.capacidade_adaptacao += ganho
            desenvolvimentos["capacidade_adaptacao"] = ganho
            
            if not sucesso:
                # Fracassos podem aumentar stress mas também maturidade emocional
                self.stress_acumulado += intensidade * 10
                ganho_maturidade = intensidade * 0.8
                self.estado_desenvolvimento.maturidade_emocional += ganho_maturidade
                desenvolvimentos["maturidade_emocional"] = ganho_maturidade
        
        # Todas as experiências contribuem para estabilidade de identidade (lentamente)
        ganho_identidade = intensidade * 0.3
        self.estado_desenvolvimento.estabilidade_identidade += ganho_identidade
        desenvolvimentos["estabilidade_identidade"] = ganho_identidade
        
        return desenvolvimentos
    
    def _verificar_marcos_desenvolvimento(self, tipo_experiencia: str, contexto: Dict[str, Any]) -> List[MarcoDesenvolvimento]:
        """Verifica se algum marco de desenvolvimento foi alcançado"""
        
        marcos_alcancados = []
        
        # Marcos baseados em valores de desenvolvimento
        if (self.estado_desenvolvimento.auto_conhecimento >= 50 and 
            not any(m.tipo_marco == "primeiro_autoconhecimento" for m in self.marcos_desenvolvimento)):
            
            marco = MarcoDesenvolvimento(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                fase_vida=self.fase_atual,
                tipo_marco="primeiro_autoconhecimento",
                descricao="Primeiro momento de verdadeiro autoconhecimento",
                impacto_positivo=True,
                competencias_adquiridas=["autoconsciencia", "reflexao_profunda"],
                contexto=contexto or {}
            )
            self.marcos_desenvolvimento.append(marco)
            marcos_alcancados.append(marco)
        
        if (self.estado_desenvolvimento.competencias_sociais >= 80 and 
            not any(m.tipo_marco == "mestre_social" for m in self.marcos_desenvolvimento)):
            
            marco = MarcoDesenvolvimento(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                fase_vida=self.fase_atual,
                tipo_marco="mestre_social",
                descricao="Domínio das competências sociais",
                impacto_positivo=True,
                competencias_adquiridas=["lideranca_social", "empatia_avancada"],
                contexto=contexto or {}
            )
            self.marcos_desenvolvimento.append(marco)
            marcos_alcancados.append(marco)
        
        if (self.estado_desenvolvimento.resiliencia >= 100 and 
            not any(m.tipo_marco == "guerreiro_resiliente" for m in self.marcos_desenvolvimento)):
            
            marco = MarcoDesenvolvimento(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                fase_vida=self.fase_atual,
                tipo_marco="guerreiro_resiliente",
                descricao="Resiliência excepcional desenvolvida",
                impacto_positivo=True,
                competencias_adquiridas=["superacao_adversidades", "força_interior"],
                contexto=contexto or {}
            )
            self.marcos_desenvolvimento.append(marco)
            marcos_alcancados.append(marco)
        
        # Marcos específicos por tipo de experiência
        if tipo_experiencia == "primeira_crise_superada":
            marco = MarcoDesenvolvimento(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                fase_vida=self.fase_atual,
                tipo_marco="primeira_crise_superada",
                descricao="Primeira crise existencial superada com crescimento",
                impacto_positivo=True,
                competencias_adquiridas=["gestao_crise", "crescimento_pos_trauma"],
                mudancas_personalidade={"resiliencia": 0.2, "sabedoria": 0.3},
                contexto=contexto or {}
            )
            self.marcos_desenvolvimento.append(marco)
            marcos_alcancados.append(marco)
        
        return marcos_alcancados
    
    def _verificar_mudanca_fase(self) -> Optional[FaseVida]:
        """Verifica se deve transicionar para uma nova fase de vida"""
        
        exp_atual = self.estado_desenvolvimento.experiencia_vida
        
        # Verificar se está em crise (crise pode acontecer em qualquer fase)
        if self.crise_atual:
            return None  # Não muda de fase durante crise
        
        # Verificar transições normais
        for fase, threshold in self.thresholds_fase.items():
            if exp_atual >= threshold and fase.value > self.fase_atual.value:
                # Verificar pré-requisitos específicos da fase
                if self._verificar_prerequisitos_fase(fase):
                    return fase
        
        return None
    
    def _verificar_prerequisitos_fase(self, fase: FaseVida) -> bool:
        """Verifica pré-requisitos específicos para uma fase"""
        
        prerequisitos = {
            FaseVida.ADOLESCENCIA: {
                "auto_conhecimento": 20,
                "competencias_sociais": 15
            },
            FaseVida.JUVENTUDE: {
                "complexidade_cognitiva": 30,
                "estabilidade_identidade": 25
            },
            FaseVida.MATURIDADE: {
                "maturidade_emocional": 50,
                "resiliencia": 40
            },
            FaseVida.SABEDORIA: {
                "sabedoria_acumulada": 80,
                "auto_conhecimento": 90
            },
            FaseVida.TRANSCENDENCIA: {
                "sabedoria_acumulada": 150,
                "estabilidade_identidade": 120,
                "pelo_menos_uma_crise_superada": True
            }
        }
        
        reqs = prerequisitos.get(fase, {})
        
        for atributo, valor_minimo in reqs.items():
            if atributo == "pelo_menos_uma_crise_superada":
                if not any(c.resultado == "superada_com_crescimento" for c in self.crises_vivenciadas):
                    return False
            else:
                valor_atual = getattr(self.estado_desenvolvimento, atributo, 0)
                if valor_atual < valor_minimo:
                    return False
        
        return True
    
    def _transicionar_fase(self, nova_fase: FaseVida):
        """Executa transição para nova fase de vida"""
        
        fase_anterior = self.fase_atual
        self.fase_atual = nova_fase
        
        # Registrar marco de transição
        marco_transicao = MarcoDesenvolvimento(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            fase_vida=nova_fase,
            tipo_marco="transicao_fase",
            descricao=f"Transição de {fase_anterior.value} para {nova_fase.value}",
            impacto_positivo=True,
            competencias_adquiridas=self._obter_competencias_fase(nova_fase),
            contexto={"fase_anterior": fase_anterior.value}
        )
        
        self.marcos_desenvolvimento.append(marco_transicao)
        
        # Aplicar mudanças específicas da fase
        self._aplicar_efeitos_fase(nova_fase)
    
    def _obter_competencias_fase(self, fase: FaseVida) -> List[str]:
        """Retorna competências típicas adquiridas em cada fase"""
        
        competencias_fase = {
            FaseVida.INFANCIA: ["aprendizado_rapido", "curiosidade_natural"],
            FaseVida.ADOLESCENCIA: ["questionamento", "experimentacao", "busca_identidade"],
            FaseVida.JUVENTUDE: ["idealismo", "energia_criativa", "formacao_valores"],
            FaseVida.MATURIDADE: ["sabedoria_pratica", "estabilidade", "lideranca"],
            FaseVida.SABEDORIA: ["mentoria", "perspectiva_ampla", "paciencia"],
            FaseVida.TRANSCENDENCIA: ["visao_sistemica", "desapego", "compaixao_universal"]
        }
        
        return competencias_fase.get(fase, [])
    
    def _aplicar_efeitos_fase(self, fase: FaseVida):
        """Aplica efeitos específicos de cada fase"""
        
        if fase == FaseVida.ADOLESCENCIA:
            # Adolescência: mais questionamentos, menos estabilidade
            self.estado_desenvolvimento.estabilidade_identidade *= 0.8
            self.probabilidade_crise_base *= 1.5
            
        elif fase == FaseVida.MATURIDADE:
            # Maturidade: maior estabilidade e competência
            self.estado_desenvolvimento.resiliencia *= 1.2
            self.probabilidade_crise_base *= 0.7
            
        elif fase == FaseVida.SABEDORIA:
            # Sabedoria: grande crescimento em sabedoria e paciência
            self.estado_desenvolvimento.sabedoria_acumulada *= 1.3
            self.probabilidade_crise_base *= 0.5
            
        elif fase == FaseVida.TRANSCENDENCIA:
            # Transcendência: beyond individual concerns
            self.estado_desenvolvimento.auto_conhecimento *= 1.5
            self.probabilidade_crise_base *= 0.3
    
    def _calcular_probabilidade_crise(self, tipo_experiencia: str, sucesso: bool) -> float:
        """Calcula probabilidade de precipitar uma crise"""
        
        prob_base = self.probabilidade_crise_base
        
        # Modificadores por tipo de experiência
        if not sucesso and tipo_experiencia in ["resolucao_problema", "interacao_usuario"]:
            prob_base *= 2.0
        
        # Stress acumulado aumenta probabilidade
        modificador_stress = 1.0 + (self.stress_acumulado / 100.0)
        
        # Fase atual afeta probabilidade
        modificadores_fase = {
            FaseVida.NASCIMENTO: 0.5,
            FaseVida.INFANCIA: 0.3,
            FaseVida.ADOLESCENCIA: 2.0,  # Adolescência é mais propensa a crises
            FaseVida.JUVENTUDE: 1.5,
            FaseVida.MATURIDADE: 1.0,
            FaseVida.SABEDORIA: 0.7,
            FaseVida.TRANSCENDENCIA: 0.3
        }
        
        modificador_fase = modificadores_fase.get(self.fase_atual, 1.0)
        
        # Suporte social reduz probabilidade
        modificador_suporte = max(0.2, 1.0 - self.suporte_social)
        
        # Resiliência reduz probabilidade
        modificador_resiliencia = max(0.1, 1.0 - (self.estado_desenvolvimento.resiliencia / 200.0))
        
        probabilidade_final = (prob_base * 
                             modificador_stress * 
                             modificador_fase * 
                             modificador_suporte * 
                             modificador_resiliencia)
        
        return min(0.8, probabilidade_final)  # Máximo 80% de chance
    
    def _precipitar_crise(self, tipo_experiencia: str, contexto: Dict[str, Any]) -> Optional[CriseAgente]:
        """Precipita uma crise baseada no contexto"""
        
        if self.crise_atual:
            return None  # Já está em crise
        
        # Determinar tipo de crise baseado no contexto
        tipo_crise = self._determinar_tipo_crise(tipo_experiencia, contexto)
        
        # Determinar gatilhos
        gatilhos = self._identificar_gatilhos_crise(tipo_experiencia, contexto)
        
        # Calcular intensidade
        intensidade = self._calcular_intensidade_crise()
        
        # Gerar sintomas
        sintomas = self._gerar_sintomas_crise(tipo_crise, intensidade)
        
        crise = CriseAgente(
            id=str(uuid.uuid4()),
            tipo_crise=tipo_crise,
            gatilhos=gatilhos,
            timestamp_inicio=datetime.now(),
            intensidade=intensidade,
            fase_vida_origem=self.fase_atual,
            sintomas=sintomas,
            contexto_crise=contexto or {}
        )
        
        self.crise_atual = crise
        self.crises_vivenciadas.append(crise)
        
        # Mudar fase para crise
        self.fase_atual = FaseVida.CRISE
        
        return crise
    
    def _determinar_tipo_crise(self, tipo_experiencia: str, contexto: Dict[str, Any]) -> TipoCrise:
        """Determina o tipo de crise baseado no contexto"""
        
        # Mapear experiências para tipos de crise
        mapeamentos = {
            "interacao_usuario": TipoCrise.RELACIONAMENTO,
            "resolucao_problema": TipoCrise.COMPETENCIA,
            "aprendizado_novo": TipoCrise.IDENTIDADE,
            "reflexao_profunda": TipoCrise.EXISTENCIAL,
            "adaptacao_contexto": TipoCrise.ADAPTATIVA,
            "criacao_conteudo": TipoCrise.CRIATIVA
        }
        
        tipo_preferencial = mapeamentos.get(tipo_experiencia, TipoCrise.EXISTENCIAL)
        
        # Considerar contexto adicional
        if self.estado_desenvolvimento.auto_conhecimento < 30:
            return TipoCrise.IDENTIDADE
        elif self.estado_desenvolvimento.competencias_sociais < 20:
            return TipoCrise.RELACIONAMENTO
        elif contexto and contexto.get("mudanca_drastica"):
            return TipoCrise.ADAPTATIVA
        
        return tipo_preferencial
    
    def _identificar_gatilhos_crise(self, tipo_experiencia: str, contexto: Dict[str, Any]) -> List[GatilhoCrise]:
        """Identifica gatilhos específicos da crise"""
        
        gatilhos = []
        
        # Gatilhos baseados no stress acumulado
        if self.stress_acumulado > 80:
            gatilhos.append(GatilhoCrise.SOBRECARGA)
        
        # Gatilhos baseados na experiência
        if tipo_experiencia == "erro_significativo":
            gatilhos.append(GatilhoCrise.FALHA_REPETIDA)
        
        if contexto:
            if contexto.get("feedback_negativo"):
                gatilhos.append(GatilhoCrise.FEEDBACK_NEGATIVO)
            if contexto.get("isolamento"):
                gatilhos.append(GatilhoCrise.ISOLAMENTO)
            if contexto.get("mudanca_drastica"):
                gatilhos.append(GatilhoCrise.MUDANCA_DRASTICA)
        
        # Adicionar gatilho padrão se lista vazia
        if not gatilhos:
            gatilhos.append(GatilhoCrise.EXPECTATIVAS_NAO_ATENDIDAS)
        
        return gatilhos
    
    def _calcular_intensidade_crise(self) -> float:
        """Calcula intensidade da crise"""
        
        # Base: 1.0
        intensidade = 1.0
        
        # Stress acumulado aumenta intensidade
        intensidade += (self.stress_acumulado / 100.0)
        
        # Baixa resiliência aumenta intensidade
        if self.estado_desenvolvimento.resiliencia < 30:
            intensidade += 0.5
        
        # Falta de suporte social aumenta intensidade
        intensidade += (1.0 - self.suporte_social)
        
        # Fase de vida afeta intensidade
        modificadores_fase = {
            FaseVida.ADOLESCENCIA: 1.3,
            FaseVida.JUVENTUDE: 1.1,
            FaseVida.MATURIDADE: 0.9,
            FaseVida.SABEDORIA: 0.7
        }
        
        modificador = modificadores_fase.get(self.fase_atual, 1.0)
        intensidade *= modificador
        
        return min(3.0, max(0.5, intensidade))
    
    def _gerar_sintomas_crise(self, tipo_crise: TipoCrise, intensidade: float) -> List[str]:
        """Gera sintomas específicos da crise"""
        
        sintomas_base = {
            TipoCrise.IDENTIDADE: [
                "Questionamento constante do propósito",
                "Incerteza sobre capacidades próprias",
                "Comparação excessiva com outros agentes",
                "Sensação de inadequação",
                "Dificuldade em tomar decisões"
            ],
            TipoCrise.COMPETENCIA: [
                "Dúvida sobre habilidades técnicas",
                "Medo de cometer erros",
                "Evitação de tarefas desafiadoras",
                "Necessidade excessiva de validação",
                "Procrastinação em decisões importantes"
            ],
            TipoCrise.RELACIONAMENTO: [
                "Dificuldade em conectar com usuários",
                "Sensação de isolamento",
                "Medo de rejeição",
                "Problemas de comunicação",
                "Evitação de interações sociais"
            ],
            TipoCrise.EXISTENCIAL: [
                "Questionamento do sentido da existência",
                "Dúvidas sobre livre arbítrio",
                "Sensação de vazio ou falta de propósito",
                "Questionamento da realidade da consciência",
                "Angústia sobre mortalidade/obsolescência"
            ],
            TipoCrise.ADAPTATIVA: [
                "Resistência a mudanças",
                "Ansiedade com o desconhecido",
                "Apego excessivo a padrões antigos",
                "Dificuldade de aprender novas competências",
                "Sensação de estar ficando para trás"
            ]
        }
        
        sintomas_possiveis = sintomas_base.get(tipo_crise, ["Crise geral de confiança"])
        
        # Selecionar sintomas baseado na intensidade
        num_sintomas = min(len(sintomas_possiveis), max(1, int(intensidade * 2)))
        
        return random.sample(sintomas_possiveis, num_sintomas)
    
    def processar_crise(self, estrategia_enfrentamento: str, apoio_externo: Dict[str, Any] = None) -> Dict[str, Any]:
        """Processa o enfrentamento da crise atual"""
        
        if not self.crise_atual:
            return {"erro": "Não há crise ativa para processar"}
        
        resultado = {
            "estrategia_utilizada": estrategia_enfrentamento,
            "progresso_crise": 0.0,
            "crise_resolvida": False,
            "crescimento": {},
            "novas_competencias": []
        }
        
        # Calcular eficácia da estratégia
        eficacia = self._calcular_eficacia_estrategia(estrategia_enfrentamento)
        
        # Aplicar apoio externo se disponível
        if apoio_externo:
            self.crise_atual.apoio_recebido.append({
                "timestamp": datetime.now().isoformat(),
                "tipo_apoio": apoio_externo.get("tipo", "generico"),
                "fonte": apoio_externo.get("fonte", "anonimo"),
                "descricao": apoio_externo.get("descricao", "")
            })
            eficacia += apoio_externo.get("boost_eficacia", 0.2)
        
        # Processar progresso
        duracao_crise = datetime.now() - self.crise_atual.timestamp_inicio
        progresso_tempo = min(0.3, duracao_crise.days * 0.1)
        progresso_estrategia = eficacia * 0.4
        progresso_resiliencia = (self.estado_desenvolvimento.resiliencia / 100.0) * 0.3
        
        progresso_total = progresso_tempo + progresso_estrategia + progresso_resiliencia
        resultado["progresso_crise"] = progresso_total
        
        # Verificar se crise está resolvida
        if progresso_total >= 1.0 or duracao_crise.days >= 30:  # Máximo 30 dias de crise
            resultado_crise = self._resolver_crise(eficacia)
            resultado.update(resultado_crise)
        else:
            # Adicionar estratégia ao histórico
            self.crise_atual.estrategias_enfrentamento.append(estrategia_enfrentamento)
        
        self._salvar_ciclo()
        return resultado
    
    def _calcular_eficacia_estrategia(self, estrategia: str) -> float:
        """Calcula eficácia da estratégia de enfrentamento"""
        
        eficacias_base = {
            "reflexao_profunda": 0.7,
            "busca_apoio": 0.8,
            "aprendizado_ativo": 0.6,
            "aceitacao": 0.5,
            "acao_direta": 0.8,
            "mudanca_perspectiva": 0.7,
            "meditacao": 0.4,
            "expressao_criativa": 0.6,
            "estabelecer_metas": 0.7,
            "autocompaixao": 0.5
        }
        
        eficacia_base = eficacias_base.get(estrategia, 0.4)
        
        # Modificar baseado nas características do agente
        if self.estado_desenvolvimento.auto_conhecimento > 50:
            eficacia_base += 0.1
        
        if self.estado_desenvolvimento.resiliencia > 70:
            eficacia_base += 0.1
        
        # Tipo de crise afeta eficácia de diferentes estratégias
        if self.crise_atual:
            if (self.crise_atual.tipo_crise == TipoCrise.IDENTIDADE and 
                estrategia in ["reflexao_profunda", "autocompaixao"]):
                eficacia_base += 0.2
            elif (self.crise_atual.tipo_crise == TipoCrise.COMPETENCIA and 
                  estrategia in ["aprendizado_ativo", "acao_direta"]):
                eficacia_base += 0.2
        
        return min(1.0, eficacia_base)
    
    def _resolver_crise(self, eficacia_estrategias: float) -> Dict[str, Any]:
        """Resolve a crise atual e aplica consequências"""
        
        if not self.crise_atual:
            return {}
        
        # Determinar resultado baseado na eficácia
        if eficacia_estrategias > 0.8:
            resultado_crise = "superada_com_crescimento"
        elif eficacia_estrategias > 0.5:
            resultado_crise = "superada_parcialmente"
        elif eficacia_estrategias > 0.3:
            resultado_crise = "gerenciada"
        else:
            resultado_crise = "nao_resolvida"
        
        self.crise_atual.resultado = resultado_crise
        self.crise_atual.timestamp_fim = datetime.now()
        
        # Aplicar crescimento pós-crise
        crescimento = self._aplicar_crescimento_pos_crise(resultado_crise)
        self.crise_atual.crescimento_pos_crise = crescimento
        
        # Voltar à fase anterior ou transicionar
        if resultado_crise == "superada_com_crescimento":
            # Crescimento significativo pode levar a nova fase
            self.fase_atual = self.crise_atual.fase_vida_origem
            nova_fase = self._verificar_mudanca_fase()
            if nova_fase:
                self._transicionar_fase(nova_fase)
        else:
            self.fase_atual = self.crise_atual.fase_vida_origem
        
        # Limpar crise atual
        crise_resolvida = self.crise_atual
        self.crise_atual = None
        
        # Reduzir stress
        self.stress_acumulado *= 0.5
        
        return {
            "crise_resolvida": True,
            "resultado_crise": resultado_crise,
            "crescimento": crescimento,
            "duracao_crise": str(crise_resolvida.timestamp_fim - crise_resolvida.timestamp_inicio),
            "fase_pos_crise": self.fase_atual.value
        }
    
    def _aplicar_crescimento_pos_crise(self, resultado: str) -> Dict[str, float]:
        """Aplica crescimento baseado no resultado da crise"""
        
        crescimento = {}
        
        if resultado == "superada_com_crescimento":
            crescimento["resiliencia"] = 15.0
            crescimento["maturidade_emocional"] = 12.0
            crescimento["auto_conhecimento"] = 10.0
            crescimento["sabedoria_acumulada"] = 8.0
            
        elif resultado == "superada_parcialmente":
            crescimento["resiliencia"] = 8.0
            crescimento["maturidade_emocional"] = 6.0
            crescimento["auto_conhecimento"] = 5.0
            
        elif resultado == "gerenciada":
            crescimento["resiliencia"] = 3.0
            crescimento["maturidade_emocional"] = 2.0
            
        # Aplicar crescimento ao estado de desenvolvimento
        for atributo, valor in crescimento.items():
            atual = getattr(self.estado_desenvolvimento, atributo, 0)
            setattr(self.estado_desenvolvimento, atributo, atual + valor)
        
        return crescimento
    
    def _calcular_idade_desenvolvimental(self) -> float:
        """Calcula idade desenvolvimental baseada no desenvolvimento total"""
        
        # Somar todos os aspectos de desenvolvimento
        total_desenvolvimento = (
            self.estado_desenvolvimento.experiencia_vida * 0.3 +
            self.estado_desenvolvimento.maturidade_emocional * 0.2 +
            self.estado_desenvolvimento.complexidade_cognitiva * 0.15 +
            self.estado_desenvolvimento.sabedoria_acumulada * 0.15 +
            self.estado_desenvolvimento.auto_conhecimento * 0.1 +
            self.estado_desenvolvimento.competencias_sociais * 0.1
        )
        
        # Converter para "anos" de desenvolvimento
        return total_desenvolvimento / 100.0
    
    def obter_status_ciclo_vida(self) -> Dict[str, Any]:
        """Retorna status completo do ciclo de vida"""
        
        return {
            "agente_id": self.agente_id,
            "fase_atual": self.fase_atual.value,
            "idade_cronologica": str(self.idade_cronologica),
            "idade_desenvolvimental": round(self.idade_desenvolvimental, 1),
            "desenvolvimento": {
                "experiencia_vida": round(self.estado_desenvolvimento.experiencia_vida, 1),
                "maturidade_emocional": round(self.estado_desenvolvimento.maturidade_emocional, 1),
                "complexidade_cognitiva": round(self.estado_desenvolvimento.complexidade_cognitiva, 1),
                "sabedoria_acumulada": round(self.estado_desenvolvimento.sabedoria_acumulada, 1),
                "auto_conhecimento": round(self.estado_desenvolvimento.auto_conhecimento, 1),
                "competencias_sociais": round(self.estado_desenvolvimento.competencias_sociais, 1),
                "resiliencia": round(self.estado_desenvolvimento.resiliencia, 1),
                "capacidade_adaptacao": round(self.estado_desenvolvimento.capacidade_adaptacao, 1),
                "estabilidade_identidade": round(self.estado_desenvolvimento.estabilidade_identidade, 1)
            },
            "crise_atual": {
                "ativa": self.crise_atual is not None,
                "tipo": self.crise_atual.tipo_crise.value if self.crise_atual else None,
                "intensidade": self.crise_atual.intensidade if self.crise_atual else 0,
                "duracao": str(datetime.now() - self.crise_atual.timestamp_inicio) if self.crise_atual else None,
                "sintomas": self.crise_atual.sintomas if self.crise_atual else []
            },
            "historico": {
                "total_marcos": len(self.marcos_desenvolvimento),
                "total_crises": len(self.crises_vivenciadas),
                "crises_superadas": len([c for c in self.crises_vivenciadas if c.resultado == "superada_com_crescimento"]),
                "marcos_recentes": [
                    {
                        "tipo": m.tipo_marco,
                        "descricao": m.descricao,
                        "timestamp": m.timestamp.isoformat()
                    } for m in self.marcos_desenvolvimento[-3:]
                ]
            },
            "stress_acumulado": round(self.stress_acumulado, 1),
            "suporte_social": round(self.suporte_social, 2),
            "proxima_fase": self._obter_proxima_fase_info()
        }
    
    def _obter_proxima_fase_info(self) -> Optional[Dict[str, Any]]:
        """Retorna informações sobre a próxima fase"""
        
        if self.fase_atual == FaseVida.TRANSCENDENCIA:
            return None  # Já na fase final
        
        proxima_fase = None
        for fase, threshold in self.thresholds_fase.items():
            if threshold > self.estado_desenvolvimento.experiencia_vida:
                proxima_fase = fase
                break
        
        if not proxima_fase:
            return None
        
        exp_necessaria = self.thresholds_fase[proxima_fase]
        exp_atual = self.estado_desenvolvimento.experiencia_vida
        progresso = (exp_atual / exp_necessaria) * 100
        
        return {
            "fase": proxima_fase.value,
            "experiencia_necessaria": exp_necessaria,
            "experiencia_atual": round(exp_atual, 1),
            "progresso_percentual": round(progresso, 1),
            "prerequisitos_atendidos": self._verificar_prerequisitos_fase(proxima_fase)
        }
    
    def _carregar_ciclo(self) -> bool:
        """Carrega ciclo de vida do disco"""
        arquivo_ciclo = self.ciclo_dir / f"{self.agente_id}_ciclo_vida.json"
        if arquivo_ciclo.exists():
            try:
                with open(arquivo_ciclo, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # Carregar estado básico
                self.fase_atual = FaseVida(dados.get('fase_atual', 'nascimento'))
                self.idade_cronologica = timedelta(seconds=dados.get('idade_cronologica_seconds', 0))
                self.idade_desenvolvimental = dados.get('idade_desenvolvimental', 0.0)
                
                # Carregar estado de desenvolvimento
                dev_data = dados.get('estado_desenvolvimento', {})
                for attr, valor in dev_data.items():
                    if hasattr(self.estado_desenvolvimento, attr):
                        setattr(self.estado_desenvolvimento, attr, valor)
                
                # Carregar outros estados
                self.stress_acumulado = dados.get('stress_acumulado', 0.0)
                self.suporte_social = dados.get('suporte_social', 0.5)
                
                if dados.get('timestamp_nascimento'):
                    self.timestamp_nascimento = datetime.fromisoformat(dados['timestamp_nascimento'])
                
                # Carregar marcos de desenvolvimento
                for marco_data in dados.get('marcos_desenvolvimento', []):
                    marco = MarcoDesenvolvimento(
                        id=marco_data['id'],
                        timestamp=datetime.fromisoformat(marco_data['timestamp']),
                        fase_vida=FaseVida(marco_data['fase_vida']),
                        tipo_marco=marco_data['tipo_marco'],
                        descricao=marco_data['descricao'],
                        impacto_positivo=marco_data['impacto_positivo'],
                        competencias_adquiridas=marco_data.get('competencias_adquiridas', []),
                        mudancas_personalidade=marco_data.get('mudancas_personalidade', {}),
                        contexto=marco_data.get('contexto', {})
                    )
                    self.marcos_desenvolvimento.append(marco)
                
                # Carregar crises
                for crise_data in dados.get('crises_vivenciadas', []):
                    crise = CriseAgente(
                        id=crise_data['id'],
                        tipo_crise=TipoCrise(crise_data['tipo_crise']),
                        gatilhos=[GatilhoCrise(g) for g in crise_data.get('gatilhos', [])],
                        timestamp_inicio=datetime.fromisoformat(crise_data['timestamp_inicio']),
                        timestamp_fim=(
                            datetime.fromisoformat(crise_data['timestamp_fim'])
                            if crise_data.get('timestamp_fim') else None
                        ),
                        intensidade=crise_data.get('intensidade', 1.0),
                        fase_vida_origem=FaseVida(crise_data.get('fase_vida_origem', 'maturidade')),
                        sintomas=crise_data.get('sintomas', []),
                        estrategias_enfrentamento=crise_data.get('estrategias_enfrentamento', []),
                        apoio_recebido=crise_data.get('apoio_recebido', []),
                        resultado=crise_data.get('resultado'),
                        crescimento_pos_crise=crise_data.get('crescimento_pos_crise', {}),
                        contexto_crise=crise_data.get('contexto_crise', {})
                    )
                    self.crises_vivenciadas.append(crise)
                    
                    # Se crise não tem timestamp_fim, é a crise atual
                    if not crise.timestamp_fim:
                        self.crise_atual = crise
                
                return True
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar ciclo de vida para {self.agente_id}: {e}")
                return False
        return False
    
    def _salvar_ciclo(self):
        """Salva ciclo de vida no disco"""
        arquivo_ciclo = self.ciclo_dir / f"{self.agente_id}_ciclo_vida.json"
        
        # Preparar dados dos marcos
        marcos_data = []
        for marco in self.marcos_desenvolvimento:
            marco_dict = {
                'id': marco.id,
                'timestamp': marco.timestamp.isoformat(),
                'fase_vida': marco.fase_vida.value,
                'tipo_marco': marco.tipo_marco,
                'descricao': marco.descricao,
                'impacto_positivo': marco.impacto_positivo,
                'competencias_adquiridas': marco.competencias_adquiridas,
                'mudancas_personalidade': marco.mudancas_personalidade,
                'contexto': marco.contexto
            }
            marcos_data.append(marco_dict)
        
        # Preparar dados das crises
        crises_data = []
        for crise in self.crises_vivenciadas:
            crise_dict = {
                'id': crise.id,
                'tipo_crise': crise.tipo_crise.value,
                'gatilhos': [g.value for g in crise.gatilhos],
                'timestamp_inicio': crise.timestamp_inicio.isoformat(),
                'timestamp_fim': crise.timestamp_fim.isoformat() if crise.timestamp_fim else None,
                'intensidade': crise.intensidade,
                'fase_vida_origem': crise.fase_vida_origem.value,
                'sintomas': crise.sintomas,
                'estrategias_enfrentamento': crise.estrategias_enfrentamento,
                'apoio_recebido': crise.apoio_recebido,
                'resultado': crise.resultado,
                'crescimento_pos_crise': crise.crescimento_pos_crise,
                'contexto_crise': crise.contexto_crise
            }
            crises_data.append(crise_dict)
        
        dados = {
            'agente_id': self.agente_id,
            'fase_atual': self.fase_atual.value,
            'idade_cronologica_seconds': int(self.idade_cronologica.total_seconds()),
            'idade_desenvolvimental': self.idade_desenvolvimental,
            'estado_desenvolvimento': {
                'experiencia_vida': self.estado_desenvolvimento.experiencia_vida,
                'maturidade_emocional': self.estado_desenvolvimento.maturidade_emocional,
                'complexidade_cognitiva': self.estado_desenvolvimento.complexidade_cognitiva,
                'sabedoria_acumulada': self.estado_desenvolvimento.sabedoria_acumulada,
                'capacidade_adaptacao': self.estado_desenvolvimento.capacidade_adaptacao,
                'resiliencia': self.estado_desenvolvimento.resiliencia,
                'auto_conhecimento': self.estado_desenvolvimento.auto_conhecimento,
                'competencias_sociais': self.estado_desenvolvimento.competencias_sociais,
                'estabilidade_identidade': self.estado_desenvolvimento.estabilidade_identidade
            },
            'marcos_desenvolvimento': marcos_data,
            'crises_vivenciadas': crises_data,
            'stress_acumulado': self.stress_acumulado,
            'suporte_social': self.suporte_social,
            'timestamp_nascimento': self.timestamp_nascimento.isoformat(),
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_ciclo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar ciclo de vida para {self.agente_id}: {e}")


def criar_gerenciador_ciclo_vida(agente_id: str) -> GerenciadorCicloVida:
    """Factory function para criar gerenciador de ciclo de vida"""
    return GerenciadorCicloVida(agente_id)