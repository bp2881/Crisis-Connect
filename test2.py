from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from iplocation import *

app = Flask(__name__, static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////database/help.db'
db = SQLAlchemy(app)

class HelpRequest(db.Model):
    id1 = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    location = ip()
    
    help_request = HelpRequest(name=name, email=email, message=message, location=location)
    db.session.add(help_request)
    db.session.commit()
    
    return 'Form submitted successfully!'

if __name__ == '__main__':
    app.run(debug=True)