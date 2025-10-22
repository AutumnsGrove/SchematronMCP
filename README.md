# Schematron MCP Server

A **Model Context Protocol (MCP) server** that provides HTML-to-JSON extraction using the [Schematron-3B](https://huggingface.co/inference-net/Schematron-3B) model running locally via MLX.

This server enables AI agents (like Claude) to convert messy HTML into clean, structured JSON that conforms to custom schemas - perfect for web scraping, data extraction, and building intelligent web agents.

## 🎯 Features

- **Schema-First Extraction**: Define your data structure with JSON Schema, get back perfectly conforming JSON
- **Local Inference**: Runs Schematron-3B locally using MLX for fast, private processing
- **Automatic HTML Cleaning**: Built-in preprocessing matches Schematron's training data
- **Long Context Support**: Handles HTML documents up to 128K tokens
- **MCP Native**: Integrates seamlessly with Claude Desktop, Claude Code, and Claude Agent SDK
- **Progress Reporting**: Real-time feedback on extraction progress

## 🏗️ Architecture

```
┌────────────────────────────────────────────────────────────┐
│  Claude (Desktop/Code/Agent-SDK)                           │
│  "Extract product data from this e-commerce page"         │
└────────────────┬───────────────────────────────────────────┘
                 │
                 │ (via MCP protocol)
                 ▼
┌────────────────────────────────────────────────────────────┐
│  Schematron MCP Server                                     │
│  - Receives HTML and JSON Schema                           │
│  - Cleans HTML (optional)                                  │
│  - Runs MLX inference                                      │
│  - Returns validated JSON                                  │
└────────────────┬───────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────────┐
│  MLX-LM (Local Inference)                                  │
│  - Loads Schematron-3B quantized model                     │
│  - Fast, private inference on Mac Silicon                  │
└────────────────────────────────────────────────────────────┘
```

## 📋 Requirements

- **macOS** with Apple Silicon (M1/M2/M3/M4)
- **Python 3.10+**
- **MLX framework** (for Apple Silicon inference)
- **MCP SDK** (for protocol support)

## 🚀 Installation

### 1. Clone or Download

```bash
# If you have this as a git repo
git clone https://github.com/yourusername/schematron-mcp.git
cd schematron-mcp

# Or just extract the ZIP file
cd schematron-mcp
```

### 2. Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -e .

# Or install manually
pip install mcp>=0.9.0 mlx-lm>=0.19.0 lxml>=4.9.0 pydantic>=2.0.0
```

### 3. Download the Model

The model will be automatically downloaded on first use, or you can download it manually:

```bash
# The server expects this path by default:
# mlx-community/Schematron-3B-4bit

# If you want to use a different model path, set the environment variable:
export SCHEMATRON_MODEL_PATH="/path/to/your/model"
```

## ⚙️ Configuration

### For Claude Desktop

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "schematron": {
      "command": "python",
      "args": ["/absolute/path/to/schematron-mcp/server.py"],
      "env": {
        "SCHEMATRON_MODEL_PATH": "mlx-community/Schematron-3B-4bit"
      }
    }
  }
}
```

### For Claude Code / Agent SDK

When using programmatically, the server runs via stdio transport:

```python
import subprocess
import json

# Start the MCP server
process = subprocess.Popen(
    ["python", "/path/to/schematron-mcp/server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Communicate via MCP protocol
# (See MCP SDK documentation for details)
```

## 🛠️ Tools Provided

### 1. `schematron_extract_structured_data`

Extract structured JSON from HTML using a custom schema.

**Parameters:**
- `html` (str, required): Raw HTML content (NOT a URL)
- `schema` (dict, required): JSON Schema defining output structure
- `auto_clean` (bool, default: true): Auto-clean HTML before extraction
- `temperature` (float, default: 0.0): Generation temperature (keep at 0 for deterministic)
- `max_tokens` (int, default: 8000): Maximum tokens to generate
- `response_format` (str, default: "json"): Output format ("json" or "markdown")

**Example Usage:**

```json
{
  "html": "<div><h1>MacBook Pro M3</h1><p>Price: $2,499.99</p><ul><li>RAM: 16GB</li></ul></div>",
  "schema": {
    "type": "object",
    "properties": {
      "name": {"type": "string"},
      "price": {"type": "number"},
      "specs": {
        "type": "object",
        "properties": {
          "ram": {"type": "string"}
        }
      }
    }
  },
  "auto_clean": true,
  "temperature": 0.0
}
```

**Returns:**

```json
{
  "success": true,
  "extracted_data": {
    "name": "MacBook Pro M3",
    "price": 2499.99,
    "specs": {
      "ram": "16GB"
    }
  },
  "metadata": {
    "html_length": 123,
    "was_cleaned": true
  }
}
```

### 2. `schematron_clean_html`

Clean HTML by removing scripts, styles, and JavaScript.

**Parameters:**
- `html` (str, required): Raw HTML to clean
- `cleaning_level` (str, default: "standard"): "light", "standard", or "aggressive"
- `response_format` (str, default: "markdown"): Output format

**Returns:** Cleaned HTML with statistics

## 📝 Example Schemas

See `example_schemas.py` for common patterns:

```python
# Product extraction
PRODUCT_SCHEMA = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "description": "Product name"},
        "price": {"type": "number", "description": "Price in USD"},
        "rating": {"type": "number", "description": "Star rating 1-5"},
        "in_stock": {"type": "boolean"}
    }
}

# Article extraction
ARTICLE_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "author": {"type": "string"},
        "published_date": {"type": "string"},
        "content": {"type": "string"},
        "tags": {"type": "array", "items": {"type": "string"}}
    }
}
```

## 🎮 Usage Example with Claude

**User**: "Extract product information from this Amazon page"
[Uploads or fetches HTML]

**Claude** (internally):
1. Uses web tools to fetch the HTML
2. Calls `schematron_extract_structured_data` with:
   - The fetched HTML
   - A product schema (name, price, rating, etc.)
   - `auto_clean: true`
3. Receives structured JSON
4. Presents the data to the user

## 🧪 Testing

### Test the Server

```bash
# Test that the server starts
python server.py --help

# Test imports
python -c "from mlx_inference import SchematronModel; from html_cleaner import clean_html_content; print('OK')"
```

### Manual Testing

```bash
# Start the server in one terminal
python server.py

# In another terminal, use the MCP Inspector or client to test
# (The server will wait for MCP protocol messages on stdin)
```

## 📂 Project Structure

```
schematron-mcp/
├── server.py              # Main MCP server
├── mlx_inference.py       # MLX model loading and inference
├── html_cleaner.py        # HTML preprocessing
├── example_schemas.py     # Common schema examples
├── pyproject.toml         # Dependencies and config
├── README.md              # This file
└── LICENSE                # MIT License
```

## 🔧 Troubleshooting

### Model Loading Issues

**Problem**: "Model not found" error
**Solution**: Check that MLX can access the model:

```bash
# Verify model path
export SCHEMATRON_MODEL_PATH="mlx-community/Schematron-3B-4bit"

# Or download manually with MLX
python -c "import mlx_lm; mlx_lm.load('mlx-community/Schematron-3B-4bit')"
```

### HTML Cleaning Failures

**Problem**: HTML cleaning returns original HTML
**Solution**: This is by design - if lxml fails, we return the original HTML to avoid data loss. Check the logs for details.

### Memory Issues

**Problem**: Out of memory during inference
**Solution**: 
- Reduce `max_tokens` parameter
- Clean HTML more aggressively
- Chunk large documents

### Performance Tips

1. **Pre-clean HTML**: Use `auto_clean=True` for best results
2. **Use temperature=0.0**: For deterministic, reproducible outputs
3. **Keep schemas focused**: Don't extract more fields than needed
4. **Reuse the server**: Model loads once and stays in memory

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Add more example schemas
- [ ] Support for streaming responses
- [ ] Batch processing multiple pages
- [ ] Schema validation improvements
- [ ] Better error messages
- [ ] Performance optimizations

## 📄 License

MIT License - See LICENSE file for details.

## 🙏 Acknowledgments

- [Schematron](https://huggingface.co/inference-net/Schematron-3B) by Inference.net
- [MLX](https://github.com/ml-explore/mlx) by Apple
- [Model Context Protocol](https://modelcontextprotocol.io/) by Anthropic

## 📚 References

- [Schematron Blog Post](https://inference.net/blog/Schematron)
- [Schematron Documentation](https://docs.inference.net/use-cases/json-extraction)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [MLX-LM Documentation](https://github.com/ml-explore/mlx-examples/tree/main/llms)

---

**Built for local-first AI agents** 🤖✨
