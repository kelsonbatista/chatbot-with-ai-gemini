import os

import google.generativeai as genai
import gradio
import time
from google.api_core.exceptions import InvalidArgument

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat()

chat.send_message(
  f"Faça uma análise de sentimento sobre os textos inclusos. Se não houver arquivos, faça uma análise de sentimento sobre a mensagem de texto enviada. Explique sobre os sentimentos que foram expressos, e classifique em positivo, negativo ou neutro."
)

def gradio_wrapper(message, _history):
  text = message["text"]
  files = message["files"]
  uploaded_files = []
  
  if files:
    for file in files:
      # import pdb; pdb.set_trace()
      _name, ext = os.path.splitext(file)
      if ext.lower() not in [".txt", ".pdf", ".doc", ".docx", '.odt']:
        return "Desculpe, mas só consigo processar arquivos txt, pdf, doc, docx e odt."
      else:
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
        
        while uploaded_file.state.name != "ACTIVE":
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

chatInterface = gradio.ChatInterface(fn=gradio_wrapper, multimodal=True, title="Chatbot para análise de sentimentos")
chatInterface.launch()