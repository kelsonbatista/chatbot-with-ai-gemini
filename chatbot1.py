import os
#import google.generativeai as genai
from google import genai
from google.genai import types
import gradio
from dotenv import load_dotenv

#genai.configure(api_key=os.environ["GEMINI_API_KEY"])
#model = genai.GenerativeModel("gemini-1.5-flash")

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
model = "gemini-2.0-flash"

client = genai.Client(api_key=GOOGLE_API_KEY)

#chat = model.start_chat()

#response = chat.send_message("Hello, how are you?")

initial_prompt = "Você é um consultor de desenvolvimento de projetos."

config = types.GenerateContentConfig(system_instruction=initial_prompt)

chat = client.chats.create(model=model, config=config) #Essa função ja preserva o historico da conversa
#chat.send_message("Hello, how are you?")

def gradio_wrapper(message, _history):
	response = chat.send_message(message)
	return response.text


#theme = gradio.themes.Monochrome().set(mode="dark")

chat_interface = gradio.ChatInterface(gradio_wrapper, type="messages", title="My Chatbot", theme='Taithrah/Minimal')
chat_interface.launch(share=False)
#print(chat.text)
