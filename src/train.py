import pandas as pd
from torch.utils.data import Dataset, DataLoader
import glob
import re
import csv
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import logging
import torch
import numpy as np



def party_to_label(party:str) -> int:
    """
    1 : 自民党
    2 : 立憲民主党
    3 : 日本維新の会
    4 : 公明党
    5 : 日本共産党
    6 : 国民民主党
    7 : れいわ新選組
    8 : 社会民主党
    9 : 政治家女子48党
    10 : 参政党
    11 : 無所属
    12 : 欠員(Noneとする)
    """
    if(party == "自民党"):
        return 1
    elif(party == "立憲民主党"):
        return 2
    elif(party == "日本維新の会"):
        return 3
    elif(party == "公明党"):
        return 4
    elif(party == "日本共産党"):
        return 5
    elif(party == "国民民主党"):
        return 6
    elif(party == "れいわ新選組"):
        return 7
    elif(party == "社会民主党"):
        return 8
    elif(party == "政治家女子48党"):
        return 9
    elif(party == "参政党"):
        return 10
    elif(party == "無所属"):
        return 11
    else:
        return None

class MyDataset(Dataset):
    def __init__(self, tokenizer):
        self.data = []
        self.tokenizer = tokenizer
        
        for csv_file in glob.glob('/work/full_data/2022_data/2022-01-07.csv', recursive=True):
            with open(csv_file, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    row[8] = re.sub("\n", "", row[8])
                    self.data.append(row)
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        row = self.data[idx]
        date = row[0]
        name_of_house = row[1]
        speaker = row[3]
        title = row[6]
        label = int(row[7])
        speech = row[8]
        
        inputs = self.tokenizer.encode_plus(
            speech,
            add_special_tokens=True,
            padding="max_length",
            truncation=True,
            max_length=512,
            return_tensors="pt"
        )
        
        input_ids = inputs["input_ids"].squeeze()
        attention_mask = inputs["attention_mask"].squeeze()
        
        return input_ids, attention_mask, label

model_name = 'cl-tohoku/bert-base-japanese'
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
# tokenizerはJUMAN
tokenizer = AutoTokenizer.from_pretrained(model_name)

# カスタムデータセットの作成
dataset = MyDataset(tokenizer)    

# データローダーの作成
batch_size = 32
dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# モデルの訓練
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

optimizer = torch.optim.Adam(model.parameters(), lr=1e-5)
loss_fn = torch.nn.CrossEntropyLoss()

num_epochs = 10
for epoch in range(num_epochs):
    total_loss = 0
    model.train()
    for batch in dataloader:
        input_ids, attention_mask, labels = batch
        input_ids = input_ids.to(device)
        attention_mask = attention_mask.to(device)
        labels = labels.to(device)
        
        optimizer.zero_grad()
        
        outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        logits = outputs.logits
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    avg_loss = total_loss / len(dataloader)
    print(f"Epoch {epoch+1}/{num_epochs}, Average Loss: {avg_loss}")