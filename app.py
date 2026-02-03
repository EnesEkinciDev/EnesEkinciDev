"""
Etsy Listing Generator - Advanced Gradio App
AI-powered Etsy listing generation with image analysis
"""

import gradio as gr
import json
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
import traceback

from utils.prompt_loader import PromptLoader
from utils.claude_client import ClaudeClient


# Initialize components
try:
    prompt_loader = PromptLoader()
    claude_client = ClaudeClient()
    CATEGORIES = prompt_loader.get_category_list()
    CATEGORY_DISPLAY = {cat: prompt_loader.get_category_display_name(cat) for cat in CATEGORIES}
except Exception as e:
    print(f"⚠️  Initialization error: {e}")
    CATEGORIES = ["wall_sign", "wall_clock"]
    CATEGORY_DISPLAY = {"wall_sign": "Wall Sign", "wall_clock": "Wall Clock"}


def format_listing_display(listing: Dict[str, Any]) -> str:
    """Format listing data for display in UI."""
    if 'error' in listing:
        return f"❌ **Error:** {listing['error']}\n\n```\n{listing.get('raw_response', 'No details available')}\n```"

    output = "# 📋 Generated Etsy Listing\n\n"

    # Title
    output += f"## 📝 Title\n`{listing.get('title', 'N/A')}`\n\n"

    # Tags
    tags = listing.get('tags', [])
    output += f"## 🏷️ Tags ({len(tags)}/13)\n"
    output += " · ".join([f"`{tag}`" for tag in tags]) + "\n\n"

    # Description
    description = listing.get('description', 'N/A')
    output += f"## 📄 Description ({len(description)} chars)\n"
    output += f"{description}\n\n"

    # Attributes
    attributes = listing.get('attributes', {})
    output += f"## ⚙️ Attributes\n"
    for key, value in attributes.items():
        output += f"- **{key}:** {value}\n"
    output += "\n"

    # Alt Text
    alt_text = listing.get('alt_text', 'N/A')
    output += f"## 🖼️ Alt Text\n`{alt_text}`\n\n"

    # SEO Keywords
    seo_keywords = listing.get('seo_keywords_used', [])
    if seo_keywords:
        output += f"## 🔍 SEO Keywords Used\n"
        output += " · ".join([f"`{kw}`" for kw in seo_keywords]) + "\n\n"

    # Image Analysis Summary
    analysis = listing.get('image_analysis_summary', '')
    if analysis:
        output += f"## 👁️ Image Analysis\n{analysis}\n\n"

    # Optimization Notes
    notes = listing.get('optimization_notes', '')
    if notes:
        output += f"## 💡 Optimization Notes\n{notes}\n\n"

    # Metadata
    metadata = listing.get('_metadata', {})
    if metadata:
        output += f"## 📊 Generation Stats\n"
        output += f"- Model: `{metadata.get('model', 'N/A')}`\n"
        output += f"- Tokens: {metadata.get('tokens_used', 'N/A'):,}\n"
        confidence = listing.get('confidence_score', 0)
        output += f"- Confidence: {confidence:.1%}\n"

    return output


def generate_single_listing(
    image,
    category: str,
    additional_context: str,
    temperature: float,
    progress=gr.Progress()
) -> tuple[str, str, str]:
    """Generate listing for a single image."""
    try:
        if image is None:
            return "❌ Please upload an image", "", ""

        progress(0.1, desc="Loading prompts...")

        # Build prompts
        system_prompt = prompt_loader.build_system_prompt(category)
        user_prompt = prompt_loader.build_user_prompt(category, additional_context)

        progress(0.3, desc="Analyzing image with Claude...")

        # Generate listing
        listing = claude_client.generate_listing(
            image_path=image,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature
        )

        progress(1.0, desc="Complete!")

        # Format outputs
        display_text = format_listing_display(listing)
        json_output = json.dumps(listing, indent=2, ensure_ascii=False)

        # Create download-ready JSON
        download_json = json.dumps(listing, indent=2, ensure_ascii=False)

        return display_text, json_output, download_json

    except Exception as e:
        error_msg = f"❌ **Generation Failed**\n\n```\n{str(e)}\n\n{traceback.format_exc()}\n```"
        return error_msg, "", ""


