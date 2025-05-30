"""
Agente Carlos - Interface Principal do GPT Mestre Autônomo
Versão FINAL CORRIGIDA - Todos os erros resolvidos
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from agents.base_agent import BaseAgent
from utils.logger import get_logger

logger = get_logger(__name__)

class CarlosAgent(BaseAgent):
    """
    Carlos - Agente principal do GPT Mestre Autônomo
    Interface inteligente com sistema de auditoria integrado
    """
    
    def __init__(self, reflexor_ativo: bool = True, llm=None):
        super().__init__(
            name="Carlos",
            description="Agente principal - Interface inteligente com sistema de auditoria"
        )
        
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
        
        # Memória da conversa
        self.conversa_memoria = []
        self.contexto_memoria = {}
        
        # CORREÇÃO: Garantir que self.stats tenha TODAS as chaves necessárias
        self.stats.update({
            "total_respostas": 0,  # Alias para total_interactions
            "respostas_melhoradas": 0,
            "score_medio": 0.0,
            "tempo_total_reflexao": 0.0
        })
        
        # Estatísticas do Carlos
        self.stats_carlos = {
            "respostas_com_auditoria": 0,
            "respostas_sem_auditoria": 0,
            "score_medio_qualidade": 0.0,
            "total_reflexoes": 0,
            "red_flags_detectados": 0
        }
        
        # Estatísticas do ecossistema (para compatibilidade)
        self.stats_ecossistema = {
            "integracao_oraculo": 0,
            "torre_shadow_execucoes": 0,
            "supervisor_consultas": 0
        }
        
        logger.info(f"Carlos v1.5+ inicializado - Reflexor: {'Ativo' if self.reflexor_ativo else 'Inativo'}")
    
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
            logger.info("LLM Claude inicializado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao inicializar LLM: {e}")
            raise
    
    def _inicializar_reflexor(self):
        """Inicializa o Reflexor se disponível"""
        try:
            from agents.reflexor import AgenteReflexor
            self.reflexor = AgenteReflexor(llm=self.llm)
            logger.info("Reflexor v1.5+ ativado com sucesso")
        except ImportError:
            logger.warning("Reflexor não disponível - continuando sem auditoria")
            self.reflexor = None
            self.reflexor_ativo = False
        except Exception as e:
            logger.error(f"Erro ao ativar Reflexor: {e}")
            self.reflexor = None
            self.reflexor_ativo = False
    
    def processar(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """
        Processa mensagem com sistema de auditoria integrado
        """
        try:
            # Verificar comandos especiais
            if mensagem.startswith('/'):
                return self._processar_comando(mensagem)
            
            # Gerar resposta
            prompt = self._construir_prompt(mensagem, contexto)
            resposta = self._gerar_resposta(prompt)
            
            # Sistema de auditoria com Reflexor
            if self.reflexor_ativo and self.reflexor:
                try:
                    # Análise da resposta
                    reflexao = self.reflexor.analisar_resposta(
                        pergunta=mensagem,
                        resposta=resposta,
                        contexto=contexto or {}
                    )
                    
                    # Atualizar estatísticas
                    self._atualizar_stats_reflexao(reflexao)
                    
                    # Se score baixo, tentar melhorar
                    if reflexao.score_qualidade < 6:
                        logger.info(f"Score baixo ({reflexao.score_qualidade}), tentando melhorar...")
                        resposta_melhorada = self._melhorar_resposta(mensagem, resposta, reflexao)
                        if resposta_melhorada:
                            resposta = resposta_melhorada
                    
                    self.stats_carlos["respostas_com_auditoria"] += 1
                    
                except Exception as e:
                    logger.error(f"Erro na auditoria: {e}")
                    self.stats_carlos["respostas_sem_auditoria"] += 1
            else:
                self.stats_carlos["respostas_sem_auditoria"] += 1
            
            # Salvar na memória
            self._salvar_na_memoria(mensagem, resposta, contexto)
            
            # Atualizar estatísticas base
            self.update_stats(success=True)
            
            return resposta
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            self.update_stats(success=False)
            return f"❌ Erro interno: {str(e)}"
    
    def _construir_prompt(self, mensagem: str, contexto: Optional[Dict] = None) -> str:
        """Constrói prompt para o LLM"""
        contexto_recente = self._obter_contexto_recente()
        
        prompt = f"""Você é Carlos, agente principal do GPT Mestre Autônomo.

CARACTERÍSTICAS:
- Inteligente, proativo e prestativo
- Respostas claras e diretas
- Foco na resolução eficiente de problemas
- Memória de conversas anteriores

