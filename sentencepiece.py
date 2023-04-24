import sentencepiece as spm

"""
sentencepiece 入門: https://note.com/npaka/n/n90f97543ec4b

"""


# 学習の実行
spm.SentencePieceTrainer.Train(
    '--input=wiki.txt --model_prefix=sentencepiece --vocab_size=8000 --character_coverage=0.9995'
)

# モデルの作成
sp = spm.SentencePieceProcessor()
sp.Load("sentencepiece.model")

# テキストを語彙列に分割
print(corpus[0])
print(sp.EncodeAsPieces(corpus[0]))

# テキストを語彙IDに分割
print(corpus[0])
print(sp.EncodeAsIds(corpus[0]))