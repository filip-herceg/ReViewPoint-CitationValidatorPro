# Citation Validator Examples

This directory contains example scripts demonstrating how to use the Citation Validator package.

## Available Examples

### 1. Basic Usage (`basic_usage.py`)
Demonstrates the simplest way to use the Citation Validator with OpenAI:

```python
python examples/basic_usage.py
```

**Requirements:** OpenAI API key configured in environment

### 2. Basic Usage with Mock LLM (`basic_usage_mock.py`)
Same as basic usage but uses a mock LLM provider (no API key required):

```python
python examples/basic_usage_mock.py
```

**Requirements:** None - uses mock LLM for testing

### 3. Advanced Usage (`advanced_usage.py`)
Shows advanced configuration including custom output directories:

```python
python examples/advanced_usage.py
```

**Requirements:** None - preconfigured to use mock LLM

## Quick Start

1. **For testing without API keys:**
   ```bash
   python examples/basic_usage_mock.py
   ```

2. **For production with OpenAI:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   python examples/basic_usage.py
   ```

3. **For advanced features:**
   ```bash
   python examples/advanced_usage.py
   ```

## Output

All examples create output files in different locations:
- `basic_usage.py` → `output/basic_example_output.html`
- `basic_usage_mock.py` → `output/basic_example_mock_output.html`
- `advanced_usage.py` → `custom_output/advanced_example_output.html`

## Configuration

Examples demonstrate different ways to configure the Citation Validator:

- **Default configuration**: Uses environment variables
- **Custom output directories**: Specify where files are saved
- **Mock LLM**: For testing without API costs
- **Validation summaries**: View configuration and status

See the individual example files for detailed code explanations.
