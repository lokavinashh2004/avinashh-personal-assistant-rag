# Complete Setup Guide - Using Groq API

## Overview

The system is now configured to use **Groq API** for fast LLM generation. Groq provides ultra-fast inference with models like Llama 3 and Mixtral.

## Step-by-Step Setup

### 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

This will install all required packages including `requests` for API calls.

### 2. Set Up API Key

Get your Groq API key from https://console.groq.com

**Option A: Use Environment Variable (Recommended)**
```powershell
# PowerShell
$env:GROQ_API_KEY="your_api_key_here"

# Or create a .env file in the project root:
# GROQ_API_KEY=your_api_key_here
```

**Option B: Edit Code Directly**
Edit `backend/serve_models.py` and set the `GROQ_API_KEY` variable.

### 3. Index Documents

Before running the server, index your documents:

```powershell
python backend/index_documents.py
```

This reads all PDFs/text files from `data/` and creates the vector index.

### 4. Run the Server

```powershell
python backend/app.py
```

The system will:
- ✅ Use Groq API for all LLM generation
- ✅ Show which generator is active at startup
- ✅ Handle errors gracefully

## Current Configuration

- **LLM Provider**: Groq API
- **Model**: `llama-3.1-8b-instant` (default, fast and efficient)
- **API Endpoint**: https://api.groq.com/openai/v1/chat/completions

## Changing the Model

Edit `backend/serve_models.py` to change the Groq model:

```python
GROQ_MODEL = "llama-3.1-70b-versatile"  # or other available models
```

Available Groq models:
- `llama-3.1-8b-instant` (default) - Fast and efficient
- `llama-3.1-70b-versatile` - More powerful
- `mixtral-8x7b-32768` - High quality
- `gemma-7b-it` - Alternative option

## Troubleshooting

**API errors?**
- Verify the API key is correct (get from https://console.groq.com)
- Check your internet connection
- Ensure you have API credits/quota with Groq

**Import errors?**
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**No responses?**
- Check server logs for API errors
- Verify documents are indexed in `embeddings/` folder
- Test the API key manually using curl or Postman
