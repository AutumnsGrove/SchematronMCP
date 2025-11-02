#!/usr/bin/env python3
"""
Schematron MCP Server

A Model Context Protocol server that provides HTML-to-JSON extraction using Schematron-3B.
This server exposes tools for extracting structured data from HTML content using a local
MLX-quantized Schematron model.
"""

import json
import asyncio
from typing import Optional, Dict, Any
from enum import Enum

from mcp.server.fastmcp import FastMCP, Context
from pydantic import BaseModel, Field, ConfigDict, field_validator

from schematron_mcp.inference.lm_studio import SchematronModel
from schematron_mcp.cleaning.html_cleaner import clean_html_content, HTMLCleaningLevel


# Constants
CHARACTER_LIMIT = 25000  # Maximum response size in characters
DEFAULT_MODEL_PATH = "mlx-community/Schematron-3B-4bit"

# Initialize FastMCP server
mcp = FastMCP("schematron_mcp")

# Global model instance (loaded at startup)
_model: Optional[SchematronModel] = None


async def get_model() -> SchematronModel:
    """Get or initialize the Schematron model."""
    global _model
    if _model is None:
        _model = SchematronModel()
        await _model.load()
    return _model


# Response format enum
class ResponseFormat(str, Enum):
    """Output format for tool responses."""
    JSON = "json"
    MARKDOWN = "markdown"


# Input Models
class ExtractStructuredDataInput(BaseModel):
    """Input model for structured data extraction from HTML."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    html: str = Field(
        ...,
        description=(
            "Raw HTML content to extract data from. Must be HTML string, NOT a URL. "
            "For best results, this should be cleaned HTML with scripts/styles removed. "
            "Example: '<div><h1>Product Name</h1><p>Price: $99</p></div>'"
        ),
        min_length=10
    )
    
    schema: Dict[str, Any] = Field(
        ...,
        description=(
            "JSON Schema (draft-07 format) defining the structure of the desired output. "
            "Must be a valid JSON Schema object with 'type', 'properties', etc. "
            "Example: {'type': 'object', 'properties': {'name': {'type': 'string'}, "
            "'price': {'type': 'number'}}}"
        )
    )
    
    auto_clean: bool = Field(
        default=True,
        description=(
            "Whether to automatically clean the HTML before extraction. "
            "Removes scripts, styles, and JavaScript using lxml. "
            "Set to false if HTML is already cleaned or you want raw extraction."
        )
    )
    
    temperature: float = Field(
        default=0.0,
        description=(
            "Generation temperature (0.0-1.0). Keep at 0.0 for deterministic, "
            "reproducible JSON outputs. Higher values increase randomness."
        ),
        ge=0.0,
        le=1.0
    )
    
    max_tokens: Optional[int] = Field(
        default=None,
        description=(
            "Maximum number of tokens to generate. If not specified, automatically "
            "calculated based on HTML size (small: 8k, medium: 16k, large: 32k). "
            "Model maximum is 128k tokens."
        ),
        ge=100,
        le=128000
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.JSON,
        description=(
            "Output format: 'json' returns parsed JSON object, "
            "'markdown' returns formatted markdown with the JSON"
        )
    )
    
    @field_validator('schema')
    @classmethod
    def validate_schema(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Validate that schema is a proper JSON Schema object."""
        if not isinstance(v, dict):
            raise ValueError("Schema must be a dictionary")
        if 'type' not in v:
            raise ValueError("Schema must have a 'type' field")
        return v


class CleanHTMLInput(BaseModel):
    """Input model for HTML cleaning operation."""
    
    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra='forbid'
    )
    
    html: str = Field(
        ...,
        description=(
            "Raw HTML content to clean. Removes scripts, styles, JavaScript, "
            "and other noise while preserving content structure."
        ),
        min_length=10
    )
    
    cleaning_level: str = Field(
        default="standard",
        description=(
            "Cleaning aggressiveness: 'light' (remove only scripts/styles), "
            "'standard' (recommended, matches training data), "
            "'aggressive' (remove more elements but may lose some content)"
        )
    )
    
    response_format: ResponseFormat = Field(
        default=ResponseFormat.MARKDOWN,
        description="Output format: 'json' or 'markdown'"
    )


# Helper Functions
def calculate_smart_tokens(html: str, schema: Dict[str, Any]) -> int:
    """Calculate optimal max_tokens based on HTML and schema size.

    Args:
        html: HTML content
        schema: JSON Schema

    Returns:
        Recommended max_tokens value
    """
    html_chars = len(html)
    schema_chars = len(json.dumps(schema))

    # Smart token budget based on HTML size:
    # - Small HTML (<10k chars): 8k-12k tokens output
    # - Medium HTML (10k-50k): 16k-24k tokens output
    # - Large HTML (50k+): 32k-48k tokens output
    if html_chars < 10000:
        output_tokens = 8000
    elif html_chars < 50000:
        output_tokens = 16000
    else:
        output_tokens = 32000

    # Add 20% buffer for safety
    recommended = int(output_tokens * 1.2)

    # Cap at model maximum
    recommended = min(recommended, 128000)

    return recommended


