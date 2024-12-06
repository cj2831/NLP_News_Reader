# Import necessary libraries
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import matplotlib.pyplot as plt

# Download the VADER lexicon
nltk.download('vader_lexicon')

# Initialize VADER SentimentIntensityAnalyzer
vader_analyzer = SentimentIntensityAnalyzer()

# Define file paths
#file_path = "/Users/cjy/Desktop/NLP/guardian_articles(23.9-24.9).csv"  
#output_path = "/Users/cjy/Desktop/NLP/guardian_articles_with_sentiment.csv"  
file_path = "C:/Users/Conor/Columbia/Semester 1/NLP/Code Snippets/News-pushlisher-NLP-main/News-pushlisher-NLP-main/guardian_articles(23.9-24.9).csv"
output_path = "C:/Users/Conor/Columbia/Semester 1/NLP/Code Snippets/News-pushlisher-NLP-main/News-pushlisher-NLP-main/guardian_articles_with_sentiment_float.csv"



# Load the dataset
df = pd.read_csv(file_path)

# Ensure the file contains the 'first_paragraph' column
if 'first_paragraph' not in df.columns:
    raise ValueError("The CSV file does not contain the 'first_paragraph' column.")

# Function to perform sentiment analysis
def analyze_sentiment(text):
    """Perform sentiment analysis using VADER"""
    sentiment = vader_analyzer.polarity_scores(str(text))
    return sentiment['compound'], (
        "positive" if sentiment['compound'] > 0.05 else
        "negative" if sentiment['compound'] < -0.05 else
        "neutral"
    )

# Apply sentiment analysis to the 'first_paragraph' column
df['sentiment_score'], df['sentiment_label'] = zip(
    *df['first_paragraph'].apply(lambda x: analyze_sentiment(x))
)

# Save the results to a new file
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"Sentiment analysis results saved to: {output_path}")

# Visualize sentiment distribution
"""
plt.figure(figsize=(10, 6))
df['sentiment_label'].value_counts().plot(kind='bar', color=['green', 'blue', 'red'], title='Sentiment Distribution')
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()
"""
"""
plt.figure(figsize=(10, 6))
df['sentiment_score'].mean().plot(kind='bar', color=['blue'], title='Sentiment Average')
plt.xlabel("Sentiment")
plt.ylabel("Mean")
plt.show()
"""

#df.head()
df['sentiment_score'].describe()
    #mean = -0.1509
    # min = -0.98
    # max = 0.965
    # std 0.44


