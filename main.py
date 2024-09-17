from flask import Flask, render_template, request
import requests
import json
from train import train  

app = Flask(__name__)

# API keys for NewsAPI and TheNews API
newsapi_key = '3b77d430512c4f9798369125496c451a'
thenewsapi_key = 'jsDXNAmpvW54XQwBICNadREuI2ylWFKAcfgoQ5NO'  

# Function to fetch articles from NewsAPI
def fetch_newsapi_articles():
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': 'disaster',
        'sortBy': 'publishedAt',
        'language': 'en',
        'apiKey': newsapi_key,
        'country': 'in'  # Fetch articles related to India
    }

    response = requests.get(url, params=params)
    news_data = response.json()

    if news_data.get('status') == 'ok':
        return news_data['articles']
    return []

# Function to fetch articles from TheNews API
def fetch_thenewsapi_articles():
    url = 'https://api.thenewsapi.com/v1/news/all'
    params = {
        'api_token': thenewsapi_key,
        'search': 'disaster',
        'language': 'en',
        'country': 'in',  # Fetch articles related to India
        'published_on': '2023-09-17'  # Fetch recent articles
    }

    response = requests.get(url, params=params)
    news_data = response.json()

    if 'data' in news_data:
        return news_data['data']
    return []

# Function to fetch, combine, and remove duplicate articles
def fetch_combined_articles():
    # Fetch articles from both APIs
    newsapi_articles = fetch_newsapi_articles()
    thenewsapi_articles = fetch_thenewsapi_articles()

    # Combine the articles
    combined_articles = newsapi_articles + thenewsapi_articles

    # Remove duplicates using a set for descriptions
    unique_articles = []
    seen_descriptions = set()
    
    for article in combined_articles:
        description = article.get('description', '')
        if description and description not in seen_descriptions:
            unique_articles.append(article)
            seen_descriptions.add(description)
    
    return unique_articles

# Function to save categorized articles in separate JSON files
def save_to_json(category, article_data):
    filename = f"{category}.json"
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            existing_data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.append(article_data)

    with open(filename, 'w', encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)

# Main logic (part of main.py)
combined_articles = fetch_combined_articles()

for article in combined_articles:
    description = article.get("description", "")
    filtered = train(description)

    if filtered:
        article_text, category = filtered  # Get the article and category from the train function
        save_to_json(category, article)  # Save article in its respective category file
        print(f"Disaster-related article categorized as {category}: {article_text}")

