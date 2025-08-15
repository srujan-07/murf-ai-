import time
import uuid
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import (
    ChatResponse, ChatSession, ChatMessage, 
    AudioLLMQueryResponse, EchoBotResponse
)
from app.services.tts_service import TTSService
from app.services.stt_service import STTService
from app.services.llm_service import LLMService
from app.utils.file_utils import FileUtils
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/agent", tags=["agent"])

# Initialize services
tts_service = TTSService()
stt_service = STTService()
llm_service = LLMService()
file_utils = FileUtils()

# In-memory chat history storage (in production, use a proper database)
chat_sessions: dict[str, ChatSession] = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(
    audio_file: UploadFile = File(...),
    session_id: str = None
):
    """Chat with the voice agent using audio input"""
    start_time = time.time()
    
    try:
        # Create or get chat session
        if not session_id or session_id not in chat_sessions:
            session_id = str(uuid.uuid4())
            chat_sessions[session_id] = ChatSession(
                session_id=session_id,
                messages=[],
                created_at=time.time(),
                updated_at=time.time()
            )
        
        session = chat_sessions[session_id]
        
        # Validate audio file
        if not audio_file.content_type or not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Step 1: Transcribe audio
        logger.info(f"Transcribing audio for session {session_id}")
        file_content = await audio_file.read()
        transcription = await stt_service.transcribe_uploaded_file(file_content, audio_file.filename)
        
        if not transcription.success:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {transcription.message}")
        
        # Step 2: Generate LLM response
        logger.info(f"Generating LLM response for: {transcription.transcript}")
        llm_request = LLMRequest(text=transcription.transcript)
        llm_response = await llm_service.generate_response(llm_request)
        
        if not llm_response.success:
            raise HTTPException(status_code=500, detail=f"LLM generation failed: {llm_response.message}")
        
        # Step 3: Convert response to speech
        logger.info(f"Converting LLM response to speech")
        tts_request = TTSRequest(text=llm_response.response_text)
        tts_response = await tts_service.text_to_speech(tts_request)
        
        if not tts_response.success:
            raise HTTPException(status_code=500, detail=f"TTS failed: {tts_response.message}")
        
        # Update chat session
        user_message = ChatMessage(
            role="user",
            content=transcription.transcript,
            timestamp=time.time()
        )
        assistant_message = ChatMessage(
            role="assistant",
            content=llm_response.response_text,
            timestamp=time.time()
        )
        
        session.messages.extend([user_message, assistant_message])
        session.updated_at = time.time()
        
        processing_time = time.time() - start_time
        
        # Create response
        response = ChatResponse(
            success=True,
            message="Chat completed successfully",
            session_id=session_id,
            transcribed_text=transcription.transcript,
            llm_response=llm_response.response_text,
            audio_url=tts_response.audio_url,
            model_used=llm_response.model_used,
            voice_used=tts_response.audio_id,
            processing_time=processing_time,
            message_count=len(session.messages)
        )
        
        logger.info(f"Chat completed successfully for session {session_id}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/echo", response_model=EchoBotResponse)
async def echo_bot(audio_file: UploadFile = File(...)):
    """Simple echo bot that repeats what you say"""
    try:
        # Validate audio file
        if not audio_file.content_type or not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Transcribe audio
        file_content = await audio_file.read()
        transcription = await stt_service.transcribe_uploaded_file(file_content, audio_file.filename)
        
        if not transcription.success:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {transcription.message}")
        
        # Convert back to speech
        tts_request = TTSRequest(text=transcription.transcript)
        tts_response = await tts_service.text_to_speech(tts_request)
        
        if not tts_response.success:
            raise HTTPException(status_code=500, detail=f"TTS failed: {tts_response.message}")
        
        response = EchoBotResponse(
            success=True,
            message="Echo completed successfully",
            transcript=transcription.transcript,
            audio_url=tts_response.audio_url,
            voice_used=tts_response.audio_id,
            confidence=transcription.confidence
        )
        
        logger.info("Echo bot completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Echo bot error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/audio-query", response_model=AudioLLMQueryResponse)
async def audio_llm_query(
    audio_file: UploadFile = File(...),
    model: str = "gemini-1.5-flash"
):
    """Process audio query through LLM and return audio response"""
    start_time = time.time()
    
    try:
        # Validate audio file
        if not audio_file.content_type or not audio_file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Transcribe audio
        file_content = await audio_file.read()
        transcription = await stt_service.transcribe_uploaded_file(file_content, audio_file.filename)
        
        if not transcription.success:
            raise HTTPException(status_code=500, detail=f"Transcription failed: {transcription.message}")
        
        # Query LLM
        llm_request = LLMQueryRequest(text=transcription.transcript, model=model)
        llm_response = await llm_service.query_llm(llm_request)
        
        if not llm_response.success:
            raise HTTPException(status_code=500, detail=f"LLM query failed: {llm_response.message}")
        
        # Convert response to speech
        tts_request = TTSRequest(text=llm_response.response)
        tts_response = await tts_service.text_to_speech(tts_request)
        
        if not tts_response.success:
            raise HTTPException(status_code=500, detail=f"TTS failed: {tts_response.message}")
        
        processing_time = time.time() - start_time
        
        response = AudioLLMQueryResponse(
            success=True,
            message="Audio LLM query completed successfully",
            transcribed_text=transcription.transcript,
            llm_response=llm_response.response,
            audio_url=tts_response.audio_url,
            model_used=llm_response.model_used,
            voice_used=tts_response.audio_id,
            processing_time=processing_time
        )
        
        logger.info("Audio LLM query completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Audio LLM query error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sessions/{session_id}")
async def get_chat_session(session_id: str):
    """Get chat session details"""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    session = chat_sessions[session_id]
    return {
        "success": True,
        "session": session,
        "message_count": len(session.messages)
    }

@router.get("/sessions")
async def list_chat_sessions():
    """List all chat sessions"""
    sessions = []
    for session_id, session in chat_sessions.items():
        sessions.append({
            "session_id": session_id,
            "message_count": len(session.messages),
            "created_at": session.created_at,
            "updated_at": session.updated_at
        })
    
    return {
        "success": True,
        "sessions": sessions,
        "total_sessions": len(sessions)
    }

@router.delete("/sessions/{session_id}")
async def delete_chat_session(session_id: str):
    """Delete a chat session"""
    if session_id not in chat_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    del chat_sessions[session_id]
    logger.info(f"Chat session {session_id} deleted")
    
    return {
        "success": True,
        "message": f"Chat session {session_id} deleted successfully"
    }
