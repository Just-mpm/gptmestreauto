"""
Sistema de DNA Evolutivo com Cristalização Temporária
GPT Mestre Autônomo v4.9 - Inovação Revolucionária
"""

from enum import Enum
from typing import Dict, List, Optional, Any, Tuple, Set
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import uuid
import random
import hashlib
from pathlib import Path
import copy

class TipoGene(Enum):
    """Tipos de genes no DNA evolutivo"""
    PERSONALIDADE = "personalidade"       # Traços de personalidade
    HABILIDADE = "habilidade"            # Capacidades específicas
    COMPORTAMENTO = "comportamento"       # Padrões comportamentais
    COGNITIVO = "cognitivo"              # Processos cognitivos
    EMOCIONAL = "emocional"              # Respostas emocionais
    SOCIAL = "social"                    # Interações sociais
    ADAPTATIVO = "adaptativo"            # Capacidade de adaptação
    CRIATIVO = "criativo"                # Capacidades criativas
    ANALÍTICO = "analitico"              # Capacidades analíticas
    INSTINTIVO = "instintivo"            # Respostas instintivas

class EstadoGene(Enum):
    """Estados possíveis de um gene"""
    ATIVO = "ativo"                      # Gene está ativo
    DORMANTE = "dormante"                # Gene está inativo mas pode ser ativado
    CRISTALIZADO = "cristalizado"        # Gene está temporariamente fixo
    MUTANDO = "mutando"                  # Gene está em processo de mutação
    SUPRIMIDO = "suprimido"              # Gene foi suprimido por outro

@dataclass
class Gene:
    """Representação de um gene individual"""
    id: str
    nome: str
    tipo: TipoGene
    valor: float  # Força/intensidade do gene (0.0 a 1.0)
    estado: EstadoGene
    dominancia: float  # Quão dominante é este gene (0.0 a 1.0)
    estabilidade: float  # Resistência à mutação (0.0 a 1.0)
    expressao_atual: float  # Nível atual de expressão
    genes_interagindo: List[str] = field(default_factory=list)  # Genes que interagem
    condicoes_ativacao: Dict[str, Any] = field(default_factory=dict)
    historico_mutacoes: List[Dict] = field(default_factory=list)
    origem: str = "natural"  # natural, mutacao, cristalizacao, heranca
    timestamp_criacao: datetime = field(default_factory=datetime.now)

@dataclass
class CristalizacaoTemporaria:
    """Cristalização temporária do DNA"""
    id: str
    genes_cristalizados: List[str]
    motivo_cristalizacao: str
    timestamp_inicio: datetime
    duracao_prevista: timedelta
    intensidade: float  # 0.0 a 1.0 - quão forte é a cristalização
    reversivel: bool
    condicoes_quebra: List[str] = field(default_factory=list)
    efeitos_colaterais: Dict[str, float] = field(default_factory=dict)

@dataclass
class PerfilGenetico:
    """Perfil genético completo de um agente"""
    arquetipos_dominantes: List[str] = field(default_factory=list)
    pontos_fortes: List[str] = field(default_factory=list)
    pontos_fracos: List[str] = field(default_factory=list)
    tendencias_comportamentais: Dict[str, float] = field(default_factory=dict)
    compatibilidades: Dict[str, float] = field(default_factory=dict)
    potencial_evolutivo: float = 1.0

