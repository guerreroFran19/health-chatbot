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
        self.service = self._authenticate()

    def _authenticate(self):
        # 🔹 Forzar siempre login: si existe token, se borra
        if os.path.exists('token.json'):
            os.remove('token.json')

        creds = None
        # Siempre pedimos login (no reusamos tokens viejos)
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret_690728344662-77jiiifei174v9l5kfek3h75lkt9uknv.apps.googleusercontent.com.json", SCOPES
        )
        creds = flow.run_local_server(port=0)

        # Guardamos token por la sesión actual (no se reusa al reiniciar el bot)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

        return build('calendar', 'v3', credentials=creds)

    def list_upcoming_events(self, max_results=10):
        now = dt.datetime.utcnow().replace(tzinfo=dt.timezone.utc)
        tomorrow = now + dt.timedelta(days=1)

        event_result = self.service.events().list(
            calendarId='primary',
            timeMin=now.isoformat(),
            timeMax=tomorrow.isoformat(),
            maxResults=max_results,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = event_result.get("items", [])
        if not events:
            print("No upcoming events found")
        else:
            for ev in events:
                start = ev["start"].get("dateTime", ev["start"].get("date"))
                print(start, ev.get("summary", "Sin título"))
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
