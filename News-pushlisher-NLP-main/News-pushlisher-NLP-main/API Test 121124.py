# -*- coding: utf-8 -*-
"""
Created on Tue Nov 12 21:42:19 2024

@author: Conor
"""

"""
NYT API Test Run
"""

#Attempt 1
"""
# Import Libraries
import os
import pandas as pd
import requests
import json
import time
import dateutil
import datetime
from dateutil.relativedelta import relativedelta
import urllib3

#Useful Functions
def send_request(date):
    base_url = 'https://api.nytimes.com/svc/archive/v1/'
    url = base_url + '/' + date[0] + '/' + date[1] + '.json?api-key=' + API_KEY
    try:
        response = requests.get(url, verify=False).json()
    except Exception:
        return None
    time.sleep(6)
    return response


def is_valid(article, date):
    is_in_range = date > start and date < end
    has_headline = type(article['headline']) == dict and 'main' in article['headline'].keys()
    return is_in_range and has_headline


def parse_response(response):
    data = {'headline': [],  
        'date': [], 
        'web_url': [],
        'doc_type': [],
        'lead_paragraph': [],
        'material_type': [],
        'author': [],
        'section': [],
        'subsection': [],
        'keywords': []}
    
    articles = response['response']['docs']
    
    for article in articles: 
        date = dateutil.parser.parse(article['pub_date']).date()
        if is_valid(article, date):
            data['date'].append(date)
            data['headline'].append(article['headline']['main']) 
            if 'section_name' in article:
                data['section'].append(article['section_name'])
            else:
                data['section'].append(None)
            if 'lead_paragraph' in article:
                data['lead_paragraph'].append(article['lead_paragraph'])
            else:
                data['lead_paragraph'].append(None)
            if 'web_url' in article:
                data['web_url'].append(article['web_url'])
            else:
                data['web_url'].append(None)
            if 'subsection_name' in article:
                data['subsection'].append(article['subsection_name'])
            else:
                data['subsection'].append(None)
            if 'byline' in article:
                data['author'].append(article['byline']['original'])
            else:
                data['author'].append(None)
            data['doc_type'].append(article['document_type'])
            if 'type_of_material' in article: 
                data['material_type'].append(article['type_of_material'])
            else:
                data['material_type'].append(None)
            keywords = [keyword['value'] for keyword in article['keywords'] if keyword['name'] == 'subject']
            data['keywords'].append(keywords)
    return pd.DataFrame(data) 


def get_data(dates):
    total = 0
    print('Date range: ' + str(dates[0]) + ' to ' + str(dates[-1]))
    if not os.path.exists('headlines'):
        os.mkdir('headlines')
    for date in dates:
        print('Working on ' + str(date) + '...')
        csv_path = 'headlines/' + date[0] + '-' + date[1] + '.csv'
        if not os.path.exists(csv_path): # If we don't already have this month 
            response = send_request(date)
            if response is not None:
                df = parse_response(response)
                total += len(df)
                df.to_csv(csv_path, index=False)
                print('Saving ' + csv_path + '...')
    print('Number of articles collected: ' + str(total))

#Run API
API_KEY = 'G784PSPOC0GuhvP6qAAjyDzx3CZIQ6FZ'

end = datetime.date(2020, 12, 31)
start = datetime.date(2019, 1, 1)
     

months = [x.split(' ') for x in pd.date_range(start, end, freq='MS').strftime("%Y %-m").tolist()]
     

get_data(months)
     

import os
import glob
import pandas as pd
os.chdir("/content/headlines") ## use Google Colab
     

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]
     

#combine in a single file
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')
"""

#Got a weird error on this one, would need to debug
    #File c:\users\conor\columbia\semester 1\nlp\code snippets\api test 121124.py:53 in parse_response
      #articles = response['response']['docs']
      #KeyError: 'response'
      
#Seems to be some sort of key error in the parse response function

#Attempt 2
    #Based on this GitHub:
        #https://github.com/ietz/nytimes-scraper


#pip install nytimes-scraper
    #Use this library for scraping purposes
    
 # This apparently is the "programatic" use   
"""
import datetime as dt
from nytimes_scraper import run_scraper, scrape_month

# scrape february of 2020
article_df, comment_df = scrape_month('G784PSPOC0GuhvP6qAAjyDzx3CZIQ6FZ', date=dt.date(2020, 2, 1))

# scrape all articles month by month
run_scraper('G784PSPOC0GuhvP6qAAjyDzx3CZIQ6FZ')
#Running this seems to work, but it's taking like 15 minutes just for this month
    # LOL nevermind, got some sort of attribute error
"""

#This apparently is the "granular" use
import datetime as dt
from nytimes_scraper.nyt_api import NytApi
from nytimes_scraper.articles import fetch_articles_by_month, articles_to_df
#from nytimes_scraper.comments import fetch_comments, fetch_comments_by_article, comments_to_df

