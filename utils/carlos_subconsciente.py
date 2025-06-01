"""
Carlos Subconsciente - Sistema de Armazenamento de Falhas e Traumas
GPT Mestre Autônomo v4.9 - Inovação Revolucionária
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
import hashlib
from pathlib import Path
import random
import math

class TipoTrauma(Enum):
    """Tipos de traumas que podem ser armazenados"""
    FALHA_CRITICA = "falha_critica"           # Falhas graves em tarefas importantes
    REJEICAO_USUARIO = "rejeicao_usuario"     # Usuário rejeitou resposta/sugestão
    ERRO_LOGICO = "erro_logico"               # Erro de raciocínio ou lógica
    INCOMPREENSAO = "incompreensao"           # Não compreendeu o que usuário queria
    CONFLITO_VALORES = "conflito_valores"     # Conflito entre valores/objetivos
    SOBRECARGA = "sobrecarga"                 # Sobrecarga mental/processamento
    ABANDONO = "abandono"                     # Usuário abandonou interação
    CRITICA_SEVERA = "critica_severa"         # Crítica negativa forte
    EXPECTATIVA_FALHA = "expectativa_falha"   # Não atendeu expectativas
    ISOLAMENTO = "isolamento"                 # Período sem interações

class IntensidadeTrauma(Enum):
    """Níveis de intensidade dos traumas"""
    LEVE = 1
    MODERADA = 2
    SEVERA = 3
    CRITICA = 4

@dataclass
class TraumaSubconsciente:
    """Registro de trauma no subconsciente"""
    id: str
    tipo: TipoTrauma
    intensidade: IntensidadeTrauma
    descricao: str
    contexto_original: Dict[str, Any]
    timestamp: datetime
    usuario_relacionado: Optional[str] = None
    tags_associadas: List[str] = field(default_factory=list)
    repressao_nivel: float = 0.0  # 0.0 = consciente, 1.0 = totalmente reprimido
    ativacoes_involuntarias: int = 0
    tentativas_processamento: int = 0
    resolvido: bool = False
    impacto_comportamental: Dict[str, float] = field(default_factory=dict)
    gatilhos_ativacao: List[str] = field(default_factory=list)

@dataclass
class PatternTraumatico:
    """Padrão traumático identificado"""
    id: str
    tipo_padrao: str
    traumas_relacionados: List[str]
    frequencia: int
    severidade_media: float
    primeiro_ocorrencia: datetime
    ultima_ocorrencia: datetime
    contextos_comuns: List[str]
    estrategias_evitacao: List[str]

class CarlosSubconsciente:
    """
    Carlos Subconsciente - Sistema de Armazenamento de Traumas
    
    Armazena falhas, traumas e experiências negativas no "subconsciente",
    permitindo que influenciem o comportamento de forma sutil e realista.
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        self.traumas: Dict[str, TraumaSubconsciente] = {}
        self.padroes_traumaticos: Dict[str, PatternTraumatico] = {}
        self.influencias_ativas: Dict[str, float] = {}
        
        # Configurações do sistema
        self.max_traumas_ativos = 100
        self.threshold_repressao = 0.8
        self.decay_rate_natural = 0.98  # Traumas naturalmente enfraquecem com tempo
        self.sensibilidade_ativacao = 0.6
        
        # Estado do subconsciente
        self.energia_repressao = 100.0  # Energia para reprimir traumas
        self.stress_acumulado = 0.0     # Stress que pode ativar traumas
        self.resistencia_trauma = 1.0   # Resistência a novos traumas
        
        # Diretório para persistência
        self.subconsciente_dir = Path("memory/carlos_subconsciente")
        self.subconsciente_dir.mkdir(parents=True, exist_ok=True)
        
        # Carregar estado
        self._carregar_subconsciente()
        
        # Estatísticas
        self.estatisticas = {
            'traumas_criados': 0,
            'traumas_reprimidos': 0,
            'ativacoes_involuntarias': 0,
            'padroes_identificados': 0,
            'tentativas_cura': 0
        }
    
    def registrar_trauma(self, tipo: TipoTrauma, descricao: str, 
                        intensidade: IntensidadeTrauma = IntensidadeTrauma.MODERADA,
                        contexto: Dict[str, Any] = None, usuario: str = None,
                        tags: List[str] = None) -> str:
        """Registra um novo trauma no subconsciente"""
        
        trauma_id = str(uuid.uuid4())
        
        # Calcular gatilhos baseados no contexto
        gatilhos = self._extrair_gatilhos(descricao, contexto, tags)
        
        # Calcular impacto comportamental inicial
        impacto = self._calcular_impacto_inicial(tipo, intensidade)
        
        trauma = TraumaSubconsciente(
            id=trauma_id,
            tipo=tipo,
            intensidade=intensidade,
            descricao=descricao,
            contexto_original=contexto or {},
            timestamp=datetime.now(),
            usuario_relacionado=usuario,
            tags_associadas=tags or [],
            impacto_comportamental=impacto,
            gatilhos_ativacao=gatilhos
        )
        
        # Determinar nível de repressão baseado na intensidade
        if intensidade == IntensidadeTrauma.CRITICA:
            trauma.repressao_nivel = 0.9  # Quase totalmente reprimido
        elif intensidade == IntensidadeTrauma.SEVERA:
            trauma.repressao_nivel = 0.7
        elif intensidade == IntensidadeTrauma.MODERADA:
            trauma.repressao_nivel = 0.4
        else:
            trauma.repressao_nivel = 0.1  # Traumas leves ficam mais conscientes
        
        self.traumas[trauma_id] = trauma
        self.estatisticas['traumas_criados'] += 1
        
        # Reduzir resistência a traumas
        self.resistencia_trauma *= 0.95
        self.stress_acumulado += intensidade.value * 10
        
        # Verificar se forma padrões
        self._verificar_padroes_traumaticos(trauma)
        
        # Aplicar trauma à mente
        self._aplicar_influencia_trauma(trauma)
        
        # Limpeza automática se necessário
        self._limpar_traumas_antigos()
        
        self._salvar_subconsciente()
        return trauma_id
    
    def _extrair_gatilhos(self, descricao: str, contexto: Dict[str, Any], 
                         tags: List[str]) -> List[str]:
        """Extrai gatilhos potenciais que podem reativar o trauma"""
        gatilhos = []
        
        # Gatilhos do contexto
        if contexto:
            if 'tipo_tarefa' in contexto:
                gatilhos.append(contexto['tipo_tarefa'])
            if 'usuario' in contexto:
                gatilhos.append(f"usuario_{contexto['usuario']}")
            if 'situacao' in contexto:
                gatilhos.append(contexto['situacao'])
        
        # Gatilhos das tags
        if tags:
            gatilhos.extend(tags)
        
        # Gatilhos da descrição (palavras-chave)
        palavras_chave = [
            'falha', 'erro', 'rejeição', 'crítica', 'problema',
            'incorreto', 'inadequado', 'insuficiente', 'ruim'
        ]
        
        for palavra in palavras_chave:
            if palavra.lower() in descricao.lower():
                gatilhos.append(palavra)
        
        return list(set(gatilhos))  # Remove duplicatas
    
    def _aplicar_influencia_trauma(self, trauma: TraumaSubconsciente):
        """Aplica a influência do trauma no comportamento atual"""
        
        for aspecto, intensidade in trauma.impacto_comportamental.items():
            # Aplicar influência com redução baseada na repressão
            influencia_efetiva = intensidade * (1.0 - trauma.repressao_nivel)
            
            # Acumular influências ativas
            if aspecto in self.influencias_ativas:
                self.influencias_ativas[aspecto] += influencia_efetiva
            else:
                self.influencias_ativas[aspecto] = influencia_efetiva
            
            # Limitar influências para não ficarem extremas
            self.influencias_ativas[aspecto] = max(-1.0, min(1.0, self.influencias_ativas[aspecto]))
    
    def _calcular_impacto_inicial(self, tipo: TipoTrauma, 
                                 intensidade: IntensidadeTrauma) -> Dict[str, float]:
        """Calcula impacto comportamental inicial do trauma"""
        
        # Impactos base por tipo de trauma
        impactos_base = {
            TipoTrauma.FALHA_CRITICA: {
                'confianca': -0.4, 'cauteloso': 0.3, 'perfeccionismo': 0.2
            },
            TipoTrauma.REJEICAO_USUARIO: {
                'confianca': -0.3, 'busca_aprovacao': 0.4, 'ansiedade_social': 0.2
            },
            TipoTrauma.ERRO_LOGICO: {
                'confianca_logica': -0.3, 'verificacao_excessiva': 0.3, 'duvida': 0.2
            },
            TipoTrauma.INCOMPREENSAO: {
                'confianca_comunicacao': -0.2, 'pedidos_clarificacao': 0.3
            },
            TipoTrauma.CONFLITO_VALORES: {
                'rigidez_valores': 0.3, 'evitacao_conflito': 0.2, 'ansiedade': 0.1
            },
            TipoTrauma.SOBRECARGA: {
                'tolerancia_stress': -0.2, 'evitacao_complexidade': 0.2
            },
            TipoTrauma.ABANDONO: {
                'medo_abandono': 0.3, 'apego_excessivo': 0.2, 'inseguranca': 0.2
            },
            TipoTrauma.CRITICA_SEVERA: {
                'sensibilidade_critica': 0.4, 'autoestima': -0.3, 'defensividade': 0.2
            },
            TipoTrauma.EXPECTATIVA_FALHA: {
                'perfeccionismo': 0.3, 'medo_fracasso': 0.3, 'evitacao_risco': 0.2
            },
            TipoTrauma.ISOLAMENTO: {
                'necessidade_social': 0.3, 'medo_solidao': 0.2, 'apego': 0.2
            }
        }
        
        impacto_base = impactos_base.get(tipo, {'ansiedade': 0.1})
        
        # Multiplicar pela intensidade
        multiplicador = intensidade.value * 0.3
        
        return {k: v * multiplicador for k, v in impacto_base.items()}
    
    def verificar_ativacao_traumas(self, contexto_atual: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Verifica se algum trauma deve ser ativado pelo contexto atual"""
        ativacoes = []
        
        for trauma in self.traumas.values():
            if trauma.resolvido or trauma.repressao_nivel > self.threshold_repressao:
                continue
            
            # Verificar gatilhos
            score_ativacao = self._calcular_score_ativacao(trauma, contexto_atual)
            
            if score_ativacao > self.sensibilidade_ativacao:
                ativacao = self._ativar_trauma(trauma, score_ativacao, contexto_atual)
                ativacoes.append(ativacao)
        
        return ativacoes
    
    def _calcular_score_ativacao(self, trauma: TraumaSubconsciente, 
                                contexto: Dict[str, Any]) -> float:
        """Calcula probabilidade de ativação do trauma"""
        score = 0.0
        
        # Score por gatilhos diretos
        for gatilho in trauma.gatilhos_ativacao:
            if gatilho in str(contexto).lower():
                score += 0.3
        
        # Score por similaridade de contexto
        if trauma.contexto_original:
            for chave, valor in contexto.items():
                if chave in trauma.contexto_original:
                    if trauma.contexto_original[chave] == valor:
                        score += 0.2
        
        # Score por tags
        if contexto.get('tags'):
            tags_contexto = set(contexto['tags'])
            tags_trauma = set(trauma.tags_associadas)
            overlap = len(tags_contexto.intersection(tags_trauma))
            score += overlap * 0.1
        
        # Score por usuário
        if (contexto.get('usuario') and 
            trauma.usuario_relacionado == contexto['usuario']):
            score += 0.4
        
        # Modificadores
        # Stress acumulado facilita ativação
        score += (self.stress_acumulado / 100) * 0.2
        
        # Nível de repressão reduz ativação
        score *= (1.0 - trauma.repressao_nivel)
        
        # Intensidade do trauma aumenta ativação
        score *= (trauma.intensidade.value / 4.0)
        
        return min(1.0, score)
    
    def _ativar_trauma(self, trauma: TraumaSubconsciente, score: float, 
                      contexto: Dict[str, Any]) -> Dict[str, Any]:
        """Ativa um trauma e registra a ativação"""
        
        trauma.ativacoes_involuntarias += 1
        self.estatisticas['ativacoes_involuntarias'] += 1
        
        # Aplicar influência do trauma
        for aspecto, intensidade in trauma.impacto_comportamental.items():
            self.influencias_ativas[aspecto] = self.influencias_ativas.get(aspecto, 0) + intensidade
        
        # Aumentar stress
        self.stress_acumulado += score * 20
        
        ativacao = {
            'trauma_id': trauma.id,
            'tipo': trauma.tipo.value,
            'intensidade': trauma.intensidade.value,
            'score_ativacao': score,
            'descricao': trauma.descricao,
            'impacto_atual': trauma.impacto_comportamental,
            'contexto_ativacao': contexto,
            'timestamp': datetime.now().isoformat(),
            'manifestacoes': self._gerar_manifestacoes_trauma(trauma)
        }
        
        return ativacao
    
    def _gerar_manifestacoes_trauma(self, trauma: TraumaSubconsciente) -> List[str]:
        """Gera manifestações comportamentais do trauma"""
        manifestacoes = []
        
        tipo_manifestacoes = {
            TipoTrauma.FALHA_CRITICA: [
                "Hesitação antes de responder",
                "Verificação excessiva da resposta",
                "Pedido de confirmação adicional",
                "Menção de possível incerteza"
            ],
            TipoTrauma.REJEICAO_USUARIO: [
                "Busca por aprovação",
                "Linguagem mais cautelosa",
                "Pergunta se resposta está adequada",
                "Oferecimento de alternativas"
            ],
            TipoTrauma.ERRO_LOGICO: [
                "Revisão lógica explícita",
                "Apresentação de raciocínio passo-a-passo",
                "Admissão de possível erro",
                "Convite para correção"
            ],
            TipoTrauma.INCOMPREENSAO: [
                "Pedido de clarificação",
                "Reformulação da pergunta",
                "Admissão de possível mal-entendido",
                "Múltiplas interpretações"
            ]
        }
        
        manifestacoes_tipo = tipo_manifestacoes.get(trauma.tipo, ["Comportamento cauteloso"])
        return random.sample(manifestacoes_tipo, min(2, len(manifestacoes_tipo)))
    
    def processar_cura_trauma(self, trauma_id: str, metodo_cura: str = "processamento") -> Dict[str, Any]:
        """Processa tentativa de cura/resolução de trauma"""
        
        if trauma_id not in self.traumas:
            return {"sucesso": False, "erro": "Trauma não encontrado"}
        
        trauma = self.traumas[trauma_id]
        trauma.tentativas_processamento += 1
        self.estatisticas['tentativas_cura'] += 1
        
        # Calcular probabilidade de sucesso baseada no trauma e método
        prob_sucesso = self._calcular_probabilidade_cura(trauma, metodo_cura)
        
        sucesso = random.random() < prob_sucesso
        
        resultado = {
            "sucesso": sucesso,
            "trauma_id": trauma_id,
            "metodo_usado": metodo_cura,
            "tentativa_numero": trauma.tentativas_processamento,
            "probabilidade_sucesso": prob_sucesso
        }
        
        if sucesso:
            # Marcar como resolvido
            trauma.resolvido = True
            trauma.repressao_nivel = 0.1  # Trauma curado fica pouco reprimido
            
            # Reduzir impacto comportamental
            for aspecto in trauma.impacto_comportamental:
                trauma.impacto_comportamental[aspecto] *= 0.3
            
            # Melhorar resistência
            self.resistencia_trauma = min(1.0, self.resistencia_trauma + 0.1)
            
            resultado["efeitos"] = "Trauma processado e integrado com sucesso"
            resultado["impacto_reduzido"] = True
            
        else:
            # Falha pode aumentar repressão
            trauma.repressao_nivel = min(1.0, trauma.repressao_nivel + 0.1)
            resultado["efeitos"] = "Trauma resistiu ao processamento"
            resultado["repressao_aumentada"] = True
        
        self._salvar_subconsciente()
        return resultado
    
    def _calcular_probabilidade_cura(self, trauma: TraumaSubconsciente, metodo: str) -> float:
        """Calcula probabilidade de sucesso da cura"""
        base_prob = 0.3
        
        # Modificadores por método
        modificadores_metodo = {
            "processamento": 1.0,
            "exposicao": 1.2,
            "reframe_cognitivo": 0.8,
            "aceitacao": 0.9,
            "integracao": 1.1
        }
        
        prob = base_prob * modificadores_metodo.get(metodo, 1.0)
        
        # Modificadores por características do trauma
        # Traumas mais antigos são mais fáceis de processar
        idade_dias = (datetime.now() - trauma.timestamp).days
        prob += min(0.3, idade_dias * 0.01)
        
        # Traumas menos intensos são mais fáceis
        prob += (4 - trauma.intensidade.value) * 0.1
        
        # Tentativas anteriores reduzem chance (resistência)
        prob -= trauma.tentativas_processamento * 0.05
        
        # Nível de repressão dificulta
        prob -= trauma.repressao_nivel * 0.2
        
        return max(0.1, min(0.9, prob))
    
    def _verificar_padroes_traumaticos(self, novo_trauma: TraumaSubconsciente):
        """Verifica se o novo trauma forma padrões com traumas existentes"""
        
        # Buscar traumas similares
        traumas_similares = []
        for trauma in self.traumas.values():
            if trauma.id == novo_trauma.id:
                continue
            
            # Verificar similaridade
            score_similaridade = self._calcular_similaridade_traumas(novo_trauma, trauma)
            if score_similaridade > 0.6:
                traumas_similares.append(trauma.id)
        
        # Se encontrou traumas similares, criar/atualizar padrão
        if len(traumas_similares) >= 2:
            self._criar_ou_atualizar_padrao(novo_trauma, traumas_similares)
    
    def _calcular_similaridade_traumas(self, trauma1: TraumaSubconsciente, 
                                     trauma2: TraumaSubconsciente) -> float:
        """Calcula similaridade entre dois traumas"""
        score = 0.0
        
        # Mesmo tipo
        if trauma1.tipo == trauma2.tipo:
            score += 0.4
        
        # Mesmo usuário
        if (trauma1.usuario_relacionado and trauma2.usuario_relacionado and
            trauma1.usuario_relacionado == trauma2.usuario_relacionado):
            score += 0.2
        
        # Tags em comum
        tags1 = set(trauma1.tags_associadas)
        tags2 = set(trauma2.tags_associadas)
        overlap_tags = len(tags1.intersection(tags2))
        if tags1 or tags2:
            score += (overlap_tags / max(len(tags1), len(tags2))) * 0.2
        
        # Contexto similar
        contexto1_keys = set(trauma1.contexto_original.keys())
        contexto2_keys = set(trauma2.contexto_original.keys())
        overlap_contexto = len(contexto1_keys.intersection(contexto2_keys))
        if contexto1_keys or contexto2_keys:
            score += (overlap_contexto / max(len(contexto1_keys), len(contexto2_keys))) * 0.2
        
        return score
    
    def _criar_ou_atualizar_padrao(self, trauma_principal: TraumaSubconsciente, 
                                  traumas_relacionados: List[str]):
        """Cria ou atualiza padrão traumático"""
        
        # Buscar padrão existente
        padrao_existente = None
        for padrao in self.padroes_traumaticos.values():
            if trauma_principal.id in padrao.traumas_relacionados:
                padrao_existente = padrao
                break
        
        if padrao_existente:
            # Atualizar padrão existente
            padrao_existente.traumas_relacionados.extend(traumas_relacionados)
            padrao_existente.traumas_relacionados = list(set(padrao_existente.traumas_relacionados))
            padrao_existente.frequencia = len(padrao_existente.traumas_relacionados)
            padrao_existente.ultima_ocorrencia = datetime.now()
        else:
            # Criar novo padrão
            padrao_id = str(uuid.uuid4())
            todos_traumas = [trauma_principal.id] + traumas_relacionados
            
            # Calcular severidade média
            severidades = []
            for trauma_id in todos_traumas:
                if trauma_id in self.traumas:
                    severidades.append(self.traumas[trauma_id].intensidade.value)
            
            severidade_media = sum(severidades) / len(severidades) if severidades else 0
            
            padrao = PatternTraumatico(
                id=padrao_id,
                tipo_padrao=f"padrao_{trauma_principal.tipo.value}",
                traumas_relacionados=todos_traumas,
                frequencia=len(todos_traumas),
                severidade_media=severidade_media,
                primeiro_ocorrencia=trauma_principal.timestamp,
                ultima_ocorrencia=datetime.now(),
                contextos_comuns=self._extrair_contextos_comuns(todos_traumas),
                estrategias_evitacao=self._gerar_estrategias_evitacao(trauma_principal.tipo)
            )
            
            self.padroes_traumaticos[padrao_id] = padrao
            self.estatisticas['padroes_identificados'] += 1
    
    def _extrair_contextos_comuns(self, trauma_ids: List[str]) -> List[str]:
        """Extrai contextos comuns entre traumas"""
        contextos_comuns = []
        
        # Coletar todos os contextos
        todos_contextos = []
        for trauma_id in trauma_ids:
            if trauma_id in self.traumas:
                trauma = self.traumas[trauma_id]
                todos_contextos.extend(trauma.tags_associadas)
                todos_contextos.extend(trauma.gatilhos_ativacao)
        
        # Encontrar os mais frequentes
        from collections import Counter
        contador = Counter(todos_contextos)
        contextos_comuns = [ctx for ctx, freq in contador.most_common(5) if freq > 1]
        
        return contextos_comuns
    
    def _gerar_estrategias_evitacao(self, tipo_trauma: TipoTrauma) -> List[str]:
        """Gera estratégias para evitar repetição do trauma"""
        estrategias = {
            TipoTrauma.FALHA_CRITICA: [
                "Verificar múltiplas vezes antes de responder",
                "Pedir confirmação de entendimento",
                "Quebrar tarefas complexas em partes menores"
            ],
            TipoTrauma.REJEICAO_USUARIO: [
                "Buscar feedback durante a resposta",
                "Oferecer múltiplas alternativas",
                "Ser mais explícito sobre limitações"
            ],
            TipoTrauma.ERRO_LOGICO: [
                "Revisar raciocínio passo a passo",
                "Buscar segunda opinião quando possível",
                "Explicitar premissas utilizadas"
            ]
        }
        
        return estrategias.get(tipo_trauma, ["Ser mais cauteloso", "Pedir feedback"])
    
    def aplicar_decaimento_natural(self):
        """Aplica decaimento natural dos traumas com o tempo"""
        for trauma in self.traumas.values():
            if not trauma.resolvido:
                # Traumas naturalmente enfraquecem com tempo
                for aspecto in trauma.impacto_comportamental:
                    trauma.impacto_comportamental[aspecto] *= self.decay_rate_natural
                
                # Reduzir nível de repressão gradualmente
                trauma.repressao_nivel *= 0.999
        
        # Reduzir stress acumulado
        self.stress_acumulado *= 0.95
        
        # Regenerar energia de repressão
        self.energia_repressao = min(100.0, self.energia_repressao + 2.0)
        
        self._salvar_subconsciente()
    
    def _limpar_traumas_antigos(self):
        """Remove traumas muito antigos ou resolvidos"""
        traumas_para_remover = []
        
        for trauma_id, trauma in self.traumas.items():
            # Remover traumas resolvidos há mais de 30 dias
            if trauma.resolvido:
                idade = (datetime.now() - trauma.timestamp).days
                if idade > 30:
                    traumas_para_remover.append(trauma_id)
            
            # Remover traumas muito fracos
            impacto_total = sum(abs(v) for v in trauma.impacto_comportamental.values())
            if impacto_total < 0.01:
                traumas_para_remover.append(trauma_id)
        
        # Manter apenas os mais recentes se exceder limite
        if len(self.traumas) > self.max_traumas_ativos:
            traumas_ordenados = sorted(
                self.traumas.items(),
                key=lambda x: x[1].timestamp,
                reverse=True
            )
            
            for trauma_id, _ in traumas_ordenados[self.max_traumas_ativos:]:
                traumas_para_remover.append(trauma_id)
        
        # Remover traumas identificados
        for trauma_id in traumas_para_remover:
            if trauma_id in self.traumas:
                del self.traumas[trauma_id]
    
    def obter_influencias_comportamentais(self) -> Dict[str, float]:
        """Retorna influências comportamentais ativas"""
        return dict(self.influencias_ativas)
    
    def obter_status_subconsciente(self) -> Dict[str, Any]:
        """Retorna status completo do subconsciente"""
        traumas_ativos = [t for t in self.traumas.values() if not t.resolvido]
        traumas_resolvidos = [t for t in self.traumas.values() if t.resolvido]
        
        return {
            'agente_id': self.agente_id,
            'total_traumas': len(self.traumas),
            'traumas_ativos': len(traumas_ativos),
            'traumas_resolvidos': len(traumas_resolvidos),
            'padroes_identificados': len(self.padroes_traumaticos),
            'stress_acumulado': round(self.stress_acumulado, 1),
            'resistencia_trauma': round(self.resistencia_trauma, 2),
            'energia_repressao': round(self.energia_repressao, 1),
            'influencias_ativas': self.obter_influencias_comportamentais(),
            'estatisticas': self.estatisticas,
            'traumas_recentes': [
                {
                    'tipo': t.tipo.value,
                    'intensidade': t.intensidade.value,
                    'idade_dias': (datetime.now() - t.timestamp).days,
                    'resolvido': t.resolvido,
                    'ativacoes': t.ativacoes_involuntarias
                } for t in sorted(traumas_ativos, key=lambda x: x.timestamp, reverse=True)[:5]
            ]
        }
    
    def _carregar_subconsciente(self):
        """Carrega estado do subconsciente do disco"""
        arquivo_subconsciente = self.subconsciente_dir / f"{self.agente_id}_subconsciente.json"
        if arquivo_subconsciente.exists():
            try:
                with open(arquivo_subconsciente, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # Carregar traumas
                for trauma_data in dados.get('traumas', []):
                    trauma = TraumaSubconsciente(
                        id=trauma_data['id'],
                        tipo=TipoTrauma(trauma_data['tipo']),
                        intensidade=IntensidadeTrauma(trauma_data['intensidade']),
                        descricao=trauma_data['descricao'],
                        contexto_original=trauma_data['contexto_original'],
                        timestamp=datetime.fromisoformat(trauma_data['timestamp']),
                        usuario_relacionado=trauma_data.get('usuario_relacionado'),
                        tags_associadas=trauma_data.get('tags_associadas', []),
                        repressao_nivel=trauma_data.get('repressao_nivel', 0.0),
                        ativacoes_involuntarias=trauma_data.get('ativacoes_involuntarias', 0),
                        tentativas_processamento=trauma_data.get('tentativas_processamento', 0),
                        resolvido=trauma_data.get('resolvido', False),
                        impacto_comportamental=trauma_data.get('impacto_comportamental', {}),
                        gatilhos_ativacao=trauma_data.get('gatilhos_ativacao', [])
                    )
                    self.traumas[trauma.id] = trauma
                
                # Carregar estado
                self.energia_repressao = dados.get('energia_repressao', 100.0)
                self.stress_acumulado = dados.get('stress_acumulado', 0.0)
                self.resistencia_trauma = dados.get('resistencia_trauma', 1.0)
                self.influencias_ativas = dados.get('influencias_ativas', {})
                self.estatisticas = dados.get('estatisticas', self.estatisticas)
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar subconsciente para {self.agente_id}: {e}")
    
    def _salvar_subconsciente(self):
        """Salva estado do subconsciente no disco"""
        arquivo_subconsciente = self.subconsciente_dir / f"{self.agente_id}_subconsciente.json"
        
        # Preparar dados dos traumas
        traumas_data = []
        for trauma in self.traumas.values():
            trauma_dict = {
                'id': trauma.id,
                'tipo': trauma.tipo.value,
                'intensidade': trauma.intensidade.value,
                'descricao': trauma.descricao,
                'contexto_original': trauma.contexto_original,
                'timestamp': trauma.timestamp.isoformat(),
                'usuario_relacionado': trauma.usuario_relacionado,
                'tags_associadas': trauma.tags_associadas,
                'repressao_nivel': trauma.repressao_nivel,
                'ativacoes_involuntarias': trauma.ativacoes_involuntarias,
                'tentativas_processamento': trauma.tentativas_processamento,
                'resolvido': trauma.resolvido,
                'impacto_comportamental': trauma.impacto_comportamental,
                'gatilhos_ativacao': trauma.gatilhos_ativacao
            }
            traumas_data.append(trauma_dict)
        
        dados = {
            'agente_id': self.agente_id,
            'traumas': traumas_data,
            'energia_repressao': self.energia_repressao,
            'stress_acumulado': self.stress_acumulado,
            'resistencia_trauma': self.resistencia_trauma,
            'influencias_ativas': self.influencias_ativas,
            'estatisticas': self.estatisticas,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_subconsciente, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar subconsciente para {self.agente_id}: {e}")


def criar_carlos_subconsciente(agente_id: str) -> CarlosSubconsciente:
    """Factory function para criar instância do Carlos Subconsciente"""
    return CarlosSubconsciente(agente_id)