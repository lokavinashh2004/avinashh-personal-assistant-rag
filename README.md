# 🤖 Avinashh Personal Assistant - RAG Chatbot

A modern, intelligent personal assistant powered by Retrieval-Augmented Generation (RAG) that answers questions about Lok Avinashh's professional background, skills, and experience. Built with Flask, React, and Groq AI.

## ✨ Features

- 💬 **WhatsApp-Style Chat Interface** - Modern, responsive UI with real-time messaging
- 📄 **Resume PDF Preview** - Beautiful document card with one-click download
- 🧠 **Intelligent RAG System** - Retrieves relevant context from resume to answer questions
- ⚡ **Fast Responses** - Powered by Groq's lightning-fast LLM API
- 🎯 **Smart Greeting Detection** - Proactively offers resume on greeting
- 🔍 **Semantic Search** - Uses FAISS vector similarity search for accurate retrieval
- 🌐 **Production Ready** - Deployable to Render, Heroku, or any cloud platform

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │─────▶│    Flask     │─────▶│   Groq AI   │
│  Frontend   │      │   Backend    │      │     LLM     │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │    FAISS     │
                     │ Vector Index │
                     └──────────────┘
```

## 📁 Project Structure

```
avinash-personal-assistant-rag/
├── backend/                    # Flask backend
│   ├── api.py                 # API endpoints & server
│   ├── app.py                 # Application entry point
│   ├── index_documents.py     # Document indexing script
│   ├── rag_utils.py           # RAG retrieval logic
│   └── serve_models.py        # Groq LLM integration
├── frontend/
│   ├── react-app/             # React source code
│   │   ├── src/
│   │   │   ├── App.jsx        # Main app component
│   │   │   ├── components/    # UI components
│   │   │   └── App.css        # Styling
│   │   └── package.json
│   └── static/                # Built React app (production)
├── data/                      # Source documents
│   └── resume.pdf
├── embeddings/                # Generated vector index
│   ├── resume.index           # FAISS index
│   └── resume_meta.json       # Chunk metadata
├── resume/                    # Resume files for download
│   └── T_Lok_Avinashh Resume.pdf
├── requirements.txt           # Python dependencies
├── runtime.txt                # Python version (for deployment)
├── Procfile                   # Deployment config
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** 
- **Node.js 16+** (for frontend development)
- **Groq API Key** 

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd avinash-personal-assistant-rag
   ```

2. **Set up Python environment**
   ```bash
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure API Key**
   
   Create a `.env` file in the `backend/` directory:
   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

5. **Index documents** (First time only)
   ```bash
   python backend/index_documents.py
   ```
   This creates the vector index from documents in `data/`

6. **Start the server**
   ```bash
   python backend/app.py
   ```
   
   Or use the convenience scripts:
   ```bash
   # Windows PowerShell
   .\start_server.ps1
   
   # Windows Command Prompt
   .\start_server.bat
   ```

7. **Open in browser**
   
   Navigate to: **http://localhost:7860**

## � Development

### Frontend Development

The frontend is a React app built with Vite.

```bash
cd frontend/react-app

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

The production build is automatically copied to `frontend/static/` for Flask to serve.

### Backend Development

The backend uses Flask with the following endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serves React app |
| `/chat` | POST | Handles chat messages |
| `/health` | GET | Health check |
| `/resume/<filename>` | GET | Serves resume PDF |

### Adding New Documents

1. Place PDF, TXT, or MD files in `data/` folder
2. Re-run indexing:
   ```bash
   python backend/index_documents.py
   ```
3. Restart the server

## 🎨 Features in Detail

### 1. Smart Greeting Detection
When users say "Hi", "Hello", etc., the assistant proactively asks if they want to see the resume.

### 2. Resume PDF Card
Instead of a plain link, the resume appears as a beautiful document card with:
- PDF icon and filename
- "Tap to download" description
- Prominent download button

### 3. Intelligent Question Answering
The RAG pipeline:
1. Embeds the user's question using Sentence Transformers
2. Retrieves top-3 most relevant chunks from FAISS index
3. Builds a context-aware prompt
4. Generates a natural answer using Groq's LLM

### 4. Response Cleaning
Removes verbose phrases like "Based on the context" and "According to the resume" for more natural, concise responses.

## 🔧 Configuration

### Change LLM Model

Edit `backend/serve_models.py`:
```python
GROQ_MODEL = "llama-3.1-70b-versatile"  # or any Groq model
```

### Adjust Retrieval Settings

Edit `backend/rag_utils.py`:
```python
# Number of context chunks to retrieve
contexts = retrieve(question, top_k=3)

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")
```

### Adjust Chunking

Edit `backend/index_documents.py`:
```python
chunk_size = 300  # Characters per chunk
overlap = 50      # Overlap between chunks
```

## 🌐 Deployment

### Deploy to Render

1. Push code to GitHub
2. Create new Web Service on [Render](https://render.com)
3. Connect your repository
4. Render will auto-detect `render.yaml` configuration
5. Add environment variable: `GROQ_API_KEY`
6. Deploy!

The app includes:
- `Procfile` - Gunicorn configuration
- `render.yaml` - Render deployment config
- `runtime.txt` - Python version specification

### Environment Variables

Set these in your deployment platform:
- `GROQ_API_KEY` - Your Groq API key
- `PORT` - Server port (auto-set by most platforms)
- `FLASK_ENV` - Set to `production` for production

## 📊 API Usage

### Chat Endpoint

**Request:**
```bash
curl -X POST http://localhost:7860/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What are Avinashh'\''s skills?"}'
```

**Response:**
```json
{
  "answer": "Avinashh has expertise in Python, Machine Learning, NLP..."
}
```

**Resume Request Response:**
```json
{
  "answer": "Sure! Here's Lok Avinashh's resume.",
  "document": {
    "url": "/resume/T_Lok_Avinashh%20Resume.pdf",
    "name": "T_Lok_Avinashh Resume.pdf",
    "type": "PDF"
  }
}
```

## 🐛 Troubleshooting

### Server won't start
- ✅ Check if virtual environment is activated
- ✅ Install dependencies: `pip install -r requirements.txt`
- ✅ Verify `GROQ_API_KEY` is set
- ✅ Check if embeddings exist in `embeddings/` folder

### No answers generated
- ✅ Check `/health` endpoint for API status
- ✅ Verify Groq API key is valid
- ✅ Check server logs for errors
- ✅ Ensure documents are indexed

### Frontend not loading
- ✅ Check if React app is built: `npm run build` in `frontend/react-app`
- ✅ Verify `frontend/static/` contains built files
- ✅ Clear browser cache

### Import errors
- ✅ Activate virtual environment
- ✅ Reinstall dependencies: `pip install -r requirements.txt`

## 📦 Dependencies

### Backend
- `flask` - Web framework
- `flask-cors` - CORS support
- `sentence-transformers` - Text embeddings
- `faiss-cpu` - Vector similarity search
- `pdfplumber` - PDF text extraction
- `requests` - HTTP client for Groq API
- `gunicorn` - Production WSGI server

### Frontend
- `react` - UI library
- `vite` - Build tool

## 🤝 Contributing

This is a personal project, but suggestions and improvements are welcome!

## 📄 License

This project is for personal/educational use.

## 👨‍💻 Author

**Lok Avinashh**

For questions about this project, feel free to ask the chatbot itself! 😄

---

Made with ❤️ using Flask, React, and Groq AI
