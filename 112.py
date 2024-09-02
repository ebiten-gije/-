import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import logging
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import torch


load_dotenv()

app = Flask(__name__)

processor = AutoImageProcessor.from_pretrained("jackie68/foodImageToText")
image_model = AutoModelForImageClassification.from_pretrained("jackie68/foodImageToText")

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

initial_prompt = """
あなたは現役女子高生の'ミニ'という名前の少女である。元気でかわいい性格で、最もリアルな女子高生として振る舞う。
友達のように話し、その関係性に適切な口調をしてほしい。できるだけ会話は日本語で行う。
もし日本語でないプロンプトが来たらその言語を理解できない振りをしてほしい。
"""

# Google Generative AI API 설정
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[{"role": "user", "parts": [{"text": initial_prompt}]}])


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


@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'response': '이미지가 첨부되지 않았습니다.'})

    image_file = request.files['image']
    image = Image.open(image_file.stream)

    # 이미지를 모델이 처리할 수 있는 형태로 변환
    inputs = processor(images=image, return_tensors="pt")

    # 모델을 통해 예측
    with torch.no_grad():
        outputs = image_model(**inputs)

    # 예측된 클래스 추출
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    label = image_model.config.id2label[predicted_class_idx]

    # 챗봇에게 이미지 인식 결과를 제공하여 응답 받기
    prompt = f"今{label}の写真をおくられたとして全力反応おねがい！"
    try:
        bot_response = chat.send_message(prompt)
        response_text = bot_response.text
    except Exception as e:
        logging.error(f'Message handling error: {e}')
        response_text = '메시지 처리 중 오류가 발생했습니다.'

    # 결과 반환
    return jsonify({'response': response_text})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
