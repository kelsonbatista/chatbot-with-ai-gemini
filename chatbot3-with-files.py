import os

import google.generativeai as genai
import gradio

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat()

# chat.send_message("Você é um consultor de projetos. Se limite a responder coisas somente sobre o projeto.")

chat.send_message("Você é uma IA generativa capaz de processar textos e diversos tipos de arquivos. Sempre que uma pessoa te perguntar sobre um arquivo, verifique seu historico para ver se algum dos arquivos que você recebeu da pessoa bate com o pedido dela. Não diga que você não é capaz de processar imagens, textos ou outros tipos de arquivos, pois você é capaz sim. Nunca inicie uma conversa, aguarde uma mensagem do usuario.")

def gradio_wrapper(message, _history):
  # import pdb; pdb.set_trace() # debugging de python - ele para nessa linha para analisar
  text = message["text"]
  uploaded_files = []
  
  if (message["files"]):
    for file in message["files"]:
      uploaded_file = genai.upload_file(file)
      # import pdb; pdb.set_trace()
      uploaded_files.append(uploaded_file)
  
  prompt = [text]
  prompt.extend(uploaded_files)
  
  response = chat.send_message(prompt)
  return response.text

chatInterface = gradio.ChatInterface(fn=gradio_wrapper, multimodal=True, title="Chatbot com suporte a arquivos")
chatInterface.launch()
