// Handle chat functionality
const chatForm = document.getElementById('chat-form');
const chatInput = document.getElementById('chat-input');
const chatMessages = document.getElementById('chat-messages');

chatForm.addEventListener('submit', function (event) {
  event.preventDefault();

  const message = chatInput.value.trim();
  if (message) {
    // Simulate adding a message
    const newMessage = document.createElement('div');
    newMessage.textContent = `You: ${message}`;
    chatMessages.appendChild(newMessage);

    // Scroll to the bottom of the chat box
    chatMessages.scrollTop = chatMessages.scrollHeight;

    // Clear input field
    chatInput.value = '';
  }
});

// Simulate adding online users
const onlineUsers = document.getElementById('online-users');
const sampleUsers = ['Alice', 'Bob', 'Charlie', 'Diana'];

sampleUsers.forEach((user) => {
  const userItem = document.createElement('li');
  userItem.textContent = user;
  onlineUsers.appendChild(userItem);
});
