// script.js
document.addEventListener("DOMContentLoaded", () => {
    const projects = [
      { name: "AI in Healthcare", description: "Collaboration on healthcare solutions using AI." },
      { name: "Climate Change Analysis", description: "Studying the impacts of global warming." },
    ];
  
    const messages = [
      { user: "Alice", text: "Welcome to the group!" },
      { user: "Bob", text: "Thanks, Alice. Glad to be here." },
    ];
  
    const documents = [];
  
    const projectList = document.getElementById("group-projects");
    const messageForm = document.getElementById("message-form");
    const messageInput = document.getElementById("message-input");
    const messagesDiv = document.getElementById("messages");
    const documentForm = document.getElementById("document-form");
    const documentDiv = document.getElementById("documents");
  
    // Render group projects
    const renderProjects = () => {
      projectList.innerHTML = "";
      projects.forEach((project) => {
        const li = document.createElement("li");
        li.innerHTML = <strong>${project.name}</strong><p>${project.description}</p>;
        projectList.appendChild(li);
      });
    };
  
    // Render messages
    const renderMessages = () => {
      messagesDiv.innerHTML = "";
      messages.forEach((msg) => {
        const p = document.createElement("p");
        p.innerHTML = <strong>${msg.user}:</strong> ${msg.text};
        messagesDiv.appendChild(p);
      });
    };
  
    // Render documents
    const renderDocuments = () => {
      documentDiv.innerHTML = "";
      documents.forEach((doc) => {
        const a = document.createElement("a");
        a.href = doc.url;
        a.target = "_blank";
        a.textContent = doc.name;
        documentDiv.appendChild(a);
      });
    };
  
    // Add message
    messageForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const message = messageInput.value;
      messages.push({ user: "You", text: message });
      renderMessages();
      messageInput.value = "";
    });
  
    // Upload document
    documentForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const fileInput = document.getElementById("file-upload");
      const file = fileInput.files[0];
      if (file) {
        documents.push({ name: file.name, url: "#" });
        renderDocuments();
      }
      documentForm.reset();
    });
  
    // Initialize the page
    renderProjects();
    renderMessages();
    renderDocuments();
  });
  