# Schematron MCP Server - Project Summary

## 🎉 What Was Built

A complete, production-ready **Model Context Protocol (MCP) server** for Schematron-3B that enables Claude to extract structured JSON from HTML. This follows all MCP best practices and is ready to use with Claude Desktop, Claude Code, or the Claude Agent SDK.

## 📦 What's Included

### Core Files (5 Python modules)
1. **server.py** - Main MCP server with FastMCP
   - 2 tools: extract_structured_data and clean_html
   - Progress reporting, context injection
   - Proper error handling with educational messages
   - Character limit enforcement (25K)

2. **mlx_inference.py** - MLX model wrapper
   - Async model loading and inference
   - Proper prompt construction (matches Schematron format)
   - JSON parsing and validation
   - Thread-pool execution for blocking operations

3. **html_cleaner.py** - HTML preprocessing
   - 3 cleaning levels (light, standard, aggressive)
   - Uses lxml (matches training data)
   - Fallback to original HTML on errors
   - Helper functions for text extraction

4. **example_schemas.py** - Pre-built schemas
   - 9 common extraction patterns
   - Product, Article, Job, Real Estate, Restaurant, Event, Contact, Publication, Table
   - Ready to use or customize

5. **test_extraction.py** - Testing script
   - Tests product and article extraction
   - Tests HTML cleaning
   - Demonstrates async usage

### Documentation (6 files)
1. **README.md** - Comprehensive documentation
   - Architecture diagram
   - Installation instructions
   - Tool documentation
   - Usage examples
   - Troubleshooting

2. **QUICKSTART.md** - 5-minute setup guide
   - Step-by-step installation
   - Configuration for Claude Desktop
   - Common troubleshooting
   - Usage tips

3. **INSTALL.txt** - Simple text instructions
   - Plain text for easy reading
   - Quick reference format
   - Essential info only

4. **CONTRIBUTING.md** - Contribution guidelines
   - Code style guide
   - Development setup
   - Pull request process
   - Areas for contribution

5. **LICENSE** - MIT License
   - Open source, permissive

6. **This document** - Project summary

### Configuration Files (3)
1. **pyproject.toml** - Python project config
   - All dependencies defined
   - Development dependencies included
   - Build system configured
   - Tool configurations (black, ruff, mypy)

2. **claude_desktop_config.example.json**
   - Example configuration for Claude Desktop
   - Copy-paste ready with instructions

3. **.gitignore** - Git ignore rules
   - Python, virtual env, IDE files
   - MLX models (optional)
   - Logs and caches

## 🏗️ Architecture Highlights

### MCP Best Practices Followed
✅ Server naming: `schematron_mcp` (Python convention)
✅ Tool naming: `schematron_extract_structured_data` (prefixed, snake_case)
✅ Input validation: Pydantic v2 models with constraints
✅ Response formats: JSON and Markdown support
✅ Character limits: 25K with graceful truncation
✅ Error messages: Actionable, educational, LLM-friendly
✅ Annotations: readOnlyHint, destructiveHint, etc. set correctly
✅ Context injection: Progress reporting, logging
✅ Type hints: Full coverage
✅ Async/await: All I/O operations
✅ Code reuse: Helper functions extracted
✅ Documentation: Comprehensive docstrings

### Design Decisions

1. **Two-Model Architecture**
   - Claude: Orchestrator (web search, planning)
   - Schematron: Specialist (HTML→JSON only)
   - Clean separation of concerns

2. **Automatic HTML Cleaning**
   - Optional (auto_clean parameter)
   - Uses lxml to match training data
   - 3 levels: light, standard, aggressive
   - Fallback to original on errors

3. **Progress Reporting**
   - Real-time feedback via MCP context
   - Shows: loading, cleaning, extracting, formatting
   - Helps user understand long operations

4. **Error Handling**
   - Never crashes - returns error in response
   - Clear, actionable error messages
   - Logs errors via context

5. **Flexible Response Formats**
   - JSON: Machine-readable, full data
   - Markdown: Human-readable, formatted
   - Client can choose based on use case

## 🎯 How It Works

```
User → Claude → Web Tools (fetch HTML) → Schematron MCP → MLX Model → JSON
                                          ↓
                                     Validation
                                          ↓
                                    Formatting
                                          ↓
                                   Return to Claude
```

## 🚀 Getting Started

1. **Extract the zip** file when you get home
2. **Install dependencies**: `pip install -e .`
3. **Test locally**: `python test_extraction.py`
4. **Configure Claude**: Edit `claude_desktop_config.json`
5. **Restart Claude Desktop**
6. **Try it**: "Extract product data from this HTML: ..."

## 💡 Usage Example

**User to Claude:**
> "Go to this e-commerce site and extract all products with names, prices, and ratings"

**Claude internally:**
1. Uses web tools to fetch HTML
2. Calls `schematron_extract_structured_data` with:
   ```json
   {
     "html": "<fetched HTML>",
     "schema": {PRODUCT_SCHEMA},
     "auto_clean": true,
     "temperature": 0.0
   }
   ```
3. Receives clean JSON array
4. Presents to user in a nice format

## 🛠️ Technical Stack

- **Python 3.10+** - Modern Python features
- **FastMCP** - MCP server framework
- **MLX-LM** - Apple Silicon inference
- **Pydantic v2** - Data validation
- **lxml** - HTML processing
- **Schematron-3B** - 4-bit quantized model

## 📊 Statistics

- **Lines of code**: ~1,800 (well-documented)
- **Tools provided**: 2 (extract, clean)
- **Example schemas**: 9
- **Documentation pages**: 6
- **Test coverage**: Manual test script included
- **File size**: 26KB zipped (without model)
- **Model size**: ~2GB (downloads on first use)

## 🔮 Future Enhancements

Potential areas for improvement:

1. **Batch processing** - Process multiple pages efficiently
2. **Streaming responses** - For very large outputs
3. **Schema library** - Curated collection of schemas
4. **Web UI** - Simple interface for testing
5. **Caching** - Cache extraction results
6. **Multi-model** - Support Schematron-8B
7. **Metrics** - Performance monitoring
8. **Tests** - Full pytest suite

## ✅ Quality Checklist

All MCP best practices implemented:

- [x] Strategic design (workflow-focused tools)
- [x] Tool naming conventions followed
- [x] Response formats (JSON + Markdown)
- [x] Input validation with Pydantic
- [x] Error handling (graceful, educational)
- [x] Documentation (comprehensive)
- [x] Type hints throughout
- [x] Async/await for I/O
- [x] Code reuse (helper functions)
- [x] Character limits enforced
- [x] Progress reporting
- [x] Context injection
- [x] Tool annotations correct

## 🎓 Learning Resources

The code itself is educational - it demonstrates:

- How to build MCP servers with FastMCP
- Async Python best practices
- MLX integration patterns
- HTML processing techniques
- Schema-first data extraction
- Error handling strategies
- Documentation standards

## 🙏 Acknowledgments

Built following:
- Anthropic's MCP best practices
- Inference.net's Schematron documentation
- Apple's MLX examples
- Python community standards

## 📝 License

MIT License - Use freely, modify as needed, no warranty.

---

**Ready to use! Extract the zip when you get home and follow QUICKSTART.md** 🚀
