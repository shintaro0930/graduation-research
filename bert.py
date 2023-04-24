from transformers import BertJapaneseTokenizer
from transformers import BertModel





model_name = 'cl-tohoku/bert-base-japanese-whole-word-masking'
tokenizer = BertJapaneseTokenizer.from_pretrained(model_name)
bert_model = BertModel.from_pretrained(model_name)

bert_model.to("cuda")

text = "XXX"
input = tokenizer(text, return_tensors="pt")

input["input_ids"] = input["input_ids"].to("cuda")
input["token_type_ids"] = input["token_type_ids"].to("cuda")
input["attention_mask"] = input["attention_mask"].to("cuda")

outputs = bert_model(**input)
last_hidden_states = outputs.last_hidden_state
attention_mask = input.attention_mask.unsqueeze(-1)
valid_token_num = attention_mask.sum(1)
sentence_vec = (last_hidden_states*attention_mask).sum(1) / valid_token_num
sentence_vec = sentence_vec.detach().cpu().numpy()[0]

# BERTで作成した文ベクトルのshape
print(sentence_vec.shape)

# BERTで作成した文ベクトル
print(sentence_vec)