def generate_variations(
    image,
    category: str,
    num_variations: int,
    additional_context: str,
    temperature: float,
    progress=gr.Progress()
) -> tuple[str, str, str, str, str]:
    """Generate multiple variations of a listing."""
    try:
        if image is None:
            return "❌ Please upload an image", "", "", "", ""

        progress(0.1, desc="Loading prompts...")

        # Build prompts
        system_prompt = prompt_loader.build_system_prompt(category)
        user_prompt = prompt_loader.build_user_prompt(category, additional_context)

        progress(0.2, desc=f"Generating {num_variations} variations...")

        # Generate variations
        variations = claude_client.generate_variations(
            image_path=image,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            num_variations=num_variations,
            temperature=temperature
        )

        progress(1.0, desc="Complete!")

        # Format outputs for each variation
        outputs = []
        for i, listing in enumerate(variations):
            display_text = f"# Variation {i+1}\n\n" + format_listing_display(listing)
            outputs.append(display_text)

        # Pad outputs to 5 (max variations)
        while len(outputs) < 5:
            outputs.append("")

        # JSON output of all variations
        json_output = json.dumps(variations, indent=2, ensure_ascii=False)

        return tuple(outputs[:5])

    except Exception as e:
        error_msg = f"❌ **Generation Failed**\n\n```\n{str(e)}\n\n{traceback.format_exc()}\n```"
        return error_msg, "", "", "", ""


def batch_generate_listings(
    images: List,
    categories: List[str],
    additional_context: str,
    temperature: float,
    progress=gr.Progress()
) -> tuple[str, str]:
    """Generate listings for multiple images in batch."""
    try:
        if not images or len(images) == 0:
            return "❌ Please upload at least one image", ""

        num_images = len(images)
        progress(0.0, desc=f"Processing {num_images} images...")

        # Prepare prompts for each image
        system_prompts = []
        user_prompts = []

        for i, (image, category) in enumerate(zip(images, categories)):
            system_prompt = prompt_loader.build_system_prompt(category)
            user_prompt = prompt_loader.build_user_prompt(category, additional_context)
            system_prompts.append(system_prompt)
            user_prompts.append(user_prompt)

        # Progress callback
        def progress_callback(current, total, status):
            progress(current / total, desc=status)

        # Batch generate
        results = claude_client.batch_generate(
            image_paths=images,
            system_prompts=system_prompts,
            user_prompts=user_prompts,
            progress_callback=progress_callback
        )

        # Format results
        output_text = f"# 📦 Batch Results ({len(results)} listings)\n\n"
        output_text += "---\n\n"

        for i, listing in enumerate(results):
            output_text += f"## Image {i+1} - {CATEGORY_DISPLAY.get(categories[i], categories[i])}\n\n"
            output_text += format_listing_display(listing)
            output_text += "\n---\n\n"

        json_output = json.dumps(results, indent=2, ensure_ascii=False)

        return output_text, json_output

    except Exception as e:
        error_msg = f"❌ **Batch Generation Failed**\n\n```\n{str(e)}\n\n{traceback.format_exc()}\n```"
        return error_msg, ""


