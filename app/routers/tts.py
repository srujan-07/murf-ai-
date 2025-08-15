from fastapi import APIRouter, HTTPException
from app.models.schemas import TTSRequest, TTSResponse
from app.services.tts_service import TTSService
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/tts", tags=["tts"])

# Initialize TTS service
tts_service = TTSService()

@router.post("/generate", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    """Convert text to speech"""
    logger.info(f"TTS request received: {len(request.text)} characters")
    
    try:
        response = await tts_service.text_to_speech(request)
        return response
    except Exception as e:
        logger.error(f"TTS endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/voices")
async def get_available_voices():
    """Get list of available voices"""
    logger.info("Voice list requested")
    
    try:
        voices = tts_service.get_available_voices()
        return {
            "success": True,
            "voices": voices,
            "count": len(voices)
        }
    except Exception as e:
        logger.error(f"Error getting voices: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
