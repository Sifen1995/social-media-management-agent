"""List available Gemini models."""
import google.generativeai as genai

genai.configure(api_key="AIzaSyB4zthtf6hUL16sPW44TsAYHs8vUKwpnaI")

print("Available Gemini models:")
print("=" * 60)

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"Model: {model.name}")
        print(f"  Display Name: {model.display_name}")
        print(f"  Description: {model.description}")
        print(f"  Supported methods: {model.supported_generation_methods}")
        print()
