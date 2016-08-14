from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

import time
import notification
# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_events(service):
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    eventsResult = service.events().list(
    calendarId='so7bnpop77r935i5upl92ium9o@group.calendar.google.com', timeMin=now, maxResults=10, singleEvents=True,
    orderBy='startTime').execute()
    events = eventsResult.get('items', [])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        #print(event)
        #print(start, event['summary'])
    return events
def notify(id_set, events, event_type):
    for e in id_set:
        for event in events:
            if event['id'] == e:
                description = 'From '
                if 'dateTime' in event['start']:
                    description += event['start']['dateTime'] + " to "
                else:
                    description += event['start']['date'] + " to "
                if 'dateTime' in event['end']:
                    description += event['end']['dateTime']
                else:
                    description += event['end']['date'] + " to "
                notification.notify("Event " + event_type, event['summary'], description, sound=True)

def compare_events(events1, events2):
    found = False
    id1 = set([e['id'] for e in events1])
    id2 = set([e['id'] for e in events2])
    deleted = id1.difference(id2)
    created = id2.difference(id1)
    notify(deleted, events1, "Deleted")
    notify(created, events2, "Created")

def main():
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    events = get_events(service)
    time.sleep(60)
    while(True):
        tmp = get_events(service)
        compare_events(events,tmp)
        time.sleep(60)
    # event = {
    #     'summary': 'Google I/O 2015',
    #       'location': '800 Howard St., San Francisco, CA 94103',
    #       'description': 'A chance to hear more about Google\'s developer products.',
    #       'start': {
    #         'dateTime': '2016-08-28T09:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #       },
    #       'end': {
    #         'dateTime': '2016-08-28T17:00:00-07:00',
    #         'timeZone': 'America/Los_Angeles',
    #       },
    #       'recurrence': [
    #         'RRULE:FREQ=DAILY;COUNT=2'
    #       ],
    #       'attendees': [
    #         {'email': 'lpage@example.com'},
    #         {'email': 'sbrin@example.com'},
    #       ],
    #       'reminders': {
    #         'useDefault': False,
    #         'overrides': [
    #           {'method': 'email', 'minutes': 24 * 60},
    #           {'method': 'popup', 'minutes': 10},
    #         ],
    #       },
    #       }

    # Creating a calendar event
    #event = service.events().insert(calendarId='primary', body=event).execute()
    #print ('Event created: %s' % (event.get('htmlLink')))

    # Getting the calendar list
    # page_token = None
    # while True:
    #     calendar_list = service.calendarList().list(pageToken=page_token).execute()
    #     for calendar_list_entry in calendar_list['items']:
    #         print(calendar_list_entry)
    #         print(calendar_list_entry['summary'])
    #     page_token = calendar_list.get('nextPageToken')
    #     if not page_token:
    #         break


if __name__ == '__main__':
    main()
