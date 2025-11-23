from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import os

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

# Mount static files for frontend
static_dir = os.path.join(os.path.dirname(__file__), "frontend", "build", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Serve React app
@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the React frontend"""
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "build", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {"message": "MARGDARSHAK API is running"}

# Catch-all route for React Router
@app.get("/{full_path:path}", response_class=FileResponse)
async def serve_frontend_routes(full_path: str):
    """Serve React app for all frontend routes"""
    # Don't intercept API routes
    if full_path.startswith("api/") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
        return {"error": "Not Found"}
    
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "build", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    else:
        return {"message": "MARGDARSHAK API is running"}

if __name__ == "__main__":
    import uvicorn
    import os
    
    # Use PORT environment variable for Render deployment  
    port_env = os.getenv("PORT")
    if port_env and port_env != "$PORT":
        port = int(port_env)
    else:
        port = settings.PORT
    host = os.getenv("HOST", settings.HOST)
    
    print(f"🚀 Starting Student Compass API...")
    print(f"📍 Environment: {getattr(settings, 'ENVIRONMENT', 'production')}")
    print(f"🌐 Host: {host}")
    print(f"🔌 Port: {port}")
    print(f"🔑 Groq API: {'✅ Configured' if getattr(settings, 'GROQ_API_KEY', None) else '❌ Missing'}")
    
    uvicorn.run(app, host=host, port=port)
