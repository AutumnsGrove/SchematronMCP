# Contributing to Schematron MCP Server

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request:

1. Check if the issue already exists in the issue tracker
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment (OS, Python version, MLX version)
   - Relevant logs or error messages

### Code Contributions

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the guidelines below
4. **Test your changes** thoroughly
5. **Commit with clear messages**: `git commit -m "Add: feature description"`
6. **Push to your fork**: `git push origin feature/your-feature-name`
7. **Create a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR-USERNAME/schematron-mcp.git
cd schematron-mcp

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Install pre-commit hooks (optional)
pre-commit install
```

## Code Style Guidelines

### Python Code Style

We follow PEP 8 with some modifications:

- **Line length**: 100 characters
- **Imports**: Grouped (stdlib, third-party, local)
- **Type hints**: Required for all functions
- **Docstrings**: Required for all public functions (Google style)

Run linters before committing:

```bash
# Format code
black .

# Check style
ruff check .

# Type checking
mypy .
```

### MCP Best Practices

Follow the MCP best practices guide:

1. **Tool Naming**: Use `schematron_` prefix for all tools
2. **Input Validation**: Use Pydantic models with clear descriptions
3. **Error Handling**: Return helpful, actionable error messages
4. **Documentation**: Comprehensive docstrings with examples
5. **Annotations**: Set correct readOnlyHint, destructiveHint, etc.

### Commit Message Format

```
Type: Brief description (max 72 chars)

Detailed explanation if needed.

- Bullet points for multiple changes
- Reference issues: Fixes #123
```

**Types**: Add, Fix, Update, Remove, Refactor, Docs, Test

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_extraction.py

# Run with coverage
pytest --cov=. --cov-report=html
```

### Writing Tests

- Place tests in `tests/` directory
- Name files `test_*.py`
- Use descriptive test names: `test_extract_product_from_simple_html`
- Include both success and failure cases
- Mock external dependencies (MLX model) when appropriate

## Areas for Contribution

### High Priority

- [ ] **More example schemas**: Add schemas for common use cases
- [ ] **Better error messages**: Improve error handling and user feedback
- [ ] **Performance optimizations**: Reduce latency, improve caching
- [ ] **Documentation**: More examples, tutorials, troubleshooting

### Medium Priority

- [ ] **Batch processing**: Process multiple pages efficiently
- [ ] **Schema validation**: Better validation of input schemas
- [ ] **Streaming responses**: Support for streaming large outputs
- [ ] **Alternative cleaners**: Support for other HTML cleaning libraries
- [ ] **Metrics & logging**: Better observability

### Low Priority

- [ ] **Multi-model support**: Support for Schematron-8B
- [ ] **Custom prompts**: Allow user-defined extraction prompts
- [ ] **Result caching**: Cache extraction results
- [ ] **Web UI**: Simple web interface for testing

## Project Structure

```
schematron-mcp/
├── server.py              # Main MCP server
├── mlx_inference.py       # MLX model wrapper
├── html_cleaner.py        # HTML preprocessing
├── example_schemas.py     # Pre-built schemas
├── test_extraction.py     # Manual test script
├── tests/                 # Test suite (create this)
├── docs/                  # Additional docs (create this)
├── README.md             # Main documentation
├── QUICKSTART.md         # Quick start guide
└── pyproject.toml        # Project config
```

## Code Review Process

Pull requests will be reviewed for:

1. **Functionality**: Does it work as intended?
2. **Code quality**: Follows style guide, well-structured
3. **Testing**: Adequate test coverage
4. **Documentation**: Clear docstrings and comments
5. **Performance**: No unnecessary performance regressions
6. **Compatibility**: Works with existing features

## Questions?

- Open an issue for questions
- Tag with `question` label
- We'll respond as soon as possible

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

- Be respectful and constructive
- Focus on the technical merits
- Help others learn and grow
- Celebrate diversity of thought

Thank you for contributing! 🎉
