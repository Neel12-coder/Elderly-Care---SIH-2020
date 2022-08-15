from .models import HealtParameter
import ssl
from twilio.rest import Client
import json
import urllib.error,urllib.parse,urllib.request
from background_task import background
from math import radians, sin, cos, acos
import pandas
from .models import Patient
# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
twilio_sid = 'AC1c456c0adf7f87605a67e21817c0e73d'
auth_token = '03e1526a3c68259ead1093589e324b7e'
# Create your views here.
# Api address for current weather
api_address = 'https://api.thingspeak.com/channels/957630/feeds.json?api_key=5WCJ31SXSPOQCFFJ'
@background()
def job():
    try:
        uh = urllib.request.urlopen(api_address, context=ctx)
        data = uh.read().decode()
        info = json.loads(data)
        health_instance = HealtParameter(patient_id = 1 ,aclmtr_x = -2, aclmtr_y = -2, aclmtr_z = -2,pulse = -1,temperature =  info['feeds'][-1]['field1'],humidity = info['feeds'][-1]['field2'])
        health_instance.save()
        pat = Patient.objects.get(id = 1)
        slat = radians(pat.safe_latitude)
        slon = radians(pat.safe_longitude)
        elat = radians(19.046350)
        elon = radians(72.889280)
        dist = 6371000 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
        if dist >= pat.safe_distance:
            WhatsappClient = Client(twilio_sid,auth_token)
            phone_book = {"Mohit":'+919619081783', "Chetas":'+917506960879'}
            print(phone_book.items())
            for key,value in phone_book.items():
                alert_msg = WhatsappClient.messages.create(
                    body = "Hello {}, {} is leaving the safe location. Please Help Him.".format(key,pat.name),
                    from_= 'whatsapp:+14155238886',
                    to = 'whatsapp:'+value
                )
                print("hii")
                print(alert_msg.sid)
        print("Distance:",dist)
    except Exception as e:
        print(e,"Things messed up.")


