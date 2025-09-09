import pyttsx3

# Cambiá el ID según la voz que quieras (masculina/femenina/español)
ID_VOZ = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_ES-ES_HELENA_11.0"

def speak(mensaje: str):
    engine = pyttsx3.init()
    engine.setProperty("voice", ID_VOZ)
    engine.say(mensaje)
    engine.runAndWait()
