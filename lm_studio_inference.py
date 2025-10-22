"""
LM Studio Inference Module for Schematron

Handles loading and running the Schematron-3B model using LM Studio's OpenAI-compatible API.
This replaces the MLX inference for compatibility with LM Studio.
"""

import json
import os
import asyncio
from typing import Dict, Any, Optional

try:
    from openai import AsyncOpenAI
except ImportError:
    raise ImportError(
        "openai is required for LM Studio inference. Install with: pip install openai"
    )

try:
    from json_repair import repair_json
    HAS_JSON_REPAIR = True
except ImportError:
    HAS_JSON_REPAIR = False


def load_config() -> Dict[str, Any]:
    """Load configuration from config.json with fallback to defaults.

    Returns:
        Configuration dictionary with lm_studio and inference settings
    """
    config_path = os.path.join(os.path.dirname(__file__), "config.json")

    # Default configuration
    default_config = {
        "lm_studio": {
            "api_base": "http://localhost:1234/v1",
            "model_path": "/Volumes/External/Models/pchamart/schematron3B-mlx-8bit",
            "model_name": "local-model"
        },
        "inference": {
            "default_temperature": 0.0,
            "default_max_tokens": 8000,
            "verbose": False
        }
    }

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Merge with defaults to ensure all keys exist
        if "lm_studio" not in config:
            config["lm_studio"] = default_config["lm_studio"]
        if "inference" not in config:
            config["inference"] = default_config["inference"]

        return config
    except FileNotFoundError:
        # Config file not found, use defaults with env var fallbacks
        return default_config
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse config.json: {e}. Using defaults.")
        return default_config