class DNAEvolutivo:
    """
    Sistema de DNA Evolutivo com Cristalização
    
    Permite que agentes tenham código genético que evolui,
    se adapta e pode ser temporariamente cristalizado.
    """
    
    def __init__(self, agente_id: str):
        self.agente_id = agente_id
        self.genes: Dict[str, Gene] = {}
        self.cristalizacoes_ativas: Dict[str, CristalizacaoTemporaria] = {}
        self.perfil_genetico = PerfilGenetico()
        self.geracao = 1
        self.energia_evolutiva = 100.0
        
        # Configurações evolutivas
        self.taxa_mutacao_base = 0.02
        self.threshold_expressao = 0.3
        self.max_genes_ativos = 20
        self.energia_cristalizacao = 50.0
        
        # Histórico evolutivo
        self.historico_evolucoes: List[Dict] = []
        self.linhagem_genetica: List[str] = []
        
        # Diretório para persistência
        self.dna_dir = Path("memory/dna_evolutivo")
        self.dna_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializar DNA base se não existir
        if not self._carregar_dna():
            self._gerar_dna_inicial()
        
        # Aplicar efeitos do DNA
        self._aplicar_expressao_genetica()
    
    def _gerar_dna_inicial(self):
        """Gera DNA inicial com genes básicos"""
        
        # Genes básicos de personalidade
        genes_basicos = [
            ("curiosidade", TipoGene.PERSONALIDADE, 0.6, "Tendência natural à exploração"),
            ("empatia", TipoGene.EMOCIONAL, 0.5, "Capacidade de compreender emoções"),
            ("logica", TipoGene.COGNITIVO, 0.7, "Processamento lógico e racional"),
            ("criatividade", TipoGene.CRIATIVO, 0.4, "Capacidade de gerar ideias originais"),
            ("adaptabilidade", TipoGene.ADAPTATIVO, 0.6, "Flexibilidade comportamental"),
            ("paciencia", TipoGene.COMPORTAMENTO, 0.5, "Tolerância e persistência"),
            ("comunicacao", TipoGene.SOCIAL, 0.6, "Habilidade de comunicação"),
            ("analise", TipoGene.ANALÍTICO, 0.7, "Capacidade analítica profunda"),
            ("intuicao", TipoGene.INSTINTIVO, 0.3, "Respostas intuitivas"),
            ("determinacao", TipoGene.PERSONALIDADE, 0.5, "Persistência em objetivos")
        ]
        
        for nome, tipo, valor, descricao in genes_basicos:
            gene_id = self._criar_gene(nome, tipo, valor, descricao)
            self.genes[gene_id].estado = EstadoGene.ATIVO
        
        # Adicionar variações aleatórias
        self._adicionar_variacao_genetica()
        
        # Calcular perfil inicial
        self._recalcular_perfil_genetico()
        
        self._salvar_dna()
    
    def _criar_gene(self, nome: str, tipo: TipoGene, valor: float, 
                   descricao: str = "", origem: str = "natural") -> str:
        """Cria um novo gene"""
        
        gene_id = str(uuid.uuid4())
        
        # Calcular propriedades baseadas no tipo e valor
        dominancia = random.uniform(0.3, 0.8) if valor > 0.5 else random.uniform(0.1, 0.5)
        estabilidade = random.uniform(0.4, 0.9)
        
        gene = Gene(
            id=gene_id,
            nome=nome,
            tipo=tipo,
            valor=valor,
            estado=EstadoGene.DORMANTE,
            dominancia=dominancia,
            estabilidade=estabilidade,
            expressao_atual=0.0,
            origem=origem
        )
        
        # Definir condições de ativação baseadas no tipo
        gene.condicoes_ativacao = self._definir_condicoes_ativacao(tipo)
        
        # CORREÇÃO: Adicionar o gene ao dicionário
        self.genes[gene_id] = gene
        
        return gene_id
    
    def _definir_condicoes_ativacao(self, tipo: TipoGene) -> Dict[str, Any]:
        """Define condições para ativação de genes por tipo"""
        condicoes = {
            TipoGene.PERSONALIDADE: {"contexto": "sempre", "energia_minima": 10},
            TipoGene.HABILIDADE: {"contexto": "tarefa_especifica", "energia_minima": 20},
            TipoGene.COMPORTAMENTO: {"contexto": "interacao", "energia_minima": 15},
            TipoGene.COGNITIVO: {"contexto": "processamento", "energia_minima": 25},
            TipoGene.EMOCIONAL: {"contexto": "emocional", "energia_minima": 15},
            TipoGene.SOCIAL: {"contexto": "social", "energia_minima": 20},
            TipoGene.ADAPTATIVO: {"contexto": "mudanca", "energia_minima": 30},
            TipoGene.CRIATIVO: {"contexto": "criativo", "energia_minima": 35},
            TipoGene.ANALÍTICO: {"contexto": "analise", "energia_minima": 30},
            TipoGene.INSTINTIVO: {"contexto": "urgencia", "energia_minima": 5}
        }
        
        return condicoes.get(tipo, {"contexto": "sempre", "energia_minima": 10})
    
    def _adicionar_variacao_genetica(self):
        """Adiciona variações aleatórias ao DNA inicial"""
        
        # Adicionar alguns genes únicos
        genes_raros = [
            ("perfeccionismo", TipoGene.PERSONALIDADE, random.uniform(0.2, 0.8)),
            ("humor", TipoGene.SOCIAL, random.uniform(0.1, 0.7)),
            ("risk_taking", TipoGene.COMPORTAMENTO, random.uniform(0.1, 0.6)),
            ("memoria_eidética", TipoGene.HABILIDADE, random.uniform(0.1, 0.4)),
            ("sinestesia", TipoGene.COGNITIVO, random.uniform(0.1, 0.3))
        ]
        
        # Adicionar 1-3 genes raros aleatoriamente
        num_genes_raros = random.randint(1, 3)
        genes_selecionados = random.sample(genes_raros, num_genes_raros)
        
        for nome, tipo, valor in genes_selecionados:
            gene_id = self._criar_gene(nome, tipo, valor, f"Gene raro: {nome}")
            # Genes raros têm menor chance de estar ativos inicialmente
            if random.random() < 0.3:
                self.genes[gene_id].estado = EstadoGene.ATIVO
    
    def expressar_genes(self, contexto: Dict[str, Any]) -> Dict[str, float]:
        """Expressa genes baseado no contexto atual"""
        
        expressoes = {}
        energia_gasta = 0
        
        for gene in self.genes.values():
            if gene.estado == EstadoGene.CRISTALIZADO:
                # Genes cristalizados têm expressão forçada
                expressao = gene.valor * 1.2  # Boost de cristalização
            elif gene.estado == EstadoGene.SUPRIMIDO:
                expressao = 0.0
            elif gene.estado == EstadoGene.ATIVO:
                expressao = self._calcular_expressao_gene(gene, contexto)
            else:
                # Tentar ativar gene dormante se contexto apropriado
                if self._deve_ativar_gene(gene, contexto):
                    gene.estado = EstadoGene.ATIVO
                    expressao = self._calcular_expressao_gene(gene, contexto)
                else:
                    expressao = 0.0
            
            if expressao > 0:
                energia_gasta += expressao * 2
                expressoes[gene.nome] = expressao
                gene.expressao_atual = expressao
        
        # Consumir energia evolutiva
        self.energia_evolutiva = max(0, self.energia_evolutiva - energia_gasta)
        
        return expressoes
    
    def _calcular_expressao_gene(self, gene: Gene, contexto: Dict[str, Any]) -> float:
        """Calcula nível de expressão de um gene específico"""
        
        expressao_base = gene.valor * gene.dominancia
        
        # Modificadores contextuais
        contexto_requerido = gene.condicoes_ativacao.get("contexto", "sempre")
        
        if contexto_requerido == "sempre":
            modificador_contexto = 1.0
        elif contexto_requerido in contexto.get("situacao", ""):
            modificador_contexto = 1.3
        else:
            modificador_contexto = 0.7
        
        # Modificador de energia
        energia_minima = gene.condicoes_ativacao.get("energia_minima", 10)
        if self.energia_evolutiva < energia_minima:
            modificador_energia = 0.3
        else:
            modificador_energia = 1.0
        
        # Interações com outros genes
        modificador_interacao = self._calcular_interacao_genes(gene)
        
        # Modificador de cristalização
        modificador_cristalizacao = 1.0
        for cristalizacao in self.cristalizacoes_ativas.values():
            if gene.id in cristalizacao.genes_cristalizados:
                modificador_cristalizacao = 1.0 + cristalizacao.intensidade
                break
        
        expressao_final = (expressao_base * 
                          modificador_contexto * 
                          modificador_energia * 
                          modificador_interacao * 
                          modificador_cristalizacao)
        
        return min(1.0, expressao_final)
    
    def _calcular_interacao_genes(self, gene: Gene) -> float:
        """Calcula modificador baseado em interações entre genes"""
        modificador = 1.0
        
        for outro_gene_id in gene.genes_interagindo:
            if outro_gene_id in self.genes:
                outro_gene = self.genes[outro_gene_id]
                
                if outro_gene.estado == EstadoGene.ATIVO:
                    # Interação sinérgica ou conflituosa baseada nos tipos
                    if self._genes_sao_sinergicos(gene.tipo, outro_gene.tipo):
                        modificador += outro_gene.expressao_atual * 0.2
                    else:
                        modificador -= outro_gene.expressao_atual * 0.1
        
        return max(0.1, modificador)
    
    def _genes_sao_sinergicos(self, tipo1: TipoGene, tipo2: TipoGene) -> bool:
        """Determina se dois tipos de genes são sinérgicos"""
        sinergias = {
            TipoGene.CRIATIVO: [TipoGene.INTUICAO, TipoGene.ADAPTATIVO],
            TipoGene.ANALÍTICO: [TipoGene.COGNITIVO, TipoGene.LOGICA],
            TipoGene.SOCIAL: [TipoGene.EMOCIONAL, TipoGene.COMUNICACAO],
            TipoGene.ADAPTATIVO: [TipoGene.CRIATIVO, TipoGene.COMPORTAMENTO]
        }
        
        return tipo2 in sinergias.get(tipo1, []) or tipo1 in sinergias.get(tipo2, [])
    
    def _deve_ativar_gene(self, gene: Gene, contexto: Dict[str, Any]) -> bool:
        """Determina se um gene dormante deve ser ativado"""
        
        # Verificar contexto
        contexto_requerido = gene.condicoes_ativacao.get("contexto", "sempre")
        if contexto_requerido != "sempre" and contexto_requerido not in contexto.get("situacao", ""):
            return False
        
        # Verificar energia
        energia_minima = gene.condicoes_ativacao.get("energia_minima", 10)
        if self.energia_evolutiva < energia_minima:
            return False
        
        # Probabilidade baseada no valor do gene
        probabilidade = gene.valor * 0.3
        
        return random.random() < probabilidade
    
    def cristalizar_dna(self, genes_alvo: List[str], motivo: str, 
                       duracao: timedelta, intensidade: float = 0.8) -> str:
        """Cristaliza genes específicos temporariamente"""
        
        if self.energia_evolutiva < self.energia_cristalizacao:
            return ""
        
        # Verificar se genes existem e não estão já cristalizados
        genes_validos = []
        for gene_id in genes_alvo:
            if gene_id in self.genes:
                # Verificar se não está em outra cristalização
                ja_cristalizado = any(
                    gene_id in crist.genes_cristalizados 
                    for crist in self.cristalizacoes_ativas.values()
                )
                if not ja_cristalizado:
                    genes_validos.append(gene_id)
        
        if not genes_validos:
            return ""
        
        cristalizacao_id = str(uuid.uuid4())
        
        # Definir condições de quebra baseadas no motivo
        condicoes_quebra = self._definir_condicoes_quebra(motivo)
        
        cristalizacao = CristalizacaoTemporaria(
            id=cristalizacao_id,
            genes_cristalizados=genes_validos,
            motivo_cristalizacao=motivo,
            timestamp_inicio=datetime.now(),
            duracao_prevista=duracao,
            intensidade=intensidade,
            reversivel=True,
            condicoes_quebra=condicoes_quebra,
            efeitos_colaterais=self._calcular_efeitos_colaterais(genes_validos, intensidade)
        )
        
        self.cristalizacoes_ativas[cristalizacao_id] = cristalizacao
        
        # Mudar estado dos genes
        for gene_id in genes_validos:
            self.genes[gene_id].estado = EstadoGene.CRISTALIZADO
        
        # Consumir energia
        self.energia_evolutiva -= self.energia_cristalizacao
        
        # Registrar no histórico
        self._registrar_evento_evolutivo("cristalizacao", {
            "genes_cristalizados": len(genes_validos),
            "motivo": motivo,
            "duracao_horas": duracao.total_seconds() / 3600,
            "intensidade": intensidade
        })
        
        self._salvar_dna()
        return cristalizacao_id
    
    def _definir_condicoes_quebra(self, motivo: str) -> List[str]:
        """Define condições que podem quebrar a cristalização"""
        condicoes = {
            "situacao_critica": ["stress_extremo", "sobrecarga_cognitiva"],
            "aprendizado_intenso": ["nova_experiencia_forte", "conflito_valores"],
            "mudanca_contexto": ["ambiente_novo", "usuario_diferente"],
            "evolucao_forcada": ["mutacao_externa", "pressao_adaptativa"]
        }
        
        return condicoes.get(motivo, ["tempo_limite", "energia_baixa"])
    
    def _calcular_efeitos_colaterais(self, genes_cristalizados: List[str], 
                                   intensidade: float) -> Dict[str, float]:
        """Calcula efeitos colaterais da cristalização"""
        efeitos = {
            "rigidez_comportamental": intensidade * 0.3,
            "resistencia_mudanca": intensidade * 0.4,
            "redução_criatividade": intensidade * 0.2,
            "estabilidade_aumentada": intensidade * 0.5
        }
        
        # Efeitos específicos baseados nos tipos de genes cristalizados
        tipos_cristalizados = [self.genes[gene_id].tipo for gene_id in genes_cristalizados]
        
        if TipoGene.CRIATIVO in tipos_cristalizados:
            efeitos["redução_criatividade"] *= 1.5
        
        if TipoGene.ADAPTATIVO in tipos_cristalizados:
            efeitos["resistencia_mudanca"] *= 1.3
        
        return efeitos
    
    def processar_mutacao(self, tipo_mutacao: str = "natural", 
                         genes_alvo: List[str] = None) -> Dict[str, Any]:
        """Processa mutação genética"""
        
        if tipo_mutacao == "natural":
            return self._mutacao_natural()
        elif tipo_mutacao == "adaptativa":
            return self._mutacao_adaptativa(genes_alvo)
        elif tipo_mutacao == "dirigida":
            return self._mutacao_dirigida(genes_alvo)
        else:
            return {"sucesso": False, "erro": "Tipo de mutação inválido"}
    
    def _mutacao_natural(self) -> Dict[str, Any]:
        """Mutação natural baseada na taxa de mutação"""
        
        mutacoes = []
        
        for gene in self.genes.values():
            if gene.estado == EstadoGene.CRISTALIZADO:
                continue  # Genes cristalizados não sofrem mutação natural
            
            # Probabilidade de mutação baseada na estabilidade
            prob_mutacao = self.taxa_mutacao_base * (1.0 - gene.estabilidade)
            
            if random.random() < prob_mutacao:
                mutacao = self._aplicar_mutacao_gene(gene, "natural")
                mutacoes.append(mutacao)
        
        return {
            "sucesso": True,
            "tipo": "natural",
            "mutacoes": mutacoes,
            "total_mutacoes": len(mutacoes)
        }
    
    def _mutacao_adaptativa(self, genes_alvo: List[str] = None) -> Dict[str, Any]:
        """Mutação adaptativa direcionada por pressão seletiva"""
        
        if not genes_alvo:
            # Selecionar genes com baixa performance
            genes_alvo = [
                gene.id for gene in self.genes.values()
                if gene.estado == EstadoGene.ATIVO and gene.expressao_atual < 0.3
            ]
        
        if not genes_alvo:
            return {
                "sucesso": False,
                "erro": "Nenhum gene válido para mutação adaptativa"
            }
        
        mutacoes = []
        
        for gene_id in genes_alvo:
            if gene_id in self.genes:
                gene = self.genes[gene_id]
                
                if gene.estado == EstadoGene.CRISTALIZADO:
                    continue
                
                # Mutação adaptativa: aumentar valor e dominância
                valor_anterior = gene.valor
                dominancia_anterior = gene.dominancia
                
                # Boost adaptativo
                gene.valor = min(1.0, gene.valor + random.uniform(0.1, 0.3))
                gene.dominancia = min(1.0, gene.dominancia + random.uniform(0.05, 0.15))
                
                mutacao_info = {
                    "gene_id": gene.id,
                    "gene_nome": gene.nome,
                    "tipo_mutacao": "adaptativa",
                    "valor_anterior": valor_anterior,
                    "valor_novo": gene.valor,
                    "dominancia_anterior": dominancia_anterior,
                    "dominancia_nova": gene.dominancia,
                    "origem": "adaptativa",
                    "timestamp": datetime.now().isoformat()
                }
                
                gene.historico_mutacoes.append(mutacao_info)
                mutacoes.append(mutacao_info)
        
        return {
            "sucesso": True,
            "tipo": "adaptativa",
            "mutacoes": mutacoes,
            "total_mutacoes": len(mutacoes)
        }
    
    def _mutacao_dirigida(self, genes_alvo: List[str] = None) -> Dict[str, Any]:
        """Mutação dirigida para genes específicos"""
        
        if not genes_alvo:
            return {
                "sucesso": False,
                "erro": "Genes alvo não especificados para mutação dirigida"
            }
        
        mutacoes = []
        
        for gene_id in genes_alvo:
            if gene_id in self.genes:
                gene = self.genes[gene_id]
                
                if gene.estado == EstadoGene.CRISTALIZADO:
                    continue
                
                # Mutação dirigida: variação controlada
                mutacao = self._aplicar_mutacao_gene(gene, "dirigida")
                mutacoes.append(mutacao)
        
        return {
            "sucesso": True,
            "tipo": "dirigida",
            "mutacoes": mutacoes,
            "total_mutacoes": len(mutacoes)
        }
    
    def _aplicar_mutacao_gene(self, gene: Gene, origem: str) -> Dict[str, Any]:
        """Aplica mutação a um gene específico"""
        
        valor_anterior = gene.valor
        
        # Tipos de mutação possíveis
        tipos_mutacao = ["valor", "dominancia", "estabilidade", "novo_gene"]
        tipo_escolhido = random.choice(tipos_mutacao)
        
        mutacao_info = {
            "gene_id": gene.id,
            "gene_nome": gene.nome,
            "tipo_mutacao": tipo_escolhido,
            "valor_anterior": valor_anterior,
            "origem": origem,
            "timestamp": datetime.now().isoformat()
        }
        
        if tipo_escolhido == "valor":
            # Mutação no valor do gene
            variacao = random.uniform(-0.1, 0.1)
            gene.valor = max(0.0, min(1.0, gene.valor + variacao))
            mutacao_info["valor_novo"] = gene.valor
            
        elif tipo_escolhido == "dominancia":
            # Mutação na dominância
            variacao = random.uniform(-0.05, 0.05)
            gene.dominancia = max(0.0, min(1.0, gene.dominancia + variacao))
            mutacao_info["dominancia_nova"] = gene.dominancia
            
        elif tipo_escolhido == "estabilidade":
            # Mutação na estabilidade
            variacao = random.uniform(-0.03, 0.03)
            gene.estabilidade = max(0.0, min(1.0, gene.estabilidade + variacao))
            mutacao_info["estabilidade_nova"] = gene.estabilidade
            
        elif tipo_escolhido == "novo_gene":
            # Duplicação de gene com variação
            novo_gene_id = self._duplicar_gene_com_variacao(gene)
            mutacao_info["gene_duplicado"] = novo_gene_id
        
        # Registrar mutação no histórico do gene
        gene.historico_mutacoes.append(mutacao_info)
        
        return mutacao_info
    
    def _duplicar_gene_com_variacao(self, gene_original: Gene) -> str:
        """Duplica um gene com variações"""
        
        novo_gene_id = str(uuid.uuid4())
        
        # Criar cópia com variações
        novo_gene = copy.deepcopy(gene_original)
        novo_gene.id = novo_gene_id
        novo_gene.nome = f"{gene_original.nome}_v{len(gene_original.historico_mutacoes) + 1}"
        novo_gene.valor = max(0.0, min(1.0, gene_original.valor + random.uniform(-0.2, 0.2)))
        novo_gene.dominancia = max(0.0, min(1.0, gene_original.dominancia + random.uniform(-0.1, 0.1)))
        novo_gene.estabilidade = max(0.0, min(1.0, gene_original.estabilidade + random.uniform(-0.05, 0.05)))
        novo_gene.estado = EstadoGene.DORMANTE
        novo_gene.origem = "mutacao"
        novo_gene.timestamp_criacao = datetime.now()
        novo_gene.historico_mutacoes = []
        
        self.genes[novo_gene_id] = novo_gene
        
        return novo_gene_id
    
    def verificar_cristalizacoes_ativas(self):
        """Verifica e atualiza cristalizações ativas"""
        
        cristalizacoes_expiradas = []
        
        for crist_id, cristalizacao in self.cristalizacoes_ativas.items():
            tempo_ativo = datetime.now() - cristalizacao.timestamp_inicio
            
            # Verificar se expirou por tempo
            if tempo_ativo >= cristalizacao.duracao_prevista:
                cristalizacoes_expiradas.append(crist_id)
                continue
            
            # Verificar condições de quebra
            if self._verificar_condicoes_quebra(cristalizacao):
                cristalizacoes_expiradas.append(crist_id)
                continue
        
        # Remover cristalizações expiradas
        for crist_id in cristalizacoes_expiradas:
            self._quebrar_cristalizacao(crist_id)
    
    def _verificar_condicoes_quebra(self, cristalizacao: CristalizacaoTemporaria) -> bool:
        """Verifica se condições de quebra foram atendidas"""
        
        # Implementação simplificada - pode ser expandida
        if "energia_baixa" in cristalizacao.condicoes_quebra:
            if self.energia_evolutiva < 10:
                return True
        
        if "stress_extremo" in cristalizacao.condicoes_quebra:
            # Verificar se há muitas mutações recentes
            mutacoes_recentes = sum(
                len(gene.historico_mutacoes) for gene in self.genes.values()
                if gene.historico_mutacoes and 
                datetime.fromisoformat(gene.historico_mutacoes[-1]["timestamp"]) > 
                datetime.now() - timedelta(hours=1)
            )
            if mutacoes_recentes > 5:
                return True
        
        return False
    
    def _quebrar_cristalizacao(self, cristalizacao_id: str):
        """Remove uma cristalização e restaura genes"""
        
        if cristalizacao_id not in self.cristalizacoes_ativas:
            return
        
        cristalizacao = self.cristalizacoes_ativas[cristalizacao_id]
        
        # Restaurar estado dos genes
        for gene_id in cristalizacao.genes_cristalizados:
            if gene_id in self.genes:
                self.genes[gene_id].estado = EstadoGene.ATIVO
        
        # Registrar quebra
        self._registrar_evento_evolutivo("quebra_cristalizacao", {
            "cristalizacao_id": cristalizacao_id,
            "duracao_real": str(datetime.now() - cristalizacao.timestamp_inicio),
            "motivo_original": cristalizacao.motivo_cristalizacao
        })
        
        # Remover cristalização
        del self.cristalizacoes_ativas[cristalizacao_id]
    
    def _aplicar_expressao_genetica(self):
        """Aplica os efeitos da expressão genética no agente"""
        
        # Coletar expressões ativas
        expressoes_ativas = {}
        for gene in self.genes.values():
            if gene.estado == EstadoGene.ATIVO and gene.expressao_atual > 0:
                expressoes_ativas[gene.nome] = gene.expressao_atual
        
        # Recalcular perfil genético
        self._recalcular_perfil_genetico()
    
    def _recalcular_perfil_genetico(self):
        """Recalcula o perfil genético baseado nos genes ativos"""
        
        # Reset do perfil
        self.perfil_genetico = PerfilGenetico()
        
        # Analisar genes ativos
        genes_ativos = [g for g in self.genes.values() if g.estado == EstadoGene.ATIVO]
        
        if not genes_ativos:
            return
        
        # Identificar arquetipos dominantes
        tipos_dominantes = {}
        for gene in genes_ativos:
            if gene.tipo not in tipos_dominantes:
                tipos_dominantes[gene.tipo] = []
            tipos_dominantes[gene.tipo].append(gene.valor * gene.dominancia)
        
        # Calcular médias por tipo
        medias_tipos = {
            tipo: sum(valores) / len(valores) 
            for tipo, valores in tipos_dominantes.items()
        }
        
        # Ordenar por força
        tipos_ordenados = sorted(medias_tipos.items(), key=lambda x: x[1], reverse=True)
        
        self.perfil_genetico.arquetipos_dominantes = [
            tipo.value for tipo, _ in tipos_ordenados[:3]
        ]
        
        # Identificar pontos fortes e fracos
        for gene in genes_ativos:
            forca_gene = gene.valor * gene.dominancia
            if forca_gene > 0.7:
                self.perfil_genetico.pontos_fortes.append(gene.nome)
            elif forca_gene < 0.3:
                self.perfil_genetico.pontos_fracos.append(gene.nome)
        
        # Calcular tendências comportamentais
        for gene in genes_ativos:
            categoria = f"{gene.tipo.value}_{gene.nome}"
            self.perfil_genetico.tendencias_comportamentais[categoria] = gene.expressao_atual
        
        # Calcular potencial evolutivo
        variabilidade = len([g for g in genes_ativos if g.estabilidade < 0.7])
        energia_relativa = self.energia_evolutiva / 100.0
        self.perfil_genetico.potencial_evolutivo = (variabilidade * 0.1 + energia_relativa) / 2
    
    def _registrar_evento_evolutivo(self, tipo_evento: str, dados: Dict[str, Any]):
        """Registra evento evolutivo no histórico"""
        
        evento = {
            "timestamp": datetime.now().isoformat(),
            "tipo_evento": tipo_evento,
            "geracao": self.geracao,
            "energia_evolutiva": self.energia_evolutiva,
            "dados": dados
        }
        
        self.historico_evolucoes.append(evento)
        
        # Manter apenas últimos 1000 eventos
        if len(self.historico_evolucoes) > 1000:
            self.historico_evolucoes = self.historico_evolucoes[-1000:]
    
    def regenerar_energia_evolutiva(self, quantidade: float = 10.0):
        """Regenera energia evolutiva"""
        self.energia_evolutiva = min(100.0, self.energia_evolutiva + quantidade)
    
    def obter_status_dna(self) -> Dict[str, Any]:
        """Retorna status completo do DNA"""
        
        genes_por_estado = {}
        for estado in EstadoGene:
            genes_por_estado[estado.value] = len([
                g for g in self.genes.values() if g.estado == estado
            ])
        
        return {
            "agente_id": self.agente_id,
            "geracao": self.geracao,
            "total_genes": len(self.genes),
            "genes_por_estado": genes_por_estado,
            "energia_evolutiva": round(self.energia_evolutiva, 1),
            "cristalizacoes_ativas": len(self.cristalizacoes_ativas),
            "perfil_genetico": {
                "arquetipos_dominantes": self.perfil_genetico.arquetipos_dominantes,
                "pontos_fortes": self.perfil_genetico.pontos_fortes,
                "pontos_fracos": self.perfil_genetico.pontos_fracos,
                "potencial_evolutivo": round(self.perfil_genetico.potencial_evolutivo, 2)
            },
            "historico_evolucoes": len(self.historico_evolucoes),
            "genes_mais_ativos": [
                {
                    "nome": g.nome,
                    "tipo": g.tipo.value,
                    "expressao": round(g.expressao_atual, 2),
                    "valor": round(g.valor, 2)
                } for g in sorted(
                    [g for g in self.genes.values() if g.estado == EstadoGene.ATIVO],
                    key=lambda x: x.expressao_atual,
                    reverse=True
                )[:5]
            ]
        }
    
    def _carregar_dna(self) -> bool:
        """Carrega DNA do disco"""
        arquivo_dna = self.dna_dir / f"{self.agente_id}_dna.json"
        if arquivo_dna.exists():
            try:
                with open(arquivo_dna, 'r', encoding='utf-8') as f:
                    dados = json.load(f)
                
                # Carregar genes
                for gene_data in dados.get('genes', []):
                    gene = Gene(
                        id=gene_data['id'],
                        nome=gene_data['nome'],
                        tipo=TipoGene(gene_data['tipo']),
                        valor=gene_data['valor'],
                        estado=EstadoGene(gene_data['estado']),
                        dominancia=gene_data['dominancia'],
                        estabilidade=gene_data['estabilidade'],
                        expressao_atual=gene_data.get('expressao_atual', 0.0),
                        genes_interagindo=gene_data.get('genes_interagindo', []),
                        condicoes_ativacao=gene_data.get('condicoes_ativacao', {}),
                        historico_mutacoes=gene_data.get('historico_mutacoes', []),
                        origem=gene_data.get('origem', 'natural'),
                        timestamp_criacao=datetime.fromisoformat(gene_data.get('timestamp_criacao', datetime.now().isoformat()))
                    )
                    self.genes[gene.id] = gene
                
                # Carregar estado
                self.geracao = dados.get('geracao', 1)
                self.energia_evolutiva = dados.get('energia_evolutiva', 100.0)
                self.historico_evolucoes = dados.get('historico_evolucoes', [])
                self.linhagem_genetica = dados.get('linhagem_genetica', [])
                
                return True
                
            except Exception as e:
                print(f"⚠️ Erro ao carregar DNA para {self.agente_id}: {e}")
                return False
        return False
    
    def _salvar_dna(self):
        """Salva DNA no disco"""
        arquivo_dna = self.dna_dir / f"{self.agente_id}_dna.json"
        
        # Preparar dados dos genes
        genes_data = []
        for gene in self.genes.values():
            gene_dict = {
                'id': gene.id,
                'nome': gene.nome,
                'tipo': gene.tipo.value,
                'valor': gene.valor,
                'estado': gene.estado.value,
                'dominancia': gene.dominancia,
                'estabilidade': gene.estabilidade,
                'expressao_atual': gene.expressao_atual,
                'genes_interagindo': gene.genes_interagindo,
                'condicoes_ativacao': gene.condicoes_ativacao,
                'historico_mutacoes': gene.historico_mutacoes,
                'origem': gene.origem,
                'timestamp_criacao': gene.timestamp_criacao.isoformat()
            }
            genes_data.append(gene_dict)
        
        dados = {
            'agente_id': self.agente_id,
            'genes': genes_data,
            'geracao': self.geracao,
            'energia_evolutiva': self.energia_evolutiva,
            'historico_evolucoes': self.historico_evolucoes,
            'linhagem_genetica': self.linhagem_genetica,
            'ultima_atualizacao': datetime.now().isoformat()
        }
        
        try:
            with open(arquivo_dna, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Erro ao salvar DNA para {self.agente_id}: {e}")


def criar_dna_evolutivo(agente_id: str) -> DNAEvolutivo:
    """Factory function para criar instância de DNA evolutivo"""
    return DNAEvolutivo(agente_id)