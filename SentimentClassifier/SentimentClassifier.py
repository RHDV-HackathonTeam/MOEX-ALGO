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
import spacy
from spacy.util import minibatch, compounding
import os
import sklearn
import sklearn.metrics


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

    def get_lemas(self, text):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(text)
        filtered_tokens = [token for token in doc if not token.is_stop]
        print(filtered_tokens)
        lemmas = [
            f"Token: {token}, lemma: {token.lemma_}"
            for token in filtered_tokens
        ]

        return lemmas

    vector_preset = ([1.8371646, 1.4529226, -1.6147211, 0.678362, -0.6594443,
                      1.6417935, 0.5796405, 2.3021278, -0.13260496, 0.5750932,
                      1.5654886, -0.6938864, -0.59607106, -1.5377437, 1.9425622,
                      -2.4552505, 1.2321601, 1.0434952, -1.5102385, -0.5787632,
                      0.12055647, 3.6501784, 2.6160972, -0.5710199, -1.5221789,
                      0.00629176, 0.22760668, -1.922073, -1.6252862, -4.226225,
                      -3.495663, -3.312053, 0.81387717, -0.00677544, -0.11603224,
                      1.4620426, 3.0751472, 0.35958546, -0.22527039, -2.743926,
                      1.269633, 4.606786, 0.34034157, -2.1272311, 1.2619178,
                      -4.209798, 5.452852, 1.6940253, -2.5972986, 0.95049495,
                      -1.910578, -2.374927, -1.4227567, -2.2528825, -1.799806,
                      1.607501, 2.9914255, 2.8065152, -1.2510269, -0.54964066,
                      -0.49980402, -1.3882618, -0.470479, -2.9670253, 1.7884955,
                      4.5282774, -1.2602427, -0.14885521, 1.0419178, -0.08892632,
                      -1.138275, 2.242618, 1.5077229, -1.5030195, 2.528098,
                      -1.6761329, 0.16694719, 2.123961, 0.02546412, 0.38754445,
                      0.8911977, -0.07678384, -2.0690763, -1.1211847, 1.4821006,
                      1.1989193, 2.1933236, 0.5296372, 3.0646474, -1.7223308,
                      -1.3634219, -0.47471118, -1.7648507, 3.565178, -2.394205,
                      -1.3800384])

    def load_training_data(
            data_directory: str = "./",
            split: float = 0.8,
            limit: int = 0
    ) -> tuple:
        reviews = []
        for label in ["pos", "neg"]:
            labeled_directory = f"{data_directory}/{label}"
            for review in os.listdir(labeled_directory):
                if review.endswith(".txt"):
                    with open(f"{labeled_directory}/{review}") as f:
                        text = f.read()
                        if text.strip():
                            spacy_label = {
                                "cats": {
                                    "pos": "pos" == label,
                                    "neg": "neg" == label}
                            }
                            reviews.append((text, spacy_label))
        random.shuffle(reviews)

        if limit:
            reviews = reviews[:limit]
        split = int(len(reviews) * split)
        return reviews[:split], reviews[split:]

    def evaluate_model(tokenizer, textcat, test_data: list) -> dict:
        reviews, labels = zip(*test_data)
        reviews = (tokenizer(review) for review in reviews)
        TP, FP, TN, FN = 1e-8, 0, 0, 0
        for i, review in enumerate(textcat.pipe(reviews)):
            true_label = labels[i]['cats']
            score_pos = review.cats['pos']
            if true_label['pos']:
                if score_pos >= 0.5:
                    TP += 1
                else:
                    FN += 1
            else:
                if score_pos >= 0.5:
                    FP += 1
                else:
                    TN += 1
        precision = TP / (TP + FP)
        recall = TP / (TP + FN)
        f_score = 2 * precision * recall / (precision + recall)
        return {"precision": precision, "recall": recall, "f-score": f_score}

    def train_model(
            self,
            training_data: list,
            test_data: list,
            iterations: int = 20) -> None:
        nlp = spacy.load("en_core_web_sm")
        if "textcat" not in nlp.pipe_names:
            textcat = nlp.create_pipe(
                "textcat", config={"architecture": "simple_cnn"}
            )
            nlp.add_pipe(textcat, last=True)
        else:
            textcat = nlp.get_pipe("textcat")

        textcat.add_label("pos")
        textcat.add_label("neg")


        training_excluded_pipes = [
            pipe for pipe in nlp.pipe_names if pipe != "textcat"
        ]
        with nlp.disable_pipes(training_excluded_pipes):
            optimizer = nlp.begin_training()
            print("Начинаем обучение")
            print("Loss\t\tPrec.\tRec.\tF-score")  #
            batch_sizes = compounding(
                4.0, 32.0, 1.001
            )
            for i in range(iterations):
                loss = {}
                random.shuffle(training_data)
                batches = minibatch(training_data, size=batch_sizes)
                for batch in batches:
                    text, labels = zip(*batch)
                    nlp.update(
                        text,
                        labels,
                        drop=0.2,
                        sgd=optimizer,
                        losses=loss
                    )
                with textcat.model.use_params(optimizer.averages):
                    evaluation_results = self.evaluate_model(
                        tokenizer=nlp.tokenizer,
                        textcat=textcat,
                        test_data=test_data
                    )  #
                    print(f"{loss['textcat']:9.6f}\t\
    {evaluation_results['precision']:.3f}\t\
    {evaluation_results['recall']:.3f}\t\
    {evaluation_results['f-score']:.3f}")

        with nlp.use_params(optimizer.averages):
            nlp.to_disk("model_artifacts")

    def test_model(self, input_data):
        loaded_model = spacy.load("model_artifacts")
        parsed_text = loaded_model(input_data)
        if parsed_text.cats["pos"] > parsed_text.cats["neg"]:
            prediction = "good"
            score = parsed_text.cats["pos"]
        else:
            prediction = "bad"
            score = parsed_text.cats["neg"]
        return prediction

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
