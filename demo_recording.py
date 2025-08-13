#!/usr/bin/env python3
"""
Voice Recording Demo Script
Demonstrates how to use the voice AI chat agent recording functionality
"""

import webbrowser
import time
import requests
import json
from pathlib import Path

def check_server_status():
    """Check if the server is running"""
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            print("✅ Server is running and ready!")
            return True
        else:
            print(f"❌ Server responded with status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Server is not running. Please start it first.")
        return False

def demonstrate_recording_process():
    """Demonstrate the voice recording process"""
    print("\n🎤 Voice Recording Demo - Step by Step Guide")
    print("=" * 50)
    
    print("\n📋 Recording Process Overview:")
    print("1. Open the web interface")
    print("2. Grant microphone permissions")
    print("3. Start recording your voice")
    print("4. Stop recording and send")
    print("5. Listen to AI response")
    
    print("\n🔧 Technical Flow:")
    print("Voice Input → WebM Recording → Upload → AssemblyAI STT → Gemini LLM → Murf TTS → Audio Response")
    
    return True

def show_recording_instructions():
    """Show detailed recording instructions"""
    print("\n📝 Detailed Recording Instructions:")
    print("=" * 40)
    
    instructions = [
        "🌐 1. OPEN WEB INTERFACE",
        "   • Navigate to: http://localhost:8000",
        "   • The voice chat interface will load",
        "",
        "🎙️ 2. GRANT MICROPHONE PERMISSION",
        "   • Browser will request microphone access",
        "   • Click 'Allow' when prompted",
        "   • Check for microphone icon in browser address bar",
        "",
        "🔴 3. START RECORDING",
        "   • Click the 'Start Talking' button",
        "   • Button will turn red and show 'Recording...'",
        "   • Status will show: 'Recording... Speak now!'",
        "",
        "🗣️ 4. SPEAK YOUR MESSAGE",
        "   • Speak clearly into your microphone",
        "   • Try messages like:",
        "     - 'Hello, how are you today?'",
        "     - 'Tell me a joke about programming'",
        "     - 'What's the weather like?'",
        "",
        "⏹️ 5. STOP RECORDING",
        "   • Click 'Stop & Send' button",
        "   • Status will show: 'Processing your message...'",
        "   • Audio is automatically uploaded and processed",
        "",
        "🤖 6. AI PROCESSING",
        "   • Your speech is transcribed (AssemblyAI)",
        "   • AI generates response (Google Gemini)",
        "   • Response is converted to speech (Murf TTS)",
        "",
        "🔊 7. LISTEN TO RESPONSE",
        "   • AI response plays automatically",
        "   • Text transcript appears in chat",
        "   • Conversation history is maintained"
    ]
    
    for instruction in instructions:
        print(instruction)
    
def show_troubleshooting_tips():
    """Show common troubleshooting tips for recording"""
    print("\n🔧 Recording Troubleshooting Tips:")
    print("=" * 35)
    
    tips = [
        "🎤 MICROPHONE ISSUES:",
        "   • Check browser permissions (click lock icon in address bar)",
        "   • Ensure microphone is not muted in system settings",
        "   • Try refreshing the page if microphone access was denied",
        "   • Check Windows Privacy Settings → Microphone",
        "",
        "🌐 BROWSER COMPATIBILITY:",
        "   • Chrome/Edge: Full support for MediaRecorder API",
        "   • Firefox: Good support",
        "   • Safari: Limited support (try Chrome/Edge instead)",
        "",
        "🔊 AUDIO QUALITY:",
        "   • Speak clearly and at normal volume",
        "   • Avoid background noise",
        "   • Keep microphone 6-12 inches from mouth",
        "   • Test with headset microphone for best quality",
        "",
        "⚠️ COMMON ERROR FIXES:",
        "   • 'Microphone not available' → Check browser permissions",
        "   • 'Recording failed' → Refresh page and try again",
        "   • 'No audio detected' → Check microphone levels in Windows",
        "   • 'Processing timeout' → Check internet connection"
    ]
    
    for tip in tips:
        print(tip)

