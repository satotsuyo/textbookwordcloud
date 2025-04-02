import streamlit as st
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

# 必要なデータをダウンロード
nltk.download('wordnet')
nltk.download('omw-1.4')

# レンマタイザの初期化
lemmatizer = WordNetLemmatizer()

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
    # レンマタイゼーションで中心語を原形に変換
    keyword_lemma = lemmatizer.lemmatize(keyword.lower())

    # 縦に4つのグラフを配置するための設定
    fig, axes = plt.subplots(nrows=4, ncols=1, figsize=(10, 20))

    for i, (url, title) in enumerate(urls_and_titles):
        response = requests.get(url)
        if response.status_code == 200:
            text = response.text
        else:
            st.error(f"エラー: {title} のテキストデータを取得できませんでした。")
            continue

        # テキストを単語に分割して原形に変換
        words = [lemmatizer.lemmatize(word.lower()) for word in text.split()]
        context_words = []
        for idx, word in enumerate(words):
            if word == keyword_lemma:
                # 前後3語を取得（範囲外の場合を考慮）
                start = max(0, idx - 3)
                end = min(len(words), idx + 4)
                context_words.extend(words[start:idx] + words[idx+1:end])

        # 周辺語をスペースで連結してテキスト化
        context_text = " ".join(context_words)

        # context_text が空の場合の処理
        if not context_text:
            st.warning(f"'{keyword}' に関連する語が見つかりませんでした（{title}）。")
            continue

        # ワードクラウドを生成
        word_cloud = WordCloud(width=800, height=400, background_color='white', max_words=200).generate(context_text)

        # ワードクラウドをプロット
        axes[i].imshow(word_cloud, interpolation="bilinear")
        axes[i].set_title(title, fontsize=16)
        axes[i].axis("off")

    # Streamlitでプロットを表示
    st.pyplot(fig)
