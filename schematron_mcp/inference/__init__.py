"""
Inference backends for Schematron model.

Supports both MLX (Apple Silicon) and LM Studio (OpenAI-compatible API).
"""

from schematron_mcp.inference.lm_studio import SchematronModel as LMStudioModel
from schematron_mcp.inference.mlx import SchematronModel as MLXModel

# Default to LM Studio model
SchematronModel = LMStudioModel

__all__ = [
    "SchematronModel",
    "LMStudioModel",
    "MLXModel",
]
