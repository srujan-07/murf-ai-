# 30 Days of Voice Agents

Welcome to the 30 Days of Voice Agents challenge! This project will build a comprehensive voice-powered application over 30 days.

## Day 1: Project Setup ✅

### What we built:
- **FastAPI Backend**: Modern Python web framework with automatic API documentation
- **Frontend**: HTML page with JavaScript for interacting with the backend
- **Project Structure**: Organized file structure for scalability

## Day 2: REST TTS Integration ✅

### What we built today:
- **TTS API Endpoint**: `/api/tts/generate` - Accepts text and generates audio URLs
- **Voice Management**: `/api/tts/voices` - Lists available TTS voices
- **Murf API Integration**: Ready-to-use structure for Murf's REST TTS API
- **Input Validation**: Text length limits and error handling
- **Response Models**: Structured JSON responses with audio URLs

### New API Endpoints:
- `POST /api/tts/generate` - Generate TTS audio from text
- `GET /api/tts/voices` - Get available voices

### Features Added:
- ✅ Text-to-Speech API endpoint with Murf integration structure
- ✅ Configurable voice selection (Davis, Jane, Mike, Emma, Carlos)
- ✅ Speed and pitch control parameters
- ✅ Comprehensive input validation and error handling
- ✅ Demo mode with simulated responses for testing
- ✅ Production-ready code structure (commented for actual API integration)

## Project Structure:
```
murf/
├── main.py              # FastAPI backend server with TTS endpoints
├── requirements.txt     # Python dependencies (updated with httpx)
├── .env.example         # Environment configuration template
├── static/             # Frontend assets
│   ├── index.html      # Main HTML page
│   └── app.js          # JavaScript frontend logic
└── README.md           # This file
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Murf API (Optional)
```bash
cp .env.example .env
# Edit .env and add your Murf API key
```

### 3. Run the Server
```bash
python main.py
```

### 4. Test the TTS API
- **Interactive API Docs**: http://localhost:8000/docs
- **Try the TTS endpoint**: POST to `/api/tts/generate` with JSON:
```json
{
  "text": "Hello! This is a test of the text-to-speech functionality.",
  "voice_id": "en-US-davis",
  "speed": 0,
  "pitch": 0
}
```

## API Endpoints

### General Endpoints:
- `GET /` - Serves the main HTML page
- `GET /api/health` - Health check endpoint
- `GET /api/voice-agents` - Voice agents status

### TTS Endpoints (NEW):
- `POST /api/tts/generate` - Generate audio from text
- `GET /api/tts/voices` - List available voices

## What's Next?

Day 3 will add:
- Frontend TTS integration
- Audio player functionality
- Voice selection UI
- Real-time audio generation

## Technologies Used

- **Backend**: FastAPI, Uvicorn, HTTPx
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **TTS Integration**: Murf API (REST)
- **Data Validation**: Pydantic models

---

*Day 2 of 30 - TTS API Integration Complete! �🔊*
