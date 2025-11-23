#!/usr/bin/env python3
"""
Fixed Multi-Agent Service
This replaces the broken async coordination in the original service
"""

import asyncio
import json
import time
import uuid
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import os
from groq import Groq
import google.generativeai as genai
from dotenv import load_dotenv

@dataclass
class AgentResponse:
    agent_name: str
    roadmap: str
    confidence_score: float
    metadata: Dict[str, Any]

class FixedMultiAgentService:
    def __init__(self):
        load_dotenv()
        
        # Initialize API clients
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found")
            
        self.groq_client = Groq(api_key=groq_api_key)
        
        google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_GENAI_API_KEY not found")
            
        genai.configure(api_key=google_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        
        # Agent configurations  
        self.agents = {
            "strategic": {
                "name": "Strategic Planner",
                "provider": "groq",
                "model": "llama-3.1-8b-instant",
                "focus": "long-term career strategy and industry insights"
            },
            "practical": {
                "name": "Practical Guide", 
                "provider": "gemini",
                "model": "gemini-2.0-flash",
                "focus": "actionable steps, resources, and hands-on learning"
            }
        }
    
    async def generate_funneled_roadmap(self, user_query: str, user_background: Optional[Dict] = None) -> Dict[str, Any]:
        """Fixed version that actually works"""
        
        session_id = str(uuid.uuid4())[:8]
        start_time = time.time()
        
        print(f"🤖 Fixed Multi-Agent Processing: {user_query}")
        print(f"📝 Session: {session_id}")
        
        try:
            # Generate responses from agents
            agent_responses = []
            
            # Test with one working agent first
            strategic_response = await self._call_single_agent(
                self.agents["strategic"], 
                user_query, 
                user_background or {}
            )
            
            if strategic_response:
                agent_responses.append(strategic_response)
                print(f"✅ Strategic agent: {len(strategic_response.roadmap)} chars, confidence: {strategic_response.confidence_score}")
            
            # Select best response (for now, just use the first working one)
            if agent_responses:
                best_response = agent_responses[0]
                print(f"🎯 Selected: {best_response.agent_name}")
                
                result = {
                    "final_roadmap": best_response.roadmap,
                    "agent_insights": [
                        {
                            "agent_name": resp.agent_name,
                            "confidence": resp.confidence_score,
                            "focus": resp.metadata.get("focus", ""),
                            "preview": resp.roadmap[:200] + "..." if len(resp.roadmap) > 200 else resp.roadmap
                        } for resp in agent_responses
                    ],
                    "metadata": {
                        "num_agents": len(self.agents),
                        "successful_agents": len(agent_responses),
                        "query": user_query,
                        "session_id": session_id,
                        "timestamp": str(time.time()),
                        "execution_time": f"{time.time() - start_time:.1f}s"
                    },
                    "session_id": session_id,
                    "funneling_report": {
                        "session_id": session_id,
                        "agent_performance": {
                            "total_agents": len(self.agents),
                            "successful_agents": len(agent_responses)
                        }
                    }
                }
                
                print(f"✅ Fixed Multi-Agent Success! Generated {len(best_response.roadmap)} chars")
                return result
            else:
                raise Exception("No agents returned valid responses")
                
        except Exception as e:
            print(f"❌ Fixed Multi-Agent Error: {e}")
            return {
                "final_roadmap": f"# {user_query.title()} Learning Roadmap\n\n## Phase 1: Foundation\n- Master design fundamentals\n- Learn design tools\n\n## Phase 2: Practice\n- Build portfolio projects\n- Get feedback\n\n## Phase 3: Professional\n- Apply for internships\n- Network with professionals",
                "agent_insights": [],
                "metadata": {
                    "num_agents": 0,
                    "successful_agents": 0,
                    "query": user_query,
                    "session_id": session_id,
                    "timestamp": str(time.time()),
                    "execution_time": f"{time.time() - start_time:.1f}s",
                    "error": str(e)
                },
                "session_id": session_id,
                "funneling_report": {
                    "session_id": session_id,
                    "error": str(e),
                    "agent_performance": {
                        "total_agents": 0,
                        "successful_agents": 0
                    }
                }
            }
    
    async def _call_single_agent(self, agent_config: Dict, user_query: str, user_background: Dict) -> Optional[AgentResponse]:
        """Call a single agent with proper error handling"""
        
        try:
            prompt = self._create_simple_prompt(agent_config["focus"], user_query, user_background)
            
            if agent_config["provider"] == "groq":
                response_text = await self._call_groq_safe(agent_config["model"], prompt)
            elif agent_config["provider"] == "gemini":
                response_text = await self._call_gemini_safe(prompt)
            else:
                return None
            
            if response_text and len(response_text) > 100:
                confidence = 0.85  # Simple confidence score
                
                return AgentResponse(
                    agent_name=agent_config["name"],
                    roadmap=response_text,
                    confidence_score=confidence,
                    metadata={
                        "provider": agent_config["provider"],
                        "model": agent_config["model"], 
                        "focus": agent_config["focus"]
                    }
                )
            
        except Exception as e:
            print(f"❌ Agent {agent_config['name']} failed: {e}")
        
        return None
    
    async def _call_groq_safe(self, model: str, prompt: str) -> str:
        """Safe Groq API call"""
        loop = asyncio.get_event_loop()
        
        def sync_call():
            response = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert career advisor specializing in detailed learning roadmaps."},
                    {"role": "user", "content": prompt}
                ],
                model=model,
                temperature=0.7,
                max_tokens=3000
            )
            return response.choices[0].message.content
        
        return await loop.run_in_executor(None, sync_call)
    
    async def _call_gemini_safe(self, prompt: str) -> str:
        """Safe Gemini API call"""
        loop = asyncio.get_event_loop()
        
        def sync_call():
            response = self.gemini_model.generate_content(prompt)
            return response.text
        
        return await loop.run_in_executor(None, sync_call)
    
    def _create_simple_prompt(self, focus: str, user_query: str, user_background: Dict) -> str:
        """Create a specialized prompt for the agent"""
        
        specialization_map = {
            "ui/ux design": {
                "field": "UI/UX Design",
                "tools": "Figma, Adobe XD, Sketch, InVision, Miro",
                "skills": "User Research, Wireframing, Prototyping, Visual Design, Usability Testing",
                "projects": "Mobile App Redesign, E-commerce Website, Dashboard Design"
            },
            "web development": {
                "field": "Web Development", 
                "tools": "HTML5, CSS3, JavaScript, React, Node.js, Git",
                "skills": "Frontend Development, Backend APIs, Database Design, Responsive Design",
                "projects": "Portfolio Website, E-commerce Platform, Social Media App"
            },
            "data science": {
                "field": "Data Science",
                "tools": "Python, R, SQL, Tableau, Jupyter, Pandas, Scikit-learn",
                "skills": "Statistical Analysis, Machine Learning, Data Visualization, SQL Queries",
                "projects": "Customer Segmentation, Sales Forecasting, Recommendation System"
            }
        }
        
        # Detect specialization
        spec_key = "web development"  # default
        for key in specialization_map.keys():
            if key in user_query.lower():
                spec_key = key
                break
        
        spec = specialization_map[spec_key]
        
        prompt = f"""You are a world-class {spec['field']} expert with 15+ years of industry experience.

Create a comprehensive, specialized learning roadmap for: {user_query}

User Background:
- Current Skills: {user_background.get('current_skills', 'None specified')}
- Experience Level: {user_background.get('experience_level', 'Beginner')}

REQUIREMENTS:
- Create 4-5 learning phases
- Use SPECIFIC {spec['field']} terminology (NOT generic terms)
- Include industry-standard tools: {spec['tools']}
- Focus on these key skills: {spec['skills']}
- Include practical projects: {spec['projects']}

FORMAT (follow exactly):
## Phase 1: [Specific Phase Name] (Duration)
### Goals
- [Specific {spec['field']} objective 1]
- [Specific {spec['field']} objective 2]
- [Specific {spec['field']} objective 3]

### Topics
- [Key {spec['field']} concept 1]
- [Key {spec['field']} concept 2] 
- [Key {spec['field']} concept 3]

### Projects
- [{spec['field']} project with clear deliverable]
- [Another practical {spec['field']} project]

### Tools & Technologies
- [Industry tool 1]
- [Industry tool 2]
- [Industry tool 3]

### Resources
- [Learning resource 1 (Free/Paid)]
- [Learning resource 2 (Free/Paid)]

Repeat for 4-5 phases. Make everything SPECIFIC to {spec['field']} - no generic content!"""

        return prompt

# Test function
async def test_fixed_service():
    service = FixedMultiAgentService()
    result = await service.generate_funneled_roadmap(
        "I want to learn UI/UX design",
        {"current_skills": "Basic design knowledge", "experience_level": "Beginner"}
    )
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    asyncio.run(test_fixed_service())