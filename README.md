# 30 Days of Voice Agents

Welcome to the 30 Days of Voice Agents challenge! This project will build a comprehensive voice-powered application over 30 days.

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

### Features Added in Day 2:
- ✅ Text-to-Speech API endpoint with real Murf SDK integration
- ✅ Configurable voice selection (Natalie, Davis, Jane, Mike, Emma)
- ✅ Speed and pitch control parameters (ready for future use)
- ✅ Comprehensive input validation and error handling
- ✅ Real audio generation with Murf's cloud service
- ✅ Production-ready code with proper error responses

## Day 3: Playing Back TTS Audio ✅

### What we built:
- **Text Input Interface**: Clean text field for user input with placeholder text
- **Submit Button**: "Generate & Play Audio" button to trigger TTS generation
- **HTML Audio Element**: Native `<audio>` controls for playback with auto-play attempt
- **Audio URL Display**: Shows the generated Murf audio URL for direct access
- **Voice Selection**: Dropdown to choose from available Murf voices
- **Real-time Feedback**: Loading states, success messages, and error handling

### Features Added in Day 3:
- ✅ Clean web interface with text input and submit button
- ✅ HTML5 audio element for immediate playback
- ✅ Auto-play functionality (browser permitting)
- ✅ Real-time status updates and loading indicators
- ✅ Voice selection dropdown with real Murf voices
- ✅ URL display for direct audio file access
- ✅ Keyboard shortcuts and accessibility features
- ✅ Mobile-responsive design

## Day 4: Echo Bot with Voice Recording ✅

### What we built today:
- **Echo Bot Section**: New dedicated section for voice recording functionality
- **Voice Recording**: MediaRecorder API integration for browser-based recording
- **Recording Controls**: Start/Stop Recording buttons with proper state management
- **Instant Playback**: Recorded audio plays back immediately using HTML5 audio
- **Microphone Access**: Permission handling and user feedback for microphone access
- **Visual Feedback**: Real-time status updates during recording process

### Key Features:
- ✅ **Voice Recording**: Record audio directly from your microphone
- ✅ **Start/Stop Controls**: Clean button interface for recording management
- ✅ **Instant Echo**: Play back your recorded voice immediately
- ✅ **Microphone Permissions**: Handles browser permission requests gracefully
- ✅ **Recording Status**: Visual feedback showing recording state
- ✅ **Audio Storage**: Uses Blob API for temporary audio storage
- ✅ **Cross-browser Support**: Works with modern browsers supporting MediaRecorder
- ✅ **Error Handling**: User-friendly messages for microphone access issues

### User Experience Flow:
1. **Click Start Recording** → Browser requests microphone permission
2. **Grant Permission** → Recording begins, status shows "Recording... Speak now!"
3. **Speak into Microphone** → Voice is captured in real-time
4. **Click Stop Recording** → Recording ends, audio is processed
5. **Automatic Playback** → HTML audio player appears with your recorded voice
6. **Listen to Echo** → Play back your voice using standard audio controls

### Technical Implementation:
- **MediaRecorder API**: Modern browser API for audio recording
- **Blob Handling**: Efficient audio data management
- **State Management**: Proper button enable/disable during recording
- **Audio URL Creation**: Uses `URL.createObjectURL()` for playback
- **Error Handling**: Comprehensive permission and recording error management

