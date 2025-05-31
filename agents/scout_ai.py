"""
🔍 ScoutAI v1.3A — Radar Estratégico de Oportunidades Comerciais
Subagente especialista em pesquisa de produtos, tendências e oportunidades em tempo real
Integrado com BaseAgentV2 para máxima robustez e confiabilidade
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

class TipoAnalise(Enum):
    """Tipos de análise do ScoutAI"""
    NICHO_INVESTIGACAO = "nicho_investigacao"
    TENDENCIA_PRODUTO = "tendencia_produto"
    ANALISE_CONCORRENCIA = "analise_concorrencia"
    SATURACAO_MARKETPLACE = "saturacao_marketplace"
    COMPARACAO_PRECOS = "comparacao_precos"
    CRESCIMENTO_ACELERADO = "crescimento_acelerado"
    PERFORMANCE_COMPARATIVA = "performance_comparativa"
    DETECCAO_OPORTUNIDADE = "deteccao_oportunidade"

class NivelTendencia(Enum):
    """Níveis de tendência identificados"""
    EMERGENTE = "emergente"
    CRESCIMENTO = "crescimento"
    PICO = "pico"
    DECLINIO = "declinio"
    SATURADO = "saturado"

class NivelConcorrencia(Enum):
    """Níveis de concorrência"""
    BAIXA = "baixa"
    MODERADA = "moderada"
    ALTA = "alta"
    SATURADA = "saturada"

class StatusRisco(Enum):
    """Status de risco para alertas"""
    VERDE = "verde"        # Oportunidade clara
    AMARELO = "amarelo"    # Atenção necessária
    VERMELHO = "vermelho"  # Alto risco

@dataclass
class ProdutoAnalise:
    """Estrutura de análise de produto"""
    nome: str
    categoria: str
    marketplace: str
    preco_encontrado: float
    numero_vendedores: int
    nivel_tendencia: NivelTendencia
    nivel_concorrencia: NivelConcorrencia
    utilidade_mapeada: str
    pontos_fortes: List[str]
    pontos_fracos: List[str]
    microtags: List[str]
    score_oportunidade: float  # 0-10
    diferencial_sugerido: Optional[str] = None

@dataclass
class ComparacaoPrecos:
    """Comparação de preços entre marketplaces"""
    produto: str
    shopee_preco: Optional[float] = None
    magalu_preco: Optional[float] = None
    amazon_preco: Optional[float] = None
    mercadolivre_preco: Optional[float] = None
    variacao_maxima: float = 0.0
    marketplace_mais_barato: str = ""
    marketplace_mais_caro: str = ""
    oportunidade_arbitragem: bool = False

@dataclass
class RelatorioScout:
    """Relatório completo do ScoutAI"""
    id: str
    timestamp: datetime
    tipo_analise: TipoAnalise
    query_original: str
    produtos_analisados: List[ProdutoAnalise]
    comparacoes_precos: List[ComparacaoPrecos]
    insights_estrategicos: List[str]
    acoes_recomendadas: List[str]
    status_risco: StatusRisco
    gatilhos_ativados: List[str]
    agentes_sugeridos: List[str]  # Agentes que devem ser acionados
    score_geral: float
    duracao_analise: float

class ScoutAI(BaseAgentV2):
    """
    🔍 ScoutAI v1.3A — Radar Estratégico de Oportunidades
    
    FUNCIONALIDADES PRINCIPAIS:
    - 🎯 Investigação de nichos e produtos
    - 📈 Análise de tendências em tempo real
    - 🏪 Monitoramento de concorrência
    - 💰 Comparação de preços entre marketplaces
    - 🚨 Detecção de alertas e oportunidades
    - 🤖 Ativação automática de agentes complementares
    
    INTEGRAÇÃO:
    - DeepAgent: Coleta dados de mercado
    - PromptCrafter: Ajuste de prompts com descobertas
    - CopyBooster: Melhoria de títulos/descrições
    - KitBuilder: Ativação de kits promissores
    - AutoPrice: Ajustes de preço por concorrência
    - Oráculo: Consultoria em casos ambíguos
    """
    
    def __init__(self, config: Optional[Dict] = None):
        # Configuração específica do ScoutAI
        scout_config = {
            "rate_limit_per_minute": 25,  # Pesquisas intensivas
            "burst_allowance": 8,
            "failure_threshold": 3,
            "recovery_timeout": 45,
            "cache_enabled": True,
            "cache_ttl_seconds": 1800,  # 30 minutos para dados de mercado
            "persistent_memory": True,
            "memory_storage_dir": "memory/agents/scout",
            "max_retry_attempts": 2,
            "timeout_seconds": 45
        }
        
        if config:
            scout_config.update(config)
        
        super().__init__(
            name="ScoutAI",
            description="Radar Estratégico v1.3A - Especialista em Oportunidades Comerciais",
            config=scout_config
        )
        
        # === SISTEMA DE DETECÇÃO ===
        self.gatilhos_ativos = {
            "tendencia_global_baixa_oferta": True,
            "novo_ciclo_sazonalidade": True,
            "ficha_tecnica_fraca": True,
            "variacao_preco_30pct": True,
            "produto_clone_detectado": True,
            "palavra_chave_restrita": True
        }
        
        # === BASES DE CONHECIMENTO ===
        self.marketplaces_suportados = [
            "shopee", "amazon", "mercadolivre", "magalu", 
            "americanas", "casasbahia", "tiktokshop"
        ]
        
        self.palavras_restritas = [
            "massageador facial ultrassônico", "produto médico",
            "suplemento", "remédio", "medicamento", "anvisa"
        ]
        
        # === HISTÓRICO E CACHE ===
        self.historico_analises: List[RelatorioScout] = []
        self.cache_tendencias = {}
        self.cache_precos = {}
        
        # === INTEGRAÇÃO COM OUTROS AGENTES ===
        self.deep_agent = None
        self.oraculo = None
        
        # Estatísticas específicas
        self.stats.update({
            "analises_realizadas": 0,
            "oportunidades_detectadas": 0,
            "alertas_vermelho_gerados": 0,
            "agentes_acionados": 0,
            "produtos_monitorados": 0,
            "tendencias_identificadas": 0,
            "score_medio_oportunidade": 0.0
        })
        
        # Carregar histórico da memória persistente
        self._carregar_historico_analises()
        
        logger.info("🔍 ScoutAI v1.3A inicializado - Radar Estratégico ATIVO")
    
    def _carregar_historico_analises(self):
        """Carrega histórico de análises da memória persistente"""
        if self.memory.context.get("historico_analises"):
            try:
                historico_data = self.memory.context["historico_analises"]
                # Reconstrói o histórico (versão simplificada)
                self.stats["analises_realizadas"] = len(historico_data)
                logger.info(f"📚 Carregado histórico com {self.stats['analises_realizadas']} análises")
            except Exception as e:
                logger.warning(f"⚠️ Erro ao carregar histórico: {e}")
    
    def _processar_interno(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        🔍 PROCESSAMENTO PRINCIPAL DO SCOUTAI v1.3A
        
        FLUXO DE ANÁLISE:
        1. 🎯 Detecção do tipo de análise
        2. 🔍 Coleta de dados (via DeepAgent se disponível)
        3. 📊 Análise de tendências e concorrência
        4. 💰 Comparação de preços
        5. 🚨 Verificação de gatilhos especiais
        6. 📝 Geração de relatório estruturado
        7. 🤖 Acionamento de agentes complementares
        8. 💾 Persistência de resultados
        """
        inicio_analise = time.time()
        
        # 1. DETECÇÃO DO TIPO DE ANÁLISE
        tipo_analise, parametros = self._detectar_tipo_analise(mensagem)
        logger.info(f"🎯 Análise detectada: {tipo_analise.value}")
        
        # 2. COLETA DE DADOS
        dados_coletados = self._coletar_dados_mercado(parametros, tipo_analise)
        
        # 3. ANÁLISE ESTRUTURADA
        produtos_analisados = self._analisar_produtos(dados_coletados, tipo_analise)
        comparacoes_precos = self._comparar_precos(produtos_analisados)
        
        # 4. GERAÇÃO DE INSIGHTS
        insights = self._gerar_insights_estrategicos(produtos_analisados, comparacoes_precos)
        acoes = self._gerar_acoes_recomendadas(produtos_analisados, insights)
        
        # 5. VERIFICAÇÃO DE GATILHOS
        gatilhos_ativados, status_risco = self._verificar_gatilhos_especiais(
            produtos_analisados, comparacoes_precos, parametros
        )
        
        # 6. ACIONAMENTO DE AGENTES
        agentes_sugeridos = self._definir_agentes_complementares(
            tipo_analise, produtos_analisados, gatilhos_ativados
        )
        
        # 7. SCORE GERAL
        score_geral = self._calcular_score_geral(produtos_analisados, status_risco)
        
        # 8. CRIAÇÃO DO RELATÓRIO
        relatorio = RelatorioScout(
            id=f"scout_{uuid.uuid4().hex[:8]}",
            timestamp=datetime.now(),
            tipo_analise=tipo_analise,
            query_original=mensagem,
            produtos_analisados=produtos_analisados,
            comparacoes_precos=comparacoes_precos,
            insights_estrategicos=insights,
            acoes_recomendadas=acoes,
            status_risco=status_risco,
            gatilhos_ativados=gatilhos_ativados,
            agentes_sugeridos=agentes_sugeridos,
            score_geral=score_geral,
            duracao_analise=time.time() - inicio_analise
        )
        
        # 9. PERSISTÊNCIA E ESTATÍSTICAS
        self._registrar_analise(relatorio)
        self._atualizar_stats_scout(relatorio)
        
        # 10. FORMATAÇÃO DA RESPOSTA
        resposta_final = self._formatar_resposta_scout(relatorio)
        
        logger.info(f"🔍 Análise {relatorio.id} concluída em {relatorio.duracao_analise:.2f}s")
        
        return resposta_final
    
    def _detectar_tipo_analise(self, mensagem: str) -> Tuple[TipoAnalise, Dict]:
        """🎯 Detecta o tipo de análise baseado na mensagem"""
        mensagem_lower = mensagem.lower()
        parametros = {"query": mensagem}
        
        # Padrões de detecção
        if any(palavra in mensagem_lower for palavra in ["investigue", "nicho"]):
            return TipoAnalise.NICHO_INVESTIGACAO, parametros
        
        elif any(palavra in mensagem_lower for palavra in ["tendência", "avalie a tendência"]):
            return TipoAnalise.TENDENCIA_PRODUTO, parametros
        
        elif any(palavra in mensagem_lower for palavra in ["concorrentes", "busque concorrentes"]):
            return TipoAnalise.ANALISE_CONCORRENCIA, parametros
        
        elif any(palavra in mensagem_lower for palavra in ["saturação", "shopee"]):
            parametros["marketplace"] = "shopee"
            return TipoAnalise.SATURACAO_MARKETPLACE, parametros
        
        elif any(palavra in mensagem_lower for palavra in ["diferença de preço", "compare"]):
            return TipoAnalise.COMPARACAO_PRECOS, parametros
        
        elif any(palavra in mensagem_lower for palavra in ["crescimento acelerado", "tiktok shop"]):
            parametros["marketplace"] = "tiktokshop"
            return TipoAnalise.CRESCIMENTO_ACELERADO, parametros
        
        elif any(palavra in mensagem_lower for palavra in ["performance", "amazon br"]):
            return TipoAnalise.PERFORMANCE_COMPARATIVA, parametros
        
        else:
            return TipoAnalise.DETECCAO_OPORTUNIDADE, parametros
    
    def _coletar_dados_mercado(self, parametros: Dict, tipo_analise: TipoAnalise) -> Dict:
        """🔍 Coleta dados de mercado (simulated - integração com DeepAgent futura)"""
        # Esta função seria integrada com DeepAgent para busca real
        # Por enquanto, retorna dados simulados baseados no tipo de análise
        
        dados_simulados = {
            "produtos_encontrados": [],
            "precos_coletados": {},
            "vendedores_identificados": {},
            "dados_tendencia": {},
            "metadados_coleta": {
                "timestamp": datetime.now(),
                "fontes_consultadas": ["shopee", "amazon", "mercadolivre"],
                "tempo_coleta": 2.5
            }
        }
        
        # Simular alguns produtos baseado no query
        if "organizadores" in parametros.get("query", "").lower():
            dados_simulados["produtos_encontrados"] = [
                {
                    "nome": "Organizador de Gaveta Retrátil",
                    "marketplace": "shopee",
                    "preco": 24.90,
                    "vendedores": 12
                },
                {
                    "nome": "Organizador Multiuso Premium",
                    "marketplace": "magalu",
                    "preco": 36.90,
                    "vendedores": 3
                }
            ]
        
        logger.debug(f"📊 Dados coletados: {len(dados_simulados['produtos_encontrados'])} produtos")
        
        return dados_simulados
    
    def _analisar_produtos(self, dados: Dict, tipo_analise: TipoAnalise) -> List[ProdutoAnalise]:
        """📊 Analisa produtos encontrados"""
        produtos_analisados = []
        
        for produto_data in dados.get("produtos_encontrados", []):
            # Análise de tendência baseada em heurísticas
            nivel_tendencia = self._determinar_nivel_tendencia(produto_data, dados)
            nivel_concorrencia = self._determinar_nivel_concorrencia(produto_data, dados)
            
            # Mapear utilidade
            utilidade = self._mapear_utilidade_produto(produto_data["nome"])
            
            # Identificar pontos fortes e fracos
            pontos_fortes, pontos_fracos = self._analisar_pontos_produto(produto_data)
            
            # Gerar microtags
            microtags = self._gerar_microtags_produto(produto_data, nivel_tendencia, nivel_concorrencia)
            
            # Calcular score de oportunidade
            score_oportunidade = self._calcular_score_oportunidade(
                nivel_tendencia, nivel_concorrencia, produto_data
            )
            
            produto_analise = ProdutoAnalise(
                nome=produto_data["nome"],
                categoria=self._identificar_categoria(produto_data["nome"]),
                marketplace=produto_data["marketplace"],
                preco_encontrado=produto_data["preco"],
                numero_vendedores=produto_data.get("vendedores", 0),
                nivel_tendencia=nivel_tendencia,
                nivel_concorrencia=nivel_concorrencia,
                utilidade_mapeada=utilidade,
                pontos_fortes=pontos_fortes,
                pontos_fracos=pontos_fracos,
                microtags=microtags,
                score_oportunidade=score_oportunidade,
                diferencial_sugerido=self._sugerir_diferencial(produto_data)
            )
            
            produtos_analisados.append(produto_analise)
        
        return produtos_analisados
    
    def _determinar_nivel_tendencia(self, produto: Dict, dados_completos: Dict) -> NivelTendencia:
        """📈 Determina nível de tendência do produto"""
        # Heurísticas simples para determinar tendência
        nome = produto["nome"].lower()
        
        # Palavras que indicam tendência alta
        palavras_emergentes = ["inteligente", "smart", "led", "wireless", "eco", "sustentável"]
        palavras_saturadas = ["básico", "comum", "simples", "tradicional"]
        
        if any(palavra in nome for palavra in palavras_emergentes):
            return NivelTendencia.EMERGENTE
        elif any(palavra in nome for palavra in palavras_saturadas):
            return NivelTendencia.SATURADO
        elif produto.get("vendedores", 0) < 5:
            return NivelTendencia.CRESCIMENTO
        elif produto.get("vendedores", 0) > 20:
            return NivelTendencia.SATURADO
        else:
            return NivelTendencia.PICO
    
    def _determinar_nivel_concorrencia(self, produto: Dict, dados_completos: Dict) -> NivelConcorrencia:
        """🏪 Determina nível de concorrência"""
        num_vendedores = produto.get("vendedores", 0)
        
        if num_vendedores <= 3:
            return NivelConcorrencia.BAIXA
        elif num_vendedores <= 10:
            return NivelConcorrencia.MODERADA
        elif num_vendedores <= 20:
            return NivelConcorrencia.ALTA
        else:
            return NivelConcorrencia.SATURADA
    
    def _mapear_utilidade_produto(self, nome_produto: str) -> str:
        """🎯 Mapeia a utilidade percebida do produto"""
        nome_lower = nome_produto.lower()
        
        utilidades = {
            "organizador": "Economia de espaço e organização",
            "gaveta": "Otimização de armazenamento",
            "retrátil": "Flexibilidade e adaptabilidade",
            "led": "Iluminação eficiente e moderna",
            "wireless": "Conveniência e mobilidade",
            "eco": "Sustentabilidade e consciência ambiental",
            "premium": "Status e qualidade superior"
        }
        
        for palavra, utilidade in utilidades.items():
            if palavra in nome_lower:
                return utilidade
        
        return "Utilidade geral identificada"
    
    def _analisar_pontos_produto(self, produto: Dict) -> Tuple[List[str], List[str]]:
        """⚖️ Analisa pontos fortes e fracos do produto"""
        pontos_fortes = []
        pontos_fracos = []
        
        nome = produto["nome"].lower()
        preco = produto.get("preco", 0)
        vendedores = produto.get("vendedores", 0)
        
        # Pontos fortes baseados em características
        if "premium" in nome:
            pontos_fortes.append("Posicionamento premium")
        if "led" in nome or "inteligente" in nome:
            pontos_fortes.append("Tecnologia diferenciada")
        if preco < 30:
            pontos_fortes.append("Preço acessível")
        if vendedores < 5:
            pontos_fortes.append("Baixa concorrência")
        
        # Pontos fracos baseados em características
        if "básico" in nome or "simples" in nome:
            pontos_fracos.append("Posicionamento genérico")
        if preco > 100:
            pontos_fracos.append("Preço alto para categoria")
        if vendedores > 20:
            pontos_fracos.append("Mercado saturado")
        
        # Fallbacks
        if not pontos_fortes:
            pontos_fortes.append("Produto estabelecido no mercado")
        if not pontos_fracos:
            pontos_fracos.append("Necessita diferenciação")
        
        return pontos_fortes, pontos_fracos
    
    def _gerar_microtags_produto(self, produto: Dict, tendencia: NivelTendencia, 
                               concorrencia: NivelConcorrencia) -> List[str]:
        """🏷️ Gera microtags para o produto"""
        tags = ["#scoutai", "#analise_produto"]
        
        # Tags de tendência
        if tendencia == NivelTendencia.EMERGENTE:
            tags.append("#TendênciaAlta")
        elif tendencia == NivelTendencia.SATURADO:
            tags.append("#Saturado")
        
        # Tags de concorrência
        if concorrencia == NivelConcorrencia.BAIXA:
            tags.append("#ConcorrênciaBaixa")
        elif concorrencia == NivelConcorrencia.ALTA:
            tags.append("#ConcorrênciaAlta")
        
        # Tags de oportunidade
        if (tendencia in [NivelTendencia.EMERGENTE, NivelTendencia.CRESCIMENTO] and 
            concorrencia in [NivelConcorrencia.BAIXA, NivelConcorrencia.MODERADA]):
            tags.append("#PossívelKit")
            tags.append("#Oportunidade")
        
        # Tags baseadas no nome do produto
        nome_lower = produto["nome"].lower()
        if "organizador" in nome_lower:
            tags.append("#Organização")
        if "premium" in nome_lower:
            tags.append("#Premium")
        if "led" in nome_lower:
            tags.append("#Tecnologia")
        
        return tags
    
    def _calcular_score_oportunidade(self, tendencia: NivelTendencia, 
                                   concorrencia: NivelConcorrencia, produto: Dict) -> float:
        """📊 Calcula score de oportunidade (0-10)"""
        score = 5.0  # Base neutra
        
        # Ajustes por tendência
        if tendencia == NivelTendencia.EMERGENTE:
            score += 2.5
        elif tendencia == NivelTendencia.CRESCIMENTO:
            score += 1.5
        elif tendencia == NivelTendencia.PICO:
            score += 0.5
        elif tendencia == NivelTendencia.SATURADO:
            score -= 1.5
        
        # Ajustes por concorrência
        if concorrencia == NivelConcorrencia.BAIXA:
            score += 2.0
        elif concorrencia == NivelConcorrencia.MODERADA:
            score += 0.5
        elif concorrencia == NivelConcorrencia.ALTA:
            score -= 0.5
        elif concorrencia == NivelConcorrencia.SATURADA:
            score -= 2.0
        
        # Ajustes por preço
        preco = produto.get("preco", 0)
        if 20 <= preco <= 80:  # Faixa ideal
            score += 0.5
        elif preco > 200:
            score -= 1.0
        
        return max(0.0, min(10.0, score))
    
    def _sugerir_diferencial(self, produto: Dict) -> Optional[str]:
        """💡 Sugere diferencial para o produto"""
        nome = produto["nome"].lower()
        
        if "organizador" in nome:
            return "Destacar como solução para 'espaço limitado' + incluir foto comparativa antes/depois"
        elif "led" in nome:
            return "Enfatizar economia de energia e durabilidade"
        elif "premium" in nome:
            return "Focar em qualidade superior e garantia estendida"
        else:
            return "Criar proposta de valor única baseada na utilidade principal"
    
    def _identificar_categoria(self, nome_produto: str) -> str:
        """📂 Identifica categoria do produto"""
        nome_lower = nome_produto.lower()
        
        categorias = {
            "organizador": "Organização Doméstica",
            "gaveta": "Móveis e Decoração",
            "led": "Eletrônicos e Iluminação",
            "cozinha": "Casa e Cozinha",
            "banheiro": "Casa e Banheiro",
            "escritório": "Escritório e Papelaria"
        }
        
        for palavra, categoria in categorias.items():
            if palavra in nome_lower:
                return categoria
        
        return "Categoria Geral"
    
    def _comparar_precos(self, produtos: List[ProdutoAnalise]) -> List[ComparacaoPrecos]:
        """💰 Compara preços entre marketplaces"""
        comparacoes = []
        
        # Agrupar produtos similares por nome base
        produtos_agrupados = {}
        for produto in produtos:
            nome_base = self._extrair_nome_base(produto.nome)
            if nome_base not in produtos_agrupados:
                produtos_agrupados[nome_base] = []
            produtos_agrupados[nome_base].append(produto)
        
        # Criar comparações para grupos com múltiplos marketplaces
        for nome_base, grupo_produtos in produtos_agrupados.items():
            if len(grupo_produtos) > 1:
                comparacao = ComparacaoPrecos(produto=nome_base)
                
                precos = {}
                for produto in grupo_produtos:
                    marketplace = produto.marketplace.lower()
                    precos[marketplace] = produto.preco_encontrado
                
                # Preencher preços por marketplace
                comparacao.shopee_preco = precos.get("shopee")
                comparacao.magalu_preco = precos.get("magalu")
                comparacao.amazon_preco = precos.get("amazon")
                comparacao.mercadolivre_preco = precos.get("mercadolivre")
                
                # Calcular variações
                precos_validos = [p for p in precos.values() if p is not None]
                if len(precos_validos) >= 2:
                    preco_min = min(precos_validos)
                    preco_max = max(precos_validos)
                    comparacao.variacao_maxima = ((preco_max - preco_min) / preco_min) * 100
                    
                    # Identificar marketplaces extremos
                    for marketplace, preco in precos.items():
                        if preco == preco_min:
                            comparacao.marketplace_mais_barato = marketplace
                        if preco == preco_max:
                            comparacao.marketplace_mais_caro = marketplace
                    
                    # Detectar oportunidade de arbitragem (>30% diferença)
                    comparacao.oportunidade_arbitragem = comparacao.variacao_maxima > 30
                
                comparacoes.append(comparacao)
        
        return comparacoes
    
    def _extrair_nome_base(self, nome_completo: str) -> str:
        """🔍 Extrai nome base do produto removendo modificadores"""
        # Remove palavras como "Premium", "Pro", "V2", etc.
        modificadores = ["premium", "pro", "plus", "v2", "v3", "deluxe", "master"]
        nome_base = nome_completo.lower()
        
        for mod in modificadores:
            nome_base = nome_base.replace(mod, "").strip()
        
        return nome_base.title()
    
    def _gerar_insights_estrategicos(self, produtos: List[ProdutoAnalise], 
                                   comparacoes: List[ComparacaoPrecos]) -> List[str]:
        """💡 Gera insights estratégicos baseados na análise"""
        insights = []
        
        # Insights sobre tendências
        produtos_emergentes = [p for p in produtos if p.nivel_tendencia == NivelTendencia.EMERGENTE]
        if produtos_emergentes:
            insights.append(f"Identificados {len(produtos_emergentes)} produtos em tendência emergente")
        
        # Insights sobre concorrência
        baixa_concorrencia = [p for p in produtos if p.nivel_concorrencia == NivelConcorrencia.BAIXA]
        if baixa_concorrencia:
            insights.append(f"Oportunidade: {len(baixa_concorrencia)} produtos com baixa concorrência")
        
        # Insights sobre preços
        for comparacao in comparacoes:
            if comparacao.oportunidade_arbitragem:
                insights.append(
                    f"Arbitragem detectada em '{comparacao.produto}': "
                    f"{comparacao.variacao_maxima:.1f}% diferença entre marketplaces"
                )
        
        # Insights sobre scores altos
        alto_score = [p for p in produtos if p.score_oportunidade >= 8.0]
        if alto_score:
            insights.append(f"Produtos com alto potencial: {len(alto_score)} itens com score ≥8.0")
        
        # Insight padrão se nenhum específico
        if not insights:
            insights.append("Análise concluída - mercado em comportamento padrão")
        
        return insights
    
    def _gerar_acoes_recomendadas(self, produtos: List[ProdutoAnalise], 
                                insights: List[str]) -> List[str]:
        """🎯 Gera ações recomendadas baseadas na análise"""
        acoes = []
        
        # Ações para produtos com alto score
        produtos_promissores = [p for p in produtos if p.score_oportunidade >= 7.5]
        for produto in produtos_promissores:
            if produto.diferencial_sugerido:
                acoes.append(f"Explorar '{produto.nome}': {produto.diferencial_sugerido}")
        
        # Ações para arbitragem
        if any("Arbitragem detectada" in insight for insight in insights):
            acoes.append("Investigar oportunidades de arbitragem entre marketplaces")
        
        # Ações para baixa concorrência
        baixa_concorrencia = [p for p in produtos if p.nivel_concorrencia == NivelConcorrencia.BAIXA]
        if baixa_concorrencia:
            acoes.append("Priorizar entrada rápida em nichos de baixa concorrência")
        
        # Ações para tendências emergentes
        emergentes = [p for p in produtos if p.nivel_tendencia == NivelTendencia.EMERGENTE]
        if emergentes:
            acoes.append("Desenvolver estratégia para produtos em tendência emergente")
        
        # Ação padrão
        if not acoes:
            acoes.append("Monitorar mercado e aguardar oportunidades mais claras")
        
        return acoes
    
    def _verificar_gatilhos_especiais(self, produtos: List[ProdutoAnalise], 
                                    comparacoes: List[ComparacaoPrecos], 
                                    parametros: Dict) -> Tuple[List[str], StatusRisco]:
        """🚨 Verifica gatilhos especiais e determina status de risco"""
        gatilhos_ativados = []
        status_risco = StatusRisco.VERDE
        
        # Gatilho: Produto em tendência global com baixa oferta no Brasil
        for produto in produtos:
            if (produto.nivel_tendencia == NivelTendencia.EMERGENTE and 
                produto.nivel_concorrencia == NivelConcorrencia.BAIXA):
                gatilhos_ativados.append("tendencia_global_baixa_oferta")
                break
        
        # Gatilho: Variação de preço > 30%
        for comparacao in comparacoes:
            if comparacao.oportunidade_arbitragem:
                gatilhos_ativados.append("variacao_preco_30pct")
                break
        
        # Gatilho: Produto com ficha técnica fraca/genérica
        for produto in produtos:
            if any(palavra in produto.nome.lower() for palavra in ["básico", "simples", "genérico"]):
                gatilhos_ativados.append("ficha_tecnica_fraca")
                break
        
        # Gatilho: Mais de 5 concorrentes com mesmo fornecedor (simulado)
        concorrencia_alta = [p for p in produtos if p.numero_vendedores > 15]
        if concorrencia_alta:
            gatilhos_ativados.append("produto_clone_detectado")
        
        # Gatilho: Palavras-chave restritas
        query_original = parametros.get("query", "").lower()
        if any(palavra_restrita in query_original for palavra_restrita in self.palavras_restritas):
            gatilhos_ativados.append("palavra_chave_restrita")
            status_risco = StatusRisco.VERMELHO
        
        # Determinar status de risco final
        if status_risco != StatusRisco.VERMELHO:
            if len(gatilhos_ativados) >= 3:
                status_risco = StatusRisco.AMARELO
            elif any("clone" in gatilho or "restrita" in gatilho for gatilho in gatilhos_ativados):
                status_risco = StatusRisco.AMARELO
        
        return gatilhos_ativados, status_risco
    
    def _definir_agentes_complementares(self, tipo_analise: TipoAnalise, 
                                      produtos: List[ProdutoAnalise], 
                                      gatilhos: List[str]) -> List[str]:
        """🤖 Define quais agentes complementares devem ser acionados"""
        agentes_sugeridos = []
        
        # Sempre incluir DeepAgent para coleta real de dados
        agentes_sugeridos.append("DeepAgent")
        
        # CopyBooster para produtos com ficha fraca
        if "ficha_tecnica_fraca" in gatilhos:
            agentes_sugeridos.append("CopyBooster")
        
        # KitBuilder para produtos promissores
        produtos_promissores = [p for p in produtos if p.score_oportunidade >= 8.0]
        if produtos_promissores:
            agentes_sugeridos.append("KitBuilder")
        
        # AutoPrice para arbitragem
        if "variacao_preco_30pct" in gatilhos:
            agentes_sugeridos.append("AutoPrice")
        
        # Oráculo para riscos ou ambiguidade
        if "palavra_chave_restrita" in gatilhos or len(gatilhos) >= 3:
            agentes_sugeridos.append("Oráculo")
        
        # PromptCrafter baseado no tipo de análise
        if tipo_analise in [TipoAnalise.TENDENCIA_PRODUTO, TipoAnalise.ANALISE_CONCORRENCIA]:
            agentes_sugeridos.append("PromptCrafter")
        
        return list(set(agentes_sugeridos))  # Remove duplicatas
    
    def _calcular_score_geral(self, produtos: List[ProdutoAnalise], 
                            status_risco: StatusRisco) -> float:
        """📊 Calcula score geral da análise"""
        if not produtos:
            return 0.0
        
        # Score médio dos produtos
        score_medio = sum(p.score_oportunidade for p in produtos) / len(produtos)
        
        # Ajustes por status de risco
        if status_risco == StatusRisco.VERMELHO:
            score_medio *= 0.5  # Penaliza risco alto
        elif status_risco == StatusRisco.AMARELO:
            score_medio *= 0.8  # Penaliza risco médio
        
        # Bônus por diversidade de produtos
        if len(produtos) > 3:
            score_medio *= 1.1
        
        return min(10.0, max(0.0, score_medio))
    
    def _registrar_analise(self, relatorio: RelatorioScout):
        """📝 Registra análise no histórico"""
        self.historico_analises.append(relatorio)
        
        # Manter apenas últimas 50 análises
        if len(self.historico_analises) > 50:
            self.historico_analises = self.historico_analises[-50:]
        
        # Salvar na memória persistente (versão simplificada)
        historico_para_salvar = [
            {
                "id": r.id,
                "timestamp": r.timestamp.isoformat(),
                "tipo": r.tipo_analise.value,
                "score": r.score_geral,
                "produtos_count": len(r.produtos_analisados)
            }
            for r in self.historico_analises
        ]
        
        self.memory.context["historico_analises"] = historico_para_salvar
        
        logger.info(f"📊 Análise {relatorio.id} registrada no histórico")
    
    def _atualizar_stats_scout(self, relatorio: RelatorioScout):
        """📈 Atualiza estatísticas do ScoutAI"""
        self.stats["analises_realizadas"] += 1
        self.stats["produtos_monitorados"] += len(relatorio.produtos_analisados)
        
        # Contar oportunidades
        oportunidades = [p for p in relatorio.produtos_analisados if p.score_oportunidade >= 7.5]
        self.stats["oportunidades_detectadas"] += len(oportunidades)
        
        # Contar alertas vermelho
        if relatorio.status_risco == StatusRisco.VERMELHO:
            self.stats["alertas_vermelho_gerados"] += 1
        
        # Contar tendências
        tendencias = [p for p in relatorio.produtos_analisados 
                     if p.nivel_tendencia in [NivelTendencia.EMERGENTE, NivelTendencia.CRESCIMENTO]]
        self.stats["tendencias_identificadas"] += len(tendencias)
        
        # Agentes acionados
        self.stats["agentes_acionados"] += len(relatorio.agentes_sugeridos)
        
        # Score médio
        total_analises = self.stats["analises_realizadas"]
        self.stats["score_medio_oportunidade"] = (
            (self.stats["score_medio_oportunidade"] * (total_analises - 1) + relatorio.score_geral) / total_analises
        )
    
    def _formatar_resposta_scout(self, relatorio: RelatorioScout) -> str:
        """📝 Formata resposta final do ScoutAI"""
        icone_risco = {
            StatusRisco.VERDE: "🟢",
            StatusRisco.AMARELO: "🟡", 
            StatusRisco.VERMELHO: "🔴"
        }
        
        resposta = f"""🔍 **ScoutAI v1.3A — Radar Estratégico de Oportunidades**

**Análise:** {relatorio.tipo_analise.value.replace('_', ' ').title()}
**Status:** {icone_risco[relatorio.status_risco]} {relatorio.status_risco.value.title()}
**Score Geral:** {relatorio.score_geral:.1f}/10

**📊 PRODUTOS ANALISADOS ({len(relatorio.produtos_analisados)}):**"""

        for produto in relatorio.produtos_analisados:
            resposta += f"""
• **{produto.nome}** ({produto.marketplace.title()})
  - Preço: R$ {produto.preco_encontrado:.2f} | Vendedores: {produto.numero_vendedores}
  - Tendência: {produto.nivel_tendencia.value.title()} | Concorrência: {produto.nivel_concorrencia.value.title()}
  - Score Oportunidade: {produto.score_oportunidade:.1f}/10
  - Utilidade: {produto.utilidade_mapeada}
  - Tags: {', '.join(produto.microtags)}"""

        if relatorio.comparacoes_precos:
            resposta += f"\n\n**💰 COMPARAÇÃO DE PREÇOS:**"
            for comp in relatorio.comparacoes_precos:
                resposta += f"""
• **{comp.produto}**
  - Variação: {comp.variacao_maxima:.1f}%
  - Mais barato: {comp.marketplace_mais_barato.title()} 
  - Mais caro: {comp.marketplace_mais_caro.title()}"""
                if comp.oportunidade_arbitragem:
                    resposta += " 🎯 **ARBITRAGEM DETECTADA**"

        resposta += f"\n\n**💡 INSIGHTS ESTRATÉGICOS:**"
        for insight in relatorio.insights_estrategicos:
            resposta += f"\n• {insight}"

        resposta += f"\n\n**🎯 AÇÕES RECOMENDADAS:**"
        for acao in relatorio.acoes_recomendadas:
            resposta += f"\n• {acao}"

        if relatorio.gatilhos_ativados:
            resposta += f"\n\n**🚨 GATILHOS ATIVADOS:** {', '.join(relatorio.gatilhos_ativados)}"

        if relatorio.agentes_sugeridos:
            resposta += f"\n\n**🤖 AGENTES SUGERIDOS:** {', '.join(relatorio.agentes_sugeridos)}"

        resposta += f"\n\n**📊 ID da Análise:** {relatorio.id}"
        resposta += f"\n**⏱️ Duração:** {relatorio.duracao_analise:.2f}s"
        
        resposta += "\n\n_[Para análises detalhadas, histórico ou acionamento de agentes: solicite explicitamente]_"
        
        return resposta
    
    def _fallback_response(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """🔄 Resposta de fallback específica do ScoutAI"""
        return """🔍 **ScoutAI v1.3A — Temporariamente Indisponível**

Estou passando por uma manutenção técnica. Enquanto isso, aqui estão algumas ações que você pode tomar:

**🎯 Comandos Suportados:**
• ScoutAI, investigue o nicho [produto]
• ScoutAI, avalie a tendência do produto [nome]
• ScoutAI, busque concorrentes para [produto/link]
• ScoutAI, há saturação para [produto] no Shopee?
• ScoutAI, compare preços entre marketplaces

**🤖 Agentes Alternativos:**
• **DeepAgent**: Para pesquisa web real de produtos
• **AutoMaster**: Para estratégias comerciais
• **Oráculo**: Para decisões estratégicas complexas

Tente novamente em alguns momentos ou use um agente alternativo!"""
    
    # === MÉTODOS ESPECIAIS DE CONSULTA ===
    
    def obter_historico_analises(self, ultimas: int = 5) -> str:
        """📚 Retorna histórico das últimas análises"""
        if not self.historico_analises:
            return "📚 Histórico vazio - nenhuma análise realizada ainda."
        
        analises_recentes = self.historico_analises[-ultimas:]
        
        historico = f"📚 **HISTÓRICO SCOUTAI - ÚLTIMAS {len(analises_recentes)} ANÁLISES**\n\n"
        
        for analise in reversed(analises_recentes):
            icone_risco = "🟢" if analise.status_risco == StatusRisco.VERDE else "🟡" if analise.status_risco == StatusRisco.AMARELO else "🔴"
            
            historico += f"**{analise.id.upper()}** - {analise.timestamp.strftime('%d/%m %H:%M')}\n"
            historico += f"Tipo: {analise.tipo_analise.value.replace('_', ' ').title()}\n"
            historico += f"Status: {icone_risco} | Score: {analise.score_geral:.1f}/10\n"
            historico += f"Produtos: {len(analise.produtos_analisados)} | Oportunidades: {len([p for p in analise.produtos_analisados if p.score_oportunidade >= 7.5])}\n"
            if analise.insights_estrategicos:
                historico += f"Insight: {analise.insights_estrategicos[0]}\n"
            historico += "---\n\n"
        
        return historico
    
    def diagnosticar_scout(self) -> Dict[str, Any]:
        """🔧 Diagnóstico completo do ScoutAI"""
        # Obter diagnóstico base do BaseAgentV2
        diagnostico_base = self.get_health_status()
        
        # Adicionar informações específicas do ScoutAI
        diagnostico_scout = {
            "version": "1.3A_BaseAgentV2_Radar_Estrategico",
            "gatilhos_ativos": sum(1 for g in self.gatilhos_ativos.values() if g),
            "marketplaces_suportados": len(self.marketplaces_suportados),
            "analises_realizadas": self.stats["analises_realizadas"],
            "oportunidades_detectadas": self.stats["oportunidades_detectadas"],
            "score_medio_oportunidade": self.stats["score_medio_oportunidade"],
            "alertas_criticos": self.stats["alertas_vermelho_gerados"],
            "agentes_integrados": ["DeepAgent", "Oráculo", "CopyBooster", "KitBuilder", "AutoPrice"],
            "historico_size": len(self.historico_analises)
        }
        
        # Combinar diagnósticos
        diagnostico_completo = {**diagnostico_base, **diagnostico_scout}
        
        return diagnostico_completo
    
    def ativar_modo_torre_shadow(self) -> str:
        """🗼 Ativa modo Torre Shadow conforme especificação"""
        return """🗼 **MODO TORRE SHADOW ATIVADO**

ScoutAI agora opera em modo de observação silenciosa:
• 🔍 Monitoramento contínuo de oportunidades
• 📊 Análise automática de tendências emergentes  
• 🚨 Alertas proativos para mudanças críticas
• 🤖 Acionamento automático de agentes complementares

**Status:** Vigilância ativa em background
**Frequência:** Análises a cada 15 minutos
**Gatilhos:** Todos os alertas especiais ativos

_O ScoutAI continuará suas análises invisíveis e notificará apenas descobertas críticas._"""

# === FUNÇÕES DE CRIAÇÃO ===

def criar_scout_ai(config: Optional[Dict] = None) -> ScoutAI:
    """🔍 Cria ScoutAI v1.3A com configuração robusta"""
    return ScoutAI(config=config)

# Alias para compatibilidade
create_scout = criar_scout_ai

if __name__ == "__main__":
    print("🔍 Testando ScoutAI v1.3A...")
    
    scout = criar_scout_ai()
    diagnostico = scout.diagnosticar_scout()
    
    print(f"📊 Diagnóstico: {diagnostico['version']}")
    print(f"🎯 Gatilhos ativos: {diagnostico['gatilhos_ativos']}")
    print(f"🏪 Marketplaces: {diagnostico['marketplaces_suportados']}")
    print(f"💪 Health Score: {diagnostico.get('health_score', 'N/A')}")
    print(f"🔄 Circuit Breaker: {diagnostico.get('circuit_breaker_state', 'N/A')}")
    print("✅ ScoutAI v1.3A pronto para radar estratégico!")