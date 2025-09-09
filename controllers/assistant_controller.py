import datetime
import webbrowser
import wikipedia
import pywhatkit
import pyjokes
import yfinance as yf

from core.speech.speechToText import listen
from core.speech.textToSpeech import speak


def greet_user():
    """Saludo inicial basado en la hora."""
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"

    speak(f"{momento}, ¿en qué te puedo ayudar?")


def tell_day():
    """Decir qué día es hoy."""
    dia = datetime.datetime.today().weekday()
    calendario = {
        0: "Lunes", 1: "Martes", 2: "Miércoles",
        3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    speak(f"Hoy es {calendario[dia]}")


def tell_time():
    """Decir la hora actual."""
    hora = datetime.datetime.now()
    hora_texto = f"Son las {hora.hour} horas con {hora.minute} minutos"
    speak(hora_texto)


def start_assistant():
    """Bucle principal del asistente."""
    greet_user()

    while True:
        command = listen().lower()
        print(f"Comando recibido: {command}")

        if "abrir youtube" in command:
            speak("Estoy abriendo YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "abrir navegador" in command:
            speak("Estoy abriendo el navegador")
            webbrowser.open("https://www.google.com")

        elif "qué día es" in command or "que día es" in command:
            tell_day()

        elif "qué hora es" in command or "que hora es" in command:
            tell_time()

        elif "busca en wikipedia" in command:
            topic = command.replace("busca en wikipedia", "").strip()
            wikipedia.set_lang("es")
            result = wikipedia.summary(topic, sentences=1)
            speak("Esto es lo que encontré en Wikipedia")
            speak(result)

        elif "busca en internet" in command:
            topic = command.replace("busca en internet", "").strip()
            pywhatkit.search(topic)
            speak("Esto es lo que encontré en Internet")

        elif "reproducir" in command:
            song = command.replace("reproducir", "").strip()
            pywhatkit.playonyt(song)
            speak("Reproduciendo en YouTube")

        elif "chiste" in command:
            joke = pyjokes.get_joke("es")
            speak(joke)

        elif "precio de la acción" in command:
            stock = command.split("de")[-1].strip().lower()
            cartera = {
                "apple": "AAPL", "amazon": "AMZN",
                "google": "GOOGL", "tesla": "TSLA"
            }
            try:
                ticker = yf.Ticker(cartera[stock])
                price = ticker.info['regularMarketPrice']
                speak(f"El precio de {stock} es {price} dólares.")
            except Exception:
                speak("Perdón, no pude encontrar esa acción.")

        elif "adiós" in command or "hasta luego" in command:
            speak("Nos vemos, que tengas un buen día.")
            break

        else:
            speak("No entendí bien, ¿podrías repetirlo?")
