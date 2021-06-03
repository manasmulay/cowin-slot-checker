import requests
import random
import time
import json
import sys
from twilioCreds import *
from datetime import date
from playsound import playsound
from twilio.rest import Client

excluePin = [424109, 423204]

def getSearchCriteria():
  print("Enter")
  print("1. Search by district")
  print("2. Search by pinCode")
  global criteria
  criteria = input("Enter criteria 1 / 2 : ")
  data = ""
  if criteria == 1:
    data = input("Enter district_id: ")
  else:
    data = input("Enter pin: ")
  return str(data)

def twilioMessaging():
  if len(sys.argv) == 2 and sys.argv[1] == 'whatsapp':
    # client credentials are read from TWILIO_ACCOUNT_SID and AUTH_TOKEN
    client = Client(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN)

    # this is the Twilio sandbox testing number
    from_whatsapp_number='whatsapp:' + FROM_WHATSAPP_NUMBER
    # replace this number with your own WhatsApp Messaging number
    to_whatsapp_number='whatsapp:' + TO_WHATSAPP_NUMBER
    client.messages.create(body="Found COVID vaccine slot in " + "Center: " + center['name'] + "    \n\tPINCODE " +  str(center['pincode']) + " Age limit " + str(session['min_age_limit']) + " Address : " + center['address'],
                       from_=from_whatsapp_number,
                       to=to_whatsapp_number)

def getUrl(data, criteria):
  today = date.today()
  today_date = today.strftime("%d-%m-%Y")
  url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/"
  calendarByDistrict = "calendarByDistrict?"
  calendarByPin = "calendarByPin?"
  if criteria == 1:
    url = url + calendarByDistrict + "district_id=" + data + "&date=" + today_date
  else:
    url = url + calendarByPin + "pincode=" + data + "&date=" + today_date
  return url


def getHeader():
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
  return headers

def main(data,criteria):
  while(True):
      wait = random.randint(4,25)
      time.sleep(wait)

      
      response = requests.request("GET", getUrl(data,criteria), headers=getHeader(), data={})

      res = (json.loads(response.text))
      slots = 0
      for center in res['centers']:
          for session in center['sessions']:
              if session['available_capacity_dose1'] != 0 and center['pincode'] not in excluePin:
                  print("Center: " + center['name'] + "    \n\tPINCODE " +  str(center['pincode']) + " Age limit " + str(session['min_age_limit']) + " Address : " + center['address'] )
                  slots = 1
                  playsound('sound.mp3')
                  twilioMessaging()
      if slots == 0:
          print("No slots for dose 1")

if __name__ == '__main__':
  data = getSearchCriteria()
  main(data,criteria)