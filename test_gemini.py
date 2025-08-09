import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

print(f"API Key loaded: {GEMINI_API_KEY[:10]}...{GEMINI_API_KEY[-10:] if len(GEMINI_API_KEY) > 20 else 'SHORT_KEY'}")

# Configure API
try:
    genai.configure(api_key=GEMINI_API_KEY)
    print("✅ API configured successfully")
except Exception as e:
    print(f"❌ API configuration failed: {e}")
    exit(1)

# Test model initialization
try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    print("✅ Model initialized successfully")
except Exception as e:
    print(f"❌ Model initialization failed: {e}")
    exit(1)

# Test simple query
try:
    print("🧪 Testing simple query...")
    response = model.generate_content("What is 2+2? Give a short answer.")
    print(f"✅ Response received: {response.text}")
except Exception as e:
    print(f"❌ Query failed: {e}")
    print(f"Error type: {type(e).__name__}")
