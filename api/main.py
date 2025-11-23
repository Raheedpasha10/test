"""
Simple Vercel API Entry Point for Margdarshan Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from groq import Groq

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

# Initialize Groq client
groq_client = None
try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
except Exception as e:
    print(f"Warning: Groq client initialization failed: {e}")

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "groq_available": groq_client is not None
    }

@app.post("/api/multi-agent-roadmap")
async def generate_roadmap(request_data: dict):
    try:
        query = request_data.get("query", "")
        
        if not groq_client:
            return {"error": "AI service not available"}
            
        # Simple roadmap generation using Groq
        prompt = f"""Create a detailed career roadmap for: {query}

Format as markdown with exactly this structure:

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental concepts
- Build basic skills
- Understand core principles

### Topics  
- Basic concepts
- Essential skills
- Core knowledge areas

### Projects
- Beginner project 1
- Practice exercise 2

### Tools
- Tool 1
- Tool 2

## Phase 2: Development (6-8 weeks)
[Continue with similar structure]

Create 4-5 phases with specific, actionable content for {query}."""

        response = groq_client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are an expert career advisor."},
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=3000,
            temperature=0.7
        )
        
        roadmap_content = response.choices[0].message.content
        
        return {
            "final_roadmap": roadmap_content,
            "agent_insights": [],
            "metadata": {
                "query": query,
                "num_agents": 1,
                "successful_agents": 1
            }
        }
        
    except Exception as e:
        return {
            "error": f"Roadmap generation failed: {str(e)}",
            "final_roadmap": f"# {query} Learning Path\n\nBasic roadmap generation is temporarily unavailable."
        }

# Export app for Vercel
app = app