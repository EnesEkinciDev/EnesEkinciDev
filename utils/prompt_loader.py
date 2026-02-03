"""Prompt loading and management utilities."""

import json
import os
from typing import Dict, Any
from pathlib import Path


class PromptLoader:
    """Loads and manages JSON prompt templates."""

    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize prompt loader.

        Args:
            prompts_dir: Directory containing JSON prompt files
        """
        self.prompts_dir = Path(prompts_dir)
        self.base_prompt = None
        self.category_prompts = {}
        self._load_prompts()

    def _load_prompts(self):
        """Load all prompt files from the prompts directory."""
        # Load base prompt
        base_path = self.prompts_dir / "base_prompt.json"
        if base_path.exists():
            with open(base_path, 'r', encoding='utf-8') as f:
                self.base_prompt = json.load(f)
        else:
            raise FileNotFoundError(f"Base prompt not found at {base_path}")

        # Load category-specific prompts
        for prompt_file in self.prompts_dir.glob("*_prompt.json"):
            if prompt_file.name != "base_prompt.json":
                category_name = prompt_file.stem.replace("_prompt", "")
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    self.category_prompts[category_name] = json.load(f)

    def get_category_list(self) -> list:
        """Get list of available categories."""
        return list(self.category_prompts.keys())

    def build_system_prompt(self, category: str) -> str:
        """
        Build comprehensive system prompt for a category.

        Args:
            category: Category name (e.g., 'wall_sign', 'wall_clock')

        Returns:
            Complete system prompt as string
        """
        if category not in self.category_prompts:
            raise ValueError(f"Category '{category}' not found. Available: {self.get_category_list()}")

        category_prompt = self.category_prompts[category]

        # Build comprehensive prompt
        system_prompt = f"""You are an expert Etsy listing generator specializing in {category_prompt['category']}.

# Your Role
{self.base_prompt['system_role']}

# Objective
{self.base_prompt['objective']}

# Category Information
- Category: {category_prompt['category']}
- Etsy Path: {category_prompt['etsy_taxonomy_path']}
- Description: {category_prompt['category_description']}

# Image Analysis Instructions

## General Analysis (from base prompt):
{json.dumps(self.base_prompt['image_analysis_instructions'], indent=2)}

## Category-Specific Analysis:
{json.dumps(category_prompt['image_analysis_specific'], indent=2)}

# Etsy 2025 Algorithm Understanding
{json.dumps(self.base_prompt['etsy_algorithm_2025'], indent=2)}

# Title Generation Rules

## Base Rules:
{json.dumps(self.base_prompt['title_generation_rules'], indent=2)}

## Category-Specific Title Rules:
{json.dumps(category_prompt['title_generation_category_specific'], indent=2)}

# Description Generation Rules

## Base Rules:
{json.dumps(self.base_prompt['description_generation_rules'], indent=2)}

## Category-Specific Description Rules:
{json.dumps(category_prompt['description_generation_category_specific'], indent=2)}

# Tags Generation Rules

## Base Rules:
{json.dumps(self.base_prompt['tags_generation_rules'], indent=2)}

## Category-Specific Tags:
{json.dumps(category_prompt['tags_generation_category_specific'], indent=2)}

# Attributes Generation Rules

## Base Rules:
{json.dumps(self.base_prompt['attributes_generation_rules'], indent=2)}

## Category-Specific Attributes:
{json.dumps(category_prompt['attributes_category_specific'], indent=2)}

# Alt Text Generation Rules
{json.dumps(self.base_prompt['alt_text_generation_rules'], indent=2)}

## Category-Specific Alt Text:
{json.dumps(category_prompt['alt_text_category_specific'], indent=2)}

# SEO Keywords Pool (Category-Specific)
{json.dumps(category_prompt.get('seo_keywords_pool', {}), indent=2)}

# Competitive Insights
{json.dumps(category_prompt.get('competitive_insights', {}), indent=2)}

# Output Format
You MUST respond with a valid JSON object with the following structure:
{{
  "title": "Generated title (140 chars max, 10-15 words)",
  "description": "Complete description (2000-3500 chars)",
  "tags": ["tag1", "tag2", ... (exactly 13 tags, each max 20 chars)"],
  "attributes": {{
    "Primary Color": "value",
    "Secondary Color": "value",
    "Material": "value",
    "Size": "value",
    "Style": "value",
    ...
  }},
  "alt_text": "Descriptive alt text (100-150 chars)",
  "category_path": "{category_prompt['etsy_taxonomy_path']}",
  "image_analysis_summary": "Brief summary of what you observed in the image",
  "seo_keywords_used": ["keyword1", "keyword2", ...],
  "optimization_notes": "Brief notes on optimization strategy used",
  "confidence_score": 0.95
}}

# Quality Checklist (Verify before output)
{json.dumps(self.base_prompt['quality_checklist'], indent=2)}

Remember: Analyze the image carefully, apply all rules, and generate a complete, SEO-optimized Etsy listing that follows all 2025 algorithm guidelines."""

        return system_prompt

    def build_user_prompt(self, category: str, additional_context: str = None) -> str:
        """
        Build user prompt for image analysis.

        Args:
            category: Category name
            additional_context: Optional additional user instructions

        Returns:
            User prompt string
        """
        category_display = self.category_prompts[category]['category']

        prompt = f"""Please analyze the uploaded product image and generate a complete Etsy listing for the {category_display} category.

Follow all the rules and guidelines provided in the system prompt. Pay special attention to:
1. Accurate image analysis (materials, colors, style, dimensions)
2. SEO-optimized title (front-loading important keywords)
3. Compelling description (storytelling + technical details)
4. Strategic tag selection (no overlap with title)
5. Complete attribute mapping
6. Conversion-focused copywriting

"""

        if additional_context:
            prompt += f"\nAdditional Context/Instructions:\n{additional_context}\n"

        prompt += "\nGenerate the listing now in valid JSON format."

        return prompt

    def get_category_display_name(self, category: str) -> str:
        """Get friendly display name for category."""
        if category in self.category_prompts:
            return self.category_prompts[category]['category']
        return category.replace('_', ' ').title()

    def get_example_output(self, category: str) -> Dict[str, Any]:
        """Get example output structure for a category."""
        if category in self.category_prompts:
            return self.category_prompts[category].get('output_example', {})
        return {}
