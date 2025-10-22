# Quick Start Guide

Get Schematron MCP Server running in 5 minutes!

## Prerequisites

- macOS with Apple Silicon (M1/M2/M3/M4)
- Python 3.10 or later
- Claude Desktop (or Claude Code / Agent SDK)

## Installation Steps

### 1. Extract Files

```bash
cd ~/Downloads  # or wherever you downloaded
unzip schematron-mcp.zip
cd schematron-mcp
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -e .
```

This will install:
- `mcp` (Model Context Protocol SDK)
- `mlx-lm` (MLX inference framework)
- `lxml` (HTML cleaning)
- `pydantic` (Data validation)

### 4. Test the Installation

```bash
# Test that imports work
python -c "from mlx_inference import SchematronModel; print('✓ MLX imports OK')"
python -c "from html_cleaner import clean_html_content; print('✓ HTML cleaner OK')"
python -c "from server import mcp; print('✓ MCP server OK')"

# Run the test script (optional - downloads model ~2GB)
python test_extraction.py
```

### 5. Configure Claude Desktop

Get the full path to the server:

```bash
pwd  # Copy this path
```

Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "schematron": {
      "command": "python",
      "args": ["/PASTE/YOUR/PATH/HERE/schematron-mcp/server.py"],
      "env": {
        "SCHEMATRON_MODEL_PATH": "mlx-community/Schematron-3B-4bit"
      }
    }
  }
}
```

**Important**: Use the FULL ABSOLUTE PATH (not ~/schematron-mcp)

### 6. Restart Claude Desktop

Quit and reopen Claude Desktop completely.

### 7. Test in Claude

Try this prompt:

```
I need to extract product data from this HTML:

<div class="product">
  <h1>iPhone 15 Pro</h1>
  <span class="price">$999</span>
  <div class="rating">4.8 stars</div>
</div>

Can you extract: name, price, and rating?
```

Claude should automatically use the `schematron_extract_structured_data` tool!

## Troubleshooting

### "Command not found" error

Make sure you're using the absolute path to server.py:

```bash
# Find your path:
cd /path/to/schematron-mcp
pwd
# Use this FULL path in the config
```

### "mlx_lm not found" error

Activate your virtual environment:

```bash
cd /path/to/schematron-mcp
source venv/bin/activate
which python  # Should show the venv path
```

Then update your Claude config to use this Python:

```json
{
  "command": "/path/to/schematron-mcp/venv/bin/python",
  "args": ["/path/to/schematron-mcp/server.py"]
}
```

### Model download issues

The model (~2GB) downloads automatically on first use. If it fails:

```bash
# Manual download
python -c "import mlx_lm; mlx_lm.load('mlx-community/Schematron-3B-4bit')"
```

### Claude doesn't see the tool

1. Check Claude Desktop logs:
   - macOS: `~/Library/Logs/Claude/mcp*.log`

2. Verify the server runs:
   ```bash
   python server.py &
   # Should not error, will wait for input
   # Press Ctrl+C to exit
   ```

3. Check your config file is valid JSON:
   ```bash
   python -m json.tool ~/.config/claude/claude_desktop_config.json
   ```

## Next Steps

- Read `README.md` for full documentation
- Check `example_schemas.py` for pre-built schemas
- Run `test_extraction.py` to see examples
- Look at the MCP best practices in the code

## Usage Tips

1. **Let Claude fetch the HTML first**, then use the tool
2. **Use auto_clean=True** for best results
3. **Keep temperature at 0.0** for consistent output
4. **Define clear schemas** with good descriptions
5. **Start with example schemas** from `example_schemas.py`

## Example Interaction

**You**: "Go to apple.com/mac and extract all MacBook product names and prices"

**Claude** (automatically):
1. Uses web tools to fetch the HTML
2. Calls `schematron_extract_structured_data` with a product schema
3. Returns clean JSON: `{"products": [{"name": "MacBook Air", "price": 999}, ...]}`

That's it! You're ready to extract structured data from any HTML! 🎉
