from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Your NewsAPI key
api_key = '3b77d430512c4f9798369125496c451a'

@app.route('/')
def index():
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
        return render_template('index.html', articles=articles)
    else:
        return f"Error: {news_data.get('message')}"

if __name__ == "__main__":
    app.run(debug=True)
