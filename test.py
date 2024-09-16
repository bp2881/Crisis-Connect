from flask import Flask, render_template, request
import requests
import json
from train import train  # Import the updated train function

app = Flask(__name__)

# Your NewsAPI key
api_key = '3b77d430512c4f9798369125496c451a'

def dindex():
    # Define the API endpoint and parameters
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'disaster',
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': api_key
    }

    # Make the API request
    response = requests.get(url, params=params)
    news_data = response.json()

    if news_data.get('status') == 'ok':
        articles = news_data['articles']
        
        # Convert the list of articles to a dictionary
        articles_dict = {index: article for index, article in enumerate(articles)}
        
        with open("a.json", "w+", encoding="utf-8") as h:
            json.dump(articles_dict, h)

dindex()

# Load the JSON file and process each article
with open("a.json", "r") as file:
    articles_dict = json.load(file)

    # Iterate over the articles and filter using train function
    for i in range(len(articles_dict)):
        description = articles_dict[f"{i}"]["description"]
        filtered = train(description)
        
        if filtered:
            print(f"Disaster-related article: {filtered[0]}")