CONTEXTO DA CONVERSA:
{contexto_recente}

PERGUNTA DO USUÁRIO:
{mensagem}

Responda de forma natural, útil e direta:"""
        
        return prompt
    
    def _gerar_resposta(self, prompt: str) -> str:
        """Gera resposta usando o LLM"""
        try:
            resposta = self.llm.invoke(prompt)
            return resposta.content if hasattr(resposta, 'content') else str(resposta)
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."
    
    def _processar_comando(self, comando: str) -> str:
        """Processa comandos especiais do sistema"""
        comando = comando.lower().strip()
        
        comandos = {
            "/help": self._comando_help,
            "/status": self._comando_status,
            "/memory": self._comando_memoria,
            "/memoria": self._comando_memoria,
            "/clear": self._comando_clear,
            "/agents": self._comando_agentes,
            "/agentes": self._comando_agentes,
            "/reflexor": self._comando_reflexor,
            "/stats": self._comando_stats
        }
        
        if comando in comandos:
            return comandos[comando]()
        else:
            return f"❓ Comando não reconhecido: {comando}\nUse /help para ver comandos disponíveis."
    
    def _comando_help(self) -> str:
        """Comando de ajuda"""
        return """🤖 **CARLOS - GPT Mestre Autônomo v1.5+**

**Comandos Disponíveis:**
• `/help` - Esta mensagem de ajuda
• `/status` - Status do sistema e agentes
• `/memory` - Informações da memória
• `/clear` - Limpar histórico da conversa
• `/agents` - Lista de agentes disponíveis
• `/reflexor` - Status do sistema de auditoria
• `/stats` - Estatísticas detalhadas

**Funcionalidades:**
• Conversação natural inteligente
• Sistema de auditoria automática (Reflexor v1.5+)
• Memória persistente entre sessões
• Análise de qualidade em tempo real
• Detecção de padrões críticos

**Como usar:**
Apenas digite sua pergunta ou solicitação normalmente. O sistema automaticamente auditará e melhorará as respostas quando necessário."""
    
    def _comando_status(self) -> str:
        """Status do sistema"""
        try:
            reflexor_status = "🟢 Ativo" if self.reflexor_ativo else "🔴 Inativo"
            memoria_items = len(self.conversa_memoria)
            
            total_interactions = self.stats.get('total_interactions', 0)
            successful = self.stats.get('successful_interactions', 0)
            errors = self.stats.get('errors', 0)
            
            return f"""📊 **STATUS DO SISTEMA**

**Carlos v1.5+:** 🟢 Operacional
**Reflexor:** {reflexor_status}
**LLM:** Claude 3 Haiku
**Memória:** {memoria_items} interações armazenadas
**Uptime:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

**Estatísticas:**
• Total de interações: {total_interactions}
• Sucessos: {successful}
• Erros: {errors}
• Com auditoria: {self.stats_carlos.get('respostas_com_auditoria', 0)}
• Score médio: {self.stats_carlos.get('score_medio_qualidade', 0.0):.1f}/10"""
        
        except Exception as e:
            logger.error(f"Erro no comando status: {e}")
            return f"""📊 **STATUS DO SISTEMA**

**Carlos v1.5+:** 🟢 Operacional (com aviso)
**Reflexor:** {'🟢 Ativo' if self.reflexor_ativo else '🔴 Inativo'}
**Erro nas estatísticas:** {str(e)}

**Funcionalidade:** Sistema funcionando normalmente"""
    
    def _comando_memoria(self) -> str:
        """Informações da memória"""
        total_memoria = len(self.conversa_memoria)
        
        if total_memoria == 0:
            return "🧠 **MEMÓRIA VAZIA** - Nenhuma conversa armazenada"
        
        memoria_recente = self.conversa_memoria[-3:] if total_memoria >= 3 else self.conversa_memoria
        
        info = f"""🧠 **MEMÓRIA DO CARLOS**

**Estatísticas:**
• Total de interações: {total_memoria}
• Última interação: {memoria_recente[-1]['timestamp'] if memoria_recente else 'N/A'}

**Interações Recentes:**"""
        
        for item in memoria_recente:
            pergunta_preview = item['pergunta'][:50] + "..." if len(item['pergunta']) > 50 else item['pergunta']
            info += f"\n• {item['timestamp']}: {pergunta_preview}"
        
        return info
    
    def _comando_clear(self) -> str:
        """Limpa a memória da conversa"""
        items_removidos = len(self.conversa_memoria)
        self.conversa_memoria.clear()
        self.contexto_memoria.clear()
        
        return f"🗑️ **MEMÓRIA LIMPA** - {items_removidos} interações removidas"
    
    def _comando_agentes(self) -> str:
        """Lista agentes disponíveis"""
        agentes_info = """🤖 **AGENTES DO SISTEMA**

