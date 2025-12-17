const chat = document.getElementById("chat");
const input = document.getElementById("question");

let history = [];
const MAX_MESSAGES = 20;

function addMessage(role, content) {
    const div = document.createElement("div");
    div.className = `message ${role}`;
    div.textContent = content;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    return div;
}

async function askQuestion() {
    const question = input.value.trim();
    if (!question) return;

    input.value = "";
    addMessage("user", question);

    history.push({ role: "user", content: question });

    if (history.length > MAX_MESSAGES) {
        history = [];
        chat.innerHTML = "";
        addMessage("system", "🔄 Nouvelle conversation");
        return;
    }

    // 👇 Message "chargement"
    const loadingMsg = addMessage("assistant", "⏳ Chargement...");

    try {
        const res = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                question,
                history
            })
        });

        const data = await res.json();

        // 👇 Supprime le message "chargement"
        loadingMsg.remove();

        addMessage("assistant", data.answer);
        history.push({ role: "assistant", content: data.answer });

    } catch (e) {
        loadingMsg.remove();
        addMessage("assistant", "❌ Erreur serveur");
    }
}
