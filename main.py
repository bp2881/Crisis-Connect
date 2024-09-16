# app.py (Flask)
"""from flask import Flask, jsonify
import tweepy  # For Twitter API
import requests  # For news API
import json

app = Flask(__name__)"""
# Twitter API Configuration
consumer_key = 'xDyw8lBIBl89iN4OXwAgP43hY'
consumer_secret = 'WVgK8r6q6CgROyrzogWq5OqBZUSRTafZBPj6sGRtzGz5GBuy4j'
access_token = '1730900359382794240-ClmN26O5XymUoOj3q3ySwicdcif75B'
access_token_secret = 'SeSVxozL4f0pDCe9tNdnJMZyfPDRrkANt8UmmcT2N9QSj'
from flask import Flask, redirect, url_for, session, request
import tweepy
import os

app = Flask(__name__)
app.secret_key = 'AAAAAAAAAAAAAAAAAAAAACaqvwEAAAAAL6rBeSs889JtD55q%2BZW%2BnEVbESE%3DQu2eFHSqyf2ef7V43cTKjnAylUQ6CIEt7590Jki8vgYeVzCFb9' 
callback_url = 'http://127.0.0.1:5000/callback'  # Same as your registered callback URL

# Step 1: Redirect to Twitter for Authorization
@app.route('/login')
def login():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    try:
        # Redirect user to Twitter to authorize
        redirect_url = auth.get_authorization_url()
        session['request_token'] = auth.request_token  # Store the request token for the next step
        return redirect(redirect_url)
    except tweepy.TweepError as e:
        return f'Error! Failed to get request token. {e}'

# Step 2: Handle the callback from Twitter
@app.route('/callback')
def callback():
    request_token = session.get('request_token')
    del session['request_token']  # We no longer need this

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    auth.request_token = request_token

    try:
        # Get the access token
        auth.get_access_token(request.args.get('oauth_verifier'))
        session['access_token'] = auth.access_token
        session['access_token_secret'] = auth.access_token_secret
    except tweepy.TweepError as e:
        return f'Error! Failed to get access token. {e}'

    # At this point, the user is authenticated and we have the access tokens
    return redirect(url_for('welcome'))

# Welcome route after successful login
@app.route('/welcome')
def welcome():
    access_token = session.get('access_token')
    access_token_secret = session.get('access_token_secret')

    if not access_token:
        return redirect(url_for('login'))

    # Use the access token to authenticate API calls
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # Get the authenticated user's profile
    user = api.me()
    return f'Hello, {user.name}! Welcome to the app!'

if __name__ == '__main__':
    app.run()

    articles = news_data.get('articles', [])
    print(jsonify(articles))