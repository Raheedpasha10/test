#!/usr/bin/env python3

"""
Quick fix for the multi-agent system async issue
This script creates a simple working version for immediate testing
"""

import asyncio
import json
import time
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
import os
from groq import Groq
import google.generativeai as genai

# Simple working multi-agent function
async def test_single_agent():
    """Test a single agent to see if API calls work"""
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Load API keys
    groq_api_key = os.getenv("GROQ_API_KEY")
    google_api_key = os.getenv("GOOGLE_GENAI_API_KEY")
    
    if not groq_api_key or not google_api_key:
        print("❌ API keys not loaded")
        return None
    
    print("✅ API keys loaded")
    
    # Test Groq
    try:
        groq_client = Groq(api_key=groq_api_key)
        
        def sync_groq_call():
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a career advisor."},
                    {"role": "user", "content": "Create a simple UI/UX design learning roadmap with 3 phases. Format as markdown with clear sections."}
                ],
                model="llama-3.1-8b-instant",
                temperature=0.7,
                max_tokens=2000
            )
            return response.choices[0].message.content
        
        loop = asyncio.get_event_loop()
        groq_result = await loop.run_in_executor(None, sync_groq_call)
        
        print("✅ Groq test successful")
        print(f"📝 Generated {len(groq_result)} characters")
        print("=" * 50)
        print(groq_result[:500] + "..." if len(groq_result) > 500 else groq_result)
        print("=" * 50)
        
        return {
            "success": True,
            "final_roadmap": groq_result,
            "agent_insights": [],
            "metadata": {
                "num_agents": 1,
                "successful_agents": 1,
                "query": "UI/UX design learning",
                "structured_plan": {},
                "session_id": "test123",
                "timestamp": str(time.time()),
                "execution_time": "~2s"
            },
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "funneling_report": {
                "session_id": "test123",
                "agent_performance": {
                    "total_agents": 1,
                    "successful_agents": 1
                }
            }
        }
        
    except Exception as e:
        print(f"❌ Groq test failed: {e}")
        return None

if __name__ == "__main__":
    result = asyncio.run(test_single_agent())
    if result:
        print("🎉 Single agent test successful!")
        print(json.dumps(result, indent=2))
    else:
        print("❌ Single agent test failed!")