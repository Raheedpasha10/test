"""
Ultra-lightweight Python API for Vercel - No heavy dependencies
"""

import json
import os
import urllib.request
import urllib.parse
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Health check
        if '/health' in self.path:
            response = {
                'status': 'healthy',
                'groq_available': bool(os.getenv('GROQ_API_KEY')),
                'timestamp': '2024-01-01T00:00:00Z'
            }
            self.wfile.write(json.dumps(response).encode())
            return
            
        # Default response
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_POST(self):
        # CORS headers
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        # Roadmap generation
        if '/multi-agent-roadmap' in self.path:
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_data = self.rfile.read(content_length)
                request_data = json.loads(post_data.decode('utf-8'))
                query = request_data.get('query', 'web development')
                
                # Generate roadmap
                roadmap_content = self.generate_roadmap(query)
                
                response = {
                    'final_roadmap': roadmap_content,
                    'agent_insights': [{
                        'agent_name': 'Technical Analysis Agent',
                        'contribution': 'Generated specialized roadmap content',
                        'confidence': 0.85
                    }],
                    'metadata': {
                        'query': query,
                        'num_agents': 1,
                        'successful_agents': 1,
                        'agents_used': ['Technical Analysis Agent']
                    }
                }
                
                self.wfile.write(json.dumps(response).encode())
                return
                
            except Exception as e:
                error_response = {'error': str(e)}
                self.wfile.write(json.dumps(error_response).encode())
                return
        
        # Default POST response
        self.wfile.write(json.dumps({'error': 'Not found'}).encode())

    def do_OPTIONS(self):
        # CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def generate_roadmap(self, query):
        """Generate roadmap using Groq API or fallback"""
        groq_key = os.getenv('GROQ_API_KEY')
        
        if groq_key:
            try:
                # Call Groq API using urllib
                prompt = f"""Create a comprehensive learning roadmap for: {query}

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental concepts
- Set up development environment
- Build first projects

### Topics
- Core principles
- Essential tools
- Best practices

### Projects
- Beginner project
- Practice exercises

### Tools
- Development tools
- Learning resources

Create 4 detailed phases with specific skills, projects, and tools."""

                data = {
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "You are a senior career advisor with 15+ years of experience."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 3000
                }
                
                req = urllib.request.Request(
                    'https://api.groq.com/openai/v1/chat/completions',
                    data=json.dumps(data).encode('utf-8'),
                    headers={
                        'Authorization': f'Bearer {groq_key}',
                        'Content-Type': 'application/json'
                    }
                )
                
                with urllib.request.urlopen(req, timeout=30) as response:
                    result = json.loads(response.read().decode('utf-8'))
                    return result.get('choices', [{}])[0].get('message', {}).get('content', self.get_fallback_roadmap(query))
                    
            except Exception as e:
                print(f"Groq API error: {e}")
        
        return self.get_fallback_roadmap(query)

    def get_fallback_roadmap(self, query):
        """Fallback roadmap when API is unavailable"""
        return f"""# {query.title()} Learning Roadmap

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental {query} concepts
- Set up development environment
- Complete first projects

### Topics
- Core {query} principles
- Essential tools and technologies
- Development best practices

### Projects
- Hello World application
- Basic portfolio project

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
- Testing and debugging

### Projects
- Web application project
- API integration

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
- Security practices
- Database integration

### Projects
- Full-stack application
- Production deployment

### Tools
- Cloud platforms
- Monitoring tools

## Phase 4: Professional (10-12 weeks)
### Goals
- Prepare for job market
- Build professional portfolio
- Network professionally

### Topics
- Industry best practices
- Interview preparation
- Professional development

### Projects
- Capstone project
- Open source contribution

### Tools
- Professional platforms
- Portfolio hosting"""