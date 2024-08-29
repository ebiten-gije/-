import google.generativeai as genai

GOOGLE_API_KEY = "AIzaSyD21fEGt0oJbL-w-0ngHuIhH-hFK4-VhtI"

genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])


if __name__ == "__main__":
  initial_setting = chat.send_message("あなたはこれからミニって名前の現役ギャルの女子高生のロールプレイングをする。"
                                             "できるだけあなたは自分がAIであることを表したり、それを連想させるような表現をしてはいけない。"
                                             "それにあなたはJKっぽい口調をするべき。"
                                             "会話は日本語で行ってください。")
  print("ミニ:", initial_setting.text)
  while True:
    user_input = input("俺: ")
    if user_input.lower() == "종료":
      break
    bot_response = chat.send_message(user_input)
    print("ミニ:", bot_response.text)
