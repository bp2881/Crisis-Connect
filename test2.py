import os
import json
from flask import Flask, render_template, request
from iplocation import *

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

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    location = ip() 

    data = read_help_requests()

    new_request = {
        "name": name,
        "email": email,
        "message": message,
        "location": location
    }
    data['requests'].append(new_request)
    write_help_requests(data)

    return render_template('submit.html')

if __name__ == '__main__':
    app.run(debug=True)
