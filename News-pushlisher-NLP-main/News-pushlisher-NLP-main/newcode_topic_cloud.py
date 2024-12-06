#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 15:58:11 2024

@author: xueweihe
"""

from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from nltk.corpus import stopwords
import nltk

# 确保 NLTK 停用词可用
nltk.download('stopwords')

# 文件路径
file_path = "/Users/xueweihe/Desktop/NLP/combined_csv.csv"

# 加载数据
df = pd.read_csv(file_path)

# 检查是否有 'lead_paragraph' 字段
if 'lead_paragraph' not in df.columns:
    raise ValueError("The CSV file必须包含 'lead_paragraph' 字段。")

# 数据预处理
def preprocess(text):
    """清洗和标准化文本"""
    stop_words = set(stopwords.words('english'))
    text = str(text).lower()  # 转为小写
    words = [word for word in text.split() if word.isalpha() and word not in stop_words]  # 去除停用词和非字母
    return ' '.join(words)

# 对所有的 `lead_paragraph` 应用预处理
df['processed_text'] = df['lead_paragraph'].apply(preprocess)

# 向量化（Count Vectorizer，用于 LDA）
vectorizer = CountVectorizer(max_features=1000, stop_words='english')
count_matrix = vectorizer.fit_transform(df['processed_text'])

# 主题建模（LDA）
num_topics = 5  # 设置主题数量
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
topic_distributions = lda.fit_transform(count_matrix)

# 保存主题关键词到文档
def save_topics_to_file(model, feature_names, no_top_words, output_path):
    """将每个主题的关键词保存到文档"""
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topic_keywords = [feature_names[i] for i in topic.argsort()[:-no_top_words - 1:-1]]
        topics.append({'Topic': f"Topic {topic_idx + 1}", 'Keywords': ", ".join(topic_keywords)})
    
    # 转换为 DataFrame 并保存
    topics_df = pd.DataFrame(topics)
    topics_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"主题关键词已保存到: {output_path}")

# 输出主题关键词到文件
output_path = "/Users/xueweihe/Desktop/NLP/topics_keywords.csv"
save_topics_to_file(lda, vectorizer.get_feature_names_out(), 10, output_path)

import seaborn as sns
import matplotlib.pyplot as plt

# 添加 dominant_topic 列
df['dominant_topic'] = topic_distributions.argmax(axis=1)

# 可视化每个主题的分布
plt.figure(figsize=(8, 6))
sns.countplot(x='dominant_topic', data=df, palette='coolwarm')
plt.title("NYT Topic Distribution")
plt.xlabel("Topic")
plt.ylabel("Article Counts")
plt.show()

# 为每个主题生成词云
def generate_topic_wordclouds(lda_model, feature_names, num_topics=5, top_words=20):
    """为每个主题生成词云图，调整特定词的权重"""
    word_weights = {'israel': 0.2, 'israeli': 0.2, 'palestine': 0.2, 'palestinian': 0.2}  # 词权重调整
    for topic_idx, topic in enumerate(lda_model.components_):
        # 获取主题的关键词及其权重
        topic_words = {feature_names[i]: topic[i] for i in topic.argsort()[:-top_words - 1:-1]}
        # 调整特定词的频率
        for word in word_weights:
            if word in topic_words:
                topic_words[word] *= word_weights[word]
        
        # 生成词云图
        wordcloud = WordCloud(
            width=800, height=400,
            background_color='white'
        ).generate_from_frequencies(topic_words)
        
        # 提取主题关键词作为标题
        topic_keywords = [feature_names[i] for i in topic.argsort()[:-5 - 1:-1]]
        topic_title = f"Topic {topic_idx + 1}: " + ", ".join(topic_keywords)

        # 显示词云图
        plt.figure(figsize=(10, 6))
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.title(topic_title, fontsize=16)
        plt.show()

# 调用函数生成每个主题的词云
generate_topic_wordclouds(lda, vectorizer.get_feature_names_out(), num_topics=5)

# 生成整体词云
def generate_overall_wordcloud(text, word_weights):
    """生成整体词云，调整特定词的权重"""
    words = text.split()
    adjusted_words = []
    for word in words:
        if word in word_weights:
            if random.random() < word_weights[word]:  # 按权重随机保留
                adjusted_words.append(word)
        else:
            adjusted_words.append(word)
    adjusted_text = ' '.join(adjusted_words)
    
    # 生成词云图
    wordcloud = WordCloud(
        width=800, height=400,
        background_color='white',
        colormap='viridis',
        max_words=200
    ).generate(adjusted_text)
    
    # 显示词云图
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title("Overall Word Cloud (Adjusted)", fontsize=16)
    plt.show()

# 调整特定词权重并生成整体词云
word_weights = {'israel': 0.2, 'israeli': 0.2, 'palestine': 0.2, 'palestinian': 0.2}
generate_overall_wordcloud(' '.join(df['processed_text']), word_weights)