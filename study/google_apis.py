import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# If modifying these SCOPES, delete the file token.json.
GMAIL_SCOPES = ['https://www.googleapis.com/auth/gmail.send']
CALENDAR_SCOPES = ['https://www.googleapis.com/auth/calendar']
ALL_SCOPES = GMAIL_SCOPES + CALENDAR_SCOPES

def get_credentials():
    creds = None
    env_folder = os.getenv('ENV_FOLDER')
    creds_path = os.path.join(env_folder, 'token.json')
    credentials_path = os.path.join(env_folder, 'credentials.json')

    if os.path.exists(creds_path):
        creds = Credentials.from_authorized_user_file(creds_path, ALL_SCOPES)
        print("Found token.json, loading credentials...")
    else:
        print("token.json not found, initiating OAuth flow...")

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            print("Credentials expired, refreshing...")
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, ALL_SCOPES)
            creds = flow.run_local_server(port=0)
            print("OAuth flow completed, credentials obtained.")
        with open(creds_path, 'w') as token:
            token.write(creds.to_json())
            print("Credentials saved to token.json.")

    return creds

def get_gmail_service():
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    print("Gmail service built successfully.")
    return service

def get_calendar_service():
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)
    print("Calendar service built successfully.")
    return service

def send_email(user_email, subject, html_content):
    service = get_gmail_service()
    
    message = MIMEMultipart()
    message['to'] = user_email
    message['subject'] = subject
    message.attach(MIMEText(html_content, 'html'))
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw_message}
    
    try:
        message = service.users().messages().send(userId='me', body=message_body).execute()
        print('Message Id: %s' % message['id'])
        return message
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def create_calendar_event(summary, location, description, start_datetime, end_datetime, attendees_emails):
    service = get_calendar_service()
    
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'America/Los_Angeles',
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'America/Los_Angeles',
        },
        'attendees': [{'email': email} for email in attendees_emails],
        'conferenceData': {
            'createRequest': {
                'requestId': 'random-string',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
                'status': {
                    'statusCode': 'success'
                }
            }
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
        },
    }
    
    try:
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        print('Event created: %s' % (event.get('htmlLink')))
        print('Meet Link: %s' % (event['conferenceData']['entryPoints'][0]['uri']))
        return event
    except Exception as error:
        print(f'An error occurred: {error}')
        return None

# Example usage
if __name__ == '__main__':
    # Send an email
    send_email('nagasaroghislaine3@gmail.com', 'Test Subject', '<h1>Test HTML Content</h1>')

    # Create a calendar event with Google Meet link
    create_calendar_event(
        summary='Google Meet Event',
        location='Online',
        description='A chance to talk with friends.',
        start_datetime='2024-07-30T09:00:00-07:00',
        end_datetime='2024-07-30T10:00:00-07:00',
        attendees_emails=['attendee1@example.com', 'attendee2@example.com']
    )
