from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

# Create FastAPI instance
app = FastAPI(title="Voice Agents - Day 1", description="30 Days of Voice Agents Backend")

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
        "day": 1,
        "task": "Project Setup",
        "agents": []
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
