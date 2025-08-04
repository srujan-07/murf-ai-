#!/usr/bin/env python3
"""
Day 3 Test Script - Testing TTS Audio Playback
Tests the complete flow: text input -> API call -> audio URL -> playback
"""

import asyncio
import httpx
from datetime import datetime

async def test_day3_functionality():
    """Test the Day 3 TTS and audio playback functionality"""
    
    base_url = "http://localhost:8000"
    
    print("🎤 Day 3: Testing TTS Audio Playback")
    print("=" * 50)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test texts for Day 3
    test_cases = [
        {
            "name": "Day 3 Welcome Message",
            "text": "Hello! Welcome to Day 3 of the 30 Days of Voice Agents challenge. Today we are implementing audio playback functionality using HTML audio elements.",
            "voice_id": "en-US-natalie"
        },
        {
            "name": "Short Test",
            "text": "This is a quick test of our text-to-speech and audio playback integration.",
            "voice_id": "en-US-davis"
        },
        {
            "name": "Feature Description",
            "text": "Our Day 3 implementation includes a text field for input, a submit button to generate audio, and an HTML audio element for playback.",
            "voice_id": "en-US-jane"
        }
    ]
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        
        # Test 1: Check API Health
        print("1️⃣ Testing API Health")
        try:
            response = await client.get(f"{base_url}/api/health")
            if response.status_code == 200:
                health_data = response.json()
                print(f"   ✅ API Health: {health_data['status']}")
                print(f"   📝 Message: {health_data['message']}")
            else:
                print(f"   ❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
        
        print()
        
        # Test 2: Test each TTS case
        for i, test_case in enumerate(test_cases, 2):
            print(f"{i}️⃣ Testing: {test_case['name']}")
            print(f"   📝 Text: {test_case['text'][:60]}...")
            print(f"   🎙️ Voice: {test_case['voice_id']}")
            
            try:
                # Make TTS request
                tts_response = await client.post(
                    f"{base_url}/api/tts/generate",
                    json={
                        "text": test_case['text'],
                        "voice_id": test_case['voice_id']
                    }
                )
                
                if tts_response.status_code == 200:
                    result = tts_response.json()
                    print(f"   ✅ Success: {result['success']}")
                    print(f"   🔊 Audio URL: {result['audio_url'][:60]}...")
                    print(f"   🆔 Audio ID: {result.get('audio_id', 'N/A')}")
                    
                    # Test if audio URL is accessible
                    try:
                        audio_check = await client.head(result['audio_url'])
                        if audio_check.status_code == 200:
                            print(f"   🎵 Audio file accessible: Yes")
                        else:
                            print(f"   ⚠️ Audio file status: {audio_check.status_code}")
                    except Exception as audio_error:
                        print(f"   ⚠️ Audio file check failed: {audio_error}")
                        
                else:
                    print(f"   ❌ TTS failed: {tts_response.status_code}")
                    print(f"   📄 Response: {tts_response.text}")
                    
            except Exception as e:
                print(f"   ❌ Request error: {e}")
            
            print()
        
        # Test 3: Voice list
        print("4️⃣ Testing Voice List")
        try:
            voices_response = await client.get(f"{base_url}/api/tts/voices")
            if voices_response.status_code == 200:
                voices_data = voices_response.json()
                print(f"   ✅ Available voices: {voices_data['total_count']}")
                print(f"   📊 Source: {voices_data['source']}")
                for voice in voices_data['voices'][:3]:
                    print(f"      - {voice['name']} ({voice['language']}, {voice['gender']})")
            else:
                print(f"   ❌ Voices request failed: {voices_response.status_code}")
        except Exception as e:
            print(f"   ❌ Voices error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Day 3 Test Suite")
    print("📍 Make sure the server is running on http://localhost:8000")
    print("🎯 Testing: Text input -> TTS generation -> Audio playback flow")
    print()
    
    try:
        asyncio.run(test_day3_functionality())
        print("\n🎉 Day 3 Tests Completed!")
        print("\n📋 Next Steps:")
        print("1. 🌐 Open http://localhost:8000 in your browser")
        print("2. ✍️ Enter text in the input field")
        print("3. 🔘 Click 'Generate & Play Audio' button")
        print("4. 🎵 Listen to the generated audio")
        print("5. 📸 Take a screenshot for your LinkedIn post!")
        
    except KeyboardInterrupt:
        print("\n🛑 Tests cancelled by user")
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
