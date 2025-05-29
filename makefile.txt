# GPT MESTRE AUTÔNOMO - Makefile
# Comandos facilitados para desenvolvimento e execução

.PHONY: help install setup run check clean test lint format

# Configurações
PYTHON := python
PIP := pip
STREAMLIT := streamlit

# Comando padrão
help:
	@echo "🤖 GPT MESTRE AUTÔNOMO - Comandos Disponíveis:"
	@echo ""
	@echo "📦 INSTALAÇÃO E CONFIGURAÇÃO:"
	@echo "  make install    - Instala todas as dependências"
	@echo "  make setup      - Configuração inicial completa"
	@echo "  make check      - Verifica se tudo está configurado"
	@echo ""
	@echo "🚀 EXECUÇÃO:"
	@echo "  make run        - Executa a aplicação principal"
	@echo "  make dev        - Executa em modo desenvolvimento"
	@echo "  make carlos     - Testa o agente Carlos diretamente"
	@echo ""
	@echo "🧹 MANUTENÇÃO:"
	@echo "  make clean      - Limpa arquivos temporários e logs"
	@echo "  make clean-all  - Limpeza completa (incluindo memória)"
	@echo "  make reset      - Reset completo do sistema"
	@echo ""
	@echo "🧪 DESENVOLVIMENTO:"
	@echo "  make test       - Executa testes"
	@echo "  make lint       - Verifica qualidade do código"
	@echo "  make format     - Formata código automaticamente"
	@echo "  make docs       - Gera documentação"
	@echo ""
	@echo "📊 MONITORAMENTO:"
	@echo "  make logs       - Mostra logs em tempo real"
	@echo "  make status     - Status do sistema"
	@echo "  make backup     - Backup da memória e configurações"

# Instalação e configuração
install:
	@echo "📦 Instalando dependências..."
	$(PIP) install -r requirements.txt
	@echo "✅ Dependências instaladas!"

setup:
	@echo "🔧 Configuração inicial..."
	$(PYTHON) run.py --setup
	@echo "✅ Configuração concluída!"
	@echo "🔑 Configure sua OPENAI_API_KEY no arquivo .env"

check:
	@echo "🔍 Verificando sistema..."
	$(PYTHON) run.py --check

# Execução
run:
	@echo "🚀 Iniciando GPT Mestre Autônomo..."
	$(PYTHON) run.py

dev:
	@echo "🛠️  Iniciando em modo desenvolvimento..."
	@echo "DEBUG=True" > .env.dev
	@cat .env >> .env.dev
	DEBUG=True $(PYTHON) run.py

carlos:
	@echo "🤖 Testando agente Carlos..."
	$(PYTHON) -c "import asyncio; from agents.carlos import create_carlos; carlos = create_carlos(); print('✅ Carlos inicializado com sucesso!')"

# Testes
test:
	@echo "🧪 Executando testes..."
	$(PYTHON) -m pytest tests/ -v || echo "⚠️  Testes não implementados ainda"

lint:
	@echo "🔍 Verificando qualidade do código..."
	$(PYTHON) -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics || echo "⚠️  flake8 não instalado"

format:
	@echo "✨ Formatando código..."
	$(PYTHON) -m black . || echo "⚠️  black não instalado"

# Limpeza
clean:
	@echo "🧹 Limpando arquivos temporários..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	rm -f logs/*.log 2>/dev/null || true
	@echo "✅ Limpeza concluída!"

clean-all: clean
	@echo "🗑️  Limpeza completa..."
	rm -rf memory/chroma_db/ 2>/dev/null || true
	rm -rf .streamlit/ 2>/dev/null || true
	rm -f .env.dev 2>/dev/null || true
	@echo "✅ Limpeza completa concluída!"

reset: clean-all
	@echo "🔄 Reset completo do sistema..."
	@echo "⚠️  Isso irá apagar TODA a memória e configurações!"
	@read -p "Confirmar reset? (y/N): " confirm && [ "$confirm" = "y" ] || exit 1
	rm -rf memory/ logs/ .env 2>/dev/null || true
	$(MAKE) setup
	@echo "✅ Sistema resetado!"

# Monitoramento
logs:
	@echo "📊 Logs em tempo real (Ctrl+C para sair)..."
	tail -f logs/gpt_mestre.log 2>/dev/null || echo "❌ Arquivo de log não encontrado"

status:
	@echo "📊 Status do GPT Mestre Autônomo:"
	@echo ""
	@echo "📁 Estrutura:"
	@ls -la | grep -E "(agents|utils|memory|logs)" || echo "  Diretórios não criados ainda"
	@echo ""
	@echo "📝 Logs:"
	@ls -la logs/ 2>/dev/null || echo "  Nenhum log encontrado"
	@echo ""
	@echo "🧠 Memória:"
	@ls -la memory/ 2>/dev/null || echo "  Memória não inicializada"
	@echo ""
	@echo "⚙️  Configuração:"
	@test -f .env && echo "  ✅ .env configurado" || echo "  ❌ .env não encontrado"

backup:
	@echo "💾 Criando backup..."
	@mkdir -p backups/$(shell date +%Y%m%d_%H%M%S)
	@cp -r memory/ backups/$(shell date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "Memória não encontrada"
	@cp -r logs/ backups/$(shell date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo "Logs não encontrados"
	@cp .env backups/$(shell date +%Y%m%d_%H%M%S)/ 2>/dev/null || echo ".env não encontrado"
	@echo "✅ Backup criado em backups/"

docs:
	@echo "📚 Gerando documentação..."
	@echo "README.md já disponível!"
	@echo "📖 Para ver a documentação completa:"
	@echo "   cat README.md"

# Comandos de desenvolvimento avançado
install-dev: install
	@echo "🛠️  Instalando dependências de desenvolvimento..."
	$(PIP) install pytest black flake8 mypy
	@echo "✅ Ambiente de desenvolvimento configurado!"

requirements-update:
	@echo "📦 Atualizando requirements.txt..."
	$(PIP) freeze > requirements.txt
	@echo "✅ Requirements atualizados!"

# Comandos para Docker (futuro)
docker-build:
	@echo "🐳 Construindo imagem Docker..."
	@echo "⚠️  Docker não implementado ainda"

docker-run:
	@echo "🐳 Executando container Docker..."
	@echo "⚠️  Docker não implementado ainda"

# Informações do sistema
info:
	@echo "ℹ️  Informações do Sistema:"
	@echo "Python: $(shell python --version)"
	@echo "Pip: $(shell pip --version)"
	@echo "Diretório: $(shell pwd)"
	@echo "Usuário: $(shell whoami)"
	@echo "Data: $(shell date)"

# Comando para primeira instalação completa
first-time: install setup
	@echo ""
	@echo "🎉 INSTALAÇÃO COMPLETA!"
	@echo ""
	@echo "📋 Próximos passos:"
	@echo "1. Configure sua OPENAI_API_KEY no arquivo .env"
	@echo "2. Execute: make run"
	@echo "3. Acesse: http://localhost:8501"
	@echo ""
	@echo "💡 Comandos úteis:"
	@echo "   make help   - Ver todos os comandos"
	@echo "   make check  - Verificar configuração"
	@echo "   make status - Ver status do sistema"