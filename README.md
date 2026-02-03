# Etsy Listing Generator 🎨

AI-powered Etsy listing generator using advanced image analysis and Etsy's 2025 algorithm best practices.

## ✨ Features

### Core Capabilities
- 🖼️ **Image Analysis** - Advanced vision AI analyzes product photos for materials, colors, style, and dimensions
- 📝 **SEO-Optimized Content** - Generates titles, descriptions, tags following Etsy 2025 algorithm
- 🏷️ **Smart Tagging** - 13 strategic tags with long-tail keywords and zero title overlap
- ⚙️ **Attribute Mapping** - Automatic category-specific attribute suggestions
- 🎯 **Conversion-Focused** - Copywriting optimized for Listing Quality Score (LQS)

### Advanced Features
- 🔄 **Multiple Variations** - Generate 2-5 different listing versions to compare
- 📦 **Batch Processing** - Process multiple images at once
- 💾 **JSON Export** - Download complete listing data
- 📋 **Copy to Clipboard** - Quick copy for each field
- 🎨 **Modern UI** - Clean, intuitive Gradio interface

## 📂 Categories Supported

- 🪧 **Wall Sign** - Decorative signs, motivational quotes, custom name signs
- 🕐 **Wall Clock** - Decorative timepieces, rustic clocks, modern wall clocks

*More categories coming soon!*

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/settings/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/EnesEkinciDev/EnesEkinciDev.git
   cd EnesEkinciDev
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   ```bash
   # Copy example env file
   cp .env.example .env

   # Edit .env and add your Anthropic API key
   # ANTHROPIC_API_KEY=your_api_key_here
   ```

   Or set it directly in your environment:
   ```bash
   export ANTHROPIC_API_KEY='your_api_key_here'
   ```

4. **Run the app**
   ```bash
   python app.py
   ```

5. **Open in browser**
   - Navigate to `http://localhost:7860`
   - Start generating listings!

## 📖 Usage Guide

### Single Listing Generation

1. **Upload Image** - Drag & drop or browse for your product image (min 2000px recommended)
2. **Select Category** - Choose Wall Sign or Wall Clock
3. **Add Context** (Optional) - Provide additional details like "personalized" or "reclaimed wood"
4. **Adjust Creativity** - Slider for temperature (higher = more creative)
5. **Generate** - Click "Generate Listing" and wait 30-60 seconds
6. **Review & Export** - Copy fields or download JSON

### Generate Variations

1. Upload image and select category
2. Choose number of variations (2-5)
3. Generate to see multiple approaches
4. Compare variations side-by-side
5. Pick the best one or mix elements from different versions

### Batch Processing

1. Upload multiple images at once
2. Select category for each (or apply same to all)
3. Process batch - generates listings for all images
4. Download complete batch as JSON

## 🏗️ Project Structure

```
EnesEkinciDev/
├── app.py                      # Main Gradio application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
├── README.md                  # This file
├── prompts/                   # JSON prompt templates
│   ├── base_prompt.json       # Core Etsy algorithm rules
│   ├── wall_sign_prompt.json  # Wall Sign specific rules
│   └── wall_clock_prompt.json # Wall Clock specific rules
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── prompt_loader.py       # Prompt management
│   └── claude_client.py       # Claude API integration
└── docs/                      # Etsy documentation PDFs
    └── *.pdf                  # Algorithm & SEO research
```

## 🎯 Etsy 2025 Algorithm Optimization

This tool is built on comprehensive research of Etsy's 2025 search algorithm:

### Ranking Factors Implemented
- ✅ **Listing Quality Score (LQS)** - Optimized for conversion rate, CTR, favorites
- ✅ **Query Matching** - Semantic keyword strategy with long-tail variants
- ✅ **Mobile-First** - Front-loading keywords for mobile visibility
- ✅ **Shipping Cost Factor** - Guidance for <$6 threshold
- ✅ **Context Specific Ranking (CSR)** - Personalization awareness

### Title Optimization
- 10-15 words (140 char max)
- First 40 characters critical for mobile
- Front-loading high-value keywords
- Natural readability (no keyword stuffing)
- No title-tag overlap

### Tag Strategy
- 13 unique long-tail keywords
- No repetition from title
- Multi-word phrases for specificity
- Semantic variations included
- 20 character limit per tag

### Description Best Practices
- 2000-3500 characters optimal
- Storytelling + technical details
- SEO keyword density 2-3%
- Structured with clear sections
- Conversion-focused copywriting

## 🛠️ Configuration

### Environment Variables

```bash
# Required
ANTHROPIC_API_KEY=your_api_key_here

# Optional
CLAUDE_MODEL=claude-sonnet-4-20250514  # Default model
GRADIO_SERVER_PORT=7860                # Default port
GRADIO_SHARE=False                     # Public URL sharing
```

### Customization

- **Add Categories**: Create new `{category}_prompt.json` in `prompts/` folder
- **Modify Rules**: Edit JSON prompts to adjust generation strategy
- **Change Model**: Update `CLAUDE_MODEL` in `.env`

## 📊 API Usage & Costs

- **Model**: Claude Sonnet 4 (Vision + Text)
- **Average Tokens**: 3,000-5,000 per listing
- **Estimated Cost**: ~$0.05-0.10 per listing
- **Processing Time**: 30-60 seconds per image

💡 **Tip**: Use variations sparingly - each variation is a separate API call

## 🐛 Troubleshooting

### "API key not found"
- Ensure `ANTHROPIC_API_KEY` is set in `.env` or environment
- Check API key is valid at [Anthropic Console](https://console.anthropic.com)

### "Invalid image"
- Image must be <5MB
- Minimum 500px (2000px recommended)
- Supported formats: JPG, PNG, GIF, WebP

### "JSON parsing error"
- Rare Claude API response format issue
- Try regenerating with lower temperature
- Check raw response in JSON output accordion

### Slow generation
- Normal: 30-60 seconds per image
- Check internet connection
- Verify API key has sufficient credits

## 📚 Documentation

Detailed Etsy algorithm research and documentation are stored in `docs/` folder:
- Search optimization strategies
- Title & SEO best practices
- Conversion rate optimization
- 2025 algorithm updates

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- [ ] Add more product categories
- [ ] Implement A/B testing comparison
- [ ] Add bulk CSV export
- [ ] Category auto-detection from image
- [ ] Multi-language support
- [ ] Integration with Etsy API for direct upload

## 📝 License

MIT License - Feel free to use for commercial purposes

## 🙏 Acknowledgments

- Built with [Anthropic Claude](https://anthropic.com) vision models
- UI powered by [Gradio](https://gradio.app)
- Research based on official Etsy seller documentation

## 📧 Contact

For questions or support, open an issue on GitHub.

---

**Made with ❤️ for Etsy sellers**
