import MeCab
mecab = MeCab.Tagger ("-d /work/mecab-ipadic-neologd/build/mecab-ipadic-2.7.0-20070801-neologd-20200910/")
testwords = "8月3日に放送された「中居正広の金曜日のスマイルたちへ」(TBS系)で、1日たった5分でぽっこりおなかを解消するというダイエット方法を紹介。キンタロー。のダイエットにも密着。"
print(mecab.parse(testwords))