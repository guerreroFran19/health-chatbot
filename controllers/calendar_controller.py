from core.utils.parse_natural_time import parse_natural_datetime
from services.calendar_service import GoogleCalendarManager
from core.speech.speechToText import listen
from core.speech.textToSpeech import speak

calendar = GoogleCalendarManager()

def list_upcoming_events():

    for days in [3, 7, 30]:
        events = calendar.list_upcoming_events(max_results=30, days=days)


        if events:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'Sin título')
                print(f"🔍 {start} - {summary}")
            break

    if not events:
        speak("No tengo recordatorios programados. ¿Quieres agregar uno?")
        choice = listen().lower()
        print(choice)
        try:
            if choice == "sí" :
                create_event()
            else:
                return
        except ValueError:
            speak("No entendí el número")
            return False
    else:
        speak(f"Encontré {len(events)} recordatorios:")
        for event in events:
            summary = event.get('summary', 'Recordatorio')
            speak(summary)

def create_event():
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

        if success:
            speak(f"Recordatorio '{reminder_name}' agendado exitosamente")
        else:
            speak("No pude guardar el recordatorio. Intenta de nuevo")
    except Exception as e:
        speak(f"Error en el recordatorio: {e}")


def delete_event(event_name):
    """Eliminar un evento por nombre"""
    calendar = GoogleCalendarManager()

    # 🔹 BUSCAR eventos por nombre
    events = calendar.find_events_by_name(event_name)

    if not events:
        speak(f"No encontré recordatorios con el nombre '{event_name}'")
        return False
    elif len(events) == 1:

        event_id = events[0]['id']
        if calendar.delete_event(event_id):
            speak(f"Recordatorio '{event_name}' eliminado exitosamente")
            return True
        else:
            speak("No pude eliminar el recordatorio")
            return False
    else:
        # Multiples eventos - mostrar opciones
        speak(f"Encontré {len(events)} recordatorios. ¿Cuál quieres eliminar?")
        for i, event in enumerate(events, 1):
            start_time = event['start'][:10]
            speak(f"Opción {i}: {event['summary']} del {start_time}")

        speak("Di el número del recordatorio a eliminar")
        choice = listen().lower()

        try:
            choice_num = int(choice) - 1
            if 0 <= choice_num < len(events):

                event_id = events[choice_num]['id']
                if calendar.delete_event(event_id):
                    speak("Recordatorio eliminado exitosamente")
                    return True
                else:
                    speak("No pude eliminar el recordatorio")
                    return False
            else:
                speak("Número inválido")
                return False
        except ValueError:
            speak("No entendí el número")
            return False
