import os 
import csv
import pandas as pd
import glob


# 政党ごとにラベルを変える
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


file_path = glob.glob('/work/full_data/2022_data/2022-01-07.csv')
df = pd.read_csv(file_path[0], header=None, names=['date', 'house', 'meeting', 'speaker', 'speaker yomi', 'speaker group', 'theme', 'label', 'sentence'])

df = df.drop(columns=['date', 'speaker yomi'])

print(f'データサイズ: {df.shape}')
print(df.sample(10))
# print(df.iloc[1, 1])

