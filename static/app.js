const form = document.querySelector("#chat-form");
const input = document.querySelector("#message-input");
const sendButton = document.querySelector("#send-button");
const messages = document.querySelector("#messages");

const history = [];

function appendFormattedText(parent, text) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g);

  parts.forEach((part) => {
    if (!part) return;

    if (part.startsWith("**") && part.endsWith("**")) {
      const strong = document.createElement("strong");
      strong.textContent = part.slice(2, -2);
      parent.appendChild(strong);
      return;
    }

    parent.appendChild(document.createTextNode(part));
  });
}

function renderFormattedContent(container, content) {
  const lines = content.split(/\r?\n/);
  let currentList = null;
  let currentListType = null;
  let paragraphLines = [];

  function flushParagraph() {
    if (paragraphLines.length === 0) return;

    const paragraph = document.createElement("p");
    appendFormattedText(paragraph, paragraphLines.join(" "));
    container.appendChild(paragraph);
    paragraphLines = [];
  }

  function closeList() {
    currentList = null;
    currentListType = null;
  }

  lines.forEach((rawLine) => {
    const line = rawLine.trim();

    if (!line) {
      flushParagraph();
      closeList();
      return;
    }

    const unorderedListMatch = line.match(/^[-*]\s+(.+)$/);
    const orderedListMatch = line.match(/^\d+\.\s+(.+)$/);
    const listMatch = unorderedListMatch || orderedListMatch;

    if (listMatch) {
      flushParagraph();
      const listType = orderedListMatch ? "ol" : "ul";
      if (!currentList || currentListType !== listType) {
        currentList = document.createElement(listType);
        currentListType = listType;
        container.appendChild(currentList);
      }

      const item = document.createElement("li");
      appendFormattedText(item, listMatch[1]);
      currentList.appendChild(item);
      return;
    }

    closeList();
    paragraphLines.push(line);
  });

  flushParagraph();
}

function appendMessage(role, content, sources = []) {
  const wrapper = document.createElement("article");
  wrapper.className = `message ${role}`;

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (role === "assistant") {
    renderFormattedContent(bubble, content);
  } else {
    bubble.textContent = content;
  }

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
  return wrapper;
}

function appendTypingMessage() {
  const wrapper = document.createElement("article");
  wrapper.className = "message assistant typing";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  const label = document.createElement("span");
  label.textContent = "Escribiendo";

  const dots = document.createElement("span");
  dots.className = "typing-dots";
  dots.append(document.createElement("span"), document.createElement("span"), document.createElement("span"));

  bubble.append(label, dots);
  wrapper.appendChild(bubble);
  messages.appendChild(wrapper);
  messages.scrollTop = messages.scrollHeight;
  return wrapper;
}

function removeSuggestions() {
  const suggestions = document.querySelector("#suggestions");
  if (suggestions) {
    suggestions.remove();
  }
}

function resizeInput() {
  input.style.height = "auto";
  input.style.height = `${Math.min(input.scrollHeight, 160)}px`;
}

function submitMessage(message) {
  input.value = message;
  form.requestSubmit();
}

input.addEventListener("input", resizeInput);
input.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();
    form.requestSubmit();
  }
});

document.querySelectorAll(".suggestion").forEach((button) => {
  button.addEventListener("click", () => {
    submitMessage(button.textContent.trim());
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const message = input.value.trim();
  if (!message) return;

  removeSuggestions();
  appendMessage("user", message);
  history.push({ role: "user", content: message });

  input.value = "";
  resizeInput();
  sendButton.disabled = true;
  sendButton.textContent = "Enviando";
  const typingMessage = appendTypingMessage();

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, history: history.slice(0, -1) }),
    });

    const contentType = response.headers.get("content-type") || "";
    const payload = contentType.includes("application/json")
      ? await response.json()
      : { detail: await response.text() };

    if (!response.ok) {
      throw new Error(payload.detail || "No se pudo responder.");
    }

    typingMessage.remove();
    appendMessage("assistant", payload.answer, payload.sources);
    history.push({ role: "assistant", content: payload.answer });
  } catch (error) {
    typingMessage.remove();
    appendMessage("assistant", error.message);
  } finally {
    sendButton.disabled = false;
    sendButton.textContent = "Enviar";
    input.focus();
  }
});
