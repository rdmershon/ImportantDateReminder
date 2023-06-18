#big thanks to chatgpt for making this, lets see if it works!
import pandas as pd
from twilio.rest import Client
import gspread
from google.oauth2.service_account import Credentials

# Twilio credentials
TWILIO_ACCOUNT_SID = 'your_twilio_account_sid'
TWILIO_AUTH_TOKEN = 'your_twilio_auth_token'
TWILIO_PHONE_NUMBER = 'your_twilio_phone_number'

# Google Sheets credentials
GOOGLE_SHEETS_CREDS_FILE = 'path_to_your_google_sheets_creds_file.json'
GOOGLE_SHEETS_SPREADSHEET_ID = 'your_google_sheets_spreadsheet_id'
GOOGLE_SHEETS_WORKSHEET_NAME = 'your_google_sheets_worksheet_name'

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Authenticate Google Sheets API
credentials = Credentials.from_service_account_file(GOOGLE_SHEETS_CREDS_FILE)
client_sheets = gspread.authorize(credentials)

# Load data from Google Sheets into a Pandas DataFrame
spreadsheet = client_sheets.open_by_key(GOOGLE_SHEETS_SPREADSHEET_ID)
worksheet = spreadsheet.worksheet(GOOGLE_SHEETS_WORKSHEET_NAME)
data = worksheet.get_all_records()
df = pd.DataFrame(data)

# Search for specific birthday
birthday_to_search = '2023-06-18'
matching_records = df[df['Birthday'] == birthday_to_search]

# Iterate through matching records and send SMS
for _, row in matching_records.iterrows():
    recipient_name = row['Name']
    recipient_phone = row['Phone']
    sms_message = f"Happy birthday, {recipient_name}!"
    client.messages.create(
        body=sms_message,
        from_=TWILIO_PHONE_NUMBER,
        to=recipient_phone
    )

print("SMS sent successfully!")
