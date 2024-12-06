#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 14:05:50 2024

@author: xueweihe
"""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import matplotlib.pyplot as plt
import seaborn as sns
import nltk

# 下载停用词
nltk.download('stopwords')

# 文件路径
file_path = "/Users/xueweihe/Desktop/NLP/combined_csv.csv"  # 替换为您的文件路径

# 加载数据
df = pd.read_csv(file_path)

# 确保数据中包含必要的字段
if 'lead_paragraph' not in df.columns:
    raise ValueError("The CSV file必须包含 'lead_paragraph' 字段。")

# 数据预处理
def preprocess(text):
    """预处理文本"""
    stop_words = set(stopwords.words('english'))
    text = str(text).lower()  # 转为小写
    words = [word for word in text.split() if word.isalpha() and word not in stop_words]  # 去除停用词和非字母
    return ' '.join(words)

df['processed_text'] = df['lead_paragraph'].apply(preprocess)

# 向量化（Count Vectorizer，用于 LDA）
vectorizer = CountVectorizer(max_features=1000, stop_words='english')
count_matrix = vectorizer.fit_transform(df['processed_text'])

# 主题建模（LDA）
num_topics = 5  # 设置主题数量
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
topic_distributions = lda.fit_transform(count_matrix)

# 输出主题关键词
def display_topics(model, feature_names, no_top_words):
    """显示每个主题的关键词"""
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic {topic_idx + 1}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]))

print("主要主题及其关键词：")
display_topics(lda, vectorizer.get_feature_names_out(), 10)

# 添加主题分布到数据框
df['dominant_topic'] = topic_distributions.argmax(axis=1)

# 可视化每个主题的分布
plt.figure(figsize=(8, 6))
sns.countplot(x='dominant_topic', data=df, palette='coolwarm')
plt.title("NYT 数据的主题分布")
plt.xlabel("主题编号")
plt.ylabel("文章数量")
plt.show()

# 保存结果到文件
output_path = "/Users/xueweihe/Desktop/NLP/nyt_with_topics.csv"
df.to_csv(output_path, index=False, encoding='utf-8-sig')
print(f"主题分析结果已保存到: {output_path}")

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# 确保 `lda` 模型已经运行并提取了主题关键词
def generate_wordclouds(lda_model, feature_names, num_topics=5, top_words=20):
    """为每个主题生成词云图"""
    for topic_idx, topic in enumerate(lda_model.components_):
        # 获取主题的关键词及其权重
        topic_words = {feature_names[i]: topic[i] for i in topic.argsort()[:-top_words - 1:-1]}
        
        # 生成词云图
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white'
        ).generate_from_frequencies(topic_words)
        
        # 显示词云图
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(f"Topic {topic_idx + 1}", fontsize=16)
        plt.show()

# 调用函数生成词云
generate_wordclouds(lda, vectorizer.get_feature_names_out(), num_topics=5)

from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk

# 确保 NLTK 停用词可用
nltk.download('stopwords')

# 文件路径
file_path = "/Users/xueweihe/Desktop/NLP/combined_csv.csv"  # 替换为您的文件路径

# 加载数据
df = pd.read_csv(file_path)

# 检查是否有 'lead_paragraph' 字段
if 'lead_paragraph' not in df.columns:
    raise ValueError("The CSV file must contain a 'lead_paragraph' column.")

# 数据预处理
def preprocess(text):
    """清洗和标准化文本"""
    stop_words = set(stopwords.words('english'))
    text = str(text).lower()  # 转为小写
    words = [word for word in text.split() if word.isalpha() and word not in stop_words]  # 去除停用词和非字母
    return ' '.join(words)

# 对所有的 `lead_paragraph` 应用预处理
df['processed_text'] = df['lead_paragraph'].apply(preprocess)

# 将所有处理后的文本合并为一个字符串
all_text = ' '.join(df['processed_text'])

# 生成词云
wordcloud = WordCloud(
    width=800, height=400,
    background_color='white',
    colormap='viridis',  # 设置词云颜色方案
    max_words=200  # 限制最多显示的单词数量
).generate(all_text)

# 显示词云图
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Word Cloud for All Lead Paragraphs", fontsize=16)
plt.show()


