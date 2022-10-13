# Import Libraries
import requests
import json
import time
import datetime
import os
import sys
from plyer import notification


def get_vaccine_availability(url, alert_duration, api_request_frequency, date):
    '''
    url: Cowin API url for vaccine slot availability.
    alert_duration: Duration for which alert remains in system.
    api_request_frequency: Frequency at which api must be hit.

    Finds the open slots of vaccine and generates system notification.
    '''
    while True:
        # Start a Session
        with requests.session() as session:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
            response = session.get(url, headers=headers)

            # Receive the response
            response = response.json()
            for center in response['centers']:
                for session in center['sessions']:
                    # For Age less than 45 and capacity is above zero
                    if (session['min_age_limit'] == 18) & (
                            session['available_capacity'] > 0):
                        message_string = f"Subject: {date}'s Alert'!! \n\n Available - {session['available_capacity']} in {center['pincode']} on {session['date']} for the age {session['min_age_limit']}"
                        notification.notify(
                            # title of the notification,
                            title="Alert",
                            # the body of the notification
                            message=message_string,
                            # the notification stays for alert_duration
                            timeout=alert_duration
                        )
        time.sleep(api_request_frequency)


def get_vaccine_slot(pincode, date, alert_duration, api_request_frequency):
    '''
    pincode: pincode of area where vaccine availability needs to be checked.
    date: date for which vaccine availability needs to be checked.

    Finds the vaccine slot availability for a given pincode & date.
    '''
    url = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode={pincode}&date={date}"
    get_vaccine_availability(url, alert_duration, api_request_frequency, date)


if __name__ == "__main__":
    pincode = int(sys.argv[1])  # Read the pincode from command line.
    date = sys.argv[2]  # Read the date from command line.
    alert_duration = int(sys.argv[3])  # Read the alert duration from command line.
    # Read the api request frequency from command line.
    api_request_frequency = int(sys.argv[4])
    get_vaccine_slot(pincode, date, alert_duration, api_request_frequency)