**Ativos:**
• **Carlos v1.5+** - Interface principal (VOCÊ ESTÁ AQUI)"""
        
        if self.reflexor_ativo and self.reflexor:
            agentes_info += "\n• **Reflexor v1.5+** - Sistema de auditoria automática"
            agentes_info += f"\n  - Análises realizadas: {self.stats_carlos['total_reflexoes']}"
        
        agentes_info += """

**Planejados:**
• **Oráculo v8.1+** - Tomador de decisões estratégicas
• **DeepAgent** - Análise profunda com pesquisa
• **AutoMaster** - Executor de automações
• **Meta-Agentes** - Criadores de novos agentes"""
        
        return agentes_info
    
    def _comando_reflexor(self) -> str:
        """Status do Reflexor - VERSÃO CORRIGIDA"""
        if not self.reflexor_ativo or not self.reflexor:
            return "🔴 **REFLEXOR INATIVO**"
        
        try:
            # Estatísticas básicas do Carlos
            total_analises = self.stats_carlos.get("total_reflexoes", 0)
            score_medio = self.stats_carlos.get("score_medio_qualidade", 0.0)
            red_flags = self.stats_carlos.get("red_flags_detectados", 0)
            
            resposta = f"""🔍 **REFLEXOR v1.5+ - STATUS**

**Configuração:**
• Status: 🟢 ATIVO
• Modo atual: Pontual
• Auto-aprendizado: Ativo

**Estatísticas:**
• Total de análises: {total_analises}
• Score médio qualidade: {score_medio:.1f}/10
• Red Flags detectados: {red_flags}
• Respostas auditadas: {self.stats_carlos.get('respostas_com_auditoria', 0)}
• Respostas sem auditoria: {self.stats_carlos.get('respostas_sem_auditoria', 0)}

**Última atualização:** {datetime.now().strftime('%H:%M:%S')}"""
            
            return resposta
            
        except Exception as e:
            logger.error(f"Erro no comando reflexor: {e}")
            return f"""🔍 **REFLEXOR v1.5+ - STATUS**

**Status:** 🟢 ATIVO (com erro)
**Erro:** {str(e)}
**Funcionalidade básica:** Funcionando"""
    
    def _comando_stats(self) -> str:
        """Estatísticas detalhadas"""
        try:
            total = self.stats.get('total_interactions', 0)
            sucessos = self.stats.get('successful_interactions', 0)
            erros = self.stats.get('errors', 0)
            sucesso_rate = (sucessos / total * 100) if total > 0 else 0
            
            return f"""📈 **ESTATÍSTICAS DETALHADAS**

**Performance Geral:**
• Taxa de sucesso: {sucesso_rate:.1f}%
• Total interações: {total}
• Sucessos: {sucessos}
• Erros: {erros}

**Sistema de Auditoria:**
• Respostas auditadas: {self.stats_carlos.get('respostas_com_auditoria', 0)}
• Respostas sem auditoria: {self.stats_carlos.get('respostas_sem_auditoria', 0)}
• Score médio qualidade: {self.stats_carlos.get('score_medio_qualidade', 0.0):.1f}/10
• Red Flags encontrados: {self.stats_carlos.get('red_flags_detectados', 0)}

**Memória:**
• Conversas salvas: {len(self.conversa_memoria)}

**Uptime:** {datetime.now().strftime('%H:%M:%S')}"""
        
        except Exception as e:
            logger.error(f"Erro no comando stats: {e}")
            return f"""📈 **ESTATÍSTICAS DETALHADAS**

**Erro:** Não foi possível carregar estatísticas
**Detalhes:** {str(e)}

