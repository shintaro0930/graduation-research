import xml.etree.ElementTree as ET
import glob
import csv
import os
import re
import spacy
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

"""
xml -> csv

参考リンク
https://qiita.com/Robot-Inventor/items/2264590f392a1a9e8831
"""

# 言語モデルを読み込みます
nlp = spacy.load("ja_core_news_md")

def calculate_similarity(text):
    # 文章全体と"賛成"という単語をトークン化します
    doc = nlp(text)
    support_token = nlp("賛成")[0]

    # トークンを単語ベクトルに変換します
    support_vec = support_token.vector
    doc_vec = doc.vector

    # コサイン類似度を計算します
    similarity = doc_vec.dot(support_vec) / (np.linalg.norm(doc_vec) * np.linalg.norm(support_vec))
    plt.scatter(len(text), similarity)

    plt.title(u'cos_sim between text and "pro"')
    plt.xlabel(u'text size')
    plt.ylabel(u'cos_sim')
    plt.savefig('sample.png')
    plt.xlim(0, 500) 
    plt.show()

    print(similarity)
    return similarity

def labeling(text):
    # 賛成に近しい単語リスト
    support_words = [
        "賛成",
        "賛同",
        "賛決",
        "同意",
        "了解",
        "可決",
        "支持",
        "肯定",
        "好意的",
        "賛唱",
        "同感",
        "理解",
        "賛美",
        "是認",
        "賛成の立場から",
        "支持する考え",
        "前向きに受け止める",
        "前向きな姿勢"
    ]
    # 賛成に近しい単語をトークン化します
    support_tokens = [nlp(w)[0] for w in support_words]

    # 文章全体をトークン化します
    doc = nlp(text)

    # 賛成に近しい単語と文章全体とのcos類似度を計算します
    support_similarities = [cosine_similarity(t.vector.reshape(1, -1), support_token.vector.reshape(1, -1))[0][0] for t in doc for support_token in support_tokens]

    # 賛成に近しい単語とのcos類似度の最大値を求めます
    max_support_similarity = max(support_similarities)
    print(max_support_similarity)
    plt.scatter(len(text), max_support_similarity)
    plt.xlim(0, 500)
    plt.title(u'cos_sim between text and "pro"')
    plt.xlabel(u'text size')
    plt.ylabel(u'cos_sim')
    plt.savefig('sample.png')

    # cos類似度の閾値を設定して、賛成に近しいと判定するかどうかを決めます
    # threshold = 0.3
    # if max_support_similarity >= threshold:
    #     label = 1
    # else:
    #     label = 0 if "反対" in text else 2

    return max_support_similarity


def pattern_match(text):
    yen_regex = r"(〇|一|二|三|四|五|六|七|八|九|十|百|千|万)+(円|枚|人|名|億|兆|件|団体|代)"
    per_regex = r"(〇|一|二|三|四|五|六|七|八|九)*(・)*(〇|一|二|三|四|五|六|七|八|九)(％|倍|億円|兆円)"
    date_regex = r"(〇|一|二|三|四|五|六|七|八|九|十|千|百|万)+(月|日|歳|年|時|分|秒|つ)"

    yen_matches = re.finditer(yen_regex, text, re.MULTILINE)
    for match in yen_matches:
        text = text.replace(match.group(), converter(match.group()))

    date_matches = re.finditer(date_regex, text, re.MULTILINE)
    for match in date_matches:
        text = text.replace(match.group(), converter(match.group()))

    per_matches = re.finditer(per_regex, text, re.MULTILINE)
    for match in per_matches:
        text = text.replace(match.group(), converter(match.group()).replace('・', '.'))

    return text

def converter(string):
    result = string.translate(str.maketrans("〇一二三四五六七八九", "0123456789", ""))
    convert_table = {"十": "0", "百": "00", "千": "000", "万": "0000"}

    for unit in convert_table.keys():
        zeros = convert_table[unit]
        for numbers in re.findall(f"(\d+){unit}(\d+)", result):
            result = result.replace(
                numbers[0] + unit + numbers[1], numbers[0] + zeros[len(numbers[1]):len(zeros)] + numbers[1])
        for number in re.findall(f"(\d+){unit}", result):
            result = result.replace(number + unit, number + zeros)
        for number in re.findall(f"{unit}(\d+)", result):
            result = result.replace(
                unit + number, "1" + zeros[len(number):len(zeros)] + number)
        result = result.replace(unit, "1" + zeros)
    return result


def main():
    """rangeの日付は適宜変更"""
    for i in range(2022, 2023):
        file_paths: list = glob.glob(
            '/work/data/' + str(i) + '_data/2022_*.xml', recursive=True)
        for file in file_paths:
            tree = ET.parse(file)
            root = tree.getroot()

            try:
                make_dir = '/work/csv_data/' + str(i) + '_data'
                if not os.path.exists(make_dir):
                    os.makedirs(make_dir)
            except Exception as e:
                continue

            for record in root.iter(tag='speechRecord'):
                speech_list = []
                speaker = record.find('speaker').text
                speaker_yomi = record.find('speakerYomi').text
                speech = record.find('speech').text
                date = record.find('date').text
                speaker_group = record.find('speakerGroup').text
                name_of_house = record.find('nameOfHouse').text
                name_of_meeting = record.find('nameOfMeeting').text

                speech_list.append([
                    date,
                    name_of_house,
                    name_of_meeting,
                    speaker,
                    speaker_yomi,
                    speaker_group,
                    labeling(speech),
                    pattern_match(speech)
                ])
                with open('/work/csv_data/' + str(i) + '_data/' + str(date) + '.csv', mode='a') as f:
                    writer = csv.writer(f)
                    writer.writerows(speech_list)
                    # print(speech_list)


if __name__ == "__main__":
    main()