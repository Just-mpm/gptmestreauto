# 🚀 Guia de Execução - GPT Mestre Autônomo v5.0

## ⚡ Execução Rápida

### 1. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar API
Criar arquivo `.env` na raiz do projeto:
```env
GOOGLE_API_KEY=sua_chave_gemini_aqui
```

### 3. Executar Sistema
```bash
chainlit run app.py -w
```

### 4. Acessar Interface
Abrir navegador em: `http://localhost:8000`

## 🔧 Solução de Problemas

### Erro: "1 validation error for Action"
✅ **Corrigido na versão atual**
- Problema era conflito de decoradores `@cl.on_chat_start`
- Solução: Actions integradas no start() principal

### Cache não funcionando
```bash
# Limpar cache se necessário
rm -rf data/cache.db
```

### Logs de debug
```bash
# Ver logs em tempo real
tail -f logs/gpt_mestre.log
```

## 📊 Comandos de Teste

### Testar Comandos Naturais
```
"Carlos, como está o sistema?"
"Carlos, quem está por aí?"
"Ping"
```

### Testar Onboarding
- Acesse como usuário novo
- Sistema iniciará automaticamente

### Testar Cache
```
"Qual a capital da França?"
# Repetir - deve usar cache
```

## 🎯 Estrutura Limpa

### Arquivos Principais
```
📱 app.py              # Interface principal
🔧 config.py           # Configurações  
🤖 agents/             # Agentes especializados
🛠️ utils/              # Otimizações
```

### Arquivos Arquivados
```
📚 archive/
├── docs/              # Documentos antigos
├── tests_old/         # Testes antigos  
└── apps_old/          # Apps antigos
```

## 💡 Dicas de Uso

### Para Desenvolvimento
```bash
# Modo desenvolvimento com reload
chainlit run app.py -w --reload
```

### Para Produção
```bash
# Modo produção
chainlit run app.py --host 0.0.0.0 --port 8000
```

### Monitoramento
- Use botões de ação na interface
- Comandos naturais economizam tokens
- Dashboard mostra custos em tempo real

---

**Sistema pronto para uso! Todas as 5 etapas implementadas e testadas.**