#!/usr/bin/env python3
"""
Gradio Web UI for Schematron Extraction Testing

A comprehensive web interface for testing the Schematron model's ability to extract
structured data from HTML using custom or predefined JSON schemas.
"""

import asyncio
import json
import time
from typing import Dict, Any, Optional, Tuple

import gradio as gr

try:
    import httpx
except ImportError:
    raise ImportError(
        "httpx is required for URL fetching. Install with: pip install httpx"
    )

# Import Schematron modules
from lm_studio_inference import get_global_model, SchematronModel
from html_cleaner import clean_html_content, HTMLCleaningLevel
from example_schemas import ALL_SCHEMAS, list_schemas


# Global model instance
_model: Optional[SchematronModel] = None


async def initialize_model() -> Tuple[bool, str]:
    """Initialize the global Schematron model.

    Returns:
        Tuple of (success: bool, message: str)
    """
    global _model

    if _model is not None and _model._loaded:
        return True, "Model already loaded"

    try:
        _model = get_global_model(verbose=True)
        await _model.load()
        return True, "Model loaded successfully"
    except Exception as e:
        return False, f"Failed to load model: {str(e)}"


async def fetch_html_from_url(url: str) -> Tuple[str, str]:
    """Fetch HTML content from a URL.

    Args:
        url: URL to fetch

    Returns:
        Tuple of (html_content: str, status_message: str)
    """
    if not url or not url.strip():
        return "", "Please enter a URL"

    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

            html = response.text
            status = f"Successfully fetched {len(html):,} characters from {url}"
            return html, status

    except httpx.TimeoutException:
        return "", f"Timeout fetching {url} (30s limit exceeded)"
    except httpx.HTTPStatusError as e:
        return "", f"HTTP {e.response.status_code}: {url}"
    except Exception as e:
        return "", f"Error fetching URL: {str(e)}"


def load_example_schema(schema_name: str) -> str:
    """Load a predefined schema by name.

    Args:
        schema_name: Name of the schema (product, article, etc.)

    Returns:
        JSON string of the schema
    """
    if not schema_name or schema_name == "Select a schema...":
        return json.dumps({
            "type": "object",
            "properties": {},
            "required": []
        }, indent=2)

    schema = ALL_SCHEMAS.get(schema_name, {})
    return json.dumps(schema, indent=2)


async def extract_data(
    html_input: str,
    schema_json: str,
    auto_clean: bool,
    cleaning_level: str,
    temperature: float,
    max_tokens: int
) -> Tuple[str, str, str, str]:
    """Extract structured data from HTML using the Schematron model.

    Args:
        html_input: Raw HTML content
        schema_json: JSON schema string
        auto_clean: Whether to automatically clean HTML
        cleaning_level: Cleaning level (light, standard, aggressive)
        temperature: Model temperature (0.0-1.0)
        max_tokens: Maximum tokens to generate

    Returns:
        Tuple of (cleaned_html_preview, extracted_json, metadata, error_msg)
    """
    global _model

    # Validate inputs
    if not html_input or not html_input.strip():
        return "", "", "", "Please provide HTML content"

    if not schema_json or not schema_json.strip():
        return "", "", "", "Please provide a JSON schema"

    # Parse schema
    try:
        schema = json.loads(schema_json)
    except json.JSONDecodeError as e:
        return "", "", "", f"Invalid JSON schema: {str(e)}"

    # Initialize model if needed
    if _model is None or not _model._loaded:
        success, msg = await initialize_model()
        if not success:
            return "", "", "", msg

    # Clean HTML if requested
    cleaned_html = html_input
    if auto_clean:
        level_map = {
            "light": HTMLCleaningLevel.LIGHT,
            "standard": HTMLCleaningLevel.STANDARD,
            "aggressive": HTMLCleaningLevel.AGGRESSIVE
        }
        level = level_map.get(cleaning_level.lower(), HTMLCleaningLevel.STANDARD)
        cleaned_html = clean_html_content(html_input, level=level)

    # Create cleaned HTML preview
    preview_length = 2000
    cleaned_preview = f"Cleaned HTML ({len(cleaned_html):,} chars):\n\n"
    if len(cleaned_html) > preview_length:
        cleaned_preview += cleaned_html[:preview_length] + f"\n\n... (truncated, showing first {preview_length} chars)"
    else:
        cleaned_preview += cleaned_html

    # Extract data
    start_time = time.time()
    try:
        result = await _model.extract(
            html=cleaned_html,
            schema=schema,
            temperature=temperature,
            max_tokens=max_tokens
        )

        extraction_time = time.time() - start_time

        # Format result
        result_json = json.dumps(result, indent=2, ensure_ascii=False)

        # Create metadata
        metadata = f"""Extraction Metadata:
- Processing time: {extraction_time:.2f}s
- HTML length: {len(html_input):,} chars (original) → {len(cleaned_html):,} chars (cleaned)
- Result length: {len(result_json):,} chars
- Temperature: {temperature}
- Max tokens: {max_tokens}
- Cleaning: {cleaning_level if auto_clean else 'disabled'}
"""

        return cleaned_preview, result_json, metadata, ""

    except Exception as e:
        error_msg = f"Extraction failed: {str(e)}"
        import traceback
        error_msg += f"\n\nTraceback:\n{traceback.format_exc()}"
        return cleaned_preview, "", "", error_msg


