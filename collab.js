// script.js
document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages");
    const chatForm = document.getElementById("chat-form");
    const chatInput = document.getElementById("chat-input");
    const onlineUsersList = document.getElementById("online-users");
  
    // Sample users and messages
    const users = ["Alice", "Bob", "Charlie"];
    const messages = [
      { user: "Alice", message: "Hello everyone!" },
      { user: "Bob", message: "Hi Alice, how are you?" }
    ];
  
    // Function to render messages
    const renderMessages = () => {
      chatMessages.innerHTML = "";
      messages.forEach((msg) => {
        const p = document.createElement("p");
        p.innerHTML = <strong>${msg.user}:</strong> ${msg.message};
        chatMessages.appendChild(p);
      });
      chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll
    };
  
    // Function to render online users
    const renderUsers = () => {
      onlineUsersList.innerHTML = "";
      users.forEach((user) => {
        const li = document.createElement("li");
        li.textContent = user;
        onlineUsersList.appendChild(li);
      });
    };
  
    // Add new message
    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const message = chatInput.value;
      messages.push({ user: "You", message });
      renderMessages();
      chatInput.value = ""; // Clear input
    });
  
    // Initial render
    renderMessages();
    renderUsers();
  });
  