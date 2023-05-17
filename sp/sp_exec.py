import sentencepiece as spm


def Tokenizer(text):
    sp = spm.SentencePieceProcessor(model_file='./sp/sp_bpe.model')

    encoding = sp.encode(text)
    print(encoding)

    # tokenizer
    tokens = sp.encode_as_pieces(text)
    print(tokens)
    return tokens

if __name__ == '__main__':
    sample_text = "私が目指すのは、新しい資本主義の実現です。成長を目指すことは極めて重要であり、その実現に向けて全力で取り組みます。"
    Tokenizer(sample_text)
