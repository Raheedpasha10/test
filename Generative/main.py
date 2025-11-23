from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from config.settings import settings
from routes import analyze, health, mock_test, auth, update_skills, ai_search, agents
from routes import resources as resources_routes
from routes import multi_agent_roadmap  # NEW: Multi-agent system

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description=settings.API_DESCRIPTION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(health.router)
app.include_router(analyze.router)
app.include_router(mock_test.router)
app.include_router(update_skills.router)
app.include_router(ai_search.router)
app.include_router(agents.router)
app.include_router(resources_routes.router)
app.include_router(multi_agent_roadmap.router)  # NEW: Multi-agent V2 endpoints
from routes import real_multi_agent
app.include_router(real_multi_agent.router, prefix="/api/real-multi-agent")

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT environment variable for Render deployment
    port = int(os.getenv("PORT", settings.PORT))
    host = os.getenv("HOST", settings.HOST)
    
    print(f"🚀 Starting Student Compass API...")
    print(f"📍 Environment: {settings.ENVIRONMENT}")
    print(f"🌐 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔑 Groq API: {'✅ Configured' if settings.GROQ_API_KEY else '❌ Missing'}")
    
    uvicorn.run(app, host=host, port=port)
