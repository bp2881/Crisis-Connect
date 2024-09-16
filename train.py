disaster_keywords = [
    "disaster", "floods", "flood", "earthquake", "tsunami", 
    "cyclone", "hurricane", "wildfire", "avalanche",
    "drought", "tornado", "landslide"
]

def train(text):
    filtered_articles = []

    for word in disaster_keywords:
        if word.lower() in text.lower():
            filtered_articles.append(text)
            break 

    return filtered_articles
