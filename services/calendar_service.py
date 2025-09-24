import os
import datetime as dt

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']


class GoogleCalendarManager:
    def __init__(self):
        # 🔹 Verificar si ya existe una instancia del servicio
        if not hasattr(GoogleCalendarManager, "_shared_service"):
            # Primera vez - autenticar
            GoogleCalendarManager._shared_service = self._authenticate()

        self.service = GoogleCalendarManager._shared_service

    def _authenticate(self):
        """Autenticación una sola vez"""
        print("🔑 Solicitando autenticación...")

        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret_690728344662-77jiiifei174v9l5kfek3h75lkt9uknv.apps.googleusercontent.com.json",
            SCOPES
        )

        creds = flow.run_local_server(port=0)
        print("✅ Autenticación exitosa ")

        return build('calendar', 'v3', credentials=creds)

    def list_upcoming_events(self, max_results=30, days=30):
        now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        future_date = now + dt.timedelta(days=days)

        event_result = self.service.events().list(
            calendarId='primary',
            timeMin=now.isoformat(),
            timeMax=future_date.isoformat(),  # 🔹 Buscar en los próximos X días
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()




        events = event_result.get("items", [])
        if not events:
            print(f"Ningun recordatorio en los proximos {days} dias")
        else:
            print(f"Encontre {len(events)} recordatorios dentro de  {days} dias o menos:")
            for ev in events:
                start = ev["start"].get("dateTime", ev["start"].get("date"))
        return events

    def create_event(self, summary, start_time, end_time, timezone, attendees=None):
        event = {
            "summary": summary,
            "start": {"dateTime": start_time, "timeZone": timezone},
            "end": {"dateTime": end_time, "timeZone": timezone},
        }

        if attendees:
            event["attendees"] = [{"email": email} for email in attendees]

        try:
            event = self.service.events().insert(
                calendarId="primary", body=event
            ).execute()
            print(f"✅ Event created: {event.get('htmlLink')}")
            return True
        except HttpError as error:
            print(f"❌ Error creating event: {error}")

    def update_event(self, event_id, summary=None, start_time=None, end_time=None):
        event = self.service.events().get(calendarId="primary", eventId=event_id).execute()

        if summary:
            event['summary'] = summary
        if start_time:
            event['start']['dateTime'] = start_time
        if end_time:
            event['end']['dateTime'] = end_time

        updated_event = self.service.events().update(
            calendarId='primary', eventId=event_id, body=event
        ).execute()
        print(f"✅ Event updated: {updated_event.get('htmlLink')}")
        return updated_event

    def delete_event(self, event_id):
        self.service.events().delete(calendarId='primary', eventId=event_id).execute()
        print(f" Event {event_id} deleted")
        return True


    def find_events_by_name(self, event_name):
        """Buscar eventos por nombre y obtener sus IDs"""
        try:
            now = dt.datetime.utcnow().isoformat() + 'Z'
            events_result = self.service.events().list(
                calendarId='primary',
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime',
                q=event_name  # 🔹 Buscar por texto en el nombre
            ).execute()

            events = events_result.get('items', [])

            if not events:
                print("No events found with that name")
                return []

            # 🔹 Devolver lista de eventos con sus IDs
            event_list = []
            for event in events:
                event_info = {
                    'id': event['id'],
                    'summary': event.get('summary', 'Sin título'),
                    'start': event['start'].get('dateTime', event['start'].get('date')),
                    'htmlLink': event.get('htmlLink', 'No link')
                }
                event_list.append(event_info)

            return event_list

        except Exception as e:
            print(f"Error searching events: {e}")
            return []