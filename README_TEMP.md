# Citation Validator Pro

A comprehensive tool for validating academic citations in HTML documents using Large Language Models (LLMs). This professional-grade solution helps researchers, academic publishers, and content creators ensure citation accuracy and consistency.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## 🚀 Features

- **🎯 Smart Citation Validation**: AI-powered validation using OpenAI GPT models
- **📊 Multiple Validation Modes**: Simplified mode with simulated sources or comprehensive source verification
- **🔧 Flexible Configuration**: Environment-based configuration with CLI overrides
- **📁 Organized Output**: Automatic output directory management with customizable paths
- **🧪 Testing Support**: Mock LLM provider for development and testing
- **📝 Professional Reports**: Detailed HTML reports with citation analysis
- **🏗️ Modular Architecture**: Extensible design for custom implementations

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [Examples](#examples)
- [Project Structure](#project-structure)
- [Development](#development)
- [License](#license)

## 🛠️ Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (optional, for production use)

### From Source

```bash
git clone https://github.com/filip-herceg/ReViewPoint-CitationValidatorPro.git
cd ReViewPoint-CitationValidatorPro
pip install -e .
```

### Dependencies

```bash
pip install -r requirements.txt
```

## 🚀 Quick Start

### 1. Basic Setup

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your OpenAI API key (optional)
# OPENAI_API_KEY=your-api-key-here
```

### 2. Prepare Your Data

Place your files in the `input/` directory:
- `content.html` - HTML document with citations
- `footnotes.json` - Citation metadata

### 3. Run Validation

```bash
# Using mock LLM (no API key required)
python main.py --mock-llm

# Using OpenAI (requires API key)
python main.py

# Custom output directory
python main.py --output-dir my_results --output my_report.html
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# LLM Configuration
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=1000
OPENAI_TEMPERATURE=0.7

# Processing Configuration
USE_MOCK_LLM=false
LOG_LEVEL=INFO
MODE=Simplified

# Input/Output Configuration
INPUT_DIR=input
OUTPUT_DIR=output
OUTPUT_FILE=content_reviewed.html
```

### CLI Options

```bash
python main.py --help
```

**Available options:**
- `--mock-llm` - Use mock LLM instead of OpenAI
- `--output-dir DIR` - Custom output directory
- `--output FILE` - Custom output filename
- `--log-level LEVEL` - Logging level (DEBUG, INFO, WARNING, ERROR)

## 📖 Usage

### Command Line Interface

```bash
# Basic validation with default settings
python main.py

# Advanced usage with custom settings
python main.py \
  --output-dir results \
  --output validation_report.html \
  --log-level DEBUG

# Testing mode (no API costs)
python main.py --mock-llm
```

### Python API

```python
from citation_validator import CitationValidator

# Create validator instance
validator = CitationValidator(
    input_dir="input",
    output_file="my_report.html"
)

# Get configuration summary
summary = validator.get_validation_summary()
print(f"Output will be saved to: {summary['output_file']}")

# Run validation pipeline
try:
    validator.run_pipeline()
    print("✅ Validation completed successfully!")
except Exception as e:
    print(f"❌ Validation failed: {e}")
```

## 📚 Examples

The `examples/` directory contains three demonstration scripts:

### Basic Usage
```bash
python examples/basic_usage.py
```
Demonstrates simple validation with OpenAI API.

### Mock LLM Usage
```bash
python examples/basic_usage_mock.py
```
Shows validation using mock LLM (no API key required).

### Advanced Configuration
```bash
python examples/advanced_usage.py
```
Demonstrates custom output directories and advanced settings.

See [examples/README.md](examples/README.md) for detailed documentation.

## 📁 Project Structure

```
Citation-Validator-Pro/
├── src/citation_validator/          # Main package
│   ├── __init__.py                  # Package initialization
│   ├── core.py                      # Main validation pipeline
│   ├── config.py                    # Configuration management
│   ├── cli.py                       # Command-line interface
│   ├── processors/                  # Processing modules
│   │   ├── html_processor.py        # HTML document processing
│   │   └── citation_processor.py    # Citation data processing
│   ├── llm/                         # LLM provider abstraction
│   │   ├── base.py                  # Base provider interface
│   │   ├── openai_provider.py       # OpenAI implementation
│   │   ├── mock_provider.py         # Mock implementation
│   │   └── factory.py               # Provider factory
│   └── utils/                       # Utility modules
│       ├── prompts.py               # LLM prompts
│       └── source_simulator.py      # Source simulation
├── examples/                        # Usage examples
├── input/                           # Input data directory
├── output/                          # Generated output files
├── tests/                           # Test suite
├── archive/                         # Archived old files
├── main.py                          # CLI entry point
├── setup.py                         # Package setup
├── requirements.txt                 # Dependencies
├── .env.template                    # Environment template
└── README.md                        # This file
```

## 🔧 Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/filip-herceg/ReViewPoint-CitationValidatorPro.git
cd ReViewPoint-CitationValidatorPro

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .
pip install -r requirements.txt
```

### Running Tests

```bash
# Run with mock LLM (recommended for development)
python main.py --mock-llm

# Test examples
python examples/basic_usage_mock.py
python examples/advanced_usage.py
```

### Code Organization

The codebase follows clean architecture principles:

- **Core Layer**: Business logic in `core.py`
- **Application Layer**: CLI and configuration in `cli.py` and `config.py`
- **Infrastructure Layer**: LLM providers and processors
- **Utilities Layer**: Shared utilities and helpers

### Adding New LLM Providers

1. Create a new provider class inheriting from `LLMProvider`
2. Implement the `generate_response()` method
3. Add provider creation logic to `LLMFactory`
4. Update configuration options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [examples](examples/) for usage patterns
2. Review the configuration options in `.env.template`
3. Enable debug logging with `--log-level DEBUG`
4. Open an issue on GitHub

## 🏷️ Version History

- **v2.0.0** - Complete refactor with modular architecture and output directory support
- **v1.0.0** - Initial release with basic citation validation

---

**Citation Validator Pro** - Making academic citation validation simple and reliable.
