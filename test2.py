import os
import json
from flask import Flask, render_template, request
from iplocation import *
from sms import *


app = Flask(__name__, static_folder='static')

db_file = os.path.join('database', 'help_requests.json')

if not os.path.exists('database'):
    os.makedirs('database')

def read_help_requests():
    if os.path.exists(db_file):
        with open(db_file, 'r') as file:
            return json.load(file)
    else:
        return {"requests": []}

def write_help_requests(data):
    with open(db_file, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/emergency')
def emergency():
    ip_location = ip()
    ip_address = get_public_ip()
    phone = '+919100026483'
    message = f'An emergency request has been received from {ip_location} \nip- {ip_address}'

    r = send_sms(message=message, phno=phone)
    return render_template('emergency.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    location = ip()
    name = request.form['name']
    phno = request.form['phone']
    message = request.form['message']
    message = f'{name} has requested help\n{message}\nContact number - {phno}\nArea - {location}'
    send_sms(message=message)
    
    data = read_help_requests()
    new_request = {
        "name": name,
        "phno": phno,
        "message": message,
        "location": location
    }
    data['requests'].append(new_request)
    write_help_requests(data)

    return render_template('submit.html', iplocation=location)

if __name__ == '__main__':
    app.run(debug=True)