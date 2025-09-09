import wikipedia
from core.speech.textToSpeech import speak

def buscar_wikipedia(tema: str):
    wikipedia.set_lang("es")
    try:
        resultado = wikipedia.summary(tema, sentences=1)
        speak("Encontré esta información en Wikipedia")
        speak(resultado)
    except:
        speak("No encontré nada en Wikipedia sobre ese tema")
