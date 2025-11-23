import json
import os
import urllib.request

def handler(event, context=None):
    """Ultra-lightweight Vercel handler"""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    method = event.get('httpMethod', 'GET')
    path = event.get('path', '/')
    
    # Handle OPTIONS for CORS
    if method == 'OPTIONS':
        return {'statusCode': 200, 'headers': headers, 'body': '{}'}
    
    # Health check
    if 'health' in path:
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({'status': 'healthy'})
        }
    
    # Roadmap endpoint
    if 'roadmap' in path and method == 'POST':
        try:
            body = event.get('body', '{}')
            data = json.loads(body) if isinstance(body, str) else body
            query = data.get('query', 'web development')
            
            # Try AI call or use fallback
            roadmap = get_roadmap(query)
            
            return {
                'statusCode': 200,
                'headers': headers,
                'body': json.dumps({
                    'final_roadmap': roadmap,
                    'agent_insights': [{'agent_name': 'AI Agent', 'confidence': 0.8}],
                    'metadata': {'query': query, 'num_agents': 1}
                })
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': headers,
                'body': json.dumps({'error': str(e)})
            }
    
    return {
        'statusCode': 404,
        'headers': headers,
        'body': json.dumps({'error': 'Not found'})
    }

def get_roadmap(query):
    """Get roadmap from AI or fallback"""
    groq_key = os.getenv('GROQ_API_KEY')
    
    if groq_key:
        try:
            prompt = f"Create a detailed {query} learning roadmap with 4 phases, goals, topics, projects, and tools for each phase."
            
            req_data = {
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000
            }
            
            req = urllib.request.Request(
                'https://api.groq.com/openai/v1/chat/completions',
                data=json.dumps(req_data).encode(),
                headers={
                    'Authorization': f'Bearer {groq_key}',
                    'Content-Type': 'application/json'
                }
            )
            
            with urllib.request.urlopen(req, timeout=25) as response:
                result = json.loads(response.read().decode())
                return result.get('choices', [{}])[0].get('message', {}).get('content', fallback_roadmap(query))
        except:
            pass
    
    return fallback_roadmap(query)

def fallback_roadmap(query):
    """Fallback roadmap"""
    return f"""# {query.title()} Learning Roadmap

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental {query} concepts
- Set up development environment
- Complete basic projects

### Topics
- Core {query} principles
- Essential tools and technologies
- Best practices

### Projects
- Hello World project
- Basic portfolio site

### Tools
- Code editor (VS Code)
- Version control (Git)

## Phase 2: Development (6-8 weeks)
### Goals
- Build intermediate skills
- Create portfolio projects
- Learn frameworks

### Topics
- Advanced {query} concepts
- Popular frameworks
- Testing basics

### Projects
- Interactive application
- API integration project

### Tools
- Framework tools
- Testing frameworks

## Phase 3: Advanced (8-10 weeks)
### Goals
- Master advanced concepts
- Build complex applications
- Learn deployment

### Topics
- Performance optimization
- Security best practices
- Deployment strategies

### Projects
- Full-stack application
- Open source contribution

### Tools
- Cloud platforms
- CI/CD tools

## Phase 4: Professional (10-12 weeks)
### Goals
- Prepare for job market
- Build professional portfolio
- Network with professionals

### Topics
- Interview preparation
- Industry trends
- Soft skills

### Projects
- Capstone project
- Portfolio website

### Tools
- Professional networking
- Portfolio platforms"""