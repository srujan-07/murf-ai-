# 🎤🤖 Voice AI Chat Agent

A robust, conversational AI agent with voice input/output, chat history, and comprehensive error handling. Built with FastAPI, AssemblyAI, Google Gemini, and Murf TTS.

## 🌟 Features

### 🎯 Core Capabilities
- **Voice-to-Voice AI**: Speak to the AI and hear responses back
- **Chat History & Memory**: Persistent conversation context across sessions
- **Multi-Modal Input**: Voice, text, and file uploads
- **Real-time Transcription**: High-accuracy speech-to-text
- **Natural Voice Output**: High-quality AI-generated speech
- **Session Management**: URL-based conversation tracking

### 🛡️ Robustness & Error Handling
- **Graceful Degradation**: System continues functioning with partial service failures
- **Smart Fallbacks**: Context-aware error responses for each service type
- **Alternative Audio**: Browser speech synthesis when cloud TTS fails
- **Visual Error Indicators**: Clear user feedback with error categorization
- **Service Health Monitoring**: Real-time API status checking

### 🎨 User Experience
- **Intuitive Interface**: Clean, responsive web UI
- **Auto-Continue Conversations**: Seamless chat flow
- **Voice Selection**: Multiple AI voices to choose from
- **Model Selection**: Choose between different AI models
- **Real-time Status**: Live feedback during processing

## 🏗️ Architecture

```
Voice Input → AssemblyAI STT → Google Gemini LLM → Murf TTS → Audio Output
     ↓              ↓                ↓               ↓            ↓
  WebM Audio → Text Transcript → AI Response → Audio URL → Browser Playback
```

### 🔧 Technology Stack

**Backend:**
- **FastAPI**: Modern, fast Python web framework
- **AssemblyAI**: Speech-to-text transcription
- **Google Gemini**: Large language model for AI responses
- **Murf TTS**: High-quality text-to-speech synthesis
- **Python 3.13**: Latest Python with type hints

**Frontend:**
- **Vanilla JavaScript**: No framework dependencies
- **MediaRecorder API**: Browser-native audio recording
- **SpeechSynthesis API**: Fallback text-to-speech
- **HTML5**: Modern web standards

