import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import base64
from email import message_from_bytes
import quopri
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
        print(creds.expired)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            #print(creds.refresh(Request()))
            #print(creds.expired())
            
        else:
            flow = InstalledAppFlow.from_client_secrets_file('path/to/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message

    except Exception as error:
        print(f'An error occurred: {error}')
        return None

def decode_body(body):
    # Decode base64 encoded body
    body_data = base64.urlsafe_b64decode(body.encode('UTF-8'))
    # Decode quoted-printable encoding
    body_data = quopri.decodestring(body_data).decode('utf-8')
    return body_data

def extract_message_contents(message):
    payload = message['payload']
    headers = payload['headers']
    subject = next((header['value'] for header in headers if header['name'] == 'Subject'), '')

    # Extract body
    if 'data' in payload['body']:
        body = payload['body']['data']
        body = decode_body(body)
        soup = BeautifulSoup(body, 'html.parser')
        body_text = soup.get_text()
        print(f'Subject: {subject}')
        print('Body:')
        print(body_text)

    # Extract attachments (if any)
    for part in payload['parts']:
        if 'filename' in part:
            filename = part['filename']
            print(filename)
            # data = part['body']['attachmentData']
            # file_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
            # with open(filename, 'wb') as f:
            #     f.write(file_data)
            # print(f'Attachment saved: {filename}')

def read_emails():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)
    user_id = 'me'
    subject = 'Dmarc'

    response = service.users().messages().list(userId=user_id, q=f'subject:{subject}').execute()
    messages = response.get('messages', [])
    print(response)

    if not messages:
        print('No messages found with the specified subject.')
    else:
        for message in messages:
            message_id = message['id']
            email_message = get_message(service, user_id, message_id)
            if email_message:
                extract_message_contents(email_message)

if __name__ == '__main__':
    read_emails();

