import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import logging

load_dotenv()

app = Flask(__name__)

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# Google Generative AI API 설정
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def message():
    user_input = request.json.get('message')
    try:
        # 사용자 메시지 전송 및 응답 받기
        try:
            bot_response = chat.send_message(user_input)
            return jsonify({'response': bot_response.text})
        except Exception as e:
            logging.error(f'Message handling error: {e}')
            return jsonify({'response': '메시지 처리 중 오류가 발생했습니다.'})
    except Exception as e:
        logging.error(f'General error: {e}')
        return jsonify({'response': '응답 처리 중 오류가 발생했습니다.'})
    return jsonify({'response': '잘못된 입력입니다.'})

if __name__ == '__main__':
    app.run(debug=True)
