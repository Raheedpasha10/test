"""
Vercel deployment of the exact working local backend
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

# Add the Generative directory to path
generative_path = os.path.join(os.path.dirname(__file__), '..', 'Generative')
sys.path.insert(0, generative_path)

# Import the exact working FastAPI app
from main import app

# Vercel handler
def handler(scope, receive, send):
    """ASGI handler for Vercel that uses your exact working FastAPI app"""
    import asyncio
    return asyncio.run(app(scope, receive, send))