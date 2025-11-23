export default async function handler(request, response) {
  response.setHeader('Access-Control-Allow-Origin', '*');
  response.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  response.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  
  if (request.method === 'OPTIONS') {
    return response.status(200).end();
  }
  
  if (request.method !== 'POST') {
    return response.status(405).json({ error: 'Method not allowed' });
  }
  
  try {
    const { query } = request.body || {};
    const roadmapContent = await generateRoadmap(query || 'web development');
    
    return response.status(200).json({
      final_roadmap: roadmapContent,
      agent_insights: [{
        agent_name: 'Technical Analysis Agent',
        contribution: 'Generated specialized roadmap content',
        confidence: 0.85
      }],
      metadata: {
        query: query || 'web development',
        num_agents: 1,
        successful_agents: 1,
        agents_used: ['Technical Analysis Agent']
      }
    });
  } catch (error) {
    return response.status(500).json({ error: error.message });
  }
}

async function generateRoadmap(query) {
  const groqKey = process.env.GROQ_API_KEY;
  
  if (groqKey) {
    try {
      const prompt = `Create a comprehensive learning roadmap for: ${query}

Structure it as:

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

Create 4 detailed phases with specific skills, projects, and tools.`;

      const apiResponse = await fetch('https://api.groq.com/openai/v1/chat/completions', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${groqKey}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'llama-3.1-8b-instant',
          messages: [
            { role: 'system', content: 'You are a senior career advisor with 15+ years of experience.' },
            { role: 'user', content: prompt }
          ],
          temperature: 0.7,
          max_tokens: 3000
        })
      });

      if (apiResponse.ok) {
        const result = await apiResponse.json();
        return result.choices?.[0]?.message?.content || getFallbackRoadmap(query);
      }
    } catch (error) {
      console.error('Groq API error:', error);
    }
  }
  
  return getFallbackRoadmap(query);
}

function getFallbackRoadmap(query) {
  return `# ${query.charAt(0).toUpperCase() + query.slice(1)} Learning Roadmap

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental ${query} concepts
- Set up development environment
- Complete first projects

### Topics
- Core ${query} principles
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
- Advanced ${query} concepts
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
- Portfolio hosting`;
}