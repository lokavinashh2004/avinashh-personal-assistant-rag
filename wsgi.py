#!/usr/bin/env python
"""
WSGI entry point for production deployment (Gunicorn).
This file makes the Flask app available to Gunicorn.
"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the Flask app from backend.api
from backend.api import app

# Gunicorn expects a variable named 'application'
application = app

# Also expose as 'app' for compatibility
if __name__ == "__main__":
    application.run()
