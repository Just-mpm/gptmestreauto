"""
Agente Carlos v2.1 - INTEGRAÇÃO COMPLETA com DeepAgent v2.0 Web Search
ATUALIZAÇÃO: Carlos agora detecta automaticamente quando fazer pesquisa web!
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)

class CarlosAgent(BaseAgent):
    """
    Carlos v2.1 - Interface Principal com DeepAgent v2.0 WEB SEARCH INTEGRADO
    
    ✨ SISTEMA INTEGRADO v2.1 COM WEB SEARCH:
    - 🧠 Memória vetorial integrada (ChromaDB)
    - 🔍 Busca semântica em conversas anteriores
    - 📚 Aprendizado contínuo automático
    - 🤖 Reflexor v1.5+ para auditoria
    - 🧠 SupervisorAI v1.3 para classificação inteligente
    - 🌐 DeepAgent v2.0 para pesquisa WEB REAL! 🆕
    - 💡 Detecção automática de necessidade de web search
    """
    
    def __init__(self, reflexor_ativo: bool = True, supervisor_ativo: bool = True, 
                 memoria_ativa: bool = True, deepagent_ativo: bool = True, llm=None):
        super().__init__(
            name="Carlos",
            description="Interface principal v2.1 com DeepAgent v2.0 Web Search"
        )
        
        # Sistema de memória
        self.memoria_ativa = memoria_ativa
        self.memory_manager = None
        
        if self.memoria_ativa:
            try:
                from memory.vector_store import get_memory_manager
                self.memory_manager = get_memory_manager()
                if self.memory_manager.memory_active:
                    logger.info("🧠 Memória vetorial ativada com sucesso!")
                else:
                    logger.warning("⚠️ Memória vetorial não disponível")
                    self.memoria_ativa = False
            except ImportError:
                logger.warning("⚠️ Módulo de memória não encontrado")
                self.memoria_ativa = False
        
        # Configuração do LLM
        if llm is None:
            self._inicializar_llm()
        else:
            self.llm = llm
        
        # Sistema de SupervisorAI
        self.supervisor_ativo = supervisor_ativo
        self.supervisor = None
        if self.supervisor_ativo:
            self._inicializar_supervisor()
        
        # Sistema de Reflexor
        self.reflexor_ativo = reflexor_ativo
        self.reflexor = None
        if self.reflexor_ativo:
            self._inicializar_reflexor()
        
        # 🆕 Sistema DeepAgent v2.0 com Web Search
        self.deepagent_ativo = deepagent_ativo
        self.deepagent = None
        if self.deepagent_ativo:
            self._inicializar_deepagent_v2()
        
        # Memória da sessão (backup)
        self.conversa_memoria = []
        self.contexto_memoria = {}
        
        # Estatísticas v2.1 EXPANDIDAS com DeepAgent Web Search
        self.stats.update({
            "total_respostas": 0,
            "respostas_com_memoria": 0,
            "respostas_sem_memoria": 0,
            "busca_semantica_usado": 0,
            "contexto_recuperado": 0,
            "aprendizados_salvos": 0,
            "score_medio_qualidade": 0.0,
            "classificacoes_supervisor": 0,
            "modo_profundo_usado": 0,
            "modo_direto_usado": 0,
            "deepagent_pesquisas": 0,
            "deepagent_web_search_usado": 0,  # 🆕 Contador de web search real
            "deepagent_oportunidades": 0,
            "tempo_medio_processamento": 0.0
        })
        
        # Palavras-chave que ativam web search automaticamente
        self.web_search_triggers = [
            "pesquise", "busque", "investigue", "analise", "verifique",
            "preço", "preços", "quanto custa", "valor", "mercado",
            "concorrente", "concorrência", "tendência", "oportunidade",
            "shopee", "mercado livre", "magalu", "aliexpress", "amazon",
            "internet", "web", "online", "atual", "atualizado", "recente",
            "vender", "vendendo", "investimento", "investir", "marketplace",
            "produto", "viabilidade", "potencial", "demanda", "nicho",
            "lucrativo", "rentável", "vale a pena", "compensa",
            "vendas", "venda", "anúncios", "anúncio", "mais vendidos",
            "vendem", "vendido", "pesquisa", "fazer uma pesquisa",
            "quero saber", "pode fazer", "pode pesquisar"
        ]
        
        logger.info(f"🤖 Carlos v2.1 WEB SEARCH inicializado - DeepAgent: {'✅' if self.deepagent_ativo else '❌'}")
    
    def _inicializar_llm(self):
        """Inicializa o LLM com configurações padrão"""
        try:
            from langchain_anthropic import ChatAnthropic
            import config
            
            if not config.ANTHROPIC_API_KEY:
                raise ValueError("ANTHROPIC_API_KEY não configurada no arquivo .env")
            
            self.llm = ChatAnthropic(
                model=config.CLAUDE_MODEL,
                max_tokens=config.CLAUDE_MAX_TOKENS,
                temperature=config.CLAUDE_TEMPERATURE,
                anthropic_api_key=config.ANTHROPIC_API_KEY,
            )
            logger.info("🔗 LLM Claude inicializado para Carlos v2.1")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar LLM: {e}")
            raise
    
    def _inicializar_supervisor(self):
        """Inicializa o SupervisorAI v1.3"""
        try:
            from agents.supervisor_ai import criar_supervisor_ai
            self.supervisor = criar_supervisor_ai(llm=self.llm)
            logger.info("🧠 SupervisorAI v1.3 ativado e integrado!")
        except ImportError:
            logger.warning("⚠️ SupervisorAI não disponível")
            self.supervisor = None
            self.supervisor_ativo = False
        except Exception as e:
            logger.error(f"❌ Erro ao ativar SupervisorAI: {e}")
            self.supervisor = None
            self.supervisor_ativo = False
    
    def _inicializar_reflexor(self):
        """Inicializa o Reflexor se disponível"""
        try:
            from agents.reflexor import AgenteReflexor
            self.reflexor = AgenteReflexor(llm=self.llm)
            logger.info("🔍 Reflexor v1.5+ ativado")
        except ImportError:
            logger.warning("⚠️ Reflexor não disponível")
            self.reflexor = None
            self.reflexor_ativo = False
        except Exception as e:
            logger.error(f"❌ Erro ao ativar Reflexor: {e}")
            self.reflexor = None
            self.reflexor_ativo = False
    
    def _inicializar_deepagent_v2(self):
        """🆕 Inicializa o DeepAgent v2.0 com Web Search"""
        try:
            from agents.deep_agent import criar_deep_agent_websearch
            self.deepagent = criar_deep_agent_websearch()
            
            # Verificar se web search está ativo
            web_status = "✅ ATIVO" if getattr(self.deepagent, 'web_search_enabled', False) else "❌ INATIVO"
            logger.info(f"🌐 DeepAgent v2.0 Web Search inicializado - Status: {web_status}")
            
        except ImportError:
            logger.warning("⚠️ DeepAgent v2.0 não disponível - verifique agents/deep_agent.py")
            self.deepagent = None
            self.deepagent_ativo = False
        except Exception as e:
            logger.error(f"❌ Erro ao ativar DeepAgent v2.0: {e}")
            self.deepagent = None
            self.deepagent_ativo = False
    
    def _detectar_necessidade_web_search(self, mensagem: str) -> bool:
        """🆕 DETECÇÃO AUTOMÁTICA: Verifica se a mensagem precisa de web search"""
        if not self.deepagent_ativo or not self.deepagent:
            return False
        
        mensagem_lower = mensagem.lower()
        
        # Verificar palavras-chave que indicam necessidade de web search
        for trigger in self.web_search_triggers:
            if trigger in mensagem_lower:
                return True
        
        # Padrões específicos que indicam pesquisa web
        padroes_web_search = [
            "quanto custa",
            "qual o preço",
            "pesquise na internet",
            "busque na web",
            "dados atuais",
            "informações recentes",
            "preços no brasil",
            "mercado brasileiro"
        ]
        
        for padrao in padroes_web_search:
            if padrao in mensagem_lower:
                return True
        
        return False
    
    def processar(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        🔄 FLUXO v2.1 COM DETECÇÃO AUTOMÁTICA DE WEB SEARCH:
        1. Verifica comandos especiais
        2. 🌐 DETECTA automaticamente se precisa de web search
        3. 🔍 EXECUTA DeepAgent v2.0 se necessário
        4. 🧠 SupervisorAI classifica a tarefa
        5. 🧠 Busca contexto na memória vetorial
        6. 💭 Gera resposta ÚNICA integrando TODOS os dados
        7. 🔍 Auditoria com Reflexor v1.5+
        8. 💾 Salva na memória vetorial
        """
        inicio_processamento = time.time()
        
        try:
            # 1. Verificar comandos especiais
            if mensagem.startswith('/'):
                resposta = self._processar_comando(mensagem)
                self._salvar_na_memoria_sessao(mensagem, resposta, contexto)
                return resposta
            
            # 🆕 2. DETECÇÃO AUTOMÁTICA DE WEB SEARCH
            resultado_deepagent = None
            if self._detectar_necessidade_web_search(mensagem):
                logger.info("🌐 Web search detectado automaticamente!")
                
                try:
                    # Extrair produto/termo para pesquisa
                    termo_pesquisa = self._extrair_termo_pesquisa(mensagem)
                    
                    # 🌐 EXECUTAR WEB SEARCH REAL
                    resultado_deepagent = self.deepagent.pesquisar_produto_web(termo_pesquisa)
                    self.stats["deepagent_pesquisas"] += 1
                    
                    if resultado_deepagent.web_search_used:
                        self.stats["deepagent_web_search_usado"] += 1
                        logger.info(f"🌐 Web search REAL executado: {termo_pesquisa}")
                    
                    if resultado_deepagent.score_oportunidade >= 7.0:
                        self.stats["deepagent_oportunidades"] += 1
                    
                except Exception as e:
                    logger.error(f"⚠️ Erro no DeepAgent Web Search: {e}")
                    resultado_deepagent = None
            
            # 3. 🧠 CLASSIFICAÇÃO INTELIGENTE COM SUPERVISORAI
            classificacao = None
            modo_execucao = "direto"  # fallback
            
            if self.supervisor_ativo and self.supervisor:
                try:
                    classificacao = self.supervisor.classificar_tarefa(mensagem, contexto)
                    modo_execucao = classificacao.modo_recomendado.value
                    self.stats["classificacoes_supervisor"] += 1
                    
                    # Estatísticas de modo
                    if modo_execucao == "profundo":
                        self.stats["modo_profundo_usado"] += 1
                    elif modo_execucao == "direto":
                        self.stats["modo_direto_usado"] += 1
                        
                except Exception as e:
                    logger.error(f"⚠️ Erro no SupervisorAI: {e}")
                    modo_execucao = "direto"
                    classificacao = None
            
            # 4. 🧠 Recuperar contexto da memória vetorial
            contexto_recuperado = ""
            if self.memoria_ativa and self.memory_manager:
                try:
                    contexto_recuperado = self.memory_manager.recall_context(mensagem)
                    self.stats["busca_semantica_usado"] += 1
                    
                    if len(contexto_recuperado) > 50 and "CONVERSAS ANTERIORES" in contexto_recuperado:
                        self.stats["contexto_recuperado"] += 1
                        logger.debug("🧠 Contexto relevante encontrado!")
                except Exception as e:
                    logger.error(f"⚠️ Erro ao buscar contexto: {e}")
                    contexto_recuperado = ""
            
            # 🆕 5. GERAR RESPOSTA INTEGRANDO WEB SEARCH
            if resultado_deepagent:
                # Resposta com dados de web search
                resposta = self._gerar_resposta_com_web_search(
                    mensagem, resultado_deepagent, contexto_recuperado, 
                    modo_execucao, classificacao
                )
            else:
                # Resposta normal sem web search
                if modo_execucao == "profundo":
                    resposta = self._processar_modo_profundo(mensagem, contexto, contexto_recuperado, classificacao)
                elif modo_execucao == "analise_modular":
                    resposta = self._processar_modo_modular(mensagem, contexto, contexto_recuperado, classificacao)
                elif modo_execucao == "intermediario":
                    resposta = self._processar_modo_intermediario(mensagem, contexto, contexto_recuperado, classificacao)
                else:  # direto
                    resposta = self._processar_modo_direto(mensagem, contexto, contexto_recuperado)
            
            # 6. 🔍 Sistema de auditoria com Reflexor v1.5+
            if self.reflexor_ativo and self.reflexor:
                try:
                    reflexao = self.reflexor.analisar_resposta(
                        pergunta=mensagem,
                        resposta=resposta,
                        contexto=contexto or {}
                    )
                    
                    self._atualizar_stats_reflexao(reflexao)
                    
                    # Se score baixo, tentar melhorar
                    if reflexao.score_qualidade < 6:
                        logger.info(f"⚠️ Score baixo ({reflexao.score_qualidade}), melhorando...")
                        resposta_melhorada = self._melhorar_resposta(mensagem, resposta, reflexao)
                        if resposta_melhorada:
                            resposta = resposta_melhorada
                    
                    # Salvar aprendizado se relevante
                    if reflexao.score_qualidade >= 8 and len(mensagem) > 30:
                        self._salvar_aprendizado_automatico(mensagem, resposta, reflexao)
                    
                except Exception as e:
                    logger.error(f"⚠️ Erro na auditoria: {e}")
            
            # 7. 💾 Salvar na memória vetorial
            if self.memoria_ativa and self.memory_manager:
                try:
                    session_id = contexto.get('session_id') if contexto else None
                    self.memory_manager.remember_conversation(
                        user_input=mensagem,
                        assistant_response=resposta,
                        agent_name="Carlos",
                        session_id=session_id
                    )
                    self.stats["respostas_com_memoria"] += 1
                    logger.debug("💾 Conversa salva na memória")
                except Exception as e:
                    logger.error(f"⚠️ Erro ao salvar: {e}")
                    self.stats["respostas_sem_memoria"] += 1
            else:
                self.stats["respostas_sem_memoria"] += 1
            
            # 8. Backup na memória da sessão + estatísticas
            self._salvar_na_memoria_sessao(mensagem, resposta, contexto)
            
            # 9. Atualizar estatísticas de tempo
            tempo_total = time.time() - inicio_processamento
            self._atualizar_tempo_medio(tempo_total)
            
            self.update_stats(success=True)
            self.stats["total_respostas"] += 1
            
            return resposta
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento completo v2.1: {e}")
            self.update_stats(success=False)
            return f"❌ Erro interno: {str(e)}"
    
    def _extrair_termo_pesquisa(self, mensagem: str) -> str:
        """🆕 Extrai termo para pesquisa web da mensagem"""
        import re
        
        # Primeiro, tentar extrair o produto específico após palavras-chave
        mensagem_lower = mensagem.lower()
        
        # Padrões para encontrar o produto
        padroes = [
            r'vender\s+(.+?)(?:\s+está|\s+nos|\s+no\s|$)',
            r'pesquise\s+(?:para\s+mim\s+)?(?:se\s+)?(?:vender\s+)?(.+?)(?:\s+está|\s+nos|\s+no\s|$)',
            r'analise\s+(.+?)(?:\s+está|\s+nos|\s+no\s|$)',
            r'produto\s+(.+?)(?:\s+está|\s+nos|\s+no\s|$)',
            r'sobre\s+(.+?)(?:\s+está|\s+nos|\s+no\s|$)'
        ]
        
        for padrao in padroes:
            match = re.search(padrao, mensagem_lower)
            if match:
                produto = match.group(1).strip()
                # Limpar palavras desnecessárias do final
                produto = re.sub(r'\s+(está|sendo|um|bom|investimento|nos|marketplaces?|para|vender).*$', '', produto)
                if len(produto) > 3:
                    return produto
        
        # Fallback: método anterior melhorado
        palavras_remover = {
            "carlos", "pesquise", "busque", "investigue", "analise", "verifique",
            "na", "internet", "web", "online", "para", "ver", "os", "preços",
            "que", "estão", "vendendo", "quanto", "custa", "valor", "preço",
            "me", "mim", "se", "está", "sendo", "um", "bom", "nos", "é",
            "oi", "olá", "tudo", "bem", "por", "favor", "marketplace", "marketplaces",
            "investimento", "vender", "vendendo"
        }
        
        palavras = mensagem.lower().split()
        termo_palavras = []
        
        for palavra in palavras:
            palavra_limpa = palavra.strip('.,!?')
            if palavra_limpa not in palavras_remover and len(palavra_limpa) > 2:
                if not palavra_limpa.startswith(("http", "www", ".")):
                    termo_palavras.append(palavra_limpa)
        
        # Se conseguiu extrair algo, usar
        if termo_palavras:
            return " ".join(termo_palavras[:4])  # Máximo 4 palavras
        
        # Fallback: tentar padrões específicos
        mensagem_lower = mensagem.lower()
        if "patinho" in mensagem_lower:
            if "resina" in mensagem_lower:
                return "patinhos de resina"
            elif "decorativo" in mensagem_lower:
                return "patinhos decorativos"
            else:
                return "patinhos"
        
        return "produto"
    
    def _gerar_resposta_com_web_search(self, mensagem: str, resultado_web, 
                                     contexto_memoria: str, modo_execucao: str, classificacao) -> str:
        """🆕 Gera resposta integrando dados de web search REAL"""
        
        # Status do web search
        web_status = "🌐 PESQUISA WEB REAL" if resultado_web.web_search_used else "🔄 PESQUISA SIMULADA"
        
        # Construir informações do web search
        info_web_search = f"""
{web_status} - DADOS ENCONTRADOS:

**Produto Pesquisado:** {resultado_web.query}
**Score de Oportunidade:** {resultado_web.score_oportunidade:.1f}/10
**Score de Confiabilidade:** {resultado_web.score_confiabilidade:.1f}/10

**Resumo dos Dados:**
{resultado_web.resumo}

**Principais Insights:**
{chr(10).join(f"• {insight}" for insight in resultado_web.insights[:3])}

**Recomendação:**
{resultado_web.recomendacao}

**Fontes Consultadas:** {resultado_web.sources_count}
"""
        
        if resultado_web.citacoes:
            info_web_search += f"**Sites Consultados:** {', '.join(resultado_web.citacoes[:3])}"
        
        # Prompt integrado baseado no modo
        prompt = f"""Você é Carlos v2.1 do GPT Mestre Autônomo com PESQUISA WEB REAL integrada.

{info_web_search}

🎯 **INSTRUÇÕES:**
Com base nos dados de web search acima, responda de forma natural e útil à pergunta do usuário.

**IMPORTANTE:**
- Use os dados REAIS encontrados na pesquisa
- Mencione que fez uma pesquisa web atual
- Cite os preços e informações específicas encontradas
- Seja prático e direto
- Informe o status da pesquisa (real ou simulada)

{self._construir_contexto_base(mensagem, None, contexto_memoria)}

RESPONDA DE FORMA NATURAL INTEGRANDO OS DADOS DA PESQUISA WEB:"""
        
        return self._gerar_resposta(prompt)
    
    def _construir_contexto_base(self, mensagem: str, contexto: Optional[Dict], 
                               contexto_memoria: str) -> str:
        """Constrói contexto base para todos os modos"""
        base = f"""
🧠 CONTEXTO DA SESSÃO:
{self._obter_contexto_recente()}"""

        if contexto_memoria and len(contexto_memoria) > 50:
            base += f"""

{contexto_memoria}"""
        
        base += f"""

💬 PERGUNTA DO USUÁRIO:
{mensagem}"""
        
        return base
    
    def _obter_contexto_recente(self) -> str:
        """Obtém contexto das conversas recentes da sessão"""
        if not self.conversa_memoria:
            return "Nova sessão iniciada."
        
        contexto_items = []
        for item in self.conversa_memoria[-2:]:  # Últimas 2 da sessão
            pergunta_short = item['pergunta'][:80] + "..." if len(item['pergunta']) > 80 else item['pergunta']
            resposta_short = item['resposta'][:80] + "..." if len(item['resposta']) > 80 else item['resposta']
            contexto_items.append(f"P: {pergunta_short}\nR: {resposta_short}")
        
        return "\n".join(contexto_items)
    
    def _salvar_na_memoria_sessao(self, mensagem: str, resposta: str, contexto: Optional[Dict] = None):
        """Salva na memória temporária da sessão"""
        interacao = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "pergunta": mensagem,
            "resposta": resposta,
            "contexto": contexto
        }
        
        self.conversa_memoria.append(interacao)
        
        # Manter apenas últimas 15 na sessão
        if len(self.conversa_memoria) > 15:
            self.conversa_memoria = self.conversa_memoria[-15:]
    
    def _gerar_resposta(self, prompt: str) -> str:
        """Gera resposta usando o LLM"""
        try:
            resposta = self.llm.invoke(prompt)
            return resposta.content if hasattr(resposta, 'content') else str(resposta)
        except Exception as e:
            logger.error(f"❌ Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."
    
    # 🆕 Métodos de processamento atualizados (versões simplificadas)
    def _processar_modo_profundo(self, mensagem: str, contexto: Optional[Dict], 
                                contexto_memoria: str, classificacao) -> str:
        prompt = f"""Você é Carlos em MODO PROFUNDO. Analise detalhadamente a questão:

{self._construir_contexto_base(mensagem, contexto, contexto_memoria)}

FORNEÇA ANÁLISE PROFUNDA E ESTRATÉGICA:"""
        return self._gerar_resposta(prompt)
    
    def _processar_modo_modular(self, mensagem: str, contexto: Optional[Dict], 
                              contexto_memoria: str, classificacao) -> str:
        prompt = f"""Você é Carlos em MODO MODULAR. Estruture a resposta de forma clara:

{self._construir_contexto_base(mensagem, contexto, contexto_memoria)}

RESPONDA DE FORMA ESTRUTURADA:"""
        return self._gerar_resposta(prompt)
    
    def _processar_modo_intermediario(self, mensagem: str, contexto: Optional[Dict], 
                                    contexto_memoria: str, classificacao) -> str:
        prompt = f"""Você é Carlos em MODO INTERMEDIÁRIO. Resposta equilibrada:

{self._construir_contexto_base(mensagem, contexto, contexto_memoria)}

RESPONDA DE FORMA EQUILIBRADA:"""
        return self._gerar_resposta(prompt)
    
    def _processar_modo_direto(self, mensagem: str, contexto: Optional[Dict], 
                             contexto_memoria: str) -> str:
        prompt = f"""Você é Carlos em MODO DIRETO. Seja objetivo:

{self._construir_contexto_base(mensagem, contexto, contexto_memoria)}

RESPONDA DE FORMA DIRETA:"""
        return self._gerar_resposta(prompt)
    
    # Métodos auxiliares (simplificados)
    def _atualizar_stats_reflexao(self, reflexao):
        """Atualiza estatísticas do Reflexor"""
        try:
            score_atual = reflexao.score_qualidade
            scores_anteriores = self.stats.get("score_medio_qualidade", 0.0)
            total_avaliacoes = self.stats.get("successful_interactions", 0) + 1
            nova_media = ((scores_anteriores * (total_avaliacoes - 1)) + score_atual) / total_avaliacoes
            self.stats["score_medio_qualidade"] = nova_media
        except Exception as e:
            logger.error(f"Erro ao atualizar stats: {e}")
    
    def _atualizar_tempo_medio(self, tempo_atual: float):
        """Atualiza tempo médio de processamento"""
        try:
            tempo_anterior = self.stats.get("tempo_medio_processamento", 0.0)
            total_respostas = self.stats.get("total_respostas", 0) + 1
            novo_tempo = ((tempo_anterior * (total_respostas - 1)) + tempo_atual) / total_respostas
            self.stats["tempo_medio_processamento"] = novo_tempo
        except Exception as e:
            logger.error(f"Erro ao atualizar tempo médio: {e}")
    
    def _melhorar_resposta(self, mensagem: str, resposta: str, reflexao) -> Optional[str]:
        """Tenta melhorar resposta com base na análise"""
        try:
            if self.reflexor and hasattr(self.reflexor, 'melhorar_resposta'):
                return self.reflexor.melhorar_resposta(mensagem, resposta)
        except Exception as e:
            logger.error(f"⚠️ Erro ao melhorar resposta: {e}")
        return None
    
    def _salvar_aprendizado_automatico(self, mensagem: str, resposta: str, reflexao):
        """Salva aprendizados importantes automaticamente"""
        try:
            if not self.memory_manager or not self.memoria_ativa:
                return
            
            categoria = "web_search" if "web search" in resposta.lower() else "geral"
            aprendizado = f"P: {mensagem[:100]}...\nR: {resposta[:200]}...\nScore: {reflexao.score_qualidade:.1f}/10"
            
            self.memory_manager.remember_learning(
                text=aprendizado,
                category=categoria,
                agent="Carlos_v2.1_WebSearch"
            )
            
            self.stats["aprendizados_salvos"] += 1
            logger.info(f"📚 Aprendizado salvo: {categoria}")
            
        except Exception as e:
            logger.error(f"⚠️ Erro ao salvar aprendizado: {e}")
    
    def _processar_comando(self, comando: str) -> str:
        """Processa comandos especiais"""
        try:
            comando = comando.lower().strip()
            
            if comando == '/help':
                return self._comando_help_websearch()
            elif comando == '/status':
                return self._comando_status_websearch()
            elif comando == '/deepagent':
                return self._comando_deepagent_websearch()
            elif comando == '/stats':
                return self._comando_stats_websearch()
            elif comando.startswith('/pesquisar ') or comando.startswith('/search '):
                # Comando direto para forçar pesquisa
                termo = comando.replace('/pesquisar', '').replace('/search', '').strip()
                return self._forcar_pesquisa_web(termo)
            else:
                return f"❓ Comando não encontrado: `{comando}`\n\n💡 Use `/help` para ver comandos disponíveis."
                
        except Exception as e:
            logger.error(f"❌ Erro ao processar comando {comando}: {e}")
            return f"❌ Erro ao processar comando: {str(e)}"
    
    def _comando_help_websearch(self) -> str:
        """Help com informações de web search"""
        web_status = "✅ ATIVO" if (self.deepagent_ativo and getattr(self.deepagent, 'web_search_enabled', False)) else "❌ INATIVO"
        
        return f"""🌐 **CARLOS v2.1 - SISTEMA COMPLETO COM WEB SEARCH**

🚀 **NOVIDADE v2.1: DETECÇÃO AUTOMÁTICA DE WEB SEARCH!**

🌐 **Status Web Search:** {web_status}

💬 **Como funciona AGORA:**
1. Você faz uma pergunta normalmente
2. ✨ **DETECTA AUTOMATICAMENTE** se precisa de web search
3. 🌐 **EXECUTA PESQUISA REAL** na internet (se necessário)
4. 🧠 Integra dados reais com inteligência do sistema
5. 💡 Responde com informações ATUAIS e verificáveis

🔍 **Exemplos que ATIVAM web search automaticamente:**
• "Carlos, pesquise patinhos de resina na internet"
• "Quanto custam produtos decorativos?"
• "Verifique preços no Shopee"
• "Analise a concorrência deste produto"
• "Busque tendências atuais"

📋 **Comandos Especiais:**
• `/help` - Esta ajuda completa
• `/status` - Status completo do sistema
• `/deepagent` - Status específico do web search
• `/stats` - Estatísticas detalhadas

🎯 **REVOLUÇÃO:** Agora o Carlos faz pesquisas REAIS automaticamente!
Você pergunta naturalmente e ele decide se precisa buscar na internet!"""
    
    def _comando_status_websearch(self) -> str:
        """Status com informações de web search"""
        try:
            web_enabled = self.deepagent_ativo and getattr(self.deepagent, 'web_search_enabled', False)
            web_status = "🌐 ATIVO" if web_enabled else "❌ INATIVO"
            
            return f"""📊 **CARLOS v2.1 - STATUS COM WEB SEARCH**

🤖 **Carlos:** v2.1 Operacional COMPLETO
🌐 **Web Search:** {web_status}
🔍 **DeepAgent v2.0:** {'✅ Integrado' if self.deepagent_ativo else '❌ Inativo'}
🧠 **Reflexor:** {'✅ v1.5+' if self.reflexor_ativo else '❌ Inativo'}
🧠 **Memória Vetorial:** {'✅ Ativa' if self.memoria_ativa else '❌ Inativa'}
🔗 **LLM:** Claude 3.5 Haiku
📱 **Interface:** Streamlit v2.1

📊 **Estatísticas Web Search:**
• Total pesquisas: {self.stats.get('deepagent_pesquisas', 0)}
• Web search real usado: {self.stats.get('deepagent_web_search_usado', 0)}
• Oportunidades encontradas: {self.stats.get('deepagent_oportunidades', 0)}

✨ **FUNCIONALIDADE PRINCIPAL:**
Detecção automática de necessidade de web search!
Carlos decide sozinho quando pesquisar na internet.

⏰ **Uptime:** {datetime.now().strftime('%H:%M:%S')}"""
            
        except Exception as e:
            return f"📊 **CARLOS v2.1 WEB SEARCH - STATUS** (Erro: {str(e)[:100]})"
    
    def _comando_deepagent_websearch(self) -> str:
        """Status específico do DeepAgent com web search"""
        if not self.deepagent_ativo or not self.deepagent:
            return "🔴 **DEEPAGENT v2.0 - INATIVO**"
        
        try:
            web_enabled = getattr(self.deepagent, 'web_search_enabled', False)
            
            return f"""🌐 **DEEPAGENT v2.0 - WEB SEARCH STATUS**

✅ **Configuração:**
• Status: {'🟢 ATIVO' if web_enabled else '🔴 INATIVO'}
• Versão: v2.0 com web search real
• Integração: ✅ Totalmente integrado ao Carlos
• Detecção: ✅ Automática

📊 **Estatísticas:**
• Total pesquisas: {self.stats.get('deepagent_pesquisas', 0)}
• Web search real: {self.stats.get('deepagent_web_search_usado', 0)}
• Pesquisas simuladas: {self.stats.get('deepagent_pesquisas', 0) - self.stats.get('deepagent_web_search_usado', 0)}
• Oportunidades: {self.stats.get('deepagent_oportunidades', 0)}

🎯 **Funcionalidades Ativas:**
• 🌐 Pesquisa web REAL via Claude 3.5 Haiku
• 🔍 Detecção automática de necessidade
• 📊 Análise de oportunidade (0-10)
• 🌟 Score de confiabilidade baseado em fontes
• 📚 Citações de fontes consultadas

💡 **Como ativar:**
Simplesmente fale naturalmente:
"Carlos, pesquise [produto] na internet"
"Quanto custa [produto]?"
"Verifique preços de [produto]"

🚀 **REVOLUÇÃO:** Web search automático integrado!"""
            
        except Exception as e:
            return f"🌐 **DEEPAGENT v2.0** - Erro: {str(e)[:100]}"
    
    def _forcar_pesquisa_web(self, termo: str) -> str:
        """Força uma pesquisa web direta"""
        if not termo:
            return "❌ Por favor, forneça um termo para pesquisar.\nExemplo: /pesquisar gel adesivo refrescante"
        
        if not self.deepagent_ativo or not self.deepagent:
            return "❌ DeepAgent não está ativo no momento."
        
        try:
            logger.info(f"🔍 Forçando pesquisa web para: {termo}")
            
            # Executar pesquisa diretamente
            resultado = self.deepagent.pesquisar_produto_web(termo)
            
            # Formatar resposta
            if resultado.web_search_used:
                self.stats["deepagent_web_search_usado"] += 1
                
            self.stats["deepagent_pesquisas"] += 1
            
            # Retornar resultado formatado
            return self.deepagent._formatar_resultado(resultado)
            
        except Exception as e:
            logger.error(f"❌ Erro na pesquisa forçada: {e}")
            return f"❌ Erro ao pesquisar: {str(e)}"
    
    def _comando_stats_websearch(self) -> str:
        """Estatísticas com web search"""
        try:
            total = self.stats.get('total_interactions', 0)
            sucessos = self.stats.get('successful_interactions', 0)
            taxa_sucesso = (sucessos / max(1, total)) * 100 if total > 0 else 0
            
            return f"""📈 **ESTATÍSTICAS SISTEMA v2.1 COM WEB SEARCH**

🎯 **Performance Geral:**
• Taxa de sucesso: {taxa_sucesso:.1f}%
• Total interações: {total}
• Sucessos: {sucessos}
• Erros: {self.stats.get('errors', 0)}

🌐 **Web Search (NOVIDADE):**
• Pesquisas acionadas: {self.stats.get('deepagent_pesquisas', 0)}
• Web search real usado: {self.stats.get('deepagent_web_search_usado', 0)}
• Oportunidades identificadas: {self.stats.get('deepagent_oportunidades', 0)}
• Taxa de web search: {(self.stats.get('deepagent_web_search_usado', 0) / max(1, self.stats.get('deepagent_pesquisas', 1)) * 100):.1f}%

🧠 **Sistema de Memória:**
• Respostas com memória: {self.stats.get('respostas_com_memoria', 0)}
• Buscas semânticas: {self.stats.get('busca_semantica_usado', 0)}
• Contexto recuperado: {self.stats.get('contexto_recuperado', 0)}
• Aprendizados salvos: {self.stats.get('aprendizados_salvos', 0)}

⚡ **Performance:**
• Tempo médio: {self.stats.get('tempo_medio_processamento', 0.0):.3f}s
• Score médio qualidade: {self.stats.get('score_medio_qualidade', 0.0):.1f}/10

📱 **Sessão Atual:**
• Conversas: {len(self.conversa_memoria)}
• Uptime: {datetime.now().strftime('%H:%M:%S')}

🚀 **Versão:** Carlos v2.1 COMPLETO - Web Search Automático!"""
        
        except Exception as e:
            return f"📈 **ESTATÍSTICAS v2.1** - Erro: {str(e)[:100]}"


# ===== FUNÇÕES DE CRIAÇÃO v2.1 =====

def criar_carlos_integrado(supervisor_ativo: bool = True, reflexor_ativo: bool = True, 
                          deepagent_ativo: bool = True, llm=None):
    """Cria Carlos v2.1 COMPLETO com Web Search automático"""
    return CarlosAgent(
        reflexor_ativo=reflexor_ativo, 
        supervisor_ativo=supervisor_ativo, 
        deepagent_ativo=deepagent_ativo, 
        memoria_ativa=True, 
        llm=llm
    )

def create_carlos_full_system(llm=None) -> CarlosAgent:
    """Cria Carlos v2.1 com TODOS os sistemas ativados incluindo Web Search"""
    return CarlosAgent(
        reflexor_ativo=True, 
        supervisor_ativo=True, 
        deepagent_ativo=True, 
        memoria_ativa=True, 
        llm=llm
    )

# ===== TESTE E DIAGNÓSTICO =====

def diagnosticar_carlos_websearch():
    """Diagnóstica o Carlos v2.1 com Web Search"""
    try:
        carlos = create_carlos_full_system()
        
        web_enabled = carlos.deepagent_ativo and getattr(carlos.deepagent, 'web_search_enabled', False)
        
        return {
            "version": "2.1_WEB_SEARCH_COMPLETO",
            "carlos_ok": True,
            "deepagent_integrado": carlos.deepagent_ativo,
            "web_search_enabled": web_enabled,
            "supervisor_integrado": carlos.supervisor_ativo,
            "reflexor_integrado": carlos.reflexor_ativo,
            "memoria_disponivel": carlos.memoria_ativa,
            "sistema_completo": all([
                carlos.deepagent_ativo,
                web_enabled,
                carlos.supervisor_ativo,
                carlos.reflexor_ativo,
                carlos.memoria_ativa
            ]),
            "config_ok": carlos.llm is not None,
            "stats": carlos.stats
        }
    except Exception as e:
        return {
            "version": "2.1_WEB_SEARCH_COMPLETO",
            "carlos_ok": False,
            "erro": str(e)
        }

if __name__ == "__main__":
    print("🧪 Testando Carlos v2.1 WEB SEARCH...")
    diag = diagnosticar_carlos_websearch()
    print(f"📊 Diagnóstico: {diag}")
    
    if diag.get("carlos_ok"):
        print("✅ Carlos v2.1 Web Search OK!")
        if diag.get("sistema_completo"):
            print("🌐 SISTEMA COMPLETO: Web Search + SupervisorAI + Reflexor + Memória!")
        else:
            print("⚠️ Sistema parcial - alguns componentes indisponíveis")
    else:
        print(f"❌ Erro: {diag.get('erro')}")