def calculate_dynamic_tokens(
    html_input: str,
    schema_json: str,
    auto_clean: bool,
    cleaning_level: str
) -> tuple[int, str]:
    """Calculate recommended max_tokens based on HTML and schema size.

    Args:
        html_input: HTML content
        schema_json: JSON schema string
        auto_clean: Whether to clean HTML first
        cleaning_level: Cleaning level (light/standard/aggressive)

    Returns:
        Tuple of (recommended_tokens, info_message)
    """
    if not html_input or not html_input.strip():
        return 32000, "⚠️ No HTML provided - using default 32k tokens"

    # Clean HTML first if requested (to match what model will see)
    if auto_clean:
        level_map = {
            "light": HTMLCleaningLevel.LIGHT,
            "standard": HTMLCleaningLevel.STANDARD,
            "aggressive": HTMLCleaningLevel.AGGRESSIVE
        }
        level = level_map.get(cleaning_level.lower(), HTMLCleaningLevel.STANDARD)
        html_to_analyze = clean_html_content(html_input, level=level)
        html_note = f" (after {cleaning_level} cleaning)"
    else:
        html_to_analyze = html_input
        html_note = " (raw HTML)"

    # Estimate tokens on CLEANED HTML (rough: 1 token ≈ 4 characters)
    html_chars = len(html_to_analyze)
    schema_chars = len(schema_json)

    # Input tokens (HTML + schema + system prompt overhead)
    input_tokens = (html_chars + schema_chars + 500) // 4

    # Output tokens estimate:
    # - Small HTML (<10k chars): 4k-8k tokens output
    # - Medium HTML (10k-50k): 8k-16k tokens output
    # - Large HTML (50k+): 16k-32k tokens output
    if html_chars < 10000:
        output_tokens = 8000
    elif html_chars < 50000:
        output_tokens = 16000
    else:
        output_tokens = 32000

    # Add buffer for safety
    recommended = int(output_tokens * 1.2)

    # Cap at model max
    recommended = min(recommended, 128000)

    info = f"""✅ **Auto-calculated tokens:**
- HTML{html_note}: {html_chars:,} chars (~{html_chars//4:,} tokens)
- Schema: {schema_chars:,} chars (~{schema_chars//4:,} tokens)
- Estimated output: ~{output_tokens:,} tokens
- **Recommended max_tokens: {recommended:,}** (with 20% buffer)"""

    return recommended, info


