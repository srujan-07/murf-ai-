#!/usr/bin/env python3
"""
Voice Agents Backend - Main Entry Point
Refactored version with clean architecture
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
