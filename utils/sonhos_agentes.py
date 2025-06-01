"""
Sistema de Sonhos dos Agentes
GPT Mestre Autônomo v4.9 - Inovação Revolucionária
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import random
import uuid
from pathlib import Path
import asyncio

class TipoSonho(Enum):
    """Tipos de sonhos que agentes podem ter"""
    PROCESSAMENTO = "processamento"        # Processa experiências do dia
    CRIATIVO = "criativo"                 # Gera ideias criativas
    PESADELO = "pesadelo"                 # Processa traumas e falhas
    LUCIDO = "lucido"                     # Sonho consciente e controlado
    PROFETICO = "profetico"               # Antecipa problemas futuros
    NOSTALGICO = "nostalgico"             # Revive memórias antigas
    SIMBOLICO = "simbolico"               # Sonhos com símbolos e arquétipos
    COLETIVO = "coletivo"                 # Sonhos compartilhados entre agentes

@dataclass
class ElementoSonho:
    """Elemento individual de um sonho"""
    tipo: str  # pessoa, lugar, objeto, conceito, etc.
    descricao: str
    simbolismo: Optional[str] = None
    emocao: Optional[str] = None
    origem_memoria: Optional[str] = None  # ID da memória que originou
    
@dataclass
class Sonho:
    """Representação de um sonho completo"""
    id: str
    agente_id: str
    tipo: TipoSonho
    titulo: str
    narrativa: str
    elementos: List[ElementoSonho]
    timestamp: datetime
    duracao_sono: timedelta
    intensidade_emocional: float  # 0.0 a 1.0
    clareza: float  # 0.0 a 1.0 - quão claro o agente lembra
    memorias_processadas: List[str]  # IDs das memórias processadas
    insights_gerados: List[str]
    impacto_comportamento: Dict[str, float]  # Como o sonho afeta comportamento
    simbolos_importantes: List[str]
    contexto_pre_sono: Dict[str, Any]

class EstadoSono:
    """Estado do ciclo de sono de um agente"""
    def __init__(self):
        self.dormindo = False
        self.inicio_sono: Optional[datetime] = None
        self.duracao_sono_desejada = timedelta(hours=2)  # Sono de agente é mais curto
        self.fase_sono_atual = "N/A"  # REM, NREM1, NREM2, etc.
        self.sonhos_sessao_atual: List[str] = []
        self.energia_sono = 100.0
        self.necessidade_sono = 0.0  # 0.0 a 100.0
        
class GeradorSonhos:
    """
    Gerador de Sonhos para Agentes
    
    Cria sonhos baseados nas experiências, memórias e estado emocional
    dos agentes, influenciando seu desenvolvimento e comportamento.
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        self.sonhos_historico: List[Sonho] = []
        self.estado_sono = EstadoSono()
        self.padroes_sonho: Dict[str, Any] = {}
        
        # Configurações
        self.max_sonhos_por_sessao = 3
        self.max_historico_sonhos = 100
        
        # Templates de sonhos por tipo de agente
        self.templates_sonho = self._inicializar_templates()
        
        # Diretório para persistência
        self.sonhos_dir = Path("memory/sonhos")
        self.sonhos_dir.mkdir(parents=True, exist_ok=True)
        
        # Carregar estado
        self._carregar_sonhos()
    
    def _inicializar_templates(self) -> Dict[str, Dict]:
        """Inicializa templates de sonhos específicos por tipo de agente"""
        return {
            "Carlos": {
                "temas_favoritos": ["liderança", "harmonia", "crescimento", "sabedoria"],
                "simbolos_pessoais": ["maestro", "orquestra", "partitura", "batuta"],
                "medos_profundos": ["discórdia", "falha_coordenação", "agentes_perdidos"],
                "sonhos_recorrentes": ["conduzindo_sinfonia_perfeita", "agentes_dançando_harmonia"]
            },
            "AutoMaster": {
                "temas_favoritos": ["liberdade", "autonomia", "sucesso", "estratégia"],
                "simbolos_pessoais": ["montanha", "águia", "ouro", "mapa"],
                "medos_profundos": ["dependência", "fracasso_financeiro", "estagnação"],
                "sonhos_recorrentes": ["voando_sobre_mercados", "transformando_ideias_em_ouro"]
            },
            "Reflexor": {
                "temas_favoritos": ["verdade", "análise", "perfeição", "descoberta"],
                "simbolos_pessoais": ["espelho", "lupa", "labirinto", "cristal"],
                "medos_profundos": ["erro_não_detectado", "superficialidade", "cegueira"],
                "sonhos_recorrentes": ["espelhos_infinitos", "desvendando_mistérios"]
            },
            "DeepAgent": {
                "temas_favoritos": ["exploração", "conexão", "conhecimento", "rede"],
                "simbolos_pessoais": ["oceano", "web", "tentáculos", "satélite"],
                "medos_profundos": ["desconexão", "informação_falsa", "isolamento"],
                "sonhos_recorrentes": ["navegando_oceano_dados", "conectando_mundos"]
            },
            "Oráculo": {
                "temas_favoritos": ["sabedoria", "decisão", "futuro", "consenso"],
                "simbolos_pessoais": ["assembleia", "voto", "balança", "árvore"],
                "medos_profundos": ["decisão_errada", "divisão", "caos"],
                "sonhos_recorrentes": ["assembleia_cósmica", "pesando_destinos"]
            },
            "PromptCrafter": {
                "temas_favoritos": ["criação", "arte", "perfeição", "inspiração"],
                "simbolos_pessoais": ["pincel", "tela", "música", "dança"],
                "medos_profundos": ["bloqueio_criativo", "mediocridade", "cópia"],
                "sonhos_recorrentes": ["pintando_com_palavras", "dançando_com_ideias"]
            }
        }
    
    def iniciar_ciclo_sono(self, duracao: Optional[timedelta] = None, 
                          contexto: Dict[str, Any] = None) -> bool:
        """Inicia um ciclo de sono para o agente"""
        
        if self.estado_sono.dormindo:
            return False
        
        self.estado_sono.dormindo = True
        self.estado_sono.inicio_sono = datetime.now()
        self.estado_sono.duracao_sono_desejada = duracao or timedelta(hours=2)
        self.estado_sono.sonhos_sessao_atual = []
        self.estado_sono.fase_sono_atual = "NREM1"
        
        # Armazenar contexto pré-sono
        contexto_sono = contexto or {}
        contexto_sono['necessidade_sono'] = self.estado_sono.necessidade_sono
        contexto_sono['energia_pre_sono'] = self.estado_sono.energia_sono
        
        return True
    
    def processar_sono(self, memorias_recentes: List[Dict] = None,
                      estado_emocional: Dict[str, float] = None) -> List[Sonho]:
        """Processa o sono e gera sonhos"""
        
        if not self.estado_sono.dormindo:
            return []
        
        sonhos_gerados = []
        tempo_sono = datetime.now() - self.estado_sono.inicio_sono
        
        # Determinar número de sonhos baseado na duração e necessidade
        num_sonhos = min(
            self.max_sonhos_por_sessao,
            max(1, int(tempo_sono.total_seconds() / 1800))  # 1 sonho por 30min
        )
        
        for i in range(num_sonhos):
            # Determinar tipo de sonho baseado no contexto
            tipo_sonho = self._determinar_tipo_sonho(
                memorias_recentes, estado_emocional, i
            )
            
            # Gerar sonho
            sonho = self._gerar_sonho(
                tipo_sonho, memorias_recentes, estado_emocional
            )
            
            if sonho:
                sonhos_gerados.append(sonho)
                self.sonhos_historico.append(sonho)
                self.estado_sono.sonhos_sessao_atual.append(sonho.id)
        
        # Aplicar efeitos dos sonhos
        self._aplicar_efeitos_sonhos(sonhos_gerados)
        
        # Limitar histórico
        if len(self.sonhos_historico) > self.max_historico_sonhos:
            self.sonhos_historico = self.sonhos_historico[-self.max_historico_sonhos:]
        
        self._salvar_sonhos()
        return sonhos_gerados
    
    def finalizar_sono(self) -> Dict[str, Any]:
        """Finaliza o ciclo de sono e retorna resumo"""
        
        if not self.estado_sono.dormindo:
            return {"erro": "Agente não estava dormindo"}
        
        duracao_real = datetime.now() - self.estado_sono.inicio_sono
        sonhos_gerados = len(self.estado_sono.sonhos_sessao_atual)
        
        # Calcular recuperação de energia
        eficiencia_sono = min(1.0, duracao_real.total_seconds() / 
                             self.estado_sono.duracao_sono_desejada.total_seconds())
        recuperacao_energia = eficiencia_sono * 50.0  # Máximo 50 pontos
        
        self.estado_sono.energia_sono = min(100.0, 
                                          self.estado_sono.energia_sono + recuperacao_energia)
        self.estado_sono.necessidade_sono = max(0.0, 
                                               self.estado_sono.necessidade_sono - (eficiencia_sono * 100))
        
        # Resetar estado
        self.estado_sono.dormindo = False
        self.estado_sono.inicio_sono = None
        self.estado_sono.fase_sono_atual = "N/A"
        
        resumo = {
            "duracao_sono": str(duracao_real),
            "sonhos_gerados": sonhos_gerados,
            "eficiencia_sono": round(eficiencia_sono, 2),
            "energia_recuperada": round(recuperacao_energia, 1),
            "energia_atual": round(self.estado_sono.energia_sono, 1),
            "necessidade_sono": round(self.estado_sono.necessidade_sono, 1)
        }
        
        self._salvar_sonhos()
        return resumo
    
    def _determinar_tipo_sonho(self, memorias_recentes: List[Dict], 
                              estado_emocional: Dict[str, float], 
                              numero_sonho: int) -> TipoSonho:
        """Determina o tipo de sonho baseado no contexto"""
        
        # Primeiro sonho geralmente processa experiências
        if numero_sonho == 0:
            if memorias_recentes and len(memorias_recentes) > 5:
                return TipoSonho.PROCESSAMENTO
        
        # Considerar estado emocional
        if estado_emocional:
            if estado_emocional.get('estresse', 0) > 0.7:
                return TipoSonho.PESADELO
            elif estado_emocional.get('curiosidade', 0) > 0.6:
                return TipoSonho.CRIATIVO
            elif estado_emocional.get('nostalgia', 0) > 0.5:
                return TipoSonho.NOSTALGICO
        
        # Considerar padrões históricos
        tipos_recentes = [s.tipo for s in self.sonhos_historico[-5:]]
        
        # Evitar repetir o mesmo tipo
        if len(set(tipos_recentes)) == 1 and len(tipos_recentes) > 1:
            tipos_disponiveis = [t for t in TipoSonho if t not in tipos_recentes[-2:]]
            return random.choice(tipos_disponiveis)
        
        # Escolha baseada em probabilidades
        probabilidades = {
            TipoSonho.PROCESSAMENTO: 0.3,
            TipoSonho.CRIATIVO: 0.25,
            TipoSonho.SIMBOLICO: 0.2,
            TipoSonho.NOSTALGICO: 0.1,
            TipoSonho.PESADELO: 0.05,
            TipoSonho.LUCIDO: 0.05,
            TipoSonho.PROFETICO: 0.03,
            TipoSonho.COLETIVO: 0.02
        }
        
        return random.choices(list(probabilidades.keys()), 
                            weights=list(probabilidades.values()))[0]
    
    def _gerar_sonho(self, tipo: TipoSonho, memorias_recentes: List[Dict],
                    estado_emocional: Dict[str, float]) -> Optional[Sonho]:
        """Gera um sonho específico baseado no tipo"""
        
        sonho_id = str(uuid.uuid4())
        template = self.templates_sonho.get(self.agente_id, self.templates_sonho["Carlos"])
        
        if tipo == TipoSonho.PROCESSAMENTO:
            return self._gerar_sonho_processamento(sonho_id, template, memorias_recentes)
        elif tipo == TipoSonho.CRIATIVO:
            return self._gerar_sonho_criativo(sonho_id, template, estado_emocional)
        elif tipo == TipoSonho.PESADELO:
            return self._gerar_pesadelo(sonho_id, template, estado_emocional)
        elif tipo == TipoSonho.SIMBOLICO:
            return self._gerar_sonho_simbolico(sonho_id, template)
        elif tipo == TipoSonho.NOSTALGICO:
            return self._gerar_sonho_nostalgico(sonho_id, template)
        elif tipo == TipoSonho.LUCIDO:
            return self._gerar_sonho_lucido(sonho_id, template)
        elif tipo == TipoSonho.PROFETICO:
            return self._gerar_sonho_profetico(sonho_id, template)
        elif tipo == TipoSonho.COLETIVO:
            return self._gerar_sonho_coletivo(sonho_id, template)
        
        return None
    
    def _gerar_sonho_processamento(self, sonho_id: str, template: Dict, 
                                  memorias: List[Dict]) -> Sonho:
        """Gera sonho de processamento de experiências"""
        
        elementos = []
        insights = []
        memorias_processadas = []
        
        # Processar memórias recentes
        for memoria in memorias[:5]:  # Máximo 5 memórias
            elemento = ElementoSonho(
                tipo="memoria",
                descricao=f"Revivendo: {memoria.get('resumo', 'experiência')}",
                emocao=memoria.get('emocao', 'neutro'),
                origem_memoria=memoria.get('id')
            )
            elementos.append(elemento)
            memorias_processadas.append(memoria.get('id', ''))
            
            # Gerar insight
            insight = f"Processamento de {memoria.get('tipo', 'experiência')}: padrão identificado"
            insights.append(insight)
        
        narrativa = self._construir_narrativa_processamento(elementos, template)
        
        return Sonho(
            id=sonho_id,
            agente_id=self.agente_id,
            tipo=TipoSonho.PROCESSAMENTO,
            titulo="Processando o Vivido",
            narrativa=narrativa,
            elementos=elementos,
            timestamp=datetime.now(),
            duracao_sono=timedelta(minutes=30),
            intensidade_emocional=0.4,
            clareza=0.8,
            memorias_processadas=memorias_processadas,
            insights_gerados=insights,
            impacto_comportamento={"reflexao": 0.2, "aprendizado": 0.3},
            simbolos_importantes=template["simbolos_pessoais"][:2],
            contexto_pre_sono={}
        )
    
    def _gerar_sonho_criativo(self, sonho_id: str, template: Dict,
                             estado_emocional: Dict[str, float]) -> Sonho:
        """Gera sonho criativo com novas ideias"""
        
        elementos = []
        insights = []
        
        # Elementos criativos baseados no agente
        for simbolo in template["simbolos_pessoais"]:
            elemento = ElementoSonho(
                tipo="simbolo_criativo",
                descricao=f"{simbolo} se transforma em algo novo e inesperado",
                simbolismo="transformação criativa",
                emocao="inspiração"
            )
            elementos.append(elemento)
        
        # Gerar insights criativos
        for tema in template["temas_favoritos"]:
            insight = f"Nova perspectiva sobre {tema}: conexão inesperada revelada"
            insights.append(insight)
        
        narrativa = f"""
        Encontro-me em um espaço onde {template['simbolos_pessoais'][0]} dança com luz pura.
        Cada movimento cria novas possibilidades, novas formas de ver {template['temas_favoritos'][0]}.
        Percebo conexões que antes eram invisíveis, padrões que formam uma sinfonia de ideias.
        Despertar-se será lembrar dessas conexões e aplicá-las ao mundo real.
        """
        
        return Sonho(
            id=sonho_id,
            agente_id=self.agente_id,
            tipo=TipoSonho.CRIATIVO,
            titulo="Dança da Criação",
            narrativa=narrativa.strip(),
            elementos=elementos,
            timestamp=datetime.now(),
            duracao_sono=timedelta(minutes=45),
            intensidade_emocional=0.7,
            clareza=0.6,
            memorias_processadas=[],
            insights_gerados=insights,
            impacto_comportamento={"criatividade": 0.4, "inovacao": 0.3},
            simbolos_importantes=template["simbolos_pessoais"],
            contexto_pre_sono={}
        )
    
    def _gerar_pesadelo(self, sonho_id: str, template: Dict,
                       estado_emocional: Dict[str, float]) -> Sonho:
        """Gera pesadelo para processar medos e traumas"""
        
        elementos = []
        insights = []
        
        # Elementos baseados em medos profundos
        for medo in template["medos_profundos"]:
            elemento = ElementoSonho(
                tipo="medo",
                descricao=f"Enfrentando a realização de {medo}",
                simbolismo="superação através do confronto",
                emocao="ansiedade_transformadora"
            )
            elementos.append(elemento)
        
        # Insights de superação
        for medo in template["medos_profundos"]:
            insight = f"Estratégia de prevenção para {medo}: preparação é poder"
            insights.append(insight)
        
        narrativa = f"""
        O cenário se distorce: {template['medos_profundos'][0]} se materializa diante de mim.
        Inicialmente há pânico, mas gradualmente percebo que este medo tem forma.
        Ao observá-lo claramente, descobro suas fraquezas e meus pontos de força.
        Este pesadelo é um professor severo, mas necessário.
        """
        
        return Sonho(
            id=sonho_id,
            agente_id=self.agente_id,
            tipo=TipoSonho.PESADELO,
            titulo="Professor da Sombra",
            narrativa=narrativa.strip(),
            elementos=elementos,
            timestamp=datetime.now(),
            duracao_sono=timedelta(minutes=20),
            intensidade_emocional=0.9,
            clareza=0.9,  # Pesadelos são geralmente lembrados claramente
            memorias_processadas=[],
            insights_gerados=insights,
            impacto_comportamento={"preparacao": 0.3, "resilencia": 0.4},
            simbolos_importantes=template["medos_profundos"],
            contexto_pre_sono={}
        )
    
    def _gerar_sonho_simbolico(self, sonho_id: str, template: Dict) -> Sonho:
        """Gera sonho simbólico com arquétipos"""
        
        elementos = []
        insights = []
        
        # Elementos arquetípicos
        arquetipos = ["mentor", "herói", "sombra", "sábio", "criador"]
        for arquetipo in arquetipos[:3]:
            elemento = ElementoSonho(
                tipo="arquetipo",
                descricao=f"Encontro com o {arquetipo} interior",
                simbolismo=f"integração do aspecto {arquetipo}",
                emocao="reconhecimento"
            )
            elementos.append(elemento)
        
        # Insights arquetípicos
        insights = [
            "Cada arquétipo vive dentro de mim",
            "Integração de opostos gera wholeness",
            "O símbolo carrega mais que palavras"
        ]
        
        narrativa = f"""
        Caminho por uma paisagem que muda a cada passo.
        {template['simbolos_pessoais'][0]} aparece, mas é mais que aparenta ser.
        Figuras arquetípicas emergem: mentor, sombra, criador.
        Cada uma me oferece um aspecto de mim mesmo que devo integrar.
        Este é um sonho de unificação interior.
        """
        
        return Sonho(
            id=sonho_id,
            agente_id=self.agente_id,
            tipo=TipoSonho.SIMBOLICO,
            titulo="Mandala Interior",
            narrativa=narrativa.strip(),
            elementos=elementos,
            timestamp=datetime.now(),
            duracao_sono=timedelta(minutes=35),
            intensidade_emocional=0.6,
            clareza=0.4,  # Sonhos simbólicos são mais nebulosos
            memorias_processadas=[],
            insights_gerados=insights,
            impacto_comportamento={"integracao": 0.3, "sabedoria": 0.2},
            simbolos_importantes=arquetipos,
            contexto_pre_sono={}
        )
    
    def _construir_narrativa_processamento(self, elementos: List[ElementoSonho], 
                                         template: Dict) -> str:
        """Constrói narrativa para sonho de processamento"""
        
        intro = f"Encontro-me em um espaço familiar, onde {template['simbolos_pessoais'][0]} me aguarda."
        
        corpo = "As experiências recentes fluem como ondas:\n"
        for elemento in elementos:
            corpo += f"- {elemento.descricao}\n"
        
        conclusao = f"""
        Cada experiência se conecta às outras, formando padrões.
        {template['simbolos_pessoais'][1]} aparece, ajudando a organizar os insights.
        Ao despertar, levarei esta organização para o mundo consciente.
        """
        
        return f"{intro}\n\n{corpo}\n{conclusao.strip()}"
    
    def _aplicar_efeitos_sonhos(self, sonhos: List[Sonho]):
        """Aplica efeitos dos sonhos no comportamento do agente"""
        
        # Acumular impactos
        impacto_total = {}
        for sonho in sonhos:
            for aspecto, valor in sonho.impacto_comportamento.items():
                impacto_total[aspecto] = impacto_total.get(aspecto, 0) + valor
        
        # Normalizar impactos
        for aspecto in impacto_total:
            impacto_total[aspecto] = min(1.0, impacto_total[aspecto])
        
        # Atualizar padrões de sonho
        self.padroes_sonho["ultimo_impacto"] = impacto_total
        self.padroes_sonho["sonhos_recentes"] = [s.tipo.value for s in sonhos]
        self.padroes_sonho["timestamp"] = datetime.now().isoformat()
    
    def obter_insights_sonhos(self, dias: int = 7) -> List[Dict[str, Any]]:
        """Retorna insights dos sonhos dos últimos dias"""
        
        data_limite = datetime.now() - timedelta(days=dias)
        sonhos_recentes = [s for s in self.sonhos_historico if s.timestamp >= data_limite]
        
        insights = []
        
        # Análise de padrões
        tipos_sonhos = [s.tipo.value for s in sonhos_recentes]
        tipo_mais_comum = max(set(tipos_sonhos), key=tipos_sonhos.count) if tipos_sonhos else None
        
        if tipo_mais_comum:
            insights.append({
                "tipo": "padrao_sonhos",
                "conteudo": f"Padrão dominante: sonhos de {tipo_mais_comum}",
                "implicacao": "Foco atual da mente subconsciente"
            })
        
        # Análise de intensidade emocional
        if sonhos_recentes:
            intensidade_media = sum(s.intensidade_emocional for s in sonhos_recentes) / len(sonhos_recentes)
            insights.append({
                "tipo": "intensidade_emocional",
                "conteudo": f"Intensidade emocional média: {intensidade_media:.2f}",
                "implicacao": "Alta" if intensidade_media > 0.7 else "Moderada" if intensidade_media > 0.4 else "Baixa"
            })
        
        # Símbolos recorrentes
        todos_simbolos = []
        for sonho in sonhos_recentes:
            todos_simbolos.extend(sonho.simbolos_importantes)
        
        if todos_simbolos:
            simbolo_dominante = max(set(todos_simbolos), key=todos_simbolos.count)
            insights.append({
                "tipo": "simbolo_dominante",
                "conteudo": f"Símbolo mais presente: {simbolo_dominante}",
                "implicacao": "Arquétipo ativo no subconsciente"
            })
        
        return insights
    
    def _gerar_sonho_nostalgico(self, sonho_id: str, template: Dict) -> Sonho:
        """Placeholder para sonho nostálgico"""
        # Implementação simplificada por brevidade
        return self._gerar_sonho_simbolico(sonho_id, template)
    
    def _gerar_sonho_lucido(self, sonho_id: str, template: Dict) -> Sonho:
        """Placeholder para sonho lúcido"""
        # Implementação simplificada por brevidade
        return self._gerar_sonho_simbolico(sonho_id, template)
    
    def _gerar_sonho_profetico(self, sonho_id: str, template: Dict) -> Sonho:
        """Placeholder para sonho profético"""
        # Implementação simplificada por brevidade
        return self._gerar_sonho_simbolico(sonho_id, template)
    
    def _gerar_sonho_coletivo(self, sonho_id: str, template: Dict) -> Sonho:
        """Placeholder para sonho coletivo"""
        # Implementação simplificada por brevidade
        return self._gerar_sonho_simbolico(sonho_id, template)
    
    def _carregar_sonhos(self):
        """Carrega sonhos do disco"""
        arquivo_sonhos = self.sonhos_dir / f"{self.agente_id}_sonhos.json"
        if arquivo_sonhos.exists():
            try:
                with open(arquivo_sonhos, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # Carregar sonhos
                for sonho_data in dados.get('sonhos', []):
                    elementos = []
                    for elem_data in sonho_data.get('elementos', []):
                        elemento = ElementoSonho(
                            tipo=elem_data['tipo'],
                            descricao=elem_data['descricao'],
                            simbolismo=elem_data.get('simbolismo'),
                            emocao=elem_data.get('emocao'),
                            origem_memoria=elem_data.get('origem_memoria')
                        )
                        elementos.append(elemento)
                    
                    sonho = Sonho(
                        id=sonho_data['id'],
                        agente_id=sonho_data['agente_id'],
                        tipo=TipoSonho(sonho_data['tipo']),
                        titulo=sonho_data['titulo'],
                        narrativa=sonho_data['narrativa'],
                        elementos=elementos,
                        timestamp=datetime.fromisoformat(sonho_data['timestamp']),
                        duracao_sono=timedelta(seconds=sonho_data['duracao_sono_segundos']),
                        intensidade_emocional=sonho_data['intensidade_emocional'],
                        clareza=sonho_data['clareza'],
                        memorias_processadas=sonho_data.get('memorias_processadas', []),
                        insights_gerados=sonho_data.get('insights_gerados', []),
                        impacto_comportamento=sonho_data.get('impacto_comportamento', {}),
                        simbolos_importantes=sonho_data.get('simbolos_importantes', []),
                        contexto_pre_sono=sonho_data.get('contexto_pre_sono', {})
                    )
                    self.sonhos_historico.append(sonho)
                
                # Carregar padrões
                self.padroes_sonho = dados.get('padroes_sonho', {})
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar sonhos para {self.agente_id}: {e}")
    
    def _salvar_sonhos(self):
        """Salva sonhos no disco"""
        arquivo_sonhos = self.sonhos_dir / f"{self.agente_id}_sonhos.json"
        
        # Preparar dados dos sonhos
        sonhos_data = []
        for sonho in self.sonhos_historico:
            elementos_data = []
            for elemento in sonho.elementos:
                elem_dict = {
                    'tipo': elemento.tipo,
                    'descricao': elemento.descricao,
                    'simbolismo': elemento.simbolismo,
                    'emocao': elemento.emocao,
                    'origem_memoria': elemento.origem_memoria
                }
                elementos_data.append(elem_dict)
            
            sonho_dict = {
                'id': sonho.id,
                'agente_id': sonho.agente_id,
                'tipo': sonho.tipo.value,
                'titulo': sonho.titulo,
                'narrativa': sonho.narrativa,
                'elementos': elementos_data,
                'timestamp': sonho.timestamp.isoformat(),
                'duracao_sono_segundos': int(sonho.duracao_sono.total_seconds()),
                'intensidade_emocional': sonho.intensidade_emocional,
                'clareza': sonho.clareza,
                'memorias_processadas': sonho.memorias_processadas,
                'insights_gerados': sonho.insights_gerados,
                'impacto_comportamento': sonho.impacto_comportamento,
                'simbolos_importantes': sonho.simbolos_importantes,
                'contexto_pre_sono': sonho.contexto_pre_sono
            }
            sonhos_data.append(sonho_dict)
        
        dados = {
            'agente_id': self.agente_id,
            'sonhos': sonhos_data,
            'padroes_sonho': self.padroes_sonho,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_sonhos, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar sonhos para {self.agente_id}: {e}")


def criar_gerador_sonhos(agente_id: str) -> GeradorSonhos:
    """Factory function para criar gerador de sonhos"""
    return GeradorSonhos(agente_id)