from nsetools import Nse
import requests
import sys

def smsMethod(cmp,contact):
   API_ENDPOINT = "https://alerts.solutionsinfini.com//api/v4/index.php"
   data = {'method': 'sms',
       'message': 'Your alert has been triggered CMP='+cmp,
       'sender': 'HACKAT',
       'api_key': 'A91862b9c45ff3872032bb46332b1be86',
       'to': contact}
   r = requests.post(url=API_ENDPOINT, data=data)
   print(r.status_code)

def voiceMethod(contact):
   API_ENDPOINT="https://voice.solutionsinfini.com/api/v1/"
   data={
       'method':'dial.click2call',
       'format':'xml',
       'caller':contact,
       'receiver':'ivr:57342',
       'api_key':'Ad9b6d364b7d3fa47d382ec64efc043fd'}
   r = requests.post(url=API_ENDPOINT, data=data)
   print(r.status_code)

nse = Nse()

symbol = sys.argv[1]
contact_number = int(sys.argv[2])
high = int(sys.argv[3])
low = int(sys.argv[4])
notification_type = int(sys.argv[5])
datekey = sys.argv[6]

check_file = open("file.txt","r")
content  = check_file.readlines()

if datekey in content:
    exit()

q = nse.get_quote(symbol)
price = q["pricebandupper"]

check_file_append = open("file.txt","+a")

if price >= high or price <=low:
    check_file_append.write(datekey)
    if notification_type==1:
        smsMethod(str(price),contact_number)
    elif notification_type == 2:
        voiceMethod(contact_number)
    else:
        smsMethod(str(price),contact_number)
        voiceMethod(contact_number)
