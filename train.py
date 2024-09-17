import os
import json
import re

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

other_countries = [
    "China", "United States", "Indonesia", "Pakistan", "Brazil", "Nigeria", "Bangladesh",
    "Russia", "Mexico", "Japan", "Ethiopia", "Philippines", "Egypt", "Vietnam", "DR Congo", 
    "Turkey", "Iran", "Germany", "Thailand", "United Kingdom", "France", "Italy", "Tanzania",
    "South Africa", "Myanmar", "Kenya", "South Korea", "Colombia", "Spain", "Uganda", 
    "Argentina", "Sudan", "Iraq", "Poland", "Canada", "Morocco", "Saudi Arabia", "Uzbekistan", 
    "Peru", "Angola", "Afghanistan", "Malaysia", "Venezuela", "Nepal", "Ghana", "Yemen", 
    "Mozambique", "North Korea", "Australia", "Taiwan", "Ivory Coast", "Madagascar", "Cameroon", 
    "Niger", "Sri Lanka", "Burkina Faso", "Mali", "Romania", "Kazakhstan", "Malawi", "Chile", 
    "Zambia", "Guatemala", "Ecuador", "Syria", "Netherlands", "Senegal", "Cambodia", "Chad", 
    "Somalia", "Zimbabwe", "Guinea", "Rwanda", "Benin", "Burundi", "Tunisia", "Bolivia", 
    "Belgium", "Haiti", "Cuba", "South Sudan", "Dominican Republic", "Czech Republic", 
    "Greece", "Jordan", "Portugal", "Azerbaijan", "Sweden", "Honduras", "United Arab Emirates", 
    "Hungary", "Tajikistan", "Belarus", "Austria", "Papua New Guinea", "Serbia", "Israel", 
    "Switzerland", "Togo", "Sierra Leone", "Laos", "Paraguay", "Bulgaria", "Libya"
]

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

def clean_content(content, countries):
    """Remove occurrences of country names from the content."""
    for country in countries:
        content = re.sub(r'\b' + re.escape(country) + r'\b', '', content, flags=re.IGNORECASE)
    return content

def contains_invalid_key(content):
    """Check if the content contains any invalid political party references."""
    content = content.lower()
    for abbrev, keywords in INVALID_KEYS.items():
        for keyword in keywords:
            if keyword in content:
                return True
    return False

def categorize_articles(article):
    title = article.get('title', '').lower()
    description = article.get('description', '').lower()

    # Clean content by removing country names
    title = clean_content(title, other_countries)
    description = clean_content(description, other_countries)

    # If the article contains political content, it is invalid
    if contains_invalid_key(title) or contains_invalid_key(description):
        return 'invalid_key'

    # Add additional context to avoid financial or unrelated articles
    # Check for unrelated contexts like finance or market
    unrelated_terms = ['finance', 'investment', 'market', 'funds', 'office', 'business', 'gift city']
    if any(term in title for term in unrelated_terms) or any(term in description for term in unrelated_terms):
        return 'uncategorized'

    # Categorize based on keywords in the title
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            # Check if the keyword is accompanied by natural disaster-related terms
            if keyword in title and ('rain' in title or 'flood' in title or 'cyclone' in title):
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
