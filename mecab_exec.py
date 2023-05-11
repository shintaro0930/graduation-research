"""
docker run後の初回実行の場合はパスを通す必要がある
cp /etc/mecabrc/ usr/local/etc/
"""

import MeCab
mecab = MeCab.Tagger ("-d /work/b4_work/mecab-ipadic-neologd/build/mecab-ipadic-2.7.0-20070801-neologd-20200910/")
testwords = "そもそも地方の財源不足は、国の政策に地方を巻き込んで、また三位一体改革等で地方交付税を削減してきた政府の責任です。"
word_list = []

for word in mecab.parse(testwords).splitlines()[:-1]:
    feature, surface = word.split('\t')
    word_list.append(feature)

print(word_list)
print(''.join(word_list))