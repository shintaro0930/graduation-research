import sentencepiece as spm
import xml.etree.ElementTree as ET
import os
import glob
import csv
# spm: SentencePiece Model

"""
sentencepiece 入門: https://note.com/npaka/n/n90f97543ec4b
sentencepieceを使ってみた: https://analytics-note.xyz/machine-learning/sentencepiece-usage/

"""


"""本来は何年分にするか"""
for i in range(2022, 2023):
    file_paths:list = glob.glob('/work/full_data/' + str(i) + '_data/*.csv', recursive=True)
    for file in file_paths:
        with open(file, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                with open('/work/spm/sp_result.txt', 'a') as spm_f:
                    speech = row[8]
                    print(speech)
                    spm_f.write(speech.rstrip())


# 1 行に 1 文の生のコーパス ファイル。

spm.SentencePieceTrainer.train(
    input = "../spm/sp_result.txt",
    model_type = "bpe",     # Byte Pair Encoding algorithm
    model_prefix = '../spm/sp_bpe',
    vocab_size = 32000,
)