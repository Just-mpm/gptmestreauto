# GPT Mestre Autônomo - Project Structure

## Overview
Clean and organized structure for the GPT Mestre Autônomo project using Chainlit.

## Directory Structure

```
GPT Mestre Autônomo/
│
├── .chainlit/              # Chainlit configuration and translations
│   ├── config.toml
│   └── translations/       # Multi-language support files
│
├── .claude/                # Claude AI configuration
│   └── settings.local.json
│
├── agents/                 # All AI agents (v2 versions)
│   ├── __init__.py
│   ├── automaster_v2.py   # Economic autonomy agent
│   ├── base_agent_v2.py   # Base agent class
│   ├── carlos.py          # Central orchestrator agent
│   ├── deep_agent_v2.py   # Deep analysis agent
│   ├── oraculo_v2.py      # Oracle prediction agent
│   ├── psymind_v2.py      # Psychological analysis agent
│   ├── reflexor_v2.py     # Reflection and feedback agent
│   ├── scout_ai.py        # Scout exploration agent
│   ├── supervisor_ai_v2.py # Supervision and quality agent
│   └── task_breaker_v2.py # Task decomposition agent
│
├── memory/                 # Memory and persistence
│   ├── __init__.py
│   ├── vector_store.py    # Vector database implementation
│   ├── agents/            # Agent-specific memory storage
│   └── chroma_db/         # ChromaDB storage
│
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── logger.py          # Logging configuration
│   └── web_search.py      # Web search capabilities
│
├── logs/                   # Application logs (auto-generated)
│
├── app.py                 # Main Chainlit application
├── chainlit.md            # Chainlit welcome message
├── config.py              # System configuration
├── requirements.txt       # Python dependencies
│
├── .env                   # Environment variables
├── .env.example          # Example environment file
├── .gitignore            # Git ignore rules
│
├── README.md             # Project documentation
├── CHAINLIT_INSTRUCTIONS.md    # Chainlit usage guide
├── PLANO_MELHORIAS_COMPLETO.txt  # Complete improvement plan
└── ROADMAP_EVOLUCAO_v4.0.md      # Evolution roadmap v4.0
```

## Key Changes Made

### Removed Files:
- Old Streamlit files (app.py, app_backup.py, app_complex_backup.py)
- Python cache directories (__pycache__)
- Empty .files directory
- Log files (will be regenerated)
- Old memory/session files (.pkl files)
- ChromaDB database file (will be regenerated)
- Duplicate planning document (PLANO_TRANSFORMACAO_PRODUTO.txt)

### Kept Files:
- All planning and documentation files
- Chainlit implementation files
- All v2 agent implementations
- Core system modules (memory, utils)
- Configuration files
- Environment files

## Running the Application

To run the application with Chainlit:
```bash
chainlit run app.py -w
```

The system is now clean and organized, ready for continued development.