"""
docker run後の初回実行の場合はパスを通す必要がある
cp /etc/mecabrc/ usr/local/etc/
"""

import MeCab
mecab = MeCab.Tagger ("-d /work/mecab-ipadic-neologd/build/mecab-ipadic-2.7.0-20070801-neologd-20200910/")
testwords = "8月3日に放送された「中居正広の金曜日のスマイルたちへ」(TBS系)で、1日たった5分でぽっこりおなかを解消するというダイエット方法を紹介。キンタロー。のダイエットにも密着。"
word_list = []

for word in mecab.parse(testwords).splitlines()[:-1]:
    feature, surface = word.split('\t')
    word_list.append(feature)

print(word_list)
print(''.join(word_list))

# with open('morpheme_result.txt', 'w') as f:
#     f.write(mecab.parse(testwords))

#     for c in tagger.parse(text).splitlines()[:-1]:
#         surface, feature = c.split('\t')
#         pos = feature.split(',')[0]
#         if pos == '名詞':
#             words.append(surface)
#    return ' '.join(words)