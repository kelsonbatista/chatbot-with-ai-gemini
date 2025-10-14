import os
from google import genai
from google.genai import types
from google.genai.errors import ClientError
import gradio
from dotenv import load_dotenv
import time
from home_assistant_commands import set_light_values, intruder_alert, start_music, good_morning

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
model = "gemini-2.0-flash"

client = genai.Client(api_key=GOOGLE_API_KEY)

initial_prompt = (
	"Você é um assistente virtual capaz e processar arquivos como iamgens, textos e outros tipos."
	"Sempre que alguém perguntar sobre o arquivo, verifique o histórico para encontrar o arquivo correspondente que essa pessoa já enviou."
	"Não diga que não é capaz de processar arquivos pois você é."
	"Fale sempre em portguês."
	"Você é capaz de executar comandos para controlar dispositivos domésticos, como luzes, músicas e segurança, além de uma função de bom dia. Suas funções são apenas essas."
	"Não se esqueça de fato chamar as funções quando for o caso."
)

config = types.GenerateContentConfig(
	system_instruction=initial_prompt,
	tools=[set_light_values, intruder_alert, start_music, good_morning]
)

chat = client.chats.create(model=model, config=config)
#Essa função ja preserva o historico da conversa

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
	uploaded_files = upload_files(message)
	prompt = [text]
	prompt.extend(uploaded_files)

	return prompt


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

chat_interface = gradio.ChatInterface(gradio_wrapper, type="messages", title="My Chatbot", theme='Taithrah/Minimal', multimodal=True)
chat_interface.launch(share=False)
