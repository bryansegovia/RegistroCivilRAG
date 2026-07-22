const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const messages = document.querySelector("#messages");

const history = [];

function appendMessage(role, content, sources = []) {
  const wrapper = document.createElement("article");
  wrapper.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = content;

  if (sources.length > 0) {
    const details = document.createElement("details");
    details.className = "sources";
    const summary = document.createElement("summary");
    summary.textContent = "Fuentes usadas";
    const list = document.createElement("ul");

    sources.forEach((source) => {
      const item = document.createElement("li");
      const page = Number.isInteger(source.page) ? `, pagina ${source.page + 1}` : "";
      item.textContent = `${source.source}${page}: ${source.preview}`;
      list.appendChild(item);
    });

    details.append(summary, list);
    bubble.appendChild(details);
  }

  wrapper.appendChild(bubble);
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;
}

function resizeInput() {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 160)}px`;
}

input.addEventListener("input", resizeInput);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  appendMessage("user", message);
  history.push({ role: "user", content: message });

  input.value = "";
  resizeInput();
  sendButton.disabled = true;
  sendButton.textContent = "Enviando";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: history.slice(0, -1) }),
    });

    const payload = await response.json();
    if (!response.ok) {
      throw new Error(payload.detail || "No se pudo responder.");
    }

    appendMessage("assistant", payload.answer, payload.sources);
    history.push({ role: "assistant", content: payload.answer });
  } catch (error) {
    appendMessage("assistant", error.message);
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "Enviar";
    input.focus();
  }
});
