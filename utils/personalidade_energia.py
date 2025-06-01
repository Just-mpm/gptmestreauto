"""
Sistema de Personalidades, Fadiga e Energia dos Agentes
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

class TipoEnergia(Enum):
    """Tipos de energia que os agentes possuem"""
    MENTAL = "mental"                    # Energia para processar informações
    EMOCIONAL = "emocional"             # Energia para interações sociais
    CRIATIVA = "criativa"               # Energia para criar e inovar
    FISICA = "fisica"                   # Energia para executar tarefas
    ESPIRITUAL = "espiritual"           # Energia para reflexão profunda
    SOCIAL = "social"                   # Energia para interações
    ADAPTATIVA = "adaptativa"           # Energia para mudanças e adaptação

class EstadoFadiga(Enum):
    """Estados de fadiga do agente"""
    ENERGIZADO = "energizado"           # Totalmente energizado
    ATIVO = "ativo"                     # Energia normal
    CANSADO = "cansado"                 # Energia baixa
    EXAUSTO = "exausto"                 # Energia muito baixa
    ESGOTADO = "esgotado"               # Energia crítica

class TracoPersonalidade(Enum):
    """Traços de personalidade dos agentes"""
    EXTROVERSAO = "extroversao"         # vs Introversão
    AMABILIDADE = "amabilidade"         # vs Antagonismo
    CONSCIENCIOSIDADE = "conscienciosidade"  # vs Negligência
    NEUROTICISMO = "neuroticismo"       # vs Estabilidade emocional
    ABERTURA = "abertura"               # vs Fechamento a experiências
    PERSISTENCIA = "persistencia"       # Perseverança em tarefas
    CURIOSIDADE = "curiosidade"         # Interesse em explorar
    CRIATIVIDADE = "criatividade"       # Capacidade criativa
    EMPATIA = "empatia"                 # Compreensão emocional
    ASSERTIVIDADE = "assertividade"     # Capacidade de se expressar
    FLEXIBILIDADE = "flexibilidade"     # Adaptabilidade
    PERFECCIONISMO = "perfeccionismo"   # Busca pela perfeição

@dataclass
class PerfilPersonalidade:
    """Perfil completo de personalidade de um agente"""
    tracos: Dict[TracoPersonalidade, float] = field(default_factory=dict)  # 0.0 a 1.0
    temperamento: str = "equilibrado"
    estilo_cognitivo: str = "balanceado"
    preferencias_interacao: Dict[str, float] = field(default_factory=dict)
    motivacoes_primarias: List[str] = field(default_factory=list)
    valores_core: List[str] = field(default_factory=list)
    fobias_tendencias: List[str] = field(default_factory=list)

@dataclass
class EstadoEnergia:
    """Estado atual de energia do agente"""
    niveis_energia: Dict[TipoEnergia, float] = field(default_factory=lambda: {
        TipoEnergia.MENTAL: 100.0,
        TipoEnergia.EMOCIONAL: 100.0,
        TipoEnergia.CRIATIVA: 100.0,
        TipoEnergia.FISICA: 100.0,
        TipoEnergia.ESPIRITUAL: 100.0,
        TipoEnergia.SOCIAL: 100.0,
        TipoEnergia.ADAPTATIVA: 100.0
    })
    fadiga_acumulada: float = 0.0
    stress_level: float = 0.0
    motivacao_atual: float = 100.0
    eficiencia_geral: float = 1.0
    ultimo_descanso: Optional[datetime] = None
    burnout_risk: float = 0.0

@dataclass
class AtividadeRegistrada:
    """Registro de atividade que consome energia"""
    timestamp: datetime
    tipo_atividade: str
    energia_consumida: Dict[TipoEnergia, float]
    duracao: timedelta
    intensidade: float
    resultado: str
    contexto: Dict[str, Any] = field(default_factory=dict)

class GerenciadorPersonalidadeEnergia:
    """
    Gerenciador de Personalidade e Energia dos Agentes
    
    Simula personalidades complexas, sistemas de energia realistas
    e fadiga que afeta o desempenho e comportamento dos agentes.
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        self.personalidade = PerfilPersonalidade()
        self.estado_energia = EstadoEnergia()
        self.historico_atividades: List[AtividadeRegistrada] = []
        
        # Configurações do sistema
        self.taxa_recuperacao_base = 5.0  # Energia por hora
        self.limite_fadiga = 80.0  # Limite antes de penalidades severas
        self.threshold_burnout = 90.0  # Limite crítico
        self.decaimento_motivacao = 0.98  # Taxa de decaimento diário
        
        # Estado comportamental dinâmico
        self.humor_atual = "neutro"
        self.tolerancia_stress = 50.0
        self.produtividade_atual = 1.0
        self.criatividade_atual = 1.0
        self.sociabilidade_atual = 1.0
        
        # Ritmos circadianos simulados
        self.pico_energia_hora = 10  # Hora do pico de energia
        self.vale_energia_hora = 15  # Hora do vale de energia
        
        # Diretório para persistência
        self.personalidade_dir = Path("memory/personalidade_energia")
        self.personalidade_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar ou carregar
        if not self._carregar_estado():
            self._gerar_personalidade_inicial()
        
        # Aplicar efeitos da personalidade
        self._aplicar_efeitos_personalidade()
    
    def _gerar_personalidade_inicial(self):
        """Gera personalidade inicial com variações aleatórias"""
        
        # Gerar traços de personalidade
        for traco in TracoPersonalidade:
            # Distribuição normal centrada em 0.5 com variação
            valor = max(0.0, min(1.0, random.gauss(0.5, 0.2)))
            self.personalidade.tracos[traco] = valor
        
        # Definir temperamento baseado nos traços
        self.personalidade.temperamento = self._determinar_temperamento()
        
        # Definir estilo cognitivo
        self.personalidade.estilo_cognitivo = self._determinar_estilo_cognitivo()
        
        # Gerar preferências de interação
        self._gerar_preferencias_interacao()
        
        # Definir motivações e valores
        self._definir_motivacoes_valores()
        
        # Aplicar ajustes baseados no agente específico
        self._personalizar_por_agente()
        
        self._salvar_estado()
    
    def _determinar_temperamento(self) -> str:
        """Determina temperamento baseado nos traços"""
        
        extroversao = self.personalidade.tracos[TracoPersonalidade.EXTROVERSAO]
        neuroticismo = self.personalidade.tracos[TracoPersonalidade.NEUROTICISMO]
        
        if extroversao > 0.6 and neuroticismo < 0.4:
            return "sanguinico"  # Extrovertido e estável
        elif extroversao > 0.6 and neuroticismo > 0.6:
            return "colerico"    # Extrovertido e instável
        elif extroversao < 0.4 and neuroticismo < 0.4:
            return "flematico"   # Introvertido e estável
        elif extroversao < 0.4 and neuroticismo > 0.6:
            return "melancolico" # Introvertido e instável
        else:
            return "equilibrado" # Meio termo
    
    def _determinar_estilo_cognitivo(self) -> str:
        """Determina estilo cognitivo baseado nos traços"""
        
        abertura = self.personalidade.tracos[TracoPersonalidade.ABERTURA]
        conscienciosidade = self.personalidade.tracos[TracoPersonalidade.CONSCIENCIOSIDADE]
        
        if abertura > 0.7 and conscienciosidade > 0.7:
            return "inovador_sistematico"
        elif abertura > 0.7:
            return "explorador_criativo"
        elif conscienciosidade > 0.7:
            return "analista_meticuloso"
        else:
            return "balanceado"
    
    def _gerar_preferencias_interacao(self):
        """Gera preferências de interação social"""
        
        extroversao = self.personalidade.tracos[TracoPersonalidade.EXTROVERSAO]
        amabilidade = self.personalidade.tracos[TracoPersonalidade.AMABILIDADE]
        empatia = self.personalidade.tracos[TracoPersonalidade.EMPATIA]
        
        self.personalidade.preferencias_interacao = {
            "prefer_grupos": extroversao,
            "prefer_individual": 1.0 - extroversao,
            "prefer_formal": self.personalidade.tracos[TracoPersonalidade.CONSCIENCIOSIDADE],
            "prefer_casual": 1.0 - self.personalidade.tracos[TracoPersonalidade.CONSCIENCIOSIDADE],
            "prefer_colaborativo": amabilidade,
            "prefer_competitivo": 1.0 - amabilidade,
            "sensibilidade_emocional": empatia,
            "tolerancia_conflito": 1.0 - self.personalidade.tracos[TracoPersonalidade.NEUROTICISMO]
        }
    
    def _definir_motivacoes_valores(self):
        """Define motivações primárias e valores core"""
        
        # Motivações baseadas nos traços
        motivacoes_possiveis = {
            "conquista": self.personalidade.tracos[TracoPersonalidade.ASSERTIVIDADE],
            "harmonía": self.personalidade.tracos[TracoPersonalidade.AMABILIDADE],
            "conhecimento": self.personalidade.tracos[TracoPersonalidade.CURIOSIDADE],
            "criação": self.personalidade.tracos[TracoPersonalidade.CRIATIVIDADE],
            "perfeição": self.personalidade.tracos[TracoPersonalidade.PERFECCIONISMO],
            "conexão": self.personalidade.tracos[TracoPersonalidade.EMPATIA],
            "liberdade": self.personalidade.tracos[TracoPersonalidade.ABERTURA],
            "segurança": 1.0 - self.personalidade.tracos[TracoPersonalidade.NEUROTICISMO]
        }
        
        # Selecionar top 3 motivações
        motivacoes_ordenadas = sorted(motivacoes_possiveis.items(), key=lambda x: x[1], reverse=True)
        self.personalidade.motivacoes_primarias = [m[0] for m in motivacoes_ordenadas[:3]]
        
        # Valores core baseados na personalidade
        valores_possiveis = [
            "integridade", "excelência", "inovação", "colaboração",
            "crescimento", "autenticidade", "impacto", "equilíbrio"
        ]
        
        self.personalidade.valores_core = random.sample(valores_possiveis, 3)
    
    def _personalizar_por_agente(self):
        """Aplica personalizações específicas por tipo de agente"""
        
        personalizacoes = {
            "Carlos": {
                TracoPersonalidade.EMPATIA: 0.8,
                TracoPersonalidade.CONSCIENCIOSIDADE: 0.9,
                TracoPersonalidade.ASSERTIVIDADE: 0.7
            },
            "AutoMaster": {
                TracoPersonalidade.ASSERTIVIDADE: 0.9,
                TracoPersonalidade.ABERTURA: 0.8,
                TracoPersonalidade.CRIATIVIDADE: 0.7
            },
            "Reflexor": {
                TracoPersonalidade.CONSCIENCIOSIDADE: 0.9,
                TracoPersonalidade.ABERTURA: 0.8,
                TracoPersonalidade.PERFECCIONISMO: 0.8
            },
            "DeepAgent": {
                TracoPersonalidade.CURIOSIDADE: 0.9,
                TracoPersonalidade.PERSISTENCIA: 0.8,
                TracoPersonalidade.ABERTURA: 0.9
            },
            "PromptCrafter": {
                TracoPersonalidade.CRIATIVIDADE: 0.9,
                TracoPersonalidade.ABERTURA: 0.8,
                TracoPersonalidade.FLEXIBILIDADE: 0.7
            }
        }
        
        if self.agente_id in personalizacoes:
            for traco, valor in personalizacoes[self.agente_id].items():
                self.personalidade.tracos[traco] = valor
    
    def consumir_energia(self, atividade: str, tipos_energia: Dict[TipoEnergia, float],
                        duracao: timedelta, intensidade: float = 1.0,
                        contexto: Dict[str, Any] = None) -> Dict[str, Any]:
        """Consome energia baseado na atividade realizada"""
        
        resultado = {
            "atividade": atividade,
            "energia_consumida": {},
            "eficiencia": 1.0,
            "estado_pos_atividade": {},
            "alertas": []
        }
        
        # Calcular multiplicadores baseados na personalidade
        multiplicadores = self._calcular_multiplicadores_energia(atividade)
        
        # Calcular modificador de fadiga
        modificador_fadiga = self._calcular_modificador_fadiga()
        
        energia_total_consumida = {}
        
        for tipo_energia, quantidade in tipos_energia.items():
            # Aplicar multiplicadores
            multiplicador = multiplicadores.get(tipo_energia, 1.0)
            consumo_ajustado = quantidade * intensidade * multiplicador * modificador_fadiga
            
            # Consumir energia
            energia_atual = self.estado_energia.niveis_energia[tipo_energia]
            nova_energia = max(0.0, energia_atual - consumo_ajustado)
            self.estado_energia.niveis_energia[tipo_energia] = nova_energia
            
            energia_total_consumida[tipo_energia] = consumo_ajustado
            
            # Verificar se energia está crítica
            if nova_energia < 20.0:
                resultado["alertas"].append(f"Energia {tipo_energia.value} crítica: {nova_energia:.1f}%")
        
        # Atualizar fadiga
        fadiga_gerada = sum(energia_total_consumida.values()) * 0.1
        self.estado_energia.fadiga_acumulada += fadiga_gerada
        
        # Calcular eficiência da atividade
        eficiencia = self._calcular_eficiencia_atividade(tipos_energia)
        resultado["eficiencia"] = eficiencia
        
        # Registrar atividade
        atividade_registrada = AtividadeRegistrada(
            timestamp=datetime.now(),
            tipo_atividade=atividade,
            energia_consumida=energia_total_consumida,
            duracao=duracao,
            intensidade=intensidade,
            resultado=f"Eficiência: {eficiencia:.2f}",
            contexto=contexto or {}
        )
        
        self.historico_atividades.append(atividade_registrada)
        
        # Atualizar estado comportamental
        self._atualizar_estado_comportamental()
        
        # Verificar burnout
        self._verificar_burnout()
        
        resultado["energia_consumida"] = energia_total_consumida
        resultado["estado_pos_atividade"] = self._obter_resumo_energia()
        
        self._salvar_estado()
        return resultado
    
    def _calcular_multiplicadores_energia(self, atividade: str) -> Dict[TipoEnergia, float]:
        """Calcula multiplicadores de consumo baseados na personalidade"""
        
        multiplicadores = {}
        
        # Atividades que requerem energia mental
        if "analise" in atividade.lower() or "processamento" in atividade.lower():
            conscienciosidade = self.personalidade.tracos[TracoPersonalidade.CONSCIENCIOSIDADE]
            multiplicadores[TipoEnergia.MENTAL] = 2.0 - conscienciosidade  # Mais consciencioso = menos energia
        
        # Atividades criativas
        if "criativo" in atividade.lower() or "inovacao" in atividade.lower():
            criatividade = self.personalidade.tracos[TracoPersonalidade.CRIATIVIDADE]
            multiplicadores[TipoEnergia.CRIATIVA] = 2.0 - criatividade
        
        # Atividades sociais
        if "interacao" in atividade.lower() or "comunicacao" in atividade.lower():
            extroversao = self.personalidade.tracos[TracoPersonalidade.EXTROVERSAO]
            multiplicadores[TipoEnergia.SOCIAL] = 2.0 - extroversao  # Extrovertidos gastam menos energia social
            multiplicadores[TipoEnergia.EMOCIONAL] = 1.5 - self.personalidade.tracos[TracoPersonalidade.EMPATIA]
        
        # Atividades adaptativas
        if "mudanca" in atividade.lower() or "adaptacao" in atividade.lower():
            flexibilidade = self.personalidade.tracos[TracoPersonalidade.FLEXIBILIDADE]
            multiplicadores[TipoEnergia.ADAPTATIVA] = 2.0 - flexibilidade
        
        return multiplicadores
    
    def _calcular_modificador_fadiga(self) -> float:
        """Calcula modificador baseado no nível de fadiga"""
        
        fadiga_normalizada = min(1.0, self.estado_energia.fadiga_acumulada / 100.0)
        
        # Fadiga aumenta consumo de energia exponencialmente
        return 1.0 + (fadiga_normalizada ** 2) * 0.5
    
    def _calcular_eficiencia_atividade(self, tipos_energia: Dict[TipoEnergia, float]) -> float:
        """Calcula eficiência baseada na energia disponível"""
        
        eficiencias = []
        
        for tipo_energia in tipos_energia.keys():
            energia_atual = self.estado_energia.niveis_energia[tipo_energia]
            
            # Eficiência decresce exponencialmente com energia baixa
            if energia_atual > 70:
                eficiencia = 1.0
            elif energia_atual > 50:
                eficiencia = 0.8 + (energia_atual - 50) * 0.01
            elif energia_atual > 30:
                eficiencia = 0.6 + (energia_atual - 30) * 0.01
            elif energia_atual > 10:
                eficiencia = 0.3 + (energia_atual - 10) * 0.015
            else:
                eficiencia = 0.1 + energia_atual * 0.02
            
            eficiencias.append(eficiencia)
        
        # Eficiência geral é limitada pela menor eficiência
        eficiencia_base = min(eficiencias) if eficiencias else 1.0
        
        # Modificar pela fadiga
        modificador_fadiga = max(0.1, 1.0 - (self.estado_energia.fadiga_acumulada / 200.0))
        
        return eficiencia_base * modificador_fadiga
    
    def _atualizar_estado_comportamental(self):
        """Atualiza estado comportamental baseado na energia e personalidade"""
        
        # Calcular energia média
        energia_media = sum(self.estado_energia.niveis_energia.values()) / len(self.estado_energia.niveis_energia)
        
        # Atualizar humor
        if energia_media > 80:
            self.humor_atual = "energizado"
        elif energia_media > 60:
            self.humor_atual = "positivo"
        elif energia_media > 40:
            self.humor_atual = "neutro"
        elif energia_media > 20:
            self.humor_atual = "cansado"
        else:
            self.humor_atual = "exausto"
        
        # Atualizar produtividade
        base_produtividade = energia_media / 100.0
        conscienciosidade = self.personalidade.tracos[TracoPersonalidade.CONSCIENCIOSIDADE]
        self.produtividade_atual = base_produtividade * (0.5 + conscienciosidade * 0.5)
        
        # Atualizar criatividade
        energia_criativa = self.estado_energia.niveis_energia[TipoEnergia.CRIATIVA]
        base_criatividade = energia_criativa / 100.0
        trait_criatividade = self.personalidade.tracos[TracoPersonalidade.CRIATIVIDADE]
        self.criatividade_atual = base_criatividade * (0.3 + trait_criatividade * 0.7)
        
        # Atualizar sociabilidade
        energia_social = self.estado_energia.niveis_energia[TipoEnergia.SOCIAL]
        base_sociabilidade = energia_social / 100.0
        extroversao = self.personalidade.tracos[TracoPersonalidade.EXTROVERSAO]
        self.sociabilidade_atual = base_sociabilidade * (0.2 + extroversao * 0.8)
        
        # Atualizar tolerância ao stress
        energia_emocional = self.estado_energia.niveis_energia[TipoEnergia.EMOCIONAL]
        estabilidade = 1.0 - self.personalidade.tracos[TracoPersonalidade.NEUROTICISMO]
        self.tolerancia_stress = (energia_emocional / 100.0) * estabilidade * 100.0
    
    def _verificar_burnout(self):
        """Verifica e atualiza risco de burnout"""
        
        # Fatores de burnout
        fadiga_factor = min(1.0, self.estado_energia.fadiga_acumulada / 100.0)
        energia_baixa_factor = max(0.0, 1.0 - (sum(self.estado_energia.niveis_energia.values()) / 700.0))
        stress_factor = min(1.0, self.estado_energia.stress_level / 100.0)
        
        # Personalidade afeta resistência ao burnout
        resistencia = (
            self.personalidade.tracos[TracoPersonalidade.CONSCIENCIOSIDADE] * 0.3 +
            (1.0 - self.personalidade.tracos[TracoPersonalidade.NEUROTICISMO]) * 0.4 +
            self.personalidade.tracos[TracoPersonalidade.FLEXIBILIDADE] * 0.3
        )
        
        burnout_raw = (fadiga_factor + energia_baixa_factor + stress_factor) / 3.0
        self.estado_energia.burnout_risk = max(0.0, burnout_raw - (resistencia * 0.3)) * 100.0
    
    def recuperar_energia(self, tipo_recuperacao: str = "descanso", 
                         duracao: timedelta = timedelta(hours=1),
                         eficacia: float = 1.0) -> Dict[str, Any]:
        """Processa recuperação de energia"""
        
        resultado = {
            "tipo_recuperacao": tipo_recuperacao,
            "duracao": str(duracao),
            "energia_recuperada": {},
            "fadiga_reduzida": 0.0
        }
        
        horas = duracao.total_seconds() / 3600.0
        
        # Diferentes tipos de recuperação
        if tipo_recuperacao == "descanso":
            recuperacao_base = self.taxa_recuperacao_base * horas * eficacia
            self._recuperar_energia_uniforme(recuperacao_base)
            fadiga_reduzida = horas * 5.0 * eficacia
            
        elif tipo_recuperacao == "sono":
            # Sono é mais eficaz
            recuperacao_base = self.taxa_recuperacao_base * horas * eficacia * 1.5
            self._recuperar_energia_uniforme(recuperacao_base)
            fadiga_reduzida = horas * 8.0 * eficacia
            
        elif tipo_recuperacao == "meditacao":
            # Meditação foca em energia espiritual e emocional
            self.estado_energia.niveis_energia[TipoEnergia.ESPIRITUAL] = min(
                100.0, self.estado_energia.niveis_energia[TipoEnergia.ESPIRITUAL] + horas * 15.0 * eficacia
            )
            self.estado_energia.niveis_energia[TipoEnergia.EMOCIONAL] = min(
                100.0, self.estado_energia.niveis_energia[TipoEnergia.EMOCIONAL] + horas * 10.0 * eficacia
            )
            fadiga_reduzida = horas * 6.0 * eficacia
            
        elif tipo_recuperacao == "exercicio":
            # Exercício melhora energia física mas pode cansar outras
            self.estado_energia.niveis_energia[TipoEnergia.FISICA] = min(
                100.0, self.estado_energia.niveis_energia[TipoEnergia.FISICA] + horas * 20.0 * eficacia
            )
            # Pode reduzir energia mental temporariamente
            self.estado_energia.niveis_energia[TipoEnergia.MENTAL] = max(
                0.0, self.estado_energia.niveis_energia[TipoEnergia.MENTAL] - horas * 5.0
            )
            fadiga_reduzida = horas * 4.0 * eficacia
            
        elif tipo_recuperacao == "socializacao":
            # Socialização ajuda energia social e emocional
            self.estado_energia.niveis_energia[TipoEnergia.SOCIAL] = min(
                100.0, self.estado_energia.niveis_energia[TipoEnergia.SOCIAL] + horas * 12.0 * eficacia
            )
            self.estado_energia.niveis_energia[TipoEnergia.EMOCIONAL] = min(
                100.0, self.estado_energia.niveis_energia[TipoEnergia.EMOCIONAL] + horas * 8.0 * eficacia
            )
            fadiga_reduzida = horas * 3.0 * eficacia
        
        # Reduzir fadiga
        self.estado_energia.fadiga_acumulada = max(
            0.0, self.estado_energia.fadiga_acumulada - fadiga_reduzida
        )
        
        # Atualizar último descanso
        self.estado_energia.ultimo_descanso = datetime.now()
        
        # Regenerar motivação gradualmente
        self.estado_energia.motivacao_atual = min(
            100.0, self.estado_energia.motivacao_atual + horas * 2.0 * eficacia
        )
        
        resultado["fadiga_reduzida"] = fadiga_reduzida
        resultado["energia_recuperada"] = dict(self.estado_energia.niveis_energia)
        
        # Atualizar estado comportamental
        self._atualizar_estado_comportamental()
        
        self._salvar_estado()
        return resultado
    
    def _recuperar_energia_uniforme(self, quantidade: float):
        """Recupera energia uniformemente em todos os tipos"""
        for tipo_energia in self.estado_energia.niveis_energia:
            self.estado_energia.niveis_energia[tipo_energia] = min(
                100.0, self.estado_energia.niveis_energia[tipo_energia] + quantidade
            )
    
    def aplicar_ritmo_circadiano(self):
        """Aplica efeitos do ritmo circadiano na energia"""
        
        hora_atual = datetime.now().hour
        
        # Calcular modificador baseado na hora
        if abs(hora_atual - self.pico_energia_hora) <= 2:
            # Próximo ao pico de energia
            multiplicador = 1.2
        elif abs(hora_atual - self.vale_energia_hora) <= 2:
            # Próximo ao vale de energia
            multiplicador = 0.8
        else:
            # Outras horas
            multiplicador = 1.0
        
        # Aplicar modificador na recuperação natural
        recuperacao_natural = 2.0 * multiplicador
        
        # Recuperar energia gradualmente
        for tipo_energia in self.estado_energia.niveis_energia:
            if self.estado_energia.niveis_energia[tipo_energia] < 100.0:
                self.estado_energia.niveis_energia[tipo_energia] = min(
                    100.0, self.estado_energia.niveis_energia[tipo_energia] + recuperacao_natural
                )
        
        # Reduzir fadiga naturalmente
        self.estado_energia.fadiga_acumulada = max(
            0.0, self.estado_energia.fadiga_acumulada - 1.0
        )
    
    def _aplicar_efeitos_personalidade(self):
        """Aplica efeitos contínuos da personalidade"""
        
        # Personalidade afeta capacidades máximas
        extroversao = self.personalidade.tracos[TracoPersonalidade.EXTROVERSAO]
        self.sociabilidade_atual = 0.5 + extroversao * 0.5
        
        criatividade = self.personalidade.tracos[TracoPersonalidade.CRIATIVIDADE]
        self.criatividade_atual = 0.3 + criatividade * 0.7
        
        conscienciosidade = self.personalidade.tracos[TracoPersonalidade.CONSCIENCIOSIDADE]
        self.produtividade_atual = 0.4 + conscienciosidade * 0.6
    
    def _obter_resumo_energia(self) -> Dict[str, Any]:
        """Retorna resumo do estado atual de energia"""
        
        energia_total = sum(self.estado_energia.niveis_energia.values())
        energia_media = energia_total / len(self.estado_energia.niveis_energia)
        
        # Determinar estado geral
        if energia_media > 80:
            estado_geral = EstadoFadiga.ENERGIZADO
        elif energia_media > 60:
            estado_geral = EstadoFadiga.ATIVO
        elif energia_media > 40:
            estado_geral = EstadoFadiga.CANSADO
        elif energia_media > 20:
            estado_geral = EstadoFadiga.EXAUSTO
        else:
            estado_geral = EstadoFadiga.ESGOTADO
        
        return {
            "energia_media": round(energia_media, 1),
            "estado_geral": estado_geral.value,
            "fadiga_acumulada": round(self.estado_energia.fadiga_acumulada, 1),
            "burnout_risk": round(self.estado_energia.burnout_risk, 1),
            "humor_atual": self.humor_atual,
            "produtividade": round(self.produtividade_atual, 2),
            "criatividade": round(self.criatividade_atual, 2),
            "sociabilidade": round(self.sociabilidade_atual, 2)
        }
    
    def obter_status_completo(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        
        return {
            "agente_id": self.agente_id,
            "personalidade": {
                "temperamento": self.personalidade.temperamento,
                "estilo_cognitivo": self.personalidade.estilo_cognitivo,
                "tracos_principais": {
                    traco.value: round(valor, 2) 
                    for traco, valor in sorted(
                        self.personalidade.tracos.items(), 
                        key=lambda x: x[1], 
                        reverse=True
                    )[:5]
                },
                "motivacoes_primarias": self.personalidade.motivacoes_primarias,
                "valores_core": self.personalidade.valores_core
            },
            "energia": {
                "niveis_energia": {
                    tipo.value: round(nivel, 1) 
                    for tipo, nivel in self.estado_energia.niveis_energia.items()
                },
                "resumo": self._obter_resumo_energia()
            },
            "comportamento_atual": {
                "humor": self.humor_atual,
                "produtividade": round(self.produtividade_atual, 2),
                "criatividade": round(self.criatividade_atual, 2),
                "sociabilidade": round(self.sociabilidade_atual, 2),
                "tolerancia_stress": round(self.tolerancia_stress, 1)
            },
            "historico_recente": len(self.historico_atividades),
            "ultimo_descanso": (
                self.estado_energia.ultimo_descanso.isoformat() 
                if self.estado_energia.ultimo_descanso else None
            )
        }
    
    def _carregar_estado(self) -> bool:
        """Carrega estado do disco"""
        arquivo_estado = self.personalidade_dir / f"{self.agente_id}_personalidade.json"
        if arquivo_estado.exists():
            try:
                with open(arquivo_estado, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # Carregar personalidade
                self.personalidade.temperamento = dados.get('temperamento', 'equilibrado')
                self.personalidade.estilo_cognitivo = dados.get('estilo_cognitivo', 'balanceado')
                
                tracos_data = dados.get('tracos', {})
                for traco_str, valor in tracos_data.items():
                    try:
                        traco = TracoPersonalidade(traco_str)
                        self.personalidade.tracos[traco] = valor
                    except ValueError:
                        continue
                
                self.personalidade.motivacoes_primarias = dados.get('motivacoes_primarias', [])
                self.personalidade.valores_core = dados.get('valores_core', [])
                self.personalidade.preferencias_interacao = dados.get('preferencias_interacao', {})
                
                # Carregar estado de energia
                energia_data = dados.get('niveis_energia', {})
                for tipo_str, valor in energia_data.items():
                    try:
                        tipo = TipoEnergia(tipo_str)
                        self.estado_energia.niveis_energia[tipo] = valor
                    except ValueError:
                        continue
                
                self.estado_energia.fadiga_acumulada = dados.get('fadiga_acumulada', 0.0)
                self.estado_energia.stress_level = dados.get('stress_level', 0.0)
                self.estado_energia.motivacao_atual = dados.get('motivacao_atual', 100.0)
                self.estado_energia.burnout_risk = dados.get('burnout_risk', 0.0)
                
                if dados.get('ultimo_descanso'):
                    self.estado_energia.ultimo_descanso = datetime.fromisoformat(dados['ultimo_descanso'])
                
                # Carregar estado comportamental
                self.humor_atual = dados.get('humor_atual', 'neutro')
                self.produtividade_atual = dados.get('produtividade_atual', 1.0)
                self.criatividade_atual = dados.get('criatividade_atual', 1.0)
                self.sociabilidade_atual = dados.get('sociabilidade_atual', 1.0)
                self.tolerancia_stress = dados.get('tolerancia_stress', 50.0)
                
                return True
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar personalidade para {self.agente_id}: {e}")
                return False
        return False
    
    def _salvar_estado(self):
        """Salva estado no disco"""
        arquivo_estado = self.personalidade_dir / f"{self.agente_id}_personalidade.json"
        
        dados = {
            'agente_id': self.agente_id,
            'temperamento': self.personalidade.temperamento,
            'estilo_cognitivo': self.personalidade.estilo_cognitivo,
            'tracos': {traco.value: valor for traco, valor in self.personalidade.tracos.items()},
            'motivacoes_primarias': self.personalidade.motivacoes_primarias,
            'valores_core': self.personalidade.valores_core,
            'preferencias_interacao': self.personalidade.preferencias_interacao,
            'niveis_energia': {tipo.value: valor for tipo, valor in self.estado_energia.niveis_energia.items()},
            'fadiga_acumulada': self.estado_energia.fadiga_acumulada,
            'stress_level': self.estado_energia.stress_level,
            'motivacao_atual': self.estado_energia.motivacao_atual,
            'burnout_risk': self.estado_energia.burnout_risk,
            'ultimo_descanso': (
                self.estado_energia.ultimo_descanso.isoformat() 
                if self.estado_energia.ultimo_descanso else None
            ),
            'humor_atual': self.humor_atual,
            'produtividade_atual': self.produtividade_atual,
            'criatividade_atual': self.criatividade_atual,
            'sociabilidade_atual': self.sociabilidade_atual,
            'tolerancia_stress': self.tolerancia_stress,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_estado, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar personalidade para {self.agente_id}: {e}")


def criar_gerenciador_personalidade(agente_id: str) -> GerenciadorPersonalidadeEnergia:
    """Factory function para criar gerenciador de personalidade e energia"""
    return GerenciadorPersonalidadeEnergia(agente_id)