import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import asyncio
from Database.DAL.WebResourcesDAL import WebResourcesDAL
from Database.DAL.ChatsDAL import ChatsDAL
from Database.session import async_session
import random
from Exchanges.MOEX.AlgoPack import *
from datetime import datetime, timedelta
from settings import basedir


async def get_all_web_news():
    async with async_session() as session:
        web_dal = WebResourcesDAL(session)
        news = await web_dal.select_all_web_resources()
        return news


async def get_all_tg_news():
    async with async_session() as session:
        chat_dal = ChatsDAL(session)
        news = await chat_dal.select_all()
        return news


async def create_and_save_dataset():
    news = await get_all_web_news()
    chats_news = await get_all_tg_news()

    combined_news = []
    combined_news.extend(news)
    combined_news.extend(chats_news)

    # for item in combined_news:
    #     item['rating'] = random.randint(0, 100)

    df = pd.DataFrame(combined_news)
    df.to_json('news_rating_dataset.json', orient='records', indent=4)


# asyncio.run(create_and_save_dataset())


class NewsSentimentClassifier:
    def __init__(self):
        self.file_path = f'{basedir}/ML/news_rating_dataset.json'
        self.vectorizer = CountVectorizer()
        self.model = LogisticRegression()
        self.df = None
        self.labels = None
        self.X = None
        self.fit_model()

    def fit_model(self):
        df = pd.read_json(self.file_path)
        df = df.dropna(subset=['text', 'rating'])

        df['rating'] = df['rating'].astype(int)
        df = df[(df['rating'] >= 0) & (df['rating'] <= 10)]

        news_texts = df['text'].tolist()
        self.labels = df['rating'].tolist()

        filtered_texts = [text for text in news_texts if text and isinstance(text, str) and text.strip()]
        self.labels = self.labels[:len(filtered_texts)]

        self.X = self.vectorizer.fit_transform(filtered_texts)
        self.model.fit(self.X, self.labels)

    def predict_sentiment(self, news_text):
        news_vector = self.vectorizer.transform([news_text])
        prediction = self.model.predict(news_vector)
        return prediction[0]





