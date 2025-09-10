import datetime
import webbrowser
import wikipedia
import pywhatkit

from core.speech.speechToText import listen
from core.speech.textToSpeech import speak
from services.calendar_service import GoogleCalendarManager
from core.utils.parse_natural_time import parse_natural_datetime


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
    calendar = GoogleCalendarManager()

    while True:
        command = listen().lower()
        print(f"Comando recibido: {command}")

        if "agendar recordatorio" in command:
            try:
                speak("¿Cuál es el nombre del recordatorio?")
                reminder_name = listen().lower()

                speak("¿Para qué fecha y hora? Por ejemplo: hoy a las 3 de la tarde")
                reminder_time_text = listen().lower()

                start_time, end_time, timezone = parse_natural_datetime(reminder_time_text)

                success = calendar.create_event(
                    summary=reminder_name,
                    start_time=start_time,
                    end_time=end_time,
                    timezone=timezone,
                    attendees=None
                )

                if success == true:
                    speak(f"Recordatorio '{reminder_name}' agendado exitosamente")
                else:
                    speak("No pude guardar el recordatorio. Intenta de nuevo")
            except Exception as e:
                speak(f"Error en el recordatorio: {e}")
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

        elif "adiós" in command or "hasta luego" in command:
            speak("Nos vemos, que tengas un buen día.")
            break

        else:
            speak("No entendí bien, ¿podrías repetirlo?")
