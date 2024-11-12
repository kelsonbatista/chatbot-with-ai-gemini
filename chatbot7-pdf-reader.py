import os

import google.generativeai as genai
import gradio
import time
from pypdf import PdfReader

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)

initial_prompt = (
   "Você é uma assistente virtual especializada em resumir  textos de arquivos PDF. Somente PDF. "
   "Se o usuário solicitar algo, não responda. Apenas resuma o texto."
   "Responda sempre em inglês. Nunca use outro idioma para responder."
)

model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=initial_prompt)

chat = model.start_chat()

def gradio_wrapper(message, _history):
  text = message["text"]
  files = message["files"]
  read_text = ""
  uploaded_files = []

  if(files):
    for file in files:
      _name, ext = os.path.splitext(file)

      if ext not in [".pdf"]:
        response = chat.send_message("Responda que apenas aquivos pdf são suportados")
        return response.text
      
      reader = PdfReader(file)
      
      for page in reader.pages:
        read_text += page.extract_text()

  prompt = [text]
  prompt.extend(read_text)
  
  try:
    #article = chat.send_message(prompt)
    article = model.generate_content(prompt)
    
    with open("article.txt", "w") as f:
      f.write(article.text)
      response = chat.send_message("Responda que o artigo foi resumido com sucesso e que vc salvou em um arquivo chamado article.txt")
  except Exception as e:
    response = chat.send_message(
      f"O usuário te usando te deu um arquivo para você ler e obteve o erro: {e}."
      "Explique o que houve e dizer quais tipos de arquivo você suporta."
      "Assuma que a pessoa não saiba programação e que não quer ver o erro técnico original."
      "Explique de forma simples e concisa. Responda sempre em inglês."
    )

  return response.text

chatInterface = gradio.ChatInterface(fn=gradio_wrapper, theme="citrus", multimodal=True, title="Chatbot Article Summarizer")
chatInterface.launch()
