const chatWindow = document.getElementById('chat-window');
const input = document.getElementById('user-input');
const placeholder = document.getElementById('chat-placeholder');

// Add a message to the chat window
function addMessage(message, sender, isBot) {
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper ' + (isBot ? 'bot' : 'user');

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    if (isBot) {
        messageContent.innerHTML = DOMPurify.sanitize(marked.parse(message));
    } else {
        messageContent.textContent = message;
    }
    
    messageDiv.appendChild(messageContent);
    messageWrapper.appendChild(messageDiv);
    chatWindow.appendChild(messageWrapper);
    
    // Scroll to bottom
    chatWindow.scrollTop = chatWindow.scrollHeight;
    
    // Hide placeholder if it exists
    if (placeholder) {
        placeholder.style.display = 'none';
    }
}

// Show typing indicator
function showTypingIndicator() {
    const messageWrapper = document.createElement('div');
    messageWrapper.className = 'message-wrapper';

    const indicator = document.createElement('div');
    indicator.className = 'message bot-message typing-indicator';
    indicator.innerHTML = '<div class="message-content">Typing...</div>';
    
    messageWrapper.appendChild(indicator);
    chatWindow.appendChild(messageWrapper);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

// Remove typing indicator
function removeTypingIndicator() {
    const indicator = document.querySelector('.typing-indicator');
    if (indicator) {
        indicator.parentElement.remove(); // Remove the wrapper as well
    }
}

// Handle Enter key press
function handleKey(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Sending a message
async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, 'user', false);
    input.value = "";

    showTypingIndicator();

    try {
        const formData = new FormData();
        formData.append('message', message);

        const res = await fetch('/chatbot/general/chat/', {
            method: 'POST',
            body: formData
        });

        removeTypingIndicator();

        if (!res.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await res.json();
        addMessage(data.response, 'bot', true);
    } catch (err) {
        removeTypingIndicator();
        addMessage("Error connecting to server. Please try again.", 'bot', true);
        console.error('Error:', err);
    }
} 