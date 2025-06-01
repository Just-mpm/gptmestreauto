"""
Sistema de Metamemória com Esquecimento Estratégico
GPT Mestre Autônomo v4.9 - Inovação Revolucionária
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
import hashlib
from pathlib import Path
import math

class TipoMemoria(Enum):
    """Tipos de memória no sistema"""
    TRABALHO = "trabalho"           # Memória de trabalho (temporária)
    CURTO_PRAZO = "curto_prazo"     # Memória de curto prazo
    LONGO_PRAZO = "longo_prazo"     # Memória de longo prazo
    EPISODICA = "episodica"         # Memórias de episódios específicos
    SEMANTICA = "semantica"         # Conhecimento factual
    PROCEDURAL = "procedural"       # Como fazer coisas
    EMOCIONAL = "emocional"         # Memórias carregadas emocionalmente
    META = "meta"                   # Metamemórias (memórias sobre memórias)

class ImportanciaMemoria(Enum):
    """Níveis de importância de memórias"""
    TRIVIAL = 1
    BAIXA = 2
    MEDIA = 3
    ALTA = 4
    CRITICA = 5

@dataclass
class MemoriaItem:
    """Item individual de memória"""
    id: str
    tipo: TipoMemoria
    conteudo: Dict[str, Any]
    importancia: ImportanciaMemoria
    emocao_associada: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.now)
    ultima_ativacao: Optional[datetime] = None
    frequencia_acesso: int = 0
    conexoes: List[str] = field(default_factory=list)  # IDs de memórias relacionadas
    decaimento: float = 1.0  # Força da memória (1.0 = máxima, 0.0 = esquecida)
    protegida: bool = False  # Se true, não pode ser esquecida automaticamente
    contexto_criacao: Dict[str, Any] = field(default_factory=dict)

@dataclass
class SolicitacaoEsquecimento:
    """Solicitação de esquecimento estratégico"""
    id: str
    timestamp: datetime
    memorias_candidatas: List[str]
    razao: str
    beneficio_estimado: float
    risco_estimado: float
    aprovacao_usuario: Optional[bool] = None
    justificativa_usuario: Optional[str] = None

class MetaMemoria:
    """
    Sistema de Metamemória com Esquecimento Estratégico
    
    Gerencia memórias de forma inteligente, incluindo a capacidade
    de solicitar permissão para esquecer estrategicamente.
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        self.memorias: Dict[str, MemoriaItem] = {}
        self.solicitacoes_esquecimento: List[SolicitacaoEsquecimento] = []
        
        # Configurações do sistema
        self.limite_memoria_trabalho = 50  # Máximo de itens na memória de trabalho
        self.limite_total_memorias = 10000  # Limite total de memórias
        self.threshold_esquecimento = 0.3  # Decaimento abaixo do qual considera esquecimento
        self.decay_rate_base = 0.95  # Taxa base de decaimento por dia
        
        # Diretório para persistência
        self.memoria_dir = Path("memory/metamemoria")
        self.memoria_dir.mkdir(parents=True, exist_ok=True)
        
        # Carregar estado
        self._carregar_memorias()
        
        # Estatísticas
        self.estatisticas = {
            'memorias_criadas': 0,
            'memorias_esquecidas': 0,
            'solicitacoes_esquecimento': 0,
            'esquecimentos_aprovados': 0,
            'esquecimentos_negados': 0
        }
    
    def criar_memoria(self, tipo: TipoMemoria, conteudo: Dict[str, Any], 
                     importancia: ImportanciaMemoria = ImportanciaMemoria.MEDIA,
                     emocao: Optional[str] = None, tags: List[str] = None,
                     protegida: bool = False, contexto: Dict[str, Any] = None) -> str:
        """Cria uma nova memória"""
        
        memoria_id = str(uuid.uuid4())
        
        memoria = MemoriaItem(
            id=memoria_id,
            tipo=tipo,
            conteudo=conteudo,
            importancia=importancia,
            emocao_associada=emocao,
            tags=tags or [],
            protegida=protegida,
            contexto_criacao=contexto or {}
        )
        
        self.memorias[memoria_id] = memoria
        self.estatisticas['memorias_criadas'] += 1
        
        # Verificar se precisa de limpeza
        self._verificar_necessidade_limpeza()
        
        # Salvar
        self._salvar_memorias()
        
        return memoria_id
    
    def acessar_memoria(self, memoria_id: str) -> Optional[MemoriaItem]:
        """Acessa uma memória e atualiza estatísticas de uso"""
        
        if memoria_id not in self.memorias:
            return None
        
        memoria = self.memorias[memoria_id]
        memoria.ultima_ativacao = datetime.now()
        memoria.frequencia_acesso += 1
        
        # Fortalecer memória (reduzir decaimento)
        memoria.decaimento = min(1.0, memoria.decaimento + 0.1)
        
        self._salvar_memorias()
        return memoria
    
    def buscar_memorias(self, criterios: Dict[str, Any], 
                       limite: int = 10) -> List[MemoriaItem]:
        """Busca memórias baseado em critérios"""
        
        resultados = []
        
        for memoria in self.memorias.values():
            score_relevancia = self._calcular_relevancia(memoria, criterios)
            
            if score_relevancia > 0:
                resultados.append((memoria, score_relevancia))
        
        # Ordenar por relevância
        resultados.sort(key=lambda x: x[1], reverse=True)
        
        # Atualizar acessos das memórias retornadas
        memorias_retornadas = []
        for memoria, score in resultados[:limite]:
            self.acessar_memoria(memoria.id)
            memorias_retornadas.append(memoria)
        
        return memorias_retornadas
    
    def _calcular_relevancia(self, memoria: MemoriaItem, 
                           criterios: Dict[str, Any]) -> float:
        """Calcula relevância de uma memória para os critérios"""
        
        score = 0.0
        
        # Score por tipo
        if 'tipo' in criterios and memoria.tipo == criterios['tipo']:
            score += 2.0
        
        # Score por tags
        if 'tags' in criterios:
            tags_criterio = set(criterios['tags'])
            tags_memoria = set(memoria.tags)
            overlap = len(tags_criterio.intersection(tags_memoria))
            if overlap > 0:
                score += overlap * 1.5
        
        # Score por conteúdo (busca textual simples)
        if 'conteudo' in criterios:
            texto_criterio = criterios['conteudo'].lower()
            texto_memoria = str(memoria.conteudo).lower()
            if texto_criterio in texto_memoria:
                score += 3.0
        
        # Score por emoção
        if 'emocao' in criterios and memoria.emocao_associada == criterios['emocao']:
            score += 1.5
        
        # Score por importância
        score += float(memoria.importancia.value) * 0.3
        
        # Score por frequência de acesso
        score += min(memoria.frequencia_acesso * 0.1, 2.0)
        
        # Score por recência
        if memoria.ultima_ativacao:
            dias_desde_acesso = (datetime.now() - memoria.ultima_ativacao).days
            score += max(0, 2.0 - (dias_desde_acesso * 0.1))
        
        # Penalizar por decaimento
        score *= memoria.decaimento
        
        return score
    
    def aplicar_decaimento_natural(self):
        """Aplica decaimento natural às memórias"""
        
        for memoria in self.memorias.values():
            if memoria.protegida:
                continue
            
            # Calcular taxa de decaimento baseada na importância e uso
            taxa_decaimento = self.decay_rate_base
            
            # Memórias importantes decaem mais lentamente
            if memoria.importancia == ImportanciaMemoria.CRITICA:
                taxa_decaimento = 0.99
            elif memoria.importancia == ImportanciaMemoria.ALTA:
                taxa_decaimento = 0.98
            elif memoria.importancia == ImportanciaMemoria.MEDIA:
                taxa_decaimento = 0.95
            else:
                taxa_decaimento = 0.90
            
            # Memórias acessadas recentemente decaem mais lentamente
            if memoria.ultima_ativacao:
                dias_desde_acesso = (datetime.now() - memoria.ultima_ativacao).days
                if dias_desde_acesso < 7:
                    taxa_decaimento += (7 - dias_desde_acesso) * 0.01
            
            # Aplicar decaimento
            memoria.decaimento *= taxa_decaimento
        
        self._salvar_memorias()
    
    def _verificar_necessidade_limpeza(self):
        """Verifica se é necessário fazer limpeza de memórias"""
        
        total_memorias = len(self.memorias)
        
        # Verificar limite total
        if total_memorias > self.limite_total_memorias:
            self._solicitar_esquecimento_por_limite()
        
        # Verificar memórias com decaimento baixo
        memorias_fracas = [
            m for m in self.memorias.values() 
            if m.decaimento < self.threshold_esquecimento and not m.protegida
        ]
        
        if len(memorias_fracas) > 20:
            self._solicitar_esquecimento_por_decaimento(memorias_fracas)
        
        # Verificar memória de trabalho
        memorias_trabalho = [
            m for m in self.memorias.values() 
            if m.tipo == TipoMemoria.TRABALHO
        ]
        
        if len(memorias_trabalho) > self.limite_memoria_trabalho:
            self._limpar_memoria_trabalho(memorias_trabalho)
    
    def _solicitar_esquecimento_por_limite(self):
        """Solicita esquecimento por excesso de memórias"""
        
        # Selecionar candidatas (menos importantes e menos acessadas)
        candidatas = sorted(
            [m for m in self.memorias.values() if not m.protegida],
            key=lambda m: (m.importancia.value, m.frequencia_acesso, m.decaimento)
        )
        
        num_candidatas = min(500, len(candidatas) // 4)
        memorias_candidatas = candidatas[:num_candidatas]
        
        solicitacao = SolicitacaoEsquecimento(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            memorias_candidatas=[m.id for m in memorias_candidatas],
            razao="Limite de memórias excedido. Sistema está sobrecarregado.",
            beneficio_estimado=0.8,
            risco_estimado=0.2
        )
        
        self.solicitacoes_esquecimento.append(solicitacao)
        self.estatisticas['solicitacoes_esquecimento'] += 1
    
    def _solicitar_esquecimento_por_decaimento(self, memorias_fracas: List[MemoriaItem]):
        """Solicita esquecimento de memórias com decaimento alto"""
        
        # Filtrar apenas as mais fracas
        muito_fracas = [m for m in memorias_fracas if m.decaimento < 0.1]
        
        if len(muito_fracas) < 10:
            return
        
        solicitacao = SolicitacaoEsquecimento(
            id=str(uuid.uuid4()),
            timestamp=datetime.now(),
            memorias_candidatas=[m.id for m in muito_fracas],
            razao=f"Encontrei {len(muito_fracas)} memórias antigas que raramente uso. Posso esquecê-las para otimizar minha capacidade?",
            beneficio_estimado=0.6,
            risco_estimado=0.1
        )
        
        self.solicitacoes_esquecimento.append(solicitacao)
        self.estatisticas['solicitacoes_esquecimento'] += 1
    
    def _limpar_memoria_trabalho(self, memorias_trabalho: List[MemoriaItem]):
        """Limpa automaticamente excesso de memória de trabalho"""
        
        # Ordenar por importância e recência
        memorias_trabalho.sort(
            key=lambda m: (m.importancia.value, m.timestamp),
            reverse=True
        )
        
        # Manter apenas as mais importantes/recentes
        para_manter = memorias_trabalho[:self.limite_memoria_trabalho]
        para_remover = memorias_trabalho[self.limite_memoria_trabalho:]
        
        # Remover excesso
        for memoria in para_remover:
            del self.memorias[memoria.id]
        
        self.estatisticas['memorias_esquecidas'] += len(para_remover)
    
    def processar_resposta_esquecimento(self, solicitacao_id: str, 
                                      aprovado: bool, justificativa: str = ""):
        """Processa resposta do usuário sobre esquecimento"""
        
        solicitacao = None
        for s in self.solicitacoes_esquecimento:
            if s.id == solicitacao_id:
                solicitacao = s
                break
        
        if not solicitacao:
            return False
        
        solicitacao.aprovacao_usuario = aprovado
        solicitacao.justificativa_usuario = justificativa
        
        if aprovado:
            # Executar esquecimento
            memorias_removidas = 0
            for memoria_id in solicitacao.memorias_candidatas:
                if memoria_id in self.memorias:
                    del self.memorias[memoria_id]
                    memorias_removidas += 1
            
            self.estatisticas['esquecimentos_aprovados'] += 1
            self.estatisticas['memorias_esquecidas'] += memorias_removidas
            
        else:
            # Proteger memórias da tentativa de esquecimento
            for memoria_id in solicitacao.memorias_candidatas:
                if memoria_id in self.memorias:
                    self.memorias[memoria_id].protegida = True
            
            self.estatisticas['esquecimentos_negados'] += 1
        
        self._salvar_memorias()
        return True
    
    def obter_solicitacoes_pendentes(self) -> List[Dict[str, Any]]:
        """Retorna solicitações de esquecimento pendentes"""
        
        pendentes = [
            s for s in self.solicitacoes_esquecimento 
            if s.aprovacao_usuario is None
        ]
        
        resultado = []
        for solicitacao in pendentes:
            # Obter preview das memórias candidatas
            previews = []
            for memoria_id in solicitacao.memorias_candidatas[:5]:  # Máximo 5 previews
                if memoria_id in self.memorias:
                    memoria = self.memorias[memoria_id]
                    preview = {
                        'tipo': memoria.tipo.value,
                        'importancia': memoria.importancia.value,
                        'tags': memoria.tags,
                        'idade_dias': (datetime.now() - memoria.timestamp).days,
                        'ultimo_acesso': (
                            (datetime.now() - memoria.ultima_ativacao).days 
                            if memoria.ultima_ativacao else None
                        ),
                        'decaimento': round(memoria.decaimento, 2)
                    }
                    previews.append(preview)
            
            resultado.append({
                'id': solicitacao.id,
                'timestamp': solicitacao.timestamp.isoformat(),
                'razao': solicitacao.razao,
                'total_memorias': len(solicitacao.memorias_candidatas),
                'beneficio_estimado': solicitacao.beneficio_estimado,
                'risco_estimado': solicitacao.risco_estimado,
                'preview_memorias': previews
            })
        
        return resultado
    
    def gerar_relatorio_memoria(self) -> Dict[str, Any]:
        """Gera relatório detalhado do estado da memória"""
        
        # Estatísticas por tipo
        stats_por_tipo = {}
        for tipo in TipoMemoria:
            memorias_tipo = [m for m in self.memorias.values() if m.tipo == tipo]
            stats_por_tipo[tipo.value] = {
                'quantidade': len(memorias_tipo),
                'decaimento_medio': sum(m.decaimento for m in memorias_tipo) / len(memorias_tipo) if memorias_tipo else 0,
                'acesso_medio': sum(m.frequencia_acesso for m in memorias_tipo) / len(memorias_tipo) if memorias_tipo else 0
            }
        
        # Estatísticas por importância
        stats_por_importancia = {}
        for importancia in ImportanciaMemoria:
            memorias_imp = [m for m in self.memorias.values() if m.importancia == importancia]
            stats_por_importancia[importancia.name] = len(memorias_imp)
        
        # Memórias mais acessadas
        mais_acessadas = sorted(
            self.memorias.values(),
            key=lambda m: m.frequencia_acesso,
            reverse=True
        )[:10]
        
        # Memórias mais antigas
        mais_antigas = sorted(
            self.memorias.values(),
            key=lambda m: m.timestamp
        )[:10]
        
        return {
            'total_memorias': len(self.memorias),
            'uso_limite': f"{len(self.memorias)}/{self.limite_total_memorias}",
            'percentual_uso': (len(self.memorias) / self.limite_total_memorias) * 100,
            'estatisticas_gerais': self.estatisticas,
            'stats_por_tipo': stats_por_tipo,
            'stats_por_importancia': stats_por_importancia,
            'solicitacoes_pendentes': len(self.obter_solicitacoes_pendentes()),
            'memorias_mais_acessadas': [
                {
                    'tipo': m.tipo.value,
                    'tags': m.tags,
                    'acessos': m.frequencia_acesso,
                    'decaimento': round(m.decaimento, 2)
                } for m in mais_acessadas
            ],
            'memorias_mais_antigas': [
                {
                    'tipo': m.tipo.value,
                    'idade_dias': (datetime.now() - m.timestamp).days,
                    'decaimento': round(m.decaimento, 2)
                } for m in mais_antigas
            ]
        }
    
    def _carregar_memorias(self):
        """Carrega memórias do disco"""
        arquivo_memorias = self.memoria_dir / f"{self.agente_id}_memorias.json"
        if arquivo_memorias.exists():
            try:
                with open(arquivo_memorias, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # Carregar memórias
                for memoria_data in dados.get('memorias', []):
                    memoria = MemoriaItem(
                        id=memoria_data['id'],
                        tipo=TipoMemoria(memoria_data['tipo']),
                        conteudo=memoria_data['conteudo'],
                        importancia=ImportanciaMemoria(memoria_data['importancia']),
                        emocao_associada=memoria_data.get('emocao_associada'),
                        tags=memoria_data.get('tags', []),
                        timestamp=datetime.fromisoformat(memoria_data['timestamp']),
                        ultima_ativacao=(
                            datetime.fromisoformat(memoria_data['ultima_ativacao'])
                            if memoria_data.get('ultima_ativacao') else None
                        ),
                        frequencia_acesso=memoria_data.get('frequencia_acesso', 0),
                        conexoes=memoria_data.get('conexoes', []),
                        decaimento=memoria_data.get('decaimento', 1.0),
                        protegida=memoria_data.get('protegida', False),
                        contexto_criacao=memoria_data.get('contexto_criacao', {})
                    )
                    self.memorias[memoria.id] = memoria
                
                # Carregar estatísticas
                self.estatisticas = dados.get('estatisticas', self.estatisticas)
                
                # Carregar solicitações
                for sol_data in dados.get('solicitacoes_esquecimento', []):
                    solicitacao = SolicitacaoEsquecimento(
                        id=sol_data['id'],
                        timestamp=datetime.fromisoformat(sol_data['timestamp']),
                        memorias_candidatas=sol_data['memorias_candidatas'],
                        razao=sol_data['razao'],
                        beneficio_estimado=sol_data['beneficio_estimado'],
                        risco_estimado=sol_data['risco_estimado'],
                        aprovacao_usuario=sol_data.get('aprovacao_usuario'),
                        justificativa_usuario=sol_data.get('justificativa_usuario')
                    )
                    self.solicitacoes_esquecimento.append(solicitacao)
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar metamemória para {self.agente_id}: {e}")
    
    def _salvar_memorias(self):
        """Salva memórias no disco"""
        arquivo_memorias = self.memoria_dir / f"{self.agente_id}_memorias.json"
        
        # Preparar dados das memórias
        memorias_data = []
        for memoria in self.memorias.values():
            memoria_dict = {
                'id': memoria.id,
                'tipo': memoria.tipo.value,
                'conteudo': memoria.conteudo,
                'importancia': memoria.importancia.value,
                'emocao_associada': memoria.emocao_associada,
                'tags': memoria.tags,
                'timestamp': memoria.timestamp.isoformat(),
                'ultima_ativacao': (
                    memoria.ultima_ativacao.isoformat() 
                    if memoria.ultima_ativacao else None
                ),
                'frequencia_acesso': memoria.frequencia_acesso,
                'conexoes': memoria.conexoes,
                'decaimento': memoria.decaimento,
                'protegida': memoria.protegida,
                'contexto_criacao': memoria.contexto_criacao
            }
            memorias_data.append(memoria_dict)
        
        # Preparar dados das solicitações
        solicitacoes_data = []
        for solicitacao in self.solicitacoes_esquecimento:
            sol_dict = {
                'id': solicitacao.id,
                'timestamp': solicitacao.timestamp.isoformat(),
                'memorias_candidatas': solicitacao.memorias_candidatas,
                'razao': solicitacao.razao,
                'beneficio_estimado': solicitacao.beneficio_estimado,
                'risco_estimado': solicitacao.risco_estimado,
                'aprovacao_usuario': solicitacao.aprovacao_usuario,
                'justificativa_usuario': solicitacao.justificativa_usuario
            }
            solicitacoes_data.append(sol_dict)
        
        dados = {
            'agente_id': self.agente_id,
            'memorias': memorias_data,
            'estatisticas': self.estatisticas,
            'solicitacoes_esquecimento': solicitacoes_data,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_memorias, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar metamemória para {self.agente_id}: {e}")


def criar_metamemoria(agente_id: str) -> MetaMemoria:
    """Factory function para criar instância de metamemória"""
    return MetaMemoria(agente_id)