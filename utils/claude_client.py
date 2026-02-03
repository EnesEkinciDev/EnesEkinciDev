"""Claude API client for generating Etsy listings."""

import os
import json
import base64
from typing import Dict, Any, Optional, List
from pathlib import Path
import anthropic
from PIL import Image
import io


class ClaudeClient:
    """Client for interacting with Claude API for listing generation."""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client.

        Args:
            api_key: Anthropic API key. If not provided, reads from ANTHROPIC_API_KEY env var
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key not found. Set ANTHROPIC_API_KEY environment variable or pass api_key parameter."
            )

        self.client = anthropic.Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"  # Latest Sonnet model with vision

    def _encode_image(self, image_path: str) -> tuple[str, str]:
        """
        Encode image to base64 and determine media type.

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (base64_data, media_type)
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

        return image_data, media_type

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
                # Check size (Claude supports up to 5MB per image)
                file_size = Path(image_path).stat().st_size
                if file_size > 5 * 1024 * 1024:  # 5MB
                    return False

                # Check dimensions (recommended minimum for Etsy: 2000px)
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
        max_tokens: int = 4096,
        temperature: float = 1.0
    ) -> Dict[str, Any]:
        """
        Generate Etsy listing from product image.

        Args:
            image_path: Path to product image
            system_prompt: System prompt with all rules and guidelines
            user_prompt: User prompt with specific instructions
            max_tokens: Maximum tokens for response
            temperature: Temperature for generation (0.0-1.0)

        Returns:
            Generated listing as dictionary

        Raises:
            ValueError: If image is invalid
            Exception: If API call fails
        """
        # Validate image
        if not self._validate_image(image_path):
            raise ValueError(f"Invalid image: {image_path}. Must be <5MB and at least 500px.")

        # Encode image
        image_data, media_type = self._encode_image(image_path)

        # Build message with vision
        message = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type,
                                "data": image_data
                            }
                        },
                        {
                            "type": "text",
                            "text": user_prompt
                        }
                    ]
                }
            ]
        )

        # Extract response
        response_text = message.content[0].text

        # Parse JSON response
        try:
            # Try to find JSON in response (in case there's extra text)
            start_idx = response_text.find('{')
            end_idx = response_text.rfind('}') + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                listing_data = json.loads(json_str)
            else:
                # No JSON found, try parsing entire response
                listing_data = json.loads(response_text)

            # Add metadata
            listing_data['_metadata'] = {
                'model': self.model,
                'tokens_used': message.usage.input_tokens + message.usage.output_tokens,
                'input_tokens': message.usage.input_tokens,
                'output_tokens': message.usage.output_tokens
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
                    temperature=min(temperature + (i * 0.1), 1.0)  # Slightly increase temp for variations
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
