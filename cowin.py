import requests
import random
import time
import json
import sys
from datetime import date

url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=389&date="

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
    if slots == 0:
        print("No slots for dose 1")
