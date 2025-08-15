import os
import time
from typing import Optional
from pathlib import Path
from murf import Murf
from app.models.schemas import TTSRequest, TTSResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)

class TTSService:
    def __init__(self):
        self.api_key = os.getenv("MURF_API_KEY", "YOUR_MURF_API_KEY_HERE")
        self.client = Murf(api_key=self.api_key)
        self.uploads_dir = Path("uploads")
        self.uploads_dir.mkdir(exist_ok=True)
        
    async def text_to_speech(self, request: TTSRequest) -> TTSResponse:
        """Convert text to speech using Murf API"""
        try:
            logger.info(f"Converting text to speech: {request.text[:50]}...")
            
            # Generate unique filename
            timestamp = int(time.time())
            filename = f"tts_{timestamp}.mp3"
            filepath = self.uploads_dir / filename
            
            # Create TTS request
            tts_request = {
                "text": request.text,
                "voice_id": request.voice_id,
                "speed": request.speed,
                "pitch": request.pitch
            }
            
            # Generate audio
            audio_data = self.client.generate_audio(**tts_request)
            
            # Save audio file
            with open(filepath, "wb") as f:
                f.write(audio_data)
            
            # Create response
            response = TTSResponse(
                success=True,
                message="Text converted to speech successfully",
                audio_url=f"/static/{filename}",
                audio_id=filename
            )
            
            logger.info(f"TTS successful: {filename}")
            return response
            
        except Exception as e:
            logger.error(f"TTS error: {str(e)}")
            return TTSResponse(
                success=False,
                message=f"Error converting text to speech: {str(e)}"
            )
    
    def get_available_voices(self) -> list:
        """Get list of available voices"""
        try:
            voices = self.client.get_voices()
            return voices
        except Exception as e:
            logger.error(f"Error getting voices: {str(e)}")
            return []
