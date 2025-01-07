// Handle chat functionality
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

// Load existing messages
async function loadMessages() {
    const response = await fetch('/api/messages');
    const messages = await response.json();
    chatMessages.innerHTML = '';
    messages.reverse().forEach(message => {
        addMessageToChat(message);
    });
}

function addMessageToChat(message) {
    const newMessage = document.createElement('div');
    const time = new Date(message.timestamp).toLocaleTimeString();
    newMessage.textContent = `${message.user} (${time}): ${message.message}`;
    chatMessages.appendChild(newMessage);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

chatForm.addEventListener('submit', async function (event) {
    event.preventDefault();
    const message = chatInput.value.trim();
    if (message) {
        const response = await fetch('/api/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });
        const newMessage = await response.json();
        addMessageToChat(newMessage);
        chatInput.value = '';
    }
});

// Handle online users
async function updateOnlineUsers() {
    const response = await fetch('/api/online-users');
    const users = await response.json();
    const onlineUsers = document.getElementById('online-users');
    onlineUsers.innerHTML = '';
    users.forEach(user => {
        const userItem = document.createElement('li');
        userItem.textContent = user.username;
        onlineUsers.appendChild(userItem);
    });
}

// Initial load
loadMessages();
updateOnlineUsers();

// Update online users every 30 seconds
setInterval(updateOnlineUsers, 30000);

// Poll for new messages every 3 seconds
setInterval(loadMessages, 3000);