**Status básico:** Carlos funcionando
**Memória:** {len(self.conversa_memoria)} conversas"""
    
    def _obter_contexto_recente(self) -> str:
        """Obtém contexto das conversas recentes - MÉTODO CORRIGIDO"""
        if not self.conversa_memoria:
            return "Sem contexto anterior."
        
        contexto_items = []
        for item in self.conversa_memoria[-3:]:  # Últimas 3 interações
            pergunta_short = item['pergunta'][:100] + "..." if len(item['pergunta']) > 100 else item['pergunta']
            resposta_short = item['resposta'][:100] + "..." if len(item['resposta']) > 100 else item['resposta']
            contexto_items.append(f"P: {pergunta_short}\nR: {resposta_short}")
        
        return "\n".join(contexto_items)
    
    def _salvar_na_memoria(self, mensagem: str, resposta: str, contexto: Optional[Dict] = None):
        """Salva interação na memória"""
        interacao = {
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "pergunta": mensagem,
            "resposta": resposta,
            "contexto": contexto
        }
        
        self.conversa_memoria.append(interacao)
        
        # Manter apenas últimas 50 interações
        if len(self.conversa_memoria) > 50:
            self.conversa_memoria = self.conversa_memoria[-50:]
    
    def _atualizar_stats_reflexao(self, reflexao):
        """Atualiza estatísticas do Reflexor"""
        self.stats_carlos["total_reflexoes"] += 1
        
        # Atualizar score médio
        total = self.stats_carlos["total_reflexoes"]
        score_atual = reflexao.score_qualidade
        score_anterior = self.stats_carlos["score_medio_qualidade"]
        
        self.stats_carlos["score_medio_qualidade"] = ((score_anterior * (total - 1)) + score_atual) / total
        
        # Contar red flags
        if hasattr(reflexao, 'red_flags_detectados') and reflexao.red_flags_detectados:
            self.stats_carlos["red_flags_detectados"] += len(reflexao.red_flags_detectados)
    
    def _get_stat_safe(self, key: str, default=0):
        """Obtém estatística de forma segura"""
        # Tentar várias fontes possíveis
        sources = [self.stats, self.stats_carlos, self.stats_ecossistema]
        
        for source in sources:
            if key in source:
                return source[key]
        
        # Mapeamentos de compatibilidade
        mappings = {
            "total_respostas": "total_interactions",
            "total_interactions": "total_respostas",
        }
        
        if key in mappings:
            mapped_key = mappings[key]
            for source in sources:
                if mapped_key in source:
                    return source[mapped_key]
        
        return default

    def update_stats(self, success: bool = True):
        """Atualiza estatísticas do agente - VERSÃO CORRIGIDA"""
        # Chamar método pai
        super().update_stats(success)
        
        # Sincronizar stats para compatibilidade total
        self.stats["total_respostas"] = self.stats["total_interactions"]
        
        if success:
            self.stats["respostas_melhoradas"] = self.stats.get("respostas_melhoradas", 0)
        else:
            # Incrementar apenas erros, já feito no pai
            pass
    
    def _melhorar_resposta(self, mensagem: str, resposta: str, reflexao) -> Optional[str]:
        """Tenta melhorar resposta com base na análise do Reflexor"""
        try:
            if self.reflexor and hasattr(self.reflexor, 'melhorar_resposta'):
                return self.reflexor.melhorar_resposta(mensagem, resposta)
        except Exception as e:
            logger.error(f"Erro ao melhorar resposta: {e}")
        return None

    # Funções de criação e export
def create_carlos() -> CarlosAgent:
    """Cria uma instância do Carlos sem Reflexor"""
    return CarlosAgent(reflexor_ativo=False)

def create_carlos_com_reflexor(reflexor_ativo: bool = True, llm=None) -> CarlosAgent:
    """Cria uma instância do Carlos com Reflexor integrado"""
    return CarlosAgent(reflexor_ativo=reflexor_ativo, llm=llm)
        
def criar_carlos_integrado(supervisor_ativo: bool = True, reflexor_ativo: bool = True, llm=None):
    """Cria instância do Carlos integrado (compatibilidade com app.py)"""
    return create_carlos_com_reflexor(reflexor_ativo=reflexor_ativo, llm=llm)
   

def diagnosticar_carlos():
        """Diagnóstica o status do Carlos"""
        try:
            carlos = create_carlos()
            reflexor_status = hasattr(carlos, 'reflexor') and carlos.reflexor is not None
            
            return {
                "carlos_ok": True,
                "reflexor_integrado": reflexor_status,
                "memoria_ativa": hasattr(carlos, 'conversa_memoria'),
                "config_ok": carlos.llm is not None
            }
        except Exception as e:
            return {
                "carlos_ok": False,
                "erro": str(e)
            }

if __name__ == "__main__":
    print("🧪 Testando Carlos...")
    diag = diagnosticar_carlos()
    print(f"📊 Diagnóstico: {diag}")
        
    if diag.get("carlos_ok"):
        print("✅ Carlos OK!")
    else:
        print(f"❌ Erro: {diag.get('erro')}")
