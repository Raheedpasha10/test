"""
Vercel API Entry Point for Margdarshan Backend
This file serves as the entry point for all API requests on Vercel
"""

import os
import sys

# Add the Generative directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Generative'))

# Import the FastAPI app from the main application
from main import app

# Vercel serverless function handler
def handler(request, response):
    """
    Vercel serverless function handler
    """
    return app(request, response)

# For Vercel, we need to export the app
# The app is already configured in Generative/main.py
if __name__ == "__main__":
    # This won't be called in Vercel, but useful for local testing
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)