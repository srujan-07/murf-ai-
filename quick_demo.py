#!/usr/bin/env python3
"""
Quick Voice Recording Demo
Simple demonstration of the recording process
"""

import time
import webbrowser
import requests

def quick_demo():
    """Quick demo of voice recording"""
    print("🎤 VOICE RECORDING QUICK DEMO")
    print("=" * 30)
    
    # Check server
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code != 200:
            print("❌ Server not running! Start with:")
            print("   uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
            return
    except:
        print("❌ Server not running! Start with:")
        print("   uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
        return
    
    print("✅ Server is running!")
    print("\n🚀 Opening browser...")
    webbrowser.open("http://localhost:8000")
    
    print("\n📋 FOLLOW THESE STEPS:")
    print("─" * 25)
    
    steps = [
        "1️⃣  Allow microphone access when prompted",
        "2️⃣  Click the 'Start Talking' button", 
        "3️⃣  Say: 'Hello, can you tell me a joke?'",
        "4️⃣  Click 'Stop & Send' button",
        "5️⃣  Wait for AI response (5-10 seconds)",
        "6️⃣  Listen to the voice response!"
    ]
    
    for step in steps:
        print(f"   {step}")
        time.sleep(1)
    
    print("\n🎯 WHAT HAPPENS:")
    print("   Your voice → Text → AI thinking → Voice response")
    
    print("\n🔧 TROUBLESHOOTING:")
    print("   • No mic access? Check browser address bar")
    print("   • Recording failed? Refresh page and retry")
    print("   • No response? Check terminal for errors")
    
    print("\n✨ Try these voice commands:")
    print("   • 'Tell me about yourself'")
    print("   • 'What's the weather like?'") 
    print("   • 'Write a short poem'")
    print("   • 'How does AI work?'")

if __name__ == "__main__":
    quick_demo()
