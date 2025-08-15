from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import TranscriptionResponse, AudioUploadResponse
from app.services.stt_service import STTService
from app.utils.file_utils import FileUtils
from app.utils.logging import get_logger

logger = get_logger(__name__)
router = APIRouter(prefix="/api/stt", tags=["stt"])

# Initialize services
stt_service = STTService()
file_utils = FileUtils()

@router.post("/transcribe-file", response_model=TranscriptionResponse)
async def transcribe_audio_file(file: UploadFile = File(...)):
    """Transcribe uploaded audio file"""
    logger.info(f"Audio transcription request: {file.filename}")
    
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Read file content
        file_content = await file.read()
        
        # Transcribe using STT service
        response = await stt_service.transcribe_uploaded_file(file_content, file.filename)
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"STT endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe-path", response_model=TranscriptionResponse)
async def transcribe_audio_path(file_path: str):
    """Transcribe audio file from path"""
    logger.info(f"Audio transcription from path: {file_path}")
    
    try:
        response = await stt_service.transcribe_audio(file_path)
        return response
        
    except Exception as e:
        logger.error(f"STT path endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload", response_model=AudioUploadResponse)
async def upload_audio_file(file: UploadFile = File(...)):
    """Upload audio file for later transcription"""
    logger.info(f"Audio upload request: {file.filename}")
    
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('audio/'):
            raise HTTPException(status_code=400, detail="File must be an audio file")
        
        # Save file
        success, filename, filepath = await file_utils.save_uploaded_file(file)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save uploaded file")
        
        # Get file info
        file_info = file_utils.get_file_info(filepath)
        
        response = AudioUploadResponse(
            success=True,
            message="Audio file uploaded successfully",
            filename=filename,
            content_type=file.content_type,
            size_bytes=file_info.get("size_bytes", 0),
            upload_path=filepath
        )
        
        logger.info(f"Audio upload successful: {filename}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Upload endpoint error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
