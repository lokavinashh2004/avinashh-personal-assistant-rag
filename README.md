# RAG Assistant - Avinashh Resume Chatbot

A Retrieval-Augmented Generation (RAG) system that allows you to ask questions about Avinashh's resume using natural language.

## 🏗️ Project Structure

```
Avinashh-RAG/
├── backend/              # Backend Python code
│   ├── __init__.py
│   ├── app.py            # Main application entry point
│   ├── api.py            # Flask server and API endpoints
│   ├── index_documents.py # Document indexing script
│   ├── rag_utils.py      # RAG retrieval and prompt building
│   └── serve_models.py   # LLM model integration (Groq API)
├── frontend/             # Frontend files
│   ├── templates/        # HTML templates (Flask)
│   │   └── index.html   # Main chat interface
│   └── static/          # Static files (CSS, JS)
│       ├── css/
│       │   └── style.css # WhatsApp-style styling
│       └── js/
│           └── chat.js   # Frontend JavaScript
├── data/                 # Documents to index (PDFs, TXT, MD)
│   └── resume.pdf
├── embeddings/           # Generated vector index files
│   ├── resume.index     # FAISS vector index
│   └── resume_meta.json # Metadata for indexed chunks
├── venv/                # Python virtual environment
├── requirements.txt     # Python dependencies
├── start_server.bat     # Windows batch script to start server
├── start_server.ps1     # PowerShell script to start server
└── README.md           # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+**
2. **Groq API Key** - Get from https://console.groq.com

### Installation

1. **Clone or navigate to the project directory**

2. **Create and activate virtual environment** (if not already done)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1  # Windows PowerShell
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Index documents**
   ```powershell
   python backend/index_documents.py
   ```
   This reads all PDFs/text files from `data/` and creates the vector index.

5. **Start the server**
   ```powershell
   python backend/app.py
   ```
   Or use the convenience scripts:
   ```powershell
   .\start_server.ps1    # PowerShell
   .\start_server.bat    # Command Prompt
   ```
   Server runs on `http://localhost:7860`

6. **Open in browser**
   Navigate to: `http://localhost:7860`

## 📝 Usage

1. **Start the backend server**
   ```powershell
   python src/backend.py
   ```

2. **Access the web interface**
   - Open `http://localhost:7860` in your browser
   - The modern UI will load automatically

3. **Ask questions**
   - Type questions about the resume content
   - Examples:
     - "What skills does Avinashh have?"
     - "Tell me about Avinashh's experience"
     - "What is Avinashh's education background?"

## 🔧 Configuration

### Changing the LLM Model

Edit `backend/serve_models.py` to change the Groq model:
```python
GROQ_MODEL = "llama-3.1-70b-versatile"  # Change to your preferred Groq model
```

### Adjusting Retrieval

Edit `src/rag_utils.py` to change:
- Number of retrieved contexts: `top_k=3` in `retrieve()` function
- Embedding model: `"all-MiniLM-L6-v2"` in `SentenceTransformer()`

### Adjusting Chunking

Edit `src/index_documents.py`:
- Chunk size: `chunk_size=300` in `chunk_text()`
- Overlap: `overlap=50` in `chunk_text()`

## 🔌 API Endpoints

- `GET /` - Main web interface
- `POST /chat` - Send a question and get an answer
  ```json
  {
    "question": "What skills does Avinashh have?"
  }
  ```
  Response:
  ```json
  {
    "answer": "Based on the resume, Avinashh has..."
  }
  ```
- `GET /health` - Health check endpoint

## 🛠️ Development

### Project Structure Explained

- **Backend (Flask)**: Serves the web interface and handles API requests
- **RAG Pipeline**: 
  1. User asks a question
  2. Question is embedded using Sentence Transformers
  3. Similar chunks are retrieved from FAISS index
  4. Context is built into a prompt
  5. LLM (Groq API) generates an answer
- **Frontend**: Modern, responsive chat interface with real-time updates

### Adding New Documents

1. Place PDF, TXT, or MD files in the `data/` folder
2. Re-run indexing: `python src/index_documents.py`
3. The new content will be searchable immediately

## 📦 Dependencies

- **flask**: Web framework
- **flask-cors**: CORS support
- **sentence-transformers**: Text embeddings
- **faiss-cpu**: Vector similarity search
- **pdfplumber**: PDF text extraction
- **requests**: HTTP library for Groq API calls

## 🐛 Troubleshooting

### Server won't start
- Check if dependencies are installed: `pip install -r requirements.txt`
- Verify API key is set (environment variable GROQ_API_KEY or in `backend/serve_models.py`)
- Check if embeddings exist in `embeddings/` folder

### No answers generated
- Verify Groq API connection: Check `/health` endpoint
- Check server logs for API errors
- Ensure documents are indexed
- Verify you have API credits/quota with Groq (https://console.groq.com)

### Import errors
- Make sure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

## 📄 License

This project is for personal/educational use.

