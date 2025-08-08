from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from murf import Murf
import os
import shutil
from typing import Optional
from pathlib import Path
import assemblyai as aai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Create FastAPI instance
app = FastAPI(title="Voice Agents - Day 7", description="30 Days of Voice Agents Backend with TTS, Audio Upload, Transcription, and Echo Bot v2")

# Pydantic models for request/response
class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = "en-US-natalie"  # Default voice (from Murf reference)
    speed: Optional[int] = 0  # Normal speed
    pitch: Optional[int] = 0  # Normal pitch
    
class TTSResponse(BaseModel):
    success: bool
    message: str
    audio_url: Optional[str] = None
    audio_id: Optional[str] = None

# Day 5: Audio upload response model
class AudioUploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    content_type: str
    size_bytes: int
    upload_path: str

# Day 6: Transcription response model
class TranscriptionResponse(BaseModel):
    success: bool
    message: str
    transcript: Optional[str] = None
    confidence: Optional[float] = None
    audio_duration: Optional[float] = None

# Day 7: Echo Bot response model
class EchoBotResponse(BaseModel):
    success: bool
    message: str
    transcript: Optional[str] = None
    audio_url: Optional[str] = None
    voice_used: Optional[str] = None
    confidence: Optional[float] = None

# Murf API configuration
MURF_API_KEY = os.getenv("MURF_API_KEY", "ap2_69e1ff6e-6193-4da9-8f71-b7aad1573f38")

# AssemblyAI configuration - you'll need to set your API key
ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY", "YOUR_ASSEMBLY_AI_API_KEY_HERE")
aai.settings.api_key = ASSEMBLY_AI_API_KEY

# Initialize Murf client
murf_client = Murf(api_key=MURF_API_KEY)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/api/health")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy", "message": "Voice Agents Backend is running!"}

@app.get("/api/voice-agents")
async def get_voice_agents():
    """Sample API endpoint for voice agents"""
    return {
        "project": "30 Days of Voice Agents",
        "day": 7,
        "task": "Echo Bot v2 with TTS",
        "features": ["TTS", "Audio Upload", "Transcription", "Echo Bot v2"],
        "agents": []
    }

