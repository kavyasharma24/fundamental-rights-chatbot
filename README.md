

# 📚 Fundamental Rights Chatbot - Deployment Guide

A RAG-based chatbot that answers questions about Part III of the Indian Constitution (Fundamental Rights).

## 🚀 Quick Deploy to Hugging Face Spaces

### Method 1: Using Web Interface (Easiest)

1. **Go to Hugging Face Spaces**: https://huggingface.co/spaces
2. **Create new Space**:
   - Click "Create new Space"
   - Name: `fundamental-rights-chatbot` (or your choice)
   - SDK: Select **Gradio**
   - Visibility: Public or Private
   - Click "Create Space"

3. **Upload files**:
   - Go to "Files" tab in your Space
   - Upload these 3 files:
     - `app.py` ✓
     - `requirements.txt` ✓
     - `part3.pdf` ✓ (your Constitution PDF - rename it to exactly `part3.pdf`)

4. **Wait for build**: 
   - Check "Logs" tab to see build progress (takes 5-10 minutes)
   - Once complete, your app will be live!

### Method 2: Using Git (Advanced)

```bash
# Clone your Space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# Copy files
cp app.py requirements.txt part3.pdf ./

# Commit and push
git add .
git commit -m "Initial deployment"
git push
```

---

## 🌐 Alternative Deployment Options

### Option 2: Deploy on Railway.app

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Connect your GitHub repo with these files
4. Railway will auto-detect and deploy

**Add `Procfile`:**
```
web: python app.py
```

### Option 3: Deploy on Render.com

1. Go to https://render.com
2. Create "New Web Service"
3. Connect GitHub repository
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `python app.py`

### Option 4: Deploy on Google Cloud Run

```bash
# Create Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]

# Deploy
gcloud run deploy fundamental-rights-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 5: Deploy on AWS (EC2)

```bash
# SSH into EC2 instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install dependencies
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt

# Run in background
nohup python3 app.py &
```

---

## 📊 Deployment Comparison

| Platform | Difficulty | Cost | Best For |
|----------|-----------|------|----------|
| **Hugging Face Spaces** | ⭐ Easy | Free | Quick demos, sharing |
| Railway.app | ⭐⭐ Medium | $5/mo free tier | Production apps |
| Render.com | ⭐⭐ Medium | Free tier available | Small projects |
| Google Cloud Run | ⭐⭐⭐ Hard | Pay per use | Scalable apps |
| AWS EC2 | ⭐⭐⭐⭐ Expert | ~$10/mo | Full control |

---

## ⚙️ Configuration Tips

### For Better Performance:

1. **Upgrade model** in `app.py`:
```python
model="google/flan-t5-xl"  # Even better than large
```

2. **Use GPU** (Hugging Face Spaces):
   - Settings → Hardware → Select GPU (requires paid plan)

3. **Increase token limit**:
```python
max_new_tokens=1024  # Longer answers
```

### For Production:

1. **Add authentication** (Gradio built-in):
```python
interface.launch(auth=("username", "password"))
```

2. **Enable analytics**:
```python
interface.launch(analytics_enabled=True)
```

3. **Add rate limiting** to prevent abuse

---

## 🐛 Troubleshooting

### Build fails on Hugging Face:
- Check "Logs" tab for errors
- Ensure `part3.pdf` is uploaded
- Verify all dependencies in `requirements.txt`

### App runs but gives errors:
- Check PDF file name is exactly `part3.pdf`
- Ensure PDF is in same directory as `app.py`

### Slow responses:
- Upgrade to GPU hardware
- Use smaller model: `flan-t5-base`
- Reduce `max_new_tokens`

### Out of memory:
- Reduce `chunk_size` to 400
- Reduce `k` (retrieval chunks) to 2
- Use `flan-t5-base` instead of `flan-t5-large`

---

## 📝 Files Needed

✅ `app.py` - Main application code
✅ `requirements.txt` - Python dependencies  
✅ `part3.pdf` - Your Constitution PDF document
✅ `README.md` - This file (optional)

---

## 🎯 Next Steps After Deployment

1. **Test thoroughly** with various questions
2. **Share the link** with users
3. **Monitor usage** and errors
4. **Iterate and improve** based on feedback

---

## 💡 Tips for Success

- **Start with Hugging Face Spaces** - it's the easiest
- **Test locally first** before deploying
- **Monitor the build logs** carefully
- **Keep your PDF file small** (under 10MB ideally)

---

## 📧 Need Help?

- Hugging Face Discord: https://discord.gg/hugging-face
- Gradio Documentation: https://gradio.app/docs
- LangChain Docs: https://python.langchain.com

---

**Ready to deploy? Start with Hugging Face Spaces - it takes just 5 minutes!** 🚀
