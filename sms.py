import requests
import json

def send_sms(message):
    smsapikey = "96af9f9734775c0fb1b1960e1bb1dd3a028ebe1f"
    deviceId = "00000000-0000-0000-3040-adcbd60613fe"
    phno = '+919100026483'

    param = {
        "secret": smsapikey,
        "mode": "devices",
        "device": deviceId,
        "sim": 1,
        "priority": 1,
        "phone": phno,
        "message": message
    }

    r = requests.post(url="https://www.cloud.smschef.com/api/send/sms", params=param)

if __name__ == "__main__":
    send_sms()