# 30 Days of Voice Agents

Welcome to the 30 Days of Voice Agents challenge! This project will build a comprehensive voice-powered application over 30 days.

## Day 1: Project Setup ✅

### What we built today:
- **FastAPI Backend**: Modern Python web framework with automatic API documentation
- **Frontend**: HTML page with JavaScript for interacting with the backend
- **Project Structure**: Organized file structure for scalability

### Project Structure:
```
murf/
├── main.py              # FastAPI backend server
├── requirements.txt     # Python dependencies
├── static/             # Frontend assets
│   ├── index.html      # Main HTML page
│   └── app.js          # JavaScript frontend logic
└── README.md           # This file
```

### Features:
- ✅ FastAPI backend with automatic API documentation
- ✅ Static file serving for frontend assets
- ✅ Health check endpoint
- ✅ Sample voice agents API endpoint
- ✅ Responsive web interface
- ✅ Browser voice capability detection
- ✅ Error handling and status indicators

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python main.py
```

### 3. Access the Application
- **Main App**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## API Endpoints

- `GET /` - Serves the main HTML page
- `GET /api/health` - Health check endpoint
- `GET /api/voice-agents` - Sample voice agents endpoint

## What's Next?

Tomorrow we'll start building the core voice functionality:
- Speech recognition setup
- Text-to-speech integration
- Basic voice commands

## Technologies Used

- **Backend**: FastAPI, Uvicorn
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Voice APIs**: Web Speech API (coming in future days)

---

*Day 1 of 30 - Project Setup Complete! 🎉*
