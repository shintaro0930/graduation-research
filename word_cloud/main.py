import os, csv, glob, nltk, MeCab, requests
from tqdm import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def get_stopwords():
    url = "http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt"
    r = requests.get(url)
    tmp = r.text.split('\r\n')
    stopwords = []
    for i in range(len(tmp)):
        if len(tmp[i]) < 1:
            continue
        stopwords.append(tmp[i])
    return stopwords


# 名前だけのcsvを作って、まずそこになければ実行できないようにする

def visualize_frequent_phrases(name, text_list):
    # ストップワードのリストを取得
    stop_words = get_stopwords()

    # 全ての文章を結合して1つの文字列にする
    text = " ".join(text_list)

    # Mecabを初期化
    tagger = MeCab.Tagger()

    # 形態素解析して単語ごとに分割
    node = tagger.parseToNode(text)
    words = []
    while node:
        if node.surface != "":
            words.append(node.surface)
        node = node.next

    # ストップワードを除外
    words = [word for word in words if word not in stop_words]

    # 単語の出現頻度を数える
    freq_dist = nltk.FreqDist(words)

    # 上位20件の出現頻度を取得
    top_words = freq_dist.most_common(20)

    # 口癖の出現頻度データを辞書に変換
    word_freq = dict(top_words)

    # ワードクラウドを作成
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)

    # ワードクラウドを表示
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f'{name}の口癖の出現頻度')
    plt.tight_layout()
    plt.savefig("wordcloud.jpg")

def main(name):
    files_path = glob.glob('/work/csv_data/2022_data/*.csv', recursive=True)
    for file in tqdm(files_path, desc="検索中..."):
        with open(file, "r") as f:
            reader = csv.reader(f)
            rows = list(reader)
            sentences:list = []
            
            for row in rows:
                if(row[3] == name):
                    sentences.append(row[8])
            
    visualize_frequent_phrases(name, sentences)





if __name__ == "__main__":
    name  = input("気になる国会議員の名前を入力してください: ")
    main(name)
