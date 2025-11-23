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

# Check if frontend build exists
build_dir = os.path.join(os.path.dirname(__file__), "frontend", "build")
static_dir = os.path.join(build_dir, "static")

print(f"🔍 Checking build directory: {build_dir}")
print(f"📁 Build directory exists: {os.path.exists(build_dir)}")
print(f"📁 Static directory exists: {os.path.exists(static_dir)}")

# Mount static files BEFORE defining routes
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    print("✅ Mounted static files at /static")

# Include API routers BEFORE frontend routes (keep existing prefixes)
app.include_router(auth.router)  # has prefix="/auth"
app.include_router(mock_test.router)  # has prefix="/mock-test"
app.include_router(agents.router)  # has prefix="/agents" 
app.include_router(resources_routes.router)  # has prefix="/resources"
app.include_router(health.router, prefix="/api")  # avoid conflict with frontend route
app.include_router(analyze.router)
app.include_router(update_skills.router)
app.include_router(ai_search.router)
app.include_router(multi_agent_roadmap.router)
from routes import real_multi_agent
app.include_router(real_multi_agent.router, prefix="/api/real-multi-agent")

# Route for root path to serve React app
@app.get("/")
async def serve_frontend():
    """Serve the React frontend"""
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "build", "index.html")
    print(f"🏠 Serving frontend from: {frontend_path}")
    print(f"📄 Frontend file exists: {os.path.exists(frontend_path)}")
    
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path, media_type='text/html')
    else:
        return {"message": "MARGDARSHAK API is running - Frontend build not found"}

# Catch-all route for React Router (must be last)
@app.get("/{full_path:path}")
async def serve_spa_routes(full_path: str):
    """Serve React app for all routes (SPA routing)"""
    print(f"🔄 SPA route requested: {full_path}")
    
    # Don't serve SPA for API routes
    if full_path.startswith("api/"):
        return {"error": "API endpoint not found"}
    
    # Try to serve static file first
    file_path = os.path.join(os.path.dirname(__file__), "frontend", "build", full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        print(f"📄 Serving static file: {file_path}")
        return FileResponse(file_path)
    
    # Serve React app for all other routes
    frontend_path = os.path.join(os.path.dirname(__file__), "frontend", "build", "index.html")
    if os.path.exists(frontend_path):
        print(f"🏠 Serving SPA for route: {full_path}")
        return FileResponse(frontend_path, media_type='text/html')
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
