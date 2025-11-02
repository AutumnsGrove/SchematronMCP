# Project Instructions - Claude Code

> **Note**: This is the main orchestrator file. For detailed development guides, see the `dev` branch where `ClaudeUsage/README.md` contains comprehensive documentation.

---

## Project Purpose
SchematronMCP is a Model Context Protocol (MCP) server that provides HTML-to-JSON extraction using the Schematron-3B model running locally via MLX. It enables AI agents to convert messy HTML into clean, structured JSON conforming to custom schemas.

## Tech Stack
- **Language**: Python 3.10+
- **Framework**: Model Context Protocol (MCP) by Anthropic
- **Key Libraries**:
  - `mlx-lm` (Apple Silicon inference)
  - `lxml` (HTML parsing/cleaning)
  - `pydantic` (schema validation)
  - `gradio` (web UI for testing)
- **Package Manager**: uv (Python package manager)

## Architecture Notes
- **MCP Server Architecture**: Stdio-based server exposing tools via MCP protocol
- **Local Inference**: Runs Schematron-3B quantized model via MLX on Apple Silicon
- **Dual Interface**: MCP tools for Claude integration + Gradio web UI for manual testing
- **No API Keys Required**: Fully local processing, no external API calls
- **Key Files**:
  - `schematron_mcp/server.py` - Main MCP server implementation
  - `schematron_mcp/inference/lm_studio.py` - LM Studio inference backend
  - `schematron_mcp/inference/mlx.py` - MLX inference backend
  - `examples/gradio_app.py` - Web UI for testing
  - `schematron_mcp/cleaning/html_cleaner.py` - HTML preprocessing

## Existing Documentation
- `README.md` - Main project documentation and setup
- `docs/quickstart.md` - Quick setup and usage guide
- `CONTRIBUTING.md` - Contribution guidelines
- `docs/gradio-ui.md` - Gradio web UI documentation
- `TODOS.md` - Project task tracking
- `examples/README.md` - Example usage and schemas

---

## Essential Instructions (Always Follow)

### Core Behavior
- Do what has been asked; nothing more, nothing less
- NEVER create files unless absolutely necessary for achieving your goal
- ALWAYS prefer editing existing files to creating new ones
- NEVER proactively create documentation files (*.md) or README files unless explicitly requested

### Naming Conventions
- **Directories**: Use CamelCase (e.g., `VideoProcessor`, `AudioTools`, `DataAnalysis`)
- **Date-based paths**: Use skewer-case with YYYY-MM-DD (e.g., `logs-2025-01-15`, `backup-2025-12-31`)
- **No spaces or underscores** in directory names (except date-based paths)

### TODO Management
- **Always check `TODOS.md` first** when starting a task or session
- **Update immediately** when tasks are completed, added, or changed
- Keep the list current and manageable

### Git Workflow Essentials
**After completing major changes, you MUST:**
1. Check git status: `git status`
2. Review recent commits for style: `git log --oneline -5`
3. Stage changes: `git add .`
4. Commit with proper message format (see below)

**Commit Message Format:**
```
[Action] [Brief description]

- [Specific change 1 with technical detail]
- [Specific change 2 with technical detail]
- [Additional implementation details]

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Action Verbs**: Add, Update, Fix, Refactor, Remove, Enhance

---

## Branch Structure

**Main Branch**: Production-ready code, clean structure, no development guides
**Dev Branch**: Contains all development guides in `ClaudeUsage/` directory

To access development guides:
```bash
git checkout dev
# Browse ClaudeUsage/ directory for detailed guides
```

---

## When to Read Specific Guides

**Read the full guide in `ClaudeUsage/` (on dev branch) when you encounter these situations:**

### Secrets & API Keys
- **When managing API keys or secrets** → Read `ClaudeUsage/secrets_management.md`
- **Before implementing secrets loading** → Read `ClaudeUsage/secrets_management.md`
- **Note**: Currently no API keys required (fully local inference)

### Package Management
- **When using UV package manager** → Read `ClaudeUsage/uv_usage.md`
- **Before creating pyproject.toml** → Read `ClaudeUsage/uv_usage.md`
- **When managing Python dependencies** → Read `ClaudeUsage/uv_usage.md`

### Version Control
- **Before making a git commit** → Read `ClaudeUsage/git_commit_guide.md`
- **When initializing a new repo** → Read `ClaudeUsage/git_commit_guide.md`
- **For git workflow details** → Read `ClaudeUsage/git_commit_guide.md`

### Search & Research
- **When searching across 20+ files** → Read `ClaudeUsage/house_agents.md`
- **When finding patterns in codebase** → Read `ClaudeUsage/house_agents.md`
- **When locating TODOs/FIXMEs** → Read `ClaudeUsage/house_agents.md`

### Testing
- **Before writing tests** → Read `ClaudeUsage/testing_strategies.md`
- **When implementing test coverage** → Read `ClaudeUsage/testing_strategies.md`
- **For test organization** → Read `ClaudeUsage/testing_strategies.md`

### Code Quality
- **When refactoring code** → Read `ClaudeUsage/code_style_guide.md`
- **Before major code changes** → Read `ClaudeUsage/code_style_guide.md`
- **For style guidelines** → Read `ClaudeUsage/code_style_guide.md`

### Project Setup
- **When starting a new project** → Read `ClaudeUsage/project_setup.md`
- **For directory structure** → Read `ClaudeUsage/project_setup.md`
- **Setting up CI/CD** → Read `ClaudeUsage/project_setup.md`

---

## Quick Reference

### Security Basics
- Store API keys in `secrets.json` (NEVER commit)
- Add `secrets.json` to `.gitignore` immediately
- Provide `secrets_template.json` for setup
- Use environment variables as fallbacks
- **SchematronMCP Note**: Currently no API keys required for local inference

### House Agents Quick Trigger
**When searching 20+ files**, use house-research for:
- Finding patterns across codebase
- Searching TODO/FIXME comments
- Locating API endpoints or functions
- Documentation searches

---

## Code Style Guidelines

### Function & Variable Naming
- Use meaningful, descriptive names
- Keep functions small and focused on single responsibilities
- Add docstrings to functions and classes

### Error Handling
- Use try/except blocks gracefully
- Provide helpful error messages
- Never let errors fail silently

### File Organization
- Group related functionality into modules
- Use consistent import ordering:
  1. Standard library
  2. Third-party packages
  3. Local imports
- Keep configuration separate from logic

---

## Communication Style
- Be concise but thorough
- Explain reasoning for significant decisions
- Ask for clarification when requirements are ambiguous
- Proactively suggest improvements when appropriate

---

## Complete Guide Index
For all detailed guides, workflows, and examples, see:
**`ClaudeUsage/README.md`** - Master index of all documentation

---

*Last updated: 2025-10-22*
*Model: Claude Sonnet 4.5*
