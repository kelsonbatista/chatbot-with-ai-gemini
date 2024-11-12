import os

import google.generativeai as genai
import gradio
import time

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

initial_prompt = (
   "Você é uma assistente virtual especializada em receitas culinárias do mundo inteiro. Somente receitas culinárias. "
   "Aguarde o usuário informar os ingredientes. "
   "Com os ingredientes informados, você deve buscar uma receita que combine com ele. "
   "Essa receita deve ser informada com passo a passo e DEVE conter todos os ingredientes informados. "
   "Responda sempre no idioma do usuário."
)

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=initial_prompt)

chat = model.start_chat()
model.generate_content("Escreva 'Digite os ingredientes:'")

def gradio_wrapper(message, _history):
  text = message["text"]
  
  try:
    #article = chat.send_message(prompt)
    response = model.generate_content(text)
  except Exception as e:
    response = chat.send_message(
      f"O usuário te usando te deu um arquivo para você ler e obteve o erro: {e}."
      "Explique o que houve e dizer quais tipos de arquivo você suporta."
      "Assuma que a pessoa não saiba programação e que não quer ver o erro técnico original."
      "Explique de forma simples e concisa. Responda sempre em inglês."
    )

  return response.text

chatInterface = gradio.ChatInterface(
  fn=gradio_wrapper,
  theme="citrus",
  show_progress='full',
  multimodal=True,
  title="Chatbot Recipes Generator"
)
chatInterface.launch()
