# 🚀 GPT Mestre Autônomo - Guia de Instalação Completo

## 📦 Dependências Críticas

### Instalação Automática
```bash
# 1. Criar ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 2. Instalar todas as dependências
pip install -r requirements.txt
```

### Instalação Manual (caso necessário)
```bash
# Core LLM e Orquestração
pip install google-generativeai>=0.4.0
pip install langchain-google-genai>=1.0.0
pip install anthropic>=0.25.0
pip install langchain>=0.3.0
pip install langchain-core>=0.3.0
pip install langchain-anthropic>=0.3.14

# Interface
pip install chainlit==1.2.0
pip install streamlit==1.34.0
pip install fastapi>=0.111.0
pip install uvicorn>=0.25.0

# Memória Vetorial
pip install chromadb==0.5.0
pip install sentence-transformers==2.7.0

# Web Search
pip install duckduckgo-search>=6.2.0
pip install httpx>=0.24.0
pip install beautifulsoup4>=4.12.0

# Utilitários
pip install python-dotenv==1.0.1
pip install requests==2.31.0
pip install pandas==2.2.2
pip install numpy<2.0.0
pip install loguru==0.7.2
```

## ⚙️ Configuração de Ambiente

### 1. Arquivo .env
Copie e configure o arquivo `.env` com suas chaves:

```bash
# === LLM PROVIDER CONFIGURATION ===
LLM_PROVIDER=gemini
GOOGLE_API_KEY=sua_chave_google_aqui

# Para usar Claude (alternativo)
# LLM_PROVIDER=anthropic
# ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
```

### 2. Verificação da Instalação
```bash
# Execute o sistema de auditoria para verificar
python3 system_audit.py
```

### 3. Inicialização
```bash
# Para interface Chainlit
chainlit run app.py

# Para interface Streamlit (alternativa)
streamlit run app_streamlit.py

# Para modo terminal
python3 app_terminal.py
```

## 🔧 Resolução de Problemas Comuns

### Erro: "No module named 'chainlit'"
```bash
pip install chainlit==1.2.0
```

### Erro: "No module named 'google.generativeai'"
```bash
pip install google-generativeai>=0.4.0
```

### Erro: "ChromaDB não disponível"
```bash
pip install chromadb==0.5.0
```

### Erro: "DuckDuckGo Search não disponível"
```bash
pip install duckduckgo-search>=6.2.0
```

## 🛡️ Segurança

### Variáveis de Ambiente Obrigatórias
- `GOOGLE_API_KEY`: Chave da API do Google Gemini
- `LLM_PROVIDER`: Provider padrão (gemini/anthropic)

### Arquivos Sensíveis
- `.env`: Nunca commitar para o Git
- `logs/`: Configurar rotação automática
- `memory/`: Backup regular recomendado

## ✅ Status do Sistema

### ✅ Componentes Funcionais
- BaseAgentV2: Sistema de robustez implementado
- Agentes v2.0: 10/10 agentes migrados
- Sistema de Auditoria: Funcionando
- Cache Manager: Ativo
- Logger: Funcionando
- Memória Persistente: Ativa

### ⚠️ Dependências Externas Necessárias
- chainlit: Interface principal
- google-generativeai: LLM Gemini
- langchain-google-genai: Integração Gemini
- chromadb: Banco vetorial
- duckduckgo-search: Web search

### 🎯 Próximos Passos
1. Instalar dependências listadas acima
2. Configurar chaves de API no .env
3. Executar auditoria final: `python3 system_audit.py`
4. Inicializar sistema: `chainlit run app.py`

## 📊 Sistema de Monitoramento

O sistema inclui auditoria automática que:
- ✅ Verifica estrutura de arquivos
- ✅ Testa imports e dependências  
- ✅ Valida funcionamento dos agentes
- ✅ Monitora configurações
- ✅ Executa testes automatizados
- ✅ Verifica sistemas de memória
- ✅ Audita logs e monitoramento
- ✅ Analisa segurança

Execute `python3 system_audit.py` após a instalação para validação completa.