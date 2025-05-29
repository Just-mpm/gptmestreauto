# 🤖 GPT Mestre Autônomo

Sistema operacional autônomo com agentes inteligentes baseado em GPT-4 e LangChain.

## 📋 Visão Geral

O GPT Mestre Autônomo é um sistema de agentes inteligentes que permite:

- **Conversa natural** com interface "Carlos"
- **Agentes especializados** (Reflexor, Oráculo, DeepAgent, etc.)
- **Memória persistente** entre sessões
- **Integração com APIs externas**
- **Automações e rotinas em background**
- **Evolução contínua** com aprendizado

## 🏗️ Arquitetura

### Camadas do Sistema

1. **Interface** - Chat frontend (Streamlit/React)
2. **Núcleo Cognitivo** - LLM + Agentes (GPT-4 + LangChain)  
3. **Execução & Automação** - Python + APIs + Scheduler
4. **Memória Persistente** - ChromaDB (vetorial)
5. **Integrações Externas** - APIs diversas

### Agentes Principais

- **Carlos** - Interface principal e coordenador
- **Reflexor** - Auditor interno e validador
- **Oráculo** - Tomador de decisões estratégicas
- **DeepAgent** - Análise profunda e pesquisa
- **AutoMaster** - Automações e execuções

## 🚀 Instalação Rápida

### Pré-requisitos

- Python 3.8+
- Chave API da OpenAI
- Git (opcional)

### Passo a Passo

1. **Clone o projeto** (ou baixe os arquivos)
```bash
git clone <repository-url>
cd gpt-mestre-autonomo
```

2. **Configuração inicial**
```bash
python run.py --setup
```

3. **Instale dependências**
```bash
pip install -r requirements.txt
```

4. **Configure sua API Key**
- Edite o arquivo `.env`
- Adicione sua `OPENAI_API_KEY=sk-sua-chave-aqui`

5. **Execute o sistema**
```bash
python run.py
```

6. **Acesse no navegador**
- Abra: `http://localhost:8501`
- Comece a conversar com Carlos!

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
   - Digite qualquer pergunta para Carlos
   - Ele responde naturalmente e mantém contexto
   - Exemplo: "Olá Carlos, me ajude a criar um plano de marketing"

2. **Comandos Especiais**
   - `/help` - Mostra ajuda completa
   - `/status` - Status do sistema  
   - `/memory` - Informações da memória
   - `/clear` - Limpa a sessão atual
   - `/agents` - Lista agentes disponíveis

### Exemplos de Uso

```
Usuário: "Analise este texto e me dê sugestões de melhoria"
Carlos: Vou analisar seu texto detalhadamente...

Usuário: "/status" 
Carlos: 📊 Status do GPT Mestre Autônomo:
        ✅ Carlos ativo e operacional...

Usuário: "Crie um cronograma para meu projeto"
Carlos: Vou criar um cronograma estruturado para você...
```

## ⚙️ Configuração Avançada

### Arquivo .env

```bash
# Configurações principais
DEBUG=False
OPENAI_API_KEY=sk-sua-chave-openai-aqui

# Configurações opcionais  
LOG_LEVEL=INFO
API_HOST=0.0.0.0
API_PORT=8000

# Integrações futuras
TELEGRAM_BOT_TOKEN=
NOTION_API_KEY=
```

### Parâmetros do Sistema

Edite `config.py` para ajustar:

- **Modelo LLM**: `DEFAULT_MODEL = "gpt-4-turbo"`
- **Temperatura**: `TEMPERATURE = 0.7`
- **Máximo de tokens**: `MAX_TOKENS = 4000`
- **Agentes ativos**: `AGENTES_ATIVOS = [...]`

## 🔧 Desenvolvimento

### Fases de Desenvolvimento

**✅ Fase 1 - MVP Básico** (Atual)
- Interface Streamlit com Carlos
- Sistema de logging
- Configuração base
- Memória básica

**🔄 Fase 2 - Memória Vetorial** (Próxima)
- ChromaDB integrado
- Busca semântica
- Agente Reflexor

**⏳ Fase 3 - Agentes Avançados**
- Oráculo e DeepAgent
- Scheduler básico
- Executor de funções

**⏳ Fase 4 - Integrações**
- APIs externas
- Webhooks
- Painel de controle

**⏳ Fase 5 - Automação Completa**
- Rotinas em background
- Meta-agentes
- Auto-evolução

### Adicionando Novos Agentes

1. Crie arquivo em `agents/novo_agente.py`
2. Herde de `BaseAgent`
3. Implemente `_default_personality()` e `process_message()`
4. Registre em `config.py`

Exemplo:
```python
from agents.base_agent import BaseAgent

class NovoAgent(BaseAgent):
    def _default_personality(self):
        return "Personalidade do seu agente..."
    
    async def process_message(self, message, context=None):
        return await self.think(f"Processe: {message}")
```

## 🐛 Solução de Problemas

### Problemas Comuns

**❌ "Module not found"**
```bash
pip install -r requirements.txt
```

**❌ "API key missing"**  
- Configure `OPENAI_API_KEY` no arquivo `.env`

**❌ "Permission denied"**
- Execute como administrador/sudo
- Verifique permissões dos diretórios

**❌ Interface não carrega**
- Verifique se porta 8501 está livre
- Execute: `python run.py --check`

### Logs e Debug

- **Logs gerais**: `logs/gpt_mestre.log`
- **Logs de erros**: `logs/errors.log`  
- **Logs de agentes**: `logs/agents.log`
- **Debug mode**: Configure `DEBUG=True` no `.env`

### Comandos Úteis

```bash
# Verificar sistema
python run.py --check

# Configuração inicial
python run.py --setup

# Mostrar ajuda
python run.py --help

# Executar com logs verbose
DEBUG=True python run.py
```

## 💰 Custos Estimados

### Desenvolvimento
- **Software**: R$ 0 (open-source)
- **Tempo**: 3-9 meses (conforme complexidade)

### Operação Mensal
- **OpenAI API**: R$ 150-500+ (conforme uso)
- **Hospedagem**: R$ 50-150 (para produção)
- **Memória Vetorial**: R$ 0 (ChromaDB local)
- **Total**: R$ 210-780+/mês

## 🔮 Roadmap

### Próximas Funcionalidades

- [ ] Sistema de memória vetorial (ChromaDB)
- [ ] Agente Reflexor para auditoria
- [ ] Agente Oráculo para decisões
- [ ] Scheduler para automações
- [ ] API REST para integração
- [ ] Painel de métricas
- [ ] Integração com Telegram
- [ ] Integração com Notion/Sheets
- [ ] Sistema de webhooks
- [ ] Meta-agentes auto-evolutivos

### Integrações Planejadas

- **E-commerce**: Shopee, Magalu, AliExpress
- **Produtividade**: Notion, Google Sheets, Calendário
- **Comunicação**: Telegram, Discord, Slack
- **Análise**: Google Analytics, métricas personalizadas

## 🤝 Contribuição

Este é um projeto em desenvolvimento ativo. Contribuições são bem-vindas!

### Como Contribuir

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

Projeto em desenvolvimento por Matheus Meireles.

## 📞 Suporte

- **Logs**: Verifique `logs/` para diagnóstico
- **Issues**: Reporte problemas e sugestões
- **Documentação**: Este README e comentários no código

---

**🚀 Desenvolvido com ❤️ por Matheus Meireles**

*Sistema de agentes inteligentes para automação e produtividade*
