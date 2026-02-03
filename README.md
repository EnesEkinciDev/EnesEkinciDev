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
- Groq API key - **100% FREE!** ([Get one here](https://console.groq.com/keys))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/EnesEkinciDev/Etsy-listing-generator.git
   cd Etsy-listing-generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API key**
   ```bash
   # Copy example env file
   cp .env.example .env

   # Edit .env and add your Groq API key
   # GROQ_API_KEY=your_api_key_here
   ```

   Or set it directly in your environment:
   ```bash
   export GROQ_API_KEY='your_api_key_here'
   ```

   **Get your FREE Groq API key:** [console.groq.com/keys](https://console.groq.com/keys)

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
Etsy-listing-generator/
├── app.py                      # Main Gradio application
├── requirements.txt            # Python dependencies
├── .env.example               # Environment configuration template
├── .env                       # Your API keys (not in git)
├── README.md                  # This file
├── DEPLOYMENT.md              # Deployment guide
├── vercel.json                # Vercel configuration
├── runtime.txt                # Python version
├── prompts/                   # JSON prompt templates
│   ├── base_prompt.json       # Core Etsy algorithm rules
│   ├── wall_sign_prompt.json  # Wall Sign specific rules
│   └── wall_clock_prompt.json # Wall Clock specific rules
├── utils/                     # Utility modules
│   ├── __init__.py
│   ├── prompt_loader.py       # Prompt management
│   ├── groq_client.py         # Groq API integration
│   └── claude_client.py       # Claude API (legacy)
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
GROQ_API_KEY=your_groq_api_key_here

# Optional
GROQ_MODEL=llama-3.2-90b-vision-preview  # Default (best quality)
# GROQ_MODEL=llama-3.2-11b-vision-preview  # Faster alternative
GRADIO_SERVER_PORT=7860                  # Default port
GRADIO_SHARE=False                       # Public URL sharing
```

### Customization

- **Add Categories**: Create new `{category}_prompt.json` in `prompts/` folder
- **Modify Rules**: Edit JSON prompts to adjust generation strategy
- **Change Model**: Update `CLAUDE_MODEL` in `.env`

## 📊 API Usage & Performance

### Groq (Llama 3.2 Vision 90B)
- **Model**: Llama 3.2 Vision 90B - Open source, state-of-the-art
- **Cost**: **$0.00** - Completely FREE! 🎉
- **Speed**: ⚡ 10-20x faster than traditional LLMs (Groq's LPU technology)
- **Processing Time**: 5-15 seconds per image (vs 30-60s with Claude)
- **Rate Limits**: Generous free tier - perfect for production

### Why Groq?
- ✅ **Zero Cost** - No credit card required, no usage fees
- ✅ **Lightning Fast** - Groq's LPU (Language Processing Unit) delivers unmatched speed
- ✅ **High Quality** - Llama 3.2 Vision 90B rivals proprietary models
- ✅ **Scalable** - Handle multiple requests without cost concerns
- ✅ **Open Source** - Built on Meta's Llama 3.2

💡 **Tip**: Generate variations freely - no cost per API call!

## 🐛 Troubleshooting

### "API key not found"
- Ensure `GROQ_API_KEY` is set in `.env` or environment
- Get free API key at [Groq Console](https://console.groq.com/keys)
- Verify key is active in your Groq dashboard

### "Invalid image"
- Image must be <5MB
- Minimum 500px (2000px recommended)
- Supported formats: JPG, PNG, GIF, WebP

### "JSON parsing error"
- Rare Claude API response format issue
- Try regenerating with lower temperature
- Check raw response in JSON output accordion

### Slow generation
- Normal: 5-15 seconds per image with Groq
- If slower: Check internet connection
- Cold start may take 2-3 seconds on first request
- Consider switching to 11B model for even faster results

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

- Powered by [Groq](https://groq.com) ultra-fast LPU inference
- Vision AI: [Meta's Llama 3.2](https://ai.meta.com/llama/) 90B Vision model
- UI framework: [Gradio](https://gradio.app)
- Research based on official Etsy seller documentation

### Why This Stack?
This project demonstrates that **world-class AI applications can be built for $0**:
- ✅ Groq: Free, unlimited (fair use) API access
- ✅ Llama 3.2 Vision: Open-source, commercial-friendly
- ✅ Gradio: Free, easy deployment to multiple platforms
- ✅ Vercel: Free hosting for hobby projects

**Total Monthly Cost: $0** 🎉

## 📧 Contact

For questions or support, open an issue on GitHub.

---

**Made with ❤️ for Etsy sellers**
