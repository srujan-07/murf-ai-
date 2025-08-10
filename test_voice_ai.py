import requests
import os

# Test the voice-to-voice AI endpoint with correct voice ID
def test_voice_ai():
    # Check if we have a test audio file
    audio_file_path = "uploads/echo_recording_1754504235.webm"
    
    if not os.path.exists(audio_file_path):
        print("❌ No test audio file found. Please record some audio first.")
        return
    
    # Prepare the request
    url = "http://localhost:8000/api/llm/query/audio"
    
    with open(audio_file_path, 'rb') as audio_file:
        files = {'audio_file': audio_file}
        data = {
            'voice': 'en-US-natalie',  # Use working voice ID
            'model': 'gemini-1.5-flash',
            'temperature': 0.7
        }
        
        print("🧪 Testing Voice-to-Voice AI endpoint...")
        print(f"Using voice: {data['voice']}")
        
        try:
            response = requests.post(url, files=files, data=data, timeout=60)
            
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Success!")
                print(f"Transcribed: {result.get('transcribed_text', 'N/A')[:100]}...")
                print(f"LLM Response: {result.get('llm_response', 'N/A')[:100]}...")
                print(f"Audio URL: {result.get('audio_url', 'N/A')}")
                print(f"Processing Time: {result.get('processing_time', 'N/A')}s")
            else:
                print("❌ Error:")
                try:
                    error_data = response.json()
                    print(error_data)
                except:
                    print(response.text)
                    
        except Exception as e:
            print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    test_voice_ai()
