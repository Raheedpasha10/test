"""
Simple Vercel API Entry Point for Margdarshan Backend
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import httpx

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
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")

# Lightweight Groq AI function
async def call_groq_ai(prompt: str) -> str:
    """Call Groq AI API"""
    if not groq_api_key:
        return None
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "You are a senior technical career advisor with 15+ years of industry experience."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 3000
                },
                timeout=30.0
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
        "groq_available": groq_api_key is not None,
        "google_ai_available": google_api_key is not None
    }

@app.post("/api/multi-agent-roadmap")
async def generate_roadmap(request: Request):
    """Generate multi-agent roadmap"""
    try:
        request_data = await request.json()
        query = request_data.get("query", "")
        
        if not groq_api_key:
            # Fallback roadmap
            fallback_roadmap = f"""# {query} Learning Roadmap

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental concepts for {query}
- Build basic skills and understanding
- Establish strong learning foundation

### Topics
- Core principles and concepts
- Essential tools and technologies
- Best practices and methodologies

### Projects
- Beginner-friendly project
- Hands-on practice exercises

### Tools
- Industry-standard tools
- Learning platforms and resources

## Phase 2: Development (6-8 weeks)
### Goals
- Apply knowledge in practical scenarios
- Build intermediate-level skills
- Create portfolio projects

### Topics
- Advanced concepts and techniques
- Real-world applications
- Problem-solving approaches

### Projects
- Intermediate project development
- Portfolio building

### Tools
- Professional development tools
- Advanced frameworks

## Phase 3: Professional Application (8-10 weeks)
### Goals
- Develop professional-level competency
- Build advanced projects
- Prepare for job market

### Topics
- Advanced {query} concepts
- Industry best practices
- Professional development

### Projects
- Advanced portfolio projects
- Real-world applications

### Tools
- Professional-grade tools
- Industry-standard platforms"""

            return {
                "final_roadmap": fallback_roadmap,
                "agent_insights": [],
                "metadata": {
                    "query": query,
                    "num_agents": 0,
                    "successful_agents": 0,
                    "error": "AI service not available - using fallback",
                    "fallback": True
                }
            }
        
        # Create technical roadmap prompt
        technical_prompt = f"""As a technical career expert, create a detailed roadmap for: {query}

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

Create 4-5 phases with SPECIFIC {query} terminology and real industry requirements."""

        # Call Groq AI
        groq_content = await call_groq_ai(technical_prompt)
        
        if groq_content:
            return {
                "final_roadmap": groq_content,
                "agent_insights": [{
                    "agent_name": "Technical Analysis Agent",
                    "contribution": "Generated specialized roadmap content",
                    "confidence": 0.85
                }],
                "metadata": {
                    "query": query,
                    "num_agents": 1,
                    "successful_agents": 1,
                    "agents_used": ["Technical Analysis Agent"]
                }
            }
        else:
            # Fallback if AI call fails
            fallback_roadmap = f"""# {query} Learning Roadmap

## Phase 1: Foundation (4-6 weeks)
### Goals
- Learn fundamental {query} concepts
- Set up development environment
- Complete first practice projects

### Topics
- Basic {query} principles
- Core tools and technologies
- Development best practices

### Projects
- Hello World application
- Basic project implementation

### Tools
- Code editor/IDE
- Version control (Git)

## Phase 2: Development (6-8 weeks)
### Goals
- Build intermediate {query} skills
- Create portfolio projects
- Learn advanced concepts

### Topics
- Advanced {query} features
- Framework knowledge
- Testing and debugging

### Projects
- Portfolio project 1
- Technical challenge completion

### Tools
- Framework tools
- Testing frameworks"""

            return {
                "final_roadmap": fallback_roadmap,
                "agent_insights": [],
                "metadata": {
                    "query": query,
                    "num_agents": 0,
                    "successful_agents": 0,
                    "error": "AI generation failed - using fallback",
                    "fallback": True
                }
            }
        
    except Exception as e:
        return {
            "error": f"Multi-agent roadmap generation failed: {str(e)}",
            "final_roadmap": f"# {query} Learning Path\n\nRoadmap generation temporarily unavailable."
        }