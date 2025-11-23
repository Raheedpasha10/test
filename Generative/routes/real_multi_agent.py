"""
REAL Multi-Agent System Route - Fixed Integration
This replaces the broken multi-agent implementation with proper synthesis
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging

from services.multi_agent_service import MultiAgentFunnelService

router = APIRouter(tags=["Real Multi-Agent System"])

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserBackground(BaseModel):
    current_skills: Optional[str] = Field(None, description="User's current skills")
    experience_level: Optional[str] = Field("Beginner", description="Experience level")
    time_available: Optional[str] = Field("10-15 hours per week", description="Time available per week")
    goals: Optional[str] = Field(None, description="Career goals")
    education: Optional[str] = Field(None, description="Educational background")

class MultiAgentRequest(BaseModel):
    query: str = Field(..., description="User's career query or goal", min_length=10)
    background: Optional[UserBackground] = Field(None, description="User background information")
    include_agent_details: bool = Field(True, description="Include individual agent insights")

class MultiAgentRoadmapResponse(BaseModel):
    status: str
    final_roadmap: str
    metadata: Dict[str, Any]
    agent_insights: List[Dict[str, Any]]
    funneling_report: Dict[str, Any]
    revolutionary_features: Optional[Dict[str, Any]] = {}
    discovery_constellation: Optional[Dict[str, Any]] = {}
    intelligence_nexus: Optional[Dict[str, Any]] = {}
    mastery_acceleration: Optional[Dict[str, Any]] = {}

@router.post("/generate-roadmap", response_model=MultiAgentRoadmapResponse)
async def generate_real_multi_agent_roadmap(request: MultiAgentRequest):
    """
    REAL Multi-Agent Roadmap Generation with Proper Synthesis
    
    This endpoint uses the actual multi-agent synthesis system with:
    - 3 specialized AI agents (Strategic, Practical, Technical)
    - Real AI API calls (Groq + Gemini)
    - Intelligent synthesis and funneling
    - Node-optimized output for frontend
    """
    logger.info(f"🚀 Starting REAL Multi-Agent Generation for: {request.query}")
    
    try:
        # Initialize the real multi-agent service
        multi_agent_service = MultiAgentFunnelService()
        
        # Convert background to proper format
        background_dict = None
        if request.background:
            background_dict = {
                "current_skills": request.background.current_skills or "",
                "experience_level": request.background.experience_level or "Beginner",
                "time_available": request.background.time_available or "10-15 hours per week",
                "goals": request.background.goals or f"Master {request.query}",
                "education": request.background.education or ""
            }
        
        logger.info(f"🤖 Calling real multi-agent synthesis...")
        
        # Use the NEW synthesis method we just implemented
        result = await multi_agent_service.generate_roadmap(
            user_query=request.query,
            user_background=background_dict
        )
        
        logger.info(f"✅ Multi-Agent synthesis complete - Session: {result.get('metadata', {}).get('session_id', 'unknown')}")
        
        return MultiAgentRoadmapResponse(
            status="success",
            final_roadmap=result.get("final_roadmap", ""),
            metadata=result.get("metadata", {}),
            agent_insights=result.get("agent_insights", []),
            funneling_report=result.get("funneling_report", {}),
            revolutionary_features={},
            discovery_constellation={},
            intelligence_nexus={},
            mastery_acceleration={}
        )
        
    except Exception as e:
        logger.error(f"❌ Real multi-agent generation failed: {str(e)}")
        
        # Provide detailed error information
        error_detail = str(e)
        if "All agents failed" in error_detail:
            error_detail = "All AI agents failed to generate responses. Please check API keys and try again."
        elif "rate_limit" in error_detail.lower():
            error_detail = "API rate limit exceeded. Please wait a moment and try again."
        elif "API key" in error_detail:
            error_detail = "AI service configuration error. Please check API keys."
        
        raise HTTPException(
            status_code=500,
            detail=f"Multi-agent synthesis failed: {error_detail}"
        )

@router.get("/health")
async def health_check():
    """Check if the real multi-agent service is properly configured"""
    import os
    
    config_status = {
        "groq_configured": bool(os.getenv("GROQ_API_KEY")),
        "gemini_configured": bool(os.getenv("GOOGLE_GENAI_API_KEY")),
        "service_type": "Real Multi-Agent with Synthesis"
    }
    
    minimum_configured = config_status["groq_configured"] and config_status["gemini_configured"]
    
    return {
        "status": "ready" if minimum_configured else "misconfigured",
        "multi_agent_enabled": minimum_configured,
        "configurations": config_status,
        "message": "Real Multi-Agent System with Synthesis" if minimum_configured else "Missing API keys for real agents"
    }

@router.get("/test-synthesis")
async def test_synthesis():
    """Test the synthesis system with a simple query"""
    try:
        service = MultiAgentFunnelService()
        
        # Test with minimal query
        result = await service.generate_roadmap(
            user_query="Learn Python programming",
            user_background={
                "experience_level": "Beginner",
                "time_available": "5 hours per week"
            }
        )
        
        return {
            "success": True,
            "test_result": "Synthesis system working",
            "session_id": result.get("metadata", {}).get("session_id"),
            "phases_generated": len(result.get("metadata", {}).get("structured_plan", {}).get("phases", [])),
            "synthesis_confidence": result.get("metadata", {}).get("synthesis_confidence", 0),
            "agents_used": len(result.get("agent_insights", [])),
            "message": "Real multi-agent synthesis test completed successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "Synthesis test failed - check API keys and service configuration"
        }