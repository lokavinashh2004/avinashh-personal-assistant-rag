# backend/api.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.rag_utils import retrieve, build_prompt
from backend.serve_models import generate_with_grok  # Function name kept as generate_with_grok for compatibility

# Get the base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configure for React build
REACT_BUILD_DIR = os.path.join(BASE_DIR, 'frontend', 'static')
RESUME_DIR = os.path.join(BASE_DIR, 'resume')
RESUME_FILENAME = "T_Lok_Avinashh Resume.pdf"

app = Flask(
    __name__,
    static_folder=REACT_BUILD_DIR,
    static_url_path=''
)

# Enable CORS for all routes (useful if you want to access from different origins)
CORS(app)

# Use Grok as the generator
GENERATOR = "grok"

@app.route("/")
def index():
    """Serve the React app"""
    return app.send_static_file('index.html')

def clean_response(text):
    """
    Clean and format the response for WhatsApp-style chat.
    Removes excessive verbosity and ensures concise formatting.
    """
    if not text:
        return text
    
    # Remove common verbose patterns
    text = text.strip()
    
    # Remove phrases like "Based on the context", "According to the resume", etc. at the start
    verbose_starters = [
        "Based on the context",
        "According to the resume",
        "According to the information provided",
        "Based on the provided context",
        "From the context",
        "Based on the documentation",
        "According to his resume",
        "Based on his resume",
        "From his resume",
        "As mentioned in",
        "Per the resume"
    ]
    
    # Remove common assistant-like disclaimers that sound too robotic
    robotic_phrases = [
        "Based on what I know",
        "From what I can see",
        "According to my knowledge",
        "I can tell you that",
        "Let me tell you",
        "I would say that"
    ]
    
    # Remove greetings
    greetings = [
        "Hello",
        "Hi",
        "Hey",
        "Hi there",
        "Hey there"
    ]
    
    # Check for verbose starters (case insensitive) - must be complete phrases
    text_lower = text.lower()
    for starter in verbose_starters + robotic_phrases:
        starter_lower = starter.lower()
        if text_lower.startswith(starter_lower):
            # Ensure it's a complete phrase (check boundary)
            next_char_idx = len(starter)
            if next_char_idx >= len(text) or text[next_char_idx] in ' \t\n,:.!?':
                text = text[len(starter):].strip()
                # Remove trailing commas/colons
                if text and text[0] in (',', ':', '-'):
                    text = text[1:].strip()
                break
    
    # Remove greetings at the start (only if they're complete words, not part of other words like "His")
    for greeting in greetings:
        greeting_lower = greeting.lower()
        if text_lower.startswith(greeting_lower):
            # Check if it's a complete word (followed by space, punctuation, or end of string)
            # NOT followed by a letter (to avoid removing "Hi" from "His")
            next_char_idx = len(greeting)
            if next_char_idx >= len(text):
                # Greeting is at the end - remove it
                text = ""
                break
            next_char = text[next_char_idx].lower()
            # Only remove if followed by space, punctuation, or is end of string
            # NOT if followed by a letter (to avoid breaking words like "His")
            if next_char in ' \t\n,!:.':
                text = text[len(greeting):].strip()
                if text and text[0] in ',!:.':
                    text = text[1:].strip()
                break
    
    # Fix grammatical errors: incomplete words at the start
    if text:
        text = text.strip()
        
        # Fix common cases where a word might be cut off at the start (e.g., "s mastery" -> "His mastery")
        # Check before capitalization to handle lowercase cases
        text_lower_start = text.lower()
        if text_lower_start.startswith('s mastery'):
            text = 'His mastery' + text[9:]
        elif text_lower_start.startswith('s '):
            text = 'His ' + text[2:]
        elif text_lower_start.startswith('e '):
            text = 'He ' + text[2:]
        elif text_lower_start.startswith('t '):
            text = 'That ' + text[2:]
        
        # Ensure proper capitalization at the start after word fixes
        if text and text[0].islower():
            text = text[0].upper() + text[1:]
    
    # Ensure it doesn't end with "..." or similar
    text = text.rstrip('. ')
    
    # If response is too long, try to truncate at a sentence boundary
    max_length = 400  # Character limit for WhatsApp-style (shorter is better)
    if len(text) > max_length:
        # Try to cut at a sentence boundary
        sentences = text.split('. ')
        result = []
        char_count = 0
        for sentence in sentences:
            if char_count + len(sentence) + 2 > max_length:
                break
            result.append(sentence)
            char_count += len(sentence) + 2
        
        if result:
            text = '. '.join(result) + '.'
        else:
            # Fallback: just truncate
            text = text[:max_length] + '...'
    
    return text