class SchematronModel:
    """Wrapper for Schematron-3B model using LM Studio API."""

    def __init__(
        self,
        model_path: Optional[str] = None,
        api_base: Optional[str] = None,
        verbose: Optional[bool] = None
    ):
        """Initialize SchematronModel for LM Studio.

        Args:
            model_path: Path or name reference for the model (default: from config.json, env vars, or default)
            api_base: LM Studio API endpoint (default: from config.json, env vars, or http://localhost:1234/v1)
            verbose: Whether to print verbose output (default: from config.json or False)
        """
        # Load configuration
        config = load_config()

        # Priority: explicit parameter > environment variable > config.json > default
        self.model_path = (
            model_path or
            os.getenv("SCHEMATRON_MODEL_PATH") or
            config["lm_studio"]["model_path"]
        )
        self.api_base = (
            api_base or
            os.getenv("LM_STUDIO_API_BASE") or
            config["lm_studio"]["api_base"]
        )
        self.verbose = (
            verbose if verbose is not None else
            config["inference"]["verbose"]
        )
        self.model_name = config["lm_studio"]["model_name"]
        self._loaded = False

        # Initialize OpenAI client pointing to LM Studio
        self.client = AsyncOpenAI(
            base_url=self.api_base,
            api_key="lm-studio"  # LM Studio doesn't require a real key
        )

        if self.verbose:
            print(f"LM Studio API configured:")
            print(f"  - Endpoint: {self.api_base}")
            print(f"  - Model reference: {self.model_path}")
            print(f"  - Model name: {self.model_name}")

    async def load(self) -> None:
        """Load the model (verify LM Studio connection)."""
        if self._loaded:
            return

        if self.verbose:
            print(f"Verifying LM Studio connection at {self.api_base}...")

        try:
            # Test connection by listing models
            models = await self.client.models.list()
            if self.verbose:
                print("LM Studio connection verified!")
                print(f"Available models: {[m.id for m in models.data]}")
            self._loaded = True
        except Exception as e:
            raise ConnectionError(
                f"Failed to connect to LM Studio at {self.api_base}. "
                f"Make sure LM Studio is running and the model is loaded. Error: {str(e)}"
            )

    def _construct_prompt(self, schema: Dict[str, Any], html: str) -> str:
        """Construct the Schematron prompt following official format.

        Args:
            schema: JSON Schema object
            html: Cleaned HTML content

        Returns:
            Formatted prompt string
        """
        schema_str = json.dumps(schema, indent=2)

        return f"""You are going to be given a JSON schema following the standardized JSON Schema format. You are going to be given a HTML page and you are going to apply the schema to the HTML page however you see it as applicable and return the results in a JSON object. The schema is as follows:

{schema_str}

Here is the HTML page:

{html}

MAKE SURE ITS VALID JSON."""

    def _fix_json_escape_sequences(self, json_str: str) -> str:
        """Fix invalid escape sequences in JSON strings.

        Args:
            json_str: JSON string with potentially invalid escapes

        Returns:
            Fixed JSON string
        """
        import re

        # Replace invalid escape sequences with proper escaping
        # Valid escapes are: \", \\, \/, \b, \f, \n, \r, \t, \uXXXX
        # Everything else needs the backslash escaped

        # First, let's try using json.dumps on the raw string decode
        # to let Python handle the escaping properly
        try:
            # Use raw string literals to handle this
            # Replace problematic patterns
            fixed = json_str

            # Common invalid escapes that models generate
            invalid_escapes = [
                (r'\"', '"'),  # Already escaped quotes - keep them
                (r'\\', '\\'),  # Already escaped backslash - keep them
                # Fix invalid escapes like \d, \s, \w etc (not valid JSON)
                (r'\\([^"\\/bfnrtu])', r'\\\\\1'),  # Double-escape invalid ones
            ]

            # Actually, better approach: use strict=False in json.loads
            # But that doesn't exist, so let's manually fix

            # Replace control characters that aren't properly escaped
            fixed = fixed.replace('\t', '\\t')
            fixed = fixed.replace('\n', '\\n')
            fixed = fixed.replace('\r', '\\r')

            return fixed

        except Exception:
            return json_str

    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse and validate the JSON response.

        Args:
            response: Raw model output

        Returns:
            Parsed JSON object

        Raises:
            ValueError: If response is not valid JSON
        """
        # Strip whitespace
        response = response.strip()

        # Remove markdown code blocks if present
        if response.startswith("```"):
            # Split by ``` and get the content
            parts = response.split("```")
            if len(parts) >= 2:
                response = parts[1]
                # Remove 'json' language identifier if present
                if response.startswith("json"):
                    response = response[4:]
                response = response.strip()

        # Try to parse JSON - first attempt with strict=False for more lenient parsing
        try:
            # Use strict=False to allow control characters and other issues
            return json.loads(response, strict=False)
        except json.JSONDecodeError as e:
            # Try json-repair library first if available
            if HAS_JSON_REPAIR:
                try:
                    if self.verbose:
                        print(f"\nJSON parse failed, attempting repair...")
                    repaired = repair_json(response)
                    result = json.loads(repaired)
                    if self.verbose:
                        print(f"✅ Successfully repaired JSON")
                    return result
                except Exception as repair_error:
                    if self.verbose:
                        print(f"⚠️ JSON repair failed: {repair_error}")

            # If parsing fails, try to fix escape sequences
            if "Invalid \\escape" in str(e):
                try:
                    # Use ast.literal_eval as a more lenient parser
                    import ast
                    # Try to fix by using Python's literal eval (more lenient)
                    # But this won't work for true/false/null

                    # Better approach: manually fix the escapes
                    import re

                    # Find all strings in the JSON and fix their escapes
                    def fix_string_escapes(match):
                        string_content = match.group(1)
                        # Fix invalid escapes by double-escaping the backslash
                        # Keep valid escapes as-is
                        fixed = re.sub(
                            r'\\(?!["\\/bfnrtu])',  # Backslash not followed by valid escape char
                            r'\\\\',  # Replace with double backslash
                            string_content
                        )
                        return f'"{fixed}"'

                    # Fix escapes in all strings (content between quotes)
                    fixed_response = re.sub(
                        r'"((?:[^"\\]|\\.)*)' + r'"',  # Match strings
                        fix_string_escapes,
                        response,
                        flags=re.DOTALL
                    )

                    return json.loads(fixed_response)

                except Exception as fix_error:
                    # If fixing didn't work, raise original error
                    raise ValueError(
                        f"Failed to parse JSON response: {str(e)}\n"
                        f"Attempted fix but got: {str(fix_error)}\n"
                        f"Response: {response[:500]}..."
                    )
            else:
                # Different JSON error, re-raise
                raise ValueError(f"Failed to parse JSON response: {str(e)}\nResponse: {response[:500]}...")

    async def extract(
        self,
        html: str,
        schema: Dict[str, Any],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """Extract structured data from HTML using LM Studio.

        Args:
            html: HTML content (should be cleaned)
            schema: JSON Schema defining output structure
            temperature: Generation temperature (default: from config.json or 0.0)
            max_tokens: Maximum tokens to generate (default: from config.json or 8000)

        Returns:
            Extracted data as dictionary conforming to schema

        Raises:
            ValueError: If model not loaded or extraction fails
            ConnectionError: If LM Studio is not accessible
        """
        if not self._loaded:
            raise ValueError("Model not loaded. Call load() first.")

        # Load config for defaults
        config = load_config()

        # Use config defaults if not explicitly provided
        if temperature is None:
            temperature = config["inference"]["default_temperature"]
        if max_tokens is None:
            max_tokens = config["inference"]["default_max_tokens"]

        # Construct prompt
        prompt = self._construct_prompt(schema, html)

        if self.verbose:
            print(f"\nSending request to LM Studio...")
            print(f"  - Temperature: {temperature}")
            print(f"  - Max tokens: {max_tokens}")
            print(f"  - Prompt length: {len(prompt)} chars")

        try:
            # Call LM Studio API (OpenAI-compatible)
            response = await self.client.chat.completions.create(
                model=self.model_name,  # Use model_name from config
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that extracts structured data from HTML."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=False
            )

            # Extract response text
            response_text = response.choices[0].message.content

            if self.verbose:
                print(f"\nReceived response ({len(response_text)} chars)")

            # Parse and return JSON
            return self._parse_response(response_text)

        except Exception as e:
            raise ConnectionError(
                f"Failed to get response from LM Studio. "
                f"Make sure the model is loaded in LM Studio. Error: {str(e)}"
            )


# Singleton instance for reuse
_global_model: Optional[SchematronModel] = None


def get_global_model(
    model_path: Optional[str] = None,
    api_base: Optional[str] = None,
    verbose: bool = False
) -> SchematronModel:
    """Get or create the global SchematronModel instance.

    Args:
        model_path: Path to model (only used on first call)
        api_base: LM Studio API base URL (only used on first call)
        verbose: Verbose output (only used on first call)

    Returns:
        SchematronModel instance
    """
    global _global_model
    if _global_model is None:
        _global_model = SchematronModel(model_path, api_base, verbose)
    return _global_model
