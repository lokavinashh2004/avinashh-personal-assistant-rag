# backend/serve_models.py
import os
import requests
from typing import Optional

# Groq API Configuration
# Get your API key from https://console.groq.com
# You can set it as an environment variable: GROQ_API_KEY
# Or create a .env file with: GROQ_API_KEY=your_key_here
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load environment variables from .env file if it exists
except ImportError:
    pass  # dotenv is optional

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")  # Get from environment variable, with fallback

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# Available Groq models: llama-3.1-8b-instant, llama-3.1-70b-versatile, mixtral-8x7b-32768, gemma-7b-it
GROQ_MODEL = "llama-3.1-8b-instant"  # Default Groq model - fast and efficient


def generate_with_grok(prompt: str, model: Optional[str] = None) -> str:
    """
    Generate response using Groq API.
    Configured for shorter, WhatsApp-style responses.
    Groq provides fast inference with models like Llama and Mixtral.
    """
    if not GROQ_API_KEY:
        raise RuntimeError(
            "Groq API key not configured. Please set GROQ_API_KEY environment variable.\n"
            "Get your API key from: https://console.groq.com"
        )
    
    # Use provided model or default
    model_name = model or GROQ_MODEL
    
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": model_name,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7,  # Lower temperature for more focused responses
        "max_tokens": 200,  # Limit tokens for concise responses (~150 words, WhatsApp-friendly)
        "top_p": 0.9  # Nucleus sampling
    }
    
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=30)
        
        # Check if request was successful
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            # Try to get detailed error message from response
            try:
                error_data = response.json()
                error_message = error_data.get('error', {}).get('message', 'Unknown error')
                raise RuntimeError(f"Groq API error ({response.status_code}): {error_message}")
            except:
                raise RuntimeError(f"Groq API request failed: {response.status_code} {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Groq API request failed: {str(e)}")
    except (KeyError, IndexError) as e:
        raise RuntimeError(f"Unexpected response format from Groq API: {str(e)}")

