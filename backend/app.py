#!/usr/bin/env python
"""
RAG Assistant - Main Application Entry Point
Run this file to start the Flask server.
"""
import sys
import os

# Add parent directory to path so we can import backend modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from backend.api import app

# For Gunicorn compatibility - export both app and application
application = app
app = app  # Explicitly make app available at module level

if __name__ == "__main__":
    try:
        # Get port from environment variable (Render provides this)
        port = int(os.environ.get("PORT", 7860))
        debug = os.environ.get("FLASK_ENV") != "production"
        
        print("=" * 50)
        print("Starting RAG Assistant Server...")
        print(f"Port: {port}")
        print(f"Debug: {debug}")
        print("=" * 50)
        app.run(host="0.0.0.0", port=port, debug=debug)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError starting server: {e}")
        sys.exit(1)

