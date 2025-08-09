import requests
import json

# Test data
test_data = {
    "text": "Hello, what is 2+2?",
    "model": "gemini-1.5-flash",
    "max_tokens": 100,
    "temperature": 0.7
}

# Make request
try:
    print("🧪 Testing LLM endpoint...")
    response = requests.post(
        "http://localhost:8000/api/llm/query",
        json=test_data,
        timeout=30
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Success!")
        print(f"Response: {data.get('response', 'No response field')}")
        print(f"Model Used: {data.get('model_used', 'Unknown')}")
        print(f"Tokens Used: {data.get('tokens_used', 'Unknown')}")
    else:
        print("❌ Error response:")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(f"Raw response: {response.text}")
            
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
