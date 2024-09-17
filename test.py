import requests
import json
import aiohttp
import asyncio

# APIs and endpoints configuration
NEWS_API_URLS = {
    'newsapi': 'https://newsapi.org/v2/everything',
    'thenewsapi': 'https://api.thenewsapi.com/v1/news/all',
    'gnews': 'https://gnews.io/api/v4/search'
}

NEWS_API_KEY = '3b77d430512c4f9798369125496c451a'  # Replace with your actual NewsAPI key
THENEWSAPI_KEY = 'wBtI4TWud7HcW2zTd4PwcdlpCh5OoE8M38RsD3LY'  # Replace with your TheNewsAPI key
GNEWS_API_KEY = '9f3f425a304be7e01cceac21c0e69799'  # Replace with your actual GNews API key

# List of Indian states to filter news
INDIAN_STATES = ['maharashtra', 'kerala', 'tamil nadu', 'uttar pradesh', 'bihar', 'west bengal', 'karnataka', 'gujarat', 'rajasthan', 'madhya pradesh', 'andhra pradesh', 'odisha', 'telangana', 'punjab', 'haryana', 'chhattisgarh', 'assam', 'jharkhand', 'uttarakhand', 'jammu', 'kashmir', 'goa', 'manipur', 'meghalaya', 'nagaland', 'sikkim', 'tripura', 'mizoram', 'arunachal pradesh']

# Function to fetch news from APIs
async def fetch_news(url, params):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                try:
                    return await response.json()  # Ensure it's valid JSON
                except aiohttp.ContentTypeError:
                    print(f"Error: Unexpected content type at {response.url}")
            return {}

# Function to fetch news from various sources asynchronously
async def fetch_news_async(query, categories):
    tasks = []
    
    # Fetch from NewsAPI
    params_newsapi = {'q': query + ' India', 'sortBy': 'publishedAt', 'apiKey': NEWS_API_KEY}
    tasks.append(fetch_news(NEWS_API_URLS['newsapi'], params_newsapi))
    
    # Fetch from TheNewsAPI
    params_thenewsapi = {'q': query + ' India', 'sort': 'published_at', 'api_token': THENEWSAPI_KEY}
    tasks.append(fetch_news(NEWS_API_URLS['thenewsapi'], params_thenewsapi))
    
    # Fetch from GNews
    params_gnews = {'q': query + ' India', 'lang': 'en', 'country': 'in', 'max': 10, 'apikey': GNEWS_API_KEY}
    tasks.append(fetch_news(NEWS_API_URLS['gnews'], params_gnews))
    
    results = await asyncio.gather(*tasks)
    return [article for source in results if isinstance(source, dict) for article in source.get('articles', [])]  # Check if source is a dict

# Function to collect and store news
async def collect_and_store_news(disaster_type, queries, categories):
    all_articles = []
    
    for query in queries:
        results = await fetch_news_async(query, categories)
        all_articles.extend(results)

    relevant_articles = []
    for article in all_articles:
        content = (
            (article.get('title') or '').lower() + ' ' +
            (article.get('description') or '').lower() + ' ' +
            (article.get('content') or '').lower()
        )
        if any(state in content for state in INDIAN_STATES):
            if article not in relevant_articles:
                relevant_articles.append(article)
    
    relevant_articles = sorted(relevant_articles, key=lambda x: x.get('publishedAt', ''), reverse=True)
    top_articles = relevant_articles[:5]
    
    file_name = f"{disaster_type}.json"
    with open(file_name, 'w') as f:
        json.dump(top_articles, f, indent=4)
    print(f"Relevant news for {disaster_type} saved to {file_name}")

async def main():
    disasters = {
        'flood': {'queries': ['flood', 'heavy rain', 'flash flood'], 'categories': ['science', 'world']},
        'earthquake': {'queries': ['earthquake', 'seismic activity', 'tremor'], 'categories': ['science', 'world']},
        'cyclone': {'queries': ['cyclone', 'hurricane', 'storm'], 'categories': ['world', 'technology']},
    }
    
    tasks = [collect_and_store_news(disaster, info['queries'], info['categories']) for disaster, info in disasters.items()]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
