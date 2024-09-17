import os
import json

CATEGORIES = {
    "flood": ["flood", "heavy rain", "flash flood"],
    "earthquake": ['earthquake', 'seismic', 'tremor', 'quake'],
    "cyclone": ['cyclone', 'hurricane', 'storm', 'typhoon'],
    "tsunami": ["tsunami"],
    "wildfire": ["wildfire", "forest fire", "bushfire"],
    "avalanche": ["avalanche"],
    "drought": ["drought"],
    "tornado": ["tornado"],
    "landslide": ["landslide", "mudslide"]
}

# List of political parties to filter out articles
INVALID_KEYS = {
    "BJP": ["bjp", "bharatiya janata party"],
    "INC": ["inc", "indian national congress", "congress", "cong"],
    "AAP": ["aap", "aam aadmi party"],
    "CPI": ["cpi", "communist party of india"],
    "CPM": ["cpm", "communist party of india marxist"],
    "TMC": ["tmc", "trinamool congress"],
    "SP": ["sp", "samajwadi party"],
    "RJD": ["rjd", "rashtriya janata dal"],
    "JD(U)": ["jdu", "janata dal united"],
    "DMK": ["dmk", "dravida munnetra kazhagam"],
    "AIADMK": ["aiadmk", "all india anna dravida munnetra kazhagam"],
    "Shiv Sena": ["shiv sena", "ss"],
    "Politics": ["political", "debate"]
}

NEWS_DIR = './'  # Directory containing the news articles

def contains_invalid_key(content):
    """Check if the content contains any invalid political party references."""
    content = content.lower()
    for abbrev, keywords in INVALID_KEYS.items().lower():
        for keyword in keywords:
            if keyword in content:
                return True
    return False

def categorize_articles(article):
    title = article.get('title', '').lower()
    description = article.get('description', '').lower()

    # If the article contains political content, it is invalid
    if contains_invalid_key(title) or contains_invalid_key(description):
        return 'invalid_key'
    
    # Categorize based on keywords in the title
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title:
                return category
    return 'uncategorized'

# Function to process articles and categorize them
def categorize_and_store_articles():
    categorized_articles = {category: [] for category in CATEGORIES.keys()}
    categorized_articles['invalid_key'] = []  # Category for invalid political articles
    
    # Process each JSON file in the NEWS_DIR
    for filename in os.listdir(NEWS_DIR):
        if filename.endswith('.json'):
            with open(os.path.join(NEWS_DIR, filename), 'r') as f:
                articles = json.load(f)
                for article in articles:
                    category = categorize_articles(article)
                    if category in categorized_articles:
                        categorized_articles[category].append(article)
    
    # Save categorized articles into separate JSON files
    for category, articles in categorized_articles.items():
        if articles:
            file_name = f"{category}.json"
            with open(file_name, 'w') as f:
                json.dump(articles, f, indent=4)
            print(f"Categorized articles saved to {file_name}")

# Main function
if __name__ == '__main__':
    categorize_and_store_articles()
