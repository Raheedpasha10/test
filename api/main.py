"""
Simple Vercel API Entry Point for Margdarshan Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx
import asyncio
import json
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

# Initialize AI clients
groq_client = None
google_api_key = None

try:
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        groq_client = Groq(api_key=groq_api_key)
        
    google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
except Exception as e:
    print(f"Warning: AI client initialization failed: {e}")

# Lightweight Google AI function
async def call_google_ai(prompt: str) -> str:
    if not google_api_key:
        return None
        
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={google_api_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {
                        "temperature": 0.7,
                        "maxOutputTokens": 2000
                    }
                }
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
    except Exception as e:
        print(f"Google AI error: {e}")
    return None

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "groq_available": groq_client is not None,
        "google_ai_available": google_api_key is not None
    }

@app.post("/api/multi-agent-roadmap")
async def generate_roadmap(request_data: dict):
    try:
        query = request_data.get("query", "")
        
        if not groq_client and not google_api_key:
            return {"error": "AI services not available"}
        
        # Multi-agent approach: Use both AI services for better results
        agents_used = []
        roadmap_results = []
        
        # Agent 1: Groq for technical analysis
        if groq_client:
            try:
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

                groq_response = groq_client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are a senior technical career advisor with 15+ years of industry experience."},
                        {"role": "user", "content": technical_prompt}
                    ],
                    model="llama-3.1-8b-instant",
                    max_tokens=3000,
                    temperature=0.7
                )
                
                groq_content = groq_response.choices[0].message.content
                roadmap_results.append(groq_content)
                agents_used.append("Technical Analysis Agent")
                
            except Exception as e:
                print(f"Groq agent failed: {e}")
        
        # Agent 2: Google AI for market insights
        if google_api_key:
            try:
                market_prompt = f"""As a market research expert, enhance this {query} roadmap with current industry trends and market insights.

Provide the same markdown structure but focus on:
- Current market demands for {query}
- Emerging technologies and trends
- Industry-specific certifications
- Real job market requirements
- Salary progression expectations

Format exactly as:
## Phase 1: [Phase Name] (duration)
### Goals
- [Market-relevant goal 1]
- [Market-relevant goal 2]

Continue for 4-5 phases with real market insights."""

                google_content = await call_google_ai(market_prompt)
                if google_content:
                    roadmap_results.append(google_content)
                    agents_used.append("Market Research Agent")
                    
            except Exception as e:
                print(f"Google AI agent failed: {e}")
        
        # Combine results or use best available
        if roadmap_results:
            # Use the most comprehensive roadmap (usually the first/longest one)
            final_roadmap = max(roadmap_results, key=len)
            
            return {
                "final_roadmap": final_roadmap,
                "agent_insights": [
                    {
                        "agent_name": agent,
                        "contribution": "Generated specialized roadmap content",
                        "confidence": 0.85
                    } for agent in agents_used
                ],
                "metadata": {
                    "query": query,
                    "num_agents": len(agents_used),
                    "successful_agents": len(roadmap_results),
                    "agents_used": agents_used
                }
            }
        else:
            # Fallback response
            return {
                "final_roadmap": f"# {query} Learning Roadmap\n\n## Phase 1: Foundation\n- Start with basic concepts\n- Build fundamental skills\n\n## Phase 2: Practice\n- Apply knowledge in projects\n- Gain hands-on experience",
                "agent_insights": [],
                "metadata": {
                    "query": query,
                    "num_agents": 0,
                    "successful_agents": 0,
                    "error": "All AI agents unavailable"
                }
            }
        
    except Exception as e:
        return {
            "error": f"Multi-agent roadmap generation failed: {str(e)}",
            "final_roadmap": f"# {query} Learning Path\n\nRoadmap generation temporarily unavailable."
        }

# Export app for Vercel
app = app