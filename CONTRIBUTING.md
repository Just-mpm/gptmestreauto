# 🤝 Contributing to GPT Mestre Autônomo

Thank you for your interest in contributing to GPT Mestre Autônomo! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/GPT-Mestre-Autonomo.git
   cd GPT-Mestre-Autonomo
   ```
3. **Create a branch** for your feature:
   ```bash
   git checkout -b feature/amazing-feature
   ```

## 🛠️ Development Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Run tests**:
   ```bash
   python -m pytest
   ```

## 📝 Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Comment complex logic

## 🧪 Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Test coverage should not decrease

## 📋 Pull Request Process

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Update README.md** if needed
4. **Ensure all tests pass**
5. **Submit PR** with clear description

### PR Title Format
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

## 🐛 Reporting Issues

- Use GitHub Issues
- Include detailed description
- Provide steps to reproduce
- Include error messages/logs
- Specify environment details

## 💡 Feature Requests

- Open an issue with `enhancement` label
- Describe the feature clearly
- Explain use cases
- Discuss implementation ideas

## 🏗️ Project Structure

```
GPT-Mestre-Autonomo/
├── agents/           # Agent implementations
├── utils/            # Utility functions
├── memory/           # Memory/storage systems
├── tests/            # Test files
├── app_chainlit.py   # Main application
├── config.py         # Configuration
└── requirements.txt  # Dependencies
```

## 🤖 Adding New Agents

1. Create new file in `agents/` directory
2. Inherit from `BaseAgentV2`
3. Implement required methods
4. Add tests in `tests/`
5. Update documentation

## 📞 Contact

- GitHub Issues for bugs/features
- Pull Requests for contributions
- Discussions for questions

Thank you for contributing! 🎉