from flask import Flask, render_template, request, g
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import datetime

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '16fyKjO2-N_WIkZCy_VTRgvnguGb9jyFr5znKhBUxOT0'
SAMPLE_RANGE_NAME = 'Email List!A2:E'


def authenticate():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return creds


creds = authenticate()
service = build('sheets', 'v4', credentials=creds)
sheet = service.spreadsheets()

# Call the Sheets API

app = Flask(__name__)


@app.route('/')
def hello_world():

    dateTime = datetime.now()
    dt_string = dateTime.strftime("%d/%m/%Y %H:%M:%S")

    values = [
        [
            # Cell values ...
            dt_string, None, True
        ]
        # Additional rows ...
    ]
    body = {
        'values': values
    }
    try:
        result = service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
            valueInputOption="USER_ENTERED", body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))
    except:
        pass

    return render_template('index.html')


@app.route('/preorder', methods=['POST', 'GET'])
def preorder():
    print("Form submitted")
    email = request.form['email']

    if email:
        dateTime = datetime.now()
        dt_string = dateTime.strftime("%d/%m/%Y %H:%M:%S")

        values = [
            [
                # Cell values ...
                dt_string, email
            ]
            # Additional rows ...
        ]
        body = {
            'values': values
        }
        try:
            result = service.spreadsheets().values().append(
                spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                valueInputOption="USER_ENTERED", body=body).execute()
            print('{0} cells updated.'.format(result.get('updatedCells')))
        except:
            pass

    # your code
    # return a response
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
