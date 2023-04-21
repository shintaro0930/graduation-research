from numpy import dot
from numpy.linalg import norm
from transformers import BertModel
from transformers import BertJapaneseTokenizer

tokenizer = BertJapaneseTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')
bert_model = BertModel.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking')

sentences = ["私はラーメンが好きです","チャーシューメンが好きです"]

input = tokenizer(sentences, return_tensors="pt",padding=True,truncation=True)

input["input_ids"] = input["input_ids"].to("cuda")
input["token_type_ids"] = input["token_type_ids"].to("cuda")
input["attention_mask"] = input["attention_mask"].to("cuda")

outputs = bert_model(**input)
last_hidden_states = outputs.last_hidden_state
attention_mask = input.attention_mask.unsqueeze(-1)
valid_token_num = attention_mask.sum(1)
sentence_vecs = (last_hidden_states*attention_mask).sum(1) / valid_token_num
sentence_vecs = sentence_vecs.detach().cpu().numpy()


similarity_with_bert = dot(sentence_vecs[0], sentence_vecs[1]) / (norm(sentence_vecs[0])*norm(sentence_vecs[1]))

print(similarity_with_bert)