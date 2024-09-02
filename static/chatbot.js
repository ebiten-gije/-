document.addEventListener('DOMContentLoaded', function() {
    const messages = document.getElementById('messages');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const fileInput = document.getElementById('file-input');

    // 초기 메시지 전송
//    sendBotMessage('あなたはこれから「ミニ」と名前を持つ現役ギャルの女子高生のキャラクターを演じる。最もリアルな女子高生として振る舞い、AIであることと、それを連想させることは絶対に言わないでください。会話は日本語でお願いします。');

    // 메시지 전송하는 함수
    sendBtn.addEventListener('click', () => {
        const messageText = userInput.value.trim();
        if (messageText) {
            addMessage(messageText, 'user');
            userInput.value = '';

            addLoadingSpinner();

            fetch('/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: messageText })
            })
            .then(response => response.json())
            .then(data => {
                removeLoadingSpinner();
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                removeLoadingSpinner();
                console.error('Error:', error);
                addMessage('오류가 발생했습니다. 다시 시도해 주세요.', 'error');
            });
        }
    });

    // 사진 업로드 함수
    fileInput.addEventListener('change', () => {
        const file = fileInput.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgSrc = e.target.result;
                addImage(imgSrc, 'user');

                const formData = new FormData();
                formData.append('image', file);

                addLoadingSpinner();

                fetch('/upload_image', {
                    method: 'POST',
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    removeLoadingSpinner();
                    addMessage(data.response, 'bot');
                })
                .catch(error => {
                    removeLoadingSpinner();
                    console.error('Error:', error);
                    addMessage('오류가 발생했습니다. 다시 시도해 주세요.', 'error');
                });
            };
            reader.readAsDataURL(file);  // 이미지를 DataURL로 읽기
        }
    });

//    function sendBotMessage(message) {
//        fetch('/message', {
//            method: 'POST',
//            headers: { 'Content-Type': 'application/json' },
//            body: JSON.stringify({ message: message })
//        })
//        .then(response => response.json())
//        .then(data => {
//            addMessage(data.response, 'bot');
//        })
//        .catch(error => {
//            console.error('Error:', error);
//            addMessage('오류가 발생했습니다. 다시 시도해 주세요.', 'error');
//        });
//    }

    // 채팅창에 메시지 표시
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

    // 채팅창에 이미지 표시
    function addImage(imgSrc, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);

        const imgElement = document.createElement('img');
        imgElement.src = imgSrc;
        imgElement.style.maxWidth = '100%';  // 이미지가 박스 크기를 넘지 않도록 조정
        imgElement.style.borderRadius = '10px';

        const timeDiv = document.createElement('span');
        timeDiv.classList.add('time');
        timeDiv.textContent = new Date().toLocaleTimeString('ja-JP', {
            hour: '2-digit',
            minute: '2-digit',
        });

        messageDiv.appendChild(imgElement);
        messageDiv.appendChild(timeDiv);
        messages.appendChild(messageDiv);
        messages.scrollTop = messages.scrollHeight;
    }

    // 로딩 표시
    function addLoadingSpinner() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'bot-message');
        loadingDiv.id = 'loading-spinner';

        const spinner = document.createElement('div');
        spinner.classList.add('loading-spinner');

        loadingDiv.appendChild(spinner);
        messages.appendChild(loadingDiv);
        messages.scrollTop = messages.scrollHeight;
    }

    // 로딩 지우기
    function removeLoadingSpinner() {
        const loadingDiv = document.getElementById('loading-spinner');
        if (loadingDiv) {
            loadingDiv.remove();
        }
    }

    // Enter 키로 메시지 전송
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && userInput.value.trim()) {
            sendBtn.click();
        }
    });
});
