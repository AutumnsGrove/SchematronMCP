# Gradio Web UI for Schematron Extraction

A comprehensive web interface for testing the Schematron-3B model's structured data extraction capabilities.

## Features

- **URL Fetching**: Automatically fetch HTML from any URL
- **HTML Preview**: View and edit HTML content before extraction
- **Schema Selection**: Choose from 9 predefined schemas or create custom ones
- **Extraction Settings**: Configure temperature, max tokens, and HTML cleaning
- **Real-time Results**: See extracted JSON, metadata, and errors
- **Progress Indicators**: Visual feedback during fetch and extraction

## Installation

### Prerequisites

1. **LM Studio** must be running with the Schematron model loaded
2. Python 3.9+ with required dependencies

### Install Dependencies

```bash
pip install gradio httpx openai lxml
```

Or if using UV:

```bash
uv pip install gradio httpx openai lxml
```

## Usage

### Starting the App

```bash
python gradio_app.py
```

Or make it executable:

```bash
chmod +x gradio_app.py
./gradio_app.py
```

The app will launch at: `http://localhost:7860`

### Using the Interface

#### 1. Input HTML

**Option A: Fetch from URL**
- Enter a URL in the "URL to Fetch" field
- Click "Fetch HTML from URL"
- HTML will appear in the "HTML Content" field

**Option B: Paste HTML**
- Directly paste HTML into the "HTML Content" field

#### 2. Configure Schema

**Option A: Use Predefined Schema**
- Select from the dropdown:
  - `product` - E-commerce products
  - `article` - Blog posts/news articles
  - `job` - Job postings
  - `real_estate` - Real estate listings
  - `restaurant` - Restaurant/business listings
  - `event` - Event information
  - `contact` - Contact information
  - `publication` - Research papers
  - `table` - Generic table data

**Option B: Custom Schema**
- Edit the JSON schema directly in the code editor
- Must be valid JSON Schema format

#### 3. Extraction Settings

- **Auto-clean HTML**: Enable to remove scripts, styles, etc.
- **Cleaning Level**:
  - `light` - Remove only scripts and styles
  - `standard` - Recommended, matches training data
  - `aggressive` - Remove more elements (forms, nav, etc.)
- **Temperature**: 0.0 (deterministic) to 1.0 (creative)
- **Max Tokens**: 1000-16000 (default: 8000)

#### 4. Extract Data

- Click "Extract Data" button
- View results in the output panels:
  - **Cleaned HTML Preview**: See processed HTML (collapsible)
  - **Extracted Data (JSON)**: Structured output
  - **Metadata**: Processing time, token count, etc.
  - **Errors**: Any errors during extraction

## Example Workflow

### Extracting Product Data

1. Enter URL: `https://www.amazon.com/dp/B08N5WRWNW`
2. Click "Fetch HTML from URL"
3. Select schema: `product`
4. Settings:
   - Auto-clean: ✓
   - Cleaning level: `standard`
   - Temperature: `0.0`
   - Max tokens: `8000`
5. Click "Extract Data"
6. Review extracted JSON with product details

### Extracting Article Data

1. Paste HTML of a blog post
2. Select schema: `article`
3. Keep default settings
4. Click "Extract Data"
5. Get structured article data (title, author, content, etc.)

## Predefined Schemas

### Product Schema
Extracts: name, price, rating, reviews, stock status, description, specs, images

### Article Schema
Extracts: title, author, published date, content, summary, tags, word count

### Job Posting Schema
Extracts: title, company, location, salary, employment type, requirements, benefits

### Real Estate Schema
Extracts: address, price, bedrooms, bathrooms, square feet, features, images

### Restaurant Schema
Extracts: name, cuisine, address, rating, price range, hours, features

### Event Schema
Extracts: title, date, time, location, description, organizer, ticket price

### Contact Schema
Extracts: name, email, phone, address, website, social media

### Publication Schema
Extracts: title, authors, abstract, publication date, journal, DOI, keywords

### Table Schema
Extracts: headers and rows from HTML tables

## Tips for Best Results

1. **Use Standard Cleaning**: The model was trained on cleaned HTML
2. **Temperature 0.0**: Most reliable for data extraction
3. **Appropriate Schema**: Choose the schema that matches your content
4. **Valid HTML**: Better HTML structure = better extraction
5. **Max Tokens**: Increase if output is being truncated

## Troubleshooting

### Model Not Loading

**Error**: "Failed to load model: Connection refused"

**Solution**:
1. Ensure LM Studio is running
2. Load the Schematron model in LM Studio
3. Verify API endpoint in `config.json`:
   ```json
   {
     "lm_studio": {
       "api_base": "http://localhost:1234/v1",
       "model_name": "local-model"
     }
   }
   ```

### URL Fetch Timeout

**Error**: "Timeout fetching URL (30s limit exceeded)"

**Solution**:
- Try fetching manually and pasting HTML
- Check if the URL is accessible
- Some sites block automated requests

### Invalid JSON Schema

**Error**: "Invalid JSON schema"

**Solution**:
- Use the predefined schemas as templates
- Validate JSON syntax (commas, brackets, quotes)
- Ensure schema follows JSON Schema format

### Extraction Errors

**Error**: "Extraction failed"

**Solution**:
1. Check that HTML is not empty
2. Try different cleaning levels
3. Increase max_tokens if output is complex
4. Verify schema matches content type

## Advanced Usage

### Custom Schemas

Create custom schemas by editing the JSON editor:

```json
{
  "type": "object",
  "properties": {
    "custom_field": {
      "type": "string",
      "description": "Description of what to extract"
    },
    "price": {
      "type": "number",
      "description": "Numeric price value"
    },
    "items": {
      "type": "array",
      "items": {"type": "string"},
      "description": "List of items"
    }
  },
  "required": ["custom_field"]
}
```

### Programmatic Access

The Gradio app can be accessed programmatically:

```python
import gradio as gr

# Connect to running instance
client = gr.Client("http://localhost:7860")

# Call extraction
result = client.predict(
    html_input="<html>...</html>",
    schema_json='{"type": "object", ...}',
    auto_clean=True,
    cleaning_level="standard",
    temperature=0.0,
    max_tokens=8000
)
```

## Configuration

Edit `config.json` to customize:

```json
{
  "lm_studio": {
    "api_base": "http://localhost:1234/v1",
    "model_path": "/path/to/schematron-model",
    "model_name": "local-model"
  },
  "inference": {
    "default_temperature": 0.0,
    "default_max_tokens": 8000,
    "verbose": false
  }
}
```

## Performance Notes

- First extraction initializes the model (may take a few seconds)
- Subsequent extractions are faster (model stays loaded)
- Large HTML (>50KB) may take longer to process
- Temperature 0.0 is fastest (no sampling randomness)

## Known Limitations

- Maximum HTML size: ~1M characters (limited by model context)
- URL fetch timeout: 30 seconds
- Some websites block automated requests
- Complex JavaScript-rendered sites may not work (fetch static HTML only)

## Support

For issues or questions:
1. Check that LM Studio is running with the model loaded
2. Review error messages in the "Errors" panel
3. Try the examples to verify setup
4. Check the main project `../README.md` for model configuration

---

Built with [Gradio](https://gradio.app/) and [Schematron-3B](https://huggingface.co/pchamart/schematron3B-mlx-8bit)
