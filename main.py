from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn
from murf import Murf
import os
import shutil
import time
from typing import Optional
from pathlib import Path
import assemblyai as aai
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv()

# Create FastAPI instance
app = FastAPI(title="Voice Agents - Day 9", description="30 Days of Voice Agents Backend with TTS, Transcription, LLM Integration, and Voice-to-Voice AI Pipeline")

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

# Day 8: LLM request/response models
class LLMRequest(BaseModel):
    text: str
    model: Optional[str] = "gemini-2.0-flash-exp"  # Default Gemini model

class LLMResponse(BaseModel):
    success: bool
    message: str
    response_text: Optional[str] = None
    model_used: Optional[str] = None

# Day 8: LLM Query request/response models
class LLMQueryRequest(BaseModel):
    text: str
    model: Optional[str] = "gemini-1.5-flash"  # Default Gemini model
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class LLMQueryResponse(BaseModel):
    success: bool
    message: str
    query: str
    response: Optional[str] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None

# Day 9: Audio LLM Query response model
class AudioLLMQueryResponse(BaseModel):
    success: bool
    message: str
    transcribed_text: Optional[str] = None
    llm_response: Optional[str] = None
    audio_url: Optional[str] = None
    model_used: Optional[str] = None
    voice_used: Optional[str] = None
    processing_time: Optional[float] = None

# Day 10: Chat History models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: float

class ChatSession(BaseModel):
    session_id: str
    messages: list[ChatMessage]
    created_at: float
    updated_at: float

class ChatResponse(BaseModel):
    success: bool
    message: str
    session_id: str
    transcribed_text: Optional[str] = None
    llm_response: Optional[str] = None
    audio_url: Optional[str] = None
    model_used: Optional[str] = None
    voice_used: Optional[str] = None
    processing_time: Optional[float] = None
    message_count: Optional[int] = None

# Murf API configuration
MURF_API_KEY = os.getenv("MURF_API_KEY", "YOUR_MURF_API_KEY_HERE")

# AssemblyAI configuration - you'll need to set your API key
ASSEMBLY_AI_API_KEY = os.getenv("ASSEMBLY_AI_API_KEY", "YOUR_ASSEMBLY_AI_API_KEY_HERE")
aai.settings.api_key = ASSEMBLY_AI_API_KEY

# Google Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Murf client
murf_client = Murf(api_key=MURF_API_KEY)

# Day 10: In-memory chat history storage
# Note: In production, use a proper database like Redis, PostgreSQL, etc.
chat_sessions: dict[str, ChatSession] = {}

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

# Day 11: Enhanced API Health Check with Service Monitoring
@app.get("/api/health/detailed")
async def detailed_health_check():
    """Detailed health check that monitors all API services"""
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
        if ASSEMBLY_AI_API_KEY == "YOUR_ASSEMBLY_AI_API_KEY_HERE":
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
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
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
        if MURF_API_KEY == "YOUR_MURF_API_KEY_HERE":
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
    
    if error_count == 0:
        health_status["overall_status"] = "healthy"
    elif error_count < 3:
        health_status["overall_status"] = "degraded"
    else:
        health_status["overall_status"] = "critical"
    
    return health_status

