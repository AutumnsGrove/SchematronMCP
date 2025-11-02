"""
Schematron MCP Server

A Model Context Protocol server that provides HTML-to-JSON extraction using Schematron-3B.
"""

__version__ = "0.1.0"

# Export main server components
from schematron_mcp.server import mcp

# Export inference models
from schematron_mcp.inference.lm_studio import SchematronModel

# Export cleaning utilities
from schematron_mcp.cleaning.html_cleaner import (
    clean_html_content,
    HTMLCleaningLevel,
)

__all__ = [
    "mcp",
    "SchematronModel",
    "clean_html_content",
    "HTMLCleaningLevel",
    "__version__",
]
