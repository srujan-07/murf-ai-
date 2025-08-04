# 30 Days of Voice Agents

Welcome to the 30 Days of Voice Agents challenge! This project will build a comprehensive voice-powere## What's Next?

Day 4 will add:
- Speech recognition (Speech-to-Text)
- Voice command processing
- Interactive voice conversations
- Advanced audio controls

## Technologies Used

- **Backend**: FastAPI, Uvicorn, Murf Python SDK
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), HTML5 Audio API
- **TTS Integration**: Murf AI cloud service
- **Data Validation**: Pydantic models
- **Audio Playback**: Native HTML5 audio elements

---

*Day 3 of 30 - TTS Audio Playback Complete! 🎤🔊🎵* 30 days.

## Day 1: Project Setup ✅

### What we built:
- **FastAPI Backend**: Modern Python web framework with automatic API documentation
- **Frontend**: HTML page with JavaScript for interacting with the backend
- **Project Structure**: Organized file structure for scalability

## Day 2: REST TTS Integration ✅

### What we built:
- **TTS API Endpoint**: `/api/tts/generate` - Accepts text and generates audio URLs
- **Voice Management**: `/api/tts/voices` - Lists available TTS voices
- **Murf API Integration**: Real integration with Murf's Python SDK
- **Input Validation**: Text length limits and error handling
- **Response Models**: Structured JSON responses with audio URLs

## Day 3: Playing Back TTS Audio ✅

### What we built today:
- **Text Input Interface**: Clean text field for user input with placeholder text
- **Submit Button**: "Generate & Play Audio" button to trigger TTS generation
- **HTML Audio Element**: Native `<audio>` controls for playback with auto-play attempt
- **Audio URL Display**: Shows the generated Murf audio URL for direct access
- **Voice Selection**: Dropdown to choose from available Murf voices
- **Real-time Feedback**: Loading states, success messages, and error handling

### Key Features:
- ✅ **Text Field**: Large textarea with placeholder and character validation
- ✅ **Submit Button**: Generates audio and automatically plays it
- ✅ **HTML Audio Player**: Native browser controls with volume, seek, download
- ✅ **URL Display**: Shows actual Murf S3 audio URLs for sharing/downloading
- ✅ **Voice Selection**: Real Murf voices (Natalie, Davis, Jane, Mike, Emma)
- ✅ **Keyboard Shortcuts**: Press Enter to generate (Ctrl+Enter for new line)
- ✅ **Auto-play**: Attempts to play audio immediately after generation
- ✅ **Error Handling**: User-friendly error messages and validation
- ✅ **Responsive Design**: Works on desktop and mobile devices

### User Experience Flow:
1. **Enter Text** → User types in the textarea
2. **Select Voice** → Choose from dropdown (default: Natalie)
3. **Click Generate** → Button calls `/api/tts/generate` endpoint
4. **API Processing** → Murf SDK generates real audio file
5. **Audio Playback** → HTML `<audio>` element plays the generated speech
6. **URL Available** → Direct link to Murf S3 audio file displayed

### New API Endpoints:
- `POST /api/tts/generate` - Generate TTS audio from text
- `GET /api/tts/voices` - Get available voices

### Features Added in Day 2:
- ✅ Text-to-Speech API endpoint with real Murf SDK integration
- ✅ Configurable voice selection (Natalie, Davis, Jane, Mike, Emma)
- ✅ Speed and pitch control parameters (ready for future use)
- ✅ Comprehensive input validation and error handling
- ✅ Real audio generation with Murf's cloud service
- ✅ Production-ready code with proper error responses

### Features Added in Day 3:
- ✅ Clean web interface with text input and submit button
- ✅ HTML5 audio element for immediate playback
- ✅ Auto-play functionality (browser permitting)
- ✅ Real-time status updates and loading indicators
- ✅ Voice selection dropdown with real Murf voices
- ✅ URL display for direct audio file access
- ✅ Keyboard shortcuts and accessibility features
- ✅ Mobile-responsive design

## Project Structure:
```
murf/
├── main.py              # FastAPI backend server with TTS endpoints
├── requirements.txt     # Python dependencies (murf SDK, FastAPI, uvicorn)
├── .env.example         # Environment configuration template
├── static/             # Frontend assets
│   ├── index.html      # Day 3: Enhanced UI with audio playback
│   └── app.js          # Day 3: TTS functionality and audio controls
├── test_day3.py        # Day 3: Complete testing suite
├── test_murf_sdk.py    # Day 2: SDK integration tests
├── test_tts.py         # Day 2: Legacy test file
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

### 4. Test the Application
**Day 3 Interface**: http://localhost:8000
- Enter text in the input field
- Select a voice from the dropdown
- Click "Generate & Play Audio"
- Listen to the generated speech!

**API Documentation**: http://localhost:8000/docs
- **Try the TTS endpoint**: POST to `/api/tts/generate` with JSON:
```json
{
  "text": "Hello! This is Day 3 of the Voice Agents challenge!",
  "voice_id": "en-US-natalie"
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
