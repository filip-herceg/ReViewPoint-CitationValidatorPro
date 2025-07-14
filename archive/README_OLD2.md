# Citation Validator Pro

A comprehensive tool for validating academic citations in HTML documents using Large Language Models (LLMs).

## Features

- **Multi-mode validation**: Simplified mode with simulated sources or full mode with actual source verification
- **Multiple LLM providers**: Support for OpenAI GPT models and mock responses for testing
- **Flexible configuration**: Environment variables and CLI arguments
- **Professional output**: HTML reports with detailed citation analysis
- **Extensible architecture**: Modular design for easy customization

## Installation

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

## Quick Start

### 1. Prepare Input Files

Create an `input/` directory with:
- `content.html`: HTML document with div elements having numeric IDs corresponding to footnotes
- `footnotes.json`: JSON array of citation metadata

### 2. Configuration

Copy `.env.template` to `.env` and configure:

```env
# Mode settings
USE_SIMPLIFIED_MODE=true
USE_MOCK_LLM=false

# OpenAI settings (if not using mock)
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=500
OPENAI_TEMPERATURE=0.3

# File paths
INPUT_DIR=input
OUTPUT_FILE=content_reviewed.html
LOG_LEVEL=INFO
```

### 3. Run Validation

#### Command Line

```bash
# Basic usage
python main.py

# With custom options
python main.py --input-dir my_input --output-dir my_output --output report.html --mock-llm

# Validate configuration
python main.py --validate-config
```

#### Python API
```python
from citation_validator import CitationValidator

validator = CitationValidator(
    input_dir="input",
    output_file="content_reviewed.html"
)

validator.run_pipeline()
```

## Project Structure

```
src/citation_validator/
├── __init__.py              # Package initialization
├── cli.py                   # Command-line interface
├── config.py                # Configuration management
├── core.py                  # Main citation validator
├── llm/                     # LLM providers
│   ├── __init__.py
│   ├── base.py              # Abstract LLM interface
│   ├── factory.py           # LLM provider factory
│   ├── mock_provider.py     # Mock LLM for testing
│   └── openai_provider.py   # OpenAI integration
├── processors/              # Data processors
│   ├── __init__.py
│   ├── citation_processor.py  # Citation data handling
│   └── html_processor.py      # HTML processing
└── utils/                   # Utilities
    ├── __init__.py
    ├── prompts.py           # LLM prompt templates
    └── source_simulator.py  # Source content simulation
```

## Input Format

### content.html
```html
<!DOCTYPE html>
<html>
<head><title>Academic Paper</title></head>
<body>
    <div id="1">This text contains a citation to be validated.</div>
    <div id="2">Another paragraph with citation reference.</div>
</body>
</html>
```

### footnotes.json
```json
[
  {
    "number": 1,
    "title": "Paper Title",
    "authors": "Author Name",
    "year": "2024",
    "citation": "Author, N. (2024). Paper Title. Journal Name.",
    "doi": "10.1000/journal.123"
  }
]
```

## Output

The tool generates an HTML file in the output directory with citation evaluations inserted after each referenced div:

```html
<div id="1">Original text with citation.</div>
<div class="response">
✅ **Citation Evaluation**: This citation is appropriately placed...
**Strengths:**
- Relevant and current source
- Supports the claims made
...
</div>
```

## Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `USE_SIMPLIFIED_MODE` | `true` | Use simulated source content |
| `USE_MOCK_LLM` | `false` | Use mock responses for testing |
| `LLM_PROVIDER` | `openai` | LLM provider to use |
| `OPENAI_API_KEY` | - | OpenAI API key |
| `OPENAI_MODEL` | `gpt-3.5-turbo` | OpenAI model name |
| `OPENAI_MAX_TOKENS` | `500` | Maximum response tokens |
| `OPENAI_TEMPERATURE` | `0.3` | Model temperature |
| `INPUT_DIR` | `input` | Input directory path |
| `OUTPUT_DIR` | `output` | Output directory path |
| `OUTPUT_FILE` | `content_reviewed.html` | Output file name |
| `LOG_LEVEL` | `INFO` | Logging level |

## Examples

See the `examples/` directory for usage examples:

- `basic_usage.py`: Simple validation example
- `advanced_usage.py`: Custom configuration example

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/filip-herceg/ReViewPoint-CitationValidatorPro.git
cd ReViewPoint-CitationValidatorPro

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e .[dev]
```

### Running Tests

```bash
pytest tests/
```

### Code Quality

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type checking
mypy src/
```

## Architecture

The tool follows a modular architecture:

1. **Core**: Main validation pipeline orchestration
2. **Processors**: Handle HTML and citation data processing
3. **LLM Providers**: Abstract interface for different LLM services
4. **Configuration**: Centralized configuration management
5. **Utilities**: Helper functions and prompt templates

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### Version 1.0.0
- Initial release
- Modular architecture
- OpenAI and mock LLM support
- CLI interface
- Configuration management
- Comprehensive documentation