def create_ui() -> gr.Blocks:
    """Create the Gradio UI.

    Returns:
        Gradio Blocks interface
    """

    # Get available schema names
    schema_names = ["Select a schema..."] + list_schemas()

    with gr.Blocks(
        title="Schematron Extraction Tester",
        theme=gr.themes.Default(primary_hue="slate")
    ) as app:

        gr.Markdown("""
        # Schematron Extraction Tester

        Test the Schematron-3B model's ability to extract structured data from HTML.

        **Quick Start:**
        1. Enter a URL and click "Fetch HTML" (or paste HTML directly)
        2. Select a predefined schema or edit the JSON schema
        3. Configure extraction settings
        4. Click "Extract Data"
        """)

        with gr.Row():
            with gr.Column(scale=1):
                gr.Markdown("### 1. Input HTML")

                # URL input
                url_input = gr.Textbox(
                    label="URL to Fetch",
                    placeholder="https://example.com/product",
                    lines=1
                )

                fetch_btn = gr.Button("Fetch HTML from URL", variant="secondary")
                fetch_status = gr.Textbox(label="Fetch Status", lines=1, interactive=False)

                # HTML input
                html_input = gr.Textbox(
                    label="HTML Content",
                    placeholder="Paste HTML here or fetch from URL...",
                    lines=10,
                    max_lines=20
                )

                gr.Markdown("### 2. Configure Schema")

                # Schema selection
                schema_dropdown = gr.Dropdown(
                    choices=schema_names,
                    label="Example Schemas",
                    value="Select a schema...",
                    info="Select a predefined schema or edit JSON below"
                )

                schema_editor = gr.Code(
                    label="JSON Schema",
                    language="json",
                    value=json.dumps({
                        "type": "object",
                        "properties": {},
                        "required": []
                    }, indent=2),
                    lines=15
                )

                gr.Markdown("### 3. Extraction Settings")

                auto_clean = gr.Checkbox(
                    label="Auto-clean HTML",
                    value=True,
                    info="Remove scripts, styles, and other noise"
                )

                cleaning_level = gr.Radio(
                    choices=["light", "standard", "aggressive"],
                    value="standard",
                    label="Cleaning Level",
                    info="How aggressively to clean HTML"
                )

                with gr.Row():
                    temperature = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=0.0,
                        step=0.05,
                        label="Temperature",
                        info="Higher = more creative, Lower = more deterministic"
                    )

                    max_tokens = gr.Slider(
                        minimum=1000,
                        maximum=128000,
                        value=32000,
                        step=4000,
                        label="Max Tokens (Model max: 128k)",
                        info="Maximum length of model output - higher values take longer"
                    )

                auto_tokens_btn = gr.Button(
                    "🔢 Auto-Calculate Tokens",
                    variant="secondary",
                    size="sm"
                )

                token_info = gr.Markdown(
                    "Click to estimate tokens based on HTML length",
                    visible=True
                )

                extract_btn = gr.Button("Extract Data", variant="primary", size="lg")

            with gr.Column(scale=1):
                gr.Markdown("### 4. Results")

                # Cleaned HTML preview (collapsible)
                with gr.Accordion("Cleaned HTML Preview", open=False):
                    cleaned_html_preview = gr.Textbox(
                        label="Cleaned HTML",
                        lines=10,
                        max_lines=20,
                        interactive=False
                    )

                # Extracted JSON
                extracted_json = gr.Code(
                    label="Extracted Data (JSON)",
                    language="json",
                    lines=15,
                    interactive=False
                )

                # Metadata
                metadata_output = gr.Textbox(
                    label="Metadata",
                    lines=6,
                    interactive=False
                )

                # Errors
                error_output = gr.Textbox(
                    label="Errors",
                    lines=5,
                    interactive=False,
                    visible=True
                )

        # Example data
        gr.Markdown("### Examples")

        gr.Examples(
            examples=[
                [
                    "https://www.example.com",
                    "product",
                    True,
                    "standard",
                    0.0,
                    8000
                ],
                [
                    "<h1>Test Article</h1><p>Content here</p>",
                    "article",
                    True,
                    "standard",
                    0.0,
                    8000
                ]
            ],
            inputs=[url_input, schema_dropdown, auto_clean, cleaning_level, temperature, max_tokens],
            label="Quick Examples"
        )

        # Event handlers
        def fetch_html_wrapper(url):
            """Wrapper for fetch_html_from_url to work with Gradio."""
            html, status = asyncio.run(fetch_html_from_url(url))
            return html, status

        fetch_btn.click(
            fn=fetch_html_wrapper,
            inputs=[url_input],
            outputs=[html_input, fetch_status]
        )

        schema_dropdown.change(
            fn=load_example_schema,
            inputs=[schema_dropdown],
            outputs=[schema_editor]
        )

        # Auto-calculate tokens button
        auto_tokens_btn.click(
            fn=calculate_dynamic_tokens,
            inputs=[html_input, schema_editor, auto_clean, cleaning_level],
            outputs=[max_tokens, token_info]
        )

        def extract_wrapper(html_input, schema_json, auto_clean, cleaning_level, temperature, max_tokens):
            """Wrapper for extract_data to work with Gradio."""
            cleaned_preview, result_json, metadata, error = asyncio.run(
                extract_data(html_input, schema_json, auto_clean, cleaning_level, temperature, max_tokens)
            )
            return cleaned_preview, result_json, metadata, error

        extract_btn.click(
            fn=extract_wrapper,
            inputs=[html_input, schema_editor, auto_clean, cleaning_level, temperature, max_tokens],
            outputs=[cleaned_html_preview, extracted_json, metadata_output, error_output]
        )

        gr.Markdown("""
        ---

        **Tips:**
        - Use temperature 0.0 for deterministic results
        - Standard cleaning level works best for most websites
        - The model was trained on cleaned HTML (remove scripts/styles)
        - Larger max_tokens allows for more detailed extraction

        **Troubleshooting:**
        - Ensure LM Studio is running with the Schematron model loaded
        - Check that the API endpoint is configured correctly in config.json
        - Verify your JSON schema is valid
        """)

    return app


def main():
    """Launch the Gradio app."""

    # Initialize model on startup
    print("Initializing Schematron model...")
    success, msg = asyncio.run(initialize_model())

    if success:
        print(f"✓ {msg}")
    else:
        print(f"⚠ Warning: {msg}")
        print("  The model will be initialized on first extraction.")

    # Create and launch UI
    app = create_ui()

    print("\nLaunching Gradio interface...")
    app.launch(
        share=False,
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True
    )


if __name__ == "__main__":
    main()
