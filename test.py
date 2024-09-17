import requests
import json

# APIs and endpoints configuration
NEWS_API_URLS = {
    'newsapi': 'https://newsapi.org/v2/everything',
    'thenewsapi': 'https://api.thenewsapi.com/v1/news/all',
    'inshorts': 'https://inshorts.deta.dev/news?category=',
    'gnews': 'https://gnews.io/api/v4/search'
}

# Add your API keys here
NEWS_API_KEY = '3b77d430512c4f9798369125496c451a'  # Replace with your actual NewsAPI key
THENEWSAPI_KEY = 'jsDXNAmpvW54XQwBICNadREuI2ylWFKAcfgoQ5NO'  # Replace with your TheNewsAPI key
GNEWS_API_KEY = '9f3f425a304be7e01cceac21c0e69799'  # Replace with your actual GNews API key

# List of Indian states to filter news
INDIAN_STATES = ['maharashtra', 'kerala', 'tamil nadu', 'uttar pradesh', 'bihar', 'west bengal', 'karnataka', 'gujarat', 'rajasthan', 'madhya pradesh', 'andhra pradesh', 'odisha', 'telangana', 'punjab', 'haryana', 'chhattisgarh', 'assam', 'jharkhand', 'uttarakhand', 'jammu', 'kashmir', 'goa', 'manipur', 'meghalaya', 'nagaland', 'sikkim', 'tripura', 'mizoram', 'arunachal pradesh']

# Function to fetch news from NewsAPI
def fetch_news_from_newsapi(query):
    params = {
        'q': query + ' India',  # Append 'India' to query to narrow it down to Indian news
        'sortBy': 'publishedAt',
        'apiKey': NEWS_API_KEY
    }
    response = requests.get(NEWS_API_URLS['newsapi'], params=params)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []

# Function to fetch news from TheNewsAPI
def fetch_news_from_thenewsapi(query):
    params = {
        'q': query + ' India',  # Append 'India' to query to narrow it down to Indian news
        'sort': 'published_at',
        'api_token': THENEWSAPI_KEY
    }
    response = requests.get(NEWS_API_URLS['thenewsapi'], params=params)
    if response.status_code == 200:
        return response.json().get('data', [])
    return []

# Function to fetch news from Inshorts
def fetch_news_from_inshorts(category):
    try:
        response = requests.get(NEWS_API_URLS['inshorts'] + category)
        response.raise_for_status()  # Raise an exception for bad responses (like 404, 500, etc.)
        
        # Try to parse the response as JSON
        try:
            news_data = response.json()
            if news_data.get('success'):
                return news_data.get('data', [])
            else:
                print(f"No success in fetching news for category: {category}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON for category: {category}")
            return []
    except requests.RequestException as e:
        print(f"Error fetching news from Inshorts API for category: {category}, Error: {e}")
    return []

# Function to fetch news from GNews
def fetch_news_from_gnews(query):
    params = {
        'q': query + ' India',  # Append 'India' to query to narrow it down to Indian news
        'lang': 'en',
        'country': 'in',  # Restrict to India (may not always work, so we add 'India' in query)
        'max': 10,  # Maximum number of results
        'apikey': GNEWS_API_KEY
    }
    response = requests.get(NEWS_API_URLS['gnews'], params=params)
    if response.status_code == 200:
        return response.json().get('articles', [])
    return []

def collect_and_store_news(disaster_type, queries, categories):
    all_articles = []
    
    # Fetch news from various sources based on query
    for query in queries:
        all_articles += fetch_news_from_newsapi(query)
        all_articles += fetch_news_from_thenewsapi(query)
        all_articles += fetch_news_from_gnews(query)
    
    # Fetch news from Inshorts based on category
    for category in categories:
        all_articles += fetch_news_from_inshorts(category)
    
    # Filter articles to ensure they are related to the disaster type and in Indian states
    relevant_articles = []
    for article in all_articles:
        # Handle NoneType by providing an empty string as fallback
        content = (
            (article.get('title') or '').lower() + ' ' +
            (article.get('description') or '').lower() + ' ' +
            (article.get('content') or '').lower()
        )
        if any(query.lower() in content for query in queries) and any(state in content for state in INDIAN_STATES):
            # Ensure no duplicate articles
            if article not in relevant_articles:
                relevant_articles.append(article)
    
    # Sort relevant articles by date (newest first, if date is included)
    relevant_articles = sorted(relevant_articles, key=lambda x: x.get('publishedAt', ''), reverse=True)
    
    # Get top 5 articles
    top_articles = relevant_articles[:5]
    
    # Save to JSON file
    file_name = f"{disaster_type}.json"
    with open(file_name, 'w') as f:
        json.dump(top_articles, f, indent=4)
    print(f"Relevant news for {disaster_type} saved to {file_name}")


if __name__ == '__main__':
    # Define disaster types and corresponding search queries and categories
    disasters = {
        'flood': {
            'queries': ['flood', 'heavy rain', 'flash flood'],
            'categories': ['science', 'world']
        },
        'earthquake': {
            'queries': ['earthquake', 'seismic activity', 'tremor'],
            'categories': ['science', 'world']
        },
        'cyclone': {
            'queries': ['cyclone', 'hurricane', 'storm'],
            'categories': ['world', 'technology']
        },
        # Add more disasters and queries/categories as needed
    }
    
    for disaster, info in disasters.items():
        collect_and_store_news(disaster, info['queries'], info['categories'])
