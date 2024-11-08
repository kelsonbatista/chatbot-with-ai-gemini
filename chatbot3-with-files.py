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

#model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat()

# chat.send_message("Você é um consultor de projetos. Se limite a responder coisas somente sobre o projeto.")

# chat.send_message("Você é uma IA generativa capaz de processar textos e diversos tipos de arquivos. Sempre que uma pessoa te perguntar sobre um arquivo, verifique seu historico para ver se algum dos arquivos que você recebeu da pessoa bate com o pedido dela. Não diga que você não é capaz de processar imagens, textos ou outros tipos de arquivos, pois você é capaz sim. Nunca inicie uma conversa, aguarde uma mensagem do usuario.")

def gradio_wrapper(message, _history):
  # import pdb; pdb.set_trace() # debugging de python - ele para nessa linha para analisar
  text = message["text"]
  uploaded_files = []
  
  if (message["files"]):
    for file in message["files"]:
      try:
        uploaded_file = genai.upload_file(file)
      except Exception as e:
        response = chat.send_message(
          f"O usuário te usando te deu um arquivo para você ler e obteve o erro: {e}."
          "Explique o que houve e dizer quais tipos de arquivo você suporta."
          "Assuma que a pessoa não saiba programação e que não quer ver o erro técnico original."
          "Explique de forma simples e concisa"
        )
        return response.text
      #import pdb; pdb.set_trace()
      
      while uploaded_file.state.name == "PROCESSING": # aguarda o arquivo ser processado
        time.sleep(3)
        uploaded_file = genai.get_file(uploaded_file.name)
        
      uploaded_files.append(uploaded_file)
  
  prompt = [text]
  prompt.extend(uploaded_files)
  
  try:
    response = chat.send_message(prompt)
  except InvalidArgument as e:
    response = chat.send_message(
      f"O usuário te usando te deu um arquivo para você ler e obteve o erro: {e}."
      "Explique o que houve e dizer quais tipos de arquivo você suporta."
      "Assuma que a pessoa não saiba programação e que não quer ver o erro técnico original."
      "Explique de forma simples e concisa"
    )
    
  return response.text

chatInterface = gradio.ChatInterface(fn=gradio_wrapper, multimodal=True, title="Chatbot com suporte a arquivos")
chatInterface.launch()
