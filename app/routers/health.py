from fastapi import APIRouter, HTTPException
import time
import os
from app.models.schemas import HealthResponse, DetailedHealthResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Simple health check endpoint"""
    logger.info("Health check requested")
    return HealthResponse(
        status="healthy",
        message="Voice Agents Backend is running!"
    )

@router.get("/detailed", response_model=DetailedHealthResponse)
async def detailed_health_check():
    """Detailed health check that monitors all API services"""
    logger.info("Detailed health check requested")
    
    health_status = {
        "overall_status": "healthy",
        "timestamp": time.time(),
        "services": {
            "assembly_ai": {"status": "unknown", "message": ""},
            "gemini_llm": {"status": "unknown", "message": ""},
            "murf_tts": {"status": "unknown", "message": ""}
        }
    }
    
    # Check AssemblyAI
    try:
        assembly_ai_key = os.getenv("ASSEMBLY_AI_API_KEY", "YOUR_ASSEMBLY_AI_API_KEY_HERE")
        if assembly_ai_key == "YOUR_ASSEMBLY_AI_API_KEY_HERE":
            health_status["services"]["assembly_ai"] = {
                "status": "error",
                "message": "API key not configured"
            }
        else:
            health_status["services"]["assembly_ai"] = {
                "status": "configured",
                "message": "API key configured"
            }
    except Exception as e:
        health_status["services"]["assembly_ai"] = {
            "status": "error",
            "message": str(e)
        }
    
    # Check Gemini
    try:
        gemini_key = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
        if gemini_key == "YOUR_GEMINI_API_KEY_HERE":
            health_status["services"]["gemini_llm"] = {
                "status": "error",
                "message": "API key not configured"
            }
        else:
            health_status["services"]["gemini_llm"] = {
                "status": "configured",
                "message": "API key configured"
            }
    except Exception as e:
        health_status["services"]["gemini_llm"] = {
            "status": "error",
            "message": str(e)
        }
    
    # Check Murf
    try:
        murf_key = os.getenv("MURF_API_KEY", "YOUR_MURF_API_KEY_HERE")
        if murf_key == "YOUR_MURF_API_KEY_HERE":
            health_status["services"]["murf_tts"] = {
                "status": "error",
                "message": "API key not configured"
            }
        else:
            health_status["services"]["murf_tts"] = {
                "status": "configured",
                "message": "API key configured"
            }
    except Exception as e:
        health_status["services"]["murf_tts"] = {
            "status": "error",
            "message": str(e)
        }
    
    # Determine overall status
    error_count = sum(1 for service in health_status["services"].values() if service["status"] == "error")
    if error_count > 0:
        health_status["overall_status"] = "degraded" if error_count < len(health_status["services"]) else "unhealthy"
    
    logger.info(f"Health check completed: {health_status['overall_status']}")
    return DetailedHealthResponse(**health_status)
