"""
Agente Carlos v2.0 - Interface Principal com Memória Vetorial Integrada
Versão FINAL: Sistema de memória + auditoria + facilidade de uso
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
    Carlos v2.0 - Interface Principal com Memória Inteligente
    
    ✨ NOVIDADES v2.0:
    - 🧠 Memória vetorial integrada (ChromaDB)
    - 🔍 Busca semântica em conversas anteriores
    - 📚 Aprendizado contínuo automático
    - 🤖 Reflexor v1.5+ para auditoria
    - 💡 Respostas contextualizadas
    """
    
    def __init__(self, reflexor_ativo: bool = True, memoria_ativa: bool = True, llm=None):
        super().__init__(
            name="Carlos",
            description="Interface principal v2.0 com memória vetorial inteligente"
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
        
        # Sistema de Reflexor
        self.reflexor_ativo = reflexor_ativo
        self.reflexor = None
        if self.reflexor_ativo:
            self._inicializar_reflexor()
        
        # Memória da sessão (backup)
        self.conversa_memoria = []
        self.contexto_memoria = {}
        
        # Estatísticas v2.0
        self.stats.update({
            "total_respostas": 0,
            "respostas_com_memoria": 0,
            "respostas_sem_memoria": 0,
            "busca_semantica_usado": 0,
            "contexto_recuperado": 0,
            "aprendizados_salvos": 0,
            "score_medio_qualidade": 0.0
        })
        
        # Compatibilidade com versões anteriores
        self.stats_carlos = self.stats
        self.stats_ecossistema = {"versao": "2.0"}
        
        logger.info(f"🤖 Carlos v2.0 inicializado - Memória: {'✅' if self.memoria_ativa else '❌'}")
    
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
            logger.info("🔗 LLM Claude inicializado para Carlos v2.0")
            
        except Exception as e:
            logger.error(f"❌ Erro ao inicializar LLM: {e}")
            raise
    
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
    
    def processar(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        Processa mensagem com sistema de memória vetorial v2.0
        
        🔄 FLUXO v2.0:
        1. Verifica comandos especiais
        2. 🧠 Busca contexto na memória vetorial
        3. 💭 Gera resposta enriquecida com contexto
        4. 🔍 Auditoria com Reflexor v1.5+
        5. 💾 Salva na memória vetorial
        """
        try:
            # 1. Verificar comandos especiais
            if mensagem.startswith('/'):
                resposta = self._processar_comando(mensagem)
                self._salvar_na_memoria_sessao(mensagem, resposta, contexto)
                return resposta
            
            # 2. 🧠 Recuperar contexto da memória vetorial
            contexto_recuperado = ""
            if self.memoria_ativa and self.memory_manager:
                try:
                    contexto_recuperado = self.memory_manager.recall_context(mensagem)
                    self.stats["busca_semantica_usado"] += 1
                    
                    # Verificar se encontrou contexto relevante
                    if len(contexto_recuperado) > 50 and "CONVERSAS ANTERIORES" in contexto_recuperado:
                        self.stats["contexto_recuperado"] += 1
                        logger.debug("🧠 Contexto relevante encontrado!")
                except Exception as e:
                    logger.error(f"⚠️ Erro ao buscar contexto: {e}")
                    contexto_recuperado = ""
            
            # 3. 💭 Gerar resposta com contexto enriquecido
            prompt = self._construir_prompt_com_memoria(mensagem, contexto, contexto_recuperado)
            resposta = self._gerar_resposta(prompt)
            
            # 4. 🔍 Sistema de auditoria com Reflexor v1.5+
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
            
            # 5. 💾 Salvar na memória vetorial
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
            
            # 6. Backup na memória da sessão
            self._salvar_na_memoria_sessao(mensagem, resposta, contexto)
            
            # 7. Atualizar estatísticas
            self.update_stats(success=True)
            self.stats["total_respostas"] += 1
            
            return resposta
            
        except Exception as e:
            logger.error(f"❌ Erro no processamento v2.0: {e}")
            self.update_stats(success=False)
            return f"❌ Erro interno: {str(e)}"
    
    def _construir_prompt_com_memoria(self, mensagem: str, contexto: Optional[Dict], 
                                    contexto_memoria: str) -> str:
        """Constrói prompt v2.0 enriquecido com contexto da memória"""
        
        prompt_base = f"""Você é Carlos v2.0, agente principal do GPT Mestre Autônomo.

🤖 CARACTERÍSTICAS v2.0:
- Interface inteligente e proativa
- Sistema de memória vetorial ativo
- Respostas baseadas em contexto histórico
- Aprendizado contínuo e auditoria integrada

🧠 CONTEXTO DA SESSÃO ATUAL:
{self._obter_contexto_recente()}"""

        # Adicionar contexto da memória vetorial se disponível
        if contexto_memoria and len(contexto_memoria) > 50:
            prompt_base += f"""

{contexto_memoria}"""
        
        prompt_base += f"""

💬 PERGUNTA ATUAL:
{mensagem}

📋 INSTRUÇÕES v2.0:
- Use o contexto histórico para respostas mais precisas
- Mantenha continuidade com conversas anteriores
- Seja natural e direto
- Aplique aprendizados relevantes

Responda de forma útil e contextualizada:"""
        
        return prompt_base
    
    def _salvar_aprendizado_automatico(self, mensagem: str, resposta: str, reflexao):
        """v2.0: Salva aprendizados importantes automaticamente"""
        try:
            if not self.memory_manager or not self.memoria_ativa:
                return
            
            # Identificar categoria
            categoria = self._identificar_categoria(mensagem)
            
            # Criar aprendizado
            aprendizado = f"P: {mensagem[:100]}{'...' if len(mensagem) > 100 else ''}\nR: {resposta[:200]}{'...' if len(resposta) > 200 else ''}\nScore: {reflexao.score_qualidade:.1f}/10"
            
            self.memory_manager.remember_learning(
                text=aprendizado,
                category=categoria,
                agent="Carlos_v2"
            )
            
            self.stats["aprendizados_salvos"] += 1
            logger.info(f"📚 Aprendizado salvo: {categoria}")
            
        except Exception as e:
            logger.error(f"⚠️ Erro ao salvar aprendizado: {e}")
    
    def _identificar_categoria(self, mensagem: str) -> str:
        """Identifica categoria do aprendizado"""
        msg_lower = mensagem.lower()
        
        if any(word in msg_lower for word in ["produto", "vender", "comprar"]):
            return "produto"
        elif any(word in msg_lower for word in ["preço", "custo", "valor"]):
            return "preco"
        elif any(word in msg_lower for word in ["anúncio", "copy", "marketing"]):
            return "marketing"
        elif any(word in msg_lower for word in ["como", "explicar", "tutorial"]):
            return "tutorial"
        else:
            return "geral"
    
    # ===== COMANDOS v2.0 ATUALIZADOS =====
    
    def _comando_status(self) -> str:
        """Status v2.0 com informações de memória"""
        try:
            reflexor_status = "🟢 v1.5+" if self.reflexor_ativo else "🔴 Inativo"
            memoria_status = "🧠 Ativa" if self.memoria_ativa else "❌ Inativa"
            
            info_base = f"""📊 **CARLOS v2.0 - STATUS DO SISTEMA**

🤖 **Carlos:** v2.0 Operacional
🔍 **Reflexor:** {reflexor_status}
🧠 **Memória Vetorial:** {memoria_status}
🔗 **LLM:** Claude 3 Haiku
📱 **Interface:** Streamlit
"""
            
            # Estatísticas de memória
            if self.memoria_ativa and self.memory_manager:
                try:
                    stats = self.memory_manager.get_stats()
                    if stats.get('memory_active'):
                        vm = stats['vector_memory']
                        info_base += f"""
🧠 **MEMÓRIA VETORIAL:**
• Conversas indexadas: {vm.get('conversations', 0)}
• Aprendizados salvos: {vm.get('learnings', 0)}
• Total documentos: {vm.get('total_documents', 0)}
• Modelo: {vm.get('embedding_model', 'N/A')}"""
                except:
                    info_base += "\n🧠 **MEMÓRIA:** Erro ao carregar stats"
            
            # Estatísticas da sessão
            info_base += f"""

📈 **ESTATÍSTICAS v2.0:**
• Total respostas: {self.stats.get('total_respostas', 0)}
• Com memória: {self.stats.get('respostas_com_memoria', 0)}
• Buscas semânticas: {self.stats.get('busca_semantica_usado', 0)}
• Contexto usado: {self.stats.get('contexto_recuperado', 0)}
• Aprendizados: {self.stats.get('aprendizados_salvos', 0)}

⏰ **Uptime:** {datetime.now().strftime('%H:%M:%S')}"""
            
            return info_base
            
        except Exception as e:
            return f"📊 **CARLOS v2.0 - STATUS** (Erro: {str(e)[:100]})"
    
    def _comando_memoria(self) -> str:
        """Comando memória v2.0"""
        try:
            sessao_items = len(self.conversa_memoria)
            
            info = f"""🧠 **MEMÓRIA v2.0 - SISTEMA INTELIGENTE**

📱 **Memória da Sessão:** {sessao_items} interações"""
            
            if self.memoria_ativa and self.memory_manager:
                try:
                    stats = self.memory_manager.get_stats()
                    if stats.get('memory_active'):
                        vm = stats['vector_memory']
                        info += f"""

🧠 **Memória Vetorial (ChromaDB):**
• Status: ✅ Ativa e funcionando
• Conversas salvas: {vm.get('conversations', 0)}
• Aprendizados: {vm.get('learnings', 0)}
• Modelo de busca: {vm.get('embedding_model', 'N/A')}
• Localização: {vm.get('storage_path', 'N/A')}

📊 **Performance da Memória:**
• Buscas realizadas: {self.stats.get('busca_semantica_usado', 0)}
• Contexto encontrado: {self.stats.get('contexto_recuperado', 0)}
• Taxa de sucesso: {(self.stats.get('contexto_recuperado', 0) / max(1, self.stats.get('busca_semantica_usado', 1)) * 100):.1f}%"""
                    else:
                        info += f"\n🧠 **Memória Vetorial:** ❌ {stats.get('error', 'Erro desconhecido')}"
                except Exception as e:
                    info += f"\n🧠 **Memória Vetorial:** ⚠️ Erro: {str(e)[:100]}"
            else:
                info += "\n🧠 **Memória Vetorial:** ❌ Desativada"
            
            # Últimas interações
            if self.conversa_memoria:
                info += "\n\n📋 **Últimas Interações:**"
                for item in self.conversa_memoria[-3:]:
                    preview = item['pergunta'][:40] + "..." if len(item['pergunta']) > 40 else item['pergunta']
                    info += f"\n• {item['timestamp']}: {preview}"
            
            return info
            
        except Exception as e:
            return f"🧠 **MEMÓRIA v2.0** - Erro: {str(e)}"
    
    def _comando_help(self) -> str:
        """Help v2.0 atualizado"""
        return """🤖 **CARLOS v2.0 - SISTEMA INTELIGENTE COM MEMÓRIA**

🧠 **NOVIDADES v2.0:**
• **Memória Vetorial**: Lembro de TODAS as nossas conversas
• **Busca Semântica**: Encontro automaticamente contexto relevante
• **Aprendizado Contínuo**: Cada conversa me torna mais inteligente
• **Reflexor v1.5+**: Auditoria automática de qualidade

💬 **Como usar:**
Converse naturalmente! Automaticamente:
• Busco conversas similares anteriores
• Recupero aprendizados relevantes
• Aplico contexto para respostas melhores
• Salvo novos conhecimentos importantes

📋 **Comandos Especiais:**
• `/help` - Esta ajuda completa
• `/status` - Status do sistema com memória
• `/memory` - Informações detalhadas da memória
• `/clear` - Limpar sessão (mantém memória vetorial)
• `/agents` - Lista de agentes disponíveis
• `/reflexor` - Status do sistema de auditoria
• `/stats` - Estatísticas completas v2.0

🔍 **Funcionalidades Avançadas:**
• Continuidade entre sessões diferentes
• Respostas contextualizadas baseadas no histórico
• Detecção automática de padrões e aprendizados
• Sistema de qualidade em tempo real
• Memória persistente local (ChromaDB)

⚡ **Exemplos de Uso:**
• "Volte ao assunto que falamos sobre preços"
• "Como ficou aquela análise de produto?"
• "Lembra do que discutimos sobre marketing?"

🎯 **O Carlos v2.0 é muito mais inteligente porque nunca esquece!**"""
    
    def _comando_clear(self) -> str:
        """Clear v2.0 - preserva memória vetorial"""
        items_removidos = len(self.conversa_memoria)
        self.conversa_memoria.clear()
        self.contexto_memoria.clear()
        
        return f"""🗑️ **SESSÃO LIMPA v2.0**

✅ **Removido da sessão:**
• {items_removidos} interações temporárias
• Cache de contexto da sessão atual

🧠 **Preservado na memória vetorial:**
• Todas as conversas anteriores
• Aprendizados acumulados
• Conhecimento histórico

💡 **Nota:** A memória vetorial é permanente e continua ativa!
Para acessar conversas anteriores, apenas converse normalmente."""
    
    def _comando_reflexor(self) -> str:
        """Status do Reflexor v2.0"""
        if not self.reflexor_ativo or not self.reflexor:
            return "🔴 **REFLEXOR v1.5+ - INATIVO**"
        
        try:
            return f"""🔍 **REFLEXOR v1.5+ - STATUS AVANÇADO**

✅ **Configuração:**
• Status: 🟢 ATIVO e Integrado
• Versão: v1.5+ com memória
• Modo: Auditoria automática
• Auto-aprendizado: ✅ Ativo

📊 **Estatísticas v2.0:**
• Score médio: {self.stats.get('score_medio_qualidade', 0.0):.1f}/10
• Respostas auditadas: {self.stats.get('successful_interactions', 0)}
• Melhorias aplicadas: {self.stats.get('respostas_melhoradas', 0)}
• Aprendizados gerados: {self.stats.get('aprendizados_salvos', 0)}

🧠 **Integração com Memória:**
• Salva automaticamente respostas de alta qualidade
• Aprende padrões de sucesso
• Melhora respostas com base no histórico

⏰ **Última verificação:** {datetime.now().strftime('%H:%M:%S')}"""
            
        except Exception as e:
            return f"🔍 **REFLEXOR v1.5+** - Erro: {str(e)[:100]}"
    
    def _comando_stats(self) -> str:
        """Stats v2.0 completas"""
        try:
            total = self.stats.get('total_interactions', 0)
            sucessos = self.stats.get('successful_interactions', 0)
            taxa_sucesso = (sucessos / max(1, total)) * 100
            
            return f"""📈 **ESTATÍSTICAS COMPLETAS v2.0**

🎯 **Performance Geral:**
• Taxa de sucesso: {taxa_sucesso:.1f}%
• Total interações: {total}
• Sucessos: {sucessos}
• Erros: {self.stats.get('errors', 0)}

🧠 **Sistema de Memória:**
• Respostas com memória: {self.stats.get('respostas_com_memoria', 0)}
• Respostas sem memória: {self.stats.get('respostas_sem_memoria', 0)}
• Buscas semânticas: {self.stats.get('busca_semantica_usado', 0)}
• Contexto recuperado: {self.stats.get('contexto_recuperado', 0)}
• Taxa de contexto: {(self.stats.get('contexto_recuperado', 0) / max(1, self.stats.get('busca_semantica_usado', 1)) * 100):.1f}%

🔍 **Sistema de Auditoria:**
• Score médio qualidade: {self.stats.get('score_medio_qualidade', 0.0):.1f}/10
• Aprendizados salvos: {self.stats.get('aprendizados_salvos', 0)}

📱 **Sessão Atual:**
• Conversas na sessão: {len(self.conversa_memoria)}
• Uptime: {datetime.now().strftime('%H:%M:%S')}

🚀 **Versão:** Carlos v2.0 com Memória Inteligente"""
        
        except Exception as e:
            return f"📈 **ESTATÍSTICAS v2.0** - Erro: {str(e)[:100]}"
    
    # ===== MÉTODOS DE SUPORTE =====
    
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
    
    def _atualizar_stats_reflexao(self, reflexao):
        """Atualiza estatísticas do Reflexor"""
        try:
            score_atual = reflexao.score_qualidade
            
            # Calcular média móvel do score
            scores_anteriores = self.stats.get("score_medio_qualidade", 0.0)
            total_avaliacoes = self.stats.get("successful_interactions", 0) + 1
            
            nova_media = ((scores_anteriores * (total_avaliacoes - 1)) + score_atual) / total_avaliacoes
            self.stats["score_medio_qualidade"] = nova_media
            
        except Exception as e:
            logger.error(f"Erro ao atualizar stats: {e}")
    
    def _melhorar_resposta(self, mensagem: str, resposta: str, reflexao) -> Optional[str]:
        """Tenta melhorar resposta com base na análise"""
        try:
            if self.reflexor and hasattr(self.reflexor, 'melhorar_resposta'):
                return self.reflexor.melhorar_resposta(mensagem, resposta)
        except Exception as e:
            logger.error(f"⚠️ Erro ao melhorar resposta: {e}")
        return None
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas completas v2.0"""
        stats = {
            "version": "2.0",
            "session_memory": {
                "conversations": len(self.conversa_memoria),
                "context_items": len(self.contexto_memoria)
            },
            "processing_stats": {
                "total_responses": self.stats.get("total_respostas", 0),
                "with_memory": self.stats.get("respostas_com_memoria", 0),
                "without_memory": self.stats.get("respostas_sem_memoria", 0),
                "semantic_searches": self.stats.get("busca_semantica_usado", 0),
                "context_retrieved": self.stats.get("contexto_recuperado", 0),
                "learnings_saved": self.stats.get("aprendizados_salvos", 0),
                "avg_quality_score": self.stats.get("score_medio_qualidade", 0.0)
            }
        }
        
        if self.memory_manager and self.memoria_ativa:
            try:
                vector_stats = self.memory_manager.get_stats()
                stats["vector_memory"] = vector_stats
            except Exception as e:
                stats["vector_memory"] = {"error": str(e)}
        
        return stats

# ===== FUNÇÕES DE CRIAÇÃO v2.0 =====

def create_carlos() -> CarlosAgent:
    """Cria Carlos v2.0 básico (sem Reflexor)"""
    return CarlosAgent(reflexor_ativo=False, memoria_ativa=True)

def create_carlos_com_reflexor(reflexor_ativo: bool = True, llm=None) -> CarlosAgent:
    """Cria Carlos v2.0 com Reflexor integrado"""
    return CarlosAgent(reflexor_ativo=reflexor_ativo, memoria_ativa=True, llm=llm)

def criar_carlos_integrado(supervisor_ativo: bool = True, reflexor_ativo: bool = True, llm=None):
    """Cria Carlos v2.0 completo (compatibilidade com app.py)"""
    return CarlosAgent(reflexor_ativo=reflexor_ativo, memoria_ativa=True, llm=llm)

def create_carlos_full_system(llm=None) -> CarlosAgent:
    """Cria Carlos v2.0 com todos os sistemas ativados"""
    return CarlosAgent(reflexor_ativo=True, memoria_ativa=True, llm=llm)

# ===== DIAGNÓSTICO v2.0 =====

def diagnosticar_carlos():
    """Diagnóstica o Carlos v2.0"""
    try:
        carlos = create_carlos()
        
        return {
            "version": "2.0",
            "carlos_ok": True,
            "memoria_disponivel": carlos.memoria_ativa,
            "reflexor_integrado": hasattr(carlos, 'reflexor') and carlos.reflexor is not None,
            "memoria_ativa": hasattr(carlos, 'memory_manager') and carlos.memory_manager is not None,
            "config_ok": carlos.llm is not None,
            "stats": carlos.stats
        }
    except Exception as e:
        return {
            "version": "2.0",
            "carlos_ok": False,
            "erro": str(e)
        }

# ===== TESTE BÁSICO =====

if __name__ == "__main__":
    print("🧪 Testando Carlos v2.0...")
    diag = diagnosticar_carlos()
    print(f"📊 Diagnóstico v2.0: {diag}")
    
    if diag.get("carlos_ok"):
        print("✅ Carlos v2.0 OK!")
        if diag.get("memoria_disponivel"):
            print("🧠 Memória vetorial disponível!")
        else:
            print("⚠️ Memória vetorial não disponível - instale: pip install chromadb sentence-transformers")
    else:
        print(f"❌ Erro: {diag.get('erro')}")
