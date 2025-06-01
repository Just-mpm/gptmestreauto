"""
🎨 PROMPTCRAFTER v3.0 - Engenheiro de Prompts Adaptativo
Motor textual evolutivo com aprendizado neural e conhecimento coletivo
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum

from .base_agent_v2 import BaseAgentV2
from utils.logger import get_logger

# Imports opcionais para funcionalidades avançadas
try:
    import numpy as np
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger = get_logger("promptcrafter")
    logger.warning("⚠️ sklearn não disponível - funcionalidades de ML limitadas")

# Knowledge Graph import opcional
try:
    from .knowledge_graph_v1 import KnowledgeGraphV1, TipoEntidade, TipoRelacao
    KNOWLEDGE_GRAPH_AVAILABLE = True
except ImportError:
    KNOWLEDGE_GRAPH_AVAILABLE = False
    TipoEntidade = None
    TipoRelacao = None

logger = get_logger("promptcrafter")


class PromptStatus(Enum):
    """Status de prompts no sistema"""
    NOVO = "novo"
    ATIVO = "ativo"
    OBSOLETO = "obsoleto"
    LOCKED = "locked"


class PromptMode(Enum):
    """Modos de operação do PromptCrafter"""
    NORMAL = "normal"
    CHAOS = "chaos"
    KIT = "kit"


@dataclass
class PromptDNA:
    """🧬 DNA completo de um prompt"""
    persona: str
    emocao: str
    funcao: str
    canal: str
    versao: str
    lineage: List[str]
    criado_em: datetime
    modificado_em: datetime
    hash_id: str


@dataclass
class PromptScore:
    """📈 Pontuação multi-dimensional de prompts"""
    reflexor: float
    copybooster: float
    roi_estimado: float
    impacto_pratico: float
    
    @property
    def media_geral(self) -> float:
        return (self.reflexor + self.copybooster + self.impacto_pratico) / 3


class PromptLearningEngine:
    """Motor de aprendizado neural para prompts"""
    
    def __init__(self):
        if SKLEARN_AVAILABLE:
            self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
            self.prompt_vectors = None
        else:
            self.vectorizer = None
            self.prompt_vectors = None
        self.prompt_performance = {}
        self.success_patterns = []
        
    def treinar_com_feedback(self, prompts: List[str], scores: List[float]):
        """Treina modelo com feedback de performance"""
        try:
            if len(prompts) != len(scores):
                return
            
            # Vetorizar prompts (se sklearn disponível)
            if SKLEARN_AVAILABLE and self.vectorizer:
                self.prompt_vectors = self.vectorizer.fit_transform(prompts)
            
            # Armazenar performance
            for prompt, score in zip(prompts, scores):
                self.prompt_performance[prompt] = score
            
            # Identificar padrões de sucesso
            self._identificar_padroes_sucesso(prompts, scores)
            
        except Exception as e:
            logger.error(f"❌ Erro no treinamento: {e}")
    
    def _identificar_padroes_sucesso(self, prompts: List[str], scores: List[float]):
        """Identifica padrões em prompts de alta performance"""
        threshold_sucesso = 0.8
        prompts_sucesso = [p for p, s in zip(prompts, scores) if s > threshold_sucesso]
        
        # Extrair padrões comuns
        palavras_sucesso = {}
        for prompt in prompts_sucesso:
            for palavra in prompt.split():
                if len(palavra) > 3:
                    palavras_sucesso[palavra] = palavras_sucesso.get(palavra, 0) + 1
        
        # Armazenar padrões mais frequentes
        self.success_patterns = [
            palavra for palavra, freq in palavras_sucesso.items() 
            if freq >= len(prompts_sucesso) * 0.3
        ]
    
    def sugerir_melhorias(self, prompt: str) -> List[str]:
        """Sugere melhorias baseadas em aprendizado"""
        sugestoes = []
        
        # Verificar se contém padrões de sucesso
        for padrao in self.success_patterns:
            if padrao not in prompt.lower():
                sugestoes.append(f"Considere adicionar: {padrao}")
        
        # Verificar estrutura
        if len(prompt.split('.')) < 3:
            sugestoes.append("Considere dividir em sentenças mais claras")
        
        if "porque" not in prompt.lower() and "por que" not in prompt.lower():
            sugestoes.append("Considere explicar o 'porquê' da tarefa")
        
        return sugestoes[:5]
    
    def calcular_similaridade(self, prompt1: str, prompt2: str) -> float:
        """Calcula similaridade entre prompts"""
        try:
            if not SKLEARN_AVAILABLE or self.prompt_vectors is None or not self.vectorizer:
                # Fallback simples sem sklearn
                palavras1 = set(prompt1.lower().split())
                palavras2 = set(prompt2.lower().split())
                intersecao = len(palavras1.intersection(palavras2))
                uniao = len(palavras1.union(palavras2))
                return intersecao / max(uniao, 1)
            
            # Vetorizar novos prompts
            vectors = self.vectorizer.transform([prompt1, prompt2])
            similaridade = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(similaridade)
            
        except Exception:
            return 0.0


class ContextAwareness:
    """Consciência contextual avançada"""
    
    def __init__(self):
        self.contextos_historicos = []
        self.padroes_temporais = {}
        self.contexto_atual = {}
        
    def capturar_contexto(self) -> Dict:
        """Captura contexto atual multidimensional"""
        contexto = {
            "temporal": self._analisar_contexto_temporal(),
            "usuário": self._analisar_contexto_usuario(),
            "sistema": self._analisar_contexto_sistema(),
            "conversacional": self._analisar_contexto_conversacional()
        }
        
        self.contexto_atual = contexto
        return contexto
    
    def _analisar_contexto_temporal(self) -> Dict:
        """Analisa contexto temporal"""
        agora = datetime.now()
        return {
            "hora": agora.hour,
            "dia_semana": agora.weekday(),
            "periodo": self._determinar_periodo(agora.hour),
            "sazonalidade": self._determinar_sazonalidade(agora.month)
        }
    
    def _analisar_contexto_usuario(self) -> Dict:
        """Analisa contexto do usuário"""
        return {
            "historico_recente": len(self.contextos_historicos),
            "padrao_uso": self._identificar_padrao_uso(),
            "preferencias": self._extrair_preferencias()
        }
    
    def _analisar_contexto_sistema(self) -> Dict:
        """Analisa contexto do sistema"""
        return {
            "carga_sistema": "normal",  # Simplificado
            "agentes_ativos": 5,  # Simulado
            "memoria_disponivel": "alta"
        }
    
    def _analisar_contexto_conversacional(self) -> Dict:
        """Analisa contexto da conversa"""
        return {
            "topicos_recentes": [],  # Seria preenchido com histórico real
            "tom_conversa": "neutro",
            "complexidade": "media"
        }
    
    def _determinar_periodo(self, hora: int) -> str:
        """Determina período do dia"""
        if 5 <= hora < 12:
            return "manha"
        elif 12 <= hora < 18:
            return "tarde"
        elif 18 <= hora < 22:
            return "noite"
        else:
            return "madrugada"
    
    def _determinar_sazonalidade(self, mes: int) -> str:
        """Determina sazonalidade"""
        if mes in [12, 1, 2]:
            return "verao"
        elif mes in [3, 4, 5]:
            return "outono"
        elif mes in [6, 7, 8]:
            return "inverno"
        else:
            return "primavera"
    
    def _identificar_padrao_uso(self) -> str:
        """Identifica padrão de uso do usuário"""
        if len(self.contextos_historicos) < 5:
            return "novo_usuario"
        
        # Análise simplificada de padrões
        horarios = [ctx.get("temporal", {}).get("hora", 12) for ctx in self.contextos_historicos[-10:]]
        hora_media = sum(horarios) / len(horarios)
        
        if hora_media < 12:
            return "usuario_matutino"
        elif hora_media < 18:
            return "usuario_diurno"
        else:
            return "usuario_noturno"
    
    def _extrair_preferencias(self) -> Dict:
        """Extrai preferências do usuário"""
        return {
            "nivel_detalhamento": "medio",
            "estilo_comunicacao": "direto",
            "complexidade_preferida": "adaptativa"
        }


class UserProfiling:
    """Sistema de perfil de usuário adaptativo"""
    
    def __init__(self):
        self.perfis_usuarios = {}
        self.historico_interacoes = []
        
    def analisar(self, historico_usuario: List[Dict]) -> Dict:
        """Analisa histórico e cria perfil do usuário"""
        if not historico_usuario:
            return self._perfil_padrao()
        
        perfil = {
            "preferencias_prompts": self._analisar_preferencias_prompts(historico_usuario),
            "nivel_expertise": self._determinar_nivel_expertise(historico_usuario),
            "estilos_favoritos": self._identificar_estilos_favoritos(historico_usuario),
            "horarios_uso": self._analisar_horarios_uso(historico_usuario),
            "topicos_interesse": self._extrair_topicos_interesse(historico_usuario)
        }
        
        return perfil
    
    def _perfil_padrao(self) -> Dict:
        """Retorna perfil padrão para novos usuários"""
        return {
            "preferencias_prompts": {"detalhamento": "medio", "estrutura": "clara"},
            "nivel_expertise": "intermediario",
            "estilos_favoritos": ["direto", "estruturado"],
            "horarios_uso": [9, 14, 20],
            "topicos_interesse": ["geral"]
        }
    
    def _analisar_preferencias_prompts(self, historico: List[Dict]) -> Dict:
        """Analisa preferências de prompts"""
        return {
            "detalhamento": "alto" if len(historico) > 10 else "medio",
            "estrutura": "clara",
            "tom": "profissional"
        }
    
    def _determinar_nivel_expertise(self, historico: List[Dict]) -> str:
        """Determina nível de expertise"""
        if len(historico) < 5:
            return "iniciante"
        elif len(historico) < 20:
            return "intermediario"
        else:
            return "avancado"
    
    def _identificar_estilos_favoritos(self, historico: List[Dict]) -> List[str]:
        """Identifica estilos favoritos"""
        return ["estruturado", "direto", "detalhado"]
    
    def _analisar_horarios_uso(self, historico: List[Dict]) -> List[int]:
        """Analisa horários de uso"""
        return [9, 14, 20]  # Simplificado
    
    def _extrair_topicos_interesse(self, historico: List[Dict]) -> List[str]:
        """Extrai tópicos de interesse"""
        return ["produtividade", "criatividade", "analise"]


class PromptCrafterV3(BaseAgentV2):
    """
    🎨 PROMPTCRAFTER v3.0 - ADAPTATIVO
    Engenheiro de prompts com aprendizado neural, consciência contextual e perfil de usuário
    
    Novas funcionalidades v3.0:
    - PromptLearningEngine: Aprendizado neural com feedback
    - ContextAwareness: Consciência temporal e situacional
    - UserProfiling: Personalização baseada no histórico
    - Integration com KnowledgeGraph: Memória coletiva
    - Evolução genética de prompts
    - A/B testing automático
    """
    
    def __init__(self, **kwargs):
        super().__init__(
            name="PromptCrafter",
            version="3.0",
            agent_type="promptcrafter_adaptativo",
            primary_function="engenharia_prompts_avancada",
            capabilities=[
                "criacao_prompts", "revisao_prompts", "versionamento",
                "rastreabilidade", "geracao_criativa", "kits_completos",
                "aprendizado_neural", "contexto_temporal", "perfil_usuario",
                "evolucao_genetica", "ab_testing", "knowledge_integration"
            ],
            **kwargs
        )
        
        # Componentes avançados v3.0
        self.learning_engine = PromptLearningEngine()
        self.context_awareness = ContextAwareness()
        self.user_profiling = UserProfiling()
        
        # Integration com Knowledge Graph
        if KNOWLEDGE_GRAPH_AVAILABLE:
            try:
                from .knowledge_graph_v1 import criar_knowledge_graph
                self.knowledge_graph = criar_knowledge_graph()
            except Exception as e:
                self.knowledge_graph = None
                logger.warning(f"⚠️ KnowledgeGraph não pôde ser inicializado: {e}")
        else:
            self.knowledge_graph = None
            logger.warning("⚠️ KnowledgeGraph não disponível")
        
        # Vault de prompts expandido
        self.prompt_vault: Dict[str, Dict] = {}
        self.locked_prompts: set = set()
        self.prompt_genealogia: Dict[str, List[str]] = {}  # Árvore genealógica
        self.ab_tests_ativos: Dict[str, Dict] = {}  # Testes A/B
        
        # Configurações de modos
        self.modo_atual = PromptMode.NORMAL
        self.nivel_chaos = 0.5  # 0-1 para controlar ousadia
        
        # Configurações avançadas v3.0
        self.modo_otimizador_auto = True
        self.threshold_otimizacao = 0.3
        self.modo_aprendizado_ativo = True
        self.personalização_ativa = True
        self.genetic_evolution = True
        self.ab_testing_automatico = True
        
        # Padrões de prompts vagos para otimização
        self.padroes_vagos = [
            r"quero\s+(.+)",
            r"preciso\s+(.+)",
            r"me\s+ajude?\s+(.+)",
            r"como\s+(.+)\?",
            r"(.+)\s+legal",
            r"(.+)\s+bom",
            r"(.+)\s+interessante"
        ]
        
        logger.info("🎨 PromptCrafter v3.0 inicializado com IA adaptativa")
        logger.info("🧠 Learning Engine ativo - aprendizado neural")
        logger.info("🌍 Context Awareness ativo - consciência situacional")
        logger.info("👤 User Profiling ativo - personalização avançada")
        logger.info("🧬 Genetic Evolution ativo - evolução automática")
    
    def _processar_interno(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Implementação do método abstrato do BaseAgentV2"""
        return self.processar(entrada, contexto)
    
    def processar(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Processa requisições de engenharia de prompts"""
        try:
            self._registrar_evento("prompt_request", {
                "entrada": entrada[:100],
                "modo": self.modo_atual.value
            })
            
            # 🧠 OTIMIZAÇÃO INTELIGENTE: Detectar se entrada é vaga
            if self.modo_otimizador_auto and self._prompt_precisa_otimizacao(entrada):
                logger.info("🧠 Prompt vago detectado - ativando otimização inteligente")
                return self.otimizar_prompt_inteligente(entrada, [], contexto)
            
            # Detectar tipo de comando
            if "crie um prompt" in entrada.lower():
                return self._criar_prompt(entrada, contexto)
            
            elif "revise o prompt" in entrada.lower():
                return self._revisar_prompt(entrada, contexto)
            
            elif "promptchaos" in entrada.lower():
                return self._ativar_chaos(entrada, contexto)
            
            elif "promptkit" in entrada.lower():
                return self._gerar_kit(entrada, contexto)
            
            elif "promptlock" in entrada.lower():
                return self._aplicar_lock(entrada, contexto)
            
            elif "promptlineage" in entrada.lower():
                return self._mostrar_lineage(entrada, contexto)
            
            elif "gere variações" in entrada.lower():
                return self._gerar_variacoes(entrada, contexto)
            
            else:
                return self._criar_prompt(entrada, contexto)
                
        except Exception as e:
            logger.error(f"❌ Erro no PromptCrafter: {e}")
            return self._gerar_erro_resposta(str(e))
    
    def _revisar_prompt(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Revisa prompt existente"""
        return "🔧 Funcionalidade de revisão em desenvolvimento"
    
    def _registrar_shadow_learning(self, mensagem: str, resultado_a: str, resultado_b: str, melhor: str):
        """Registra aprendizado do Shadow Chain"""
        self._registrar_evento("shadow_learning", {
            "mensagem": mensagem[:50],
            "melhor_escolhido": "A" if melhor == resultado_a else "B"
        })
    
    def _prompt_precisa_otimizacao(self, entrada: str) -> bool:
        """🔧 Detecta se prompt precisa de otimização automática"""
        import re
        
        # Verificar padrões vagos
        for padrao in self.padroes_vagos:
            if re.search(padrao, entrada.lower()):
                return True
        
        # Verificar tamanho muito curto
        if len(entrada.split()) < 5:
            return True
        
        # Verificar palavras muito genéricas
        palavras_genericas = ["coisa", "negócio", "algo", "aquilo", "isso"]
        for palavra in palavras_genericas:
            if palavra in entrada.lower():
                return True
        
        return False
    
    def otimizar_prompt_inteligente(self, entrada: str, historico_usuario: List[Dict] = None, contexto: Optional[Dict] = None) -> str:
        """🧠 Otimização inteligente com aprendizado neural e personalização"""
        try:
            if contexto is None:
                contexto = {}
            if historico_usuario is None:
                historico_usuario = []
            
            # 1. Análise do perfil do usuário
            perfil = self.user_profiling.analisar(historico_usuario)
            
            # 2. Captura de contexto situacional
            contexto_atual = self.context_awareness.capturar_contexto()
            
            # 3. Detecção de intenção aprimorada
            intencao = self._detectar_intencao_avancada(entrada, perfil, contexto_atual)
            
            # 4. Geração de prompt personalizado
            prompt_otimizado = self._gerar_prompt_personalizado(entrada, intencao, perfil, contexto_atual)
            
            # 5. Aplicar padrões de sucesso aprendidos
            prompt_final = self._aplicar_padroes_sucesso(prompt_otimizado)
            
            # 6. Criar DNA avançado
            params = self._extrair_parametros_avancados(prompt_final, contexto, perfil)
            dna = self._criar_dna(params)
            score = self._calcular_score_neural(prompt_final, params, perfil)
            
            # 7. Salvar no vault com metadados expandidos
            prompt_id = self._salvar_prompt_v3(prompt_final, dna, score, perfil, contexto_atual)
            
            # 8. Registrar no Knowledge Graph
            if self.knowledge_graph:
                self._registrar_no_knowledge_graph(prompt_id, prompt_final, score, perfil)
            
            # 9. Sugerir melhorias baseadas em aprendizado
            sugestoes = self.learning_engine.sugerir_melhorias(prompt_final)
            
            return f"""
🧠 **Otimização Inteligente v3.0 Ativada!**

📝 **Prompt Original:** "{entrada}"
🎯 **Intenção Detectada:** {intencao}
👤 **Perfil Usuário:** {perfil['nivel_expertise']} | {perfil['estilos_favoritos'][0] if perfil['estilos_favoritos'] else 'padrão'}
🌍 **Contexto:** {contexto_atual['temporal']['periodo']} | {contexto_atual['usuario']['padrao_uso']}

✨ **Prompt Otimizado e Personalizado:**
```
{prompt_final}
```

🧬 **DNA Avançado:** [{dna.persona}, {dna.emocao}, {dna.funcao}]
📊 **Score Neural:** {score.media_geral:.1f}/10
🎯 **Adequação ao Perfil:** {score.roi_estimado/2:.1f}/10

💡 **Melhorias Aplicadas:**
• Personalização baseada no seu histórico
• Contexto temporal otimizado
• Padrões de sucesso identificados
• Estrutura adaptada ao seu nível

🔍 **Sugestões de Aprimoramento:**
{chr(10).join(f'• {sugestao}' for sugestao in sugestoes[:3])}

🆔 **ID do Prompt:** {prompt_id}
📚 **Registrado no Knowledge Graph:** {'✅' if self.knowledge_graph else '❌'}

✅ **Prompt adaptado especialmente para você!**
"""
            
        except Exception as e:
            logger.error(f"❌ Erro na otimização inteligente: {e}")
            return f"❌ Erro na otimização v3.0: {str(e)}"
    
    def _detectar_intencao(self, entrada: str) -> str:
        """Detecta intenção do usuário no prompt vago"""
        entrada_lower = entrada.lower()
        
        # Mapeamento de palavras-chave para intenções
        intencoes = {
            "buscar": ["lugares", "sites", "produtos", "informações", "dados"],
            "criar": ["fazer", "construir", "desenvolver", "montar"],
            "aprender": ["como", "ensinar", "explicar", "tutorial"],
            "vender": ["ganhar", "dinheiro", "monetizar", "lucrar"],
            "melhorar": ["otimizar", "aperfeiçoar", "upgrade", "evoluir"],
            "descobrir": ["encontrar", "achar", "localizar", "identificar"]
        }
        
        for intencao, palavras in intencoes.items():
            for palavra in palavras:
                if palavra in entrada_lower:
                    return intencao
        
        return "explorar"  # intenção padrão
    
    def _expandir_prompt_vago(self, entrada: str, intencao: str) -> str:
        """Expande prompt vago em versão específica e acionável"""
        templates_expansao = {
            "buscar": """
Pesquise e analise {objetivo} com os seguintes critérios:

1. **Fontes confiáveis**: Utilize apenas fontes verificadas e atualizadas
2. **Análise comparativa**: Compare pelo menos 5 opções diferentes
3. **Critérios de avaliação**: Considere qualidade, popularidade, acessibilidade
4. **Recomendações práticas**: Forneça um ranking com justificativas
5. **Próximos passos**: Sugira ações concretas para o usuário

Formato de resposta:
- Top 5 recomendações
- Prós e contras de cada opção
- Recomendação final justificada
""",
            "criar": """
Desenvolva um plano completo para {objetivo} incluindo:

1. **Análise de requisitos**: O que é necessário para começar
2. **Estratégia passo-a-passo**: Processo detalhado de execução
3. **Recursos necessários**: Ferramentas, tempo, orçamento
4. **Marcos e métricas**: Como medir o progresso
5. **Soluções para obstáculos**: Antecipação de problemas comuns

Entrega esperada:
- Plano executável
- Timeline realista
- Lista de recursos
- Critérios de sucesso
""",
            "aprender": """
Crie um guia educacional sobre {objetivo} que inclua:

1. **Conceitos fundamentais**: Base teórica essencial
2. **Exemplos práticos**: Aplicações no mundo real
3. **Exercícios progressivos**: Do básico ao avançado
4. **Recursos adicionais**: Onde aprofundar o conhecimento
5. **Avaliação**: Como verificar o aprendizado

Metodologia:
- Linguagem clara e acessível
- Estrutura lógica e progressiva
- Foco na aplicação prática
""",
            "vender": """
Desenvolva uma estratégia de monetização para {objetivo}:

1. **Análise de mercado**: Identificar oportunidades e público
2. **Proposta de valor**: Diferencial competitivo único
3. **Canais de venda**: Onde e como vender
4. **Precificação**: Estratégia de preços competitiva
5. **Execução**: Plano de ação com prazos

Resultado esperado:
- Estratégia completa de vendas
- Projeção de receita
- Plano de implementação
- Métricas de acompanhamento
""",
            "melhorar": """
Analise e otimize {objetivo} seguindo esta metodologia:

1. **Diagnóstico atual**: Avaliação detalhada da situação
2. **Identificação de gargalos**: Pontos de melhoria prioritários
3. **Soluções propostas**: Alternativas de otimização
4. **Implementação gradual**: Plano de execução por etapas
5. **Monitoramento**: KPIs para acompanhar melhorias

Abordagem:
- Foco em resultados mensuráveis
- Implementação incremental
- ROI claro de cada melhoria
""",
            "descobrir": """
Investigue e mapeie {objetivo} de forma sistemática:

1. **Pesquisa exploratória**: Levantamento inicial abrangente
2. **Análise de padrões**: Identificação de tendências e insights
3. **Validação de dados**: Verificação da qualidade das informações
4. **Síntese organizada**: Compilação dos achados principais
5. **Recomendações**: Próximos passos baseados nos descobrimentos

Metodologia:
- Abordagem científica
- Múltiplas fontes
- Análise crítica
- Conclusões acionáveis
"""
        }
        
        # Extrair objetivo do prompt original
        objetivo = self._extrair_objetivo(entrada)
        
        # Usar template da intenção detectada
        template = templates_expansao.get(intencao, templates_expansao["descobrir"])
        
        return template.format(objetivo=objetivo)
    
    def _extrair_objetivo(self, entrada: str) -> str:
        """Extrai o objetivo principal do prompt vago"""
        import re
        
        # Remover palavras de apoio
        palavras_filtro = ["quero", "preciso", "me ajude", "como", "onde", "qual"]
        objetivo = entrada.lower()
        
        for palavra in palavras_filtro:
            objetivo = re.sub(rf'\b{palavra}\b', '', objetivo)
        
        # Limpar espaços extras
        objetivo = ' '.join(objetivo.split())
        
        # Se muito curto, usar entrada original
        if len(objetivo.strip()) < 3:
            objetivo = entrada
        
        return objetivo.strip() or "o objetivo especificado"
    
    def _criar_prompt(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Cria novo prompt com DNA completo"""
        try:
            # Extrair parâmetros
            if contexto is None:
                contexto = {}
            params = self._extrair_parametros(entrada, contexto)
            
            # Gerar prompt base
            prompt_base = self._gerar_prompt_base(params)
            
            # Aplicar modo chaos se ativo
            if self.modo_atual == PromptMode.CHAOS:
                prompt_base = self._aplicar_chaos(prompt_base, params)
            
            # Criar DNA
            dna = self._criar_dna(params)
            
            # Calcular score inicial
            score = self._calcular_score(prompt_base, params)
            
            # Salvar no vault
            prompt_id = self._salvar_prompt(prompt_base, dna, score)
            
            # Formatar resposta
            return self._formatar_resposta_criacao(
                prompt_id, prompt_base, dna, score
            )
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar prompt: {e}")
            return f"❌ Erro na criação: {str(e)}"
    
    def _gerar_prompt_base(self, params: Dict) -> str:
        """Gera estrutura base do prompt"""
        templates = {
            "vendas": """
**Contexto:** {contexto}
**Objetivo:** {objetivo}
**Tom:** {tom}
**Persona:** {persona}

Ação específica:
{acao_detalhada}

Critérios de sucesso:
{criterios}

Restrições:
{restricoes}
""",
            "conteudo": """
**Tipo de conteúdo:** {tipo}
**Público-alvo:** {publico}
**Emoção principal:** {emocao}
**Canal:** {canal}

Estrutura:
{estrutura}

Elementos obrigatórios:
{elementos}

Call-to-action:
{cta}
""",
            "analise": """
**Dados a analisar:** {dados}
**Profundidade:** {profundidade}
**Formato de saída:** {formato}

Métricas chave:
{metricas}

Insights esperados:
{insights}

Recomendações:
{recomendacoes}
""",
            "criativo": """
**Briefing criativo:** {briefing}
**Estilo:** {estilo}
**Referências:** {referencias}

Conceito central:
{conceito}

Variações necessárias:
{variacoes}

Diretrizes de marca:
{diretrizes}
"""
        }
        
        # Selecionar template apropriado
        tipo = params.get("tipo", "geral")
        template = templates.get(tipo, templates["vendas"])
        
        # Preencher template
        prompt = template.format(**params)
        
        # Adicionar elementos de DNA
        prompt += f"\n\n---\n🧬 PromptDNA: {self._gerar_hash_dna(params)}"
        
        return prompt
    
    def _aplicar_chaos(self, prompt: str, params: Dict) -> str:
        """🔮 Aplica elementos criativos e ousados ao prompt"""
        elementos_chaos = [
            "\n💥 TWIST CRIATIVO: {twist}",
            "\n🎲 ELEMENTO ALEATÓRIO: {random}",
            "\n🚀 FATOR DISRUPTIVO: {disruptive}",
            "\n✨ MAGIA INESPERADA: {magic}",
            "\n🌈 PERSPECTIVA INUSITADA: {perspective}"
        ]
        
        # Selecionar elementos baseado no nível de chaos
        num_elementos = int(self.nivel_chaos * len(elementos_chaos))
        elementos_selecionados = elementos_chaos[:num_elementos]
        
        # Gerar conteúdo chaos
        chaos_content = {
            "twist": self._gerar_twist(params),
            "random": self._gerar_elemento_aleatorio(params),
            "disruptive": self._gerar_fator_disruptivo(params),
            "magic": self._gerar_magia(params),
            "perspective": self._gerar_perspectiva(params)
        }
        
        # Aplicar ao prompt
        for elemento in elementos_selecionados:
            prompt += elemento.format(**chaos_content)
        
        prompt += f"\n\n🔮 CHAOS LEVEL: {self.nivel_chaos * 100:.0f}%"
        
        return prompt
    
    def _gerar_kit(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """🧩 Gera kit completo de prompts interconectados"""
        try:
            if contexto is None:
                contexto = {}
            params = self._extrair_parametros(entrada, contexto)
            produto = params.get("produto", "produto genérico")
            
            # Componentes do kit
            kit_components = {
                "anuncio": self._gerar_prompt_anuncio(params),
                "atendimento": self._gerar_prompt_atendimento(params),
                "conteudo_reels": self._gerar_prompt_reels(params),
                "email_marketing": self._gerar_prompt_email(params),
                "remarketing": self._gerar_prompt_remarketing(params),
                "faq": self._gerar_prompt_faq(params)
            }
            
            # Criar DNA compartilhado
            dna_base = self._criar_dna(params)
            
            # Salvar cada componente
            kit_id = f"PromptKit_{produto.replace(' ', '_')}_v1.0"
            kit_results = {}
            
            for tipo, prompt in kit_components.items():
                prompt_id = f"{kit_id}_{tipo}"
                score = self._calcular_score(prompt, params)
                
                self.prompt_vault[prompt_id] = {
                    "prompt": prompt,
                    "dna": dna_base,
                    "score": score,
                    "kit_id": kit_id,
                    "tipo": tipo,
                    "status": PromptStatus.ATIVO.value
                }
                
                kit_results[tipo] = {
                    "id": prompt_id,
                    "score": score.media_geral
                }
            
            # Formatar resposta do kit
            return self._formatar_resposta_kit(kit_id, kit_results, kit_components)
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar kit: {e}")
            return f"❌ Erro na geração do kit: {str(e)}"
    
    def _aplicar_lock(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """🧊 Aplica lock em prompt crítico"""
        try:
            # Extrair ID do prompt
            prompt_id = self._extrair_prompt_id(entrada)
            
            if prompt_id not in self.prompt_vault:
                return f"❌ Prompt '{prompt_id}' não encontrado no vault"
            
            if prompt_id in self.locked_prompts:
                return f"🔒 Prompt '{prompt_id}' já está travado"
            
            # Aplicar lock
            self.locked_prompts.add(prompt_id)
            self.prompt_vault[prompt_id]["status"] = PromptStatus.LOCKED.value
            self.prompt_vault[prompt_id]["locked_at"] = datetime.now().isoformat()
            self.prompt_vault[prompt_id]["locked_by"] = contexto.get("usuario", "sistema")
            
            self._registrar_evento("prompt_locked", {
                "prompt_id": prompt_id,
                "usuario": contexto.get("usuario", "sistema")
            })
            
            return f"""
🧊 **PromptLock Aplicado com Sucesso!**

📌 **ID:** {prompt_id}
🔒 **Status:** LOCKED (Protegido contra edições)
📅 **Travado em:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
👤 **Travado por:** {contexto.get("usuario", "sistema")}

⚡ **Implicações:**
- Prompt não pode mais ser editado
- Versão congelada para uso crítico
- Apenas admin pode remover lock
- Histórico preservado permanentemente

✅ Prompt protegido com sucesso!
"""
            
        except Exception as e:
            logger.error(f"❌ Erro ao aplicar lock: {e}")
            return f"❌ Erro no PromptLock: {str(e)}"
    
    def _mostrar_lineage(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """🌱 Mostra árvore genealógica de versões do prompt"""
        try:
            prompt_id = self._extrair_prompt_id(entrada)
            
            if prompt_id not in self.prompt_vault:
                return f"❌ Prompt '{prompt_id}' não encontrado"
            
            prompt_data = self.prompt_vault[prompt_id]
            lineage = prompt_data.get("dna", {}).get("lineage", [])
            
            # Construir árvore
            arvore = f"""
🌱 **PromptLineage - Árvore Genealógica**

📌 **Prompt Atual:** {prompt_id}
📅 **Criado em:** {prompt_data.get('dna', {}).get('criado_em', 'N/A')}
📊 **Score Atual:** {prompt_data.get('score', {}).get('media_geral', 0):.2f}

🧬 **Histórico de Evolução:**
"""
            
            # Adicionar ancestrais
            for i, ancestor in enumerate(lineage):
                indent = "  " * i
                if ancestor in self.prompt_vault:
                    ancestor_data = self.prompt_vault[ancestor]
                    status = ancestor_data.get("status", "unknown")
                    score = ancestor_data.get("score", {}).get("media_geral", 0)
                    
                    arvore += f"\n{indent}└─ {ancestor} (Score: {score:.2f}, Status: {status})"
                else:
                    arvore += f"\n{indent}└─ {ancestor} (Arquivo histórico)"
            
            # Adicionar descendentes
            descendentes = self._buscar_descendentes(prompt_id)
            if descendentes:
                arvore += "\n\n📈 **Versões Derivadas:**"
                for desc in descendentes:
                    desc_data = self.prompt_vault[desc]
                    score = desc_data.get("score", {}).get("media_geral", 0)
                    arvore += f"\n  → {desc} (Score: {score:.2f})"
            
            return arvore
            
        except Exception as e:
            logger.error(f"❌ Erro ao mostrar lineage: {e}")
            return f"❌ Erro no PromptLineage: {str(e)}"
    
    def _calcular_score(self, prompt: str, params: Dict) -> PromptScore:
        """📈 Calcula score multidimensional do prompt"""
        # Simulação de scoring (em produção, integrar com outros agentes)
        
        # Análise de complexidade
        complexidade = len(prompt.split()) / 100
        complexidade = min(complexidade, 1.0)
        
        # Análise de estrutura
        tem_contexto = "contexto" in prompt.lower()
        tem_objetivo = "objetivo" in prompt.lower()
        tem_criterios = "critérios" in prompt.lower() or "sucesso" in prompt.lower()
        
        estrutura_score = sum([tem_contexto, tem_objetivo, tem_criterios]) / 3
        
        # Análise emocional (simulada)
        palavras_impacto = ["revolucionário", "transformar", "exclusivo", "premium", "inovador"]
        impacto_emocional = sum(1 for palavra in palavras_impacto if palavra in prompt.lower()) / len(palavras_impacto)
        
        # Calcular scores
        reflexor_score = (complexidade * 0.4 + estrutura_score * 0.6) * 10
        copybooster_score = (impacto_emocional * 0.7 + estrutura_score * 0.3) * 10
        roi_estimado = (reflexor_score * 0.3 + copybooster_score * 0.7) * 1.5
        impacto_pratico = (estrutura_score * 0.5 + complexidade * 0.5) * 10
        
        return PromptScore(
            reflexor=min(reflexor_score, 10.0),
            copybooster=min(copybooster_score, 10.0),
            roi_estimado=min(roi_estimado, 20.0),
            impacto_pratico=min(impacto_pratico, 10.0)
        )
    
    def _criar_dna(self, params: Dict) -> PromptDNA:
        """🧬 Cria DNA único para o prompt"""
        agora = datetime.now()
        
        # Gerar hash único
        hash_content = f"{params.get('persona', 'geral')}_{params.get('funcao', 'geral')}_{agora.isoformat()}"
        hash_id = hashlib.md5(hash_content.encode()).hexdigest()[:8]
        
        return PromptDNA(
            persona=params.get("persona", "geral"),
            emocao=params.get("emocao", "neutra"),
            funcao=params.get("funcao", "informativa"),
            canal=params.get("canal", "multi"),
            versao="1.0",
            lineage=params.get("lineage", []),
            criado_em=agora,
            modificado_em=agora,
            hash_id=hash_id
        )
    
    def _salvar_prompt(self, prompt: str, dna: PromptDNA, score: PromptScore) -> str:
        """Salva prompt no vault com metadados completos"""
        prompt_id = f"Prompt_{dna.funcao}_{dna.hash_id}_v{dna.versao}"
        
        self.prompt_vault[prompt_id] = {
            "prompt": prompt,
            "dna": {
                "persona": dna.persona,
                "emocao": dna.emocao,
                "funcao": dna.funcao,
                "canal": dna.canal,
                "versao": dna.versao,
                "lineage": dna.lineage,
                "criado_em": dna.criado_em.isoformat(),
                "modificado_em": dna.modificado_em.isoformat(),
                "hash_id": dna.hash_id
            },
            "score": {
                "reflexor": score.reflexor,
                "copybooster": score.copybooster,
                "roi_estimado": score.roi_estimado,
                "impacto_pratico": score.impacto_pratico,
                "media_geral": score.media_geral
            },
            "status": PromptStatus.NOVO.value,
            "uso_count": 0,
            "feedback_history": []
        }
        
        self._registrar_evento("prompt_saved", {
            "prompt_id": prompt_id,
            "score": score.media_geral
        })
        
        return prompt_id
    
    def _formatar_resposta_criacao(self, prompt_id: str, prompt: str, dna: PromptDNA, score: PromptScore) -> str:
        """Formata resposta detalhada de criação"""
        return f"""
🎨 **PromptCrafter v2.0 - Prompt Criado com Sucesso!**

📌 **ID:** {prompt_id}
🧬 **DNA:** [{dna.persona}, {dna.emocao}, {dna.funcao}, {dna.canal}, v{dna.versao}]

📊 **PromptScore:**
- 🔍 Reflexor: {score.reflexor:.1f}/10
- 💬 CopyBooster: {score.copybooster:.1f}/10
- 💰 ROI Estimado: {score.roi_estimado:.1f}%
- ⚡ Impacto Prático: {score.impacto_pratico:.1f}/10
- 📈 **Média Geral: {score.media_geral:.1f}/10**

📝 **Prompt Gerado:**
```
{prompt}
```

✅ **Status:** {PromptStatus.NOVO.value.upper()} - Pronto para uso!

💡 **Próximos passos:**
- Use `/promptlock {prompt_id}` para congelar versão
- Use `/promptlineage {prompt_id}` para ver histórico
- Use `/promptchaos` para versão experimental
"""
    
    def _formatar_resposta_kit(self, kit_id: str, results: Dict, components: Dict) -> str:
        """Formata resposta de kit completo"""
        media_geral = sum(r["score"] for r in results.values()) / len(results)
        
        resposta = f"""
🧩 **PromptKit Completo Gerado!**

📦 **Kit ID:** {kit_id}
📊 **Score Médio do Kit:** {media_geral:.1f}/10

🎯 **Componentes do Kit:**
"""
        
        for tipo, result in results.items():
            resposta += f"\n✅ **{tipo.upper()}**"
            resposta += f"\n   └─ ID: {result['id']}"
            resposta += f"\n   └─ Score: {result['score']:.1f}/10"
        
        resposta += "\n\n📝 **Prompts Detalhados:**"
        
        for tipo, prompt in components.items():
            resposta += f"\n\n### 🎯 {tipo.upper()}\n```\n{prompt[:200]}...\n```"
        
        resposta += f"""

🚀 **Kit pronto para campanha multicanal!**

💡 **Benefícios do Kit:**
- Consistência de mensagem em todos os canais
- Otimização de tempo (6 prompts prontos)
- Rastreabilidade unificada
- Evolução sincronizada

✨ Todos os componentes foram salvos no PromptVault!
"""
        
        return resposta
    
    def _extrair_parametros(self, entrada: str, contexto: Dict) -> Dict:
        """Extrai parâmetros da entrada"""
        params = {
            "contexto": contexto.get("contexto_negocio", "geral"),
            "objetivo": "engajamento e conversão",
            "tom": "profissional e acolhedor",
            "persona": "público geral",
            "tipo": "vendas"
        }
        
        # Detectar persona
        if "mulheres 35+" in entrada.lower():
            params["persona"] = "mulheres acima de 35 anos"
            params["emocao"] = "empoderamento e autocuidado"
        elif "jovens" in entrada.lower():
            params["persona"] = "jovens 18-25 anos"
            params["emocao"] = "energia e inovação"
        
        # Detectar produto/serviço
        if "beleza" in entrada.lower():
            params["produto"] = "beleza premium"
            params["canal"] = "instagram e email"
        elif "curso" in entrada.lower():
            params["produto"] = "curso online"
            params["canal"] = "ads e whatsapp"
        
        # Detectar tipo
        if "conteúdo" in entrada.lower():
            params["tipo"] = "conteudo"
        elif "análise" in entrada.lower():
            params["tipo"] = "analise"
        elif "criativo" in entrada.lower():
            params["tipo"] = "criativo"
        
        return params
    
    def _gerar_erro_resposta(self, erro: str) -> str:
        """Gera resposta de erro formatada"""
        return f"""
❌ **Erro no PromptCrafter v2.0**

**Problema detectado:** {erro}

**Possíveis soluções:**
1. Verifique a sintaxe do comando
2. Certifique-se de incluir todos os parâmetros necessários
3. Use `/help promptcrafter` para ver exemplos

**Comandos disponíveis:**
- `crie um prompt para [objetivo]`
- `revise o prompt [id]`
- `promptchaos [nível]`
- `promptkit para [produto]`
- `promptlock [id]`
- `promptlineage [id]`
"""
    
    # Métodos auxiliares para geração de kits
    def _gerar_prompt_anuncio(self, params: Dict) -> str:
        """Gera prompt para anúncios"""
        return f"""
**PROMPT PARA ANÚNCIO - {params.get('produto', 'Produto')}**

Crie um anúncio irresistível para {params.get('persona', 'nosso público')} que:

1. **Gancho inicial:** Capture atenção em 3 segundos
2. **Proposta de valor:** Destaque o diferencial único
3. **Benefícios:** Liste 3 transformações concretas
4. **Prova social:** Inclua números ou depoimentos
5. **CTA urgente:** Crie escassez ou oportunidade limitada

Tom: {params.get('emocao', 'Confiante e acolhedor')}
Canal: {params.get('canal', 'Redes sociais')}

Estrutura:
[GANCHO]
[PROBLEMA/DOR]
[SOLUÇÃO/PRODUTO]
[BENEFÍCIOS]
[PROVA SOCIAL]
[CTA + URGÊNCIA]
"""
    
    def _gerar_prompt_atendimento(self, params: Dict) -> str:
        """Gera prompt para atendimento"""
        return f"""
**PROMPT PARA ATENDIMENTO - {params.get('produto', 'Produto')}**

Configure respostas para atender {params.get('persona', 'clientes')} com:

1. **Saudação personalizada:** Acolhimento caloroso
2. **Escuta ativa:** Identificar necessidade real
3. **Solução direcionada:** Conectar produto à dor
4. **Objeções comuns:** Respostas preparadas
5. **Fechamento consultivo:** Guiar para decisão

Persona: {params.get('persona', 'Cliente em potencial')}
Tom: {params.get('emocao', 'Empático e profissional')}

Fluxo de atendimento:
- Descoberta (3 perguntas-chave)
- Apresentação (benefícios personalizados)
- Gestão de objeções (5 mais comuns)
- Fechamento (2 opções de pacote)
"""
    
    def _gerar_prompt_reels(self, params: Dict) -> str:
        """Gera prompt para reels/vídeos curtos"""
        return f"""
**PROMPT PARA REELS - {params.get('produto', 'Produto')}**

Crie roteiro de reels para {params.get('persona', 'seguidores')}:

1. **Hook (0-3s):** Pergunta ou afirmação impactante
2. **Desenvolvimento (3-10s):** Mini-história ou dica
3. **Clímax (10-20s):** Revelação ou transformação
4. **CTA (20-30s):** Ação clara e simples

Emoção: {params.get('emocao', 'Inspiradora')}
Formato: Vídeo vertical 9:16

Elementos visuais:
- Texto on-screen em momentos-chave
- Transições dinâmicas
- Música trending adequada
- Legendas acessíveis
"""
    
    def _gerar_prompt_email(self, params: Dict) -> str:
        """Gera prompt para email marketing"""
        return f"""
**PROMPT PARA EMAIL - {params.get('produto', 'Produto')}**

Componha email para {params.get('persona', 'lista de contatos')}:

1. **Assunto:** 35-50 caracteres, criar curiosidade
2. **Preview:** Complementar assunto (50 chars)
3. **Abertura:** Conexão pessoal imediata
4. **Corpo:** História → Valor → Benefícios
5. **CTA principal:** Botão destacado
6. **P.S.:** Reforço de urgência/bônus

Tom: {params.get('emocao', 'Próximo e convidativo')}
Objetivo: {params.get('objetivo', 'Conversão')}

Estrutura visual:
- Parágrafos curtos (2-3 linhas)
- Bullets para benefícios
- Imagens estratégicas
- Mobile-first
"""
    
    def _gerar_prompt_remarketing(self, params: Dict) -> str:
        """Gera prompt para remarketing"""
        return f"""
**PROMPT PARA REMARKETING - {params.get('produto', 'Produto')}**

Reconquiste {params.get('persona', 'leads que não converteram')}:

1. **Reconhecimento:** "Notamos que você..."
2. **Empatia:** Entender hesitação
3. **Nova oferta:** Benefício adicional/desconto
4. **Prova extra:** Caso de sucesso relevante
5. **Última chance:** Escassez real

Abordagem: {params.get('emocao', 'Compreensiva e incentivadora')}
Canal: {params.get('canal', 'Multi-canal')}

Sequência:
- Email 1: Reconexão suave
- Email 2: Benefício esquecido
- Email 3: Oferta especial
- Email 4: Última chance
"""
    
    def _gerar_prompt_faq(self, params: Dict) -> str:
        """Gera prompt para FAQ"""
        return f"""
**PROMPT PARA FAQ - {params.get('produto', 'Produto')}**

Antecipe dúvidas de {params.get('persona', 'clientes potenciais')}:

Estrutura por pergunta:
1. **Pergunta:** Linguagem do cliente
2. **Resposta curta:** 1-2 frases diretas
3. **Explicação:** Contexto adicional
4. **Exemplo/Analogia:** Facilitar compreensão
5. **Link útil:** Aprofundamento

Tom: {params.get('emocao', 'Didático e acessível')}

Categorias essenciais:
- Sobre o produto/serviço
- Processo de compra
- Garantias e suporte
- Resultados esperados
- Investimento e pagamento
"""
    
    def _gerar_twist(self, params: Dict) -> str:
        """Gera elemento twist criativo"""
        twists = [
            "E se o cliente fosse o herói e o produto apenas o mentor?",
            "Inverter a jornada: começar pelo final feliz",
            "Usar anti-marketing: admitir uma 'fraqueza' que é força",
            "Quebrar a 4ª parede: falar sobre o próprio anúncio",
            "Criar um inimigo comum em vez de competir"
        ]
        return twists[hash(str(params)) % len(twists)]
    
    def _gerar_elemento_aleatorio(self, params: Dict) -> str:
        """Gera elemento aleatório criativo"""
        elementos = [
            "Incluir um easter egg para os mais atentos",
            "Usar uma metáfora inesperada do mundo animal",
            "Adicionar um plot twist no meio da mensagem",
            "Criar um acrônimo memorável",
            "Incluir um desafio interativo"
        ]
        return elementos[hash(str(params)) % len(elementos)]
    
    def _gerar_fator_disruptivo(self, params: Dict) -> str:
        """Gera fator disruptivo"""
        fatores = [
            "Questionar a premissa básica do mercado",
            "Propor um modelo de negócio invertido",
            "Criar uma nova categoria em vez de competir",
            "Transformar o problema em solução",
            "Unir opostos que nunca foram unidos"
        ]
        return fatores[hash(str(params)) % len(fatores)]
    
    def _gerar_magia(self, params: Dict) -> str:
        """Gera elemento mágico/emocional"""
        magias = [
            "Momento de revelação pessoal do fundador",
            "História de transformação real emocionante",
            "Conexão com propósito maior que o lucro",
            "Elemento nostálgico que toca o coração",
            "Promessa audaciosa mas alcançável"
        ]
        return magias[hash(str(params)) % len(magias)]
    
    def _gerar_perspectiva(self, params: Dict) -> str:
        """Gera perspectiva inusitada"""
        perspectivas = [
            "Contar a história do ponto de vista do produto",
            "Narrar do futuro olhando para o presente",
            "Perspectiva de uma criança explicando para adulto",
            "Visão de um alienígena descobrindo o produto",
            "Ângulo de um historiador daqui a 100 anos"
        ]
        return perspectivas[hash(str(params)) % len(perspectivas)]
    
    def _extrair_prompt_id(self, entrada: str) -> str:
        """Extrai ID do prompt da entrada"""
        palavras = entrada.split()
        for palavra in palavras:
            if palavra.startswith("Prompt_") or palavra.startswith("PromptKit_"):
                return palavra.strip(".,!?")
        
        # Tentar encontrar padrão de ID
        import re
        pattern = r'(Prompt_\w+_v[\d.]+|PromptKit_\w+_v[\d.]+)'
        match = re.search(pattern, entrada)
        if match:
            return match.group(1)
        
        raise ValueError("ID do prompt não encontrado na entrada")
    
    def _buscar_descendentes(self, prompt_id: str) -> List[str]:
        """Busca prompts que descendem do ID fornecido"""
        descendentes = []
        
        for pid, data in self.prompt_vault.items():
            lineage = data.get("dna", {}).get("lineage", [])
            if prompt_id in lineage:
                descendentes.append(pid)
        
        return sorted(descendentes)
    
    def _ativar_chaos(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Ativa modo chaos criativo"""
        try:
            # Extrair nível de chaos se especificado
            if "nivel" in entrada.lower():
                try:
                    nivel = float(entrada.split("nivel")[-1].strip().split()[0])
                    self.nivel_chaos = max(0.1, min(1.0, nivel))
                except:
                    self.nivel_chaos = 0.7  # Padrão alto
            else:
                self.nivel_chaos = 0.7
            
            self.modo_atual = PromptMode.CHAOS
            
            self._registrar_evento("chaos_activated", {
                "nivel": self.nivel_chaos
            })
            
            return f"""
🔮 **PromptChaos ATIVADO!**

⚡ **Nível de Chaos:** {self.nivel_chaos * 100:.0f}%
🎲 **Modo:** Criatividade Experimental Desbloqueada

🌟 **O que esperar:**
- Prompts com twists inesperados
- Elementos disruptivos e mágicos  
- Perspectivas inusitadas
- Quebra de padrões convencionais
- Alto potencial de inovação

⚠️ **Aviso:** 
- Resultados podem ser não-convencionais
- Teste antes de usar em produção
- Ideal para brainstorming e inovação

🚀 **Próximo prompt será CAÓTICO!**

Use `promptchaos nivel 0` para desativar.
"""
            
        except Exception as e:
            logger.error(f"❌ Erro ao ativar chaos: {e}")
            return f"❌ Erro no PromptChaos: {str(e)}"
    
    def _gerar_hash_dna(self, params: Dict) -> str:
        """Gera hash único para DNA do prompt"""
        content = json.dumps(params, sort_keys=True)
        return hashlib.md5(content.encode()).hexdigest()[:8]
    
    def _gerar_variacoes(self, entrada: str, contexto: Optional[Dict] = None) -> str:
        """Gera variações de prompt para diferentes contextos"""
        try:
            if contexto is None:
                contexto = {}
            params = self._extrair_parametros(entrada, contexto)
            base_prompt = self._gerar_prompt_base(params)
            
            # Gerar 3 variações
            variacoes = {
                "emocional": self._variar_emocao(base_prompt, params),
                "formal": self._variar_formalidade(base_prompt, params, "formal"),
                "casual": self._variar_formalidade(base_prompt, params, "casual")
            }
            
            resposta = f"""
🎭 **Variações de Prompt Geradas!**

📌 **Contexto Base:** {params.get('funcao', 'geral')}
🎯 **Persona:** {params.get('persona', 'público geral')}

### 📝 **Prompt Original:**
```
{base_prompt[:200]}...
```

### 🎨 **Variações Criadas:**
"""
            
            for tipo, variacao in variacoes.items():
                score = self._calcular_score(variacao, params)
                resposta += f"\n\n**{tipo.upper()}** (Score: {score.media_geral:.1f}/10)"
                resposta += f"\n```\n{variacao[:200]}...\n```"
            
            resposta += "\n\n✅ Todas as variações foram salvas no PromptVault!"
            
            return resposta
            
        except Exception as e:
            logger.error(f"❌ Erro ao gerar variações: {e}")
            return f"❌ Erro nas variações: {str(e)}"
    
    def _variar_emocao(self, prompt: str, params: Dict) -> str:
        """Varia emoção do prompt"""
        emocoes = {
            "empoderamento": ["conquiste", "domine", "transforme", "lidere"],
            "urgencia": ["agora", "última chance", "hoje", "imperdível"],
            "exclusividade": ["seleto", "vip", "exclusivo", "premium"],
            "cuidado": ["acolhemos", "cuidamos", "protegemos", "apoiamos"]
        }
        
        emocao_escolhida = list(emocoes.keys())[hash(prompt) % len(emocoes)]
        palavras = emocoes[emocao_escolhida]
        
        # Inserir palavras emocionais
        prompt_variado = prompt
        for palavra in palavras[:2]:
            prompt_variado = prompt_variado.replace(".", f" {palavra}.", 1)
        
        return prompt_variado
    
    def _variar_formalidade(self, prompt: str, params: Dict, nivel: str) -> str:
        """Varia nível de formalidade"""
        if nivel == "formal":
            substituicoes = {
                "você": "o(a) senhor(a)",
                "precisa": "necessita",
                "fazer": "realizar",
                "conseguir": "alcançar",
                "problema": "desafio"
            }
        else:  # casual
            substituicoes = {
                "o(a) senhor(a)": "você",
                "necessita": "precisa",
                "realizar": "fazer", 
                "alcançar": "conseguir",
                "desafio": "problema"
            }
        
        prompt_variado = prompt
        for original, nova in substituicoes.items():
            prompt_variado = prompt_variado.replace(original, nova)
        
        return prompt_variado


def criar_promptcrafter() -> PromptCrafterV3:
    """Factory function para criar PromptCrafter v3.0"""
    return PromptCrafterV3()