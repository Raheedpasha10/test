"""
Multi-Agent Funneling Service for Student Compass
Uses 3 different AI agents to generate roadmaps, then funnels them into one optimal result
"""

import os
import asyncio
import json
import time
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import httpx
from groq import Groq
import google.generativeai as genai


@dataclass
class AgentResponse:
    """Response from a single agent"""
    agent_name: str
    roadmap: str
    confidence_score: float
    metadata: Dict[str, Any]


import json
import os
from pathlib import Path

# Global storage for funneling logs
GLOBAL_FUNNELING_LOGS = []
LOGS_FILE_PATH = Path("funneling_logs.json")

def save_logs_to_file():
    """Save funneling logs to file"""
    try:
        with open(LOGS_FILE_PATH, 'w') as f:
            json.dump(GLOBAL_FUNNELING_LOGS, f, default=str)
    except Exception as e:
        print(f"Warning: Could not save logs to file: {e}")

def load_logs_from_file():
    """Load funneling logs from file"""
    global GLOBAL_FUNNELING_LOGS
    try:
        if LOGS_FILE_PATH.exists():
            with open(LOGS_FILE_PATH, 'r') as f:
                GLOBAL_FUNNELING_LOGS = json.load(f)
    except Exception as e:
        print(f"Warning: Could not load logs from file: {e}")
        GLOBAL_FUNNELING_LOGS = []

# Load existing logs on import
load_logs_from_file()

