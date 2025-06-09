const chatWindow = document.getElementById('chat-window');
const input = document.getElementById('user-input');

function addMessage(text, className, isBot = false) {
    const wrapper = document.createElement('div');
    wrapper.className = 'message-wrapper ' + (isBot ? 'bot' : 'user');

    if (isBot) {
        const avatar = document.createElement('img');
        avatar.className = 'bot-avatar';
        avatar.src = 'https://i.pinimg.com/236x/9e/c4/a5/9ec4a54f57a449e2442dee76f35109d5.jpg';
        avatar.alt = 'Bot Avatar';
        wrapper.appendChild(avatar);
    }

    const msg = document.createElement('div');
    msg.className = 'message ' + (isBot ? 'bot-message' : 'user-message');
    msg.textContent = text;

    wrapper.appendChild(msg);
    chatWindow.appendChild(wrapper);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, 'user', false);
    input.value = "";

    try {
        const formData = new FormData();
        formData.append('message', message);

        const res = await fetch('/chatbot/chat/', {
            method: 'POST',
            body: formData
        });

        if (!res.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await res.json();
        addMessage(data.response, 'bot', true);
    } catch (err) {
        addMessage("Error connecting to server. Please try again.", 'bot', true);
        console.error('Error:', err);
    }
}

function handleKey(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}