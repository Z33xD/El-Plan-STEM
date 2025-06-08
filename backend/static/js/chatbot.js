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
        const res = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });

        const data = await res.json();
        addMessage(data.response, 'bot', true);
      } catch (err) {
        addMessage("Error connecting to server.", 'bot', true);
      }
    }

    function handleKey(event) {
      if (event.key === 'Enter') {
        sendMessage();
      }
    }