# 🤖 GPT Mestre Autônomo v4.0

> Sistema operacional autônomo com agentes inteligentes e arquitetura hierárquica suprema

[\![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[\![Streamlit](https://img.shields.io/badge/Streamlit-1.34+-red.svg)](https://streamlit.io)
[\![Claude 3](https://img.shields.io/badge/Claude%203-Sonnet%204-orange.svg)](https://anthropic.com)
[\![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌟 Visão Geral

O GPT Mestre Autônomo v4.0 é um sistema revolucionário de agentes inteligentes com **autonomia total**:

### 🧠 **Hierarquia Inteligente**
```
👑 Carlos v4.0 - Maestro Central (Coordenador Geral)
    ↓
🧠 Oráculo v8.1 - REGENTE SUPREMO (Supervisor de Excelência)
    ↓
🤖 Agentes Especializados
```

### 🚀 **Capacidades v4.0**
- **🧠 Interpretação automática** de qualquer comando
- **🔨 Quebra inteligente** de tarefas complexas (TaskBreaker)
- **⚡ Execução paralela** de múltiplos agentes
- **👑 Supervisão suprema** do Oráculo (Regente)
- **🎯 Padrão de excelência** garantido
- **🌐 Pesquisa web real** integrada
- **💾 Memória vetorial** persistente

## 🤖 Agentes Ativos

 < /dev/null |  Agente | Versão | Função | Status |
|--------|--------|--------|--------|
| **Carlos** | v4.0 | Maestro Central e Coordenador | ✅ ATIVO |
| **Oráculo** | v8.1+ | Regente Supremo e Supervisor | ✅ ATIVO |
| **SupervisorAI** | v1.4 | Classificação inteligente | ✅ ATIVO |
| **DeepAgent** | v2.0 | Pesquisa web real | ✅ ATIVO |
| **Reflexor** | v1.5+ | Auditoria de qualidade | ✅ ATIVO |
| **AutoMaster** | v4.0 | Planejamento estratégico | ✅ ATIVO |
| **TaskBreaker** | v1.0 | Quebra de tarefas | ✅ ATIVO |

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8+
- Chave API da Anthropic (Claude)
- Git (opcional)

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/gpt-mestre-autonomo.git
cd gpt-mestre-autonomo
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` com:
```env
ANTHROPIC_API_KEY=sua_chave_aqui
CLAUDE_MODEL=claude-3-sonnet-20241022
CLAUDE_MAX_TOKENS=8192
LOG_LEVEL=INFO
```

### 4. Execute o sistema
```bash
streamlit run app.py
```

### 5. Acesse no navegador
```
http://localhost:8501
```

## 🎯 Como Usar

### **Comando Universal**
O sistema interpreta **qualquer tipo de comando** automaticamente:

```bash
# Comercial
"Analise viabilidade de adesivo repelente infantil para revenda"

# Técnico  
"Desenvolva um app mobile com login e notificações"

# Pessoal
"Planeje minha carreira para os próximos 5 anos"

# Criativo
"Escreva um roteiro para vídeo de marketing"
```

### **Comandos do Sistema**
```bash
/help     # Hierarquia e comandos
/agents   # Lista todos os agentes
/status   # Status completo do sistema
/stats    # Estatísticas de desempenho
/agenda   # Agenda estratégica interna
```

## 🏗️ Arquitetura v4.0

### **Fluxo de Execução Autônoma**
```
Comando → Interpretação Automática → Análise de Complexidade
    ↓
[TaskBreaker] → Quebra em subtarefas (se complexo)
    ↓  
[Carlos] → Seleção dinâmica de agentes
    ↓
[Agentes] → Execução paralela/serial
    ↓
[Oráculo] → SUPERVISÃO SUPREMA (Aprovar/Melhorar/Refazer)
    ↓
Resposta Final de Excelência
```

### **Estrutura do Projeto**
```
gpt-mestre-autonomo/
├── 📄 app.py                  # Interface Streamlit
├── 📄 config.py               # Configurações
├── 📄 run.py                  # Script de execução
├── 📄 requirements.txt        # Dependências
├── 📄 test_sistema_v4.py      # Testes do sistema
├── 📁 agents/                 # Todos os agentes
│   ├── 📄 carlos.py           # Maestro Central v4.0
│   ├── 📄 oraculo.py          # Regente Supremo v8.1
│   ├── 📄 supervisor_ai.py    # Classificador v1.4
│   ├── 📄 deep_agent.py       # Web Search v2.0
│   ├── 📄 reflexor.py         # Auditor v1.5+
│   ├── 📄 automaster.py       # Estrategista v4.0
│   ├── 📄 task_breaker.py     # Decompositor v1.0
│   └── 📄 base_agent.py       # Classe base
├── 📁 memory/                 # Memória vetorial
│   └── 📄 vector_store.py     # ChromaDB
├── 📁 utils/                  # Utilitários
│   ├── 📄 logger.py           # Sistema de logging
│   └── 📄 web_search.py       # Web search real
└── 📁 tests/                  # Testes automatizados
```

## ⚙️ Configuração Avançada

### **Modelos Suportados**
- **Claude 3.5 Sonnet** (recomendado) - Qualidade superior
- **Claude 3 Haiku** - Rápido e econômico
- **Claude 3 Opus** - Máxima qualidade

### **Personalização**
```python
# Criar Carlos personalizado
carlos = criar_carlos_maestro(
    reflexor_ativo=True,      # Auditoria ativa
    supervisor_ativo=True,    # Classificação ativa
    oraculo_ativo=True,       # Supervisão suprema
    taskbreaker_ativo=True,   # Quebra de tarefas
    modo_proativo=True        # Modo proativo
)
```

## 🧪 Testes

### **Teste Completo**
```bash
python test_sistema_v4.py
```

### **Teste de Funcionalidades**
```bash
# Verificar TaskBreaker
python -c "
from agents.task_breaker import criar_task_breaker
tb = criar_task_breaker()
plano = tb.analisar_tarefa('Criar app mobile')
print(f'Subtarefas: {len(plano.subtarefas)}')
"
```

## 🌟 Características Únicas

### **1. Autonomia Total**
- ✅ Interpreta qualquer comando automaticamente
- ✅ Quebra tarefas complexas sozinho
- ✅ Seleciona agentes por capacidade
- ✅ Executa em paralelo quando possível

### **2. Supervisão Suprema**
- ✅ Oráculo avalia TODAS as respostas
- ✅ Assembleia dinâmica para decisões complexas
- ✅ Score de qualidade obrigatório (≥8.5/10)
- ✅ Poder de veto e melhoria

### **3. Resistência a Falhas**
- ✅ Funciona com dependências faltantes
- ✅ Fallbacks inteligentes
- ✅ Logger com múltiplos níveis
- ✅ Recuperação automática

## 💰 Custos Estimados

### **Desenvolvimento**
- **Software**: R$ 0 (open-source)
- **Tempo**: Sistema completo pronto

### **Operação Mensal**
- **Claude API**: R$ 10-50/mês (uso médio)
- **Hospedagem local**: R$ 0
- **Total**: R$ 10-50/mês

## 🔧 Desenvolvimento

### **Executando Testes**
```bash
# Teste completo
python test_sistema_v4.py

# Teste específico  
python -m pytest tests/

# Verificar imports
python -c "from agents import carlos; print('✅ OK')"
```

### **Adicionando Novos Agentes**
1. Crie arquivo em `agents/novo_agente.py`
2. Herde de `BaseAgent`
3. Implemente `processar()` 
4. Registre no Carlos

## 🐛 Solução de Problemas

### **Problemas Comuns**
```bash
# Dependências faltando
pip install -r requirements.txt

# API key missing
echo "ANTHROPIC_API_KEY=sua_chave" > .env

# Teste de funcionamento
python test_sistema_v4.py
```

### **Logs e Debug**
- **Sistema**: Logs automáticos no console
- **Agentes**: Logs específicos por agente
- **Erros**: Tratamento automático com fallbacks

## 🏆 Status do Projeto

✅ **Sistema 100% funcional**  
✅ **Todos os agentes ativos**  
✅ **Autonomia total implementada**  
✅ **Supervisão suprema funcionando**  
✅ **TaskBreaker criando subtarefas**  
✅ **Web search real integrada**  
✅ **Memória vetorial persistente**  
✅ **Resistente a falhas**  

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Anthropic](https://anthropic.com) pelo Claude
- [LangChain](https://langchain.com) pelo framework
- [Streamlit](https://streamlit.io) pela interface
- [ChromaDB](https://www.trychroma.com/) pela memória vetorial

---

**🚀 GPT Mestre Autônomo v4.0 - Sistema de Agentes Inteligentes com Autonomia Total**

*Transcende o potencial de todos os outros sistemas* 🎯
