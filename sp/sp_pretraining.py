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


# """本来は何年分にするか"""
# for i in range(2013, 2014):
#     file_paths:list = glob.glob('/work/data/' + str(i) + '_data/*.xml', recursive=True)
#     for file in file_paths:
#         tree = ET.parse(file)
#         root = tree.getroot()         

#         for record in root.iter(tag='speechRecord'):
#             speech = record.find('speech').text
#             print(speech)
#             with open('/work/sp/sp_result.txt', mode='a') as f:
#                 f.write(speech.rstrip())


# 1 行に 1 文の生のコーパス ファイル。

spm.SentencePieceTrainer.train(
    input = "sp_esult.txt",
    model_type = "bpe",     # Byte Pair Encoding algorithm
    model_prefix = './sp/sp_bpe',
    vocab_size = 32000,
)