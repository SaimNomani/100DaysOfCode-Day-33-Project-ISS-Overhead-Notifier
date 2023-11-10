# ISS-Overhead-Notifier
import requests
from datetime import datetime
from smtplib import SMTP
from data import my_email, my_password, recievers_email
import time
MY_LAT=24.860735
MY_LONG=67.001137
def check_is_iss_overhead():
    responses=requests.get(url="http://api.open-notify.org/iss-now.json")
    responses.raise_for_status()
    print(responses)
    data=responses.json()
    print(data)
    iss_longitude=float(data['iss_position']['latitude'])
    iss_latitude=float(data['iss_position']['latitude'])
    if MY_LAT+5>=iss_latitude>=MY_LAT-5 and MY_LONG+5>=iss_longitude>=MY_LONG-5:
        return True
def is_night():
    prameters={
        'lat':MY_LAT,
        'lng':MY_LONG,
        'formatted': 0,
    }
    now=datetime.now().hour
    print(now.time())
    response=requests.get(url="https://api.sunrise-sunset.org/json", params=prameters)
    response.raise_for_status()
    data=response.json()
    sunrise=data['results']['sunrise'].split('T')
    sunset=data['results']['sunset'].split("T")
    print(sunrise)
    print(sunset)
    sunrise_h=int(sunrise[1].split(':')[0])
    sunset_h=int(sunset[1].split(':')[0])
    print(sunrise_h)
    print(sunset_h)
    if now>=sunset_h or now<=sunrise_h:
        return True
while True:
    time.sleep(60)
    if check_is_iss_overhead() and is_night():
        with SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=my_password)
            connection.sendmail(from_addr=my_email, to_addrs=recievers_email, msg=f'subject:Hey look up!\n\nThe iss is over your head')