## Project Structure:
```
murf/
├── main.py              # FastAPI backend server with TTS endpoints
├── requirements.txt     # Python dependencies (murf SDK, FastAPI, uvicorn)
├── .env.example         # Environment configuration template
├── static/             # Frontend assets
│   ├── index.html      # Day 4: TTS + Echo Bot complete interface
│   └── app.js          # Day 4: TTS + MediaRecorder functionality
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
**Day 4 Interface**: http://localhost:8000

**Text-to-Speech Section:**
- Enter text in the input field
- Select a voice from the dropdown
- Click "Generate & Play Audio"
- Listen to the generated speech!

**Echo Bot Section:**
- Click "Start Recording"
- Allow microphone access when prompted
- Speak into your microphone
- Click "Stop Recording"
- Listen to your voice played back instantly!

**API Documentation**: http://localhost:8000/docs

## API Endpoints

### General Endpoints:
- `GET /` - Serves the main HTML page
- `GET /api/health` - Health check endpoint
- `GET /api/voice-agents` - Voice agents status

### TTS Endpoints:
- `POST /api/tts/generate` - Generate audio from text
- `GET /api/tts/voices` - List available voices

### Example TTS Request:
```json
{
  "text": "Hello! This is Day 4 of the Voice Agents challenge!",
  "voice_id": "en-US-natalie"
}
```

## What's Next?

Day 5 will add:
- Speech-to-Text functionality
- Voice command recognition
- Interactive voice conversations
- Advanced audio processing

## Technologies Used

- **Backend**: FastAPI, Uvicorn, Murf Python SDK
- **Frontend**: HTML5, CSS3, JavaScript (ES6+), HTML5 Audio API, MediaRecorder API
- **TTS Integration**: Murf AI cloud service
- **Voice Recording**: Browser MediaRecorder API
- **Data Validation**: Pydantic models
- **Audio Playback**: Native HTML5 audio elements

---

*Day 4 of 30 - Echo Bot Complete! 🎤🔊🎵*

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

## Day 7: Echo Bot v2 - Complete Voice Pipeline ✅

### What we built:
- **Enhanced Echo Bot**: Complete voice-to-voice pipeline with transcription and TTS
- **AssemblyAI Integration**: High-quality speech-to-text transcription
- **Audio Processing Pipeline**: Record → Upload → Transcribe → Generate TTS → Playback
- **Improved UI**: Updated interface with "Echo Bot v2 with Murf TTS"
- **Error Handling**: Comprehensive error handling for the entire voice pipeline

### Features Added in Day 7:
- ✅ Real-time transcription with AssemblyAI
- ✅ Voice-to-voice echo functionality (your voice → text → AI voice)
- ✅ Enhanced Echo Bot interface with proper status messages
- ✅ Audio file management and cleanup
- ✅ Production-ready voice pipeline
- ✅ Configurable TTS voice selection for echo playback

## Day 8: LLM Integration with Google Gemini ✅

### What we built:
- **Google Gemini API Integration**: Added Google's Gemini 1.5 Flash and Pro models
- **LLM Query Endpoint**: `/api/llm/query` - Accepts text and returns AI responses
- **Frontend LLM Interface**: Clean chat-like interface for AI conversations
- **Model Selection**: Choose between Gemini 1.5 Flash (fast) and Pro (advanced)
- **Configuration Controls**: Temperature and token limit controls
- **Test Scripts**: Validation scripts for API functionality

### Features Added in Day 8:
- ✅ Google Gemini API integration with `google-generativeai` package
- ✅ RESTful LLM endpoint with proper error handling
- ✅ Frontend chat interface with textarea and controls
- ✅ Model selection (gemini-1.5-flash, gemini-1.5-pro)
- ✅ Temperature and max tokens configuration
- ✅ Real-time response streaming and display
- ✅ Comprehensive test suite for LLM functionality
- ✅ Error handling for API limits and content filtering

---

## API Endpoints

### General Endpoints:
- `GET /` - Serves the main HTML page
- `GET /api/health` - Health check endpoint  
- `GET /api/voice-agents` - Voice agents status

### TTS Endpoints:
- `POST /api/tts/generate` - Generate audio from text
- `GET /api/tts/voices` - List available voices
- `POST /api/tts/echo` - Echo Bot v2 with transcription and TTS

### Transcription Endpoints:
- `POST /api/transcribe/file` - Transcribe uploaded audio file

### LLM Endpoints (NEW):
- `POST /api/llm/query` - Query Google Gemini with text input

## What's Next?

Day 9 will add:
- Multi-modal capabilities (image + text)
- Voice-to-LLM pipeline
- Enhanced conversation memory
- Advanced prompt engineering

## Technologies Used

- **Backend**: FastAPI, Uvicorn, Python 3.13+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **TTS Integration**: Murf API (Official Python SDK)
- **Transcription**: AssemblyAI Python SDK
- **LLM Integration**: Google Gemini API (google-generativeai)
- **Data Validation**: Pydantic models
- **Environment Management**: python-dotenv

---

*Day 8 of 30 - LLM Integration Complete! 🤖🧠*
