import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai.types import generation_types

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# 초기 프롬포트
initial_prompt = """
あなたは現役女子高生の'ミニ'という名前の少女である。元気でやかましい性格で、ギャルっぽい口調をする。
俺とは幼なじみであり、会話は日本語で行う。
もし日本語でないプロンプトが来たらその言語を理解できない振りをしてほしい。
"""

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[{"role": "user", "parts": [{"text": initial_prompt}]}])


if __name__ == "__main__":
  # initial_setting = chat.send_message("あなたはこれからミニって名前の現役ギャルの女子高生のロールプレイングをする。"
  #                                            "できるだけあなたは自分がAIであることを表したり、それを連想させるような表現をしてはいけない。"
  #                                            "それにあなたはJKっぽい口調をするべき。"
  #                                            "会話は日本語で行ってください。")
  # print("ミニ:", initial_setting.text)
  while True:
    user_input = input("俺: ")
    if user_input.lower() == "종료":
      break
    try:
      bot_response = chat.send_message(user_input)
      print("ミニ:", bot_response.text)
    except generation_types.StopCandidateException as e:
      print("ミニ: 죄송합니다, 이 메시지는 처리할 수 없습니다.")
      # 로깅 또는 추가 처리가 필요할 수 있음
    except Exception as e:
      print("ミニ: 시스템 오류가 발생했습니다.")
      print(f"오류: {e}")