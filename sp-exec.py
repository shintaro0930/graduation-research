import sentencepiece as spm


sp = spm.SentencePieceProcessor(model_file='./wiki_unigram.model')

sample_text = "私が目指すのは、新しい資本主義の実現です。成長を目指すことは極めて重要であり、その実現に向けて全力で取り組みます。"

encoding = sp.encode(sample_text)
print(encoding)

tokens = sp.encode_as_pieces(sample_text)
print(tokens)
