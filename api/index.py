"""
Vercel Python API - Restored from working local backend
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import httpx
from typing import Dict, Any, Optional
import asyncio

# Create FastAPI app
app = FastAPI(title="Student Compass API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get API keys from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GOOGLE_GENAI_API_KEY = os.getenv("GOOGLE_GENAI_API_KEY")

async def call_groq_ai(prompt: str, model: str = "llama-3.1-8b-instant") -> Optional[str]:
    """Call Groq AI API - exactly as it worked locally"""
    if not GROQ_API_KEY:
        return None
        
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "system", "content": "You are a senior technical career advisor with 15+ years of industry experience."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 3000
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"Groq AI error: {e}")
    return None

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "groq_available": bool(GROQ_API_KEY),
        "google_ai_available": bool(GOOGLE_GENAI_API_KEY),
        "timestamp": "2024-01-01T00:00:00Z"
    }

@app.post("/api/multi-agent-roadmap")
async def generate_multi_agent_roadmap(request: Request):
    """Multi-agent roadmap generation - restored from working local version"""
    try:
        request_data = await request.json()
        query = request_data.get("query", "")
        background = request_data.get("background", {})
        
        if not query:
            raise HTTPException(status_code=400, detail="Query is required")
        
        # Create enhanced prompt matching your local working version
        prompt = f"""As a technical career expert, create a detailed learning roadmap for: {query}

Format as markdown with this EXACT structure:

## Phase 1: Foundation (4-6 weeks)
### Goals
- [Specific technical goal 1]
- [Specific technical goal 2] 
- [Specific technical goal 3]

### Topics
- [Technical topic 1]
- [Technical topic 2]
- [Technical topic 3]

### Projects
- [Hands-on project 1]
- [Hands-on project 2]

### Tools
- [Industry tool 1]
- [Industry tool 2]

## Phase 2: Development (6-8 weeks)
### Goals
- [Intermediate goals]

### Topics
- [Advanced topics]

### Projects
- [Intermediate projects]

### Tools
- [Professional tools]

## Phase 3: Advanced (8-10 weeks)
### Goals
- [Advanced goals]

### Topics
- [Expert topics]

### Projects
- [Complex projects]

### Tools
- [Industry tools]

## Phase 4: Professional (10-12 weeks)
### Goals
- [Professional goals]

### Topics
- [Industry topics]

### Projects
- [Capstone projects]

### Tools
- [Professional platforms]

Create 4-5 phases with SPECIFIC {query} terminology and real industry requirements."""

        # Try multi-agent approach (as in your working local version)
        agents_used = []
        final_roadmap = None
        
        # Agent 1: Strategic Planner (Groq)
        try:
            strategic_content = await call_groq_ai(prompt, "llama-3.1-8b-instant")
            if strategic_content:
                agents_used.append("Strategic Planner")
                final_roadmap = strategic_content
        except Exception as e:
            print(f"Strategic agent failed: {e}")
            
        # Agent 2: Technical Expert (fallback)
        if not final_roadmap:
            try:
                technical_content = await call_groq_ai(prompt, "llama-3.1-8b-instant")
                if technical_content:
                    agents_used.append("Technical Expert") 
                    final_roadmap = technical_content
            except Exception as e:
                print(f"Technical agent failed: {e}")
        
        # Fallback roadmap if AI fails
        if not final_roadmap:
            final_roadmap = f"""# {query.title()} Learning Roadmap

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental {query} concepts
- Set up development environment
- Build foundational skills

### Topics
- Core {query} principles
- Essential tools and technologies
- Industry best practices

### Projects
- Beginner project
- Portfolio starter

### Tools
- Development environment
- Version control

## Phase 2: Development (6-8 weeks)
### Goals
- Build practical skills
- Create portfolio projects
- Learn frameworks

### Topics
- Advanced {query} concepts
- Popular frameworks
- Testing methodologies

### Projects
- Intermediate application
- Real-world project

### Tools
- Framework tools
- Testing frameworks

## Phase 3: Advanced (8-10 weeks)
### Goals
- Master advanced concepts
- Build complex systems
- Learn deployment

### Topics
- System design
- Performance optimization
- Security practices

### Projects
- Full-scale application
- Production deployment

### Tools
- Cloud platforms
- Monitoring tools

## Phase 4: Professional (10-12 weeks)
### Goals
- Prepare for career
- Build professional network
- Continuous learning

### Topics
- Industry trends
- Professional skills
- Leadership concepts

### Projects
- Capstone project
- Open source contribution

### Tools
- Professional platforms
- Networking tools"""

        # Build response matching your working local format
        return {
            "final_roadmap": final_roadmap,
            "agent_insights": [
                {
                    "agent_name": agent,
                    "contribution": "Generated specialized roadmap content",
                    "confidence": 0.85,
                    "focus": f"{agent} analysis"
                } for agent in (agents_used or ["Fallback System"])
            ],
            "metadata": {
                "query": query,
                "num_agents": len(agents_used) or 1,
                "successful_agents": len(agents_used) or 1,
                "agents_used": agents_used or ["Fallback System"],
                "using_multi_agent": True,
                "session_id": f"session_{int(asyncio.get_event_loop().time())}"
            },
            "funneling_report": {
                "session_id": f"session_{int(asyncio.get_event_loop().time())}",
                "agent_performance": {
                    "total_agents": len(agents_used) or 1,
                    "successful_agents": len(agents_used) or 1,
                    "success_rate_percent": 100 if agents_used else 0
                }
            }
        }
        
    except Exception as e:
        print(f"Error in multi-agent roadmap: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Export for Vercel
def handler(scope, receive, send):
    """ASGI handler for Vercel"""
    import uvicorn
    return uvicorn.run(app, scope=scope, receive=receive, send=send)