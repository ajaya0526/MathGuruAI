# test_gemini_list.py
import google.generativeai as genai

# Use your API key here
genai.configure(api_key="AIzaSyBB_wjbbNfiGLNPKzaSUo-7Ou-Rf7YU4ZU")

try:
    print("📌 Available Gemini Models:\n")
    models = genai.list_models()
    for model in models:
        print(f"✅ Model Name: {model.name}")
        print(f"   ➤ Generation Methods: {model.supported_generation_methods}")
        print(f"   ➤ Description: {model.display_name}")
        print("-" * 50)

except Exception as e:
    print(f"❌ ERROR listing models: {e}")
