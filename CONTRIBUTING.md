# Contributing to Citation Validator Pro

Thank you for your interest in contributing to Citation Validator Pro! This document provides guidelines and instructions for contributing to the project.

## 🚀 Quick Start for Contributors

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/ReViewPoint-CitationValidatorPro.git
   cd ReViewPoint-CitationValidatorPro
   ```
3. **Set up development environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -e .
   pip install -r requirements.txt
   ```
4. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use meaningful variable and function names
- Add docstrings to all classes and functions
- Keep functions focused and small (ideally <50 lines)
- Use type hints where appropriate

### Project Structure

```
src/citation_validator/
├── core.py                    # Main business logic
├── config.py                  # Configuration management
├── cli.py                     # Command-line interface
├── processors/               # Data processing modules
├── llm/                      # LLM provider abstractions
└── utils/                    # Shared utilities
```

### Code Organization Principles

1. **Separation of Concerns**: Each module has a single responsibility
2. **Dependency Injection**: Use configuration objects rather than global state
3. **Interface Segregation**: Small, focused interfaces (like `LLMProvider`)
4. **Open/Closed Principle**: Extend functionality through new providers/processors

## 🧪 Testing

### Running Tests

```bash
# Test with mock LLM (no API costs)
python main.py --mock-llm

# Test examples
python examples/basic_usage_mock.py
python examples/advanced_usage.py

# Manual testing with custom data
python main.py --output-dir test_output --log-level DEBUG
```

### Testing Guidelines

- Always test with mock LLM first to avoid API costs
- Test both success and error scenarios
- Verify output files are generated correctly
- Check logging output for errors or warnings

## 🔧 Adding New Features

### Adding New LLM Providers

1. Create a new provider class in `src/citation_validator/llm/`:
   ```python
   from .base import LLMProvider
   
   class YourProvider(LLMProvider):
       def generate_response(self, prompt: str) -> str:
           # Implementation here
           pass
   ```

2. Update the factory in `llm/factory.py`:
   ```python
   if config.llm_provider.lower() == 'your_provider':
       return YourProvider(...)
   ```

3. Add configuration options to `config.py`
4. Update `.env.template` with new environment variables

### Adding New Processors

1. Create processor in `src/citation_validator/processors/`
2. Follow the existing pattern with clear input/output interfaces
3. Add logging for important operations
4. Handle errors gracefully with meaningful error messages

### Adding New CLI Options

1. Update `cli.py` with new argument parser options
2. Ensure options are passed to the core validator
3. Add help text and examples
4. Update documentation

## 📝 Documentation

### Required Documentation

- **Docstrings**: All public functions and classes
- **Type Hints**: Function parameters and return types
- **Comments**: Complex logic or business rules
- **README Updates**: New features or configuration options

### Documentation Style

```python
def validate_citation(content: str, metadata: Dict[str, Any]) -> ValidationResult:
    """
    Validate a single citation against its metadata.
    
    Args:
        content: The citation text to validate
        metadata: Citation metadata including source information
        
    Returns:
        ValidationResult containing success status and analysis
        
    Raises:
        ValidationError: If citation format is invalid
    """
```

## 🐛 Bug Reports

### Before Reporting

1. Check existing issues on GitHub
2. Test with mock LLM to isolate API issues
3. Enable debug logging: `--log-level DEBUG`
4. Try with minimal test data

### Bug Report Template

```markdown
**Bug Description**
Clear description of the issue

**Steps to Reproduce**
1. Step 1
2. Step 2
3. ...

**Expected Behavior**
What should have happened

**Actual Behavior**
What actually happened

**Environment**
- OS: [Windows/Mac/Linux]
- Python version: [3.8, 3.9, etc.]
- LLM Provider: [OpenAI/Mock]

**Logs**
Include relevant log output with DEBUG level
```

## ✨ Feature Requests

### Feature Request Template

```markdown
**Feature Description**
Clear description of the proposed feature

**Use Case**
Why is this feature needed?

**Proposed Implementation**
Ideas for how it could be implemented

**Alternatives Considered**
Other approaches you've considered
```

## 🔄 Pull Request Process

### Before Submitting

1. **Test thoroughly** with both mock and real LLM providers
2. **Update documentation** for any new features
3. **Add examples** if appropriate
4. **Check code style** and add docstrings
5. **Verify no breaking changes** to existing functionality

### Pull Request Template

```markdown
**Description**
Summary of changes made

**Type of Change**
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

**Testing**
- [ ] Tested with mock LLM
- [ ] Tested with real LLM
- [ ] Added/updated examples
- [ ] Verified backward compatibility

**Checklist**
- [ ] Code follows project style guidelines
- [ ] Added docstrings to new functions
- [ ] Updated relevant documentation
- [ ] No breaking changes (or documented)
```

## 🏗️ Architecture Guidelines

### Core Principles

1. **Modularity**: Keep components loosely coupled
2. **Testability**: Design for easy testing with mocks
3. **Extensibility**: Make it easy to add new providers/processors
4. **Configuration-Driven**: Avoid hardcoded values

### Design Patterns Used

- **Factory Pattern**: LLM provider creation
- **Strategy Pattern**: Different validation modes
- **Dependency Injection**: Configuration and provider injection
- **Template Method**: Validation pipeline structure

## 📞 Getting Help

- **Discord/Slack**: [Link to community chat]
- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bugs and feature requests
- **Email**: [maintainer email for sensitive issues]

## 📜 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/). By participating, you are expected to uphold this code.

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for helping make Citation Validator Pro better! 🚀
