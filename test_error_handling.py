import os
import time
from pathlib import Path

def simulate_api_failures():
    """
    Simulate API failures by commenting out API keys in .env file
    This helps test error handling scenarios
    """
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found. Please ensure it exists.")
        return
    
    # Read current .env content
    with open(env_file, 'r') as f:
        content = f.read()
    
    print("🧪 API Failure Simulation Tool")
    print("=" * 50)
    print("This tool helps test error handling by temporarily disabling API keys.")
    print()
    
    while True:
        print("Choose a failure scenario to simulate:")
        print("1. Disable AssemblyAI (STT failure)")
        print("2. Disable Gemini AI (LLM failure)")
        print("3. Disable Murf TTS (TTS failure)")
        print("4. Disable All APIs (Complete failure)")
        print("5. Restore All APIs (Fix everything)")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == "1":
            # Comment out AssemblyAI key
            updated_content = content.replace(
                "ASSEMBLY_AI_API_KEY=",
                "#ASSEMBLY_AI_API_KEY="
            )
            scenario = "STT (Speech-to-Text) failure"
            
        elif choice == "2":
            # Comment out Gemini key
            updated_content = content.replace(
                "GEMINI_API_KEY=",
                "#GEMINI_API_KEY="
            )
            scenario = "LLM (Language Model) failure"
            
        elif choice == "3":
            # Comment out Murf key
            updated_content = content.replace(
                "MURF_API_KEY=",
                "#MURF_API_KEY="
            )
            scenario = "TTS (Text-to-Speech) failure"
            
        elif choice == "4":
            # Comment out all keys
            updated_content = content.replace("ASSEMBLY_AI_API_KEY=", "#ASSEMBLY_AI_API_KEY=")
            updated_content = updated_content.replace("GEMINI_API_KEY=", "#GEMINI_API_KEY=")
            updated_content = updated_content.replace("MURF_API_KEY=", "#MURF_API_KEY=")
            scenario = "Complete API failure"
            
        elif choice == "5":
            # Restore all keys
            updated_content = content.replace("#ASSEMBLY_AI_API_KEY=", "ASSEMBLY_AI_API_KEY=")
            updated_content = updated_content.replace("#GEMINI_API_KEY=", "GEMINI_API_KEY=")
            updated_content = updated_content.replace("#MURF_API_KEY=", "MURF_API_KEY=")
            scenario = "All APIs restored"
            
        elif choice == "6":
            print("👋 Exiting simulation tool.")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")
            continue
        
        # Write updated content
        with open(env_file, 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Simulated: {scenario}")
        print("🔄 Restart the server to apply changes.")
        print("📝 Test the chat agent to see error handling in action.")
        print()
        
        # Update content for next iteration
        content = updated_content

def test_error_scenarios():
    """
    Test different error scenarios and document the results
    """
    scenarios = [
        {
            "name": "STT Failure",
            "description": "Speech recognition service unavailable",
            "expected": "Fallback message: 'Sorry, I couldn't understand what you said due to a technical issue.'"
        },
        {
            "name": "LLM Failure", 
            "description": "Language model service unavailable",
            "expected": "Fallback message: 'I'm having trouble processing your request right now due to a technical issue.'"
        },
        {
            "name": "TTS Failure",
            "description": "Text-to-speech service unavailable", 
            "expected": "Text response only with browser speech synthesis fallback"
        },
        {
            "name": "Complete Failure",
            "description": "All services unavailable",
            "expected": "Text fallback: 'I'm experiencing technical difficulties right now.'"
        }
    ]
    
    print("📊 Error Handling Test Scenarios")
    print("=" * 60)
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   Description: {scenario['description']}")
        print(f"   Expected Result: {scenario['expected']}")
    
    print("\n🧪 Test Instructions:")
    print("1. Use the simulate_api_failures() function to disable specific APIs")
    print("2. Restart the server: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
    print("3. Test the chat agent in the browser")
    print("4. Observe error handling and fallback responses")
    print("5. Document results for LinkedIn post")

if __name__ == "__main__":
    print("🔧 Voice Agent Error Handling Test Suite")
    print("=" * 50)
    print()
    
    choice = input("Choose action:\n1. Simulate API failures\n2. View test scenarios\n\nEnter choice (1-2): ").strip()
    
    if choice == "1":
        simulate_api_failures()
    elif choice == "2":
        test_error_scenarios()
    else:
        print("❌ Invalid choice.")
