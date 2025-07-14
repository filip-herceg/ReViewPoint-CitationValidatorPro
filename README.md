# Citation Validation Pipeline

A Python pipeline that processes HTML content with footnotes and evaluates citations using Large Language Models (LLMs). This tool helps academic reviewers assess whether citations are correctly used, relevant, and truthful.

## ✨ Features

- 📄 **HTML Processing**: Extracts content from `<div>` elements with footnote IDs
- 📊 **JSON Citation Metadata**: Loads structured citation information
- 🤖 **Real AI Integration**: Uses actual LLM responses (OpenAI API) or enhanced mock responses
- 📝 **HTML Output**: Generates reviewed content with embedded LLM feedback
- ⚙️ **Environment Configuration**: Secure .env-based configuration
- 🎯 **Contextual Analysis**: AI responses tailored to content type (intro, background, technical)
- 🎨 **Beautiful Styling**: CSS-styled response divs for clear visual separation
- 🔧 **Flexible Modes**: Simplified mode with source simulation, full mode for production

## 🚀 Quick Start

### 1. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Copy the environment template and configure:

```bash
cp .env.template .env
# Edit .env with your settings
```

**Key configuration options:**
```bash
USE_SIMPLIFIED_MODE=true          # Use simulated source content
USE_MOCK_LLM=true                # Use enhanced mock responses or real OpenAI
OPENAI_API_KEY=your_key_here     # Your OpenAI API key
OPENAI_MODEL=gpt-3.5-turbo       # Model to use
```

### 3. Prepare Input Files

Place your files in the `input/` directory:
- **`content.html`**: HTML file with `<div id="X">...</div>` elements
- **`footnotes.json`**: JSON file with citation metadata

### 4. Run the Pipeline

```bash
python citation_validator.py
```

### 5. View Results

Open `content_reviewed.html` in your browser to see the AI evaluations.

## 🔧 Configuration Options

### Environment Variables (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_SIMPLIFIED_MODE` | Use simulated source content | `true` |
| `USE_MOCK_LLM` | Use enhanced mock responses | `true` |
| `LLM_PROVIDER` | LLM provider (openai) | `openai` |
| `OPENAI_API_KEY` | Your OpenAI API key | *(required for real AI)* |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-3.5-turbo` |
| `OPENAI_MAX_TOKENS` | Maximum response tokens | `500` |
| `OPENAI_TEMPERATURE` | Response creativity (0-1) | `0.3` |
| `OUTPUT_FILE` | Output filename | `content_reviewed.html` |

### Operating Modes

#### 🎭 Enhanced Mock Mode (Current)
- ✅ **Real AI-style responses** based on content analysis
- ✅ **Contextual evaluation** tailored to content type
- ✅ **No API costs** or rate limits
- ✅ **Simulated source content** for demonstration
- ✅ **Fast execution** for development and testing

#### 🚀 Real AI Mode
- 🤖 **Actual OpenAI API** responses
- 📊 **Professional citation analysis**
- 💰 **Requires API key** and usage costs
- 🔄 **Rate limiting** considerations

#### 🔍 Full Mode (Future)
- 🌐 **Web crawler integration** to fetch actual paper content
- 📖 **Real source validation** against original papers
- 🔍 **Deep citation analysis** with source comparison

## 📊 AI Response Examples

### Introduction Sections
```
✅ Citation Evaluation: This citation is appropriately placed in the introduction section. 
The source provides comprehensive coverage of AI assistants and directly supports the opening statements.

Strengths:
- Relevant and current source (2024)
- Supports broad claims about AI development
- Appropriate for establishing context
```

### Technical Content
```
⚠️ Citation Evaluation: This citation needs strengthening for privacy and technical claims. 
The current source may not adequately support specific assertions about enterprise requirements.

Improvements needed:
- Add citations focused on enterprise data protection
- Include sources on privacy risks in AI tools
```

## 🔒 Security & Privacy

- **.env file**: Stores sensitive configuration (excluded from git)
- **API key protection**: Environment-based configuration
- **No data leakage**: Mock mode for testing without API calls
- **Source simulation**: Realistic content generation without external requests

## 📁 Project Structure

```
ReViewPoint-CitationValidatorPro/
├── citation_validator.py    # Main pipeline implementation
├── demo.py                 # Demonstration script
├── requirements.txt        # Python dependencies
├── .env.template          # Environment template
├── .env                   # Your configuration (git-ignored)
├── .gitignore            # Git exclusions
├── README.md             # This documentation
├── input/                # Input files directory
│   ├── content.html      # HTML content with footnotes
│   └── footnotes.json    # Citation metadata
└── data_transformation/  # Example/test data
```

## 🛠 Dependencies

- **beautifulsoup4**: HTML parsing and manipulation
- **openai**: OpenAI API integration
- **python-dotenv**: Environment variable management
- **pathlib**: File path handling
- **json**: JSON file processing
- **logging**: Structured logging

## 📖 Usage Examples

### Basic Usage
```python
from citation_validator import CitationValidator

# Create validator with default settings
validator = CitationValidator()
validator.run_pipeline()
```

### Custom Configuration
```python
import os
os.environ['USE_MOCK_LLM'] = 'false'
os.environ['OPENAI_MODEL'] = 'gpt-4'

validator = CitationValidator(output_file="custom_output.html")
validator.run_pipeline()
```

## 🔮 Future Enhancements

### Web Crawler Integration
- 🔄 Fetch actual paper content from URLs/DOIs
- 🔄 Extract relevant sections for comparison
- 🔄 Handle different paper formats (PDF, HTML, etc.)

### Advanced AI Features
- 🔄 Multiple LLM provider support (Anthropic, local models)
- 🔄 Custom prompt templates
- 🔄 Batch processing for large documents
- 🔄 Citation quality scoring

### Enhanced Analysis
- 🔄 Plagiarism detection
- 🔄 Citation style validation
- 🔄 Cross-reference verification
- 🔄 Academic integrity checks

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💡 Support

For questions, issues, or feature requests, please open an issue on GitHub.

---

**Note**: This pipeline currently operates in simplified mode with enhanced mock AI responses. The responses are realistic and contextually appropriate, demonstrating the pipeline's capabilities without requiring API costs. Set up your OpenAI API key to enable real AI evaluation.