def create_test_scenarios():
    """Create test scenarios for recording demo"""
    print("\n🧪 Test Recording Scenarios:")
    print("=" * 30)
    
    scenarios = [
        {
            "name": "Basic Greeting",
            "message": "Hello there! How are you doing today?",
            "purpose": "Test basic conversation functionality"
        },
        {
            "name": "Question Asking",
            "message": "Can you tell me about artificial intelligence?",
            "purpose": "Test AI knowledge and longer responses"
        },
        {
            "name": "Creative Request", 
            "message": "Write me a short poem about coding",
            "purpose": "Test creative AI capabilities"
        },
        {
            "name": "Technical Query",
            "message": "How does machine learning work?",
            "purpose": "Test technical knowledge responses"
        },
        {
            "name": "Casual Chat",
            "message": "What's your favorite programming language and why?",
            "purpose": "Test conversational AI personality"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"📝 Scenario {i}: {scenario['name']}")
        print(f"   Say: \"{scenario['message']}\"")
        print(f"   Purpose: {scenario['purpose']}")
        print()

def open_browser_demo():
    """Open browser and demonstrate recording"""
    print("\n🌐 Opening Browser Demo...")
    
    if check_server_status():
        print("🚀 Opening web interface in your browser...")
        webbrowser.open("http://localhost:8000")
        print("\n✨ Browser opened! Follow the on-screen recording instructions.")
        
        print("\n⏰ Demo Timeline:")
        print("1. Grant microphone permission when prompted")
        print("2. Click 'Start Talking' button")
        print("3. Say: 'Hello, this is a test of the voice recording system'")
        print("4. Click 'Stop & Send'")
        print("5. Wait for AI response")
        print("6. Listen to the generated speech response")
        
        return True
    else:
        print("\n❌ Cannot start demo - server is not running")
        print("Please run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return False

def show_recording_api_demo():
    """Show how recording works with the API"""
    print("\n🔌 Recording API Flow Demo:")
    print("=" * 30)
    
    print("📊 Backend API Endpoints Used:")
    print("1. POST /api/agent/chat/{session_id} - Main voice chat endpoint")
    print("2. POST /api/transcribe/file - Speech-to-text conversion")
    print("3. POST /api/llm/query - AI response generation")
    print("4. POST /api/tts/generate - Text-to-speech conversion")
    
    print("\n📱 Frontend JavaScript Flow:")
    print("1. navigator.mediaDevices.getUserMedia() - Get microphone access")
    print("2. MediaRecorder API - Record audio to WebM format")
    print("3. FormData upload - Send audio file to server")
    print("4. Fetch API - Handle server responses")
    print("5. HTML5 Audio - Play generated speech")

def main():
    """Main demo function"""
    print("🎤🤖 Voice AI Chat Agent - Recording Demo")
    print("=" * 45)
    
    print("This demo will show you how to:")
    print("• Record voice messages")
    print("• Troubleshoot recording issues")
    print("• Test different voice scenarios")
    print("• Understand the technical flow")
    
    # Check if server is running
    if not check_server_status():
        print("\n⚠️  Please start the server first:")
        print("   uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    # Show demo sections
    demonstrate_recording_process()
    show_recording_instructions()
    show_troubleshooting_tips()
    create_test_scenarios()
    show_recording_api_demo()
    
    # Ask user if they want to open browser demo
    print("\n" + "=" * 45)
    user_input = input("🌐 Would you like to open the browser demo now? (y/n): ").lower().strip()
    
    if user_input in ['y', 'yes']:
        open_browser_demo()
        
        print("\n🎯 Next Steps:")
        print("1. Try the test scenarios listed above")
        print("2. Test error handling by speaking very quietly")
        print("3. Try different voice questions and commands")
        print("4. Check the conversation history in the interface")
        
    else:
        print("\n📝 Manual Demo Steps:")
        print("1. Open: http://localhost:8000")
        print("2. Follow the recording instructions above")
        print("3. Try the test scenarios")
        
    print("\n✨ Happy voice chatting! 🎤🤖")

if __name__ == "__main__":
    main()
