import sentencepiece as spm

# spm: SentencePiece Model

"""
sentencepiece 入門: https://note.com/npaka/n/n90f97543ec4b
sentencepieceを使ってみた: https://analytics-note.xyz/machine-learning/sentencepiece-usage/

"""

spm.SentencePieceTrainer.train(
    input = "result.txt",
    model_type = "bpe",     # Byte Pair Encoding algorithm
    model_prefix = './sp/sp_bpe',
    vocab_size = 32000,
)