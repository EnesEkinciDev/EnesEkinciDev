# 🚀 Deployment Guide

## Vercel Deployment (Recommended)

### Prerequisites
- Vercel account (free at [vercel.com](https://vercel.com))
- Groq API key (free at [console.groq.com](https://console.groq.com/keys))

### Step-by-Step Deployment

#### 1. Prepare Repository
```bash
# Make sure all files are committed
git add .
git commit -m "Ready for Vercel deployment"
git push origin main
```

#### 2. Connect to Vercel

**Option A: Via Vercel CLI**
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel

# Follow prompts:
# - Link to existing project? No
# - Project name: etsy-listing-generator (or your choice)
# - Directory: ./
# - Override settings? No
```

**Option B: Via Vercel Dashboard**
1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure project:
   - Framework Preset: Other
   - Root Directory: ./
   - Build Command: (leave empty)
   - Output Directory: (leave empty)
4. Click "Deploy"

#### 3. Configure Environment Variables

After deployment, add your Groq API key:

1. Go to your project dashboard on Vercel
2. Navigate to **Settings** → **Environment Variables**
3. Add new variable:
   - **Name:** `GROQ_API_KEY`
   - **Value:** Your Groq API key from [console.groq.com/keys](https://console.groq.com/keys)
   - **Environments:** Production, Preview, Development
4. Click "Save"

#### 4. Redeploy

After adding the environment variable:
```bash
vercel --prod
```

Or trigger a redeploy from the Vercel dashboard.

#### 5. Access Your App

Your app will be available at:
```
https://your-project-name.vercel.app
```

### Vercel Configuration Details

The `vercel.json` file configures:
- **Python Runtime**: Uses @vercel/python builder
- **Memory**: 3008 MB (for image processing)
- **Timeout**: 300 seconds (for long API calls)
- **Environment**: Groq API key injection

### Troubleshooting Vercel

#### Build Fails
- Check `requirements.txt` has all dependencies
- Verify Python version in `runtime.txt` (3.11)
- Check build logs in Vercel dashboard

#### App Doesn't Start
- Ensure `GROQ_API_KEY` is set in environment variables
- Check function logs in Vercel dashboard
- Verify app.py has correct imports

#### Slow Response
- Normal: 5-15 seconds for first request (cold start)
- Subsequent requests: 30-60 seconds (Groq processing)
- Consider using 11B model for faster responses

#### Memory Issues
- Increase memory in vercel.json (max 3008 MB on free tier)
- Optimize image size before upload
- Use batch processing sparingly

---

## Alternative Deployment Options

### HuggingFace Spaces

1. Create new Space at [huggingface.co/new-space](https://huggingface.co/new-space)
2. Choose **Gradio** as SDK
3. Upload all files from repository
4. Add `GROQ_API_KEY` to Space secrets
5. Space will auto-deploy

**Files needed:**
- app.py
- requirements.txt
- prompts/ folder
- utils/ folder

### Render.com

1. Create new Web Service
2. Connect GitHub repository
3. Configure:
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
4. Add `GROQ_API_KEY` environment variable
5. Deploy

### Railway.app

1. Create new project from GitHub
2. Add service from repository
3. Configure:
   - Start Command: `python app.py`
   - Environment variable: `GROQ_API_KEY`
4. Deploy

### Google Cloud Run

```bash
# Build container
gcloud builds submit --tag gcr.io/PROJECT-ID/etsy-generator

# Deploy
gcloud run deploy etsy-generator \
  --image gcr.io/PROJECT-ID/etsy-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GROQ_API_KEY=your-key
```

---

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set API key
export GROQ_API_KEY='your-key-here'

# Run app
python app.py

# Access at http://localhost:7860
```

---

## Production Checklist

Before deploying to production:

- [ ] Groq API key is set as environment variable
- [ ] All dependencies in requirements.txt
- [ ] Error handling tested
- [ ] Image validation working
- [ ] JSON export functioning
- [ ] Batch processing tested
- [ ] Mobile responsive (Gradio handles this)
- [ ] Loading states visible
- [ ] Clear error messages

---

## Cost & Performance

### Groq (FREE)
- ✅ **Cost**: $0/month (completely free)
- ⚡ **Speed**: 10-20x faster than traditional LLMs
- 🎯 **Rate Limits**: Generous free tier
- 📊 **Quality**: Excellent (Llama 3.2 Vision 90B)

### Vercel (FREE Tier)
- ✅ **Hosting**: Free for hobby projects
- 💾 **Bandwidth**: 100GB/month
- ⏱️ **Function Duration**: 10 seconds (hobby), 60 seconds (pro)
- 🔄 **Builds**: Unlimited

**Note:** For production with high traffic, consider upgrading to Vercel Pro ($20/month) for:
- Extended function duration (300s)
- More memory (3008 MB)
- Priority support

---

## Monitoring & Analytics

### Vercel Analytics
Enable in project settings for:
- Page views
- Response times
- Error rates

### Groq Dashboard
Monitor at [console.groq.com](https://console.groq.com):
- API usage
- Token consumption
- Request rates

---

## Support

- **Vercel Issues**: [vercel.com/support](https://vercel.com/support)
- **Groq Support**: [console.groq.com/support](https://console.groq.com/support)
- **Project Issues**: Open GitHub issue

---

**Happy Deploying! 🚀**
