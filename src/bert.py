from transformers import BertJapaneseTokenizer, BertForMaskedLM
import torch
import logging

# warningの削除
logging.getLogger("transformers.modeling_utils").setLevel(logging.ERROR)

device = "cuda" if torch.cuda.is_available() else "cpu"
model_name = 'cl-tohoku/bert-base-japanese'
tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)

text ="私が目指すのは、新しい資本主義の実現です。成長を目指すことは極めて重要であり、その実現に向けて全力で取り組みます。"

#日本語BERTはMeCabで形態素解析
token = tokenizer.tokenize(text)
masked_index = 2
# Masked_tokenを2番目のトークンに置き換えるために先頭に[DUMMY]を挿入 / [CLS]トークンが消されないように
token.insert(0, '[DUMMY]')
token[masked_index] = '[MASK]'

print(f'masked_text: {token}')

# Encoding
encoding = tokenizer(
    text,                   # 変数textをエンコーディング
    max_length = 20, 
    padding ="max_length", 
    truncation=True,
    return_tensors="pt"
)

# Tensor型に変換して、GPUに送る
tensor_encoding = encoding['input_ids']
tensor_encoding = tensor_encoding.to(device)

# maskされたところの最大確率を求めるBERTモデル
model = BertForMaskedLM.from_pretrained(
    model_name,
    output_attentions = False,
    output_hidden_states = False,
)

#モデルをGPUへ
model = model.to(device)


with torch.no_grad():
    outputs = model(tensor_encoding)
    predictions = outputs[0][0, masked_index].topk(5)

print("=====\n[MASK]されたところに入る可能性の高い文字をtop5で出力する")
for i, index_t in enumerate(predictions.indices):
    index = index_t.item()
    token = tokenizer.convert_ids_to_tokens([index])[0]
    print(i+1, token)
