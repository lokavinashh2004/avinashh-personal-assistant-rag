# Render Deployment Checklist

Use this checklist before deploying to Render.

## ✅ Pre-Deployment Checklist

### 1. Code Preparation
- [ ] All code is committed to Git
- [ ] Code is pushed to GitHub/GitLab/Bitbucket
- [ ] `requirements.txt` is up to date
- [ ] `render.yaml` exists and is correct
- [ ] `.renderignore` is set up (optional, but recommended)

### 2. Embeddings & Data
- [ ] Documents are indexed: `python backend/index_documents.py`
- [ ] `embeddings/` folder exists with:
  - [ ] `resume.index`
  - [ ] `resume_meta.json`
- [ ] `embeddings/` folder is committed to Git

### 3. Frontend Build
- [ ] React app can build locally:
  ```bash
  cd frontend/react-app
  npm install
  npm run build
  ```
- [ ] Built files appear in `frontend/static/`
- [ ] Built frontend is committed (or will be built on Render)

### 4. Environment Variables
- [ ] You have a Groq API key from https://console.groq.com
- [ ] Ready to add `GROQ_API_KEY` in Render dashboard

### 5. Local Testing
- [ ] App runs locally: `python backend/app.py`
- [ ] Frontend loads correctly
- [ ] Chat functionality works
- [ ] API endpoints respond correctly

## 🚀 Deployment Steps

1. **Push to Git**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push
   ```

2. **Create Render Service**
   - Go to https://dashboard.render.com
   - Click "New +" → "Blueprint"
   - Connect your repository
   - Render will auto-detect `render.yaml`

3. **Add Environment Variable**
   - In Render dashboard → Environment tab
   - Add: `GROQ_API_KEY` = your API key

4. **Deploy**
   - Click "Apply"
   - Wait for build to complete (5-10 minutes)
   - Monitor logs for any errors

5. **Test**
   - Visit your service URL
   - Test `/health` endpoint
   - Test chat functionality

## 📝 Files Created for Deployment

- `render.yaml` - Render configuration
- `Procfile` - Alternative start command (for Heroku compatibility)
- `.renderignore` - Files to exclude from deployment
- `DEPLOY.md` - Detailed deployment guide
- Updated `requirements.txt` - Pinned versions
- Updated `backend/app.py` - PORT handling for Render

## ⚠️ Common Issues

**Build fails:**
- Check Node.js version (Render uses Node 18)
- Verify `package.json` is correct
- Check build logs in Render dashboard

**Service won't start:**
- Verify `GROQ_API_KEY` is set
- Check that embeddings exist
- Review runtime logs

**Frontend not loading:**
- Ensure React build completed successfully
- Check that `frontend/static/` has files
- Verify Flask is serving static files correctly

## 🔗 Useful Links

- Render Dashboard: https://dashboard.render.com
- Groq Console: https://console.groq.com
- Render Docs: https://render.com/docs

