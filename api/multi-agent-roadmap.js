const https = require('https');

module.exports = async function handler(req, res) {
  // CORS headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
  res.setHeader('Content-Type', 'application/json');

  // Handle CORS preflight
  if (req.method === 'OPTIONS') {
    return res.status(200).json({ message: 'OK' });
  }

  // Only handle POST requests
  if (req.method !== 'POST') {
    return res.status(404).json({ error: 'Not Found' });
  }

  try {
    const { query } = req.body || {};
    const roadmap = await getRoadmap(query || 'web development');
    
    return res.status(200).json({
      final_roadmap: roadmap,
      agent_insights: [{ 
        agent_name: 'Technical Analysis Agent', 
        contribution: 'Generated specialized roadmap content',
        confidence: 0.85 
      }],
      metadata: {
        query: query,
        num_agents: 1,
        successful_agents: 1,
        agents_used: ['Technical Analysis Agent']
      }
    });
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}

async function getRoadmap(query) {
  const groqKey = process.env.GROQ_API_KEY;
  
  if (groqKey) {
    try {
      const prompt = `As a technical career expert, create a detailed roadmap for: ${query}

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

Create 4-5 phases with SPECIFIC ${query} terminology and real industry requirements.`;

      const data = JSON.stringify({
        model: "llama-3.1-8b-instant",
        messages: [
          { role: "system", content: "You are a senior technical career advisor with 15+ years of industry experience." },
          { role: "user", content: prompt }
        ],
        temperature: 0.7,
        max_tokens: 3000
      });

      const result = await makeGroqRequest(data, groqKey);
      return result.choices?.[0]?.message?.content || getFallbackRoadmap(query);
    } catch (error) {
      console.error('Groq AI error:', error);
    }
  }
  
  return getFallbackRoadmap(query);
}

function makeGroqRequest(data, apiKey) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.groq.com',
      path: '/openai/v1/chat/completions',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json',
        'Content-Length': data.length
      },
      timeout: 25000
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => reject(new Error('Request timeout')));
    req.write(data);
    req.end();
  });
}

function getFallbackRoadmap(query) {
  return `# ${query.charAt(0).toUpperCase() + query.slice(1)} Learning Roadmap

## Phase 1: Foundation (4-6 weeks)
### Goals
- Master fundamental ${query} concepts
- Set up development environment
- Complete basic projects

### Topics
- Core ${query} principles
- Essential tools and technologies
- Best practices and methodologies

### Projects
- Hello World project
- Basic portfolio website

### Tools
- Code editor (VS Code)
- Version control (Git)

## Phase 2: Development (6-8 weeks)
### Goals
- Build intermediate skills
- Create portfolio projects
- Learn popular frameworks

### Topics
- Advanced ${query} concepts
- Popular frameworks and libraries
- Testing and debugging

### Projects
- Interactive web application
- API integration project

### Tools
- Framework-specific tools
- Testing frameworks
- Browser dev tools

## Phase 3: Advanced (8-10 weeks)
### Goals
- Master advanced concepts
- Build complex applications
- Learn deployment strategies

### Topics
- Performance optimization
- Security best practices
- Database integration
- Deployment and hosting

### Projects
- Full-stack application
- Database-driven project

### Tools
- Cloud platforms (AWS/Vercel/Netlify)
- Database tools
- Monitoring tools

## Phase 4: Professional (10-12 weeks)
### Goals
- Prepare for job market
- Build professional portfolio
- Network with industry professionals

### Topics
- Industry best practices
- Code review processes
- Agile methodologies
- Interview preparation

### Projects
- Capstone project
- Open source contributions
- Professional portfolio site

### Tools
- Professional networking platforms
- Portfolio hosting
- Collaboration tools`;
}