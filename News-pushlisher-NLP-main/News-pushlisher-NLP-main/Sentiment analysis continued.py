import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

# 初始化 VADER 情感分析工具
vader_analyzer = SentimentIntensityAnalyzer()

# 加载现有数据文件
#file_path = "/Users/xueweihe/Desktop/NLP/combined_csv.csv"  # change it to your path
#output_path = "/Users/xueweihe/Desktop/NLP/combined_with_sentiment.csv"  # save the output_path
file_path = "C:/Users/Conor/Columbia/Semester 1/NLP/Code Snippets/News-pushlisher-NLP-main/News-pushlisher-NLP-main/NYT_one_year_combined.csv"
output_path = "C:/Users/Conor/Columbia/Semester 1/NLP/Code Snippets/News-pushlisher-NLP-main/News-pushlisher-NLP-main/NYT_articles_with_sentiment_float.csv"


# 读取 CSV 文件
df = pd.read_csv(file_path)

# 确保数据中包含 `lead_paragraph` 字段
if 'lead_paragraph' not in df.columns:
    raise ValueError("The CSV file does not contain the 'lead_paragraph' column.")

# 情感分析
def analyze_sentiment(text):
    """使用 VADER 进行情感分析"""
    sentiment = vader_analyzer.polarity_scores(str(text))
    return sentiment['compound'], (
        "positive" if sentiment['compound'] > 0.05 else
        "negative" if sentiment['compound'] < -0.05 else
        "neutral"
    )

# 应用情感分析到每一行的 `lead_paragraph`
df['sentiment_score'], df['sentiment_label'] = zip(
    *df['lead_paragraph'].apply(lambda x: analyze_sentiment(x))
)

# 保存分析结果到新文件
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"分析结果已保存到: {output_path}")

# visualize
"""
plt.figure(figsize=(10, 6))
df['sentiment_label'].value_counts().plot(kind='bar', color=['green', 'blue', 'red'], title='Sentiment Distribution')
plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.show()
"""

df['sentiment_score'].describe()

    #mean = -0.29