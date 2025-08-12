import requests
import os
import time

def test_chat_agent():
    """Test the Day 10 chat agent with session history"""
    
    # Check if we have a test audio file
    audio_file_path = "uploads/echo_recording_1754504235.webm"
    
    if not os.path.exists(audio_file_path):
        print("❌ No test audio file found. Please record some audio first.")
        return
    
    # Test session ID
    session_id = f"test_session_{int(time.time())}"
    
    print(f"🧪 Testing Chat Agent with Session: {session_id}")
    
    # Test 1: First message in conversation
    print("\n📝 Test 1: First message in conversation")
    url = f"http://localhost:8000/api/agent/chat/{session_id}"
    
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
                print(f"✅ Success: {result['message']}")
                print(f"📝 Transcribed: {result.get('transcribed_text', 'N/A')}")
                print(f"🤖 AI Response: {result.get('llm_response', 'N/A')[:100]}...")
                print(f"🎵 Audio URL: {result.get('audio_url', 'N/A')}")
                print(f"💬 Message Count: {result.get('message_count', 'N/A')}")
                print(f"⏱️ Processing Time: {result.get('processing_time', 'N/A')}s")
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('detail', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
    
    # Small delay between requests
    time.sleep(2)
    
    # Test 2: Second message in same conversation
    print(f"\n📝 Test 2: Second message in same session")
    
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
                print(f"✅ Success: {result['message']}")
                print(f"📝 Transcribed: {result.get('transcribed_text', 'N/A')}")
                print(f"🤖 AI Response: {result.get('llm_response', 'N/A')[:100]}...")
                print(f"💬 Message Count: {result.get('message_count', 'N/A')}")
                print(f"⏱️ Processing Time: {result.get('processing_time', 'N/A')}s")
            else:
                error_data = response.json()
                print(f"❌ Error: {error_data.get('detail', 'Unknown error')}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request Error: {e}")
    
    # Test 3: Get chat history
    print(f"\n📝 Test 3: Fetch chat history")
    history_url = f"http://localhost:8000/api/agent/chat/{session_id}/history"
    
    try:
        response = requests.get(history_url, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ History Retrieved: {result.get('message_count', 0)} messages")
            print(f"📅 Created: {time.ctime(result.get('created_at', 0))}")
            print(f"📅 Updated: {time.ctime(result.get('updated_at', 0))}")
            
            messages = result.get('messages', [])
            for i, msg in enumerate(messages):
                role = msg['role'].title()
                content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
                timestamp = time.ctime(msg['timestamp'])
                print(f"  {i+1}. {role}: {content} ({timestamp})")
        else:
            error_data = response.json()
            print(f"❌ Error: {error_data.get('detail', 'Unknown error')}")
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")

if __name__ == "__main__":
    test_chat_agent()
