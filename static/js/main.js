// =========================
// DOM Element References
// =========================
const video = document.getElementById('camera');
const captureBtn = document.getElementById('captureBtn') || document.getElementById('capture-image');
const snapshot = document.getElementById('snapshot');
const feedbackAudio = document.getElementById('feedbackAudio');
const expressionOutput = document.getElementById('text');
const resultOutput = document.getElementById('result');
const stepsOutput = document.getElementById('steps');
const manualBtn = document.getElementById('manualBtn');
const manualInput = document.getElementById('manualInput');

// =========================
// 1. Start Webcam Stream
// =========================
if (video) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            alert("❌ Camera access denied or not available.");
            console.error("[Camera Error]:", err);
        });
}

// =========================
// 2. Capture Image and Upload to Server
// =========================
if (captureBtn) {
    captureBtn.addEventListener('click', () => {
        const context = snapshot.getContext('2d');
        snapshot.width = video.videoWidth;
        snapshot.height = video.videoHeight;
        context.drawImage(video, 0, 0, snapshot.width, snapshot.height);

        snapshot.toBlob(blob => {
            const formData = new FormData();
            formData.append('image', blob, 'capture.jpg');

            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => handleResponse(data))
            .catch(err => {
                console.error("[Upload Error]:", err);
                showErrorMessage('⚠️ Upload failed. Please try again.');
            });
        }, 'image/jpeg');
    });
}

// =========================
// 3. Manual Input Solve
// =========================
if (manualBtn) {
    manualBtn.addEventListener('click', () => {
        const input = manualInput.value.trim();
        if (!input) {
            alert("❗ Please enter a math expression or question.");
            return;
        }

        fetch('/manual', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ expression: input })
        })
        .then(res => res.json())
        .then(data => handleResponse(data))
        .catch(err => {
            console.error("[Manual Solve Error]:", err);
            showErrorMessage('⚠️ Manual solve failed.');
        });
    });
}

// =========================
// 4. Play English Audio
// =========================
function playHintEnglish() {
    if (feedbackAudio && feedbackAudio.src) {
        feedbackAudio.play()
            .catch(err => console.error("[Audio Playback Error]:", err));
    } else {
        alert('⚠️ No audio available to play.');
    }
}

// =========================
// 5. Play Hindi Audio (Handled separately by hindi_audio.js)
// =========================
function playHintHindi() {
    if (typeof playHindiAudio === 'function') {
        playHindiAudio(); // Call function from hindi_audio.js
    } else {
        alert('⚠️ Hindi audio not available.');
    }
}

// =========================
// 6. Handle Server Response
// =========================
function handleResponse(data) {
    if (data.extracted || data.result || data.steps) {
        expressionOutput.textContent = data.extracted || '---';
        resultOutput.innerHTML = data.result || '--';
        stepsOutput.textContent = data.steps || '📝 No step-by-step explanation available.';

        if (data.audio) {
            const audioPath = '/' + data.audio + '?t=' + new Date().getTime(); // Cache busting
            feedbackAudio.src = audioPath;
            feedbackAudio.style.display = 'block';
        } else {
            feedbackAudio.style.display = 'none';
        }

        // ✅ Re-render MathJax if available
        if (window.MathJax) {
            MathJax.typeset();
        }

    } else {
        showErrorMessage('⚠️ Invalid response received.');
    }
}

// =========================
// 7. Show Error Message Helper
// =========================
function showErrorMessage(message) {
    expressionOutput.textContent = message;
    resultOutput.textContent = '--';
    stepsOutput.textContent = '❌ No explanation returned.';
    feedbackAudio.style.display = 'none';
}

// =========================
// 8. Theme Toggle (Light / Dark Mode)
// =========================
function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const currentTheme = document.body.classList.contains('dark-mode') ? 'dark' : 'light';
    localStorage.setItem('theme', currentTheme);
}

// =========================
// 9. Load Theme on Page Load
// =========================
window.onload = () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode');
    }
};
