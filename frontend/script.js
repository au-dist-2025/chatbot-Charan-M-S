const API_URL = "http://127.0.0.1:5000/chat"; // replace with Render URL after deployment

const chatBox = document.getElementById("chat-box");
const input = document.getElementById("user-input");
const btn = document.getElementById("send-btn");

btn.addEventListener("click", sendMessage);
input.addEventListener("keydown", (e) => { if (e.key === "Enter") sendMessage(); });

function addMessage(text, who) {
  const p = document.createElement("div");
  p.className = "msg " + (who === "user" ? "user" : "bot");
  p.textContent = text;
  chatBox.appendChild(p);
  chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
  const text = input.value.trim();
  if (!text) return;
  addMessage("You: " + text, "user");
  input.value = "";
  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });
    const data = await res.json();
    addMessage("StudyBuddy: " + data.response, "bot");
  } catch (e) {
    addMessage("StudyBuddy: Sorry, I cannot reach the server. (Check backend URL)", "bot");
  }
}
