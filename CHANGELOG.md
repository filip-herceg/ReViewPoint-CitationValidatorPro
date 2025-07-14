# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-07-14

### 🎉 Major Refactor - Complete Architecture Overhaul

#### Added
- **Modular Architecture**: Transformed monolithic script into professional Python package
- **Output Directory Management**: Automatic creation and organization of output files
- **LLM Provider Abstraction**: Support for multiple LLM providers with factory pattern
- **Mock LLM Provider**: Testing and development without API costs
- **Comprehensive CLI**: Full command-line interface with help documentation
- **Environment Configuration**: Flexible configuration via environment variables
- **Professional Logging**: Structured logging throughout the application
- **Package Installation**: Proper setup.py for pip installation
- **Example Scripts**: Three comprehensive usage examples
- **Type Hints**: Full type annotation for better IDE support

#### Changed
- **Project Structure**: Moved from root-level scripts to `src/citation_validator/` package
- **Configuration System**: Environment-based configuration replacing hardcoded values
- **Error Handling**: Graceful error handling with meaningful messages
- **Output Organization**: Structured output directories instead of root-level files
- **API Design**: Clean, extensible API for programmatic usage

#### Enhanced
- **Documentation**: Comprehensive README with installation and usage guides
- **Code Quality**: PEP 8 compliance and professional code organization
- **Extensibility**: Easy to add new LLM providers and processors
- **Testing**: Mock provider for testing without API dependencies

### 🏗️ Technical Improvements

#### Core Components
- `core.py` - Main validation pipeline orchestration
- `config.py` - Centralized configuration management
- `cli.py` - Command-line interface
- `processors/` - Modular HTML and citation processing
- `llm/` - LLM provider abstraction layer
- `utils/` - Shared utilities and helpers

#### New Features
- **Custom Output Directories**: `--output-dir` CLI option
- **Flexible Output Naming**: `--output` CLI option for custom filenames
- **Validation Summary**: Configuration and status reporting
- **Automatic Directory Creation**: Output directories created as needed
- **Path Resolution**: Intelligent handling of relative vs absolute paths

### 📚 Documentation
- Complete README overhaul with professional formatting
- CONTRIBUTING.md for development guidelines
- Comprehensive examples with README
- Updated .env.template with detailed configuration options
- Inline documentation and docstrings throughout codebase

### 🔧 Configuration
- Environment variable-based configuration
- CLI argument overrides
- Sensible defaults for all options
- Template configuration file
- Validation of configuration options

## [1.0.0] - 2024-XX-XX

### Initial Release
- Basic citation validation functionality
- OpenAI integration
- HTML processing capabilities
- Simple command-line usage

---

## Version Numbering

This project follows [Semantic Versioning](https://semver.org/):
- **Major** version for incompatible API changes
- **Minor** version for backward-compatible functionality additions
- **Patch** version for backward-compatible bug fixes

## Upgrade Guides

### Upgrading from 1.x to 2.x

**Breaking Changes:**
- Project structure completely changed - update import paths
- Configuration now uses environment variables instead of CLI arguments
- Output files now organized in directories

**Migration Steps:**
1. Update configuration to use `.env` file
2. Update any scripts to use new package structure
3. Update output file paths to account for new directory structure

**New Features Available:**
- Mock LLM for testing
- Custom output directories
- Improved error handling
- Professional logging
