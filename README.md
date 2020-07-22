1. Установка среды
pip install pip-tools

pip-compile --output-file requirements.txt requirements.in

pip-sync

или 

pip install -r requirements.txt


2. Структура проекта
data/: директория с датасетами, здехь находятся скаченные и предобработанные данные

notebooks/: ноутбуки с решениями задач

notebooks/models/: директория с файлами обученных моделей,
готовые модели доступны по ссылке https://drive.google.com/file/d/1QV8XaWWzbLix9sKahAMiG5UaXUDb58ig/view?usp=sharing


3. Задачи

3.1. Постройте систему классификации текстов набора данных RuTweetCorp на два класса эмоциональной окраски: положительный, и отрицательный. В качестве меры качества используйте макро усредненную F1 меру.
 
3.2. Постройте систему предсказания количества ретвитов (количества копирований этого сообщения другими пользователями) по данному тексту из набора данных RuTweetCorp. Избегайте утечек данных - в качестве входных данных используйте те данные, которые доступны пользователю перед публикацией твита, т.е. нельзя “заглядывать в будущее” и использовать количество добавлений твита в избранное для предсказания ретвитов. В качестве меры качества используйте MAE.


4. Использованные материалы

Sentiment Analysis of Posts and Comments in the Accounts of Russian Politicians on the Social Network
https://fruct.org/publications/fruct25/files/Sve.pdf

Анализируем тональность текстов с помощью Fast.ai
https://habr.com/ru/post/472988/

Retweet Wars: Tweet Popularity Prediction via Dynamic Multimodal Regression
https://www.cs.unc.edu/~mbansal/papers/retweetwars-wacv18.pdf

Анализируем тональность текстов с помощью Fast.ai
https://habr.com/ru/post/472988/

STEPIK: Нейронные сети и обработка текста
https://stepik.org/course/54098/syllabus

PyTorch Sentiment Analysis
https://github.com/bentrevett/pytorch-sentiment-analysis
