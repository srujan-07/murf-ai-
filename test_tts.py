#!/usr/bin/env python3
"""
Test script for Day 2 TTS API endpoint
This demonstrates how to call the /api/tts/generate endpoint
"""

import asyncio
import httpx
import json

async def test_tts_endpoint():
    """Test the TTS generation endpoint"""
    
    base_url = "http://localhost:8000"
    
    # Test data
    test_requests = [
        {
            "text": "Hello! This is a test of our new text-to-speech API integration for Day 2 of the 30 Days of Voice Agents challenge.",
            "voice_id": "en-US-davis",
            "speed": 0,
            "pitch": 0
        },
        {
            "text": "Welcome to the future of voice technology!",
            "voice_id": "en-US-jane",
            "speed": 1,
            "pitch": 0
        },
        {
            "text": "¡Hola! Este es un mensaje en español.",
            "voice_id": "es-ES-carlos",
            "speed": 0,
            "pitch": -1
        }
    ]
    
    async with httpx.AsyncClient() as client:
        print("🎤 Testing TTS API Endpoints")
        print("=" * 50)
        
        # Test 1: Get available voices
        print("\n1. Testing GET /api/tts/voices")
        try:
            response = await client.get(f"{base_url}/api/tts/voices")
            if response.status_code == 200:
                voices_data = response.json()
                print(f"✅ Success! Found {voices_data['total_count']} voices")
                for voice in voices_data['voices'][:3]:  # Show first 3
                    print(f"   - {voice['name']} ({voice['language']}, {voice['gender']})")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        # Test 2: Generate TTS for each test case
        print(f"\n2. Testing POST /api/tts/generate")
        for i, test_data in enumerate(test_requests, 1):
            print(f"\n   Test {i}: {test_data['voice_id']}")
            print(f"   Text: {test_data['text'][:50]}...")
            
            try:
                response = await client.post(
                    f"{base_url}/api/tts/generate",
                    json=test_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"   ✅ Success: {result['message']}")
                    print(f"   🔊 Audio URL: {result['audio_url']}")
                    print(f"   🆔 Audio ID: {result['audio_id']}")
                else:
                    print(f"   ❌ Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"   ❌ Connection error: {e}")
        
        # Test 3: Error handling
        print(f"\n3. Testing error handling")
        error_tests = [
            {"text": "", "voice_id": "en-US-davis"},  # Empty text
            {"text": "x" * 3001, "voice_id": "en-US-davis"},  # Too long
        ]
        
        for i, test_data in enumerate(error_tests, 1):
            test_desc = "Empty text" if not test_data["text"] else "Text too long"
            print(f"   Test {i}: {test_desc}")
            
            try:
                response = await client.post(
                    f"{base_url}/api/tts/generate",
                    json=test_data
                )
                
                if response.status_code == 400:
                    error_data = response.json()
                    print(f"   ✅ Expected error: {error_data['detail']}")
                else:
                    print(f"   ❌ Unexpected status: {response.status_code}")
                    
            except Exception as e:
                print(f"   ❌ Connection error: {e}")

if __name__ == "__main__":
    print("🚀 Starting TTS API Test Suite")
    print("Make sure the server is running on http://localhost:8000")
    print()
    
    try:
        asyncio.run(test_tts_endpoint())
        print("\n🎉 Test suite completed!")
        print("\n📋 Next steps:")
        print("1. Visit http://localhost:8000/docs to try the interactive API")
        print("2. Use the 'Try it out' feature to test with your own text")
        print("3. Take a screenshot for your LinkedIn post!")
        
    except KeyboardInterrupt:
        print("\n🛑 Tests cancelled by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
