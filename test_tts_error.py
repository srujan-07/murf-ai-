import requests
import os

def test_tts_error_handling():
    """Test TTS error handling with disabled Murf API"""
    
    # Check if we have a test audio file
    audio_file_path = "uploads/echo_recording_1754504235.webm"
    
    if not os.path.exists(audio_file_path):
        print("❌ No test audio file found. Please record some audio first.")
        return
    
    session_id = "error_test_session"
    url = f"http://localhost:8000/api/agent/chat/{session_id}"
    
    print("🧪 Testing TTS Error Handling (Murf API Disabled)")
    print("=" * 55)
    
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio_file': audio_file}
        data = {
            'voice': 'en-US-natalie',
            'model': 'gemini-1.5-flash',
            'temperature': 0.7
        }
        
        try:
            response = requests.post(url, files=files, data=data, timeout=60)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response received!")
                print(f"Success: {result.get('success', 'N/A')}")
                print(f"Message: {result.get('message', 'N/A')}")
                print(f"📝 Transcribed: {result.get('transcribed_text', 'N/A')}")
                print(f"🤖 AI Response: {result.get('llm_response', 'N/A')[:100]}...")
                print(f"🎵 Audio URL: {result.get('audio_url', 'N/A')}")
                print(f"⏱️ Processing Time: {result.get('processing_time', 'N/A')}s")
                
                if result.get('audio_url') is None:
                    print("✅ EXPECTED: No audio URL returned (TTS disabled)")
                    print("✅ ERROR HANDLING: Successfully handled TTS failure")
                else:
                    print("⚠️ Unexpected: Audio URL returned despite TTS being disabled")
                    
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('detail', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")

if __name__ == "__main__":
    test_tts_error_handling()
