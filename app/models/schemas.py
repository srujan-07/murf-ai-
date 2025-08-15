from pydantic import BaseModel
from typing import Optional, List

# TTS Models
class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = "en-US-natalie"
    speed: Optional[int] = 0
    pitch: Optional[int] = 0
    
class TTSResponse(BaseModel):
    success: bool
    message: str
    audio_url: Optional[str] = None
    audio_id: Optional[str] = None

# Audio Upload Models
class AudioUploadResponse(BaseModel):
    success: bool
    message: str
    filename: str
    content_type: str
    size_bytes: int
    upload_path: str

# Transcription Models
class TranscriptionResponse(BaseModel):
    success: bool
    message: str
    transcript: Optional[str] = None
    confidence: Optional[float] = None
    audio_duration: Optional[float] = None

# Echo Bot Models
class EchoBotResponse(BaseModel):
    success: bool
    message: str
    transcript: Optional[str] = None
    audio_url: Optional[str] = None
    voice_used: Optional[str] = None
    confidence: Optional[float] = None

# LLM Models
class LLMRequest(BaseModel):
    text: str
    model: Optional[str] = "gemini-2.0-flash-exp"

class LLMResponse(BaseModel):
    success: bool
    message: str
    response_text: Optional[str] = None
    model_used: Optional[str] = None

class LLMQueryRequest(BaseModel):
    text: str
    model: Optional[str] = "gemini-1.5-flash"
    max_tokens: Optional[int] = 1000
    temperature: Optional[float] = 0.7

class LLMQueryResponse(BaseModel):
    success: bool
    message: str
    query: str
    response: Optional[str] = None
    model_used: Optional[str] = None
    tokens_used: Optional[int] = None

# Audio LLM Query Models
class AudioLLMQueryResponse(BaseModel):
    success: bool
    message: str
    transcribed_text: Optional[str] = None
    llm_response: Optional[str] = None
    audio_url: Optional[str] = None
    model_used: Optional[str] = None
    voice_used: Optional[str] = None
    processing_time: Optional[float] = None

# Chat Models
class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: float

class ChatSession(BaseModel):
    session_id: str
    messages: List[ChatMessage]
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

# Health Check Models
class HealthResponse(BaseModel):
    status: str
    message: str

class DetailedHealthResponse(BaseModel):
    overall_status: str
    timestamp: float
    services: dict