#Note: we probably don't need comments

api = NytApi('G784PSPOC0GuhvP6qAAjyDzx3CZIQ6FZ')

# Fetch articles of a specific month
articles = fetch_articles_by_month(api, dt.date(2020, 2, 1))
article_df = articles_to_df(articles)

    #Note: this takes a while, be prepared to sit for a minute (even for one month)

import pandas as pd
df_test = pd.DataFrame(article_df)

#This, to some extent, worked. But I don't fully understand the output lol

print (df_test.head())
df_test.describe()
df_test.columns

# This looks pretty good actually, I think this works


#Cutting out articles for now
"""
# Fetch comments from multiple articles
# a) using the results of a previous article query
article_ids_and_urls = list(article_df['web_url'].iteritems())
comments_a = fetch_comments(api, article_ids_and_urls)
comment_df = comments_to_df(comments_a)

# b) using a custom list of articles
comments_b = fetch_comments(api, article_ids_and_urls=[
    ('nyt://article/316ef65c-7021-5755-885c-a9e1ef2cfdf2', 'https://www.nytimes.com/2020/01/03/world/middleeast/trump-iran-suleimani.html'),
    ('nyt://article/b2d1b802-412e-51f7-8864-efc931e87bb3', 'https://www.nytimes.com/2020/01/04/opinion/impeachment-witnesses.html'),
])

# Fetch comment for one specific article by its URL
comments_c = fetch_comments_by_article(api, 'https://www.nytimes.com/2019/11/30/opinion/sunday/bernie-sanders.html')
"""


#Let's try Wall Street Journal Now!!
"""
WSJ Test Run
"""

#Inherent problem:
    # WSJ does not offer a free API
    # Sent a request to Dow Jones, but not holding my breath

#Solution:
    #Here's a list of some free APIs
        # https://github.com/public-apis/public-apis?tab=readme-ov-file#news
    # Some tempting options:
        # The Guardian
        # Associated Press
        # NPR One
        # MediaStack

###############################
# Try the Guardian
###############################

#pip install theguardian
#from theguardian import theguardian_content
#import git

"""
git clone https://github.com/prabhath6/theguardian-api-python.git
cd theguardian-api-python

source ../guardian/bin/activate
pip install -r requirements.txt

python test.py

cp -r theguardian ../guardian/lib/python3.5
"""

#import git+
#pip install git+"https://github.com/prabhath6/theguardian-api-python.git"
    #pip install git+"https://github.com/prabhath6/theguardian-api-python/theguardian.git"



#pip install git+"https://github.com/prabhath6/theguardian-api-python.git"
    #RUn the above in command line where Git is enabled
#from theguardian import theguardian_content

##############################################################################
#Having a little trouble with the above method, trying a different one for now:
##############################################################################

#https://airbyte.com/pyairbyte/the-guardian-api-python

#pip install airbyte
#import airbyte as ab
"""
source = ab.get_source(
   source-the-guardian-api,
   install_if_missing=True,
   config={
     "api_key": "yo6e5e9076-e3b7-4da1-87d7-57b8aed6fbd7",
     "start_date": "2023-01-01",
     "query": "environment AND NOT water",
     "tag": "environment/recycling",
     "section": "technology",
     "end_date": "2023-12-01"
   }
)
"""


##############################################################################
#Having a little trouble with this one too, trying a different one again:
##############################################################################

#https://github.com/haoshuai999/The-Guardian-API-Profile

"""
api_key = "yo6e5e9076-e3b7-4da1-87d7-57b8aed6fbd7"
#pip install TheGuardian_credentials
#from TheGuardian_credentials import api_key
import requests
import json
#import urllib3
#from urllib3 import packages

# set up base url
base_url = "https://content.guardianapis.com/"

# set up parameters
search_keyword = 'Brexit OR (Theresa AND May)'
data_format = 'json'
section = 'politics'
from_date = '2018-01-01'
to_date = '2018-12-31'
page = 1
page_size = 10
order_by = 'newest'
production_office = 'uk'
lang = 'en'

finalized_url = "{}search?/q={}&format={}&section={}&from-date={}&to-date={}&page={}&page-size={}&order-by={}&production-office={}&lang={}&api-key={}".format(base_url, search_keyword, data_format, section, from_date, to_date, page, page_size, order_by, production_office, lang, api_key)

# perform the request and print the query
r = requests.get(url = finalized_url, params={})

print(finalized_url, '\t')

#output the responses to a file
Guardian = json.loads(r.text)
with open('Guardian_data_query1.json', 'w') as outfile:  
    json.dump(Guardian, outfile, indent=4)
  
"""
    
###################################
# Struggling a bit here too, again!
###################################

#https://towardsdatascience.com/discovering-powerful-data-the-guardian-news-api-into-python-for-nlp-1829b568fb0f
