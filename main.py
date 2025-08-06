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

# Create FastAPI instance
app = FastAPI(title="Voice Agents - Day 5", description="30 Days of Voice Agents Backend with TTS and Audio Upload")

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

# Murf API configuration
MURF_API_KEY = os.getenv("MURF_API_KEY", "ap2_69e1ff6e-6193-4da9-8f71-b7aad1573f38")

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
        "day": 2,
        "task": "REST TTS Integration",
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

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
