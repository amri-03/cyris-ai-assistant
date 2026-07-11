import sys
import os
from dotenv import load_dotenv

# Ensure we have our test API keys loaded
os.environ["GROQ_API_KEY_1"] = "invalid_groq_key_1"
os.environ["GROQ_API_KEY_2"] = "invalid_groq_key_2"
# Note: In a real test, if the actual key is loaded by dotenv, it will be added to the registry

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

from app.services.ai.ai_provider_manager import AIProviderManager

manager = AIProviderManager()
print(f"Loaded {len(manager.providers)} providers.")
for p in manager.providers:
    print(f"- Provider: {p['name']} (Key starting with: {p['client'].api_key[:10] if p['client'].api_key else 'None'}...) Tags: {p['capabilities']}")

print("\n--- Testing Routing (Complex Reasoning) ---")
providers = manager._route_providers("Please analyze this code and reason about its complexity.")
print(f"Top choice for complex reasoning: {providers[0]['name']}")

print("\n--- Testing Routing (Fast Chat) ---")
providers = manager._route_providers("Hello!")
print(f"Top choice for fast chat: {providers[0]['name']}")

print("\n--- Testing Execution (Expect Fallback if invalid keys are present) ---")
try:
    response = manager.generate_ai_response("Say hello in one word", add_to_history=False)
    print("Response received!")
except Exception as e:
    print(f"Final error: {e}")
