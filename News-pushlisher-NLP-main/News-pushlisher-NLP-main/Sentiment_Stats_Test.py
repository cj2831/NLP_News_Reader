import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
from scipy import stats

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

#Run T-Test
# Perform independent samples t-test
t_statistic, p_value = stats.ttest_ind(df_nyt_ii['sentiment_score'], df_guardian_ii['sentiment_score'])

print("t-statistic:", t_statistic) #-15
print("p-value:", p_value) #1.5e-50
print("NYT Mean", df_nyt_ii['sentiment_score'].mean()) #-0.295
print("Guardian Mean", df_guardian_ii['sentiment_score'].mean()) #-0.151
print("Delta", df_nyt_ii['sentiment_score'].mean() - df_guardian_ii['sentiment_score'].mean()) #-0.144