@app.get("/api/voice-agents")
async def get_voice_agents():
    """Sample API endpoint for voice agents"""
    return {
        "project": "30 Days of Voice Agents",
        "day": 8,
        "task": "LLM Integration with Gemini",
        "features": ["TTS", "Audio Upload", "Transcription", "Echo Bot v2", "LLM Query"],
        "endpoints": [
            "/api/tts/generate",
            "/api/audio/upload", 
            "/api/transcribe/file",
            "/api/tts/echo",
            "/api/llm/query"
        ],
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

# Day 8: LLM Query Endpoint with Google Gemini
@app.post("/api/llm/query", response_model=LLMQueryResponse)
async def query_llm(request: LLMQueryRequest):
    """
    Query Google Gemini LLM with text input
    """
    try:
        # Validate input
        if not request.text or len(request.text.strip()) == 0:
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        if len(request.text) > 10000:  # Reasonable limit
            raise HTTPException(status_code=400, detail="Text too long. Maximum 10000 characters allowed")
        
        # Check if Gemini API key is configured
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            raise HTTPException(
                status_code=500,
                detail="Gemini API key not configured. Please set GEMINI_API_KEY environment variable."
            )
        
        print(f"Querying Gemini with: '{request.text[:100]}{'...' if len(request.text) > 100 else ''}'")
        
        # Initialize Gemini model
        model = genai.GenerativeModel(request.model)
        
        # Simple generation without complex config first
        try:
            response = model.generate_content(request.text)
            print(f"Raw response received: {type(response)}")
            print(f"Response text: {response.text[:200] if response.text else 'No text'}")
        except Exception as e:
            print(f"Error in generate_content: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate content: {str(e)}"
            )
        
        # Check if response was generated successfully
        if not response.text:
            raise HTTPException(
                status_code=500,
                detail="No response generated by Gemini. The content might have been blocked."
            )
        
        print(f"Gemini response generated successfully: {len(response.text)} characters")
        
        # Extract token usage if available
        tokens_used = None
        if hasattr(response, 'usage_metadata') and response.usage_metadata:
            tokens_used = response.usage_metadata.total_token_count
        
        return LLMQueryResponse(
            success=True,
            message="LLM query successful",
            query=request.text,
            response=response.text,
            model_used=request.model,
            tokens_used=tokens_used
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error querying Gemini LLM: {e}")
        raise HTTPException(status_code=500, detail=f"LLM query failed: {str(e)}")

# Day 9: Audio-based LLM Query Endpoint - Voice to Voice AI
@app.post("/api/llm/query/audio", response_model=AudioLLMQueryResponse)
async def query_llm_with_audio(
    audio_file: UploadFile = File(...), 
    model: str = "gemini-1.5-flash",
    voice: str = "en-US-natalie",
    temperature: float = 0.7
):
    """
    Voice-to-Voice AI Pipeline:
    1. Transcribe audio with AssemblyAI
    2. Query Google Gemini LLM 
    3. Generate response audio with Murf TTS
    4. Return audio URL for playback
    """
    start_time = time.time()
    
    try:
        # Step 1: Validate audio file
        if not audio_file.filename:
            raise HTTPException(status_code=400, detail="No audio file provided")
        
        # Save uploaded audio file
        file_id = int(time.time() * 1000)  # Use timestamp as unique ID
        audio_filename = f"voice_query_{file_id}.webm"
        audio_path = UPLOADS_DIR / audio_filename
        
        # Write uploaded file to disk
        audio_content = await audio_file.read()
        with open(audio_path, "wb") as f:
            f.write(audio_content)
        
        print(f"Step 1: Audio file saved: {audio_filename}")
        
        # Step 2: Transcribe audio with AssemblyAI
        print("Step 2: Transcribing audio with AssemblyAI...")
        
        # Check AssemblyAI API key
        if ASSEMBLY_AI_API_KEY == "YOUR_ASSEMBLY_AI_API_KEY_HERE":
            raise HTTPException(
                status_code=500,
                detail="AssemblyAI API key not configured"
            )
        
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(str(audio_path))
        
        if transcript.status == aai.TranscriptStatus.error:
            raise HTTPException(
                status_code=500,
                detail=f"Transcription failed: {transcript.error}"
            )
        
        transcribed_text = transcript.text
        if not transcribed_text or len(transcribed_text.strip()) == 0:
            raise HTTPException(
                status_code=400,
                detail="No speech detected in audio file"
            )
        
        print(f"Step 2 Complete: Transcribed text: '{transcribed_text[:100]}...'")
        
        # Step 3: Query Gemini LLM
        print("Step 3: Querying Gemini LLM...")
        
        # Check Gemini API key
        if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            raise HTTPException(
                status_code=500,
                detail="Gemini API key not configured"
            )
        
        # Add instruction to keep responses concise for TTS
        llm_prompt = f"""Please provide a helpful and concise response to this question (max 2000 characters for voice synthesis): {transcribed_text}"""
        
        gemini_model = genai.GenerativeModel(model)
        llm_response = gemini_model.generate_content(llm_prompt)
        
        if not llm_response.text:
            raise HTTPException(
                status_code=500,
                detail="No response generated by Gemini"
            )
        
        llm_text = llm_response.text.strip()
        print(f"Step 3 Complete: LLM response: '{llm_text[:100]}...' ({len(llm_text)} chars)")
        
        # Step 4: Handle long responses (Murf 3000 char limit)
        if len(llm_text) > 3000:
            print(f"Response too long ({len(llm_text)} chars), truncating to 2800 chars...")
            llm_text = llm_text[:2800] + "..."
        
        # Step 5: Generate audio with Murf TTS
        print("Step 4: Generating audio with Murf TTS...")
        
        # Check Murf API key
        if MURF_API_KEY == "YOUR_MURF_API_KEY_HERE":
            raise HTTPException(
                status_code=500,
                detail="Murf API key not configured"
            )
        
        # Generate audio with Murf
        tts_response = murf_client.text_to_speech.generate(
            voice_id=voice,
            text=llm_text
        )
        
        print(f"Murf TTS Response: {tts_response}")
        
        # Extract audio file URL from response (same as working endpoint)
        audio_url = tts_response.audio_file if hasattr(tts_response, 'audio_file') else str(tts_response)
        
        # Cleanup: Remove uploaded audio file
        try:
            audio_path.unlink()
        except:
            pass  # Ignore cleanup errors
        
        processing_time = time.time() - start_time
        
        return AudioLLMQueryResponse(
            success=True,
            message="Voice-to-voice AI query successful",
            transcribed_text=transcribed_text,
            llm_response=llm_text,
            audio_url=audio_url,
            model_used=model,
            voice_used=voice,
            processing_time=round(processing_time, 2)
        )
        
    except HTTPException:
        # Cleanup on error
        try:
            if 'audio_path' in locals():
                audio_path.unlink()
        except:
            pass
        raise
    except Exception as e:
        # Cleanup on error
        try:
            if 'audio_path' in locals():
                audio_path.unlink()
        except:
            pass
        print(f"Error in voice-to-voice AI pipeline: {e}")
        raise HTTPException(
            status_code=500, 
            detail=f"Voice-to-voice AI pipeline failed: {str(e)}"
        )

# Day 10: Chat History Helper Functions
def get_or_create_chat_session(session_id: str) -> ChatSession:
    """Get existing chat session or create a new one"""
    if session_id not in chat_sessions:
        chat_sessions[session_id] = ChatSession(
            session_id=session_id,
            messages=[],
            created_at=time.time(),
            updated_at=time.time()
        )
    return chat_sessions[session_id]

def add_message_to_session(session_id: str, role: str, content: str) -> None:
    """Add a message to the chat session"""
    session = get_or_create_chat_session(session_id)
    message = ChatMessage(
        role=role,
        content=content,
        timestamp=time.time()
    )
    session.messages.append(message)
    session.updated_at = time.time()

def build_conversation_context(session_id: str, max_messages: int = 20) -> str:
    """Build conversation context from chat history"""
    session = get_or_create_chat_session(session_id)
    
    # Get recent messages (limit to avoid token limits)
    recent_messages = session.messages[-max_messages:] if len(session.messages) > max_messages else session.messages
    
    if not recent_messages:
        return ""
    
    # Format conversation history for LLM
    context = "Previous conversation:\n"
    for msg in recent_messages:
        role_name = "User" if msg.role == "user" else "Assistant"
        context += f"{role_name}: {msg.content}\n"
    
    context += "\nNew message:\n"
    return context

# Day 10: Chat Agent Endpoint with Session Management
@app.post("/api/agent/chat/{session_id}", response_model=ChatResponse)
async def chat_with_agent(
    session_id: str,
    audio_file: UploadFile = File(...), 
    model: str = "gemini-1.5-flash",
    voice: str = "en-US-natalie",
    temperature: float = 0.7
):
    """
    Chat Agent with Session-based History:
    1. Transcribe audio with AssemblyAI
    2. Fetch chat history for session
    3. Build conversation context with previous messages
    4. Query Google Gemini LLM with full context
    5. Store user message and AI response in chat history
    6. Generate response audio with Murf TTS
    7. Return audio URL for playback
    """
    start_time = time.time()
    transcribed_text = None
    llm_response_text = None
    audio_url = None
    error_occurred = False
    error_step = None
    
    try:
        # Step 1: Validate audio file and session ID
        if not audio_file.filename:
            raise HTTPException(status_code=400, detail="No audio file provided")
        
        if not session_id or len(session_id.strip()) == 0:
            raise HTTPException(status_code=400, detail="Invalid session ID")
        
        # Save uploaded audio file
        file_id = int(time.time() * 1000)  # Use timestamp as unique ID
        audio_filename = f"chat_{session_id}_{file_id}.webm"
        audio_path = UPLOADS_DIR / audio_filename
        
        # Write uploaded file to disk
        audio_content = await audio_file.read()
        with open(audio_path, "wb") as f:
            f.write(audio_content)
        
        print(f"Step 1: Audio file saved for session {session_id}: {audio_filename}")
        
        # Step 2: Transcribe audio with AssemblyAI (with error handling)
        try:
            print("Step 2: Transcribing audio with AssemblyAI...")
            
            # Check AssemblyAI API key
            if ASSEMBLY_AI_API_KEY == "YOUR_ASSEMBLY_AI_API_KEY_HERE":
                raise ValueError("AssemblyAI API key not configured")
            
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(str(audio_path))
            
            if transcript.status == aai.TranscriptStatus.error:
                raise ValueError(f"Transcription failed: {transcript.error}")
            
            transcribed_text = transcript.text
            if not transcribed_text or len(transcribed_text.strip()) == 0:
                raise ValueError("No speech detected in audio file")
            
            print(f"Step 2 Complete: Transcribed text: '{transcribed_text[:100]}...'")
            
        except Exception as e:
            error_step = "transcription"
            error_occurred = True
            print(f"❌ Transcription Error: {e}")
            
            # Fallback: Use a default message for transcription failures
            transcribed_text = "Sorry, I couldn't understand what you said due to a technical issue."
            
            # Add fallback message to session
            add_message_to_session(session_id, "user", transcribed_text)
        
        # Step 3: Add user message to chat history (if transcription succeeded)
        if not error_occurred:
            add_message_to_session(session_id, "user", transcribed_text)
        
        # Step 4: Build conversation context with chat history
        conversation_context = build_conversation_context(session_id)
        print(f"Step 3: Built conversation context with {len(get_or_create_chat_session(session_id).messages)} messages")
        
        # Step 5: Query Gemini LLM with conversation context (with error handling)
        try:
            print("Step 4: Querying Gemini LLM with conversation context...")
            
            # Check Gemini API key
            if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
                raise ValueError("Gemini API key not configured")
            
            # Create prompt with conversation context
            if error_occurred and error_step == "transcription":
                # Special prompt for transcription failures
                llm_prompt = """I'm having trouble hearing what the user said due to a technical issue with speech recognition. Please provide a helpful apology and offer to try again, keeping the response under 2000 characters for voice synthesis."""
            elif conversation_context:
                llm_prompt = f"""{conversation_context}User: {transcribed_text}

Please provide a helpful and conversational response that takes into account the previous conversation history. Keep responses concise for voice synthesis (max 2000 characters)."""
            else:
                llm_prompt = f"""Please provide a helpful and conversational response to this message (max 2000 characters for voice synthesis): {transcribed_text}"""
            
            gemini_model = genai.GenerativeModel(model)
            llm_response = gemini_model.generate_content(llm_prompt)
            
            if not llm_response.text:
                raise ValueError("No response generated by Gemini")
            
            llm_response_text = llm_response.text.strip()
            print(f"Step 4 Complete: LLM response: '{llm_response_text[:100]}...' ({len(llm_response_text)} chars)")
            
        except Exception as e:
            if not error_occurred:
                error_step = "llm"
            error_occurred = True
            print(f"❌ LLM Error: {e}")
            
            # Fallback response for LLM failures
            if error_step == "transcription":
                llm_response_text = "I'm having trouble connecting to my speech recognition service right now. Could you please try speaking again in a moment?"
            else:
                llm_response_text = "I'm having trouble processing your request right now due to a technical issue. Please try again in a moment."
        
        # Step 6: Add AI response to chat history
        add_message_to_session(session_id, "assistant", llm_response_text)
        
        # Step 7: Handle long responses (Murf 3000 char limit)
        if len(llm_response_text) > 3000:
            print(f"Response too long ({len(llm_response_text)} chars), truncating to 2800 chars...")
            llm_response_text = llm_response_text[:2800] + "..."
        
        # Step 8: Generate audio with Murf TTS (with error handling)
        try:
            print("Step 5: Generating audio with Murf TTS...")
            
            # Check Murf API key
            if MURF_API_KEY == "YOUR_MURF_API_KEY_HERE":
                raise ValueError("Murf API key not configured")
            
            # Generate audio with Murf
            tts_response = murf_client.text_to_speech.generate(
                voice_id=voice,
                text=llm_response_text
            )
            
            print(f"Murf TTS Response: {tts_response}")
            
            # Extract audio file URL from response
            audio_url = tts_response.audio_file if hasattr(tts_response, 'audio_file') else str(tts_response)
            
        except Exception as e:
            if not error_occurred:
                error_step = "tts"
            error_occurred = True
            print(f"❌ TTS Error: {e}")
            
            # For TTS failures, we still return the text but no audio
            audio_url = None
        
        # Cleanup: Remove uploaded audio file
        try:
            audio_path.unlink()
        except:
            pass  # Ignore cleanup errors
        
        processing_time = time.time() - start_time
        message_count = len(get_or_create_chat_session(session_id).messages)
        
        # Determine success status and message
        if error_occurred:
            success_message = f"Chat response completed with {error_step} service issues"
            if not audio_url:
                success_message += " (text response only)"
        else:
            success_message = f"Chat response successful for session {session_id}"
        
        return ChatResponse(
            success=not error_occurred,  # False if any errors occurred
            message=success_message,
            session_id=session_id,
            transcribed_text=transcribed_text,
            llm_response=llm_response_text,
            audio_url=audio_url,
            model_used=model,
            voice_used=voice,
            processing_time=round(processing_time, 2),
            message_count=message_count
        )
        
    except HTTPException:
        # Cleanup on error
        try:
            if 'audio_path' in locals():
                audio_path.unlink()
        except:
            pass
        raise
    except Exception as e:
        # Cleanup on error
        try:
            if 'audio_path' in locals():
                audio_path.unlink()
        except:
            pass
        print(f"Error in chat agent pipeline: {e}")
        
        # Return fallback response for critical errors
        return ChatResponse(
            success=False,
            message="Critical system error occurred",
            session_id=session_id,
            transcribed_text="System error",
            llm_response="I'm experiencing technical difficulties right now. Please try again in a few minutes.",
            audio_url=None,
            model_used=model,
            voice_used=voice,
            processing_time=round(time.time() - start_time, 2),
            message_count=0
        )

# Day 10: Get Chat History Endpoint
@app.get("/api/agent/chat/{session_id}/history")
async def get_chat_history(session_id: str, limit: int = 50):
    """Get chat history for a session"""
    try:
        session = get_or_create_chat_session(session_id)
        
        # Return recent messages (limited)
        recent_messages = session.messages[-limit:] if len(session.messages) > limit else session.messages
        
        return {
            "success": True,
            "session_id": session_id,
            "message_count": len(session.messages),
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp
                }
                for msg in recent_messages
            ],
            "created_at": session.created_at,
            "updated_at": session.updated_at
        }
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch chat history: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
