"""
Lightweight Vercel API for Student Compass - No Heavy Dependencies
"""

import os
import json
import urllib.request
import urllib.parse
import urllib.error

# Get API keys from environment
groq_api_key = os.getenv("GROQ_API_KEY")
google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")

def call_groq_ai(prompt: str) -> str:
    """Call Groq AI API using urllib"""
    if not groq_api_key:
        return None
        
    try:
        data = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": "You are a senior technical career advisor with 15+ years of industry experience."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "max_tokens": 3000
        }
        
        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=json.dumps(data).encode('utf-8'),
            headers={
                "Authorization": f"Bearer {groq_api_key}",
                "Content-Type": "application/json"
            }
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get("choices", [{}])[0].get("message", {}).get("content", "")
            
    except Exception as e:
        print(f"Groq AI error: {e}")
    return None

def generate_fallback_roadmap(query: str) -> str:
    """Generate fallback roadmap when AI is unavailable"""
    return f"""# {query} Learning Roadmap

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
- Industry-standard platforms

## Phase 4: Specialization (10-12 weeks)
### Goals
- Deep dive into {query} specialization
- Master advanced techniques
- Build professional portfolio

### Topics
- Expert-level {query} concepts
- Industry trends and innovations
- Advanced problem solving

### Projects
- Capstone project
- Open source contributions

### Tools
- Professional toolchain
- Industry certifications"""

def generate_roadmap_response(query: str):
    """Generate roadmap using AI or fallback"""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }
    
    if not groq_api_key:
        # Use fallback roadmap
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                "final_roadmap": generate_fallback_roadmap(query),
                "agent_insights": [],
                "metadata": {
                    "query": query,
                    "num_agents": 0,
                    "successful_agents": 0,
                    "error": "AI service not available - using fallback",
                    "fallback": True
                }
            })
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
    groq_content = call_groq_ai(technical_prompt)
    
    if groq_content:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
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
            })
        }
    else:
        # Fallback if AI call fails
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({
                "final_roadmap": generate_fallback_roadmap(query),
                "agent_insights": [],
                "metadata": {
                    "query": query,
                    "num_agents": 0,
                    "successful_agents": 0,
                    "error": "AI generation failed - using fallback",
                    "fallback": True
                }
            })
        }

def handler(event, context=None):
    """Main Vercel serverless function handler"""
    try:
        # Get request info
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        
        # CORS headers
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Content-Type': 'application/json'
        }
        
        # Handle CORS preflight
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({'message': 'OK'})
            }
        
        # Health endpoint
        if path in ['/api/health', '/health'] and method == 'GET':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'status': 'healthy',
                    'groq_available': bool(groq_api_key),
                    'google_ai_available': bool(google_api_key)
                })
            }
        
        # Roadmap endpoint
        if path in ['/api/multi-agent-roadmap', '/multi-agent-roadmap'] and method == 'POST':
            body = event.get('body', '{}')
            if isinstance(body, str):
                request_data = json.loads(body)
            else:
                request_data = body
                
            query = request_data.get('query', '')
            return generate_roadmap_response(query)
        
        # 404 for other routes
        return {
            'statusCode': 404,
            'headers': headers,
            'body': json.dumps({'error': 'Not Found'})
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*', 'Content-Type': 'application/json'},
            'body': json.dumps({'error': f'Internal server error: {str(e)}'})
        }