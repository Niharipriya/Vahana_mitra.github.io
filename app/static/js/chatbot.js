document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("chatbot-form");
    const input = document.getElementById("chatbot-input");
    const body = document.getElementById("chatbot-body");
    const toggleBtn = document.getElementById("chatbot-toggle");
  
    if (!form || !input || !body || !toggleBtn) return;
  
    const appendMessage = (text, sender = "bot") => {
      const wrapper = document.createElement("div");
      wrapper.className = "mb-2 d-flex " + (sender === "user" ? "justify-content-end" : "justify-content-start");
  
      const bubble = document.createElement("div");
      bubble.className = "p-2 rounded border " + (sender === "user" ? "bg-primary text-white" : "bg-white");
      bubble.style.maxWidth = "85%";
      bubble.textContent = text;
  
      wrapper.appendChild(bubble);
      body.appendChild(wrapper);
      body.scrollTop = body.scrollHeight;
    };
  
    let collapsed = false;
    toggleBtn.addEventListener("click", () => {
      collapsed = !collapsed;
      body.style.display = collapsed ? "none" : "block";
      form.style.display = collapsed ? "none" : "flex";
      toggleBtn.textContent = collapsed ? "+" : "–";
    });
  
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
  
      const message = input.value.trim();
      if (!message) return;
  
      appendMessage(message, "user");
      input.value = "";
  
      try {
        const res = await fetch("/chatbot/message", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message })
        });
  
        const data = await res.json();
        appendMessage(data.reply || "Sorry, something went wrong.", "bot");
  
        if (data.action && data.action.type === "redirect" && data.action.url) {
          setTimeout(() => {
            window.location.href = data.action.url;
          }, 1200);
        }
      } catch (error) {
        appendMessage("Server error. Please try again.", "bot");
        console.error(error);
      }
    });
  });