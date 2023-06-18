#big thanks to ChatGPT for helping me get up and running on pandas

import pandas as pd
import datetime
from twilio.rest import Client

# Twilio credentials and the destination phone number
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_number = 'your_twilio_number'
to_number = 'destination_phone_number'

#Send Twilio SMS function
def send_sms(message, to_number):
    client = Client(account_sid, auth_token)
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=to_number
    )
    print(f"SMS sent to {to_number}")

#read CSV file into pandas data frame, iterate for values %Y, %m, %d values
#If date time reead in matches todaym then call twilio function
def schedule_sms(csv_file):
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        date_str, time_str, to_number, message = row
        schedule_datetime = datetime.datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')
        current_datetime = datetime.datetime.now()
        if schedule_datetime > current_datetime:
            time_difference = (schedule_datetime - current_datetime).total_seconds()
            print(f"Scheduling SMS to {to_number} at {schedule_datetime}")
            Timer(time_difference, send_sms, args=[message, to_number]).start()

# CSV file format: date, time, to_number, message
csv_file = 'sms_schedule.csv'
schedule_sms(csv_file)

