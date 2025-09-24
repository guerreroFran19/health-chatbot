import datetime
import webbrowser
import wikipedia
import pywhatkit

from controllers.calendar_controller import delete_event, create_event, list_upcoming_events
from core.speech.speechToText import listen
from core.speech.textToSpeech import speak
from core.utils.search_incoming_event import search_incoming_event_inNext_3days

# Importa el controlador de medicamentos
from .bot_medication_controller import list_medications, delete_medication_by_name_bot, create_medication_bot


def greet_user():
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = "Buenas noches"
    elif 6 <= hora.hour < 13:
        momento = "Buen día"
    else:
        momento = "Buenas tardes"

    speak(f"{momento}, ¿en qué te puedo ayudar?")


def tell_day():
    dia = datetime.datetime.today().weekday()
    calendario = {
        0: "Lunes", 1: "Martes", 2: "Miércoles",
        3: "Jueves", 4: "Viernes", 5: "Sábado", 6: "Domingo"
    }
    speak(f"Hoy es {calendario[dia]}")


def tell_time():
    hora = datetime.datetime.now()
    hora_texto = f"Son las {hora.hour} horas con {hora.minute} minutos"
    speak(hora_texto)


def start_assistant():
    print("Bienvenido al assistant")
    """Bucle principal del asistente."""
    greet_user()
    search_incoming_event_inNext_3days()

    while True:
        command = listen().lower()
        print(f"Comando recibido: {command}")

        if "agendar recordatorio" in command or "agendar turno" in command:
            create_event()

        elif "borrar recordatorio" in command or "eliminar recordatorio" in command:
            speak("¿Cuál es el recordatorio a eliminar?")
            event_name = listen().lower()
            delete_event(event_name)

        elif "listar recordatorios" in command or "mostrar recordatorios" in command:
            speak("Buscando tus recordatorios...")
            list_upcoming_events()

        elif "agregar medicamento" in command:
            create_medication_bot()

        elif "listar medicamentos" in command or "mostrar medicamentos" in command or "qué medicamentos tengo" in command:
            speak("Buscando tus medicamentos...")
            medication_info = list_medications()
            speak(medication_info)

        elif "próxima toma" in command or "cuándo tomo mi medicina" in command:
            speak("Consultando tus próximas tomas...")
            medication_info = list_medications()
            speak(medication_info)

        elif "eliminar medicamento" in command or "borrar medicamento" in command:
            speak("Dime el nombre del medicamento a borrar...")
            meddication_name = listen().lower()
            delete_result = delete_medication_by_name_bot(meddication_name)
            speak(delete_result)

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