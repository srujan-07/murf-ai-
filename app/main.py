from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from dotenv import load_dotenv

# Import routers
from app.routers import health, tts, stt, llm, agent, websocket

# Import utilities
from app.utils.logging import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()

# Create FastAPI instance
app = FastAPI(
    title="Voice Agents - Refactored",
    description="Refactored Voice Agents Backend with TTS, STT, LLM Integration, and Voice-to-Voice AI Pipeline",
    version="2.0.0"
)

# Create uploads directory if it doesn't exist
UPLOADS_DIR = Path("uploads")
UPLOADS_DIR.mkdir(exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(health.router)
app.include_router(tts.router)
app.include_router(stt.router)
app.include_router(llm.router)
app.include_router(agent.router)
app.include_router(websocket.router)

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Voice Agents API",
        "version": "2.0.0",
        "description": "Refactored Voice Agents Backend",
        "endpoints": {
            "health": "/api/health",
            "tts": "/api/tts",
            "stt": "/api/stt", 
            "llm": "/api/llm",
            "agent": "/api/agent",
            "websocket": "/ws"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
