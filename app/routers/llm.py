from fastapi import APIRouter, HTTPException
from app.models.schemas import LLMRequest, LLMResponse, LLMQueryRequest, LLMQueryResponse
from app.services.llm_service import LLMService
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/llm", tags=["llm"])

# Initialize LLM service
llm_service = LLMService()

@router.post("/generate", response_model=LLMResponse)
async def generate_llm_response(request: LLMRequest):
    """Generate response using LLM"""
    logger.info(f"LLM generation request: {len(request.text)} characters")
    
    try:
        response = await llm_service.generate_response(request)
        return response
    except Exception as e:
        logger.error(f"LLM generation endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/query", response_model=LLMQueryResponse)
async def query_llm(request: LLMQueryRequest):
    """Query LLM with advanced parameters"""
    logger.info(f"LLM query request: {len(request.text)} characters")
    
    try:
        response = await llm_service.query_llm(request)
        return response
    except Exception as e:
        logger.error(f"LLM query endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_available_models():
    """Get list of available LLM models"""
    logger.info("LLM models list requested")
    
    try:
        models = llm_service.get_available_models()
        return {
            "success": True,
            "models": models,
            "count": len(models),
            "default_model": llm_service.default_model
        }
    except Exception as e:
        logger.error(f"Error getting models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
