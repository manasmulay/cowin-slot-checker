import requests
import random
import time
import json
import sys
from twilioCreds import *
from datetime import date
from playsound import playsound
from twilio.rest import Client

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=389&date="

# client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

# this is the Twilio sandbox testing number
from_whatsapp_number='whatsapp:' + FROM_WHATSAPP_NUMBER
# replace this number with your own WhatsApp Messaging number
to_whatsapp_number='whatsapp:' + TO_WHATSAPP_NUMBER


payload={}
headers = {
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Origin': 'https://www.cowin.gov.in',
  'Connection': 'keep-alive',
  'Referer': 'https://www.cowin.gov.in/',
  'If-None-Match': 'W/"ab66-s8iT+mK1J+aiPPe6yVXnEfmwh3w"',
  'TE': 'Trailers'
}

while(True):
    wait = random.randint(4,25)
    time.sleep(wait)

    today = date.today()
    today_date = today.strftime("%d-%m-%Y")

    response = requests.request("GET", url + today_date, headers=headers, data=payload)

    res = (json.loads(response.text))
    slots = 0
    for center in res['centers']:
        for session in center['sessions']:
            if session['available_capacity_dose1'] != 0:
                print("Center: " + center['name'] + "    \n\tPINCODE " +  str(center['pincode']) + " Age limit " + str(session['min_age_limit']) + " Address : " + center['address'] )
                slots = 1
                playsound('sound.mp3')
                client.messages.create(body="Found COVID vaccine slot in " + "Center: " + center['name'] + "    \n\tPINCODE " +  str(center['pincode']) + " Age limit " + str(session['min_age_limit']) + " Address : " + center['address'],
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)
    if slots == 0:
        print("No slots for dose 1")
