import os
from google import genai
from google.genai import types
from google.genai.errors import ClientError
import gradio
from dotenv import load_dotenv
import time
import mimetypes

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
model = "gemini-2.0-flash"

client = genai.Client(api_key=GOOGLE_API_KEY)

initial_prompt = "Você é especialista em analisar sentimentos a partir de um texto. Identifique se é positivo, negativo ou neutro."

config = types.GenerateContentConfig(system_instruction=initial_prompt)

chat = client.chats.create(model=model, config=config) #Essa função ja preserva o historico da conversa

def upload_files(message):
	uploaded_files = []
	for file_path in message['files']:
		try:
			uploaded_file = client.files.upload(file=file_path)
		except Exception as e:
			return [f"Erro ao ler o arquivo: {e}"]
		#import pdb; pdb.set_trace() #debug
		while uploaded_file.state.name == "PROCESSING": #aguarda o upload completo do arquivo
			time.sleep(5)
			uploaded_file = client.files.get(name=uploaded_file.name)
		uploaded_files.append(uploaded_file)
	return uploaded_files

def assemble_prompt(message):
	#import pdb; pdb.set_trace() #debug
	text = message['text']
	files = message['files']

	file_contents = []

	if files:
		#uploaded_files = upload_files(message)
		for file_path in files:
			#import pdb; pdb.set_trace()
			file_type, _ = mimetypes.guess_type(file_path)
			if (file_type == "text/plain"):
				with open (file_path, "r", encoding="utf-8") as f:
					content = f.read()
				file_contents.append(content)
			else:
				pass

	combined_text = text

	if files:
		#prompt.extend(uploaded_files)
		combined_text = text + "\n\n" + "\n\n".join(file_contents)

	return combined_text

def gradio_wrapper(message, _history):
	prompt = assemble_prompt(message)

	try:
		response = chat.send_message(prompt)
	except ClientError as e:
		response = chat.send_message(
			f"O usuário te usando te enviou uma mensagem e obteve o seguinte erro: {e}."
			"Pode explicar o que houve e dizer quais tipos de arquivos você dá suporte para?"
			"Assuma que a pessoa não sabe programação e não vai entender o erro original que " \
			"você recebeu. Explique para a pessoa como evitar o erro de forma muito simples e concisa."
		)

	return response.text

chat_interface = gradio.ChatInterface(fn=gradio_wrapper, type="messages", title="My Chatbot", theme='Taithrah/Minimal', multimodal=True)
chat_interface.launch(share=False)
