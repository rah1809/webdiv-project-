function toggleMenu() {
    const menu = document.getElementById("menu");
    menu.style.left = menu.style.left === "0px" ? "-260px" : "0px";
}

function toggleChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.style.display = chatBox.style.display === "flex" ? "none" : "flex";
}

function sendMessage() {
    const input = document.getElementById("chat-input");
    const chatBody = document.getElementById("chat-body");

    if (input.value.trim() !== "") {
        const message = document.createElement("p");
        message.textContent = input.value;
        chatBody.appendChild(message);
        input.value = "";
        chatBody.scrollTop = chatBody.scrollHeight;
    }
}
