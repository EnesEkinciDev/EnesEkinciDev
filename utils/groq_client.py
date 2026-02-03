"""Groq API client for generating Etsy listings with Llama 3.2 Vision."""

import os
import json
import base64
from typing import Dict, Any, Optional, List
from pathlib import Path
from groq import Groq
from PIL import Image


class GroqClient:
    """Client for interacting with Groq API using Llama 3.2 Vision for listing generation."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client.

        Args:
            api_key: Groq API key. If not provided, reads from GROQ_API_KEY env var
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not found. Set GROQ_API_KEY environment variable or pass api_key parameter."
            )

        self.client = Groq(api_key=self.api_key)
        # Use Llama 3.2 90B Vision for best quality
        self.model = "llama-3.2-90b-vision-preview"

    def _encode_image_to_data_url(self, image_path: str) -> str:
        """
        Encode image to data URL format for Groq API.

        Args:
            image_path: Path to image file

        Returns:
            Data URL string (data:image/jpeg;base64,...)
        """
        image_path = Path(image_path)

        # Determine media type
        ext = image_path.suffix.lower()
        media_type_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        media_type = media_type_map.get(ext, 'image/jpeg')

        # Read and encode image
        with open(image_path, 'rb') as f:
            image_data = base64.standard_b64encode(f.read()).decode('utf-8')

        return f"data:{media_type};base64,{image_data}"

    def _validate_image(self, image_path: str) -> bool:
        """
        Validate image file.

        Args:
            image_path: Path to image file

        Returns:
            True if valid, False otherwise
        """
        try:
            with Image.open(image_path) as img:
                # Check size (Groq supports up to 4MB per image recommended)
                file_size = Path(image_path).stat().st_size
                if file_size > 4 * 1024 * 1024:  # 4MB
                    return False

                # Check dimensions
                width, height = img.size
                if min(width, height) < 500:  # Minimum for reasonable analysis
                    return False

                return True
        except Exception:
            return False

    def generate_listing(
        self,
        image_path: str,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 8192,
        temperature: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate Etsy listing from product image using Groq.

        Args:
            image_path: Path to product image
            system_prompt: System prompt with all rules and guidelines
            user_prompt: User prompt with specific instructions
            max_tokens: Maximum tokens for response
            temperature: Temperature for generation (0.0-2.0 for Groq)

        Returns:
            Generated listing as dictionary

        Raises:
            ValueError: If image is invalid
            Exception: If API call fails
        """
        # Validate image
        if not self._validate_image(image_path):
            raise ValueError(f"Invalid image: {image_path}. Must be <4MB and at least 500px.")

        # Encode image to data URL
        image_data_url = self._encode_image_to_data_url(image_path)

        # Build messages for Groq vision API
        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_data_url
                        }
                    },
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }
        ]

        # Call Groq API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            response_format={"type": "json_object"}  # Force JSON output
        )

        # Extract response
        response_text = response.choices[0].message.content

        # Parse JSON response
        try:
            listing_data = json.loads(response_text)

            # Add metadata
            listing_data['_metadata'] = {
                'model': self.model,
                'provider': 'Groq',
                'tokens_used': response.usage.total_tokens if hasattr(response, 'usage') else 0,
                'prompt_tokens': response.usage.prompt_tokens if hasattr(response, 'usage') else 0,
                'completion_tokens': response.usage.completion_tokens if hasattr(response, 'usage') else 0,
                'finish_reason': response.choices[0].finish_reason
            }

            return listing_data

        except json.JSONDecodeError as e:
            # If JSON parsing fails, return raw response with error
            return {
                'error': 'Failed to parse JSON response',
                'raw_response': response_text,
                'parse_error': str(e)
            }

    def generate_variations(
        self,
        image_path: str,
        system_prompt: str,
        user_prompt: str,
        num_variations: int = 3,
        temperature: float = 1.0
    ) -> List[Dict[str, Any]]:
        """
        Generate multiple listing variations.

        Args:
            image_path: Path to product image
            system_prompt: System prompt with rules
            user_prompt: User prompt
            num_variations: Number of variations to generate
            temperature: Temperature for generation

        Returns:
            List of generated listings
        """
        variations = []

        for i in range(num_variations):
            try:
                # Add variation instruction to user prompt
                varied_prompt = f"{user_prompt}\n\n(Variation {i+1}/{num_variations}: Generate a unique listing with different keyword focus and tone.)"

                listing = self.generate_listing(
                    image_path=image_path,
                    system_prompt=system_prompt,
                    user_prompt=varied_prompt,
                    temperature=min(temperature + (i * 0.2), 2.0)  # Groq supports up to 2.0
                )

                listing['variation_number'] = i + 1
                variations.append(listing)

            except Exception as e:
                variations.append({
                    'error': f'Failed to generate variation {i+1}',
                    'exception': str(e),
                    'variation_number': i + 1
                })

        return variations

    def batch_generate(
        self,
        image_paths: List[str],
        system_prompts: List[str],
        user_prompts: List[str],
        progress_callback: Optional[callable] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate listings for multiple images in batch.

        Args:
            image_paths: List of image paths
            system_prompts: List of system prompts (one per image)
            user_prompts: List of user prompts (one per image)
            progress_callback: Optional callback function(current, total, status)

        Returns:
            List of generated listings (same order as input)
        """
        results = []
        total = len(image_paths)

        for idx, (img_path, sys_prompt, usr_prompt) in enumerate(zip(image_paths, system_prompts, user_prompts)):
            if progress_callback:
                progress_callback(idx + 1, total, f"Processing image {idx + 1}/{total}")

            try:
                listing = self.generate_listing(
                    image_path=img_path,
                    system_prompt=sys_prompt,
                    user_prompt=usr_prompt
                )
                listing['batch_index'] = idx
                listing['image_path'] = img_path
                results.append(listing)

            except Exception as e:
                results.append({
                    'error': f'Failed to process image {idx + 1}',
                    'exception': str(e),
                    'batch_index': idx,
                    'image_path': img_path
                })

        if progress_callback:
            progress_callback(total, total, "Batch processing complete")

        return results

    def get_available_models(self) -> List[str]:
        """Get list of available Groq vision models."""
        return [
            "llama-3.2-90b-vision-preview",  # Best quality
            "llama-3.2-11b-vision-preview",  # Faster, smaller
        ]

    def set_model(self, model: str):
        """
        Change the model used for generation.

        Args:
            model: Model name from get_available_models()
        """
        available = self.get_available_models()
        if model not in available:
            raise ValueError(f"Model {model} not available. Choose from: {available}")
        self.model = model
