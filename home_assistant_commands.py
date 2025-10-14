# Precisa tipar todas os parametros e funcoes para a IA gnerativa entender
# Essa tipagem tem que ser a mais simples possivel

def set_light_values(brightness: int, color_temp: str) -> dict:
	print("Modificou as luzes")
	return {
		"brightness": brightness,
		"colorTemperature": color_temp
	}

def intruder_alert() -> bool:
	print("Intruder alert!")
	return True

def start_music(energetic: bool, loud: bool, bpm: int) -> str:
	print(f"Música tocando! {energetic=} {loud=} {bpm=}")

def good_morning() -> bool:
	print("Good morning!")

# export this file as a module
__all__ = ["set_light_values", "intruder_alert", "start_music", "good_morning"]