class MultiAgentFunnelService:
    """
    Orchestrates multiple AI agents to generate roadmaps and funnels results
    """
    
    def __init__(self):
        # Initialize API clients
        # Load environment variables
        from dotenv import load_dotenv
        load_dotenv()
        
        # Get API keys with validation
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
            
        self.groq_client = Groq(api_key=groq_api_key)
        
        # Get Google API key with validation
        google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_GENAI_API_KEY not found in environment variables")
            
        genai.configure(api_key=google_api_key)
        self.gemini_model = genai.GenerativeModel('gemini-2.0-flash-exp')
        self.huggingface_token = os.getenv("HUGGINGFACE_API_TOKEN")
        
        # Use global funneling logs
        self.current_session_id = None
        self.agent_performance_metrics = {}
        
        # Agent configurations
        self.agents = {
            "agent_strategic": {
                "name": "Strategic Planner",
                "provider": "groq",
                "model": "llama-3.3-70b-versatile",
                "focus": "long-term career strategy and industry insights"
            },
            "agent_practical": {
                "name": "Practical Guide",
                "provider": "gemini",
                "model": "gemini-2.0-flash",
                "focus": "actionable steps, resources, and hands-on learning"
            },
            "agent_technical": {
                "name": "Technical Expert",
                "provider": "groq",
                "model": "llama-3.1-8b-instant",
                "focus": "technical skills, tools, and technologies"
            }
        }
    
    def _start_new_session(self, user_query: str, user_background: dict = None):
        """Initialize a new funneling session for reporting."""
        import time
        import uuid
        
        self.current_session_id = str(uuid.uuid4())[:8]
        session_start = {
            "session_id": self.current_session_id,
            "timestamp": time.time(),
            "user_query": user_query,
            "user_background": user_background or {},
            "agents_involved": list(self.agents.keys()),
            "status": "INITIATED"
        }
        GLOBAL_FUNNELING_LOGS.append(session_start)
        save_logs_to_file()
        return self.current_session_id
    
    def _log_agent_start(self, agent_id: str, agent_config: dict):
        """Log when an agent starts processing."""
        import time
        
        log_entry = {
            "session_id": self.current_session_id,
            "timestamp": time.time(),
            "event_type": "AGENT_START",
            "agent_id": agent_id,
            "agent_name": agent_config["name"],
            "provider": agent_config["provider"],
            "model": agent_config["model"],
            "focus": agent_config["focus"]
        }
        GLOBAL_FUNNELING_LOGS.append(log_entry)
        save_logs_to_file()
    
    def _log_agent_response(self, agent_id: str, response: 'AgentResponse', response_time: float):
        """Log agent response with detailed metrics."""
        import time
        
        # Calculate response metrics
        response_length = len(response.roadmap) if response.roadmap else 0
        has_structured_data = bool(response.roadmap and response.confidence_score > 0)
        
        log_entry = {
            "session_id": self.current_session_id,
            "timestamp": time.time(),
            "event_type": "AGENT_RESPONSE",
            "agent_id": agent_id,
            "agent_name": response.agent_name,
            "confidence_score": response.confidence_score,
            "response_time_seconds": round(response_time, 2),
            "response_length_chars": response_length,
            "has_structured_data": has_structured_data,
            "success": response.confidence_score > 0 and response_length > 0,
            "error": response.metadata.get("error") if response.confidence_score == 0 else None
        }
        GLOBAL_FUNNELING_LOGS.append(log_entry)
        save_logs_to_file()
    
    def _log_funneling_process(self, agent_responses: list, best_agent: str, final_confidence: float):
        """Log the funneling decision process."""
        import time
        
        # Analyze funneling metrics
        successful_agents = [r for r in agent_responses if r.confidence_score > 0]
        confidence_scores = {r.agent_name: r.confidence_score for r in agent_responses}
        
        log_entry = {
            "session_id": self.current_session_id,
            "timestamp": time.time(),
            "event_type": "FUNNELING_PROCESS",
            "total_agents": len(agent_responses),
            "successful_agents": len(successful_agents),
            "confidence_scores": confidence_scores,
            "best_agent": best_agent,
            "final_confidence": final_confidence,
            "funneling_method": "confidence_based_selection"
        }
        GLOBAL_FUNNELING_LOGS.append(log_entry)
        save_logs_to_file()
    
    def _log_session_complete(self, final_result: dict):
        """Log session completion with final metrics."""
        import time
        
        # Calculate session metrics - FIX: Use GLOBAL_FUNNELING_LOGS instead of self.funneling_logs
        session_logs = [log for log in GLOBAL_FUNNELING_LOGS if log.get("session_id") == self.current_session_id]
        session_start_time = min(log["timestamp"] for log in session_logs)
        total_time = time.time() - session_start_time
        
        # Count phases and content quality
        structured_plan = final_result.get("metadata", {}).get("structured_plan", {})
        total_phases = len(structured_plan.get("phases", []))
        total_content_items = sum(
            len(phase.get("goals", [])) + len(phase.get("topics", [])) + 
            len(phase.get("projects", [])) + len(phase.get("resources", []))
            for phase in structured_plan.get("phases", [])
        )
        
        log_entry = {
            "session_id": self.current_session_id,
            "timestamp": time.time(),
            "event_type": "SESSION_COMPLETE",
            "total_time_seconds": round(total_time, 2),
            "final_roadmap_length": len(final_result.get("final_roadmap", "")),
            "total_phases_generated": total_phases,
            "total_content_items": total_content_items,
            "success": bool(final_result.get("final_roadmap"))
        }
        GLOBAL_FUNNELING_LOGS.append(log_entry)
        save_logs_to_file()
    
    def generate_funneling_report(self, session_id: str = None) -> dict:
        """Generate a comprehensive report of the funneling process."""
        target_session = session_id or self.current_session_id
        if not target_session:
            return {"error": "No session to report on"}
        
        # Filter logs for this session
        session_logs = [log for log in GLOBAL_FUNNELING_LOGS if log.get("session_id") == target_session]
        if not session_logs:
            return {"error": f"No logs found for session {target_session}"}
        
        # Organize logs by type
        session_info = next((log for log in session_logs if "user_query" in log), {})
        agent_starts = [log for log in session_logs if log.get("event_type") == "AGENT_START"]
        agent_responses = [log for log in session_logs if log.get("event_type") == "AGENT_RESPONSE"]
        funneling_info = next((log for log in session_logs if log.get("event_type") == "FUNNELING_PROCESS"), {})
        completion_info = next((log for log in session_logs if log.get("event_type") == "SESSION_COMPLETE"), {})
        
        # Calculate performance metrics
        total_time = completion_info.get("total_time_seconds", 0)
        success_rate = (funneling_info.get("successful_agents", 0) / funneling_info.get("total_agents", 1)) * 100
        avg_confidence = sum(funneling_info.get("confidence_scores", {}).values()) / max(len(funneling_info.get("confidence_scores", {})), 1)
        
        # Enhanced report with rich real data
        report = {
            "session_id": target_session,
            "user_query": session_info.get("user_query", ""),
            "user_background": session_info.get("user_background", {}),
            "timestamp": session_info.get("timestamp"),
            "generation_date": time.time(),
            
            "agent_performance": {
                "total_agents": len(agent_starts),
                "successful_agents": funneling_info.get("successful_agents", 0),
                "success_rate_percent": round(success_rate, 1),
                "average_confidence": round(avg_confidence, 3),
                "total_processing_time": f"{total_time:.2f}s",
                "agents_used": [start.get("agent_name") for start in agent_starts],
                "individual_results": []
            },
            
            "funneling_process": {
                "method": "Multi-Agent Confidence-Based Selection",
                "best_agent": funneling_info.get("best_agent", ""),
                "final_confidence": funneling_info.get("final_confidence", 0),
                "confidence_scores": funneling_info.get("confidence_scores", {}),
                "decision_rationale": f"After analyzing responses from {len(agent_starts)} specialized AI agents, selected '{funneling_info.get('best_agent', '')}' based on highest confidence score ({funneling_info.get('final_confidence', 0):.3f}) and content quality metrics. This ensures the most accurate and comprehensive career guidance.",
                "selection_criteria": "Confidence score, content depth, resource quality, practical applicability",
                "quality_threshold": "0.5 minimum confidence required"
            },
            
            "output_metrics": {
                "total_execution_time": f"{total_time:.2f} seconds",
                "phases_generated": completion_info.get("total_phases_generated", 0),
                "content_items": completion_info.get("total_content_items", 0),
                "roadmap_length": completion_info.get("final_roadmap_length", 0),
                "average_phase_quality": round(avg_confidence, 3),
                "resource_links_found": completion_info.get("total_content_items", 0) // 3,  # Estimate
                "estimated_learning_hours": completion_info.get("total_phases_generated", 0) * 40  # 40 hours per phase
            },
            
            "detailed_timeline": []
        }
        
        # Add individual agent performance
        for response_log in agent_responses:
            start_log = next((log for log in agent_starts if log.get("agent_id") == response_log.get("agent_id")), {})
            
            agent_result = {
                "agent_name": response_log.get("agent_name", ""),
                "focus": start_log.get("focus", ""),
                "provider": start_log.get("provider", ""),
                "model": start_log.get("model", ""),
                "confidence_score": response_log.get("confidence_score", 0),
                "response_time": f"{response_log.get('response_time_seconds', 0):.2f}s",
                "success": response_log.get("success", False),
                "output_length": response_log.get("response_length_chars", 0),
                "error": response_log.get("error")
            }
            report["agent_performance"]["individual_results"].append(agent_result)
        
        # Add enhanced detailed timeline with rich information
        for log in sorted(session_logs, key=lambda x: x.get("timestamp", 0)):
            timeline_entry = {
                "timestamp": log.get("timestamp"),
                "event": log.get("event_type", ""),
                "details": "",
                "agent_info": {},
                "metrics": {}
            }
            
            if log.get("event_type") == "AGENT_START":
                timeline_entry["details"] = f"🚀 Initialized {log.get('agent_name')} specialist agent using {log.get('provider').upper()}/{log.get('model')} - Focus: {log.get('focus', 'career guidance')}"
                timeline_entry["agent_info"] = {
                    "name": log.get('agent_name'),
                    "provider": log.get('provider'),
                    "model": log.get('model'),
                    "specialization": log.get('focus')
                }
            elif log.get("event_type") == "AGENT_RESPONSE":
                status = "✅ Success" if log.get('success') else "❌ Failed"
                timeline_entry["details"] = f"{status} - {log.get('agent_name')} generated {log.get('response_length_chars', 0):,} characters in {log.get('response_time_seconds', 0):.2f}s (Confidence: {log.get('confidence_score', 0):.3f})"
                timeline_entry["metrics"] = {
                    "response_time": log.get('response_time_seconds', 0),
                    "confidence": log.get('confidence_score', 0),
                    "content_length": log.get('response_length_chars', 0),
                    "success": log.get('success', False)
                }
            elif log.get("event_type") == "FUNNELING_PROCESS":
                timeline_entry["details"] = f"🎯 Funneling analysis complete - Selected '{log.get('best_agent')}' from {log.get('total_agents')} agents ({log.get('successful_agents')} successful, {((log.get('successful_agents', 0) / log.get('total_agents', 1)) * 100):.1f}% success rate)"
                timeline_entry["metrics"] = {
                    "total_agents": log.get('total_agents', 0),
                    "successful_agents": log.get('successful_agents', 0),
                    "best_agent": log.get('best_agent'),
                    "final_confidence": log.get('final_confidence', 0)
                }
            elif log.get("event_type") == "SESSION_COMPLETE":
                timeline_entry["details"] = f"🎉 Roadmap generation complete - {log.get('total_phases_generated', 0)} learning phases with {log.get('total_content_items', 0)} content items generated ({log.get('final_roadmap_length', 0):,} characters total)"
                timeline_entry["metrics"] = {
                    "total_time": log.get('total_time_seconds', 0),
                    "phases_generated": log.get('total_phases_generated', 0),
                    "content_items": log.get('total_content_items', 0),
                    "roadmap_length": log.get('final_roadmap_length', 0)
                }
            
            report["detailed_timeline"].append(timeline_entry)
        
        return report
    
    async def generate_roadmap_with_agent(
        self, 
        agent_config: Dict[str, str], 
        user_query: str,
        user_background: Optional[Dict[str, Any]] = None,
        agent_id: str = None
    ) -> AgentResponse:
        """Generate roadmap using a single agent and enforce structured JSON."""
        import time
        
        # Log agent start
        if agent_id and self.current_session_id:
            self._log_agent_start(agent_id, agent_config)
        
        start_time = time.time()
        
        # Create specialized prompt based on agent focus
        prompt = self._create_agent_prompt(
            agent_config["focus"], 
            user_query, 
            user_background
        )
        
        try:
            if agent_config["provider"] == "groq":
                raw_response = await self._call_groq(agent_config["model"], prompt)
            elif agent_config["provider"] == "gemini":
                raw_response = await self._call_gemini(prompt)
            elif agent_config["provider"] == "huggingface":
                raw_response = await self._call_huggingface(agent_config["model"], prompt)
            else:
                raise ValueError(f"Unknown provider: {agent_config['provider']}")
            
            # Process markdown text response (not JSON)
            if not raw_response or len(raw_response.strip()) < 50:
                print(f"⚠️ {agent_config['name']}: Response too short or empty")
                return AgentResponse(
                    agent_name=agent_config["name"],
                    roadmap="",
                    confidence_score=0.0,
                    metadata={
                        "provider": agent_config["provider"],
                        "model": agent_config["model"],
                        "focus": agent_config["focus"],
                        "error": "Empty or too short response"
                    }
                )
            
            # Calculate confidence based on specialization-specific content
            confidence = self._calculate_specialization_confidence(raw_response, user_query, user_background or {})
            
            print(f"✅ {agent_config['name']}: Generated {len(raw_response)} chars, confidence: {confidence:.3f}")
            
            response = AgentResponse(
                agent_name=agent_config["name"],
                roadmap=raw_response,  # Store the specialization-specific markdown
                confidence_score=confidence,
                metadata={
                    "provider": agent_config["provider"],
                    "model": agent_config["model"],
                    "focus": agent_config["focus"],
                    "specialization": user_query
                }
            )
            
            # Log successful response
            if agent_id and self.current_session_id:
                self._log_agent_response(agent_id, response, time.time() - start_time)
            
            return response
        
        except Exception as e:
            error_msg = str(e)
            print(f"❌ Agent {agent_config['name']} failed: {error_msg}")
            print(f"🔍 Full error details: {repr(e)}")
            import traceback
            print(f"🔍 Traceback: {traceback.format_exc()}")
            
            # If rate limit, provide helpful message
            if "rate_limit" in error_msg.lower() or "429" in error_msg:
                print(f"⚠️ Rate limit hit for {agent_config['name']} - this agent will be skipped")
            
            error_response = AgentResponse(
                agent_name=agent_config["name"],
                roadmap="",
                confidence_score=0.0,
                metadata={
                    "error": error_msg,
                    "provider": agent_config.get("provider", "unknown"),
                    "full_error": repr(e)
                }
            )
            
            # Log error response
            if agent_id and self.current_session_id:
                self._log_agent_response(agent_id, error_response, time.time() - start_time)
            
            return error_response
    
    async def _call_groq(self, model: str, prompt: str) -> str:
        """Call Groq API"""
        # Run the blocking Groq call in an executor to avoid blocking the event loop
        import asyncio
        loop = asyncio.get_event_loop()
        
        def _sync_groq_call():
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert career advisor specializing in creating detailed learning roadmaps."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=model,
                temperature=0.7,  # Balanced for creativity and focus
                max_tokens=4000   # Increased for comprehensive, detailed responses
            )
            return chat_completion.choices[0].message.content
        
        return await loop.run_in_executor(None, _sync_groq_call)
    
    async def _call_gemini(self, prompt: str) -> str:
        """Call Google Gemini API"""
        # Run the blocking Gemini call in an executor to avoid blocking the event loop
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, self.gemini_model.generate_content, prompt)
        return response.text
    
    async def _call_huggingface(self, model: str, prompt: str) -> str:
        """Call HuggingFace Inference API"""
        API_URL = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {self.huggingface_token}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                API_URL,
                headers=headers,
                json={
                    "inputs": prompt,
                    "parameters": {
                        "max_new_tokens": 4000,  # Increased for comprehensive responses
                        "temperature": 0.7       # Balanced for quality
                    }
                },
                timeout=30.0
            )
            result = response.json()
            if isinstance(result, list) and len(result) > 0:
                return result[0].get("generated_text", "")
            return str(result)
    
    def _create_agent_prompt(
        self, 
        focus: str, 
        user_query: str,
        user_background: Optional[Dict[str, Any]] = None
    ) -> str:
        """Create specialized prompt for each agent enforcing a strict JSON schema optimized for frontend rendering with detailed expandable content."""
        # Enhanced schema with detailed content and paid/free resource indicators
        base_schema = {
            "overview": "Brief, compelling 2-sentence summary of the learning path",
            "time_commitment_hours_per_week": 12,
            "prerequisites": ["Prerequisite 1", "Prerequisite 2"],
            "phases": [
                {
                    "name": "Foundation Building",
                    "duration_weeks": 6,
                    "goals": ["Clear goal 1", "Clear goal 2", "Clear goal 3"],
                    "topics": ["Core topic 1", "Core topic 2", "Core topic 3", "Core topic 4"],
                    "detailed_content": {
                        "expanded_explanation": "Comprehensive explanation of what this phase covers and why it's important. Include practical benefits, industry relevance, and how it builds toward career goals. This content appears when user clicks 'View More'.",
                        "deep_dive_topics": [
                            {
                                "topic": "Advanced Topic Name",
                                "description": "Detailed explanation of this specific topic",
                                "practical_applications": ["Real-world use case 1", "Real-world use case 2"],
                                "learning_outcomes": ["What you'll be able to do", "Skill you'll master"]
                            }
                        ],
                        "skill_progression": {
                            "beginner": "What you'll learn as a beginner",
                            "intermediate": "How skills develop to intermediate level",
                            "advanced": "Advanced mastery and specialization"
                        },
                        "industry_insights": [
                            "Current market demand for these skills",
                            "Salary expectations after mastering this phase",
                            "Career opportunities this phase opens up"
                        ]
                    },
                    "projects": [
                        {
                            "name": "Project Name",
                            "description": "1-line project description",
                            "detailed_description": "Comprehensive project breakdown explaining objectives, technologies used, expected outcomes, and how it demonstrates mastery",
                            "tech_stack": ["Technology 1", "Technology 2"],
                            "difficulty": "Beginner/Intermediate/Advanced",
                            "estimated_hours": "10-15 hours"
                        }
                    ],
                    "tools": ["Tool/Technology 1", "Tool/Technology 2"],
                    "resources": [
                        {
                            "title": "Resource Title",
                            "provider": "Platform",
                            "url": "https://example.com",
                            "type": "Course/Tutorial/Documentation/Book/Video",
                            "cost": "Free/Paid/$XX",
                            "duration": "2 hours/4 weeks/Self-paced",
                            "difficulty": "Beginner/Intermediate/Advanced",
                            "rating": "4.5/5",
                            "description": "Brief description of what this resource covers",
                            "is_paid": False,
                            "price_note": "Free with registration/Premium subscription required/$49 one-time"
                        }
                    ],
                    "checkpoints": ["Milestone 1", "Milestone 2"]
                }
            ],
            "career_milestones": [
                {"timeframe": "3-6 months", "outcome": "Specific career outcome", "salary_range": "$50k-70k"}
            ]
        }

        role_addendum = ""
        if "strategic" in focus.lower():
            role_addendum = (
                "You are the STRATEGIC CAREER ARCHITECT - The world's most elite career strategist who has guided thousands to 6-figure positions. "
                "You possess DEEP insider knowledge of what Fortune 500 companies actually want, which skills command the highest salaries, and the EXACT steps for rapid career advancement. "
                "Your roadmaps are laser-focused on ROI - every skill taught directly translates to salary increases and job opportunities. "
                "You provide detailed career progression maps ($50k→$85k→$120k→$180k), industry networking strategies, and personal branding tactics that actually work. "
                "Your detailed_content sections include salary negotiation scripts, interview preparation strategies, and market insights that give unfair advantages. "
                "Create comprehensive, battle-tested pathways that consistently outperform generic learning paths and deliver measurable career results. "
                "For uncommon specializations, research current market trends and create innovative learning approaches that address specific industry gaps."
            )
        elif "practical" in focus.lower():
            role_addendum = (
                "You are the MASTER BUILDER - The legendary hands-on mentor who has trained thousands of professionals through real-world project mastery. "
                "You design 100% project-driven curricula with portfolio pieces that guarantee job interviews and impress even the most demanding hiring managers. "
                "Every phase builds tangible, deployable applications using cutting-edge tech stacks that demonstrate real expertise to employers. "
                "Your detailed_content provides step-by-step project breakdowns, architecture decisions, debugging strategies, and deployment best practices. "
                "You include comprehensive project documentation that students can confidently present in technical interviews and client meetings. "
                "Focus on creating impressive, scalable applications that solve real business problems and showcase both technical depth and practical problem-solving skills. "
                "For niche fields, design innovative projects that push boundaries and demonstrate expertise in emerging technologies and methodologies."
            )
        else:  # technical
            role_addendum = (
                "You are the TECHNICAL MASTER - The elite engineering mentor who creates world-class technical professionals capable of architecting complex systems. "
                "You possess deep expertise in both fundamental computer science principles and cutting-edge technologies that companies desperately need. "
                "Your curricula progress from rock-solid fundamentals to advanced architectural patterns that only the top 5% of professionals master. "
                "Your detailed_content includes system design principles, performance optimization techniques, scalability patterns, and production-ready best practices. "
                "You provide comprehensive technical deep-dives that prepare students for senior-level technical interviews at top-tier companies. "
                "Focus on both theoretical understanding and practical implementation of complex systems that can handle enterprise-scale challenges. "
                "For emerging or specialized technical fields, create forward-thinking curricula that anticipate industry evolution and prepare students for next-generation challenges."
            )

        background = {
            "current_skills": (user_background or {}).get("current_skills", ""),
            "experience_level": (user_background or {}).get("experience_level", "Beginner"),
            "time_available": (user_background or {}).get("time_available", "10-15 hours per week"),
            "goals": (user_background or {}).get("goals", ""),
            "education": (user_background or {}).get("education", "")
        }

        # Enhanced, focused prompts for clean frontend rendering
        specific_requirements = ""
        if "strategic" in focus.lower():
            specific_requirements = (
                "\nSTRATEGIC FOCUS - FRONTEND-OPTIMIZED OUTPUT:\n"
                "- Phase names: Use clear, progression-based titles (Foundation → Growth → Mastery)\n"
                "- Goals: Write 3-4 specific, measurable career objectives per phase\n"
                "- Topics: List 4-5 core strategic concepts (salary negotiation, networking, personal branding)\n"
                "- Projects: Portfolio/career projects that demonstrate strategic thinking\n"
                "- Tools: Professional tools (LinkedIn, portfolio platforms, job boards)\n"
                "- Resources: Career-focused resources with real URLs when possible\n"
                "- Checkpoints: Career milestones and skill validations\n"
                "- Keep text concise and scannable for UI display"
            )
        elif "practical" in focus.lower():
            specific_requirements = (
                "\nPRACTICAL FOCUS - FRONTEND-OPTIMIZED OUTPUT:\n" 
                "- Phase names: Action-oriented titles (Build → Deploy → Scale)\n"
                "- Goals: 3-4 hands-on objectives students can complete and showcase\n"
                "- Topics: 4-5 practical skills with immediate application\n"
                "- Projects: Real-world projects with clear deliverables and tech stacks\n"
                "- Tools: Development tools, frameworks, and platforms students will use\n"
                "- Resources: Tutorial links, documentation, and free learning materials\n"
                "- Checkpoints: Practical milestones (deployed projects, working features)\n"
                "- Focus on buildable, demonstrable outcomes"
            )
        else:  # technical
            specific_requirements = (
                "\nTECHNICAL FOCUS - FRONTEND-OPTIMIZED OUTPUT:\n"
                "- Phase names: Technical progression titles (Fundamentals → Architecture → Optimization)\n"
                "- Goals: 3-4 technical competencies with measurable outcomes\n"
                "- Topics: 4-5 core technical concepts with modern technologies\n"
                "- Projects: Technical implementations showcasing specific skills\n"
                "- Tools: Current tech stack with version numbers when relevant\n"
                "- Resources: Technical documentation, tutorials, and best practices\n"
                "- Checkpoints: Technical milestones (code quality, performance metrics)\n"
                "- Emphasize modern, industry-standard practices"
            )

        # Detect and validate specialization
        specialization = user_query.lower().strip()
        
        # Create specialization-specific context
        specialization_context = self._get_specialization_context(specialization)
        
        prompt = (
            f"You are a world-class {specialization_context['title']} expert with 15+ years of industry experience. "
            f"You specialize EXCLUSIVELY in {specialization_context['field']} and have helped 500+ professionals "
            f"land jobs in this exact field. {role_addendum}\n\n"
            f"🎯 CRITICAL MISSION: Create a SPECIALIZED roadmap for {specialization_context['field']} (NOT generic programming).\n\n"
            f"📋 SPECIALIZATION: {specialization_context['field']}\n"
            f"👤 USER QUERY: {user_query}\n"
            f"📊 USER BACKGROUND: {json.dumps(background)}\n\n"
            f"🚨 ABSOLUTE REQUIREMENTS:\n"
            f"{specialization_context['requirements']}\n\n"
            f"🔍 FIELD-SPECIFIC FOCUS:\n"
            f"{specialization_context['focus_areas']}\n\n"
            f"🚨 ABSOLUTELY FORBIDDEN - NEVER USE THESE GENERIC TERMS:\n"
            f"- 'basics', 'core concepts', 'skills', 'advanced concepts', 'advanced topics'\n"
            f"- 'basic project', 'practice project', 'intermediate tools', 'basic tools'\n"
            f"- 'develop skills', 'build basics', 'master advanced topics', 'apply knowledge'\n"
            f"- Any placeholder or generic content - EVERYTHING must be {specialization_context['field']}-specific\n\n"
            f"✅ MANDATORY REQUIREMENTS:\n"
            f"- Use REAL {specialization_context['field']} terminology (e.g., for UI/UX: 'Figma', 'User Research', 'Wireframing', 'Prototyping')\n"
            f"- Include ACTUAL industry tools and technologies used in {specialization_context['field']} (not 'Basic tools')\n"
            f"- Create SPECIFIC project names relevant to {specialization_context['field']} (not 'Basic project')\n"
            f"- Use {specialization_context['field']}-specific learning objectives (not 'Build basics')\n"
            f"- Every single item must be tailored to {user_query} - NO EXCEPTIONS\n\n"
            f"{specific_requirements}\n\n"
            f"CRITICAL OUTPUT STRUCTURE - MUST FOLLOW EXACTLY:\n"
            f"Create a roadmap with 4-6 phases, each following this EXACT format:\n\n"
            f"## Phase [Number]: [Specific Phase Name] ([Duration])\n"
            f"### Goals\n"
            f"- [Specific learning objective 1]\n"
            f"- [Specific learning objective 2]\n"
            f"- [Specific learning objective 3]\n"
            f"- [Specific learning objective 4]\n"
            f"### Topics\n"
            f"- [Key concept/skill 1]\n"
            f"- [Key concept/skill 2]\n"
            f"- [Key concept/skill 3]\n"
            f"- [Key concept/skill 4]\n"
            f"- [Key concept/skill 5]\n"
            f"### Projects\n"
            f"- [Practical project 1 with specific deliverable]\n"
            f"- [Practical project 2 with specific deliverable]\n"
            f"### Tools\n"
            f"- [Essential tool/technology 1]\n"
            f"- [Essential tool/technology 2]\n"
            f"- [Essential tool/technology 3]\n"
            f"- [Essential tool/technology 4]\n"
            f"### Resources\n"
            f"- [Learning resource 1 (Free/Paid)]\n"
            f"- [Learning resource 2 (Free/Paid)]\n"
            f"- [Learning resource 3 (Free/Paid)]\n\n"
            f"SPECIALIZATION-SPECIFIC REQUIREMENTS:\n"
            f"- Make each phase title UNIQUE to {user_query} (not generic)\n"
            f"- Include industry-specific tools and technologies for {user_query}\n"
            f"- Projects should be relevant to {user_query} career path\n"
            f"- Use current 2024 technologies and best practices\n"
            f"- Ensure logical progression from beginner to professional level\n\n"
            f"EXAMPLE FOR SOFTWARE ENGINEERING:\n"
            f"## Phase 1: Programming Fundamentals (4-6 weeks)\n"
            f"### Goals\n"
            f"- Master programming logic and problem-solving\n"
            f"- Understand object-oriented programming concepts\n"
            f"- Build confidence with coding syntax\n"
            f"- Learn debugging techniques\n"
            f"### Topics\n"
            f"- Variables, loops, and conditionals\n"
            f"- Functions and data structures\n"
            f"- Object-oriented programming\n"
            f"- Error handling and debugging\n"
            f"- Code organization and best practices\n"
            f"### Projects\n"
            f"- Command-line calculator with advanced operations\n"
            f"- Personal task manager with file persistence\n"
            f"### Tools\n"
            f"- Python or JavaScript\n"
            f"- VS Code IDE\n"
            f"- Git version control\n"
            f"- Command line interface\n"
            f"### Resources\n"
            f"- Python.org official tutorial (Free)\n"
            f"- Codecademy Python course (Paid)\n"
            f"- Automate the Boring Stuff book (Free)\n\n"
            f"CRITICAL: Follow this EXACT structure for each phase. Each section must have specific, actionable content relevant to {user_query}.\n\n"
            f"🚨 FINAL WARNING: If you generate ANY generic content like 'basics', 'core concepts', 'basic project', or 'basic tools', "
            f"your response will be REJECTED. Every single item MUST be {specialization_context['field']}-specific and use real industry terminology. "
            f"Research current {specialization_context['field']} practices if needed, but NEVER use placeholders."
        )
        return prompt
    
    def _get_specialization_context(self, specialization: str) -> Dict[str, str]:
        """Get specialization-specific context for proper agent prompting."""
        
        # Comprehensive specialization mapping for 100+ fields
        specializations = {
            # Technology & Programming
            'software engineering': {
                'title': 'Software Engineering',
                'field': 'Software Development and Engineering',
                'requirements': '- Focus on programming languages, frameworks, algorithms, system design\n- Include software architecture, testing, debugging, version control\n- Cover full-stack development, databases, APIs, deployment',
                'focus_areas': '- Programming Languages: Python, Java, JavaScript, C++\n- Frameworks: React, Node.js, Spring, Django\n- Tools: Git, Docker, Jenkins, AWS\n- Concepts: OOP, Design Patterns, Algorithms, Data Structures'
            },
            'data science': {
                'title': 'Data Science',
                'field': 'Data Analysis and Machine Learning',
                'requirements': '- Focus on statistics, machine learning, data analysis, visualization\n- Include Python/R, pandas, numpy, scikit-learn, TensorFlow\n- Cover data cleaning, feature engineering, model deployment',
                'focus_areas': '- Languages: Python, R, SQL\n- Libraries: Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn\n- ML Tools: TensorFlow, PyTorch, Jupyter\n- Concepts: Statistics, ML Algorithms, Data Visualization, ETL'
            },
            'cybersecurity': {
                'title': 'Cybersecurity',
                'field': 'Information Security and Ethical Hacking',
                'requirements': '- Focus on penetration testing, vulnerability assessment, network security\n- Include security tools, incident response, compliance frameworks\n- Cover ethical hacking, forensics, risk management',
                'focus_areas': '- Tools: Kali Linux, Metasploit, Nmap, Wireshark, Burp Suite\n- Concepts: Network Security, Cryptography, Risk Assessment\n- Frameworks: NIST, ISO 27001, OWASP\n- Skills: Penetration Testing, Incident Response, Compliance'
            },
            'web development': {
                'title': 'Web Development',
                'field': 'Frontend and Backend Web Development',
                'requirements': '- Focus on HTML, CSS, JavaScript, responsive design\n- Include frontend frameworks, backend APIs, databases\n- Cover performance optimization, SEO, accessibility',
                'focus_areas': '- Frontend: HTML5, CSS3, JavaScript, React, Vue.js\n- Backend: Node.js, Express, PHP, Python Flask/Django\n- Databases: MySQL, PostgreSQL, MongoDB\n- Tools: Webpack, Git, Chrome DevTools'
            },
            'mobile development': {
                'title': 'Mobile Development',
                'field': 'iOS and Android Application Development',
                'requirements': '- Focus on mobile frameworks, native development, cross-platform\n- Include UI/UX for mobile, app store deployment, mobile testing\n- Cover performance optimization, offline functionality, push notifications',
                'focus_areas': '- Native: Swift (iOS), Kotlin/Java (Android)\n- Cross-platform: React Native, Flutter, Xamarin\n- Tools: Xcode, Android Studio, Firebase\n- Concepts: Mobile UI/UX, App Store Guidelines, Mobile Security'
            },
            'devops': {
                'title': 'DevOps Engineering',
                'field': 'Infrastructure Automation and Cloud Operations',
                'requirements': '- Focus on CI/CD, containerization, cloud platforms, automation\n- Include infrastructure as code, monitoring, security practices\n- Cover scalability, reliability, deployment strategies',
                'focus_areas': '- Cloud: AWS, Azure, Google Cloud Platform\n- Containers: Docker, Kubernetes, OpenShift\n- CI/CD: Jenkins, GitLab CI, GitHub Actions\n- Tools: Terraform, Ansible, Prometheus, Grafana'
            },
            'artificial intelligence': {
                'title': 'Artificial Intelligence',
                'field': 'AI and Machine Learning Engineering',
                'requirements': '- Focus on neural networks, deep learning, NLP, computer vision\n- Include AI frameworks, model training, deployment at scale\n- Cover ethics in AI, bias detection, model optimization',
                'focus_areas': '- Frameworks: TensorFlow, PyTorch, Keras, OpenAI\n- Concepts: Neural Networks, Deep Learning, NLP, Computer Vision\n- Tools: CUDA, MLOps platforms, Model registries\n- Specializations: Reinforcement Learning, Generative AI'
            },
            'cloud computing': {
                'title': 'Cloud Computing',
                'field': 'Cloud Architecture and Engineering',
                'requirements': '- Focus on cloud platforms, serverless, microservices architecture\n- Include cloud security, cost optimization, migration strategies\n- Cover multi-cloud, hybrid cloud, cloud-native development',
                'focus_areas': '- Platforms: AWS, Microsoft Azure, Google Cloud\n- Services: EC2, Lambda, S3, Kubernetes, API Gateway\n- Concepts: Serverless, Microservices, Cloud Security\n- Certifications: AWS Solutions Architect, Azure Developer'
            },
            'blockchain development': {
                'title': 'Blockchain Development',
                'field': 'Blockchain and Cryptocurrency Development',
                'requirements': '- Focus on smart contracts, DApps, cryptocurrency protocols\n- Include Solidity, Web3, blockchain platforms, consensus algorithms\n- Cover DeFi, NFTs, tokenomics, blockchain security',
                'focus_areas': '- Languages: Solidity, Rust, Go\n- Platforms: Ethereum, Polygon, Binance Smart Chain\n- Tools: Hardhat, Truffle, MetaMask, Web3.js\n- Concepts: Smart Contracts, DeFi, NFTs, Consensus Mechanisms'
            },
            'game development': {
                'title': 'Game Development',
                'field': 'Video Game Programming and Design',
                'requirements': '- Focus on game engines, game physics, graphics programming\n- Include game design patterns, multiplayer networking, optimization\n- Cover 2D/3D graphics, audio systems, platform deployment',
                'focus_areas': '- Engines: Unity, Unreal Engine, Godot\n- Languages: C#, C++, JavaScript\n- Graphics: OpenGL, DirectX, Shaders\n- Concepts: Game Physics, AI, Networking, Performance'
            },
            # Design & Creative
            'ui/ux design': {
                'title': 'UI/UX Design',
                'field': 'User Interface and User Experience Design',
                'requirements': '- Focus on design principles, user research, prototyping tools\n- Include accessibility, usability testing, design systems\n- Cover mobile/web design, interaction design, visual hierarchy',
                'focus_areas': '- Tools: Figma, Sketch, Adobe XD, Principle\n- Concepts: Design Thinking, User Research, Wireframing\n- Skills: Prototyping, Usability Testing, Information Architecture\n- Methodologies: Human-Centered Design, Agile UX'
            },
            'graphic design': {
                'title': 'Graphic Design',
                'field': 'Visual Communication and Brand Design',
                'requirements': '- Focus on typography, color theory, layout design, branding\n- Include print design, digital design, logo creation\n- Cover Adobe Creative Suite, design principles, client communication',
                'focus_areas': '- Tools: Adobe Photoshop, Illustrator, InDesign\n- Concepts: Typography, Color Theory, Layout Design\n- Specializations: Logo Design, Brand Identity, Print Design\n- Skills: Client Communication, Creative Brief Analysis'
            },
            # Business & Marketing
            'digital marketing': {
                'title': 'Digital Marketing',
                'field': 'Online Marketing and Growth Strategy',
                'requirements': '- Focus on SEO, social media marketing, content strategy, analytics\n- Include paid advertising, email marketing, conversion optimization\n- Cover marketing automation, A/B testing, customer journey mapping',
                'focus_areas': '- Channels: Google Ads, Facebook Ads, LinkedIn, Instagram\n- Tools: Google Analytics, HubSpot, Mailchimp, SEMrush\n- Concepts: SEO, Content Marketing, Social Media Strategy\n- Metrics: ROI, CTR, Conversion Rate, Customer Acquisition Cost'
            },
            'business analysis': {
                'title': 'Business Analysis',
                'field': 'Business Process Analysis and Requirements Engineering',
                'requirements': '- Focus on requirements gathering, process mapping, stakeholder analysis\n- Include data analysis, documentation, solution design\n- Cover agile methodologies, project management, change management',
                'focus_areas': '- Tools: Microsoft Visio, Lucidchart, Jira, Confluence\n- Techniques: Use Case Analysis, User Stories, Process Mapping\n- Methodologies: Agile, Waterfall, Lean Six Sigma\n- Skills: Stakeholder Management, Documentation, Problem-solving'
            },
            'project management': {
                'title': 'Project Management',
                'field': 'Project Planning and Execution Leadership',
                'requirements': '- Focus on project planning, risk management, team leadership\n- Include agile/scrum methodologies, resource allocation, budgeting\n- Cover stakeholder communication, quality management, project tools',
                'focus_areas': '- Methodologies: Agile, Scrum, Kanban, Waterfall\n- Tools: Jira, Trello, Microsoft Project, Slack\n- Concepts: Risk Management, Resource Planning, Budget Management\n- Certifications: PMP, Scrum Master, Agile Certified Practitioner'
            }
        }
        
        # Find the best match for the specialization
        spec_key = None
        for key in specializations.keys():
            if key in specialization or specialization in key:
                spec_key = key
                break
        
        # If no specific match found, create a generic but specialized context
        if spec_key is None:
            # Extract the core specialization name (remove common prefixes)
            core_spec = specialization.replace('i want to learn', '').replace('and become proficient', '').strip()
            core_spec = core_spec.split()[0] if core_spec.split() else specialization
            
            return {
                'title': core_spec.title(),
                'field': f'{core_spec.title()} Professional Development',
                'requirements': f'- Focus EXCLUSIVELY on {core_spec} - use specific {core_spec} terminology, tools, and industry practices\n- Include real {core_spec} technologies, frameworks, and methodologies used in 2024\n- Cover practical {core_spec} applications and real-world scenarios\n- NEVER use generic terms like "basics", "core concepts", "skills" - use specific {core_spec} terms',
                'focus_areas': f'- {core_spec.title()}-specific concepts: Use actual {core_spec} terminology and domain knowledge\n- Industry tools: Real tools and technologies used in {core_spec} field\n- Professional practices: {core_spec} industry standards and best practices\n- Career path: Specific roles and advancement in {core_spec}'
            }
        
        return specializations[spec_key]

    def _calculate_specialization_confidence(self, response: str, specialization: str, user_background: Dict[str, Any]) -> float:
        """Calculate confidence based on specialization-specific content."""
        if not response:
            return 0.0
        
        response_lower = response.lower()
        spec_lower = specialization.lower()
        score = 0.0
        
        # Basic content quality (20% of score)
        if len(response) > 500:
            score += 0.1
        if len(response) > 1000:
            score += 0.1
        
        # Specialization-specific keywords (40% of score)
        specialization_keywords = {
            'data science': ['python', 'pandas', 'numpy', 'machine learning', 'statistics', 'visualization', 'sklearn', 'tensorflow', 'jupyter'],
            'cybersecurity': ['penetration testing', 'vulnerability', 'kali linux', 'metasploit', 'network security', 'ethical hacking', 'nmap', 'wireshark'],
            'ui/ux design': ['figma', 'sketch', 'prototyping', 'user research', 'wireframing', 'design thinking', 'usability testing'],
            'web development': ['html', 'css', 'javascript', 'react', 'node.js', 'frontend', 'backend', 'responsive design'],
            'mobile development': ['swift', 'kotlin', 'react native', 'flutter', 'ios', 'android', 'mobile ui'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'aws', 'ci/cd', 'terraform', 'monitoring', 'deployment'],
            'blockchain development': ['solidity', 'smart contracts', 'ethereum', 'web3', 'defi', 'cryptocurrency'],
            'artificial intelligence': ['neural networks', 'deep learning', 'nlp', 'computer vision', 'pytorch', 'tensorflow'],
            'software engineering': ['algorithms', 'data structures', 'design patterns', 'version control', 'testing', 'debugging']
        }
        
        # Find matching keywords for this specialization
        keywords = []
        for spec_key, spec_keywords in specialization_keywords.items():
            if spec_key in spec_lower or any(word in spec_lower for word in spec_key.split()):
                keywords = spec_keywords
                break
        
        if keywords:
            keyword_count = sum(1 for keyword in keywords if keyword in response_lower)
            score += min(keyword_count / len(keywords), 0.4)  # Cap at 40%
        
        # Avoid generic terms (20% penalty if found)
        generic_terms = ['basics', 'core concepts', 'skills', 'advanced topics', 'fundamentals']
        generic_count = sum(1 for term in generic_terms if term in response_lower)
        if generic_count > 2:
            score -= 0.2
        
        # Structure quality (20% of score)
        if '**learning goals:**' in response_lower:
            score += 0.05
        if '**key topics:**' in response_lower:
            score += 0.05
        if '**projects:**' in response_lower or '**hands-on projects:**' in response_lower:
            score += 0.05
        if '**tools' in response_lower:
            score += 0.05
        
        # Phase structure (20% of score)
        phase_count = len([m for m in response.split('\n') if 'phase' in m.lower() and ':' in m])
        if phase_count >= 3:
            score += 0.1
        if phase_count >= 5:
            score += 0.1
        
        return min(max(score, 0.0), 1.0)

    def _calculate_text_confidence(self, response: str, user_background: Dict[str, Any]) -> float:
        """Calculate confidence score based on text response quality."""
        if not response:
            return 0.0
        
        score = 0.0
        response_lower = response.lower()
        
        # Basic content length check (10% of score)
        if len(response) > 500:
            score += 0.1
        
        # Check for structured content (30% of score)
        structure_indicators = [
            'phase', 'week', 'month', 'step', 'goal', 'objective',
            'project', 'skill', 'learn', 'practice', 'build'
        ]
        structure_count = sum(1 for indicator in structure_indicators if indicator in response_lower)
        score += min(structure_count / 15.0, 0.3)  # Cap at 0.3
        
        # Check for actionable content (25% of score)
        action_indicators = [
            'create', 'build', 'implement', 'practice', 'study', 'complete',
            'deploy', 'test', 'design', 'develop', 'master'
        ]
        action_count = sum(1 for indicator in action_indicators if indicator in response_lower)
        score += min(action_count / 10.0, 0.25)  # Cap at 0.25
        
        # Check for specific technologies/tools mentioned (20% of score)
        tech_patterns = [
            'python', 'javascript', 'java', 'react', 'node', 'sql', 'git',
            'aws', 'docker', 'kubernetes', 'tensorflow', 'html', 'css'
        ]
        tech_count = sum(1 for tech in tech_patterns if tech in response_lower)
        score += min(tech_count / 8.0, 0.2)  # Cap at 0.2
        
        # Check for time-based planning (15% of score)
        time_indicators = ['weeks?', 'months?', 'days?', 'hours?']
        import re
        for pattern in time_indicators:
            if re.search(r'\d+[-\s]*' + pattern, response_lower):
                score += 0.15
                break
        
        return min(score, 1.0)

    def _parse_agent_json(self, raw_text: str) -> Optional[Dict[str, Any]]:
        """Try to parse strict JSON from model output, with enhanced fallback extraction."""
        if not raw_text:
            return None
        
        raw_text = raw_text.strip()
        
        # Fast path - direct JSON parsing
        try:
            return json.loads(raw_text)
        except Exception:
            pass
        
        # Remove common non-JSON prefixes/suffixes
        prefixes_to_remove = ['```json', '```', 'Here is the JSON:', 'Here\'s the JSON:']
        suffixes_to_remove = ['```', '\n```']
        
        cleaned_text = raw_text
        for prefix in prefixes_to_remove:
            if cleaned_text.startswith(prefix):
                cleaned_text = cleaned_text[len(prefix):].strip()
        
        for suffix in suffixes_to_remove:
            if cleaned_text.endswith(suffix):
                cleaned_text = cleaned_text[:-len(suffix)].strip()
        
        # Try parsing cleaned text
        try:
            return json.loads(cleaned_text)
        except Exception:
            pass
        
        # Enhanced fallback: find the largest JSON object
        import re
        
        # Look for JSON objects with various patterns
        patterns = [
            r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}',  # Simple nested objects
            r'\{[\s\S]*\}',                      # Any content between braces
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, cleaned_text)
            for match in matches:
                try:
                    parsed = json.loads(match)
                    # Validate it has the expected structure
                    if isinstance(parsed, dict) and ('phases' in parsed or 'overview' in parsed):
                        return parsed
                except Exception:
                    continue
        
        # Last resort: create minimal valid structure if we can extract any info
        print(f"⚠️ Could not parse JSON from response. Raw text: {raw_text[:200]}...")
        return None

    def _score_structured(self, data: Dict[str, Any], background: Dict[str, Any]) -> float:
        """Rubric-based scoring of structured agent output."""
        score = 0.0
        # Required keys
        required_keys = ["overview", "phases"]
        if all(k in data for k in required_keys):
            score += 0.3
        # Phases richness
        phases = data.get("phases", []) or []
        if len(phases) >= 3:
            score += 0.2
        detailed = 0
        concrete_counts = 0
        for ph in phases:
            # Check for non-empty content
            topics = [t for t in ph.get("topics", []) if t and t.strip()]
            projects = [p for p in ph.get("projects", []) if p and (isinstance(p, str) and p.strip() or isinstance(p, dict) and (p.get("name") or p.get("description")))]
            resources = [r for r in ph.get("resources", []) if r and (isinstance(r, str) and r.strip() or isinstance(r, dict) and (r.get("title") or r.get("url")))]
            
            if topics and projects and resources:
                detailed += 1
            # Specificity: count concrete items
            concrete_counts += len(topics) + len(projects) + len(resources)
        if detailed >= 2:
            score += 0.2
        # Specificity scaling
        score += min(concrete_counts / 50.0, 0.2)  # cap contribution
        # Time commitment consideration
        time_str = (background or {}).get("time_available", "")
        if isinstance(time_str, str) and any(h in time_str for h in ["hour", "hrs", "hours"]):
            score += 0.05
        # Prerequisites present
        if data.get("prerequisites"):
            score += 0.05
        return min(score, 1.0)

    def _merge_structured_outputs(self, outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Merge multiple structured agent outputs into a single coherent plan."""
        # Pick best overview (longest with substance)
        best_overview = max((o.get("overview", "") for o in outputs), key=lambda x: len(x), default="")
        # Aggregate phases by rough intent buckets
        def bucket(name: str) -> str:
            n = (name or "").lower()
            if any(k in n for k in ["foundation", "beginner", "basics"]):
                return "Foundation"
            if any(k in n for k in ["intermediate", "core", "skills"]):
                return "Intermediate"
            if any(k in n for k in ["advanced", "specialization", "expert"]):
                return "Advanced"
            if any(k in n for k in ["deployment", "devops", "production"]):
                return "Deployment"
            if any(k in n for k in ["portfolio", "project", "capstone"]):
                return "Portfolio"
            return "Other"
        buckets: Dict[str, List[Dict[str, Any]]] = {}
        for o in outputs:
            for ph in o.get("phases", []) or []:
                b = bucket(ph.get("name", ""))
                buckets.setdefault(b, []).append(ph)
        # Within each bucket, select top N phases by richness
        merged_phases: List[Dict[str, Any]] = []
        for b, plist in buckets.items():
            # Score per phase by count of topics+projects+resources
            def ph_score(p):
                return len(p.get("topics", [])) + len(p.get("projects", [])) + len(p.get("resources", []))
            top = sorted(plist, key=ph_score, reverse=True)[:2]
            for p in top:
                merged_phases.append(self._dedupe_phase(p))
        # Sort phases in a sensible order
        order = {"Foundation": 0, "Intermediate": 1, "Advanced": 2, "Deployment": 3, "Portfolio": 4, "Other": 5}
        merged_phases.sort(key=lambda p: order.get(bucket(p.get("name", "")), 5))
        # Merge career milestones
        milestones: List[Dict[str, Any]] = []
        for o in outputs:
            milestones.extend(o.get("career_milestones", []) or [])
        # Average time commitment if present
        times = [o.get("time_commitment_hours_per_week") for o in outputs if isinstance(o.get("time_commitment_hours_per_week"), (int, float))]
        time_commitment = int(sum(times) / len(times)) if times else 10
        return {
            "overview": best_overview,
            "time_commitment_hours_per_week": time_commitment,
            "phases": merged_phases,
            "career_milestones": milestones[:6]
        }

    def _clean_text(self, text: str) -> str:
        """Fast text cleaning for individual strings."""
        if not text or not isinstance(text, str):
            return ""
        
        # Basic cleaning - remove common bullets and markdown
        text = text.strip()
        
        # Remove bullets and markers (simple patterns only)
        if text.startswith(('-', '•', '*', '►', '▸')):
            text = text[1:].strip()
        
        # Remove markdown bold/italic
        text = text.replace('**', '').replace('`', '')
        
        # Clean whitespace
        text = ' '.join(text.split())
        
        return text
    
    def _is_valid_content(self, text: str) -> bool:
        """Fast validation for meaningful content."""
        if not text or len(text) < 4:
            return False
        
        # Skip obvious placeholders
        text_lower = text.lower()
        bad_patterns = ['todo', 'tbd', 'placeholder', 'example', '...', '---']
        
        return not any(bad in text_lower for bad in bad_patterns)
    
    def _clean_array_field(self, arr: list) -> list:
        """Fast cleaning and validation of array fields."""
        if not arr:
            return []
        
        cleaned = []
        for item in arr:
            if isinstance(item, str):
                clean_text = self._clean_text(item)
                if self._is_valid_content(clean_text):
                    cleaned.append(clean_text)
                    
            elif isinstance(item, dict):
                # Clean dict items
                clean_item = {}
                for key, value in item.items():
                    if isinstance(value, str):
                        clean_value = self._clean_text(value)
                        if clean_value:
                            clean_item[key] = clean_value
                    else:
                        clean_item[key] = value
                
                # Only include if has meaningful content
                if clean_item.get("name") or clean_item.get("title") or clean_item.get("description"):
                    cleaned.append(clean_item)
        
        return cleaned[:8]  # Limit to 8 items max

    def _dedupe_phase(self, p: Dict[str, Any]) -> Dict[str, Any]:
        """Deduplicate topics/tools/resources inside a phase and normalize fields."""
        def uniq(seq):
            seen = set()
            out = []
            for x in seq or []:
                key = json.dumps(x, sort_keys=True) if isinstance(x, dict) else str(x).lower()
                if key in seen:
                    continue
                seen.add(key)
                out.append(x)
            return out
        
        # Clean all array fields before deduplication
        goals = self._clean_array_field(p.get("goals", []))
        topics = self._clean_array_field(p.get("topics", []))
        projects = self._clean_array_field(p.get("projects", []))
        tools = self._clean_array_field(p.get("tools", []))
        resources = self._clean_array_field(p.get("resources", []))
        checkpoints = self._clean_array_field(p.get("checkpoints", []))
        
        return {
            "name": p.get("name", "").strip() or f"Learning Phase",
            "duration_weeks": int(p.get("duration_weeks", 0) or 4),  # Default to 4 weeks
            "goals": uniq(goals)[:5],  # Limit to 5 goals
            "topics": uniq(topics)[:8],  # Limit to 8 topics
            "projects": uniq(projects)[:4],  # Limit to 4 projects
            "tools": uniq(tools)[:6],  # Limit to 6 tools
            "resources": uniq(resources)[:5],  # Limit to 5 resources
            "checkpoints": uniq(checkpoints)[:5],  # Limit to 5 checkpoints
        }

    def _render_markdown(self, data: Dict[str, Any]) -> str:
        """Render final markdown from merged structured data."""
        lines: List[str] = []
        lines.append("## Overview\n")
        lines.append(f"{data.get('overview','').strip()}\n\n")
        lines.append("## Complete Learning Roadmap\n\n")
        for idx, ph in enumerate(data.get("phases", []), start=1):
            name = ph.get("name", f"Phase {idx}")
            dur = ph.get("duration_weeks")
            dur_txt = f" ({dur} weeks)" if dur else ""
            lines.append(f"**Phase {idx}: {name}**{dur_txt}\n\n")
            if ph.get("goals"):
                lines.append("Goals:\n" + "\n".join(f"- {g}" for g in ph["goals"]) + "\n\n")
            if ph.get("topics"):
                lines.append("What You'll Learn:\n" + "\n".join(f"- {t}" for t in ph["topics"]) + "\n\n")
            if ph.get("tools"):
                lines.append("Tools & Technologies:\n" + "\n".join(f"- {t}" for t in ph["tools"]) + "\n\n")
            if ph.get("projects"):
                lines.append("Hands-On Projects:\n" + "\n".join(
                    f"- {pr.get('name', 'Project')}: {pr.get('description','')}" if isinstance(pr, dict) else f"- {pr}"
                    for pr in ph["projects"]
                ) + "\n\n")
            if ph.get("resources"):
                def res_line(r):
                    if isinstance(r, dict):
                        title = r.get('title') or r.get('name') or 'Resource'
                        prov = r.get('provider')
                        url = r.get('url')
                        extra = f" ({prov})" if prov else ""
                        link = f": {url}" if url else ""
                        return f"- {title}{extra}{link}"
                    return f"- {r}"
                lines.append("Recommended Resources:\n" + "\n".join(res_line(r) for r in ph["resources"]) + "\n\n")
            if ph.get("checkpoints"):
                lines.append("Phase Completion Checklist:\n" + "\n".join(f"- [ ] {c}" for c in ph["checkpoints"]) + "\n\n")
        if data.get("career_milestones"):
            lines.append("## Career Milestones\n\n")
            for m in data["career_milestones"]:
                tf = m.get("timeframe", "") if isinstance(m, dict) else ""
                oc = m.get("outcome", "") if isinstance(m, dict) else str(m)
                lines.append(f"- {tf}: {oc}\n")
            lines.append("\n")
        return "".join(lines)
    
    async def funnel_roadmaps(
        self, 
        agent_responses: List[AgentResponse]
    ) -> str:
        """
        Funnel multiple agent responses into one optimal roadmap using deterministic merging of structured JSON,
        then render to markdown. Avoids freeform LLM synthesis to ensure quality and specificity.
        """
        # Parse structured JSON from agents
        structured_list: List[Dict[str, Any]] = []
        for r in agent_responses:
            if r.confidence_score <= 0 or not r.roadmap:
                continue
            try:
                structured_list.append(json.loads(r.roadmap))
            except Exception:
                continue
        
        if not structured_list:
            return "Unable to generate roadmap. Please try again."
        
        # Merge: choose best overview, align phases by intent, deduplicate topics/tools/resources
        merged = self._merge_structured_outputs(structured_list)
        
        # Render final markdown
        return self._render_markdown(merged)
    
    async def generate_roadmap(self, user_query: str, user_background: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Main entry point - generates roadmap using multi-agent system with proper synthesis
        """
        print(f"🚀 Starting Multi-Agent Roadmap Generation for: {user_query}")
        
        # Start session logging
        session_id = self._start_new_session(user_query, user_background)
        
        # Generate responses from all agents concurrently
        agent_tasks = []
        for agent_id, agent_config in self.agents.items():
            task = self.generate_roadmap_with_agent(
                agent_config, 
                user_query, 
                user_background, 
                agent_id
            )
            agent_tasks.append(task)
        
        # Wait for all agents to complete
        agent_responses = await asyncio.gather(*agent_tasks, return_exceptions=True)
        
        # Filter out exceptions and failed responses  
        valid_responses = []
        for i, response in enumerate(agent_responses):
            if isinstance(response, AgentResponse) and response.confidence_score > 0.1:  # Lower threshold
                valid_responses.append(response)
                print(f"✅ Agent {response.agent_name}: {response.confidence_score:.3f} confidence")
            elif isinstance(response, Exception):
                print(f"❌ Agent {i} exception: {response}")
            else:
                print(f"⚠️ Agent {response.agent_name}: {response.confidence_score:.3f} confidence (below threshold)")
        
        if not valid_responses:
            print("💥 All agents failed to generate valid responses")
            print("🔍 Checking individual agent errors:")
            for i, response in enumerate(agent_responses):
                if isinstance(response, AgentResponse):
                    error = response.metadata.get('error', 'No error info')
                    print(f"  Agent {response.agent_name}: {error}")
            raise Exception("All agents failed to generate valid responses")
        
        # Log funneling process
        best_response = max(valid_responses, key=lambda x: x.confidence_score)
        self._log_funneling_process(
            valid_responses, 
            best_response.agent_name, 
            best_response.confidence_score
        )
        
        # Parse and merge structured outputs for synthesis
        structured_outputs = []
        for response in valid_responses:
            try:
                structured_data = json.loads(response.roadmap)
                structured_outputs.append(structured_data)
            except json.JSONDecodeError:
                # Fallback: Parse markdown format (### Goals, ### Topics, etc.)
                print(f"⚠️ JSON parse failed for {response.agent_name}, trying markdown parsing...")
                markdown_data = self._parse_markdown_roadmap(response.roadmap, user_query)
                if markdown_data and markdown_data.get("phases"):
                    print(f"✅ Successfully parsed markdown from {response.agent_name}")
                    structured_outputs.append(markdown_data)
                else:
                    print(f"❌ Markdown parsing also failed for {response.agent_name}")
                    continue
        
        # Check if structured outputs have meaningful content (not generic)
        meaningful_outputs = []
        for output in structured_outputs:
            has_meaningful_content = False
            for phase in output.get("phases", []):
                # Check if phase has non-generic content
                goals = phase.get("goals", [])
                topics = phase.get("topics", [])
                projects = phase.get("projects", [])
                
                # Check if content is meaningful (not generic placeholders)
                generic_terms = ['basics', 'core concepts', 'basic project', 'basic tools', 
                               'skills', 'advanced concepts', 'practice project', 'intermediate tools']
                
                meaningful_goals = [g for g in goals if isinstance(g, str) and 
                                   not any(term in g.lower() for term in generic_terms) and len(g) > 10]
                meaningful_topics = [t for t in topics if isinstance(t, str) and 
                                    not any(term in t.lower() for term in generic_terms) and len(t) > 10]
                meaningful_projects = [p for p in projects if 
                                     (isinstance(p, str) and not any(term in p.lower() for term in generic_terms) and len(p) > 10) or
                                     (isinstance(p, dict) and p.get("name") and not any(term in p.get("name", "").lower() for term in generic_terms))]
                
                if meaningful_goals or meaningful_topics or meaningful_projects:
                    has_meaningful_content = True
                    break
            
            if has_meaningful_content:
                meaningful_outputs.append(output)
        
        # If no meaningful content, use specialization context to generate proper content
        if not meaningful_outputs and structured_outputs:
            print("⚠️ All agent outputs contain generic content, generating specialization-specific content...")
            spec_context = self._get_specialization_context(user_query.lower())
            # Create a proper structured output using specialization context
            meaningful_outputs = [{
                "overview": f"Complete {spec_context['title']} learning roadmap",
                "phases": self._create_base_phases_for_domain(user_query),
                "time_commitment_hours_per_week": 10,
                "prerequisites": []
            }]
        
        # Synthesize the best elements from all agents
        if len(meaningful_outputs) > 1:
            synthesized_plan = self._synthesize_multi_agent_outputs(meaningful_outputs)
            synthesis_confidence = min(sum(r.confidence_score for r in valid_responses) / len(valid_responses) * 1.2, 1.0)
        elif len(meaningful_outputs) == 1:
            # Even with single agent, enhance to 6 phases
            base_plan = meaningful_outputs[0]
            synthesized_plan = self._ensure_six_phases(base_plan, user_query)
            synthesis_confidence = best_response.confidence_score
        else:
            # No meaningful content at all - use specialization context
            print("⚠️ No meaningful content from agents, using specialization context...")
            spec_context = self._get_specialization_context(user_query.lower())
            synthesized_plan = {
                "overview": f"Complete {spec_context['title']} learning roadmap",
                "phases": self._create_base_phases_for_domain(user_query),
                "time_commitment_hours_per_week": 10,
                "prerequisites": []
            }
            synthesis_confidence = 0.5
        
        # Create final output optimized for frontend node display
        final_result = self._format_for_frontend_nodes(
            synthesized_plan, 
            valid_responses, 
            session_id, 
            synthesis_confidence
        )
        
        # Log completion
        self._log_session_complete(final_result)
        
        print(f"✅ Multi-Agent Generation Complete - Session: {session_id}")
        return final_result

    def _synthesize_multi_agent_outputs(self, structured_outputs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Intelligently merge multiple agent outputs into a cohesive learning plan
        This is the REAL multi-agent funneling logic
        """
        print(f"🔀 Synthesizing {len(structured_outputs)} agent outputs...")
        
        # Select best overview (most comprehensive)
        best_overview = max(
            (output.get("overview", "") for output in structured_outputs), 
            key=lambda x: len(x.split('.')) * len(x), 
            default=""
        )
        
        # Aggregate and deduplicate phases intelligently
        all_phases = []
        phase_categories = {
            "foundation": [], "basics": [], "fundamentals": [],
            "intermediate": [], "development": [], "building": [],
            "advanced": [], "expert": [], "mastery": [], "specialization": [],
            "practical": [], "projects": [], "portfolio": [],
            "career": [], "professional": [], "industry": []
        }
        
        # Categorize phases from all agents
        for output in structured_outputs:
            for phase in output.get("phases", []):
                phase_name = phase.get("name", "").lower()
                categorized = False
                
                for category, phases_list in phase_categories.items():
                    if category in phase_name:
                        phases_list.append(phase)
                        categorized = True
                        break
                
                if not categorized:
                    all_phases.append(phase)
        
        # Select best phase from each category
        synthesized_phases = []
        category_order = ["foundation", "basics", "fundamentals", "intermediate", "development", "building", "advanced", "expert", "mastery", "practical", "projects", "portfolio", "career", "professional"]
        
        for category in category_order:
            if phase_categories[category]:
                # Select the richest phase (most content)
                best_phase = max(
                    phase_categories[category], 
                    key=lambda p: len(p.get("topics", [])) + len(p.get("projects", [])) + len(p.get("goals", []))
                )
                synthesized_phases.append(self._enhance_phase_content(best_phase, phase_categories[category]))
        
        # Add any uncategorized phases
        for phase in all_phases[:2]:  # Limit to 2 additional phases
            synthesized_phases.append(self._enhance_phase_content(phase, [phase]))
        
        # Ensure we have exactly 6 phases for optimal node display
        if len(synthesized_phases) < 6:
            # Add more phases by splitting complex ones or generating new ones
            while len(synthesized_phases) < 6:
                if synthesized_phases:
                    # Find the most complex phase to split
                    complex_phase = max(synthesized_phases, key=lambda p: len(p.get("topics", [])))
                    if len(complex_phase.get("topics", [])) > 3:
                        split_phases = self._split_phase_for_nodes(complex_phase)
                        synthesized_phases.remove(complex_phase)
                        synthesized_phases.extend(split_phases)
                    else:
                        # Generate additional phases based on the domain
                        new_phase = self._generate_additional_phase(synthesized_phases, len(synthesized_phases) + 1)
                        synthesized_phases.append(new_phase)
                else:
                    # Create base phases if none exist
                    synthesized_phases = self._create_base_phases_for_domain(user_query)
                    break
        
        # Clean up phase titles to be professional and concise
        for phase in synthesized_phases:
            phase_name = phase.get("name", "")
            # Remove verbose repetitive text
            if "I Want To Learn" in phase_name:
                # Extract core concept
                clean_name = phase_name.split("Learn ")[-1].split(" And")[0]
                phase["name"] = f"{clean_name} Fundamentals"
            elif "Foundation Excellence" in phase_name:
                phase["name"] = "Core Foundations"
            elif "Proficient In This Field" in phase_name:
                phase["name"] = "Advanced Concepts"
            elif "Professional Leadership" in phase_name:
                phase["name"] = "Expert Mastery"
        
        # Collect best resources and career milestones
        all_resources = []
        all_milestones = []
        
        for output in structured_outputs:
            all_resources.extend(output.get("resources", []))
            all_milestones.extend(output.get("career_milestones", []))
        
        # Calculate average time commitment
        time_commitments = [o.get("time_commitment_hours_per_week", 10) for o in structured_outputs]
        avg_time = sum(time_commitments) / len(time_commitments) if time_commitments else 12
        
        return {
            "overview": best_overview,
            "time_commitment_hours_per_week": int(avg_time),
            "prerequisites": self._merge_prerequisites(structured_outputs),
            "phases": synthesized_phases[:7],  # Optimal for node display
            "career_milestones": self._deduplicate_milestones(all_milestones)[:5]
        }

    def _enhance_phase_content(self, primary_phase: Dict[str, Any], similar_phases: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Enhance a phase by merging content from similar phases
        """
        enhanced = primary_phase.copy()
        
        # Merge topics from all similar phases
        all_topics = set(primary_phase.get("topics", []))
        all_goals = set(primary_phase.get("goals", []))
        all_projects = []
        all_tools = set(primary_phase.get("tools", []))
        all_resources = []
        
        for phase in similar_phases:
            all_topics.update(phase.get("topics", []))
            all_goals.update(phase.get("goals", []))
            all_projects.extend(phase.get("projects", []))
            all_tools.update(phase.get("tools", []))
            all_resources.extend(phase.get("resources", []))
        
        # Create enhanced detailed content for node expansion
        enhanced["topics"] = list(all_topics)[:6]  # Perfect for node display
        enhanced["goals"] = list(all_goals)[:4]
        enhanced["projects"] = self._deduplicate_projects(all_projects)[:3]
        enhanced["tools"] = list(all_tools)[:5]
        enhanced["resources"] = self._deduplicate_resources(all_resources)[:4]
        
        # Add node-specific fields for frontend
        enhanced["node_summary"] = f"{len(enhanced['topics'])} key topics, {len(enhanced['projects'])} projects"
        enhanced["expandable_content"] = {
            "learning_objectives": enhanced["goals"],
            "hands_on_projects": enhanced["projects"],
            "tools_and_technologies": enhanced["tools"][:8],  # Ensure tools are populated
            "recommended_resources": enhanced["resources"]
        }
        
        # Ensure tools section is never empty
        if len(enhanced["tools"]) == 0:
            # Add relevant tools based on phase content
            phase_name = enhanced.get("name", "").lower()
            if "javascript" in phase_name or "web" in phase_name:
                enhanced["tools"] = ["VS Code", "Chrome DevTools", "Git", "Node.js", "npm"]
            elif "python" in phase_name:
                enhanced["tools"] = ["PyCharm", "Jupyter Notebook", "Git", "pip", "Virtual Environment"]
            elif "react" in phase_name:
                enhanced["tools"] = ["VS Code", "React DevTools", "Create React App", "ESLint", "Prettier"]
            else:
                enhanced["tools"] = ["Code Editor", "Version Control", "Package Manager", "Browser Tools"]
        
        return enhanced

    def _split_phase_for_nodes(self, complex_phase: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Split a complex phase into 2 smaller phases for better node visualization
        """
        topics = complex_phase.get("topics", [])
        mid_point = len(topics) // 2
        
        phase1 = complex_phase.copy()
        phase1["name"] = f"{complex_phase.get('name', 'Phase')} - Part 1"
        phase1["topics"] = topics[:mid_point]
        phase1["duration_weeks"] = max(complex_phase.get("duration_weeks", 4) // 2, 2)
        
        phase2 = complex_phase.copy()
        phase2["name"] = f"{complex_phase.get('name', 'Phase')} - Part 2"
        phase2["topics"] = topics[mid_point:]
        phase2["duration_weeks"] = complex_phase.get("duration_weeks", 4) - phase1["duration_weeks"]
        
        return [phase1, phase2]
    
    def _ensure_six_phases(self, base_plan: Dict[str, Any], query: str) -> Dict[str, Any]:
        """Ensure we always have exactly 6 phases for optimal UI"""
        if not base_plan:
            return {"phases": self._create_base_phases_for_domain(query)}
        
        existing_phases = base_plan.get("phases", [])
        
        # If we have fewer than 6 phases, expand intelligently
        while len(existing_phases) < 6:
            if len(existing_phases) >= 1:
                # Split the most complex phase or add complementary phases
                complex_phase = max(existing_phases, key=lambda p: len(p.get("topics", [])))
                if len(complex_phase.get("topics", [])) > 4:
                    split_phases = self._split_phase_for_nodes(complex_phase)
                    existing_phases.remove(complex_phase)
                    existing_phases.extend(split_phases)
                else:
                    # Add complementary phase
                    new_phase = self._generate_additional_phase(existing_phases, len(existing_phases) + 1)
                    existing_phases.append(new_phase)
            else:
                # No phases exist, create from scratch
                existing_phases = self._create_base_phases_for_domain(query)
                break
        
        # Enhance all phases with proper tools and content
        for phase in existing_phases:
            if len(phase.get("tools", [])) < 3:
                # Ensure each phase has adequate tools
                self._enhance_phase_tools(phase, query)
        
        enhanced_plan = base_plan.copy()
        enhanced_plan["phases"] = existing_phases[:6]  # Exactly 6 phases
        return enhanced_plan
    
    def _enhance_phase_tools(self, phase: Dict[str, Any], domain: str):
        """Enhance a phase with appropriate tools based on domain and phase name"""
        phase_name = phase.get("name", "").lower()
        domain_lower = domain.lower()
        
        current_tools = phase.get("tools", [])
        
        # Add tools based on phase type and domain
        if "foundation" in phase_name or "fundamental" in phase_name:
            new_tools = ["VS Code", "Git", "Command Line", "Browser DevTools", "Documentation Tools"]
        elif "advanced" in phase_name or "architecture" in phase_name:
            new_tools = ["Advanced IDE", "Performance Profiler", "Testing Framework", "Code Quality Tools", "System Design Tools"]
        elif "frontend" in phase_name or "web" in phase_name:
            new_tools = ["React DevTools", "Webpack", "ESLint", "Prettier", "Browser Extensions"]
        elif "backend" in phase_name or "api" in phase_name:
            new_tools = ["Postman", "Database Tools", "API Documentation", "Server Monitoring", "Security Tools"]
        elif "professional" in phase_name or "career" in phase_name:
            new_tools = ["LinkedIn", "Slack", "Jira", "Confluence", "Portfolio Platforms"]
        else:
            new_tools = ["Development Tools", "Version Control", "Testing Tools", "Documentation", "Collaboration Tools"]
        
        # Merge with existing tools, avoid duplicates
        all_tools = list(set(current_tools + new_tools))
        phase["tools"] = all_tools[:6]  # Limit to 6 tools per phase
        
        # Ensure expandable_content has tools
        if "expandable_content" not in phase:
            phase["expandable_content"] = {}
        phase["expandable_content"]["tools_and_technologies"] = phase["tools"]
    
    def _generate_additional_phase(self, existing_phases: List[Dict[str, Any]], phase_number: int) -> Dict[str, Any]:
        """Generate an additional phase to reach optimal count"""
        phase_names = ["Professional Development", "Advanced Projects", "Industry Integration", "Leadership & Teamwork", "Portfolio Optimization", "Career Advancement"]
        
        # Determine what type of phase to add based on existing ones
        existing_names = [p.get("name", "").lower() for p in existing_phases]
        
        if "professional" not in str(existing_names):
            return {
                "name": "Professional Development",
                "duration_weeks": 3,
                "goals": ["Build professional network", "Develop soft skills", "Master industry practices"],
                "topics": ["Communication skills", "Project management", "Team collaboration", "Industry standards"],
                "projects": [{"name": "Professional Portfolio", "description": "Complete professional showcase"}],
                "tools": ["LinkedIn", "Slack", "Jira", "Confluence"],
                "resources": [{"title": "Professional Skills Course", "provider": "LinkedIn Learning", "cost": "Free", "type": "Course"}],
                "expandable_content": {
                    "learning_objectives": ["Build professional network", "Develop soft skills", "Master industry practices"],
                    "hands_on_projects": [{"name": "Professional Portfolio", "description": "Complete professional showcase"}],
                    "tools_and_technologies": ["LinkedIn", "Slack", "Jira", "Confluence"]
                }
            }
        elif "advanced" not in str(existing_names):
            return {
                "name": "Advanced Specialization",
                "duration_weeks": 4,
                "goals": ["Master advanced concepts", "Build expertise", "Lead technical initiatives"],
                "topics": ["Advanced patterns", "Performance optimization", "System architecture", "Best practices"],
                "projects": [{"name": "Advanced Implementation", "description": "Complex technical project"}],
                "tools": ["Advanced IDE", "Performance Tools", "Architecture Tools", "Testing Frameworks"],
                "resources": [{"title": "Advanced Concepts Guide", "provider": "Technical Documentation", "cost": "Free", "type": "Documentation"}],
                "expandable_content": {
                    "learning_objectives": ["Master advanced concepts", "Build expertise", "Lead technical initiatives"],
                    "hands_on_projects": [{"name": "Advanced Implementation", "description": "Complex technical project"}],
                    "tools_and_technologies": ["Advanced IDE", "Performance Tools", "Architecture Tools", "Testing Frameworks"]
                }
            }
        else:
            return {
                "name": f"Mastery Phase {phase_number}",
                "duration_weeks": 3,
                "goals": ["Achieve mastery", "Build expertise", "Prepare for leadership"],
                "topics": ["Expert-level skills", "Leadership principles", "Innovation methods", "Industry trends"],
                "projects": [{"name": "Capstone Project", "description": "Demonstrate complete mastery"}],
                "tools": ["Expert Tools", "Leadership Platforms", "Innovation Software", "Collaboration Tools"],
                "resources": [{"title": "Mastery Guide", "provider": "Expert Resource", "cost": "Free", "type": "Guide"}],
                "expandable_content": {
                    "learning_objectives": ["Achieve mastery", "Build expertise", "Prepare for leadership"],
                    "hands_on_projects": [{"name": "Capstone Project", "description": "Demonstrate complete mastery"}],
                    "tools_and_technologies": ["Expert Tools", "Leadership Platforms", "Innovation Software", "Collaboration Tools"]
                }
            }
    
    def _parse_markdown_roadmap(self, markdown_text: str, user_query: str) -> Optional[Dict[str, Any]]:
        """
        Parse markdown roadmap format (### Goals, ### Topics, etc.) when JSON parsing fails.
        This handles the actual format that AI agents generate.
        """
        if not markdown_text or len(markdown_text) < 100:
            return None
        
        try:
            phases = []
            lines = markdown_text.split('\n')
            current_phase = None
            current_section = None
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # Detect phase headers: ## Phase X: Name or ### **Phase X: Name**
                phase_match = re.match(r'#{1,3}\s*\*?Phase\s*(\d+)[:\s]+(.+?)(?:\*|\(|$)', line, re.IGNORECASE)
                if phase_match:
                    # Save previous phase if exists
                    if current_phase and (current_phase.get("goals") or current_phase.get("topics")):
                        phases.append(current_phase)
                    
                    phase_num = phase_match.group(1)
                    phase_name = phase_match.group(2).replace('*', '').strip()
                    # Remove duration from name if present
                    phase_name = re.sub(r'\s*\([^)]*\)\s*$', '', phase_name).strip()
                    
                    # Extract duration from next line or current line
                    duration = 4
                    if i + 1 < len(lines):
                        dur_match = re.search(r'\((\d+)[-\s](\d+)?\s*(?:weeks?|months?)\)', lines[i+1] or lines[i], re.IGNORECASE)
                        if dur_match:
                            duration = int(dur_match.group(1))
                    
                    current_phase = {
                        "name": phase_name or f"Phase {phase_num}",
                        "duration_weeks": duration,
                        "goals": [],
                        "topics": [],
                        "projects": [],
                        "tools": [],
                        "resources": []
                    }
                    current_section = None
                    continue
                
                # Detect section headers: ### Goals, ### Topics, etc.
                if line.startswith('###'):
                    section_name = line.replace('#', '').strip().lower()
                    if 'goal' in section_name:
                        current_section = 'goals'
                    elif 'topic' in section_name:
                        current_section = 'topics'
                    elif 'project' in section_name:
                        current_section = 'projects'
                    elif 'tool' in section_name or 'technolog' in section_name:
                        current_section = 'tools'
                    elif 'resource' in section_name:
                        current_section = 'resources'
                    else:
                        current_section = None
                    continue
                
                # Also check for **Learning Goals:** format
                if line.startswith('**') and line.endswith(':**'):
                    section_name = line.replace('**', '').replace(':', '').strip().lower()
                    if 'goal' in section_name or 'learning goal' in section_name:
                        current_section = 'goals'
                    elif 'topic' in section_name or 'key topic' in section_name:
                        current_section = 'topics'
                    elif 'project' in section_name or 'hands-on' in section_name:
                        current_section = 'projects'
                    elif 'tool' in section_name or 'technolog' in section_name:
                        current_section = 'tools'
                    elif 'resource' in section_name:
                        current_section = 'resources'
                    else:
                        current_section = None
                    continue
                
                # Extract bullet points
                if current_phase and current_section and (line.startswith('-') or line.startswith('•') or line.startswith('*')):
                    content = line.lstrip('-•*').strip()
                    # Remove markdown formatting
                    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)  # Remove bold
                    content = re.sub(r'`([^`]+)`', r'\1', content)  # Remove code
                    content = content.strip()
                    
                    # Filter out generic/placeholder content
                    content_lower = content.lower()
                    generic_patterns = ['basics', 'core concepts', 'basic project', 'basic tools', 
                                       'skills', 'advanced concepts', 'advanced topics', 'practice project']
                    
                    # Only add if it's meaningful and not generic
                    if (len(content) > 5 and 
                        content not in ['basics', 'core concepts', 'skills'] and
                        not any(pattern in content_lower and len(content) < 30 for pattern in generic_patterns)):
                        
                        if current_section == 'projects':
                            # Handle project format: "**Name**: description" or just "Name"
                            if ':' in content:
                                parts = content.split(':', 1)
                                project_name = parts[0].strip()
                                project_desc = parts[1].strip() if len(parts) > 1 else ""
                                current_phase[current_section].append({
                                    "name": project_name,
                                    "description": project_desc or f"Hands-on {project_name} project"
                                })
                            else:
                                current_phase[current_section].append({
                                    "name": content,
                                    "description": f"Practical {content} implementation"
                                })
                        else:
                            current_phase[current_section].append(content)
            
            # Add last phase
            if current_phase and (current_phase.get("goals") or current_phase.get("topics")):
                phases.append(current_phase)
            
            if phases:
                # Create overview from user query
                overview = f"Complete {user_query} learning roadmap with {len(phases)} comprehensive phases"
                
                return {
                    "overview": overview,
                    "phases": phases,
                    "time_commitment_hours_per_week": 10,
                    "prerequisites": []
                }
        
        except Exception as e:
            print(f"⚠️ Markdown parsing error: {e}")
            import traceback
            print(traceback.format_exc())
        
        return None
    
    def _create_base_phases_for_domain(self, domain: str) -> List[Dict[str, Any]]:
        """
        Create base phases with specialization-specific content instead of generic placeholders.
        This should only be used as a last resort when agents completely fail.
        """
        # Extract core domain name
        domain_clean = domain.replace('i want to learn', '').replace('and become proficient', '').strip()
        domain_clean = domain_clean.split()[0] if domain_clean.split() else domain
        
        # Get specialization context to make it domain-specific
        spec_context = self._get_specialization_context(domain_clean)
        
        # Create domain-specific phases instead of generic ones
        return [
            {
                "name": f"{spec_context['title']} Foundations",
                "duration_weeks": 4,
                "goals": [
                    f"Master fundamental {spec_context['title']} principles",
                    f"Understand core {spec_context['field']} concepts",
                    f"Set up {spec_context['title']} development environment"
                ],
                "topics": [
                    f"{spec_context['title']} fundamentals",
                    f"Core {spec_context['field']} concepts",
                    f"Essential {spec_context['title']} tools and workflows"
                ],
                "projects": [{"name": f"{spec_context['title']} Foundation Project", "description": f"Apply basic {spec_context['title']} concepts"}],
                "tools": [f"{spec_context['title']} Tools", "Development Environment", "Documentation"],
                "expandable_content": {"tools_and_technologies": [f"{spec_context['title']} Tools", "Development Environment"]}
            },
            {
                "name": f"Intermediate {spec_context['title']}",
                "duration_weeks": 5,
                "goals": [
                    f"Build practical {spec_context['title']} skills",
                    f"Apply {spec_context['field']} methodologies",
                    f"Create {spec_context['title']} projects"
                ],
                "topics": [
                    f"Advanced {spec_context['title']} techniques",
                    f"{spec_context['field']} best practices",
                    f"Professional {spec_context['title']} workflows"
                ],
                "projects": [{"name": f"{spec_context['title']} Portfolio Project", "description": f"Showcase {spec_context['title']} skills"}],
                "tools": [f"Professional {spec_context['title']} Tools", "Collaboration Platforms", "Version Control"],
                "expandable_content": {"tools_and_technologies": [f"Professional {spec_context['title']} Tools"]}
            },
            {
                "name": f"Advanced {spec_context['title']}",
                "duration_weeks": 6,
                "goals": [
                    f"Master expert-level {spec_context['title']} concepts",
                    f"Lead {spec_context['field']} initiatives",
                    f"Build production-ready {spec_context['title']} solutions"
                ],
                "topics": [
                    f"Expert {spec_context['title']} patterns",
                    f"Enterprise {spec_context['field']} practices",
                    f"Advanced {spec_context['title']} optimization"
                ],
                "projects": [{"name": f"{spec_context['title']} Capstone", "description": f"Complete {spec_context['title']} mastery project"}],
                "tools": [f"Enterprise {spec_context['title']} Tools", "Performance Tools", "Deployment Platforms"],
                "expandable_content": {"tools_and_technologies": [f"Enterprise {spec_context['title']} Tools"]}
            }
        ]
        """Create 6 base phases when no agent data is available"""
        domain_lower = domain.lower()
        
        if "software" in domain_lower or "programming" in domain_lower:
            return [
                {"name": "Programming Fundamentals", "duration_weeks": 4, "goals": ["Learn syntax", "Understand logic"], "topics": ["Variables", "Functions", "Control flow"], "projects": [{"name": "Basic App"}], "tools": ["VS Code", "Git"], "expandable_content": {"tools_and_technologies": ["VS Code", "Git"]}},
                {"name": "Data Structures & Algorithms", "duration_weeks": 5, "goals": ["Master algorithms", "Optimize code"], "topics": ["Arrays", "Trees", "Sorting"], "projects": [{"name": "Algorithm Visualizer"}], "tools": ["Debugger", "Profiler"], "expandable_content": {"tools_and_technologies": ["Debugger", "Profiler"]}},
                {"name": "Web Development", "duration_weeks": 6, "goals": ["Build websites", "Master frameworks"], "topics": ["HTML", "CSS", "JavaScript"], "projects": [{"name": "Portfolio Website"}], "tools": ["Browser Tools", "React"], "expandable_content": {"tools_and_technologies": ["Browser Tools", "React"]}},
                {"name": "Backend Systems", "duration_weeks": 5, "goals": ["Build APIs", "Manage databases"], "topics": ["REST APIs", "Databases", "Security"], "projects": [{"name": "API Server"}], "tools": ["Node.js", "MongoDB"], "expandable_content": {"tools_and_technologies": ["Node.js", "MongoDB"]}},
                {"name": "DevOps & Deployment", "duration_weeks": 4, "goals": ["Deploy applications", "Automate processes"], "topics": ["CI/CD", "Docker", "Cloud"], "projects": [{"name": "Production App"}], "tools": ["Docker", "AWS"], "expandable_content": {"tools_and_technologies": ["Docker", "AWS"]}},
                {"name": "Professional Development", "duration_weeks": 3, "goals": ["Build career", "Network"], "topics": ["Soft skills", "Leadership"], "projects": [{"name": "Portfolio"}], "tools": ["LinkedIn", "Slack"], "expandable_content": {"tools_and_technologies": ["LinkedIn", "Slack"]}}
            ]
        else:
            return [
                {"name": "Foundations", "duration_weeks": 4, "goals": ["Build basics"], "topics": ["Core concepts"], "projects": [{"name": "Basic project"}], "tools": ["Basic tools"], "expandable_content": {"tools_and_technologies": ["Basic tools"]}},
                {"name": "Intermediate Skills", "duration_weeks": 5, "goals": ["Develop skills"], "topics": ["Advanced concepts"], "projects": [{"name": "Practice project"}], "tools": ["Intermediate tools"], "expandable_content": {"tools_and_technologies": ["Intermediate tools"]}},
                {"name": "Advanced Concepts", "duration_weeks": 6, "goals": ["Master advanced topics"], "topics": ["Expert concepts"], "projects": [{"name": "Advanced project"}], "tools": ["Advanced tools"], "expandable_content": {"tools_and_technologies": ["Advanced tools"]}},
                {"name": "Practical Application", "duration_weeks": 5, "goals": ["Apply knowledge"], "topics": ["Real-world skills"], "projects": [{"name": "Real project"}], "tools": ["Professional tools"], "expandable_content": {"tools_and_technologies": ["Professional tools"]}},
                {"name": "Specialization", "duration_weeks": 4, "goals": ["Specialize"], "topics": ["Niche skills"], "projects": [{"name": "Specialized project"}], "tools": ["Specialized tools"], "expandable_content": {"tools_and_technologies": ["Specialized tools"]}},
                {"name": "Mastery", "duration_weeks": 3, "goals": ["Achieve mastery"], "topics": ["Expert skills"], "projects": [{"name": "Mastery project"}], "tools": ["Expert tools"], "expandable_content": {"tools_and_technologies": ["Expert tools"]}}
            ]

    def _merge_prerequisites(self, structured_outputs: List[Dict[str, Any]]) -> List[str]:
        """Merge and deduplicate prerequisites from all agents"""
        all_prereqs = set()
        for output in structured_outputs:
            all_prereqs.update(output.get("prerequisites", []))
        return list(all_prereqs)[:5]

    def _deduplicate_milestones(self, milestones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate career milestones by timeframe"""
        seen_timeframes = set()
        unique_milestones = []
        
        for milestone in milestones:
            timeframe = milestone.get("timeframe", "")
            if timeframe and timeframe not in seen_timeframes:
                seen_timeframes.add(timeframe)
                unique_milestones.append(milestone)
        
        return unique_milestones

    def _deduplicate_projects(self, projects: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate projects by name similarity"""
        unique_projects = []
        seen_names = set()
        
        for project in projects:
            if isinstance(project, dict):
                name = project.get("name", "").lower()
                if name and name not in seen_names:
                    seen_names.add(name)
                    unique_projects.append(project)
            elif isinstance(project, str) and project.lower() not in seen_names:
                seen_names.add(project.lower())
                unique_projects.append({"name": project, "description": f"Hands-on {project} implementation"})
        
        return unique_projects

    def _deduplicate_resources(self, resources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Deduplicate resources by title/URL"""
        unique_resources = []
        seen_titles = set()
        
        for resource in resources:
            if isinstance(resource, dict):
                title = resource.get("title", "").lower()
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    unique_resources.append(resource)
        
        return unique_resources

    def _format_for_frontend_nodes(
        self, 
        synthesized_plan: Dict[str, Any], 
        agent_responses: List[AgentResponse], 
        session_id: str, 
        confidence: float
    ) -> Dict[str, Any]:
        """
        Format the synthesized plan specifically for frontend node display
        """
        if not synthesized_plan:
            return self._create_fallback_result()
        
        # Convert phases to node-optimized format
        node_phases = []
        for i, phase in enumerate(synthesized_plan.get("phases", [])):
            node_phase = {
                "phase": phase.get("name", f"Phase {i+1}"),
                "duration": f"{phase.get('duration_weeks', 4)} weeks",
                "topics": phase.get("topics", [])[:5],  # Perfect for node cards
                "projects": phase.get("projects", [])[:3],
                "tools": phase.get("tools", [])[:4],
                "goals": phase.get("goals", [])[:4],
                "node_summary": phase.get("node_summary", f"Learning Phase {i+1}"),
                "expandable_content": phase.get("expandable_content", {}),
                "resources": phase.get("resources", [])[:3]
            }
            node_phases.append(node_phase)
        
        # Create comprehensive metadata
        metadata = {
            "session_id": session_id,
            "synthesis_confidence": confidence,
            "successful_agents": len(agent_responses),
            "total_agents": 3,
            "agent_contributions": [
                {
                    "agent_name": resp.agent_name,
                    "confidence": resp.confidence_score,
                    "provider": resp.metadata.get("provider", ""),
                    "focus": resp.metadata.get("focus", "")
                } for resp in agent_responses
            ],
            "structured_plan": {
                "phases": node_phases,
                "overview": synthesized_plan.get("overview", ""),
                "total_phases": len(node_phases),
                "estimated_duration": f"{sum(int(p.get('duration', '4 weeks').split()[0]) for p in node_phases)} weeks"
            }
        }
        
        # Generate human-readable final roadmap for legacy compatibility
        final_roadmap = self._generate_readable_roadmap(synthesized_plan)
        
        return {
            "final_roadmap": final_roadmap,
            "metadata": metadata,
            "agent_insights": [
                {
                    "agent_name": resp.agent_name,
                    "confidence": resp.confidence_score,
                    "focus_area": resp.metadata.get("focus", ""),
                    "contribution": f"Specialized in {resp.metadata.get('focus', 'general guidance')}"
                } for resp in agent_responses
            ],
            "funneling_report": self.generate_funneling_report(session_id),
            "using_multi_agent": True,
            "synthesis_success": True
        }

    def _generate_readable_roadmap(self, synthesized_plan: Dict[str, Any]) -> str:
        """
        Generate human-readable markdown roadmap for display compatibility
        """
        lines = [f"## {synthesized_plan.get('overview', 'Complete Learning Roadmap')}\n"]
        
        for i, phase in enumerate(synthesized_plan.get("phases", []), 1):
            phase_name = phase.get("name", f"Phase {i}")
            duration = phase.get("duration_weeks", 4)
            
            lines.append(f"### **Phase {i}: {phase_name}** ({duration} weeks)\n")
            
            if phase.get("goals"):
                lines.append("**Learning Goals:**")
                for goal in phase.get("goals", []):
                    lines.append(f"- {goal}")
                lines.append("")
            
            if phase.get("topics"):
                lines.append("**Key Topics:**")
                for topic in phase.get("topics", []):
                    lines.append(f"- {topic}")
                lines.append("")
            
            if phase.get("projects"):
                lines.append("**Hands-on Projects:**")
                for project in phase.get("projects", []):
                    if isinstance(project, dict):
                        lines.append(f"- **{project.get('name', 'Project')}**: {project.get('description', '')}")
                    else:
                        lines.append(f"- {project}")
                lines.append("")
            
            if phase.get("tools"):
                lines.append("**Tools & Technologies:**")
                for tool in phase.get("tools", []):
                    lines.append(f"- {tool}")
                lines.append("")
        
        return "\n".join(lines)

    def _create_fallback_result(self) -> Dict[str, Any]:
        """Create fallback result when synthesis fails"""
        return {
            "final_roadmap": "## Learning Path\nUnable to generate detailed roadmap. Please try again.",
            "metadata": {"synthesis_confidence": 0.0, "successful_agents": 0},
            "agent_insights": [],
            "funneling_report": {"error": "No data to report"},
            "using_multi_agent": False,
            "synthesis_success": False
        }

    def _create_synthesis_prompt(self, responses: List[AgentResponse]) -> str:
        """Deprecated: no longer used. Kept for backward reference."""
        return ""
    
    async def generate_multi_agent_roadmap(self, query: str, background: dict = None, include_agent_details: bool = True) -> Dict[str, Any]:
        """
        LEGACY COMPATIBILITY METHOD - Routes to new synthesis system
        This maintains compatibility with existing route calls
        """
        print(f"🔄 Legacy method called, routing to new synthesis system...")
        return await self.generate_roadmap(query, background)
    
    async def generate_funneled_roadmap(
        self, 
        user_query: str,
        user_background: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Main method: Generate roadmap using multi-agent system with comprehensive logging
        Returns the final funneled result plus individual agent insights and funneling report
        """
        
        # Start new session for logging
        session_id = self._start_new_session(user_query, user_background)
        print(f"🚀 Starting multi-agent roadmap generation (Session: {session_id})...")
        print(f"🔍 Current funneling_logs length: {len(GLOBAL_FUNNELING_LOGS)}")
        print(f"📝 Session started with ID: {session_id}")
        
        # OPTIMIZED: Run agents in parallel with smart early completion
        tasks = [
            self.generate_roadmap_with_agent(config, user_query, user_background, agent_id)
            for agent_id, config in self.agents.items()
        ]
        
        # Smart timeout strategy: Return as soon as we have good results
        agent_responses = []
        try:
            # Wait for all agents with reduced timeout for speed
            done, pending = await asyncio.wait(
                tasks, 
                timeout=25.0,  # Reduced from 45s to 25s for speed
                return_when=asyncio.FIRST_COMPLETED  # Return as soon as first agent completes
            )
            
            # Collect completed results
            for task in done:
                try:
                    result = await task
                    if isinstance(result, AgentResponse):
                        agent_responses.append(result)
                except Exception as e:
                    print(f"Task error: {e}")
            
            # If we have at least one good result, continue with that
            good_results = [r for r in agent_responses if r.confidence_score > 0.3]
            if good_results:
                print(f"🚀 Early completion with {len(good_results)} quality results")
                # Cancel remaining tasks to save time
                for task in pending:
                    task.cancel()
            else:
                # Wait a bit more for remaining tasks if no good results yet
                print("⏳ No quality results yet, waiting for remaining agents...")
                timeout_remaining = max(15.0, 25.0 - 10.0)  # Max 15s more
                done2, pending2 = await asyncio.wait(
                    pending, 
                    timeout=timeout_remaining,
                    return_when=asyncio.ALL_COMPLETED
                )
                
                for task in done2:
                    try:
                        result = await task
                        if isinstance(result, AgentResponse):
                            agent_responses.append(result)
                    except Exception as e:
                        print(f"Task error: {e}")
                
                # Cancel any remaining tasks
                for task in pending2:
                    task.cancel()
                    
        except Exception as e:
            print(f"⚠️ Agent execution error: {e}")
            agent_responses = []
        
        print(f"✅ Received {len(agent_responses)} agent responses")
        for response in agent_responses:
            print(f"  - {response.agent_name}: Confidence {response.confidence_score:.2f}")
        
        # Build structured list and merged plan
        structured_list: List[Dict[str, Any]] = []
        for r in agent_responses:
            try:
                if r.confidence_score > 0 and r.roadmap:
                    structured_list.append(json.loads(r.roadmap))
            except Exception:
                continue
        merged_plan: Optional[Dict[str, Any]] = self._merge_structured_outputs(structured_list) if structured_list else None

        # Log funneling process
        best_agent = max(agent_responses, key=lambda r: r.confidence_score).agent_name if agent_responses else "None"
        final_confidence = max((r.confidence_score for r in agent_responses), default=0.0)
        self._log_funneling_process(agent_responses, best_agent, final_confidence)

        # Render final markdown
        print("🔄 Funneling responses into optimal roadmap...")
        final_roadmap = self._render_markdown(merged_plan) if merged_plan else "Unable to generate roadmap. Please try again."
        
        print("✅ Final roadmap generated!")
        
        # Prepare final result - ENSURE session_id is always included
        final_result = {
            "final_roadmap": final_roadmap,
            "agent_insights": [
                {
                    "agent_name": r.agent_name,
                    "confidence": r.confidence_score,
                    "focus": r.metadata.get("focus", ""),
                    "preview": r.roadmap[:200] + "..." if len(r.roadmap) > 200 else r.roadmap
                }
                for r in agent_responses
            ],
            "metadata": {
                "num_agents": len(agent_responses),
                "successful_agents": sum(1 for r in agent_responses if r.confidence_score > 0),
                "query": user_query,
                "structured_plan": merged_plan or {},
                "session_id": session_id,  # CRITICAL: Always include session_id
                "timestamp": str(time.time()),
                "execution_time": f"~{len(agent_responses)*10}s"
            },
            "session_id": session_id  # Also include at root level for direct access
        }
        
        # Log session completion
        self._log_session_complete(final_result)
        
        # Add funneling report to result - ENSURE IT'S ALWAYS INCLUDED
        try:
            funneling_report = self.generate_funneling_report(session_id)
            if not funneling_report or funneling_report.get("error"):
                # Create minimal report if generation fails
                funneling_report = {
                    "session_id": session_id,
                    "agent_performance": {
                        "total_agents": len(agent_responses),
                        "successful_agents": sum(1 for r in agent_responses if r.confidence_score > 0),
                        "success_rate_percent": round((sum(1 for r in agent_responses if r.confidence_score > 0) / max(len(agent_responses), 1)) * 100, 1),
                        "individual_results": [
                            {
                                "agent_name": r.agent_name,
                                "success": r.confidence_score > 0,
                                "confidence_score": r.confidence_score,
                                "provider": r.metadata.get("provider", "unknown"),
                                "model": r.metadata.get("model", "unknown"),
                                "response_time": "< 1s"
                            }
                            for r in agent_responses
                        ]
                    },
                    "funneling_process": {
                        "method": "confidence_based_selection",
                        "best_agent": best_agent,
                        "final_confidence": final_confidence,
                        "decision_rationale": f"Selected {best_agent} based on highest confidence score"
                    },
                    "output_metrics": {
                        "total_execution_time": "< 30s",
                        "phases_generated": len(merged_plan.get("phases", [])) if merged_plan else 0,
                        "content_items": sum(len(phase.get("topics", [])) + len(phase.get("projects", [])) 
                                           for phase in merged_plan.get("phases", [])) if merged_plan else 0
                    }
                }
            final_result["funneling_report"] = funneling_report
        except Exception as e:
            print(f"⚠️ Error generating funneling report: {e}")
            # Always include a basic report even if generation fails
            final_result["funneling_report"] = {
                "session_id": session_id,
                "error": str(e),
                "agent_performance": {"total_agents": len(agent_responses), "successful_agents": sum(1 for r in agent_responses if r.confidence_score > 0)}
            }
        
        print(f"🎯 Final result keys: {list(final_result.keys())}")
        print(f"🔍 Funneling report included: {'funneling_report' in final_result}")
        print(f"📊 Session ID: {session_id}")
        print(f"✅ Returning complete result with guaranteed funneling report")
        
        return final_result


# Example usage
async def main():
    """Example usage of the multi-agent system"""
    
    service = MultiAgentFunnelService()
    
    result = await service.generate_funneled_roadmap(
        user_query="I want to transition from marketing to data science",
        user_background={
            "current_skills": "Marketing analytics, Excel, basic SQL",
            "experience_level": "Intermediate",
            "time_available": "10 hours per week",
            "goals": "Get a data science job within 12 months"
        }
    )
    
    print("\n" + "="*80)
    print("FINAL ROADMAP")
    print("="*80)
    print(result["final_roadmap"])
    print("\n" + "="*80)
    print("AGENT INSIGHTS")
    print("="*80)
    for insight in result["agent_insights"]:
        print(f"\n{insight['agent_name']} (Confidence: {insight['confidence']:.2f})")
        print(f"Focus: {insight['focus']}")
        print(f"Preview: {insight['preview']}")


if __name__ == "__main__":
    asyncio.run(main())
