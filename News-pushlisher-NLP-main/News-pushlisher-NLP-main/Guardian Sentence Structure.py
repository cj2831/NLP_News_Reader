#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 17:38:12 2024

@author: queenie
"""

import os
import pandas as pd
import requests
import time
import datetime as dt
from dateutil.relativedelta import relativedelta

# Guardian API Key
API_KEY = '629eae2c-940a-406e-b8dd-16d4aa7c64fd'  

# Set time frame
start_date = dt.date(2023, 9, 1)  # start date
end_date = dt.date(2024, 9, 30)   # end date

# Set keywords
keywords = ['Palestine', 'Israel', 'Gaza', 'West Bank', 'Hamas']

# Function to check if an article is relevant
def is_relevant(article):
    text_fields = [
        article.get('webTitle', ''),
        article.get('fields', {}).get('trailText', ''),
        article.get('fields', {}).get('bodyText', '')
    ]
    # Return True if any keyword is in the text fields
    return any(keyword.lower() in field.lower() for field in text_fields for keyword in keywords)

# Function to parse API response
def parse_response(response):
    if not response or 'response' not in response or 'results' not in response['response']:
        print("Invalid or empty response")
        return pd.DataFrame()
    
    articles = response['response']['results']
    # Filter relevant articles
    relevant_articles = [article for article in articles if is_relevant(article)]
    
    # Extract relevant fields
    data = []
    for article in relevant_articles:
        data.append({
            'webTitle': article.get('webTitle'),
            'sectionName': article.get('sectionName'),
            'webPublicationDate': article.get('webPublicationDate'),
            'webUrl': article.get('webUrl'),
            'trailText': article.get('fields', {}).get('trailText', ''),
            'bodyText': article.get('fields', {}).get('bodyText', '')
        })
    
    return pd.DataFrame(data)

# Function to fetch articles
def fetch_articles(start_date, end_date):
    base_url = "https://content.guardianapis.com/search"
    current_date = start_date
    all_articles = []

    while current_date <= end_date:
        # Define the time range
        to_date = current_date + relativedelta(months=1) - dt.timedelta(days=1)
        if to_date > end_date:
            to_date = end_date
        
        print(f"Fetching articles from {current_date} to {to_date}...")
        params = {
            'from-date': current_date.strftime('%Y-%m-%d'),
            'to-date': to_date.strftime('%Y-%m-%d'),
            'api-key': API_KEY,
            'show-fields': 'trailText,bodyText'
        }
        
        try:
            response = requests.get(base_url, params=params)
            if response.status_code == 200:
                df = parse_response(response.json())
                all_articles.append(df)
            else:
                print(f"Error fetching articles: {response.status_code}")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        current_date = to_date + dt.timedelta(days=1)
        time.sleep(1)  # Avoid hitting API limits

    # Combine all dataframes
    if all_articles:
        return pd.concat(all_articles, ignore_index=True)
    else:
        return pd.DataFrame()

# Fetch articles
articles_df = fetch_articles(start_date, end_date)

# Save the articles to a CSV file
output_file = "guardian_articles.csv"
articles_df.to_csv(output_file, index=False)
print(f"Saved {len(articles_df)} articles to {output_file}")






# To get the sentence structure
import pandas as pd
import spacy
from nltk.tokenize import sent_tokenize

# Load the CSV file
input_file = "guardian_articles.csv"
articles_df = pd.read_csv(input_file)

# Load spaCy's language model for dependency parsing
nlp = spacy.load("en_core_web_sm")

# Function to analyze sentence structure
def analyze_sentence_structure(text):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)
    sentence_analysis = []

    for sentence in sentences:
        # Process sentence with spaCy
        doc = nlp(sentence)
        
        # Count words in the sentence
        word_count = len([token.text for token in doc if not token.is_punct])
        
        # Check if the sentence is active or passive
        is_passive = any(token.dep_ == "auxpass" for token in doc)
        voice = "Passive" if is_passive else "Active"

        sentence_analysis.append({
            "sentence": sentence,
            "word_count": word_count,
            "voice": voice
        })
    return sentence_analysis

# Analyze articles in the CSV
for idx, row in articles_df.iterrows():
    print(f"Article Title: {row['webTitle']}")
    print(f"Section: {row['sectionName']}")
    print(f"Publication Date: {row['webPublicationDate']}\n")

    # Analyze body text
    body_text = row.get("bodyText", "")
    if pd.isna(body_text) or not body_text.strip():
        print("No body text available for this article.\n")
        continue

    # Get sentence structure analysis
    sentence_analysis = analyze_sentence_structure(body_text)
    for analysis in sentence_analysis:
        print(f"Sentence: {analysis['sentence']}")
        print(f"Word Count: {analysis['word_count']}")
        print(f"Voice: {analysis['voice']}\n")

    # Break after first article for brevity
    print("----------------------------------------------------")
    if idx == 0:  # Remove or increase this limit to analyze all articles
        break