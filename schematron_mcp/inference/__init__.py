"""
Inference backend for Schematron model.

Uses LM Studio (OpenAI-compatible API) for model inference.
"""

from schematron_mcp.inference.lm_studio import SchematronModel

__all__ = [
    "SchematronModel",
]
