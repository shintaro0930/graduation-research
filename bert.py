from transformers import BertJapaneseTokenizer
from transformers import BertModel
from transformers import BertForSequenceClassification, AdamW, BertConfig
import torch

print(torch.cuda.is_available())
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")

model_name = 'cl-tohoku/bert-base-japanese'
tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)

# text ="私が目指すのは、新しい資本主義の実現です。成長を目指すことは極めて重要であり、その実現に向けて全力で取り組みます。"
text = "テレビでサッカーの試合をみる。"

token = tokenizer.tokenize(text)
masked_index = 2
token[masked_index] = '[MASK]'
# print(token)


# BERTの入力データ
input_ids = tokenizer.encode(text)
print(input_ids)

tokens = tokenizer.convert_ids_to_tokens(input_ids)
# print(tokens)

encoding = tokenizer(
text, 
max_length = 20, 
padding ="max_length", 
truncation=True,
return_tensors="pt"
)
print("============")
print(type(encoding))


tensor_encoding = encoding['input_ids']
print(tensor_encoding)
tensor_encoding = tensor_encoding.to(device)

# for encode in encoding:
#     print("===****===")
#     print(encoding[encode])

model = BertForSequenceClassification.from_pretrained(
    model_name,                     #日本語pre-trainedモデルの指定
    num_labels = 2,                 # ラベル数 (True/Falseの2択)
    output_attentions = False,      # Attention Vectorを追加するかどうか
    output_hidden_states = False,       # 隠れ層を出力するか
)

#モデルをGPUへ
model = model.to(device)


# model.eval()      <--  これどういうこと?

with torch.no_grad():
    outputs = model(tensor_encoding)
    print(outputs[0].shape)
    predictions = outputs[0][0, masked_index].topk(5)

for i, index_t in enumerate(predictions.indices):
    index = index_t.item()
    token = tokenizer.convert_ids_to_tokens([index])[0]
    print(i, token)