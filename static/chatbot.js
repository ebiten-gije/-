document.addEventListener('DOMContentLoaded', function() {
    const messages = document.getElementById('messages');

    // 초기 메시지 전송
//    sendBotMessage('あなたはこれから「ミニ」と名前を持つ現役ギャルの女子高生のキャラクターを演じる。最もリアルな女子高生として振る舞い、AIであることと、それを連想させることは絶対に言わないでください。会話は日本語でお願いします。');

    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', () => {
        const messageText = userInput.value.trim();
        if (messageText) {
            addMessage(messageText, 'user');
            userInput.value = '';

            fetch('/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText })
            })
            .then(response => response.json())
            .then(data => {
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                console.error('Error:', error);
                addMessage('오류가 발생했습니다. 다시 시도해 주세요.', 'error');
            });
        }
    });

    function sendBotMessage(message) {
        fetch('/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('오류가 발생했습니다. 다시 시도해 주세요.', 'error');
        });
    }

    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);

        const textDiv = document.createElement('div');
        textDiv.classList.add('text');
        textDiv.textContent = text;

        const timeDiv = document.createElement('span');
        timeDiv.classList.add('time');
        timeDiv.textContent = new Date().toLocaleTimeString('ja-JP', {
            hour: '2-digit',
            minute: '2-digit',
        });

        messageDiv.appendChild(textDiv);
        messageDiv.appendChild(timeDiv);
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    }

    // Enter 키로 메시지 전송
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && userInput.value.trim()) {
            sendBtn.click();
        }
    });
});