@app.post("/api/tts/generate", response_model=TTSResponse)
async def generate_tts(request: TTSRequest):
    """
    Generate text-to-speech audio using Murf's API
    
    This endpoint accepts text and voice parameters, calls Murf's /generate API,
    and returns the URL to the generated audio file.
    """
    
    # Validate input
    if not request.text or len(request.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    if len(request.text) > 3000:  # Murf's typical character limit
        raise HTTPException(status_code=400, detail="Text too long. Maximum 3000 characters allowed")
    
    # For demo purposes, we'll simulate the Murf API call
    # In a real implementation, you would make the actual API call to Murf
    
    try:
        # Use the official Murf SDK
        print(f"Generating TTS with Murf SDK for text: {request.text[:50]}...")
        
        response = murf_client.text_to_speech.generate(
            text=request.text,
            voice_id=request.voice_id
        )
        
        print(f"Murf SDK Response: {response}")
        
        # Extract audio file URL from response
        audio_url = response.audio_file if hasattr(response, 'audio_file') else str(response)
        
        return TTSResponse(
            success=True,
            message=f"✅ TTS generation successful via Murf SDK! Generated audio for: '{request.text[:50]}{'...' if len(request.text) > 50 else ''}'",
            audio_url=audio_url,
            audio_id=f"murf_{int(__import__('time').time())}"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.get("/api/tts/voices")
async def get_available_voices():
    """Get list of available voices"""
    try:
        # Try to get voices from Murf SDK if it has a voices method
        # For now, we'll use common Murf voice IDs
        print("Fetching available voices...")
        
        # Common Murf voices - you can update this list based on your Murf account
        murf_voices = [
            {"id": "en-US-natalie", "name": "Natalie", "language": "English (US)", "gender": "Female", "accent": "American"},
            {"id": "en-US-davis", "name": "Davis", "language": "English (US)", "gender": "Male", "accent": "American"},
            {"id": "en-US-jane", "name": "Jane", "language": "English (US)", "gender": "Female", "accent": "American"},
            {"id": "en-US-mike", "name": "Mike", "language": "English (US)", "gender": "Male", "accent": "American"},
            {"id": "en-UK-emma", "name": "Emma", "language": "English (UK)", "gender": "Female", "accent": "British"},
            {"id": "en-AU-olivia", "name": "Olivia", "language": "English (AU)", "gender": "Female", "accent": "Australian"},
            {"id": "es-ES-carlos", "name": "Carlos", "language": "Spanish (Spain)", "gender": "Male", "accent": "Spanish"},
            {"id": "fr-FR-marie", "name": "Marie", "language": "French (France)", "gender": "Female", "accent": "French"},
        ]
        
        return {
            "success": True,
            "voices": murf_voices,
            "total_count": len(murf_voices),
            "source": "Murf Voice Library"
        }
        
    except Exception as e:
        print(f"Error fetching voices: {e}")
        
        # Fallback voices
        fallback_voices = [
            {"id": "en-US-natalie", "name": "Natalie", "language": "English (US)", "gender": "Female"},
            {"id": "en-US-davis", "name": "Davis", "language": "English (US)", "gender": "Male"},
        ]
        
        return {
            "success": True,
            "voices": fallback_voices,
            "total_count": len(fallback_voices),
            "source": "Fallback voices"
        }

# Day 5: Audio Upload Endpoint
@app.post("/api/audio/upload", response_model=AudioUploadResponse)
async def upload_audio(audio_file: UploadFile = File(...)):
    """
    Upload and save audio file from Echo Bot recording
    """
    try:
        # Validate file type
        allowed_types = ["audio/webm", "audio/wav", "audio/mp3", "audio/ogg", "audio/mpeg"]
        if audio_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Generate unique filename with timestamp
        import time
        timestamp = int(time.time())
        file_extension = audio_file.filename.split('.')[-1] if '.' in audio_file.filename else 'webm'
        safe_filename = f"echo_recording_{timestamp}.{file_extension}"
        
        # Save file to uploads directory
        file_path = UPLOADS_DIR / safe_filename
        
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)
        
        # Get file size
        file_size = os.path.getsize(file_path)
        
        return AudioUploadResponse(
            success=True,
            message="Audio file uploaded successfully",
            filename=safe_filename,
            content_type=audio_file.content_type,
            size_bytes=file_size,
            upload_path=str(file_path)
        )
        
    except Exception as e:
        print(f"Error uploading audio: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# Day 6: Audio Transcription Endpoint
@app.post("/api/transcribe/file", response_model=TranscriptionResponse)
async def transcribe_audio_file(audio_file: UploadFile = File(...)):
    """
    Transcribe audio file using AssemblyAI
    """
    try:
        # Validate file type
        allowed_types = ["audio/webm", "audio/wav", "audio/mp3", "audio/ogg", "audio/mpeg", "audio/m4a", "audio/mp4"]
        if audio_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Check if AssemblyAI API key is set
        if ASSEMBLY_AI_API_KEY == "YOUR_ASSEMBLY_AI_API_KEY_HERE":
            raise HTTPException(
                status_code=500,
                detail="AssemblyAI API key not configured. Please set ASSEMBLY_AI_API_KEY environment variable."
            )
        
        # Read audio file content
        audio_content = await audio_file.read()
        
        # Create AssemblyAI transcriber
        transcriber = aai.Transcriber()
        
        # Transcribe the audio directly from binary data
        print(f"Starting transcription for file: {audio_file.filename}")
        transcript = transcriber.transcribe(audio_content)
        
        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {transcript.error}"
            )
        
        # Calculate audio duration if available
        audio_duration = transcript.audio_duration / 1000 if transcript.audio_duration else None
        
        return TranscriptionResponse(
            success=True,
            message="Audio transcribed successfully",
            transcript=transcript.text,
            confidence=transcript.confidence,
            audio_duration=audio_duration
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

# Day 7: Echo Bot with TTS - Transcribe and replay with Murf voice
@app.post("/api/tts/echo", response_model=EchoBotResponse)
async def echo_with_tts(audio_file: UploadFile = File(...), voice_id: str = "en-US-natalie"):
    """
    Echo Bot v2: Transcribe audio and replay with Murf TTS voice
    """
    try:
        # Validate file type
        allowed_types = ["audio/webm", "audio/wav", "audio/mp3", "audio/ogg", "audio/mpeg", "audio/m4a", "audio/mp4"]
        if audio_file.content_type not in allowed_types:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
            )
        
        # Check if API keys are configured
        if ASSEMBLY_AI_API_KEY == "YOUR_ASSEMBLY_AI_API_KEY_HERE":
            raise HTTPException(
                status_code=500,
                detail="AssemblyAI API key not configured. Please set ASSEMBLY_AI_API_KEY environment variable."
            )
        
        print(f"Starting Echo Bot v2 for file: {audio_file.filename}")
        
        # Step 1: Transcribe the audio using AssemblyAI
        audio_content = await audio_file.read()
        transcriber = aai.Transcriber()
        
        print("Step 1: Transcribing audio with AssemblyAI...")
        transcript = transcriber.transcribe(audio_content)
        
        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {transcript.error}"
            )
        
        if not transcript.text or transcript.text.strip() == "":
            raise HTTPException(
                status_code=400,
                detail="No speech detected in the audio. Please try speaking more clearly."
            )
        
        print(f"Transcription successful: '{transcript.text}'")
        
        # Step 2: Generate TTS audio using Murf
        print(f"Step 2: Generating TTS with Murf voice '{voice_id}'...")
        
        try:
            murf_response = murf_client.text_to_speech.generate(
                text=transcript.text,
                voice_id=voice_id
            )
            
            print(f"Murf TTS Response: {murf_response}")
            
            # Extract audio file URL from response
            audio_url = murf_response.audio_file if hasattr(murf_response, 'audio_file') else str(murf_response)
            
            return EchoBotResponse(
                success=True,
                message=f"Echo Bot v2 successful! Transcribed and generated with {voice_id} voice.",
                transcript=transcript.text,
                audio_url=audio_url,
                voice_used=voice_id,
                confidence=transcript.confidence
            )
            
        except Exception as murf_error:
            print(f"Murf TTS Error: {murf_error}")
            raise HTTPException(
                status_code=500,
                detail=f"TTS generation failed: {str(murf_error)}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in Echo Bot v2: {e}")
        raise HTTPException(status_code=500, detail=f"Echo Bot failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
