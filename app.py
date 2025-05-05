from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import os
from werkzeug.utils import secure_filename
from utils.ocr import extract_text
from utils.feedback import evaluate_and_speak, save_feedback
from utils.auth import check_login, register_user
from utils.hints import get_gemini_hint
from utils.history import save_history, load_history

# ---------------- APP CONFIG ---------------- #
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['AUDIO_FOLDER'] = 'static/audio'
app.secret_key = 'mathguru-secret-key'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

# ---------------- AUTH ROUTES ---------------- #

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if check_login(username, password):
            session['user'] = username
            return redirect('/')
        return render_template('login.html', error="Invalid credentials.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if register_user(username, password):
            return redirect('/login')
        return render_template('register.html', error="User already exists.")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# ---------------- MAIN ROUTES ---------------- #

@app.route('/')
def index():
    if 'user' not in session:
        return redirect('/login')
    return render_template('index.html')

@app.route('/manual-page')
def manual_page():
    if 'user' not in session:
        return redirect('/login')
    return render_template('manual.html')

@app.route('/feedback')
def feedback():
    if 'user' not in session:
        return redirect('/login')
    return render_template('feedback.html')

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    try:
        name = request.form.get('name', 'Anonymous')
        message = request.form.get('message', '')
        rating = request.form.get('rating', '5')
        save_feedback(name, message, rating)
        return "<h2>✅ Thank you for your feedback!</h2><a href='/'>🔙 Back to Home</a>"
    except Exception as e:
        print(f"[FEEDBACK ERROR]: {e}")
        return "<h2>❌ Failed to save feedback</h2>", 500

@app.route('/result')
def result_page():
    if 'user' not in session:
        return redirect('/login')
    return render_template('result.html', expression="5 + 2", result="7")

@app.route('/manual', methods=['POST'])
def manual_input():
    try:
        if 'user' not in session:
            return jsonify({'error': 'Unauthorized'}), 401

        data = request.get_json()
        expression = data.get('expression', '').strip()
        print(f"[MANUAL INPUT]: {expression}")

        if not expression:
            return jsonify({'error': 'Empty expression received'}), 400

        result, audio_path = evaluate_and_speak(expression)
        print(f"[RESULT]: {result} | [AUDIO]: {audio_path}")

        # Save to history
        save_history(expression, result["answer"], result["steps"])

        return jsonify({
            'extracted': expression,
            'result': result["answer"],
            'steps': result["steps"],
            'audio': audio_path
        })

    except Exception as e:
        print(f"[MANUAL ERROR]: {e}")
        return jsonify({'error': 'Manual input processing failed'}), 500

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    file = request.files.get('image')
    if not file:
        return jsonify({'error': 'No image received'}), 400

    try:
        filename = secure_filename(file.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(image_path)

        extracted = extract_text(image_path)
        print(f"[OCR TEXT]: {extracted}")

        result, audio_path = evaluate_and_speak(extracted)
        print(f"[RESULT]: {result} | [AUDIO]: {audio_path}")

        # Save to history
        save_history(extracted, result["answer"], result["steps"])

        return jsonify({
            'extracted': extracted,
            'result': result["answer"],
            'steps': result["steps"],
            'audio': audio_path
        })

    except Exception as e:
        print(f"[UPLOAD ERROR]: {e}")
        return jsonify({'error': 'Image processing failed'}), 500

# ---------------- KHANMIGO-LIKE FEATURES ---------------- #

@app.route('/chat')
def chat():
    if 'user' not in session:
        return redirect('/login')
    return render_template('chat.html')

@app.route('/get_hint', methods=['POST'])
def get_hint():
    try:
        data = request.get_json()
        prompt = data.get('message', '')
        response = get_gemini_hint(prompt)
        return jsonify({'response': response})
    except Exception as e:
        print(f"[GEMINI ERROR]: {e}")
        return jsonify({'response': 'Sorry, there was an error generating a hint.'})

@app.route('/history')
def view_history():
    if 'user' not in session:
        return redirect('/login')
    logs = load_history()
    return render_template('history.html', logs=logs)
@app.route('/hints')
def show_hint_page():
    if 'user' not in session:
        return redirect('/login')
    return render_template('hints.html', hint="Type a question or scan to get your hint.")

# ---------------- RUN SERVER ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
