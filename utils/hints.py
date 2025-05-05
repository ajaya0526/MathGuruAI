# utils/hints.py

import os
import requests

# OPTIONAL: If you have Gemini API key
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'your-demo-api-key')  # Replace 'your-demo-api-key' if needed
GEMINI_API_URL = "https://your-gemini-api-url.com/v1/generate"     # Replace if you are using Gemini officially

# -----------------------------
# Main function to generate hint
# -----------------------------

def get_gemini_hint(prompt):
    """
    Given a math question or problem description,
    returns a simple step-by-step educational hint.
    """

    if not prompt:
        return "⚠️ No question received to generate a hint."

    try:
        # Uncomment this if you have Gemini API available
        """
        headers = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "prompt": f"Help a student solve: {prompt}. Give a friendly, simple hint without full answer."
        }
        response = requests.post(GEMINI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        hint_text = data.get('response', '❔ No detailed hint generated.')
        return hint_text
        """

        # If you don't have Gemini live yet: Use simple fallback for now
        fallback_hint = f"🔎 Tip: Break down the problem '{prompt}' into smaller parts. What can you simplify first?"
        return fallback_hint

    except Exception as e:
        print(f"[GEMINI HINT ERROR]: {e}")
        return "⚠️ Sorry, there was an error generating a hint. Please try again later."

