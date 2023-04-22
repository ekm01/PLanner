#!/home/binotto/.virtualenvs/googleapi_venv/bin/python3

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, time, timedelta
import pytz
import sys


def getCalendar(secretsPath, timezone, choice):
    # defines how to access the user's api
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']

    # authentication of the user and fetching the creds
    flow = InstalledAppFlow.from_client_secrets_file(secretsPath, scopes)
    creds = flow.run_local_server(port=0)

    # create an instance of a google api client
    cal = build('calendar', 'v3', credentials=creds)

    tz = pytz.timezone(timezone)

    # setting the start and end time
    # default start and end time which is today
    today = datetime.today()
    print(today)
    start = datetime.combine(today, time.min).astimezone(tz)
    end = start + timedelta(days=1)

    if choice == 'rest':
        end += timedelta(days=6-today.date().weekday())
    elif choice == 'week':
        start -= timedelta(days=today.date().weekday())
        end += timedelta(days=6-today.date().weekday())
    elif choice == 'nextweek':
        start -= timedelta(days=today.date().weekday())
        start += timedelta(days=7)
        end = start + timedelta(days=7)

    # fetching the events
    events = cal.events().list(calendarId='ekm7p8j@gmail.com',
                               timeMin=start.isoformat(),
                               timeMax=end.isoformat(),
                               singleEvents=True,
                               timeZone=timezone,
                               orderBy='startTime').execute()

    # getting a list of events
    return events.get('items', [])


def printEvents(events):
    if not events:
        print("No events found.")
    else:
        for i in range(0, len(events)):
            event_start = events[i]['start'].get('dateTime', events[i]['start'].get('date'))
            event_start = datetime.fromisoformat(event_start).strftime('%I:%M %p')
            print(str(i + 1) + '. ' + events[i]['summary'] + " at " + event_start)


# getting the program arguments
args = sys.argv
events = getCalendar('client_secret.json', args[1], args[2])
printEvents(events)
