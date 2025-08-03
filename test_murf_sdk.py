#!/usr/bin/env python3
"""
Quick test for Day 2 TTS API endpoint using Murf SDK
"""

import asyncio
import httpx
import json

async def test_murf_tts():
    """Test the TTS generation endpoint with Murf SDK"""
    
    base_url = "http://localhost:8000"
    
    # Test the TTS generation with example from Murf documentation
    test_request = {
        "text": "In this experiential elearning module, you'll master the basics of using this Text to Speech widget. Choose a voice, experiment with styles, explore languages, customize text, and play with various use-cases for a view into all that Murf offers.",
        "voice_id": "en-US-natalie"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        print("🎤 Testing Murf TTS API Integration")
        print("=" * 50)
        
        # Test 1: Get available voices
        print("\n1. Testing GET /api/tts/voices")
        try:
            response = await client.get(f"{base_url}/api/tts/voices")
            if response.status_code == 200:
                voices_data = response.json()
                print(f"✅ Success! Found {voices_data['total_count']} voices")
                print(f"📢 Source: {voices_data['source']}")
                for voice in voices_data['voices'][:3]:  # Show first 3
                    print(f"   - {voice['name']} ({voice['language']}, {voice['gender']})")
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")
        
        # Test 2: Generate TTS using Murf SDK
        print(f"\n2. Testing POST /api/tts/generate with Murf SDK")
        print(f"   Voice: {test_request['voice_id']}")
        print(f"   Text: {test_request['text'][:60]}...")
        
        try:
            response = await client.post(
                f"{base_url}/api/tts/generate",
                json=test_request
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Success: {result['message']}")
                print(f"   🔊 Audio URL: {result['audio_url']}")
                print(f"   🆔 Audio ID: {result['audio_id']}")
                print(f"   📊 Response: {json.dumps(result, indent=2)}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Connection error: {e}")
        
        # Test 3: Quick voice test
        print(f"\n3. Testing with shorter text")
        quick_test = {
            "text": "Hello! This is a quick test of the Murf TTS integration.",
            "voice_id": "en-US-natalie"
        }
        
        try:
            response = await client.post(
                f"{base_url}/api/tts/generate",
                json=quick_test
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"   ✅ Quick test successful!")
                print(f"   🔊 Audio URL: {result['audio_url']}")
            else:
                print(f"   ❌ Error {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Connection error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Murf TTS API Test")
    print("Make sure the server is running on http://localhost:8000")
    print()
    
    try:
        asyncio.run(test_murf_tts())
        print("\n🎉 Test completed!")
        print("\n📋 Next steps:")
        print("1. Visit http://localhost:8000/docs to test interactively")
        print("2. Try the TTS endpoint with different voices")
        print("3. Take a screenshot for your LinkedIn post!")
        
    except KeyboardInterrupt:
        print("\n🛑 Tests cancelled by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