def format_extraction_result(
    result: Dict[str, Any],
    response_format: ResponseFormat,
    html_length: int,
    cleaned: bool,
    error: Optional[str] = None
) -> str:
    """Format extraction result based on response format."""
    
    if response_format == ResponseFormat.JSON:
        output = {
            "success": error is None,
            "extracted_data": result if error is None else None,
            "metadata": {
                "html_length": html_length,
                "was_cleaned": cleaned
            }
        }
        if error:
            output["error"] = error
        return json.dumps(output, indent=2)
    
    else:  # MARKDOWN
        if error:
            return f"""# Extraction Failed

**Error:** {error}

**HTML Length:** {html_length} characters
**Was Cleaned:** {cleaned}

Please check your HTML and schema, then try again."""

        result_json = json.dumps(result, indent=2)
        
        # Check character limit
        if len(result_json) > CHARACTER_LIMIT:
            result_json = result_json[:CHARACTER_LIMIT] + "\n... (truncated)"
            truncation_notice = "\n\n⚠️ **Note:** Response was truncated. Use JSON format for full data."
        else:
            truncation_notice = ""
        
        return f"""# Extraction Successful

## Extracted Data

```json
{result_json}
```

## Metadata
- **HTML Length:** {html_length} characters
- **Was Cleaned:** {cleaned}
{truncation_notice}"""


def format_cleaned_html(
    cleaned_html: str,
    original_length: int,
    cleaned_length: int,
    response_format: ResponseFormat
) -> str:
    """Format cleaned HTML result."""
    
    if response_format == ResponseFormat.JSON:
        return json.dumps({
            "cleaned_html": cleaned_html,
            "original_length": original_length,
            "cleaned_length": cleaned_length,
            "reduction_percent": round((1 - cleaned_length / original_length) * 100, 1)
        }, indent=2)
    
    else:  # MARKDOWN
        reduction = round((1 - cleaned_length / original_length) * 100, 1)
        
        # Truncate if too long
        display_html = cleaned_html
        if len(display_html) > CHARACTER_LIMIT:
            display_html = display_html[:CHARACTER_LIMIT] + "\n... (truncated)"
            truncation_notice = "\n\n⚠️ **Note:** Output was truncated. Use JSON format for full content."
        else:
            truncation_notice = ""
        
        return f"""# HTML Cleaned Successfully

## Statistics
- **Original Length:** {original_length:,} characters
- **Cleaned Length:** {cleaned_length:,} characters
- **Reduction:** {reduction}%

## Cleaned HTML

```html
{display_html}
```
{truncation_notice}"""


