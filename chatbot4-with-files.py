import os

import google.generativeai as genai
import gradio
import time
from google.api_core.exceptions import InvalidArgument

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

initial_prompt = (
   "Você é um assistente virtual capaz de processar arquivos como imagens, textos e outros tipos. "
   "Sempre que alguém perguntar sobre um arquivo, verifique o histórico para encontrar o arquivo correspondente. "
   "Não diga que não é capaz de processar arquivos, pois você é."
)

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=initial_prompt)

chat = model.start_chat()

def error_handling(e):
  response = chat.send_message(
    f"O usuário te usando te deu um arquivo para você ler e obteve o erro: {e}."
    "Explique o que houve e dizer quais tipos de arquivo você suporta."
    "Assuma que a pessoa não saiba programação e que não quer ver o erro técnico original."
    "Explique de forma simples e concisa"
  )
  return response.text

def upload_files(files):
  uploaded_files = []
  
  if (files):
    for file in files:
      try:
        uploaded_file = genai.upload_file(file)
      except Exception as e:
        error_handling(e)
      
      while uploaded_file.state.name == "PROCESSING": # aguarda o arquivo ser processado
        time.sleep(3)
        uploaded_file = genai.get_file(uploaded_file.name)
        
      uploaded_files.append(uploaded_file)
      return uploaded_files

def gradio_wrapper(message, _history):
  text = message["text"]  
  files = message["files"]
  uploaded_files = upload_files(files) if files else None
  prompt = [text]
  prompt.extend(uploaded_files)
  
  try:
    response = chat.send_message(prompt)
  except InvalidArgument as e:
    response = error_handling(e)

  return response.text

chatInterface = gradio.ChatInterface(fn=gradio_wrapper, multimodal=True, title="Chatbot com suporte a arquivos")
chatInterface.launch()
