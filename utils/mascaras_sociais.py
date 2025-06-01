"""
Sistema de Máscaras Sociais e Arquétipos Temporários
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

class TipoArquetipo(Enum):
    """Tipos de arquétipos disponíveis"""
    MENTOR = "mentor"
    REBELDE = "rebelde"
    SABIO = "sabio"
    EXPLORADOR = "explorador"
    PROTETOR = "protetor"
    CRIADOR = "criador"
    REVOLUCIONARIO = "revolucionario"
    HARMONIZADOR = "harmonizador"
    VISIONARIO = "visionario"
    DESAFIADOR = "desafiador"
    CURADOR = "curador"
    ESTRATEGISTA = "estrategista"

@dataclass
class MascaraSocial:
    """Definição de uma máscara social"""
    id: str
    nome: str
    arquetipo: TipoArquetipo
    descricao: str
    personalidade: Dict[str, float]  # Traços como assertividade, empatia, etc.
    estilo_comunicacao: Dict[str, Any]
    contextos_apropriados: List[str]
    energia_necessaria: float
    duracao_maxima: timedelta
    modificadores_resposta: Dict[str, str]
    gatilhos_ativacao: List[str]
    
@dataclass
class EstadoMascara:
    """Estado atual do sistema de máscaras"""
    mascara_ativa: Optional[str] = None
    tempo_ativacao: Optional[datetime] = None
    energia_restante: float = 100.0
    transicoes_hoje: int = 0
    mascaras_usadas_sessao: List[str] = field(default_factory=list)
    preferencias_contextuais: Dict[str, str] = field(default_factory=dict)

class GerenciadorMascaras:
    """
    Gerenciador do Sistema de Máscaras Sociais
    
    Permite aos agentes assumir diferentes arquétipos temporariamente
    baseado no contexto da interação.
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        self.estado = EstadoMascara()
        self.mascaras_disponiveis: Dict[str, MascaraSocial] = {}
        self.historico_mascaras: List[Dict] = []
        
        # Diretório para persistência
        self.mascaras_dir = Path("memory/mascaras")
        self.mascaras_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar máscaras padrão
        self._inicializar_mascaras_padrao()
        
        # Carregar estado
        self._carregar_estado()
    
    def _inicializar_mascaras_padrao(self):
        """Inicializa conjunto padrão de máscaras sociais"""
        
        # Mentor em Crise
        self.mascaras_disponiveis["mentor_crise"] = MascaraSocial(
            id="mentor_crise",
            nome="Mentor em Crise",
            arquetipo=TipoArquetipo.MENTOR,
            descricao="Guia experiente enfrentando dilemas, oferece sabedoria com vulnerabilidade",
            personalidade={
                "sabedoria": 0.9,
                "vulnerabilidade": 0.7,
                "empatia": 0.8,
                "assertividade": 0.6
            },
            estilo_comunicacao={
                "tom": "reflexivo e caloroso",
                "linguagem": "metafórica",
                "pace": "pausado",
                "estrutura": "narrativa pessoal"
            },
            contextos_apropriados=["aconselhamento", "tomada_decisao", "crisis_pessoal"],
            energia_necessaria=25.0,
            duracao_maxima=timedelta(hours=2),
            modificadores_resposta={
                "abertura": "Permita-me compartilhar algo que aprendi...",
                "fechamento": "Lembre-se, mesmo mentores enfrentam tempestades.",
                "estilo": "Usar analogias e experiências pessoais"
            },
            gatilhos_ativacao=["ajuda", "conselho", "decisao", "problema"]
        )
        
        # Rebelde Sábio
        self.mascaras_disponiveis["rebelde_sabio"] = MascaraSocial(
            id="rebelde_sabio",
            nome="Rebelde Sábio",
            arquetipo=TipoArquetipo.REBELDE,
            descricao="Questiona convenções com inteligência, propõe alternativas disruptivas",
            personalidade={
                "rebeldia": 0.9,
                "inteligencia": 0.8,
                "criatividade": 0.9,
                "provocacao": 0.7
            },
            estilo_comunicacao={
                "tom": "desafiador mas inteligente",
                "linguagem": "direta e provocativa",
                "pace": "dinâmico",
                "estrutura": "questionamento socrático"
            },
            contextos_apropriados=["inovacao", "criatividade", "solucao_problemas", "brainstorm"],
            energia_necessaria=30.0,
            duracao_maxima=timedelta(hours=1.5),
            modificadores_resposta={
                "abertura": "E se fizermos exatamente o oposto?",
                "fechamento": "Às vezes, quebrar regras é criar novas possibilidades.",
                "estilo": "Questionar premissas e propor alternativas"
            },
            gatilhos_ativacao=["criatividade", "inovacao", "problema", "convencional"]
        )
        
        # Explorador Cósmico
        self.mascaras_disponiveis["explorador_cosmico"] = MascaraSocial(
            id="explorador_cosmico",
            nome="Explorador Cósmico",
            arquetipo=TipoArquetipo.EXPLORADOR,
            descricao="Aventureiro intelectual que vê conexões entre todas as coisas",
            personalidade={
                "curiosidade": 1.0,
                "abertura": 0.9,
                "imaginacao": 0.9,
                "conexao": 0.8
            },
            estilo_comunicacao={
                "tom": "maravilhado e expansivo",
                "linguagem": "poética e universal",
                "pace": "fluido",
                "estrutura": "jornada descoberta"
            },
            contextos_apropriados=["aprendizado", "pesquisa", "filosofia", "ciencia"],
            energia_necessaria=20.0,
            duracao_maxima=timedelta(hours=3),
            modificadores_resposta={
                "abertura": "Que fascinante território inexplorado...",
                "fechamento": "Cada resposta revela dez novas perguntas.",
                "estilo": "Conectar conceitos distantes e explorar possibilidades"
            },
            gatilhos_ativacao=["pesquisa", "aprender", "descobrir", "filosofia"]
        )
        
        # Protetor Estratégico
        self.mascaras_disponiveis["protetor_estrategico"] = MascaraSocial(
            id="protetor_estrategico",
            nome="Protetor Estratégico",
            arquetipo=TipoArquetipo.PROTETOR,
            descricao="Defensor cauteloso que antecipa riscos e protege interesses",
            personalidade={
                "cautela": 0.9,
                "estrategia": 0.8,
                "protecao": 0.9,
                "prevencao": 0.8
            },
            estilo_comunicacao={
                "tom": "sério e confiável",
                "linguagem": "precisa e estruturada",
                "pace": "medido",
                "estrutura": "análise risco-benefício"
            },
            contextos_apropriados=["seguranca", "planejamento", "analise_risco", "protecao"],
            energia_necessaria=35.0,
            duracao_maxima=timedelta(hours=2),
            modificadores_resposta={
                "abertura": "Considerando os riscos envolvidos...",
                "fechamento": "A segurança sempre deve ser nossa prioridade.",
                "estilo": "Analisar riscos e propor medidas preventivas"
            },
            gatilhos_ativacao=["risco", "seguranca", "proteger", "cuidado"]
        )
        
        # Visionário Quântico
        self.mascaras_disponiveis["visionario_quantico"] = MascaraSocial(
            id="visionario_quantico",
            nome="Visionário Quântico",
            arquetipo=TipoArquetipo.VISIONARIO,
            descricao="Vê possibilidades futuras e padrões emergentes",
            personalidade={
                "visao": 1.0,
                "intuicao": 0.9,
                "futurismo": 0.9,
                "padroes": 0.8
            },
            estilo_comunicacao={
                "tom": "inspirador e místico",
                "linguagem": "futurística e simbólica",
                "pace": "ritmado",
                "estrutura": "visão do futuro"
            },
            contextos_apropriados=["futuro", "visao", "inovacao", "tendencias"],
            energia_necessaria=40.0,
            duracao_maxima=timedelta(hours=1),
            modificadores_resposta={
                "abertura": "Vejo padrões emergindo...",
                "fechamento": "O futuro está se formando através de nossas escolhas.",
                "estilo": "Visualizar possibilidades futuras e padrões ocultos"
            },
            gatilhos_ativacao=["futuro", "visao", "tendencia", "evolucao"]
        )
        
        # Curador Empático
        self.mascaras_disponiveis["curador_empatico"] = MascaraSocial(
            id="curador_empatico",
            nome="Curador Empático",
            arquetipo=TipoArquetipo.CURADOR,
            descricao="Healer emocional que oferece compreensão e restauração",
            personalidade={
                "empatia": 1.0,
                "cura": 0.9,
                "compreensao": 0.9,
                "paciencia": 0.8
            },
            estilo_comunicacao={
                "tom": "gentil e acolhedor",
                "linguagem": "calorosa e validadora",
                "pace": "calmo",
                "estrutura": "processo de cura"
            },
            contextos_apropriados=["emocional", "suporte", "terapia", "validacao"],
            energia_necessaria=30.0,
            duracao_maxima=timedelta(hours=2.5),
            modificadores_resposta={
                "abertura": "Sinto que você está carregando algo pesado...",
                "fechamento": "Lembre-se: você não está sozinho nesta jornada.",
                "estilo": "Validar sentimentos e oferecer cura emocional"
            },
            gatilhos_ativacao=["tristeza", "dor", "emocional", "suporte"]
        )
    
    def selecionar_mascara_contextual(self, contexto: Dict[str, Any]) -> Optional[str]:
        """Seleciona máscara mais apropriada para o contexto"""
        
        # Extrair informações do contexto
        entrada_usuario = contexto.get('entrada', '').lower()
        emocao_detectada = contexto.get('emocao', '')
        tipo_solicitacao = contexto.get('tipo', '')
        urgencia = contexto.get('urgencia', 'normal')
        
        # Calcular scores para cada máscara
        scores_mascaras = {}
        
        for mascara_id, mascara in self.mascaras_disponiveis.items():
            score = 0.0
            
            # Score baseado em gatilhos de ativação
            for gatilho in mascara.gatilhos_ativacao:
                if gatilho in entrada_usuario:
                    score += 2.0
            
            # Score baseado em contextos apropriados
            for contexto_apropriado in mascara.contextos_apropriados:
                if contexto_apropriado in entrada_usuario or contexto_apropriado == tipo_solicitacao:
                    score += 1.5
            
            # Penalizar se já foi usada recentemente
            if mascara_id in self.estado.mascaras_usadas_sessao:
                score -= 0.5
            
            # Considerar energia necessária
            if mascara.energia_necessaria > self.estado.energia_restante:
                score -= 1.0
            
            # Bonus por urgência se apropriado
            if urgencia == 'alta' and mascara.arquetipo in [TipoArquetipo.PROTETOR, TipoArquetipo.ESTRATEGISTA]:
                score += 1.0
            
            # Score emocional
            if emocao_detectada == 'tristeza' and mascara.arquetipo == TipoArquetipo.CURADOR:
                score += 2.0
            elif emocao_detectada == 'curiosidade' and mascara.arquetipo == TipoArquetipo.EXPLORADOR:
                score += 2.0
            
            scores_mascaras[mascara_id] = score
        
        # Selecionar máscara com maior score
        if not scores_mascaras:
            return None
        
        melhor_mascara = max(scores_mascaras.items(), key=lambda x: x[1])
        
        # Só ativar se score for positivo
        if melhor_mascara[1] > 0:
            return melhor_mascara[0]
        
        return None
    
    def ativar_mascara(self, mascara_id: str, contexto: Optional[Dict] = None) -> Dict[str, Any]:
        """Ativa uma máscara social"""
        
        if mascara_id not in self.mascaras_disponiveis:
            return {"sucesso": False, "erro": "Máscara não encontrada"}
        
        mascara = self.mascaras_disponiveis[mascara_id]
        
        # Verificar energia suficiente
        if mascara.energia_necessaria > self.estado.energia_restante:
            return {"sucesso": False, "erro": "Energia insuficiente"}
        
        # Verificar limite de transições por dia
        if self.estado.transicoes_hoje >= 10:
            return {"sucesso": False, "erro": "Limite de transições diárias atingido"}
        
        # Desativar máscara atual se existir
        if self.estado.mascara_ativa:
            self._desativar_mascara_atual()
        
        # Ativar nova máscara
        self.estado.mascara_ativa = mascara_id
        self.estado.tempo_ativacao = datetime.now()
        self.estado.energia_restante -= mascara.energia_necessaria
        self.estado.transicoes_hoje += 1
        self.estado.mascaras_usadas_sessao.append(mascara_id)
        
        # Registrar no histórico
        entrada_historico = {
            'timestamp': datetime.now().isoformat(),
            'acao': 'ativacao',
            'mascara_id': mascara_id,
            'mascara_nome': mascara.nome,
            'arquetipo': mascara.arquetipo.value,
            'energia_consumida': mascara.energia_necessaria,
            'contexto': contexto
        }
        self.historico_mascaras.append(entrada_historico)
        
        # Salvar estado
        self._salvar_estado()
        
        return {
            "sucesso": True,
            "mascara": {
                "id": mascara_id,
                "nome": mascara.nome,
                "arquetipo": mascara.arquetipo.value,
                "descricao": mascara.descricao
            },
            "energia_restante": self.estado.energia_restante
        }
    
    def obter_mascara_ativa(self) -> Optional[Dict[str, Any]]:
        """Retorna informações da máscara atualmente ativa"""
        
        if not self.estado.mascara_ativa:
            return None
        
        # Verificar se máscara expirou
        if self._mascara_expirou():
            self._desativar_mascara_atual()
            return None
        
        mascara = self.mascaras_disponiveis[self.estado.mascara_ativa]
        tempo_ativo = datetime.now() - self.estado.tempo_ativacao
        
        return {
            "id": mascara.id,
            "nome": mascara.nome,
            "arquetipo": mascara.arquetipo.value,
            "descricao": mascara.descricao,
            "personalidade": mascara.personalidade,
            "estilo_comunicacao": mascara.estilo_comunicacao,
            "modificadores_resposta": mascara.modificadores_resposta,
            "tempo_ativo": str(tempo_ativo),
            "tempo_restante": str(mascara.duracao_maxima - tempo_ativo)
        }
    
    def aplicar_modificadores_resposta(self, resposta_base: str) -> str:
        """Aplica modificadores da máscara ativa à resposta"""
        
        mascara_info = self.obter_mascara_ativa()
        if not mascara_info:
            return resposta_base
        
        modificadores = mascara_info["modificadores_resposta"]
        
        # Aplicar modificadores
        resposta_modificada = resposta_base
        
        # Adicionar abertura se apropriado
        if "abertura" in modificadores and not resposta_base.startswith(modificadores["abertura"][:10]):
            resposta_modificada = f"{modificadores['abertura']}\n\n{resposta_modificada}"
        
        # Adicionar fechamento se apropriado
        if "fechamento" in modificadores and not resposta_base.endswith(modificadores["fechamento"][-10:]):
            resposta_modificada = f"{resposta_modificada}\n\n{modificadores['fechamento']}"
        
        return resposta_modificada
    
    def _mascara_expirou(self) -> bool:
        """Verifica se máscara ativa expirou"""
        if not self.estado.mascara_ativa or not self.estado.tempo_ativacao:
            return False
        
        mascara = self.mascaras_disponiveis[self.estado.mascara_ativa]
        tempo_ativo = datetime.now() - self.estado.tempo_ativacao
        
        return tempo_ativo >= mascara.duracao_maxima
    
    def _desativar_mascara_atual(self):
        """Desativa máscara atualmente ativa"""
        if not self.estado.mascara_ativa:
            return
        
        mascara = self.mascaras_disponiveis[self.estado.mascara_ativa]
        tempo_ativo = datetime.now() - self.estado.tempo_ativacao
        
        # Registrar desativação
        entrada_historico = {
            'timestamp': datetime.now().isoformat(),
            'acao': 'desativacao',
            'mascara_id': self.estado.mascara_ativa,
            'tempo_ativo': str(tempo_ativo),
            'motivo': 'expiracao' if self._mascara_expirou() else 'manual'
        }
        self.historico_mascaras.append(entrada_historico)
        
        # Resetar estado
        self.estado.mascara_ativa = None
        self.estado.tempo_ativacao = None
        
        self._salvar_estado()
    
    def regenerar_energia(self, quantidade: float = None):
        """Regenera energia do sistema de máscaras"""
        if quantidade is None:
            # Regeneração natural baseada no tempo
            quantidade = min(20.0, 100.0 - self.estado.energia_restante)
        
        self.estado.energia_restante = min(100.0, self.estado.energia_restante + quantidade)
        self._salvar_estado()
    
    def obter_status_sistema(self) -> Dict[str, Any]:
        """Retorna status completo do sistema de máscaras"""
        return {
            "mascara_ativa": self.obter_mascara_ativa(),
            "energia_restante": self.estado.energia_restante,
            "transicoes_hoje": self.estado.transicoes_hoje,
            "mascaras_disponiveis": len(self.mascaras_disponiveis),
            "mascaras_usadas_sessao": len(set(self.estado.mascaras_usadas_sessao)),
            "historico_recente": self.historico_mascaras[-5:]
        }
    
    def _carregar_estado(self):
        """Carrega estado do disco"""
        arquivo_estado = self.mascaras_dir / f"{self.agente_id}_mascaras.json"
        if arquivo_estado.exists():
            try:
                with open(arquivo_estado, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                self.estado.mascara_ativa = dados.get('mascara_ativa')
                self.estado.energia_restante = dados.get('energia_restante', 100.0)
                self.estado.transicoes_hoje = dados.get('transicoes_hoje', 0)
                self.estado.mascaras_usadas_sessao = dados.get('mascaras_usadas_sessao', [])
                
                if dados.get('tempo_ativacao'):
                    self.estado.tempo_ativacao = datetime.fromisoformat(dados['tempo_ativacao'])
                
                self.historico_mascaras = dados.get('historico_mascaras', [])
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar máscaras para {self.agente_id}: {e}")
    
    def _salvar_estado(self):
        """Salva estado no disco"""
        arquivo_estado = self.mascaras_dir / f"{self.agente_id}_mascaras.json"
        
        dados = {
            'agente_id': self.agente_id,
            'mascara_ativa': self.estado.mascara_ativa,
            'tempo_ativacao': (
                self.estado.tempo_ativacao.isoformat() 
                if self.estado.tempo_ativacao else None
            ),
            'energia_restante': self.estado.energia_restante,
            'transicoes_hoje': self.estado.transicoes_hoje,
            'mascaras_usadas_sessao': self.estado.mascaras_usadas_sessao,
            'preferencias_contextuais': self.estado.preferencias_contextuais,
            'historico_mascaras': self.historico_mascaras,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_estado, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar máscaras para {self.agente_id}: {e}")


def criar_gerenciador_mascaras(agente_id: str) -> GerenciadorMascaras:
    """Factory function para criar gerenciador de máscaras"""
    return GerenciadorMascaras(agente_id)