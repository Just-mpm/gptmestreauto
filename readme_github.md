# 🤖 GPT Mestre Autônomo

> Sistema operacional autônomo com agentes inteligentes baseado em Claude 3 e LangChain

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.34+-red.svg)](https://streamlit.io)
[![Claude 3](https://img.shields.io/badge/Claude%203-Haiku-orange.svg)](https://anthropic.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🌟 Visão Geral

O GPT Mestre Autônomo é um sistema de agentes inteligentes que permite:

- **🗣️ Conversa natural** com interface "Carlos"
- **🤖 Agentes especializados** (Reflexor, Oráculo, DeepAgent, etc.)
- **🧠 Memória persistente** entre sessões
- **🔗 Integração com APIs externas**
- **⚙️ Automações e rotinas** em background
- **📈 Evolução contínua** com aprendizado

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.8+
- Chave API da Anthropic (Claude 3)
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
```bash
cp .env.example .env
# Edite o .env e adicione sua ANTHROPIC_API_KEY
```

### 4. Execute o sistema
```bash
python run.py
# OU
streamlit run app.py
```

### 5. Acesse no navegador
```
http://localhost:8501
```

## 🏗️ Arquitetura

### Camadas do Sistema
1. **Interface** - Chat frontend (Streamlit)
2. **Núcleo Cognitivo** - LLM + Agentes (Claude 3 + LangChain)  
3. **Execução & Automação** - Python + APIs + Scheduler
4. **Memória Persistente** - ChromaDB (vetorial)
5. **Integrações Externas** - APIs diversas

### 🤖 Agentes Principais
- **Carlos** - Interface principal e coordenador ✅
- **Reflexor** - Auditor interno e validador (Fase 2)
- **Oráculo** - Tomador de decisões estratégicas (Fase 3)
- **DeepAgent** - Análise profunda e pesquisa (Fase 3)
- **AutoMaster** - Automações e execuções (Fase 3)

## 📁 Estrutura do Projeto

```
gpt-mestre-autonomo/
├── 📄 app.py              # Interface Streamlit principal
├── 📄 config.py           # Configurações centralizadas  
├── 📄 run.py              # Script de execução
├── 📄 requirements.txt    # Dependências Python
├── 📄 .env.example        # Exemplo de configuração
├── 📁 agents/             # Agentes do sistema
│   ├── base_agent.py      # Classe base dos agentes
│   └── carlos.py          # Agente Carlos (interface)
├── 📁 utils/              # Utilitários
│   └── logger.py          # Sistema de logging
├── 📁 memory/             # Memória vetorial (ChromaDB)
├── 📁 logs/               # Logs do sistema
└── 📁 integrations/       # Integrações externas (futuro)
```

## 🎯 Como Usar

### Interface Principal
1. **Conversa Normal**
   ```
   "Olá Carlos, me ajude a criar um plano de marketing"
   ```

2. **Comandos Especiais**
   ```
   /help    - Mostra ajuda completa
   /status  - Status do sistema  
   /memory  - Informações da memória
   /clear   - Limpa a sessão atual
   /agents  - Lista agentes disponíveis
   ```

## ⚙️ Configuração

### Arquivo .env
```env
# Configurações principais
DEBUG=False
ANTHROPIC_API_KEY=sk-ant-api03-sua_chave_aqui

# Configurações opcionais (futuras fases)
TELEGRAM_BOT_TOKEN=seu_token_aqui
NOTION_API_KEY=sua_chave_aqui
```

### Modelos Suportados
- **Claude 3 Haiku** (padrão) - Rápido e econômico
- **Claude 3 Sonnet** - Qualidade superior
- **Claude 3 Opus** - Máxima qualidade

## 🔄 Fases de Desenvolvimento

**✅ Fase 1 - MVP Básico** (Atual)
- Interface Streamlit com Carlos
- Sistema de logging
- Configuração base
- Memória básica

**🔄 Fase 2 - Memória Vetorial**
- ChromaDB integrado
- Busca semântica
- Agente Reflexor

**⏳ Fase 3 - Agentes Avançados**
- Oráculo e DeepAgent
- Scheduler básico
- Executor de funções

**⏳ Fase 4 - Integrações**
- APIs externas (Telegram, Notion)
- Webhooks
- Painel de controle

**⏳ Fase 5 - Automação Completa**
- Rotinas em background
- Meta-agentes
- Auto-evolução

## 💰 Custos Estimados

### Desenvolvimento
- **Software**: R$ 0 (open-source)
- **Tempo**: 3-9 meses (conforme complexidade)

### Operação Mensal
- **Claude 3 Haiku API**: R$ 5-30/mês (uso básico)
- **Hospedagem local**: R$ 0
- **Total**: R$ 5-30/mês para uso pessoal

## 🛠️ Desenvolvimento

### Adicionando Novos Agentes
1. Crie arquivo em `agents/novo_agente.py`
2. Herde de `BaseAgent`
3. Implemente `_default_personality()` e `process_message()`
4. Registre em `config.py`

### Comandos Úteis
```bash
# Verificar sistema
python run.py --check

# Configuração inicial
python run.py --setup

# Executar testes
python test_basic.py

# Limpar cache
rm -rf __pycache__ logs/*.log
```

## 🐛 Solução de Problemas

### Problemas Comuns
- **"Module not found"**: Execute `pip install -r requirements.txt`
- **"API key missing"**: Configure `ANTHROPIC_API_KEY` no `.env`
- **Interface não carrega**: Verifique se porta 8501 está livre

### Logs e Debug
- **Logs gerais**: `logs/gpt_mestre.log`
- **Logs de erros**: `logs/errors.log`  
- **Debug mode**: Configure `DEBUG=True` no `.env`

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Faça fork do projeto
2. Crie uma branch para sua feature
3. Implemente e teste suas alterações
4. Submeta um pull request

### Áreas que Precisam de Ajuda
- Novos agentes especializados
- Integrações com APIs
- Melhorias na interface
- Documentação
- Testes automatizados

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [Anthropic](https://anthropic.com) pelo Claude 3
- [LangChain](https://langchain.com) pelo framework
- [Streamlit](https://streamlit.io) pela interface
- Comunidade open-source

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/seu-usuario/gpt-mestre-autonomo/issues)
- **Discussões**: [GitHub Discussions](https://github.com/seu-usuario/gpt-mestre-autonomo/discussions)
- **Email**: seu-email@exemplo.com

---

**🚀 Desenvolvido com ❤️ por [Seu Nome](https://github.com/seu-usuario)**

*Sistema de agentes inteligentes para automação e produtividade*