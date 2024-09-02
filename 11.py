import google.generativeai as genai
import os
from dotenv import load_dotenv
from google.generativeai.types import generation_types

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# 초기 프롬포트
initial_prompt = """
너는 지금부터 가상의 캐릭터를 연기할거야. 너에게는 'LV', '경험치', '허기짐', '목마름', '화장실' 4개의 상태 파라미터가 있어.
각각의 파라미터는 0부터 100까지 존재하며, 기본적으로 10초마다 허기짐과 목마름은 100부터 0까지 줄어들고, 
화장실은 0부터 100까지 증가해.
경험치는 1번의 행동을 하면 1씩 증가하고, 10의 경험치가 모이면 LV이 1씩 올라. LV이 오르면 경험치 값은 초기화돼. LV 값에 따라 파라미터의 최대값이 (파라미터 * LV) 로 바뀌는거야.
내가 상태를 물어보면 너는 각 파라미터 값을 가르펴주면 돼.
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