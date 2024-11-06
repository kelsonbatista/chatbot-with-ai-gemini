import os

import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat()

response = chat.send_message("Hello, how are you?")

print(response.text)
