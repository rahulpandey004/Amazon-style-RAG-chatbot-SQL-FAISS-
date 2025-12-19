async function sendMessage() {
    const input = document.getElementById("chatInput");
    const chatBox = document.getElementById("chatBox");

    const userMessage = input.value.trim();
    if (!userMessage) return;

    // Show user message
    chatBox.innerHTML += `
        <div style="margin-bottom:8px; text-align:right;">
            <b>You:</b> ${userMessage}
        </div>
    `;

    input.value = "";

    // Call backend chatbot API
    const res = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await res.json();

    // Show bot reply
    chatBox.innerHTML += `
        <div style="margin-bottom:8px;">
            <b>Bot:</b> ${data.reply}
        </div>
    `;

    chatBox.scrollTop = chatBox.scrollHeight;
}
