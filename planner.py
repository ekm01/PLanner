#!/home/binotto/.virtualenvs/googleapi_venv/bin/python3

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime, time, timedelta
import pytz
import sys


class WrongArgumentException(Exception):
    pass


def printEvents(events, day):
    print('\n' + day + ':')
    if not events:
        print('No events found.')
    else:
        for i in range(0, len(events)):
            event_start = events[i]['start'].get('dateTime', events[i]['start'].get('date'))
            event_start = datetime.fromisoformat(event_start).strftime('%I:%M %p')
            print(str(i + 1) + '. ' + events[i]['summary'] + ' at ' + event_start)


def getCalendar(secretsPath, timezone, choice):
    tz = pytz.timezone(timezone)

    # setting the start time, end time is relative to start
    today = datetime.today()
    start = datetime.combine(today, time.min).astimezone(tz)
    loopEnd = 0

    if choice == 'rest':
        loopEnd = 7 - today.date().weekday()
    elif choice == 'week':
        start = start - timedelta(days=today.date().weekday())
        loopEnd = 7
    elif choice == 'nextweek':
        start = start + timedelta(days=7-today.date().weekday())
        loopEnd = 7
    elif choice == 'today':
        loopEnd = 1
    else:
        raise WrongArgumentException('Wrong input for the second parameter.')

    # defines how to access the user's api
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']

    # authentication of the user and fetching the creds
    flow = InstalledAppFlow.from_client_secrets_file(secretsPath, scopes)
    creds = flow.run_local_server(port=0)

    # create an instance of a google api client
    cal = build('calendar', 'v3', credentials=creds)

    # printing the events day by day
    for i in range(0, loopEnd):
        startl = start + timedelta(days=i)
        endl = startl + timedelta(days=1)

        # fetching the events
        events = cal.events().list(calendarId='ekm7p8j@gmail.com',
                                   timeMin=startl.isoformat(),
                                   timeMax=endl.isoformat(),
                                   singleEvents=True,
                                   timeZone=timezone,
                                   orderBy='startTime').execute()

        # getting a list of events
        events = events.get('items', [])
        printEvents(events, startl.strftime('%A, %d-%m-%Y'))


# getting the program arguments
def main():
    args = sys.argv

    if len(args) != 3:
        print('Invalid number of parameters: expected 2')
        sys.exit(1)

    try:
        getCalendar('client_secret.json', args[1], args[2])
    except WrongArgumentException as e:
        print(e)
        sys.exit(1)


main()
