import requests

smsapikey = "96af9f9734775c0fb1b1960e1bb1dd3a028ebe1f"
deviceId = "00000000-0000-0000-3040-adcbd60613fe"
phone = '+919100026483'
message = 'Hello! messy programmer, sending from python'

message = {
    "secret": smsapikey,
    "mode": "devices",
    "device": deviceId,
    "sim": 1,
    "priority": 1,
    "phone": phone,
    "message": message
}

r = requests.post(url = "https://www.cloud.smschef.com/api/send/sms", params = message)
result = r.json()