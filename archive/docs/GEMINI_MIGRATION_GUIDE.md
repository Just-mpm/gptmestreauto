# 🚀 Guia de Migração para Google Gemini 2.5 Flash

## 📋 Visão Geral

Este guia documenta a migração do GPT Mestre Autônomo para usar o Google Gemini 2.5 Flash como provider de LLM, mantendo compatibilidade com Anthropic Claude.

## 🎯 O que foi implementado

### 1. **Multi-Provider Support**
- ✅ Sistema agora suporta tanto Google Gemini quanto Anthropic Claude
- ✅ Fácil troca entre providers via variável de ambiente
- ✅ Compatibilidade total mantida com código existente

### 2. **LLM Factory Pattern**
- ✅ Novo módulo `utils/llm_factory.py` para abstração de LLMs
- ✅ Suporte unificado para diferentes providers
- ✅ Configuração automática baseada em environment

### 3. **Atualizações Realizadas**
- ✅ `config.py` - Suporte para ambos os providers
- ✅ `requirements.txt` - Dependências do Google Gemini adicionadas
- ✅ `base_agent_v2.py` - Usa novo sistema LLM Factory
- ✅ `carlos.py` - Migrado para multi-provider
- ✅ `deep_agent_v2.py` - Suporte Gemini em cliente direto

## 🔧 Configuração

### 1. **Instalar Dependências**

```bash
pip install -r requirements.txt
```

### 2. **Configurar Variáveis de Ambiente**

Crie ou edite o arquivo `.env` na raiz do projeto:

```env
# Escolha o provider (gemini ou anthropic)
LLM_PROVIDER=gemini

# Para usar Google Gemini
GOOGLE_API_KEY=sua_chave_api_gemini_aqui

# Para usar Anthropic (opcional, apenas se quiser manter compatibilidade)
ANTHROPIC_API_KEY=sua_chave_anthropic_aqui
```

### 3. **Obter API Key do Google Gemini**

1. Acesse: https://makersuite.google.com/app/apikey
2. Clique em "Create API Key"
3. Copie a chave gerada
4. Cole no arquivo `.env` como `GOOGLE_API_KEY`

## 🔄 Como Alternar Entre Providers

### Usar Google Gemini (Padrão)
```env
LLM_PROVIDER=gemini
GOOGLE_API_KEY=sua_chave_aqui
```

### Usar Anthropic Claude
```env
LLM_PROVIDER=anthropic
ANTHROPIC_API_KEY=sua_chave_aqui
```

## 📊 Comparação de Modelos

| Feature | Gemini 2.5 Flash | Claude 3.5 Haiku |
|---------|------------------|------------------|
| Max Tokens | 8192 | 4000 |
| Velocidade | ⚡ Muito Rápido | ⚡ Rápido |
| Custo | 💰 Mais Barato | 💰 Moderado |
| Web Search | ✅ Suportado | ✅ Suportado |
| Streaming | ✅ Sim | ✅ Sim |

## 🚨 Configurações de Segurança (Gemini)

O sistema já está configurado com níveis seguros:

```python
GEMINI_SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH", 
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_ONLY_HIGH"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_ONLY_HIGH"
    }
]
```

## 🛠️ Uso Programático

### Criar LLM com configuração padrão
```python
from utils.llm_factory import create_llm

# Usa provider do config.py
llm = create_llm()
response = llm.invoke("Olá!")
print(response.content)
```

### Forçar provider específico
```python
# Forçar Gemini
llm = create_llm(provider="gemini")

# Forçar Anthropic
llm = create_llm(provider="anthropic")
```

### Personalizar parâmetros
```python
llm = create_llm(
    temperature=0.9,  # Mais criativo
    max_tokens=2000   # Limitar tokens
)
```

## 📝 Alterações no Código

### Para Desenvolvedores

1. **BaseAgentV2** agora tenta usar `llm_factory` primeiro
2. **Carlos** usa o novo sistema com fallback para compatibilidade
3. **DeepAgent** suporta Gemini em modo cliente direto

### Compatibilidade

- ✅ Todo código existente continua funcionando
- ✅ Variáveis legadas mantidas (`CLAUDE_MODEL`, etc.)
- ✅ Fallback automático se `llm_factory` não disponível

## 🎯 Modelo Recomendado

```
models/gemini-2.5-flash-preview-05-20
```

Este é o modelo Gemini 2.5 Flash mais recente, otimizado para:
- ⚡ Velocidade extrema
- 💰 Custo reduzido
- 🧠 Qualidade comparável ao Claude
- 📏 Suporte para 8K tokens

## 🐛 Troubleshooting

### Erro: "GOOGLE_API_KEY não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme que a chave está configurada corretamente
- Reinicie o aplicativo após configurar

### Erro: "LLM_PROVIDER inválido"
- Use apenas "gemini" ou "anthropic" como valor
- Verifique ortografia no `.env`

### Respostas diferentes entre providers
- Normal - cada modelo tem seu estilo
- Ajuste `temperature` se necessário
- Gemini tende a ser mais conciso

## 📚 Recursos Adicionais

- [Documentação Google Gemini](https://ai.google.dev/docs)
- [Gemini API Reference](https://ai.google.dev/api/python/google/generativeai)
- [Preços Gemini](https://ai.google.dev/pricing)

## ✅ Checklist de Migração

- [ ] Instalar dependências: `pip install -r requirements.txt`
- [ ] Obter API Key do Google Gemini
- [ ] Configurar `.env` com `LLM_PROVIDER=gemini`
- [ ] Adicionar `GOOGLE_API_KEY` ao `.env`
- [ ] Testar sistema: `python config.py`
- [ ] Verificar logs para confirmar "Gemini configurado"

## 🎉 Pronto!

Seu sistema agora está usando Google Gemini 2.5 Flash! 

Para voltar ao Claude a qualquer momento, apenas mude:
```env
LLM_PROVIDER=anthropic
```