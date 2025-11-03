# Deploying to Render

This guide will help you deploy the RAG Assistant to Render.

## Prerequisites

1. A [Render](https://render.com) account (free tier available)
2. Your Groq API key from https://console.groq.com
3. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)

## Step-by-Step Deployment

### 1. Push Your Code to Git

Make sure your code is committed and pushed to a Git repository:

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Deploy Using Render Dashboard

**Option A: Using render.yaml (Recommended)**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your Git repository
4. Render will automatically detect `render.yaml` and configure the service
5. Add your `GROQ_API_KEY` environment variable (see below)

**Option B: Manual Setup**

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Web Service"**
3. Connect your Git repository
4. Configure:
   - **Name**: `avinashh-rag-assistant` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && cd frontend/react-app && npm install && npm run build
     ```
   - **Start Command**: 
     ```bash
     python backend/app.py
     ```
   - **Plan**: Free (or upgrade if needed)

### 3. Set Environment Variables

In your Render service dashboard, go to **Environment** tab and add:

- **GROQ_API_KEY**: Your Groq API key from https://console.groq.com

The `PORT` variable is automatically set by Render - you don't need to set it manually.

### 4. Important Notes

#### Before First Deployment

**Index your documents locally first!**

The embeddings (`embeddings/resume.index` and `embeddings/resume_meta.json`) should already be committed to your repository. If not:

1. Run locally:
   ```bash
   python backend/index_documents.py
   ```
2. Commit the `embeddings/` folder:
   ```bash
   git add embeddings/
   git commit -m "Add document embeddings"
   git push
   ```

#### Build Process

The build process:
1. Installs Python dependencies
2. Installs Node.js dependencies for React frontend
3. Builds the React app to `frontend/static/`
4. Starts the Flask server

This may take 5-10 minutes on the free tier.

### 5. Verify Deployment

Once deployed, your service will be available at:
```
https://your-service-name.onrender.com
```

Test the endpoints:
- Health check: `https://your-service-name.onrender.com/health`
- Chat: `https://your-service-name.onrender.com/`

## Troubleshooting

### Build Fails

- **Check logs**: View build logs in Render dashboard
- **Python version**: Ensure `requirements.txt` specifies compatible versions
- **Node version**: Render uses Node 18 by default (should work fine)

### Service Won't Start

- **Check environment variables**: Ensure `GROQ_API_KEY` is set
- **Check port**: The app automatically uses Render's `PORT` environment variable
- **Check logs**: View runtime logs for error messages

### Embeddings Not Found

If you see errors about missing embeddings:
1. Ensure `embeddings/` folder is committed to your repo
2. Verify `embeddings/resume.index` and `embeddings/resume_meta.json` exist
3. Re-run `python backend/index_documents.py` locally and commit

### API Errors

- **Verify API key**: Check that `GROQ_API_KEY` is correct in Render dashboard
- **Check API credits**: Ensure you have credits in your Groq account
- **Check logs**: API errors will be visible in Render logs

## Updating Your Deployment

After making changes:

1. Commit and push your changes:
   ```bash
   git add .
   git commit -m "Your update message"
   git push
   ```

2. Render will automatically detect the push and redeploy

3. Monitor the deployment in the Render dashboard

## Custom Domain (Optional)

To use a custom domain:

1. Go to your service settings in Render
2. Click **"Custom Domains"**
3. Add your domain and follow DNS configuration instructions

## Cost Considerations

- **Free tier**: 
  - Services spin down after 15 minutes of inactivity
  - First request after spin-down may be slow
- **Paid plans**: 
  - Services stay active 24/7
  - Better performance and reliability

## Security Notes

- Never commit API keys to your repository
- Always use environment variables for sensitive data
- The `.renderignore` file prevents unnecessary files from being deployed

