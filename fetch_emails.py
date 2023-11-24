import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
import psycopg2
import datetime

DB_NAME = os.environ.get('db_name', 'gmail_db')
DB_USER = os.environ.get('db_user', 'blend_user')
DB_PWD = os.environ.get(
    'db_pwd', 'blend_user')
DB_PORT = os.environ.get('db_port', '5432')
DB_HOST = os.environ.get('db_host', 'localhost')


DATABASE_CONNECTION = {
    'dbname': DB_NAME,
    'user': DB_USER,
    'password': DB_PWD,
    'host': DB_HOST,
    'port': DB_PORT
}
# Constants
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class FetchEmails:
    def authenticate_gmail_api(self):
        """
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        """
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json')    
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)    
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())    
        return creds

    def fetch_emails(self):
        """
        Used for fetching emails from gmail api
        """
        creds = self.authenticate_gmail_api()
        service = build('gmail', 'v1', credentials=creds)
        # Get a list of messages from the user's inbox
        results = service.users().messages().list(userId='me').execute()
        connection = psycopg2.connect(**DATABASE_CONNECTION)
        cursor = connection.cursor()
        # Fetches only 100 top messages present It will not fetch total messages
        #  It fetchs only top 100 messages 
        # we need to fetch messages based on page by getting the total numbers of messages present
        messages = results.get('messages', [])
        if messages:
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                msg_id = msg['id']
                subject, received_date, from_address  = '', '', ''
                for header in msg['payload']['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                    elif header['name'] == 'From':
                        from_address = header['value']
                    elif header['name'] == 'Date':
                        received_date = header["value"]
                        if ',' in header['value']:
                            received_date = header['value'].split(', ' )[1]
                        received_date = received_date.split(' ')
                        received_date = datetime.datetime.strptime(' '.join(received_date[:4]), "%d %b %Y %H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute("INSERT INTO emails_emails_data (message_id, from_address, subject, received_date) VALUES (%s, %s, %s, %s)",(msg_id, from_address, subject, received_date))
        connection.commit()
        connection.close()

obj = FetchEmails()
obj.fetch_emails()
