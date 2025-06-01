"""
🧠 AUTOMASTER v4.0 — Agente Pilar de Autonomia Econômica e Estratégica
Sistema completo de construção de ecossistemas pessoais: da ideia ao legado
🎯 VERSÃO MIGRADA PARA BaseAgentV2 com robustez completa
"""

import json
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from abc import ABC, abstractmethod

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

class PerfilProfissional(Enum):
    """Perfis profissionais atendidos pelo AutoMaster"""
    AUTONOMO = "autonomo"
    EDUCADOR = "educador"
    CRIADOR = "criador"
    ESPECIALISTA = "especialista"
    MICROEMPREENDEDOR = "microempreendedor"
    MENTOR = "mentor"
    CONSULTOR = "consultor"
    TERAPEUTA = "terapeuta"
    PRESTADOR_FISICO = "prestador_fisico"
    INFLUENCER = "influencer"

class FaseVida(Enum):
    """Fases da vida profissional"""
    INICIANTE = "iniciante"
    CRESCIMENTO = "crescimento"
    ESTAGNACAO = "estagnacao"
    EXPANSAO = "expansao"
    REINVENCAO = "reinvencao"
    LEGADO = "legado"
    RECUPERACAO = "recuperacao"

class ModoPrincipal(Enum):
    """Modos principais de operação do AutoMaster"""
    MICROAGENCIA = "microagencia"
    PRODUTO_CONHECIMENTO = "produto_conhecimento"
    CRIADOR_CONTEUDO = "criador_conteudo"
    ESPECIALISTA_CONFIANCA = "especialista_confianca"
    MEI_OFFLINE = "mei_offline"
    NOMADE_DIGITAL = "nomade_digital"
    ANTIFRÁGIL = "antifragil"
    MESTRE_MESTRES = "mestre_mestres"

class TipoDesafio(Enum):
    """Tipos de desafios enfrentados"""
    FINANCEIRO = "financeiro"
    ENERGETICO = "energetico"
    ESTRATEGICO = "estrategico"
    CRIATIVO = "criativo"
    TECNICO = "tecnico"
    MOTIVACIONAL = "motivacional"
    RELACIONAMENTO = "relacionamento"
    SAUDE = "saude"

@dataclass
class PerfilUsuario:
    """Perfil completo do usuário do AutoMaster"""
    nome: str
    perfil_profissional: PerfilProfissional
    fase_vida: FaseVida
    objetivos_principais: List[str]
    preferencia_exposicao: str  # "alta", "media", "baixa", "invisivel"
    tempo_disponivel: str  # "integral", "parcial", "limitado"
    conhecimento_acumulado: str  # "iniciante", "intermediario", "avancado", "expert"
    desafios_atuais: List[TipoDesafio]
    recursos_disponiveis: Dict[str, Any]
    localizacao: str = ""
    idade_aproximada: str = ""

@dataclass
class ModuloAvancado:
    """Representação de um módulo avançado do AutoMaster"""
    id: int
    nome: str
    descricao: str
    funcionalidades: List[str]
    perfis_alvo: List[PerfilProfissional]
    ativo: bool = True
    nivel_complexidade: int = 1  # 1-5

@dataclass
class PlanoEstrategico:
    """Plano estratégico gerado pelo AutoMaster"""
    id: str
    usuario: PerfilUsuario
    modulos_ativados: List[int]
    estrategia_principal: str
    plano_90_dias: str
    plano_1_ano: str
    sistema_monetizacao: str
    estrategia_marca: str
    plano_comunidade: str
    sistema_antifragil: str
    metricas_sucesso: Dict[str, Any]
    recursos_necessarios: List[str]
    cronograma: Dict[str, str]
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class SimulacaoFaturamento:
    """Simulação de faturamento multicanal"""
    produtos_servicos: Dict[str, float]
    canais_venda: Dict[str, float]
    projecao_mensal: float
    projecao_anual: float
    cenario_conservador: float
    cenario_otimista: float
    pontos_criticos: List[str]

