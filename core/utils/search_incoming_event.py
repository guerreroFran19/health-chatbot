from core.speech.textToSpeech import speak
from services.calendar_service import GoogleCalendarManager

calendar = GoogleCalendarManager()

def search_incoming_event_inNext_3days():
    for days in [3]:
        events = calendar.list_upcoming_events(max_results=30, days=days)

        if events:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                summary = event.get('summary', 'Sin título')
                print(f"🔍 {start} - {summary}")
            break

    if not events:
        speak("No tienes recordatorios dentro de los proximos 3 dias")
    else:
        speak("Tienes un proximo evento dentro de los 3 dias")
        for event in events:
            summary = event.get('summary', 'Recordatorio')
            speak(summary)