import MeCab
mecab = MeCab.Tagger ("-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd/")
testwords = "今日の天気は晴れです。"
print(mecab.parse(testwords))