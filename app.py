"""
title: 'update-f1-calendar'
author: 'Elias Albuquerque'
version: 'Python 3.12.0'
created: '2024-05-03'
update: '2024-05-03'
"""


import os.path
import re

from datetime import datetime, time
from decouple import config
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]
SCOPES = ["https://www.googleapis.com/auth/calendar"]
FORMULA1 = config('FORMULA1')


def delete_practice_events(service, events):
    """This function deletes all practice events from a list of events using 
    the Google Calendar API.
    
    It iterates over each event in the list of events and does the following:
    - Checks if the event summary contains the word 'Practice'. It does this 
    using a regular expression that matches '- Practice'.
    - If the event is a practice event, it calls the Google Calendar API to 
    delete the event.
    
    After deleting a practice event, it prints a message indicating that the 
    event has been deleted.
    """

    for event in events:
        summary = event["summary"]

        # Check if the event is a practice event
        match = re.search(r'- Practice', summary)

        # If it's a practice event, delete it
        if match:
            service.events().delete(
                calendarId=FORMULA1,
                eventId=event['id']
            ).execute()
            prints('- "Practice" events have been deleted')


def update_events(service, events):
    """This function updates the summary, description, and notifications of a 
    list of events using the Google Calendar API.
    
    It first creates a dictionary of locations mapping from a key to a location 
    name.
    
    Then, for each event in the list of events, it does the following:
    - Finds the location in the event summary using the locations dictionary.
    - Replaces the event summary with a new summary that includes the location 
    name. It uses the current year in the new summary.
    - Sets the event description to an empty string.
    - Checks the start time of the event. If the start time is between 11pm and 
    6am, it removes the event notifications.
    
    After updating the event summary, description, and notifications, it calls 
    the Google Calendar API to update the event.
    
    Finally, it prints a message indicating that the event summary, 
    description, and notifications have been updated.
    """

    locations = {
        "BAHRAIN": "Bahrain",
        "SAUDI ARABIAN": "Arábia Saudita",
        "AUSTRALIAN": "Austrália",
        "JAPANESE": "Japão",
        "CHINESE": "China",
        "MIAMI": "Miami, EUA",
        "MADE IN ITALY E DELL'EMILIA-ROMAGNA": "Emilia-Romagna, Itália",
        "MONACO": "Mônaco",
        "CANADA": "Canadá",
        "ESPAÑA": "Espanha",
        "AUSTRIAN": "Áustria",
        "BRITISH": "Reino Unido",
        "HUNGARIAN": "Hungria",
        "BELGIAN": "Bélgica",
        "DUTCH": "Holanda",
        "D`ITALIA": "Itália",
        "AZERBAIJAN": "Azerbaijão",
        "SINGAPORE": "Singapura",
        "UNITED STATES": "Estados Unidos",
        "CIUDAD DE MÉXICO": "Cidade do México, México",
        "SÃO PAULO": "São Paulo, Brasil",
        "LAS VEGAS": "Las Vegas, EUA",
        "QATAR": "Qatar",
        "ABU DHABI": "Abu Dhabi, Emirados Árabes Unidos"
    }

    # Update the name of the events since the start of the year
    for event in events:
        summary = event["summary"]

        # Find the location in the text
        for key in locations:
            if key in summary:
                location = locations[key]
                break
        else:
            location = "Unknown location"

        # Replace the summary using regex
        current_year = datetime.now().year
        new_summary = re.sub(
            f'FORMULA 1 .* {current_year}', f'F1 {location}', summary)

        # Update the event summary and description
        event['summary'] = new_summary
        event['description'] = ''

        # Update de notifications between 11pm at 6pm
        start_time = datetime.fromisoformat(
            event["start"].get("dateTime")).time()

        # Check if the start time is between 23:00:00 and 06:00:00
        if time(23, 0) <= start_time or start_time <= time(6, 0):
            event['reminders'] = {'useDefault': False, 'overrides': []}

        updated_event = service.events().update(
            calendarId=FORMULA1,
            eventId=event['id'],
            body=event
        ).execute()

    print("- Updated event summary, description and notifications")


def print_events(service, events):
    """This function prints the start time and summary of a list of events. For 
    it to work, you must uncomment the code in: main() -> # print all events
    
    It iterates over each event in the list of events and does the following:
    - Retrieves the start time of the event.
    - Retrieves the summary of the event.
    - Prints the start time and summary.
    """

    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        summary = event["summary"]

        print(start, summary)


def main():
    """This function uses the Google Calendar API to interact with the user's 
    calendar.
    
    It first authenticates the user and obtains necessary credentials. If valid 
    credentials are not found, it prompts the user to log in and saves these 
    credentials for future use.
    
    Once authenticated, it calls the Google Calendar API to fetch events since 
    the start of the current year from a specific calendar (FORMULA1).
    
    It then checks each event to see if it's a practice event. If it is, it 
    deletes the event using the `delete_practice_events` function.
    
    After deleting practice events, it updates the summary and descriptions of 
    the remaining events using the `update_events` function.
    
    If there are no upcoming events found, it prints a message indicating this. 
    If an error occurs during the process, it catches the error and prints an 
    error message.
    """

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        # Call the Calendar API
        now = datetime.now()
        start_of_year = datetime(now.year, 1, 1).isoformat() + "Z"

        print("Getting the events since the start of the year...")
        events_result = (
            service.events()
            .list(
                calendarId=FORMULA1,
                timeMin=start_of_year,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        # Delete all practice events end update the summary and descriptions
        print("- Checking events to remove...")
        delete_practice_events(service, events)
        print("- Checking events to update...")
        update_events(service, events)

        # # print all events
        # print("- Checking events to print...")
        # print_events(service, events)

        if not events:
            print("No upcoming events found.")
            return

        print("\n")

    except HttpError as error:
        print(f"An error occurred: {error}\n")


if __name__ == "__main__":
    main()
