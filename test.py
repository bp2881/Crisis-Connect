from flask import Flask, render_template, request
import requests
import json
from train import train  

app = Flask(__name__)

api_key = '3b77d430512c4f9798369125496c451a'

def dindex():
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'disaster',
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': api_key
    }

    response = requests.get(url, params=params)
    news_data = response.json()

    if news_data.get('status') == 'ok':
        articles = news_data['articles']
        
        articles_dict = {index: article for index, article in enumerate(articles)}
        
        with open("a.json", "w+", encoding="utf-8") as h:
            json.dump(articles_dict, h)

dindex()

with open("a.json", "r") as file:
    articles_dict = json.load(file)
    for i in range(len(articles_dict)):
        description = articles_dict[f"{i}"]["description"]
        filtered = train(description)

        if filtered:
            print(f"Disaster-related article: {filtered[0]}")
