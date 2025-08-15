import os
import time
from typing import Optional
from pathlib import Path
import assemblyai as aai
from app.models.schemas import TranscriptionResponse
from app.utils.logging import get_logger

logger = get_logger(__name__)

class STTService:
    def __init__(self):
        self.api_key = os.getenv("ASSEMBLY_AI_API_KEY", "YOUR_ASSEMBLY_AI_API_KEY_HERE")
        aai.settings.api_key = self.api_key
        self.transcriber = aai.Transcriber()
        
    async def transcribe_audio(self, audio_file_path: str) -> TranscriptionResponse:
        """Transcribe audio file using AssemblyAI"""
        try:
            logger.info(f"Transcribing audio file: {audio_file_path}")
            
            # Check if file exists
            if not Path(audio_file_path).exists():
                return TranscriptionResponse(
                    success=False,
                    message="Audio file not found"
                )
            
            # Transcribe audio
            transcript = self.transcriber.transcribe(audio_file_path)
            
            if transcript.status == aai.TranscriptStatus.error:
                return TranscriptionResponse(
                    success=False,
                    message=f"Transcription failed: {transcript.error}"
                )
            
            # Extract transcript data
            response = TranscriptionResponse(
                success=True,
                message="Audio transcribed successfully",
                transcript=transcript.text,
                confidence=transcript.confidence,
                audio_duration=transcript.audio_duration
            )
            
            logger.info(f"Transcription successful: {len(transcript.text)} characters")
            return response
            
        except Exception as e:
            logger.error(f"Transcription error: {str(e)}")
            return TranscriptionResponse(
                success=False,
                message=f"Error transcribing audio: {str(e)}"
            )
    
    async def transcribe_uploaded_file(self, file_content: bytes, filename: str) -> TranscriptionResponse:
        """Transcribe uploaded audio file"""
        try:
            logger.info(f"Transcribing uploaded file: {filename}")
            
            # Save uploaded file temporarily
            temp_path = Path("uploads") / filename
            temp_path.parent.mkdir(exist_ok=True)
            
            with open(temp_path, "wb") as f:
                f.write(file_content)
            
            # Transcribe the file
            result = await self.transcribe_audio(str(temp_path))
            
            # Clean up temp file
            if temp_path.exists():
                temp_path.unlink()
            
            return result
            
        except Exception as e:
            logger.error(f"Upload transcription error: {str(e)}")
            return TranscriptionResponse(
                success=False,
                message=f"Error processing uploaded audio: {str(e)}"
            )