@app.route("/chat", methods=["POST"])
def chat():
    """Handle chat requests"""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400
    
    question = data.get("question", "").strip()
    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        # Check if it's just a greeting - handle specially
        question_lower = question.lower().strip()
        # Remove punctuation for comparison (keep only letters, numbers, and spaces)
        question_clean = ''.join(c for c in question_lower if c.isalnum() or c == ' ').strip()
        
        # List of greeting patterns (without punctuation)
        simple_greetings = ['hello', 'hi', 'hey', 'hola', 'greetings', 'hiya', 'gm', 'gn', 'heyyo']
        extended_greetings = ['hello there', 'hi there', 'hey there', 'good morning', 'good afternoon', 'good evening']
        
        # Check if it's just a greeting
        is_greeting = (
            question_clean in simple_greetings or
            question_clean in extended_greetings or
            any(question_clean.startswith(g) and len(question_clean) <= len(g) + 5 for g in simple_greetings)
        )
        
        if is_greeting:
            # Return a simple, friendly greeting response - no RAG needed
            answer = "Hi! I'm Lok Avinashh's Personal Assistant. Would you like to have a look at his resume?"
            return jsonify({"answer": answer})
        
        # Check if user is requesting the resume
        resume_request_patterns = [
            'yes', 'yeah', 'sure', 'ok', 'okay', 'yep', 'yup', 'please',
            'show resume', 'view resume', 'see resume', 'download resume', 
            'get resume', 'resume', 'cv', 'show cv', 'view cv', 'see cv',
            'i want to see', 'can i see', 'may i see', 'show me', 
            'send resume', 'share resume', 'give resume', 'provide resume',
            'i would like to see', 'id like to see', 'want his resume',
            'see his resume', 'view his resume', 'show his resume'
        ]
        
        # Check if the question matches any resume request pattern
        is_resume_request = any(pattern in question_clean for pattern in resume_request_patterns)
        
        if is_resume_request:
            # Return resume as a document object for frontend to display
            return jsonify({
                "answer": "Sure! Here's Lok Avinashh's resume.",
                "document": {
                    "url": "/resume/T_Lok_Avinashh%20Resume.pdf",
                    "name": "T_Lok_Avinashh Resume.pdf",
                    "type": "PDF"
                }
            })
        
        # Retrieve relevant contexts for actual questions
        contexts = retrieve(question, top_k=3)
        prompt = build_prompt(question, contexts)

        # Generate answer using Grok
        answer = generate_with_grok(prompt)
        
        # Clean and format the response for WhatsApp-style chat
        answer = clean_response(answer)
        
        return jsonify({"answer": answer})
    except Exception as e:
        app.logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "ok",
        "generator": GENERATOR,
        "service": "RAG Assistant"
    })

@app.route("/resume/<path:filename>", methods=["GET"])
def serve_resume(filename):
    """Serve Lok Avinashh's resume PDF."""
    if filename != RESUME_FILENAME:
        return jsonify({"error": "File not found"}), 404
    
    file_path = os.path.join(RESUME_DIR, filename)
    if not os.path.isfile(file_path):
        return jsonify({"error": "File not found"}), 404

    return send_from_directory(RESUME_DIR, filename, mimetype="application/pdf")

@app.route("/<path:path>")
def serve_static(path):
    """Serve static files from React build (must be last route)"""
    # Don't serve API routes as static files
    if path.startswith(('chat', 'health', 'api')):
        return jsonify({"error": "Not found"}), 404
    try:
        return app.send_static_file(path)
    except:
        # If file not found, serve index.html for React Router
        return app.send_static_file('index.html')

