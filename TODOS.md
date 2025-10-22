# SchematronMCP - Development TODOs

## High Priority

### Testing Infrastructure
- [ ] Create `tests/` directory with proper pytest structure
  - [ ] Unit tests for `server.py` (tool validation, error handling)
  - [ ] Unit tests for `html_cleaner.py` (cleaning levels, edge cases)
  - [ ] Unit tests for `example_schemas.py` (schema validation)
  - [ ] Mock tests for `mlx_inference.py` (avoid loading actual model)
  - [ ] Integration tests with sample HTML fixtures
- [ ] Update `test_extraction.py` or move to examples/

### CI/CD
- [ ] Create `.github/workflows/test.yml` for automated testing
  - [ ] Run pytest on push/PR
  - [ ] Run mypy type checking
  - [ ] Run ruff linting
  - [ ] Test on Python 3.10, 3.11, 3.12
- [ ] Add `.github/workflows/release.yml` for versioning
- [ ] Configure pre-commit hooks (`.pre-commit-config.yaml`)

### Version Tracking
- [ ] Create `CHANGELOG.md` following Keep a Changelog format
- [ ] Document v0.1.0 initial release

## Medium Priority

### Alternative Dependency Management
- [ ] Generate `requirements.txt` from pyproject.toml for broader compatibility
- [ ] Add `requirements-dev.txt` for development dependencies

### Documentation Organization
- [ ] Create `docs/` directory
  - [ ] Move technical docs to `docs/`
  - [ ] Add API reference documentation
  - [ ] Add architecture diagrams

### Code Organization
- [ ] Refactor into package structure with `__init__.py` files
  - [ ] `schematron_mcp/__init__.py`
  - [ ] `schematron_mcp/server.py`
  - [ ] `schematron_mcp/inference.py`
  - [ ] `schematron_mcp/cleaning.py`
  - [ ] `schematron_mcp/schemas.py`
- [ ] Update imports and entry points accordingly

## Low Priority

### Containerization
- [ ] Create `Dockerfile` for containerized deployment
- [ ] Create `docker-compose.yml` for local development
- [ ] Document Docker usage in README

### Developer Experience
- [ ] Add API documentation generation (Sphinx/MkDocs)
- [ ] Create `examples/` directory with usage samples
- [ ] Add performance benchmarks and profiling
- [ ] Create troubleshooting guide for common MLX issues

### Advanced Testing
- [ ] Add integration tests with real MLX model (requires Apple Silicon CI)
- [ ] Add property-based testing with Hypothesis
- [ ] Add performance regression tests
- [ ] Test error scenarios and edge cases

### Community
- [ ] Add issue templates (`.github/ISSUE_TEMPLATE/`)
- [ ] Add pull request template (`.github/PULL_REQUEST_TEMPLATE.md`)
- [ ] Add code of conduct (`CODE_OF_CONDUCT.md`)
- [ ] Add security policy (`SECURITY.md`)

## Future Enhancements

### Features
- [ ] Support for streaming responses for large HTML inputs
- [ ] Caching layer for repeated extractions
- [ ] Support for additional model backends (Ollama, etc.)
- [ ] Schema validation and auto-fixing tools
- [ ] Web interface for testing extractions

### Performance
- [ ] Benchmark extraction speed vs HTML size
- [ ] Optimize model loading time
- [ ] Add batch processing support
- [ ] Profile memory usage with large inputs

---

**Last Updated:** 2025-10-22
