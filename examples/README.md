# Examples

This directory contains example usage and testing tools for SchematronMCP.

## Files

- **gradio_app.py**: Web UI for testing extraction (run with `python examples/gradio_app.py`)
- **test_extraction.py**: Manual testing script for extraction
- **schemas.py**: Example JSON schemas for common extraction tasks

## Usage

Run the Gradio web UI:
```bash
python examples/gradio_app.py
```

Run the manual test script:
```bash
python examples/test_extraction.py
```

## Available Schemas

The `schemas.py` module provides pre-built schemas for common extraction tasks:

- **product**: E-commerce product extraction
- **article**: Blog article/news extraction
- **job**: Job posting extraction
- **real_estate**: Real estate listing extraction
- **restaurant**: Restaurant/business listing extraction
- **event**: Event listing extraction
- **contact**: Contact information extraction
- **publication**: Research paper/publication extraction
- **table**: Generic table data extraction
- **general**: General purpose flexible schema

## Gradio Web UI

The Gradio app provides a comprehensive web interface for testing HTML extraction with:

- URL fetching or direct HTML input
- Predefined schema selection
- Configurable HTML cleaning levels
- Adjustable model parameters (temperature, max_tokens)
- Auto-calculated token recommendations
- Real-time extraction results

## Test Script

The `test_extraction.py` script demonstrates:

- HTML cleaning at different levels
- Product extraction from sample HTML
- Article extraction from sample HTML
- Using the MLX inference backend

Customize the HTML samples and schemas to test your specific use cases.
