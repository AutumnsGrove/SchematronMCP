"""
Schematron MCP Server

A Model Context Protocol server that provides HTML-to-JSON extraction using Schematron-3B.
"""

__version__ = "0.1.0"

# Lazy imports to avoid circular dependencies and reduce startup overhead
# Users should import from specific modules:
# - from schematron_mcp.inference.lm_studio import SchematronModel
# - from schematron_mcp.cleaning.html_cleaner import clean_html_content
# - from schematron_mcp.server import main

__all__ = [
    "__version__",
]
