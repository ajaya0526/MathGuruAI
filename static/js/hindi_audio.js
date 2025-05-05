// =========================
// Hindi Text-to-Speech Handler
// =========================

function playHindiAudio() {
    const textElement = document.getElementById('text');
    if (!textElement) {
        alert("⚠️ No text found to speak.");
        return;
    }

    const text = textElement.textContent.trim();

    if (!text || text === '--') {
        alert("⚠️ No valid text to read aloud!");
        return;
    }

    if (!('speechSynthesis' in window)) {
        alert("❌ Your browser does not support speech synthesis (text-to-speech).");
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'hi-IN'; // Hindi language
    utterance.pitch = 1.0;     // Normal pitch
    utterance.rate = 0.9;      // Slightly slower for better clarity
    utterance.volume = 1.0;    // Full volume

    // Cancel any previous speaking before starting new
    speechSynthesis.cancel();
    speechSynthesis.speak(utterance);
}