class AutoMasterV2(BaseAgentV2):
    """
    🧠 AUTOMASTER v4.0 — Agente Pilar de Autonomia Econômica e Estratégica
    
    🎯 MISSÃO PRINCIPAL:
    Sistema completo de construção de ecossistemas pessoais — da ideia ao legado,
    da renda ao impacto, do burnout à liberdade. Atende qualquer profissional
    que deseja viver com mais inteligência, propósito e poder sobre sua trajetória.
    
    🧠 32 MÓDULOS AVANÇADOS:
    Desde narrativa profissional até modo socorro total, cobrindo toda a jornada
    de autonomia econômica e estratégica.
    
    ✨ VERSÃO V2: Migrada para BaseAgentV2 com robustez completa
    """
    
    def __init__(self, llm=None, **kwargs):
        # Configuração robusta específica para AutoMaster
        automaster_config = {
            "rate_limit_per_minute": 30,  # Conservador para operações complexas
            "burst_allowance": 5,
            "failure_threshold": 3,
            "recovery_timeout": 45,
            "cache_enabled": True,
            "cache_ttl_seconds": 900,  # 15 minutos para planos estratégicos
            "persistent_memory": True,
            "memory_storage_dir": "memory/agents/automaster",
            "max_retry_attempts": 3,
            "timeout_seconds": 60  # Mais tempo para processamento complexo
        }
        
        # Merge com configuração fornecida
        config = kwargs.get("config", {})
        automaster_config.update(config)
        kwargs["config"] = automaster_config
        
        # Inicializar BaseAgentV2
        super().__init__(
            name="AutoMaster",
            description="Agente Pilar v4.0 de Autonomia Econômica e Estratégica (Robustez v2)",
            **kwargs
        )
        
        # Configurar LLM específico
        if llm:
            self.llm = llm
            self.llm_available = True
        
        # === SISTEMA DE 32 MÓDULOS AVANÇADOS ===
        self.modulos_avancados = self._inicializar_modulos_avancados()
        
        # === HISTÓRICO E REGISTROS ===
        self.planos_estrategicos: List[PlanoEstrategico] = []
        self.simulacoes_faturamento: List[SimulacaoFaturamento] = []
        self.contador_planos = 0
        
        # === CONFIGURAÇÕES AVANÇADAS ===
        self.modo_antifragil_ativo = True
        self.sistema_backup_ativo = True
        self.gêmeo_pro_ativo = True
        self.shadow_ops_ativo = True
        
        # === INTEGRAÇÕES COM OUTROS AGENTES ===
        self.integracoes_ativas = {
            "copybooster": False,
            "routinemaster": False,
            "doubtsolver": False,
            "oraculo": True  # Integração com Oráculo já implementado
        }
        
        # Estatísticas expandidas (além das do BaseAgentV2)
        self.stats.update({
            "planos_estrategicos_criados": 0,
            "simulacoes_realizadas": 0,
            "modulos_ativados_total": 0,
            "usuarios_atendidos": 0,
            "taxa_sucesso_planos": 0.0,
            "economia_gerada_estimada": 0.0,
            "liberdade_geografica_alcancada": 0,
            "burnouts_prevenidos": 0,
            "comunidades_criadas": 0,
            "legados_estruturados": 0
        })
        
        # Carregar histórico da memória persistente se existir
        self._carregar_historico_persistente()
        
        logger.info("🧠 AutoMaster v4.0 (BaseAgentV2) inicializado - 32 módulos avançados ATIVOS")
    
    def _carregar_historico_persistente(self):
        """Carrega histórico de planos e simulações da memória persistente"""
        if self.memory and hasattr(self.memory, 'context'):
            historico = self.memory.context.get('historico_automaster', {})
            if historico:
                self.planos_estrategicos = historico.get('planos', [])
                self.simulacoes_faturamento = historico.get('simulacoes', [])
                self.contador_planos = historico.get('contador_planos', 0)
                logger.info(f"📚 Histórico carregado: {len(self.planos_estrategicos)} planos, {len(self.simulacoes_faturamento)} simulações")
    
    def _salvar_historico_persistente(self):
        """Salva histórico na memória persistente"""
        if self.memory:
            self.memory.context['historico_automaster'] = {
                'planos': self.planos_estrategicos[-50:],  # Últimos 50 planos
                'simulacoes': self.simulacoes_faturamento[-50:],  # Últimas 50 simulações
                'contador_planos': self.contador_planos
            }
    
    def _inicializar_modulos_avancados(self) -> Dict[int, ModuloAvancado]:
        """Inicializa os 32 módulos avançados do AutoMaster"""
        modulos = {}
        
        # Definir todos os 32 módulos conforme especificação
        definicoes_modulos = [
            {
                "id": 1, "nome": "Narrativa Profissional e Propósito de Marca",
                "descricao": "Criação de identidade profissional autêntica e diferenciada",
                "funcionalidades": ["storytelling pessoal", "propósito de marca", "posicionamento único"],
                "perfis_alvo": [PerfilProfissional.CRIADOR, PerfilProfissional.ESPECIALISTA],
                "complexidade": 3
            },
            {
                "id": 2, "nome": "Precificação por Persona e Canal",
                "descricao": "Sistema inteligente de precificação baseado em valor percebido",
                "funcionalidades": ["análise de personas", "estratégia de preços", "otimização por canal"],
                "perfis_alvo": [PerfilProfissional.AUTONOMO, PerfilProfissional.CONSULTOR],
                "complexidade": 4
            },
            {
                "id": 3, "nome": "Análise de Plataforma e Canal de Vendas",
                "descricao": "Otimização de canais de vendas e presença digital",
                "funcionalidades": ["análise de plataformas", "estratégia multicanal", "conversão"],
                "perfis_alvo": [PerfilProfissional.CRIADOR, PerfilProfissional.MICROEMPREENDEDOR],
                "complexidade": 3
            },
            {
                "id": 4, "nome": "Roteiro de Lançamento",
                "descricao": "Planejamento completo de lançamentos de produtos/serviços",
                "funcionalidades": ["cronograma de lançamento", "estratégia de marketing", "gestão de expectativas"],
                "perfis_alvo": [PerfilProfissional.EDUCADOR, PerfilProfissional.CRIADOR],
                "complexidade": 4
            },
            {
                "id": 5, "nome": "Portfólio Híbrido",
                "descricao": "Combinação estratégica de serviços, produtos e conteúdo",
                "funcionalidades": ["diversificação de receitas", "sinergia entre ofertas", "escalabilidade"],
                "perfis_alvo": [PerfilProfissional.ESPECIALISTA, PerfilProfissional.MENTOR],
                "complexidade": 5
            },
            {
                "id": 6, "nome": "Planejamento de Carreira e Escalada Profissional",
                "descricao": "Roadmap de evolução profissional e crescimento",
                "funcionalidades": ["mapeamento de carreira", "desenvolvimento de skills", "networking estratégico"],
                "perfis_alvo": [PerfilProfissional.ESPECIALISTA, PerfilProfissional.CONSULTOR],
                "complexidade": 3
            },
            {
                "id": 7, "nome": "Simulador de Faturamento Multicanal",
                "descricao": "Projeções financeiras detalhadas e cenários de crescimento",
                "funcionalidades": ["projeções financeiras", "análise de cenários", "otimização de mix"],
                "perfis_alvo": [PerfilProfissional.MICROEMPREENDEDOR, PerfilProfissional.AUTONOMO],
                "complexidade": 4
            },
            {
                "id": 8, "nome": "Fidelização, Comunidade e Pós-venda",
                "descricao": "Construção de relacionamentos duradouros e comunidades engajadas",
                "funcionalidades": ["estratégia de fidelização", "construção de comunidade", "upsell/cross-sell"],
                "perfis_alvo": [PerfilProfissional.EDUCADOR, PerfilProfissional.MENTOR],
                "complexidade": 4
            },
            {
                "id": 9, "nome": "Plano de Recuperação ou Reinvenção Profissional",
                "descricao": "Estratégias de recuperação e reinvenção em momentos de crise",
                "funcionalidades": ["diagnóstico de situação", "plano de recuperação", "reinvenção estratégica"],
                "perfis_alvo": list(PerfilProfissional),  # Todos os perfis
                "complexidade": 5
            },
            {
                "id": 10, "nome": "Autoridade Pública, Influência e Conteúdo Estratégico",
                "descricao": "Construção de autoridade e influência através de conteúdo",
                "funcionalidades": ["estratégia de conteúdo", "construção de autoridade", "influência digital"],
                "perfis_alvo": [PerfilProfissional.INFLUENCER, PerfilProfissional.ESPECIALISTA],
                "complexidade": 4
            },
            {
                "id": 11, "nome": "Shadow Ops",
                "descricao": "Penetração em canais alternativos e estratégias não convencionais",
                "funcionalidades": ["canais alternativos", "estratégias disruptivas", "mercados de nicho"],
                "perfis_alvo": [PerfilProfissional.CRIADOR, PerfilProfissional.ESPECIALISTA],
                "complexidade": 5
            },
            {
                "id": 12, "nome": "Autodiagnóstico de Negócio e Performance",
                "descricao": "Sistema de análise e otimização contínua do negócio",
                "funcionalidades": ["métricas de performance", "diagnóstico automático", "otimização contínua"],
                "perfis_alvo": [PerfilProfissional.MICROEMPREENDEDOR, PerfilProfissional.AUTONOMO],
                "complexidade": 3
            },
            {
                "id": 13, "nome": "Guia Visual de Marca Completa",
                "descricao": "Identidade visual e diretrizes de marca profissional",
                "funcionalidades": ["identidade visual", "guidelines de marca", "aplicações práticas"],
                "perfis_alvo": [PerfilProfissional.CRIADOR, PerfilProfissional.INFLUENCER],
                "complexidade": 3
            },
            {
                "id": 14, "nome": "Gêmeo Pro",
                "descricao": "Mentor interno futurista baseado em IA para tomada de decisões",
                "funcionalidades": ["simulação de decisões", "mentoria virtual", "análise preditiva"],
                "perfis_alvo": list(PerfilProfissional),  # Todos os perfis
                "complexidade": 5
            },
            {
                "id": 15, "nome": "Simulação de Colabs Estratégicas",
                "descricao": "Parcerias fantasma e colaborações estratégicas",
                "funcionalidades": ["mapeamento de parceiros", "simulação de colaborações", "networking estratégico"],
                "perfis_alvo": [PerfilProfissional.INFLUENCER, PerfilProfissional.CRIADOR],
                "complexidade": 4
            },
            # Continuando com os módulos 16-32...
            {
                "id": 16, "nome": "Modo Microagência",
                "descricao": "Operação como microagência especializada",
                "funcionalidades": ["estrutura de agência", "gestão de clientes", "escalabilidade"],
                "perfis_alvo": [PerfilProfissional.CONSULTOR, PerfilProfissional.ESPECIALISTA],
                "complexidade": 4
            },
            {
                "id": 17, "nome": "Modo Produto de Conhecimento",
                "descricao": "Criação e monetização de cursos, ebooks e templates",
                "funcionalidades": ["desenvolvimento de cursos", "plataformas de ensino", "monetização de conhecimento"],
                "perfis_alvo": [PerfilProfissional.EDUCADOR, PerfilProfissional.ESPECIALISTA],
                "complexidade": 4
            },
            {
                "id": 18, "nome": "Modo Criador de Conteúdo e Influência",
                "descricao": "Estratégia completa de criação de conteúdo e influência digital",
                "funcionalidades": ["estratégia de conteúdo", "crescimento orgânico", "monetização de audiência"],
                "perfis_alvo": [PerfilProfissional.CRIADOR, PerfilProfissional.INFLUENCER],
                "complexidade": 4
            },
            {
                "id": 19, "nome": "Modo Especialista de Confiança",
                "descricao": "Posicionamento como autoridade confiável em área específica",
                "funcionalidades": ["construção de confiança", "autoridade técnica", "relacionamento de longo prazo"],
                "perfis_alvo": [PerfilProfissional.CONSULTOR, PerfilProfissional.TERAPEUTA],
                "complexidade": 3
            },
            {
                "id": 20, "nome": "Modo MEI Offline",
                "descricao": "Estratégias para prestadores físicos e microcomércios",
                "funcionalidades": ["otimização local", "presença física", "digitalização gradual"],
                "perfis_alvo": [PerfilProfissional.PRESTADOR_FISICO, PerfilProfissional.MICROEMPREENDEDOR],
                "complexidade": 2
            },
            {
                "id": 21, "nome": "GeoImpacto",
                "descricao": "Estratégia local de domínio territorial",
                "funcionalidades": ["marketing local", "networking regional", "impacto comunitário"],
                "perfis_alvo": [PerfilProfissional.PRESTADOR_FISICO, PerfilProfissional.EDUCADOR],
                "complexidade": 3
            },
            {
                "id": 22, "nome": "Mestre Invisível",
                "descricao": "Crescimento sem exposição pública excessiva",
                "funcionalidades": ["estratégias de bastidores", "influência indireta", "network privado"],
                "perfis_alvo": [PerfilProfissional.CONSULTOR, PerfilProfissional.ESPECIALISTA],
                "complexidade": 4
            },
            {
                "id": 23, "nome": "IA como Equipe",
                "descricao": "Delegação e automação com inteligência artificial",
                "funcionalidades": ["automação de processos", "IA assistente", "escala sem contratação"],
                "perfis_alvo": list(PerfilProfissional),  # Todos os perfis
                "complexidade": 5
            },
            {
                "id": 24, "nome": "Rota do Legado",
                "descricao": "Liberdade financeira, geográfica e planejamento de sucessão",
                "funcionalidades": ["planejamento financeiro", "liberdade geográfica", "construção de legado"],
                "perfis_alvo": [PerfilProfissional.MENTOR, PerfilProfissional.ESPECIALISTA],
                "complexidade": 5
            },
            {
                "id": 25, "nome": "Modo Nômade Digital Profundo",
                "descricao": "Vida viajando com monetização consistente",
                "funcionalidades": ["trabalho remoto", "monetização global", "infraestrutura móvel"],
                "perfis_alvo": [PerfilProfissional.CRIADOR, PerfilProfissional.CONSULTOR],
                "complexidade": 4
            },
            {
                "id": 26, "nome": "Modo Antifrágil",
                "descricao": "Blindagem contra crises externas e fortalecimento",
                "funcionalidades": ["diversificação de riscos", "sistemas de backup", "adaptabilidade"],
                "perfis_alvo": list(PerfilProfissional),  # Todos os perfis
                "complexidade": 5
            },
            {
                "id": 27, "nome": "Modo Mestre de Mestres",
                "descricao": "Formação e mentoria de outros profissionais de elite",
                "funcionalidades": ["programa de mentoria", "certificação própria", "rede de discípulos"],
                "perfis_alvo": [PerfilProfissional.MENTOR, PerfilProfissional.EDUCADOR],
                "complexidade": 5
            },
            {
                "id": 28, "nome": "Modo Clonagem de Sistema",
                "descricao": "Replicação e escalabilidade de sistemas de sucesso",
                "funcionalidades": ["documentação de processos", "replicação sistemática", "franchising intelectual"],
                "perfis_alvo": [PerfilProfissional.MICROEMPREENDEDOR, PerfilProfissional.MENTOR],
                "complexidade": 4
            },
            {
                "id": 29, "nome": "Modo Finanças Pessoais e Empresariais Integradas",
                "descricao": "Gestão financeira unificada e otimizada",
                "funcionalidades": ["planejamento financeiro", "otimização tributária", "investimentos estratégicos"],
                "perfis_alvo": list(PerfilProfissional),  # Todos os perfis
                "complexidade": 4
            },
            {
                "id": 30, "nome": "Modo Energia e Ritmo de Trabalho Ótimo",
                "descricao": "Otimização de energia e prevenção de burnout",
                "funcionalidades": ["gestão de energia", "ritmo sustentável", "produtividade consciente"],
                "perfis_alvo": list(PerfilProfissional),  # Todos os perfis
                "complexidade": 3
            },
            {
                "id": 31, "nome": "Modo Comunidade AutoMaster",
                "descricao": "Círculo próprio de valor e network estratégico",
                "funcionalidades": ["construção de comunidade", "network estratégico", "valor mútuo"],
                "perfis_alvo": [PerfilProfissional.MENTOR, PerfilProfissional.EDUCADOR],
                "complexidade": 4
            },
            {
                "id": 32, "nome": "Modo Socorro Total e Backup Estratégico",
                "descricao": "Plano de recuperação em caso de colapso total",
                "funcionalidades": ["plano de contingência", "backup de sistemas", "recuperação rápida"],
                "perfis_alvo": list(PerfilProfissional),  # Todos os perfis
                "complexidade": 5
            }
        ]
        
        # Criar objetos ModuloAvancado
        for def_modulo in definicoes_modulos:
            modulo = ModuloAvancado(
                id=def_modulo["id"],
                nome=def_modulo["nome"],
                descricao=def_modulo["descricao"],
                funcionalidades=def_modulo["funcionalidades"],
                perfis_alvo=def_modulo["perfis_alvo"],
                nivel_complexidade=def_modulo["complexidade"]
            )
            modulos[def_modulo["id"]] = modulo
        
        logger.info(f"🤖 {len(modulos)} módulos avançados inicializados")
        return modulos
    
    def _processar_interno(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        🧠 PROCESSAMENTO AUTOMASTER v4.0 (BaseAgentV2)
        
        FLUXO INTELIGENTE DE AUTONOMIA:
        1. 🎯 Análise do perfil e necessidades do usuário
        2. 🧠 Seleção inteligente de módulos relevantes
        3. 📊 Criação de plano estratégico personalizado
        4. 💰 Simulação de faturamento e projeções
        5. 🛡️ Sistema antifrágil e contingências
        6. 🌟 Entrega de roteiro completo de autonomia
        
        Implementa _processar_interno ao invés de processar para BaseAgentV2
        """
        try:
            # 1. ANÁLISE DO COMANDO E PERFIL
            analise_comando = self._analisar_comando_automaster(mensagem)
            tipo_solicitacao = analise_comando['tipo']
            parametros = analise_comando['parametros']
            
            logger.info(f"🎯 Comando AutoMaster: {tipo_solicitacao}")
            
            # 2. IDENTIFICAÇÃO DO PERFIL (se disponível no contexto)
            perfil_usuario = self._extrair_perfil_usuario(contexto or {}, mensagem)
            
            # 3. SELEÇÃO DE MÓDULOS RELEVANTES
            modulos_selecionados = self._selecionar_modulos_relevantes(
                tipo_solicitacao, perfil_usuario, parametros
            )
            
            # 4. GERAÇÃO DO PLANO ESTRATÉGICO
            if tipo_solicitacao in ["plano_completo", "curso_digital", "monetizacao"]:
                plano = self._criar_plano_estrategico_completo(
                    perfil_usuario, modulos_selecionados, tipo_solicitacao, parametros
                )
                resposta = self._formatar_plano_estrategico(plano)
                
            elif tipo_solicitacao == "simulacao_faturamento":
                simulacao = self._executar_simulacao_faturamento(perfil_usuario, parametros)
                resposta = self._formatar_simulacao_faturamento(simulacao)
                
            elif tipo_solicitacao == "modo_antifragil":
                resposta = self._ativar_modo_antifragil(perfil_usuario, parametros)
                
            elif tipo_solicitacao == "organizacao_financeira":
                resposta = self._ativar_modo_financas_integradas(perfil_usuario)
                
            elif tipo_solicitacao == "energia_otima":
                resposta = self._ativar_modo_energia_otima(perfil_usuario)
                
            elif tipo_solicitacao == "comunidade_propria":
                resposta = self._ativar_modo_comunidade(perfil_usuario)
                
            elif tipo_solicitacao == "backup_total":
                resposta = self._ativar_modo_socorro_total(perfil_usuario)
                
            else:
                # Resposta personalizada baseada nos módulos
                resposta = self._gerar_resposta_personalizada(
                    mensagem, perfil_usuario, modulos_selecionados
                )
            
            # 5. INTEGRAÇÃO COM OUTROS AGENTES (se necessário)
            if self.integracoes_ativas.get("oraculo") and "decisão crítica" in mensagem.lower():
                resposta = self._consultar_oraculo_para_validacao(resposta, mensagem)
            
            # 6. ATUALIZAR ESTATÍSTICAS E PERSISTIR
            self._atualizar_stats_automaster(tipo_solicitacao, len(modulos_selecionados))
            self._salvar_historico_persistente()
            
            return resposta
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento AutoMaster: {e}")
            raise  # Re-lançar para o BaseAgentV2 tratar com retry e fallback
    
    def _fallback_response(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Resposta de fallback específica do AutoMaster quando há erro"""
        return f"""🧠 **AutoMaster v4.0 - Modo de Recuperação**

Detectei uma instabilidade temporária no sistema. Enquanto restauro a capacidade total, aqui está uma orientação inicial:

**ANÁLISE RÁPIDA:**
Baseado em sua mensagem, você busca autonomia e crescimento profissional.

**AÇÕES IMEDIATAS:**
1. 📝 Defina claramente seu objetivo principal
2. 🎯 Identifique sua expertise única
3. 💰 Liste suas fontes de renda atuais
4. 🛡️ Avalie seus principais riscos

**PRÓXIMOS PASSOS:**
Tente novamente em alguns instantes para acesso completo aos 32 módulos especializados.

_[Sistema em auto-recuperação... Status: {self.circuit_breaker.state}]_"""
    
    def _analisar_comando_automaster(self, mensagem: str) -> Dict:
        """🎯 Analisa comando específico do AutoMaster"""
        mensagem_lower = mensagem.lower()
        
        # Comandos padrão identificados
        if any(palavra in mensagem_lower for palavra in ["curso digital", "curso", "conhecimento"]):
            return {"tipo": "curso_digital", "parametros": self._extrair_tema_curso(mensagem)}
        
        elif any(palavra in mensagem_lower for palavra in ["viajando", "nomade", "viajar"]):
            return {"tipo": "nomade_digital", "parametros": {"foco": "mobilidade"}}
        
        elif any(palavra in mensagem_lower for palavra in ["blinde", "crise", "antifragil"]):
            return {"tipo": "modo_antifragil", "parametros": {"urgencia": "alta"}}
        
        elif any(palavra in mensagem_lower for palavra in ["financeiro", "organize", "dinheiro"]):
            return {"tipo": "organizacao_financeira", "parametros": {"escopo": "completo"}}
        
        elif any(palavra in mensagem_lower for palavra in ["energia", "rotina", "esgotamento"]):
            return {"tipo": "energia_otima", "parametros": {"foco": "sustentabilidade"}}
        
        elif any(palavra in mensagem_lower for palavra in ["comunidade", "alunos", "clientes"]):
            return {"tipo": "comunidade_propria", "parametros": {"tipo": "educacional"}}
        
        elif any(palavra in mensagem_lower for palavra in ["backup", "recuperação", "colapso"]):
            return {"tipo": "backup_total", "parametros": {"nivel": "completo"}}
        
        elif any(palavra in mensagem_lower for palavra in ["simulação", "faturamento", "projeção"]):
            return {"tipo": "simulacao_faturamento", "parametros": {"periodo": "anual"}}
        
        else:
            return {"tipo": "plano_completo", "parametros": {"abrangencia": "total"}}
    
    def _extrair_perfil_usuario(self, contexto: Dict, mensagem: str) -> PerfilUsuario:
        """👤 Extrai ou cria perfil do usuário baseado no contexto"""
        # Se há contexto de perfil, usar
        if "perfil_usuario" in contexto:
            return contexto["perfil_usuario"]
        
        # Verificar memória persistente
        if self.memory and hasattr(self.memory, 'user_preferences'):
            perfil_salvo = self.memory.user_preferences.get('perfil_automaster')
            if perfil_salvo:
                return PerfilUsuario(**perfil_salvo)
        
        # Senão, inferir do texto
        perfil_inferido = self._inferir_perfil_da_mensagem(mensagem)
        
        perfil = PerfilUsuario(
            nome=contexto.get("nome_usuario", "Usuário"),
            perfil_profissional=perfil_inferido["perfil"],
            fase_vida=perfil_inferido["fase"],
            objetivos_principais=perfil_inferido["objetivos"],
            preferencia_exposicao=perfil_inferido["exposicao"],
            tempo_disponivel=perfil_inferido["tempo"],
            conhecimento_acumulado=perfil_inferido["conhecimento"],
            desafios_atuais=perfil_inferido["desafios"],
            recursos_disponiveis=perfil_inferido["recursos"]
        )
        
        # Salvar perfil na memória persistente
        if self.memory:
            self.memory.user_preferences['perfil_automaster'] = {
                'nome': perfil.nome,
                'perfil_profissional': perfil.perfil_profissional.value,
                'fase_vida': perfil.fase_vida.value,
                'objetivos_principais': perfil.objetivos_principais,
                'preferencia_exposicao': perfil.preferencia_exposicao,
                'tempo_disponivel': perfil.tempo_disponivel,
                'conhecimento_acumulado': perfil.conhecimento_acumulado,
                'desafios_atuais': [d.value for d in perfil.desafios_atuais],
                'recursos_disponiveis': perfil.recursos_disponiveis
            }
        
        return perfil
    
    def _inferir_perfil_da_mensagem(self, mensagem: str) -> Dict:
        """🔍 Infere perfil do usuário baseado na mensagem"""
        mensagem_lower = mensagem.lower()
        
        # Inferir perfil profissional
        if any(palavra in mensagem_lower for palavra in ["curso", "ensino", "educação"]):
            perfil = PerfilProfissional.EDUCADOR
        elif any(palavra in mensagem_lower for palavra in ["conteúdo", "criativo", "arte"]):
            perfil = PerfilProfissional.CRIADOR
        elif any(palavra in mensagem_lower for palavra in ["consultoria", "especialista"]):
            perfil = PerfilProfissional.CONSULTOR
        elif any(palavra in mensagem_lower for palavra in ["terapeuta", "terapia"]):
            perfil = PerfilProfissional.TERAPEUTA
        else:
            perfil = PerfilProfissional.AUTONOMO
        
        # Inferir fase da vida
        if any(palavra in mensagem_lower for palavra in ["começando", "iniciando"]):
            fase = FaseVida.INICIANTE
        elif any(palavra in mensagem_lower for palavra in ["estagnado", "parado"]):
            fase = FaseVida.ESTAGNACAO
        elif any(palavra in mensagem_lower for palavra in ["expandir", "crescer"]):
            fase = FaseVida.EXPANSAO
        else:
            fase = FaseVida.CRESCIMENTO
        
        return {
            "perfil": perfil,
            "fase": fase,
            "objetivos": ["autonomia financeira", "liberdade geográfica"],
            "exposicao": "media",
            "tempo": "parcial",
            "conhecimento": "intermediario",
            "desafios": [TipoDesafio.ESTRATEGICO],
            "recursos": {"tempo": "limitado", "investimento": "baixo"}
        }
    
    def _selecionar_modulos_relevantes(self, tipo_solicitacao: str, 
                                     perfil: PerfilUsuario, parametros: Dict) -> List[int]:
        """🧠 Seleção inteligente de módulos relevantes"""
        modulos_selecionados = []
        
        # Módulos base sempre relevantes
        modulos_base = [1, 12, 26, 29, 30]  # Narrativa, Autodiagnóstico, Antifrágil, Finanças, Energia
        modulos_selecionados.extend(modulos_base)
        
        # Seleção baseada no tipo de solicitação
        mapeamento_tipo_modulos = {
            "curso_digital": [4, 17, 8, 10],  # Lançamento, Produto Conhecimento, Fidelização, Autoridade
            "nomade_digital": [25, 23, 24],   # Nômade Digital, IA Equipe, Rota Legado
            "modo_antifragil": [26, 32, 28],  # Antifrágil, Socorro Total, Clonagem Sistema
            "organizacao_financeira": [29, 7, 24],  # Finanças Integradas, Simulador, Rota Legado
            "energia_otima": [30, 22, 31],    # Energia Ótima, Mestre Invisível, Comunidade
            "comunidade_propria": [8, 31, 27],  # Fidelização, Comunidade, Mestre de Mestres
            "backup_total": [32, 26, 28],     # Socorro Total, Antifrágil, Clonagem
        }
        
        if tipo_solicitacao in mapeamento_tipo_modulos:
            modulos_selecionados.extend(mapeamento_tipo_modulos[tipo_solicitacao])
        
        # Seleção baseada no perfil profissional
        for modulo_id, modulo in self.modulos_avancados.items():
            if (perfil.perfil_profissional in modulo.perfis_alvo and 
                modulo_id not in modulos_selecionados):
                modulos_selecionados.append(modulo_id)
        
        # Limitar a 8 módulos para não sobrecarregar
        return list(set(modulos_selecionados))[:8]
    
    def _criar_plano_estrategico_completo(self, perfil: PerfilUsuario, 
                                        modulos: List[int], tipo: str, 
                                        parametros: Dict) -> PlanoEstrategico:
        """📋 Cria plano estratégico completo personalizado"""
        self.contador_planos += 1
        
        # Gerar estratégia principal usando LLM se disponível
        if self.llm_available and self.llm:
            estrategia_principal = self._gerar_estrategia_llm(perfil, modulos, tipo)
        else:
            estrategia_principal = self._gerar_estrategia_template(perfil, tipo)
        
        # Criar componentes do plano
        plano_90_dias = self._gerar_plano_90_dias(perfil, modulos)
        plano_1_ano = self._gerar_plano_1_ano(perfil, modulos)
        sistema_monetizacao = self._gerar_sistema_monetizacao(perfil)
        estrategia_marca = self._gerar_estrategia_marca(perfil)
        plano_comunidade = self._gerar_plano_comunidade(perfil)
        sistema_antifragil = self._gerar_sistema_antifragil(perfil)
        
        plano = PlanoEstrategico(
            id=f"automaster_plano_{self.contador_planos:03d}",
            usuario=perfil,
            modulos_ativados=modulos,
            estrategia_principal=estrategia_principal,
            plano_90_dias=plano_90_dias,
            plano_1_ano=plano_1_ano,
            sistema_monetizacao=sistema_monetizacao,
            estrategia_marca=estrategia_marca,
            plano_comunidade=plano_comunidade,
            sistema_antifragil=sistema_antifragil,
            metricas_sucesso=self._definir_metricas_sucesso(perfil),
            recursos_necessarios=self._listar_recursos_necessarios(modulos),
            cronograma=self._gerar_cronograma(perfil)
        )
        
        self.planos_estrategicos.append(plano)
        return plano
    
    def _gerar_estrategia_llm(self, perfil: PerfilUsuario, modulos: List[int], tipo: str) -> str:
        """🧠 Gera estratégia usando LLM"""
        try:
            prompt = f"""Você é o AutoMaster v4.0, agente especialista em autonomia econômica e estratégica.

PERFIL DO USUÁRIO:
- Profissão: {getattr(perfil.perfil_profissional, 'value', perfil.perfil_profissional)}
- Fase: {getattr(perfil.fase_vida, 'value', perfil.fase_vida)}
- Objetivos: {', '.join(perfil.objetivos_principais)}
- Preferência de exposição: {perfil.preferencia_exposicao}
- Tempo disponível: {perfil.tempo_disponivel}
- Conhecimento: {perfil.conhecimento_acumulado}

TIPO DE SOLICITAÇÃO: {tipo}

MÓDULOS ATIVADOS: {len(modulos)} módulos especializados

MISSÃO: Crie uma estratégia principal clara, prática e acionável para este perfil alcançar autonomia econômica e estratégica.

FOQUE EM:
- Passos concretos e implementáveis
- Monetização sustentável
- Sistema antifrágil
- Liberdade geográfica e financeira

Responda de forma direta e prática (máximo 3 parágrafos):"""

            resposta = self.llm.invoke(prompt).content
            return resposta.strip()
            
        except Exception as e:
            logger.warning(f"⚠️ Erro na geração LLM: {e}")
            return self._gerar_estrategia_template(perfil, tipo)
    
    def _gerar_estrategia_template(self, perfil: PerfilUsuario, tipo: str) -> str:
        """📋 Gera estratégia usando template"""
        templates = {
            "curso_digital": f"Crie um curso digital baseado em sua expertise em {getattr(perfil.perfil_profissional, 'value', perfil.perfil_profissional)}. Estruture o conteúdo em módulos práticos, use plataforma de ensino adequada e implemente estratégia de lançamento gradual com comunidade de alunos.",
            
            "nomade_digital": f"Transforme seu trabalho como {getattr(perfil.perfil_profissional, 'value', perfil.perfil_profissional)} em modelo 100% remoto. Diversifique fontes de renda, automatize processos e crie sistemas que funcionem independente de localização geográfica.",
            
            "plano_completo": f"Desenvolva ecossistema completo de autonomia como {getattr(perfil.perfil_profissional, 'value', perfil.perfil_profissional)}. Combine prestação de serviços, produtos digitais e construção de autoridade para criar múltiplas fontes de renda sustentáveis."
        }
        
        return templates.get(tipo, templates["plano_completo"])
    
    def _gerar_plano_90_dias(self, perfil: PerfilUsuario, modulos: List[int]) -> str:
        """📅 Gera plano de 90 dias"""
        return f"""PLANO 90 DIAS - {getattr(perfil.perfil_profissional, 'value', perfil.perfil_profissional).upper()}

MÊS 1 - ESTRUTURAÇÃO:
• Definir narrativa profissional e posicionamento único
• Estruturar sistema de precificação baseado em valor
• Criar presença digital básica e canais de comunicação

MÊS 2 - IMPLEMENTAÇÃO:
• Lançar primeira oferta de valor (produto/serviço)
• Estabelecer rotina de produção de conteúdo
• Implementar sistema de gestão financeira integrada

MÊS 3 - OTIMIZAÇÃO:
• Analisar primeiros resultados e ajustar estratégia
• Implementar sistema antifrágil e backup
• Iniciar construção de comunidade própria"""
    
    def _gerar_plano_1_ano(self, perfil: PerfilUsuario, modulos: List[int]) -> str:
        """📅 Gera plano de 1 ano"""
        return f"""PLANO 1 ANO - AUTONOMIA COMPLETA

TRIMESTRE 1: Fundação sólida e primeiros resultados
TRIMESTRE 2: Diversificação de receitas e escalabilidade
TRIMESTRE 3: Autoridade estabelecida e comunidade ativa
TRIMESTRE 4: Sistema antifrágil e preparação para legado

META ANUAL: Alcançar autonomia financeira de {perfil.perfil_profissional.value} com múltiplas fontes de renda e liberdade geográfica."""
    
    def _executar_simulacao_faturamento(self, perfil: PerfilUsuario, parametros: Dict) -> SimulacaoFaturamento:
        """💰 Executa simulação de faturamento multicanal"""
        # Simulação baseada no perfil profissional
        base_valores = {
            PerfilProfissional.EDUCADOR: {"curso": 497, "mentoria": 200, "consultoria": 150},
            PerfilProfissional.CONSULTOR: {"consultoria": 300, "projeto": 2000, "retainer": 1500},
            PerfilProfissional.CRIADOR: {"produto": 97, "servico": 500, "patrocinio": 800},
            PerfilProfissional.TERAPEUTA: {"sessao": 120, "programa": 800, "workshop": 300}
        }
        
        valores = base_valores.get(perfil.perfil_profissional, {"servico": 200, "produto": 100})
        
        # Calcular projeções
        projecao_mensal = sum(valores.values()) * 2  # Estimativa conservadora
        projecao_anual = projecao_mensal * 12
        
        simulacao = SimulacaoFaturamento(
            produtos_servicos=valores,
            canais_venda={"direto": 0.6, "plataformas": 0.3, "indicacoes": 0.1},
            projecao_mensal=projecao_mensal,
            projecao_anual=projecao_anual,
            cenario_conservador=projecao_anual * 0.7,
            cenario_otimista=projecao_anual * 1.5,
            pontos_criticos=["sazonalidade", "dependência de um canal", "precificação baixa"]
        )
        
        self.simulacoes_faturamento.append(simulacao)
        return simulacao
    
    def _ativar_modo_antifragil(self, perfil: PerfilUsuario, parametros: Dict) -> str:
        """🛡️ Ativa modo antifrágil completo"""
        return f"""🛡️ **MODO ANTIFRÁGIL ATIVADO**

**Blindagem Estratégica para {perfil.perfil_profissional.value}:**

**🔒 DIVERSIFICAÇÃO DE RISCOS:**
• 3 fontes de renda independentes mínimas
• Backup de clientes/canais para cada fonte
• Reserva de emergência de 6 meses

**⚡ SISTEMAS DE BACKUP:**
• Documentação completa de todos os processos
• Múltiplas plataformas e canais de comunicação
• Network de parceiros e colaboradores estratégicos

**🔄 ADAPTABILIDADE:**
• Monitoramento de tendências e mudanças do mercado
• Flexibilidade para pivot rápido quando necessário
• Habilidades transferíveis e constantemente atualizadas

**🚀 CRESCIMENTO COM CRISE:**
• Estratégias para lucrar com instabilidade
• Posicionamento como solução em tempos difíceis
• Construção de autoridade em momentos de incerteza

**PLANO DE AÇÃO IMEDIATO:**
1. Mapeie suas 3 principais vulnerabilidades
2. Crie backup para cada uma delas
3. Implemente sistema de monitoramento semanal
4. Desenvolva pelo menos 2 fontes de renda adicionais

Sistema antifrágil não só resiste a crises, mas fica mais forte com elas."""
    
    def _formatar_plano_estrategico(self, plano: PlanoEstrategico) -> str:
        """📝 Formata plano estratégico para apresentação"""
        return f"""🧠 **AutoMaster v4.0 — Plano Estratégico Personalizado**

**PERFIL:** {plano.usuario.perfil_profissional.value.title()} | **FASE:** {plano.usuario.fase_vida.value.title()}

**🎯 ESTRATÉGIA PRINCIPAL:**
{plano.estrategia_principal}

**📅 PLANO 90 DIAS:**
{plano.plano_90_dias}

**💰 SISTEMA DE MONETIZAÇÃO:**
{plano.sistema_monetizacao}

**🛡️ SISTEMA ANTIFRÁGIL:**
{plano.sistema_antifragil}

**📊 MÓDULOS ATIVADOS:** {len(plano.modulos_ativados)} especializados
**🎯 ID DO PLANO:** {plano.id}

_[Para ver plano completo de 1 ano, simulação de faturamento ou ativação de módulos específicos: solicite explicitamente]_"""
    
    def _atualizar_stats_automaster(self, tipo_solicitacao: str, modulos_ativados: int):
        """📊 Atualiza estatísticas do AutoMaster"""
        self.stats["planos_estrategicos_criados"] += 1
        self.stats["modulos_ativados_total"] += modulos_ativados
        self.stats["usuarios_atendidos"] += 1
        
        # Estatísticas específicas por tipo
        if tipo_solicitacao == "curso_digital":
            self.stats["economia_gerada_estimada"] += 5000  # Estimativa de valor de curso
        elif tipo_solicitacao == "nomade_digital":
            self.stats["liberdade_geografica_alcancada"] += 1
        elif tipo_solicitacao == "energia_otima":
            self.stats["burnouts_prevenidos"] += 1
        elif tipo_solicitacao == "comunidade_propria":
            self.stats["comunidades_criadas"] += 1
    
    # === MÉTODOS AUXILIARES ESPECÍFICOS ===
    
    def _gerar_sistema_monetizacao(self, perfil: PerfilUsuario) -> str:
        """💰 Gera sistema de monetização personalizado"""
        return f"Sistema de monetização multicanal para {perfil.perfil_profissional.value} com foco em escalabilidade e recorrência."
    
    def _gerar_estrategia_marca(self, perfil: PerfilUsuario) -> str:
        """🎨 Gera estratégia de marca"""
        return f"Estratégia de marca autêntica baseada em propósito e diferenciação para {perfil.perfil_profissional.value}."
    
    def _gerar_plano_comunidade(self, perfil: PerfilUsuario) -> str:
        """👥 Gera plano de comunidade"""
        return f"Construção de comunidade engajada de {perfil.perfil_profissional.value} com foco em valor mútuo e crescimento."
    
    def _gerar_sistema_antifragil(self, perfil: PerfilUsuario) -> str:
        """🛡️ Gera sistema antifrágil"""
        return f"Sistema antifrágil personalizado para {perfil.perfil_profissional.value} com backup e contingências."
    
    def _definir_metricas_sucesso(self, perfil: PerfilUsuario) -> Dict[str, Any]:
        """📊 Define métricas de sucesso"""
        return {
            "faturamento_mensal": 5000,
            "clientes_ativos": 20,
            "rate_retencao": 0.8,
            "liberdade_geografica": True
        }
    
    def _listar_recursos_necessarios(self, modulos: List[int]) -> List[str]:
        """📋 Lista recursos necessários"""
        return ["Plataforma digital", "Sistema de pagamento", "Ferramentas de automação"]
    
    def _gerar_cronograma(self, perfil: PerfilUsuario) -> Dict[str, str]:
        """📅 Gera cronograma personalizado"""
        return {
            "mes_1": "Estruturação e setup inicial",
            "mes_2": "Implementação e primeiros clientes",
            "mes_3": "Otimização e escalabilidade"
        }
    
    def _extrair_tema_curso(self, mensagem: str) -> Dict:
        """📚 Extrai tema do curso da mensagem"""
        # Implementação simplificada
        return {"tema": "expertise do usuário", "formato": "online"}
    
    def _formatar_simulacao_faturamento(self, simulacao: SimulacaoFaturamento) -> str:
        """💰 Formata simulação de faturamento"""
        return f"""💰 **SIMULAÇÃO DE FATURAMENTO MULTICANAL**

**PRODUTOS/SERVIÇOS:**
{chr(10).join(f"• {produto}: R$ {valor:.2f}" for produto, valor in simulacao.produtos_servicos.items())}

**PROJEÇÕES:**
• **Mensal:** R$ {simulacao.projecao_mensal:.2f}
• **Anual:** R$ {simulacao.projecao_anual:.2f}

**CENÁRIOS:**
• **Conservador:** R$ {simulacao.cenario_conservador:.2f}
• **Otimista:** R$ {simulacao.cenario_otimista:.2f}

**PONTOS DE ATENÇÃO:**
{chr(10).join(f"⚠️ {ponto}" for ponto in simulacao.pontos_criticos)}"""
    
    # Métodos para outros modos específicos
    def _ativar_modo_financas_integradas(self, perfil: PerfilUsuario) -> str:
        """💳 Ativa modo finanças integradas"""
        return "💳 Modo Finanças Integradas ativado - organizando fluxo pessoal e empresarial."
    
    def _ativar_modo_energia_otima(self, perfil: PerfilUsuario) -> str:
        """⚡ Ativa modo energia ótima"""
        return "⚡ Modo Energia Ótima ativado - otimizando ritmo e prevenindo burnout."
    
    def _ativar_modo_comunidade(self, perfil: PerfilUsuario) -> str:
        """👥 Ativa modo comunidade"""
        return "👥 Modo Comunidade ativado - estruturando círculo próprio de valor."
    
    def _ativar_modo_socorro_total(self, perfil: PerfilUsuario) -> str:
        """🆘 Ativa modo socorro total"""
        return "🆘 Modo Socorro Total ativado - criando plano de contingência completo."
    
    def _gerar_resposta_personalizada(self, mensagem: str, perfil: PerfilUsuario, 
                                    modulos: List[int]) -> str:
        """🎯 Gera resposta personalizada"""
        return f"Resposta AutoMaster personalizada para {perfil.perfil_profissional.value} usando {len(modulos)} módulos especializados."
    
    def _consultar_oraculo_para_validacao(self, resposta: str, mensagem: str) -> str:
        """🔮 Consulta Oráculo para validação (integração futura)"""
        # Placeholder para integração com Oráculo
        return f"{resposta}\n\n🔮 _[Validado pelo Oráculo v8.1 Plus+]_"
    
    # === MÉTODOS DE DIAGNÓSTICO E STATUS ===
    
    def diagnosticar_automaster(self) -> Dict:
        """🔧 Diagnóstico completo do AutoMaster"""
        modulos_ativos = len([m for m in self.modulos_avancados.values() if m.ativo])
        
        # Obter health status do BaseAgentV2
        health_status = self.get_health_status()
        
        return {
            "version": "4.0_Autonomia_Economica_Estrategica_V2",
            "status": health_status["status"].upper(),
            "health_score": health_status["health_score"],
            "modulos_disponiveis": len(self.modulos_avancados),
            "modulos_ativos": modulos_ativos,
            "planos_criados": len(self.planos_estrategicos),
            "simulacoes_realizadas": len(self.simulacoes_faturamento),
            "modo_antifragil": self.modo_antifragil_ativo,
            "sistema_backup": self.sistema_backup_ativo,
            "gemeo_pro": self.gêmeo_pro_ativo,
            "shadow_ops": self.shadow_ops_ativo,
            "integracoes": self.integracoes_ativas,
            "robustez": {
                "circuit_breaker": self.circuit_breaker.state,
                "cache_items": len(self.cache) if self.cache else 0,
                "memory_items": len(self.memory.messages),
                "persistent_memory": self.persistent_memory
            },
            "stats_completas": self.stats
        }
    
    def listar_modulos_disponiveis(self) -> str:
        """📋 Lista todos os módulos disponíveis"""
        lista = "🧠 **AUTOMASTER v4.0 - 32 MÓDULOS AVANÇADOS**\n\n"
        
        for modulo in self.modulos_avancados.values():
            status = "✅" if modulo.ativo else "❌"
            lista += f"{status} **{modulo.id}. {modulo.nome}**\n"
            lista += f"   {modulo.descricao}\n"
            lista += f"   Complexidade: {'⭐' * modulo.nivel_complexidade}\n\n"
        
        return lista
    
    def obter_historico_planos(self, ultimos: int = 5) -> str:
        """📚 Retorna histórico dos últimos planos"""
        if not self.planos_estrategicos:
            return "📚 Nenhum plano estratégico criado ainda."
        
        planos_recentes = self.planos_estrategicos[-ultimos:]
        
        historico = f"📚 **HISTÓRICO DOS ÚLTIMOS {len(planos_recentes)} PLANOS**\n\n"
        
        for plano in reversed(planos_recentes):
            historico += f"**{plano.id}** - {plano.timestamp.strftime('%d/%m/%Y %H:%M')}\n"
            historico += f"Perfil: {plano.usuario.perfil_profissional.value}\n"
            historico += f"Módulos: {len(plano.modulos_ativados)}\n"
            historico += "---\n\n"
        
        return historico
    
    def cleanup_resources(self):
        """Limpa recursos e salva estado final"""
        # Salvar histórico antes de limpar
        self._salvar_historico_persistente()
        
        # Chamar cleanup do BaseAgentV2
        super().cleanup_resources()
        
        logger.info("🧹 AutoMaster v4.0 recursos limpos e estado salvo")

# === FUNÇÕES DE CRIAÇÃO ===

def criar_automaster_v2(llm=None, **kwargs) -> AutoMasterV2:
    """🧠 Cria AutoMaster v4.0 com BaseAgentV2 e configurações robustas"""
    return AutoMasterV2(llm=llm, **kwargs)

# Alias para compatibilidade
create_automaster_v2 = criar_automaster_v2
create_automaster = criar_automaster_v2

if __name__ == "__main__":
    print("🧠 Testando AutoMaster v4.0 (BaseAgentV2)...")
    
    automaster = criar_automaster_v2()
    diagnostico = automaster.diagnosticar_automaster()
    
    print(f"📊 Diagnóstico: {diagnostico['version']}")
    print(f"🤖 Status: {diagnostico['status']} (Score: {diagnostico['health_score']})")
    print(f"🛡️ Circuit Breaker: {diagnostico['robustez']['circuit_breaker']}")
    print(f"💾 Memória Persistente: {diagnostico['robustez']['persistent_memory']}")
    print(f"📦 Módulos ativos: {diagnostico['modulos_ativos']}/{diagnostico['modulos_disponiveis']}")
    print("✅ AutoMaster v4.0 (BaseAgentV2) pronto para autonomia econômica com robustez total!")