from transformers import BertJapaneseTokenizer
from transformers import BertModel

model_name = 'cl-tohoku/bert-base-japanese'
tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)

text ="私が目指すのは、新しい資本主義の実現です。成長を目指すことは極めて重要であり、その実現に向けて全力で取り組みます。"

token = tokenizer.tokenize(text)
print(token)

input_ids = tokenizer.encode(text)
print(input_ids)

tokens = tokenizer.convert_ids_to_tokens(input_ids)
print(tokens)

encoding = tokenizer(
    text, 
    max_length =35, 
    padding ="max_length", 
    truncation=True,
    return_tensors="pt"
)
print(encoding)

