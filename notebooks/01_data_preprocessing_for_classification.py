#!/usr/bin/env python
# coding: utf-8

import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import re
import pymorphy2


# ### Стадии очистки текста:
# 1. Приведение к нижниму регистру
# 2. Замена буквы "ё" на "е"
# 3. Удаление цифр
# 4. Удаление HTML специальных символов
# 5. Замена упоминаний пользователей @username на тег at_user
# 6. Замена символа хештега # на тег hash
# 7. Удаление RT
# 8. Замена гиперссылок на тег url
#
# В работе "Sentiment Analysis of Posts and Comments in the Accounts of Russian Politicians on the Social Network"
# в разделе "III. DATA AND METHODOLOGY" рассматривается стадия распознования смайликов в последовательностях пунктуации 
# и замену их на теги соответствующих смайлов. Это уменьшит "шум", создоваемый черезмерным употреблением символов пунктуации
# 
# Для простоты, я не стал удалять знаки пунктуации.
def preprocess_text(text):
    text = text.lower().replace("ё", "е")
    # Remove digits
    text = re.sub("\d+:\d+", " ", text)
    text = re.sub(" \d+", " ", text)
    # Removing ;quot; and &amp
    text = re.sub(';quot;', ' ', text)
    text = re.sub('&amp', ' ', text)
    # Remove HTML special entities 
    text = re.sub(r'\&\w*;', ' ', text)
    # Convert @username to AT_USER
    text = re.sub('@[^\s]+', 'at_user', text)
    # Remove whitespace (including new line characters)
    text = re.sub(r'\s\s+', ' ', text)
    # Removing '#' hash tag
    text = re.sub('#', 'hash ', text)
    # Removing RT
    text = re.sub('rt[\s]+', '', text)
    # Removing hyperlink
    text = re.sub('https?:\/\/\S+', 'url', text)
    # Separate words and punctuation
    text = re.findall(r"[\w']+|[.,!?;:()]", text)
    text = " ".join(text)
    return text


# ### Лемматизация
#
# Использую лемматизатор от pymorphy2. Он не снимает омонимию, так как обрабатывате каждое сло по отдельности.
# Для обычных текстов я бы использовал pymystem3. Он обрабатывает предложения целиком и способен различить разные слова с одинаковым написанием.
def lemmatize(text):
    words = []
    for token in text.split():
        # Если токен уже был закеширован, быстро возьмем результат из кэша.
        if token in cache.keys():
            words.append(cache[token])
        # Слово еще не встретилось, будем проводить медленный морфологический анализ.
        else:
            result = morph.parse(token)
            word = result[0].normal_form
            # Отправляем слово в результат, ...
            words.append(word)
            # ... и кешируем результат его разбора.
            cache[token] = word
    return ' '.join(words)


# ### Data preprocessing
if __name__ == "__main__":
    seed = 42
    np.random.seed(seed)
    positive_file = "../data/positive.csv"
    negative_file = "../data/negative.csv"
    cache = {}
    morph = pymorphy2.MorphAnalyzer()

    column_names = ["id", "tdate", "tmane", "ttext", "ttype", "trep", "trtw", "tfav", "tstcount", "tfoll", "tfrien",
                    "listcount"]
    positive_df = pd.read_csv(positive_file, sep=";", names=column_names, index_col=False)
    negative_df = pd.read_csv(negative_file, sep=";", names=column_names, index_col=False)
    # Смена метки класса для отрицательной эмоциональной окраски
    negative_df["ttype"] = 0
    df = pd.concat([negative_df, positive_df])
    df = df[["ttext", "ttype"]]
    df.columns = ['text', 'target']

    # Clean the tweets
    df['text'] = df['text'].apply(preprocess_text)
    df['text'] = df['text'].apply(lemmatize)
    df = df.drop(df[df['text'].map(str) == 'nan'].index)
    train, validate, test = np.split(df.sample(frac=1), [int(.6 * len(df)), int(.8 * len(df))])
    train.to_csv("../data/train_processed_data.csv", index=False)
    validate.to_csv("../data/validate_processed_data.csv", index=False)
    test.to_csv("../data/test_processed_data.csv", index=False)

