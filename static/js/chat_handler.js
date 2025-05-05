// =========================
// Chat Handler for MathGuruAI Chat Page
// =========================

async function sendMessage() {
    const chatInput = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    const userMessage = chatInput.value.trim();

    if (!userMessage) {
        alert("❗ Please type a question to ask!");
        return;
    }

    // Display user message
    const userBubble = document.createElement('div');
    userBubble.className = 'message user-message';
    userBubble.innerHTML = `<b>You:</b> ${userMessage}`;
    chatBox.appendChild(userBubble);

    chatInput.value = ''; // Clear input

    // Auto scroll to bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Send message to server
        const response = await fetch('/get_hint', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        });

        const data = await response.json();

        // Display bot reply
        const botBubble = document.createElement('div');
        botBubble.className = 'message bot-message';
        botBubble.innerHTML = `<b>MathGuru:</b> ${data.response || '🤖 Sorry, I could not generate a response.'}`;
        chatBox.appendChild(botBubble);

        // Auto scroll again
        chatBox.scrollTop = chatBox.scrollHeight;

    } catch (err) {
        console.error("[Chat Handler Error]:", err);

        const errorBubble = document.createElement('div');
        errorBubble.className = 'message bot-message';
        errorBubble.innerHTML = `<b>MathGuru:</b> ⚠️ Sorry, I could not connect. Please try again later.`;
        chatBox.appendChild(errorBubble);

        chatBox.scrollTop = chatBox.scrollHeight;
    }
}