**APIs & Services:**
- **AssemblyAI API**: Real-time speech recognition
- **Google Gemini API**: Advanced language understanding
- **Murf API**: Professional voice synthesis

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- API Keys for:
  - [AssemblyAI](https://www.assemblyai.com/)
  - [Google Gemini](https://makersuite.google.com/app/apikey)
  - [Murf](https://murf.ai/api)

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/srujan-07/murf-ai-.git
cd murf-ai-
```

2. **Create virtual environment:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

Example `.env` file:
```properties
# Murf API Configuration
MURF_API_KEY=your_murf_api_key_here

# AssemblyAI API Configuration
ASSEMBLY_AI_API_KEY=your_assemblyai_api_key_here

# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

5. **Start the server:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

6. **Open your browser:**
Visit `http://localhost:8000` to start using the voice AI chat agent!

## 📖 Usage Guide

### 🎙️ Basic Voice Chat
1. Click "Start Talking" to begin recording
2. Speak your question or message
3. Click "Stop & Send" to process
4. Listen to the AI's voice response
5. Continue the conversation with context preserved

### 💬 Session Management
- **Auto Session ID**: Generated automatically and stored in URL
- **Custom Session ID**: Enter your own session identifier
- **Session History**: View past conversation messages
- **Clear History**: Reset conversation context

### ⚙️ Configuration Options
- **Voice Selection**: Choose from multiple AI voices
- **Model Selection**: Pick AI model (Flash for speed, Pro for quality)
- **Auto-continue**: Automatically prepare for next message after response
- **Temperature**: Control AI response creativity (0.0-1.0)

## 🔌 API Endpoints

### Chat & Voice
- `POST /api/agent/chat/{session_id}` - Voice chat with session memory
- `POST /api/llm/query/audio` - Voice-to-voice AI (stateless)
- `POST /api/llm/query` - Text-based LLM queries

### Core Services
- `POST /api/tts/generate` - Text-to-speech generation
- `POST /api/transcribe/file` - Audio file transcription
- `POST /api/tts/echo` - Echo bot with voice

### Utilities
- `GET /api/health` - Basic health check
- `GET /api/health/detailed` - Detailed service status
- `GET /api/agent/chat/{session_id}/history` - Chat history
- `POST /api/audio/upload` - Audio file upload

## 🧪 Testing & Development

### Test Scripts
```bash
# Test chat functionality
python test_chat_agent.py

# Test error handling scenarios
python test_error_handling.py

# Error handling documentation
python test_error_demo.py

# TTS-specific error testing
python test_tts_error.py
```

### Error Simulation
The system includes tools to simulate API failures for testing:

```bash
# Simulate different failure scenarios
python test_error_handling.py
# Choose: STT failure, LLM failure, TTS failure, or complete failure
```

### Health Monitoring
```bash
# Check service status
curl http://localhost:8000/api/health/detailed
```

## 🛡️ Error Handling

### Graceful Degradation
- **STT Failure**: "Sorry, I couldn't understand due to technical issue"
- **LLM Failure**: "Having trouble processing your request right now"
- **TTS Failure**: Text response + browser speech synthesis backup
- **Network Issues**: Clear user guidance with retry suggestions

### Visual Indicators
- **Green**: Successful operations
- **Yellow**: Warnings or degraded service
- **Red**: Errors with clear explanations
- **Blue**: Processing states

### Fallback Mechanisms
1. **Browser TTS**: When cloud TTS fails
2. **Predefined Responses**: When LLM is unavailable
3. **Error Messages**: When STT fails
4. **Conversation Continuity**: Context preserved across failures

## 📁 Project Structure

```
murf-ai-/
├── main.py                 # FastAPI application
├── requirements.txt        # Python dependencies
├── .env.example           # Environment template
├── README.md              # This file
├── static/
│   ├── index.html         # Web interface
│   └── app.js            # Frontend JavaScript
├── uploads/               # Temporary audio files
├── __pycache__/          # Python cache
└── tests/
    ├── test_chat_agent.py     # Chat functionality tests
    ├── test_error_handling.py # Error simulation tools
    ├── test_error_demo.py     # Error documentation
    └── test_tts_error.py      # TTS error testing
```

## 🎯 Development Journey

This project was built incrementally over 11 days:

- **Day 1-3**: Basic TTS with Murf API
- **Day 4-5**: Audio upload and file handling
- **Day 6**: Speech-to-text transcription
- **Day 7**: Echo bot functionality
- **Day 8**: LLM integration with Gemini
- **Day 9**: Voice-to-voice AI pipeline
- **Day 10**: Chat history and session management
- **Day 11**: Comprehensive error handling and robustness

## 🔐 Security & Privacy

- **API Keys**: Stored securely in environment variables
- **File Cleanup**: Uploaded audio files automatically deleted
- **Session Isolation**: Chat histories separated by session ID
- **Input Validation**: All inputs sanitized and validated
- **Error Handling**: No sensitive information exposed in errors

## 🚀 Deployment

### Local Development
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Variables
Ensure all required API keys are set in production:
- `MURF_API_KEY`
- `ASSEMBLY_AI_API_KEY`
- `GEMINI_API_KEY`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AssemblyAI** for excellent speech recognition
- **Google Gemini** for powerful language understanding
- **Murf** for high-quality voice synthesis
- **FastAPI** for the excellent web framework

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/srujan-07/murf-ai-/issues) page
2. Review the error handling documentation in `test_error_demo.py`
3. Run the health check: `curl http://localhost:8000/api/health/detailed`

## 🎯 Future Enhancements

- **Database Integration**: Persistent chat history storage
- **User Authentication**: Multi-user support
- **Voice Cloning**: Custom voice training
- **Real-time Streaming**: Live audio processing
- **Mobile App**: Native iOS/Android applications
- **Multi-language Support**: International voice agents

---

Built with ❤️ by [Srujan](https://github.com/srujan-07)

**Start building the future of voice AI today!** 🚀🎤🤖
