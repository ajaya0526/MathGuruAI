import os
import json
import uuid
import time
import pyttsx3
import re
from gtts import gTTS
import google.generativeai as genai

# ✅ Gemini Configuration
genai.configure(api_key=os.getenv("GEMINI_API_KEY", "AIzaSyBB_wjbbNfiGLNPKzaSUo-7Ou-Rf7YU4ZU"))

# 💾 Feedback JSON DB
FEEDBACK_DB = 'utils/feedbacks.json'
if not os.path.exists(FEEDBACK_DB):
    with open(FEEDBACK_DB, 'w') as f:
        json.dump([], f)

# 💬 Save user feedback
def save_feedback(name, message, rating):
    entry = {"name": name, "message": message, "rating": rating}
    with open(FEEDBACK_DB, 'r') as f:
        data = json.load(f)
    data.append(entry)
    with open(FEEDBACK_DB, 'w') as f:
        json.dump(data, f, indent=4)

# 🤖 Generate Tutor-Style Hints and Answer using Gemini
def evaluate_and_speak(expression):
    try:
        print(f"[MATHGURU]: Solving: {expression}")
        model = genai.GenerativeModel("models/gemini-2.0-flash")  # ✅ Correct model name

        # 🧠 Prompt with tutoring logic
        prompt = f"""
        Act like a kind and helpful math tutor. Help a student solve: "{expression}"

        💡 Hint 1: What should they try first?
        💡 Hint 2: Which concept or formula applies?
        💡 Hint 3: What is the final step before solving?

        ✅ Final Answer (label it clearly).

        📘 Then give a step-by-step explanation in plain language.
        """

        response = model.generate_content(prompt)

        # Debug info
        print("📤 Prompt Feedback:", response.prompt_feedback)
        print("📑 Candidates:", response.candidates)

        result_text = response.text.strip()
        print("[GEMINI RESPONSE]:", result_text)

        # 🔍 Extract final answer
        match = re.search(r"(Final Answer|Answer)[:：]?\s*(.+)", result_text, re.IGNORECASE)
        answer_line = match.group(2).strip() if match else "Could not extract answer."

        # 🔊 Generate English audio
        tts = gTTS(text=answer_line, lang='en')
        filename = f"static/audio/feedback_{int(time.time())}.mp3"
        tts.save(filename)

        return {
            "answer": answer_line,
            "steps": result_text
        }, filename

    except Exception as e:
        print(f"[GEMINI ERROR]: {e}")
        return {
            "answer": "Unable to solve.",
            "steps": "There was an error processing the solution. Try again."
        }, ""

# 🔊 Hindi Audio Fallback
def synthesize_hindi_audio(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 140)
        voices = engine.getProperty('voices')
        found_hindi = False

        for voice in voices:
            langs = voice.languages
            if isinstance(langs, list) and langs:
                try:
                    lang_code = langs[0].decode('utf-8')
                    if 'hi' in lang_code or 'Hindi' in voice.name:
                        engine.setProperty('voice', voice.id)
                        print(f"✅ Hindi voice selected: {voice.name}")
                        found_hindi = True
                        break
                except Exception:
                    continue

        if not found_hindi:
            print("⚠️ Hindi voice not found. Using default voice.")

        audio_file = f"static/audio/{uuid.uuid4().hex}.mp3"
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        return audio_file

    except Exception as e:
        print(f"[AUDIO ERROR]: {e}")
        return ""