# MCP Tools
@mcp.tool(
    name="schematron_extract_structured_data",
    annotations={
        "title": "Extract Structured JSON from HTML",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def extract_structured_data(params: ExtractStructuredDataInput, ctx: Context) -> str:
    """Extract structured JSON data from HTML using Schematron-3B.
    
    This tool converts messy HTML into clean, typed JSON that conforms to your custom schema.
    It uses a locally-running MLX-quantized Schematron-3B model for fast, accurate extraction.
    
    **Key Features:**
    - Schema-first extraction with 100% conformance
    - Handles long HTML documents (up to 128K tokens)
    - Optional automatic HTML cleaning (removes scripts/styles)
    - Deterministic output with temperature=0.0
    
    **Usage Guidelines:**
    1. Provide the HTML content as a string (NOT a URL)
    2. Define a clear JSON Schema with specific field types and descriptions
    3. Let auto_clean=True for best results (matches training data)
    4. Keep temperature at 0.0 for reproducible outputs
    
    **Example Schema:**
    ```json
    {
        "type": "object",
        "properties": {
            "product_name": {"type": "string", "description": "Product title"},
            "price": {"type": "number", "description": "Product price in USD"},
            "rating": {"type": "number", "description": "Star rating 1-5"},
            "in_stock": {"type": "boolean"}
        },
        "required": ["product_name", "price"]
    }
    ```
    
    Args:
        params (ExtractStructuredDataInput): Extraction parameters containing:
            - html (str): Raw HTML content (required, min 10 chars)
            - schema (dict): JSON Schema defining output structure (required)
            - auto_clean (bool): Auto-clean HTML before extraction (default: True)
            - temperature (float): Generation temperature 0.0-1.0 (default: 0.0)
            - max_tokens (int): Max tokens to generate (default: 8000)
            - response_format (str): 'json' or 'markdown' (default: 'json')
        ctx (Context): MCP context for logging and progress reporting
    
    Returns:
        str: Extracted JSON data in the requested format
        
        JSON format returns:
        {
            "success": true,
            "extracted_data": {...},
            "metadata": {"html_length": 1234, "was_cleaned": true}
        }
        
        Markdown format returns formatted text with the JSON in code blocks.
    
    Raises:
        Returns error information in response if extraction fails.
    """
    
    # Report progress
    await ctx.report_progress(0.1, "Initializing model...")

    # Get model instance
    model = await get_model()

    # Clean HTML if requested - DO THIS FIRST
    original_length = len(params.html)
    if params.auto_clean:
        await ctx.report_progress(0.2, "Cleaning HTML...")
        cleaned_html = clean_html_content(params.html)
        await ctx.log_info(f"Cleaned HTML: {original_length} → {len(cleaned_html)} chars")
    else:
        cleaned_html = params.html
        await ctx.log_info(f"Using raw HTML: {original_length} chars")

    # NOW calculate smart token budget based on CLEANED HTML
    if params.max_tokens is None:
        params.max_tokens = calculate_smart_tokens(cleaned_html, params.schema)
        await ctx.log_info(
            f"Auto-calculated max_tokens: {params.max_tokens} "
            f"(Cleaned HTML: {len(cleaned_html):,} chars)"
        )
    
    # Extract structured data
    try:
        await ctx.report_progress(0.4, "Extracting structured data...")
        
        result = await model.extract(
            html=cleaned_html,
            schema=params.schema,
            temperature=params.temperature,
            max_tokens=params.max_tokens
        )
        
        await ctx.report_progress(0.9, "Formatting response...")
        
        # Format and return result
        response = format_extraction_result(
            result=result,
            response_format=params.response_format,
            html_length=original_length,
            cleaned=params.auto_clean,
            error=None
        )
        
        await ctx.report_progress(1.0, "Complete!")
        return response
        
    except Exception as e:
        await ctx.log_error(f"Extraction failed: {str(e)}")
        return format_extraction_result(
            result={},
            response_format=params.response_format,
            html_length=original_length,
            cleaned=params.auto_clean,
            error=str(e)
        )


@mcp.tool(
    name="schematron_clean_html",
    annotations={
        "title": "Clean HTML (Remove Scripts/Styles)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": False
    }
)
async def clean_html(params: CleanHTMLInput) -> str:
    """Clean HTML by removing scripts, styles, and JavaScript.
    
    This tool preprocesses HTML to remove noise before extraction. It's useful when you want
    to inspect cleaned HTML before passing it to the extraction tool, or when you need cleaned
    HTML for other purposes.
    
    **Cleaning Levels:**
    - **light**: Remove only scripts, <style> tags, and inline JavaScript
    - **standard**: (Recommended) Matches Schematron training data preprocessing
    - **aggressive**: Remove more elements (forms, iframes, etc.) but may lose content
    
    **When to Use:**
    - You want to see cleaned HTML before extraction
    - You need cleaned HTML for purposes other than Schematron
    - You're debugging extraction issues
    
    **When NOT to Use:**
    - Just use auto_clean=True in extract_structured_data instead
    
    Args:
        params (CleanHTMLInput): Cleaning parameters containing:
            - html (str): Raw HTML content (required)
            - cleaning_level (str): 'light', 'standard', or 'aggressive' (default: 'standard')
            - response_format (str): 'json' or 'markdown' (default: 'markdown')
    
    Returns:
        str: Cleaned HTML in the requested format
        
        JSON format returns:
        {
            "cleaned_html": "...",
            "original_length": 1234,
            "cleaned_length": 567,
            "reduction_percent": 54.1
        }
        
        Markdown format returns formatted text with statistics and cleaned HTML.
    """
    
    original_length = len(params.html)
    
    # Map cleaning level to enum
    level_map = {
        "light": HTMLCleaningLevel.LIGHT,
        "standard": HTMLCleaningLevel.STANDARD,
        "aggressive": HTMLCleaningLevel.AGGRESSIVE
    }
    cleaning_level = level_map.get(params.cleaning_level, HTMLCleaningLevel.STANDARD)
    
    # Clean HTML
    cleaned = clean_html_content(params.html, level=cleaning_level)
    cleaned_length = len(cleaned)
    
    # Format and return
    return format_cleaned_html(
        cleaned_html=cleaned,
        original_length=original_length,
        cleaned_length=cleaned_length,
        response_format=params.response_format
    )


# Main entry point
def main():
    """Main entry point for the MCP server."""
    mcp.run()


if __name__ == "__main__":
    # Run the MCP server with stdio transport
    main()
