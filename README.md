# Voice Agents Backend - Refactored

A clean, maintainable FastAPI backend for voice agents with TTS, STT, LLM integration, and voice-to-voice AI pipeline.

## 🚀 Features

- **Text-to-Speech (TTS)**: Convert text to natural-sounding speech using Murf API
- **Speech-to-Text (STT)**: Transcribe audio files using AssemblyAI
- **Language Model Integration**: Generate responses using Google Gemini
- **Voice-to-Voice AI**: Complete conversational bot with audio input/output
- **Chat Sessions**: Maintain conversation history and context
- **Health Monitoring**: Comprehensive API health checks
- **Clean Architecture**: Well-organized, maintainable code structure

## 🏗️ Architecture

The application follows a clean, modular architecture:

```
app/
├── models/          # Pydantic schemas for request/response validation
├── services/        # Business logic for TTS, STT, and LLM operations
├── routers/         # API endpoint handlers organized by feature
├── utils/           # Utility functions for logging and file operations
└── main.py         # Application entry point and configuration
```

### Key Components

- **Models**: Pydantic schemas ensure type safety and validation
- **Services**: Encapsulate business logic and external API interactions
- **Routers**: Handle HTTP requests and responses with proper error handling
- **Utils**: Provide logging, file management, and other utilities

## 🛠️ Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd voice-agents-backend
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## 🔑 Environment Variables

Create a `.env` file with the following variables:

```env
MURF_API_KEY=your_murf_api_key_here
ASSEMBLY_AI_API_KEY=your_assemblyai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🚀 Running the Application

### Development Mode
```bash
python main.py
```

### Production Mode
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Health Checks
- `GET /api/health` - Simple health check
- `GET /api/health/detailed` - Detailed service status

### Text-to-Speech
- `POST /api/tts/generate` - Convert text to speech
- `GET /api/tts/voices` - Get available voices

### Speech-to-Text
- `POST /api/stt/transcribe-file` - Transcribe uploaded audio
- `POST /api/stt/transcribe-path` - Transcribe audio from file path
- `POST /api/stt/upload` - Upload audio file

### Language Models
- `POST /api/llm/generate` - Generate LLM response
- `POST /api/llm/query` - Query LLM with parameters
- `GET /api/llm/models` - Get available models

### Voice Agent
- `POST /api/agent/chat` - Chat with voice agent
- `POST /api/agent/echo` - Echo bot functionality
- `POST /api/agent/audio-query` - Audio query through LLM
- `GET /api/agent/sessions` - List chat sessions
- `GET /api/agent/sessions/{id}` - Get session details
- `DELETE /api/agent/sessions/{id}` - Delete session

## 🎯 Usage Examples

### Basic TTS
```bash
curl -X POST "http://localhost:8000/api/tts/generate" \
     -H "Content-Type: application/json" \
     -d '{"text": "Hello, world!", "voice_id": "en-US-natalie"}'
```

### Audio Transcription
```bash
curl -X POST "http://localhost:8000/api/stt/transcribe-file" \
     -F "file=@audio.wav"
```

### Chat with Agent
```bash
curl -X POST "http://localhost:8000/api/agent/chat" \
     -F "audio_file=@user_audio.wav"
```

## 🔧 Development

### Code Structure
- **Models**: Define request/response schemas using Pydantic
- **Services**: Implement business logic and external API calls
- **Routers**: Handle HTTP endpoints with proper error handling
- **Utils**: Provide logging, file operations, and other utilities

### Adding New Features
1. Create schemas in `app/models/schemas.py`
2. Implement business logic in `app/services/`
3. Add endpoints in `app/routers/`
4. Update the main application in `app/main.py`

### Logging
The application uses structured logging throughout:
- Request/response logging
- Error tracking
- Performance monitoring
- Service health status

## 🧪 Testing

Run tests to ensure everything works correctly:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest
```

## 📦 Dependencies

- **FastAPI**: Modern, fast web framework
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server for running FastAPI
- **Murf**: Text-to-speech API
- **AssemblyAI**: Speech-to-text API
- **Google Generative AI**: Language model integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built as part of the "30 Days of Voice Agents" challenge
- Inspired by modern AI voice assistant technologies
- Uses industry-standard APIs for TTS, STT, and LLM capabilities

## 📞 Support

For questions or issues:
- Create an issue in the repository
- Check the API documentation at `/docs` when running the server
- Review the health check endpoints for service status
