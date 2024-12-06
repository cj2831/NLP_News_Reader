import requests
import pandas as pd
import json
import time

api_key = 'xxx'
base_url = "https://content.guardianapis.com/search"

# Define the function to fetch articles
def fetch_guardian_articles(keywords, start_date, end_date, page=1, page_size=50):
    # Build the query URL with parameters
    url = f"{base_url}?q={keywords}&from-date={start_date}&to-date={end_date}&page={page}&page-size={page_size}&api-key={api_key}"
    
    # Send the request to The Guardian API
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Safely extract the articles
        try:
            articles = data['response']['results']
        except KeyError:
            print("Error: No 'results' found in response.")
            return []
        
        # Process the articles
        articles_data = []
        for article in articles:
            articles_data.append({
                'headline': article['webTitle'],
                'url': article['webUrl'],
                'date': article['webPublicationDate'],
                'section': article['sectionName'],
                'keywords': [tag['webTitle'] for tag in article.get('tags', [])]  # Safely handle tags
            })
        
        return articles_data
    else:
        print(f"Error fetching articles: {response.status_code}")
        return []


# Function to fetch multiple pages
def fetch_all_guardian_articles(keywords, start_date, end_date, page_size=50):
    all_articles = []
    page = 1
    while True:
        print(f"Fetching page {page}...")
        articles = fetch_guardian_articles(keywords, start_date, end_date, page, page_size)
        
        if not articles:
            break  # Exit loop if no more articles are returned
        
        all_articles.extend(articles)
        page += 1
        
        # To avoid exceeding rate limits, sleep for a second between requests
        time.sleep(1)
    
    return all_articles


keywords = "Israel OR Palestine"
start_date = "2023-01-01"
end_date = "2023-12-31"
articles = fetch_all_guardian_articles(keywords, start_date, end_date)

df = pd.DataFrame(articles)


print(df.head())

df = pd.DataFrame(articles)

# Export to CSV
df.to_csv('guardian_articles.csv', index=False)
print("Articles exported to 'guardian_articles.csv'")

# Export to JSON
df.to_json('guardian_articles.json', orient='records', lines=True)
print("Articles exported to 'guardian_articles.json'")
