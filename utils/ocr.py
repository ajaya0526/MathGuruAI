# utils/ocr.py

import cv2
import pytesseract
import easyocr
import re
import os
import google.generativeai as genai

# ✅ Initialize EasyOCR
reader = easyocr.Reader(['en'], gpu=False)

# ✅ Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'your-fallback-api-key'))

def extract_text(image_path):
    """
    Extracts text from an image using a hybrid approach:
    - First tries Gemini Vision API
    - Falls back to Tesseract OCR
    - Further falls back to EasyOCR if needed
    """

    # =====================
    # 🔍 Step 1: Try Gemini Vision
    # =====================
    try:
        print("[INFO] Trying Gemini Vision API for OCR...")

        with open(image_path, 'rb') as img_file:
            image_bytes = img_file.read()

        model = genai.GenerativeModel("models/gemini-pro-vision")

        prompt = (
            "You are an AI assistant. Read the image and extract only the mathematical expression or question written in it. "
            "Return only the clean expression. Do not explain anything. Do not add extra text."
        )

        response = model.generate_content([
            prompt,
            {"mime_type": "image/jpeg", "data": image_bytes}
        ])

        gemini_output = response.text.strip()
        print(f"[GEMINI VISION OUTPUT]: {gemini_output}")

        # Clean Gemini output if needed
        cleaned_gemini = clean_math_expression(gemini_output)

        if len(cleaned_gemini) > 3:
            return cleaned_gemini

    except Exception as gemini_err:
        print(f"[GEMINI OCR ERROR]: {gemini_err}")
        print("[INFO] Falling back to local OCR methods...")

    # =====================
    # 🛠️ Step 2: Local OCR Fallback (Tesseract)
    # =====================
    try:
        print("[INFO] Trying Tesseract OCR...")

        image = cv2.imread(image_path)
        image = cv2.resize(image, (640, 480))
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        processed = cv2.bitwise_not(thresh)

        config = '--psm 6'
        tesseract_text = pytesseract.image_to_string(processed, config=config)
        cleaned_tesseract = clean_math_expression(tesseract_text)
        print(f"[TESSERACT OUTPUT]: {cleaned_tesseract}")

        if len(cleaned_tesseract) > 3:
            return cleaned_tesseract

    except Exception as tesseract_err:
        print(f"[TESSERACT OCR ERROR]: {tesseract_err}")

    # =====================
    # 📚 Step 3: Last Fallback - EasyOCR
    # =====================
    try:
        print("[INFO] Trying EasyOCR...")

        easy_text = reader.readtext(image_path, detail=0)
        joined_easy = ' '.join(easy_text).strip()
        cleaned_easyocr = clean_math_expression(joined_easy)
        print(f"[EASYOCR OUTPUT]: {cleaned_easyocr}")

        return cleaned_easyocr if cleaned_easyocr else "Unable to extract text."

    except Exception as easyocr_err:
        print(f"[EASYOCR ERROR]: {easyocr_err}")
        return "OCR processing error."

# =====================
# 🧹 Helper Function to Clean Math Expression
# =====================

def clean_math_expression(raw_text):
    """
    Cleans the OCR output to extract valid math expressions/questions.
    Removes unnecessary words, leaving mathematical operators and numbers.
    """

    try:
        cleaned = re.findall(r'[\d\w\s\+\-\*/\^\=\(\)\[\]\{\}\.,]+', raw_text)
        return ' '.join(cleaned).strip()
    except Exception as e:
        print(f"[CLEANING ERROR]: {e}")
        return raw_text.strip()
