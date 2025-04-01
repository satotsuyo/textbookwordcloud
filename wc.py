import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# テキストデータのURLとタイトル
urls_and_titles = [
    ("http://hirosakieigo.weblike.jp/appdvlp/txtbk/ES.txt", "Elementary School Textbooks"),
    ("http://hirosakieigo.weblike.jp/appdvlp/txtbk/JHS.txt", "Junior High School Textbooks"),
    ("http://hirosakieigo.weblike.jp/appdvlp/txtbk/EC.txt", "High School Textbooks: English Communication"),
    ("http://hirosakieigo.weblike.jp/appdvlp/txtbk/LE.txt", "High School Textbooks: Logic & Expression"),
]

# Streamlitで中心語を入力するウィジェット
keyword = st.text_input("中心語を入力してください:")

# 中心語が入力された場合のみ処理を実行
if keyword:
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 20))

    for i, (url, title) in enumerate(urls_and_titles):
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
        else:
            st.warning(f"エラー: {title} のテキストデータを取得できませんでした。")
            continue

        words = text.split()
        context_words = []
        for idx, word in enumerate(words):
            if word == keyword:
                start = max(0, idx - 3)
                end = min(len(words), idx + 4)
                context_words.extend(words[start:idx] + words[idx+1:end])

        context_text = " ".join(context_words)
        word_cloud = WordCloud(width=800, height=400, background_color='white', max_words=200).generate(context_text)

        axes[i].imshow(word_cloud, interpolation="bilinear")
        axes[i].set_title(title, fontsize=16)
        axes[i].axis("off")

    st.pyplot(fig)