# Build Gradio Interface
with gr.Blocks(
    theme=gr.themes.Soft(primary_hue="blue", secondary_hue="purple"),
    title="Etsy Listing Generator",
    css="""
    .output-markdown {font-family: 'Inter', sans-serif; line-height: 1.6;}
    .json-output {font-family: 'Fira Code', monospace; font-size: 0.9em;}
    """
) as demo:

    gr.Markdown(
        """
        # 🎨 Etsy Listing Generator
        ### AI-Powered Listing Creation with Image Analysis

        Upload your product images and let AI generate SEO-optimized Etsy listings following 2025 algorithm best practices.
        """
    )

    with gr.Tabs() as tabs:

        # ===== TAB 1: SINGLE LISTING =====
        with gr.Tab("🖼️ Single Listing"):
            gr.Markdown("Generate a complete Etsy listing from a single product image.")

            with gr.Row():
                with gr.Column(scale=1):
                    single_image = gr.Image(
                        type="filepath",
                        label="Upload Product Image",
                        height=400
                    )

                    single_category = gr.Dropdown(
                        choices=[CATEGORY_DISPLAY[cat] for cat in CATEGORIES],
                        value=CATEGORY_DISPLAY[CATEGORIES[0]],
                        label="Product Category",
                        info="Select the category that best matches your product"
                    )

                    single_context = gr.Textbox(
                        label="Additional Context (Optional)",
                        placeholder="E.g., 'This is personalized', 'Made from reclaimed wood', 'Available in 3 sizes'",
                        lines=3
                    )

                    single_temperature = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=1.0,
                        step=0.1,
                        label="Creativity (Temperature)",
                        info="Higher = more creative, Lower = more focused"
                    )

                    single_generate_btn = gr.Button(
                        "✨ Generate Listing",
                        variant="primary",
                        size="lg"
                    )

                with gr.Column(scale=2):
                    single_output = gr.Markdown(
                        label="Generated Listing",
                        elem_classes=["output-markdown"]
                    )

            with gr.Accordion("📥 JSON Output & Export", open=False):
                single_json = gr.Code(
                    label="JSON Output",
                    language="json",
                    elem_classes=["json-output"]
                )
                single_download = gr.File(label="Download JSON")

            # Single listing generation
            single_generate_btn.click(
                fn=lambda img, cat, ctx, temp: generate_single_listing(
                    img,
                    [k for k, v in CATEGORY_DISPLAY.items() if v == cat][0],
                    ctx,
                    temp
                ),
                inputs=[single_image, single_category, single_context, single_temperature],
                outputs=[single_output, single_json, single_download]
            )

        # ===== TAB 2: VARIATIONS =====
        with gr.Tab("🔄 Generate Variations"):
            gr.Markdown("Generate multiple listing variations to compare different approaches.")

            with gr.Row():
                with gr.Column(scale=1):
                    var_image = gr.Image(
                        type="filepath",
                        label="Upload Product Image",
                        height=400
                    )

                    var_category = gr.Dropdown(
                        choices=[CATEGORY_DISPLAY[cat] for cat in CATEGORIES],
                        value=CATEGORY_DISPLAY[CATEGORIES[0]],
                        label="Product Category"
                    )

                    var_num = gr.Slider(
                        minimum=2,
                        maximum=5,
                        value=3,
                        step=1,
                        label="Number of Variations",
                        info="How many different versions to generate"
                    )

                    var_context = gr.Textbox(
                        label="Additional Context (Optional)",
                        placeholder="Any specific requirements or details",
                        lines=2
                    )

                    var_temperature = gr.Slider(
                        minimum=0.5,
                        maximum=1.0,
                        value=1.0,
                        step=0.1,
                        label="Creativity"
                    )

                    var_generate_btn = gr.Button(
                        "🔄 Generate Variations",
                        variant="primary",
                        size="lg"
                    )

            with gr.Tabs() as var_tabs:
                var_outputs = []
                for i in range(5):
                    with gr.Tab(f"Variation {i+1}"):
                        var_out = gr.Markdown(elem_classes=["output-markdown"])
                        var_outputs.append(var_out)

            # Variation generation
            var_generate_btn.click(
                fn=lambda img, cat, num, ctx, temp: generate_variations(
                    img,
                    [k for k, v in CATEGORY_DISPLAY.items() if v == cat][0],
                    int(num),
                    ctx,
                    temp
                ),
                inputs=[var_image, var_category, var_num, var_context, var_temperature],
                outputs=var_outputs
            )

        # ===== TAB 3: BATCH PROCESSING =====
        with gr.Tab("📦 Batch Processing"):
            gr.Markdown("Process multiple images at once and generate listings in bulk.")

            with gr.Row():
                with gr.Column(scale=1):
                    batch_images = gr.File(
                        file_count="multiple",
                        type="filepath",
                        label="Upload Multiple Images",
                        file_types=["image"]
                    )

                    batch_categories = gr.CheckboxGroup(
                        choices=[CATEGORY_DISPLAY[cat] for cat in CATEGORIES],
                        label="Categories (Select for Each Image)",
                        info="Select categories in the same order as images"
                    )

                    batch_context = gr.Textbox(
                        label="Context for All Images (Optional)",
                        lines=2
                    )

                    batch_temperature = gr.Slider(
                        minimum=0.0,
                        maximum=1.0,
                        value=1.0,
                        step=0.1,
                        label="Creativity"
                    )

                    batch_generate_btn = gr.Button(
                        "📦 Process Batch",
                        variant="primary",
                        size="lg"
                    )

                with gr.Column(scale=2):
                    batch_output = gr.Markdown(elem_classes=["output-markdown"])

            with gr.Accordion("📥 Batch JSON Output", open=False):
                batch_json = gr.Code(language="json", elem_classes=["json-output"])

            # Batch processing
            batch_generate_btn.click(
                fn=lambda imgs, cats, ctx, temp: batch_generate_listings(
                    imgs,
                    [[k for k, v in CATEGORY_DISPLAY.items() if v == c][0] for c in cats] if cats else [CATEGORIES[0]] * len(imgs),
                    ctx,
                    temp
                ) if imgs else ("❌ Please upload images", ""),
                inputs=[batch_images, batch_categories, batch_context, batch_temperature],
                outputs=[batch_output, batch_json]
            )

    # Footer
    gr.Markdown(
        """
        ---
        ### 💡 Tips for Best Results
        - Upload high-quality images (minimum 2000px recommended)
        - Select the correct category
        - Provide additional context for personalized or unique items
        - Try generating variations to find the best listing approach
        - Review and adjust generated content before publishing

        ### 🔒 Privacy
        - Images are processed securely via Claude API
        - No data is stored permanently
        - API keys are required (set `ANTHROPIC_API_KEY` environment variable)
        """
    )


if __name__ == "__main__":
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  WARNING: ANTHROPIC_API_KEY not found in environment variables!")
        print("   Set it before running: export ANTHROPIC_API_KEY='your-key-here'")
        print("   Or create a .env file with: ANTHROPIC_API_KEY=your-key-here")

    # Launch app
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True
    )
