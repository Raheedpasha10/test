"""
Production configuration for Render deployment
"""
import os

class ProductionSettings:
    # Environment
    ENVIRONMENT = "production"
    DEBUG = False
    
    # Server Configuration
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", 8001))
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")
    
    # CORS Configuration for production
    ALLOWED_ORIGINS = [
        "https://*.onrender.com",
        "https://student-compass-frontend.onrender.com",
        "http://localhost:3000",  # For local development
    ]
    
    # Database (if needed in future)
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./production.db")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-production-secret-key")
    
    # API Configuration
    API_TITLE = "Student Compass API"
    API_VERSION = "1.0.0"
    API_DESCRIPTION = "AI-Powered Career Guidance Platform"