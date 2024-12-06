# -*- coding: utf-8 -*-
"""
NYT API Scraper with Keyword Filtering
"""

import os
import pandas as pd
import requests
import time
import datetime as dt
from dateutil.relativedelta import relativedelta

# NYT API Key
API_KEY = ' '  # change it to your own NYTimes API Key

# set time frame
start_date = dt.date(2023, 9, 1)  # start date
end_date = dt.date(2024, 9, 30)   # end date

# keyword selection
def is_relevant(article):
    # set keywords
    keywords = ['Palestine', 'Israel', 'Gaza', 'West Bank', 'Hamas']
    # text fields
    text_fields = [
        article.get('headline', {}).get('main', ''),
        article.get('lead_paragraph', ''),
        ' '.join(kw['value'] for kw in article.get('keywords', []))
    ]
    # if includes keywords，return True
    return any(keyword.lower() in field.lower() for field in text_fields for keyword in keywords)

def parse_response(response):
    if not response or 'response' not in response or 'docs' not in response['response']:
        print("Invalid or empty response")
        return pd.DataFrame()

    articles = response['response']['docs']
    data = {
        'headline': [],
        'date': [],
        'web_url': [],
        'lead_paragraph': [],
        'section': [],
        'keywords': [],
    }

    for article in articles:
        if is_relevant(article):  # select topics
            data['headline'].append(article.get('headline', {}).get('main', None))
            data['date'].append(article.get('pub_date', None))
            data['web_url'].append(article.get('web_url', None))
            data['lead_paragraph'].append(article.get('lead_paragraph', None))
            data['section'].append(article.get('section_name', None))
            keywords = [kw['value'] for kw in article.get('keywords', []) if kw['name'] == 'subject']
            data['keywords'].append(keywords)

    return pd.DataFrame(data)

# send requests
def send_request(year, month):
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    url = f"{base_url}{year}/{month}.json"
    params = {'api-key': API_KEY}

    retries = 3  # try 3 times at most
    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, verify=True)
            if response.status_code == 200:
                print(f"Request successful for {year}-{month}")
                return response.json()
            elif response.status_code == 429:  # speed limitation
                print(f"Rate limit exceeded for {year}-{month}. Retrying in 30 seconds...")
                time.sleep(30)  # wait for 30s
            else:
                print(f"Request failed for {year}-{month} with status code {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching data for {year}-{month}: {e}")
            return None
    print(f"Failed to fetch data for {year}-{month} after {retries} attempts")
    return None

def get_data(start_date, end_date):
    base_dir = "/Users/xueweihe/Desktop/NLP"
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
        print(f"Created directory: {base_dir}")

    current_date = start_date
    total_articles = 0

    while current_date <= end_date:
        year = current_date.year
        month = current_date.month
        print(f"Fetching data for {year}-{month}...")

        response = send_request(year, month)
        if response:
            df = parse_response(response)
            if not df.empty:
                # save data after selection
                file_path = os.path.join(base_dir, f"{year}-{month}.csv")
                df.to_csv(file_path, index=False, encoding='utf-8-sig')
                print(f"Saved: {file_path}")
                total_articles += len(df)
            else:
                print(f"No relevant articles found for {year}-{month}")
        else:
            print(f"Failed to fetch data for {year}-{month}")

        current_date += relativedelta(months=1)
        time.sleep(10)  # control some breaks between requests

    print(f"Total relevant articles collected: {total_articles}")

# combine all data into one file
def combine_data():
    base_dir = "/Users/xueweihe/Desktop/NLP"
    all_files = [os.path.join(base_dir, f) for f in os.listdir(base_dir) if f.endswith('.csv')]
    if not all_files:
        print("No files to combine")
        return

    combined_df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)
    combined_path = os.path.join(base_dir, "combined_csv.csv")
    combined_df.to_csv(combined_path, index=False, encoding='utf-8-sig')
    print(f"Combined CSV saved to: {combined_path}")

# Run the crawl and merge logic
get_data(start_date, end_date)
combine_data()
