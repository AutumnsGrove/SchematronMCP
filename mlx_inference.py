"""
MLX Inference Module for Schematron

Handles loading and running the Schematron-3B model using MLX.
"""

import json
import os
import asyncio
from typing import Dict, Any, Optional
from functools import lru_cache

try:
    import mlx_lm
except ImportError:
    raise ImportError(
        "mlx_lm is required. Install with: pip install mlx-lm"
    )


class SchematronModel:
    """Wrapper for Schematron-3B model using MLX."""
    
    def __init__(
        self,
        model_path: Optional[str] = None,
        verbose: bool = False
    ):
        """Initialize SchematronModel.
        
        Args:
            model_path: Path to MLX model (default: from env or default path)
            verbose: Whether to print verbose output
        """
        self.model_path = model_path or os.getenv(
            "SCHEMATRON_MODEL_PATH",
            "mlx-community/Schematron-3B-4bit"
        )
        self.verbose = verbose
        self.model = None
        self.tokenizer = None
        self._loaded = False
    
    async def load(self) -> None:
        """Load the model and tokenizer asynchronously."""
        if self._loaded:
            return
        
        # Run blocking load in thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._load_sync)
        self._loaded = True
    
    def _load_sync(self) -> None:
        """Synchronous model loading."""
        if self.verbose:
            print(f"Loading Schematron model from: {self.model_path}")
        
        self.model, self.tokenizer = mlx_lm.load(
            self.model_path,
            tokenizer_config={"trust_remote_code": True}
        )
        
        if self.verbose:
            print("Model loaded successfully!")
    
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
        
        # Parse JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON response: {str(e)}\nResponse: {response[:200]}...")
    
    async def extract(
        self,
        html: str,
        schema: Dict[str, Any],
        temperature: float = 0.0,
        max_tokens: int = 8000
    ) -> Dict[str, Any]:
        """Extract structured data from HTML.
        
        Args:
            html: HTML content (should be cleaned)
            schema: JSON Schema defining output structure
            temperature: Generation temperature (0.0 for deterministic)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Extracted data as dictionary conforming to schema
            
        Raises:
            ValueError: If model not loaded or extraction fails
        """
        if not self._loaded:
            raise ValueError("Model not loaded. Call load() first.")
        
        # Construct prompt
        prompt = self._construct_prompt(schema, html)
        
        # Build messages for chat template
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": prompt}
        ]
        
        # Apply chat template
        prompt_text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        
        # Run generation in thread pool (blocking operation)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            self._generate_sync,
            prompt_text,
            temperature,
            max_tokens
        )
        
        # Parse and return JSON
        return self._parse_response(response)
    
    def _generate_sync(
        self,
        prompt: str,
        temperature: float,
        max_tokens: int
    ) -> str:
        """Synchronous generation call.
        
        Args:
            prompt: Formatted prompt text
            temperature: Generation temperature
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text
        """
        response = mlx_lm.generate(
            self.model,
            self.tokenizer,
            prompt=prompt,
            max_tokens=max_tokens,
            temp=temperature,
            verbose=self.verbose
        )
        
        return response


# Singleton instance for reuse
_global_model: Optional[SchematronModel] = None


def get_global_model(
    model_path: Optional[str] = None,
    verbose: bool = False
) -> SchematronModel:
    """Get or create the global SchematronModel instance.
    
    Args:
        model_path: Path to model (only used on first call)
        verbose: Verbose output (only used on first call)
        
    Returns:
        SchematronModel instance
    """
    global _global_model
    if _global_model is None:
        _global_model = SchematronModel(model_path, verbose)
    return _global_model
