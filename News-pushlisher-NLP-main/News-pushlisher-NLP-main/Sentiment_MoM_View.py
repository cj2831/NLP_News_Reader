import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.pyplot as plt

# Vader
vader_analyzer = SentimentIntensityAnalyzer()

# Get New York Times Sentiment Data Path
file_path = "C:/Users/Conor/Columbia/Semester 1/NLP/Code Snippets/News-pushlisher-NLP-main/News-pushlisher-NLP-main/NYT_articles_with_sentiment_float.csv"

# load csv
df_nyt = pd.read_csv(file_path)

# Get Guardian sentiment data path
file_path = "C:/Users/Conor/Columbia/Semester 1/NLP/Code Snippets/News-pushlisher-NLP-main/News-pushlisher-NLP-main/guardian_articles_with_sentiment_float.csv"

# load csv
df_guardian = pd.read_csv(file_path)

# Determine minimal columns I need for NYT
#print(list(df_nyt.columns))
#df_nyt.head()
    # All I need is "Web_URL", "Lead Paragraph", "Sentiment Score" and then extract month and year from date
    # date looks like a full datetime object here, extract logic ideally should work

print(list(df_guardian.columns))
#df_guardian.head()
    # All I need is "url", "first_paragraph", "sentiment_score" and then extract month and year from date
#df_guardian["date"].head()
    # this also looks like a datetime object, hopefully extract logic should work

df_nyt['year'] = pd.DatetimeIndex(df_nyt['date']).year
df_nyt['month'] = pd.DatetimeIndex(df_nyt['date']).month

#print(list(df_nyt.columns))
#df_nyt.head()

df_guardian['year'] = pd.DatetimeIndex(df_guardian['date']).year
df_guardian['month'] = pd.DatetimeIndex(df_guardian['date']).month

print(list(df_guardian.columns))
df_guardian.head()

#rename some nyt variables so they match the guardians
df_nyt['url'] = df_nyt['web_url']
df_nyt['first_paragraph'] = df_nyt['lead_paragraph']
df_nyt['YearMonth'] = df_nyt['year'].astype(str) + '-' + df_nyt['month'].astype(str).str.zfill(2)
df_guardian['YearMonth'] = df_guardian['year'].astype(str) + '-' + df_guardian['month'].astype(str).str.zfill(2)

#create cut version of NYT and Guardian data sets
df_nyt_ii = df_nyt.loc[:, ['url','first_paragraph','sentiment_score','year','month','YearMonth']]
df_guardian_ii = df_guardian.loc[:, ['url','first_paragraph','sentiment_score','year','month','YearMonth']]
df_nyt_ii['paper'] = "New York Times"
df_guardian_ii['paper'] = "Guardian"

#df_nyt_ii.head()
#df_guardian_ii.head()

df_final = pd.concat([df_nyt_ii, df_guardian_ii], axis=0)
#df_final.head()

#Data Processing Complete

df_group = df_final.groupby(['paper','YearMonth']).agg({'url': ['count'], 'sentiment_score': ['mean']})

# Flatten the multi-index columns
df_group.columns = ['_'.join(col) for col in df_group.columns]

print(df_group)

output_path = "C:/Users/Conor/Columbia/Semester 1/NLP/Code Snippets/News-pushlisher-NLP-main/News-pushlisher-NLP-main/combined_yearmonth_data_sentiment.csv"


#df_group.to_csv(output_path, index=False, encoding='utf-8-sig')
#print(f"Sentiment analysis results saved to: {output_path}")

df_group.head()