import glob
import csv
import re
import os


"""
このファイルでやること
- タイトルの半自動設定(中身が1つならば自動で付与, 複数ある場合は人手付与)
    - 日付、委員会などが合っているかif文で確認してから付与
- 半自動で賛成反対ラベル付与
    - 正規表現を主に使う
- さらに要らないものを消す
    - 始めます。とか、そういうのは要らない。
    - 対話以外基本的に要らない
- 漢数字をアラビア数字にするラストチャンス
    - 漢数字をgetして、それが果たして正しいのか


"""


# 質問なのか、応答なのかの分類
# 正規表現で賛成なのか、反対なのか

# if you cannot get the label from automatic evaluations, then label = 3
def get_label(text) -> int:
    label = 3

    #automatic evaluation
    """WRITE ME"""

    # 対話以外のものを消す
    """
    賛成表現
        必要である
        賛成する
        であると思う

    反対表現
        反対する
        不必要である
        承知しない
        信用しない
        ではないと思う
    
    削除対象
        これより会議を開きます。
        蔓延防止等重点措置の実施について御報告いたします。
        各党の皆様におかれましても、何とぞ御理解と御協力をお願いいたします。
        順次これを許します。  
        御異議ありませんか
        お諮りいたします。
        御異議なしと認めます。
        起立を求めます。
        以上、御報告申し上げます。

    
    """

    pattern_pro = r"WRITEME"    # 引っ掛かれば人手入力
    pattern_con = r"WRITEME"    # 引っ掛かれば人手入力
    pattern_others = r"WRITEME" # これにかかる場合は削除する

    if re.search(pattern_pro, text):
        label = 1
    elif re.search(pattern_con, text):
        label = 0
    elif re.search(pattern_others, text):
        label = 2
    else:
        """
        WRITE ME
        while文で入力できるように
        """
        return 0


    #human evaluation
    if label == 3:
        print(text)
        while True:
            user_input = input('1:賛成, 0:反対, 2:どちらでもない')
            if user_input in ['0', '1', '2']:
                label = user_input 
                break
            else:
                print("無効な入力です")
    return label


# enough or 10 minutes
def enough_or_minutes(text):
    result = text
    return result

# change kansuji to arabic numerals
def converter(string):
    result = string.translate(str.maketrans("〇一二三四五六七八九", "0123456789", ""))
    convert_table = {"十": "0", "百": "00", "千": "000", "万": "0000"}

    for unit in convert_table.keys():
        zeros = convert_table[unit]
        for numbers in re.findall(f"(\d+){unit}(\d+)", result):
            result = result.replace(
                numbers[0] + unit + numbers[1], numbers[0] + zeros[len(numbers[1]):len(zeros)] + numbers[1])
        for number in re.findall(f"(\d+){unit}", result):
            result = result.replace(number + unit, number + zeros)
        for number in re.findall(f"{unit}(\d+)", result):
            result = result.replace(
                unit + number, "1" + zeros[len(number):len(zeros)] + number)
        result = result.replace(unit, "1" + zeros)
    return result

def main():
    """
    params:
        rows_title(list(list)) : その日のタイトルを保持
        rows_csv(list(list)) : その日のcsvファイルを保持
        row_csv(list) : 答弁セグメント
        title_csv(list) : タイトルセグメント

    """

    for i in range(2022, 2023):
        row = []
        csv_file_paths = glob.glob('/work/csv_data/' + str(i) + '_data/*.csv', recursive=True)
        title_file_paths = glob.glob('/work/title_data/' + str(i) + '_data/*.csv', recursive=True)
        csv_sorted_files = sorted(csv_file_paths, key=lambda x: tuple(map(int, re.findall(r'\d+', x))))        
        title_sorted_files = sorted(title_file_paths, key=lambda x: tuple(map(int, re.findall(r'\d+', x))))

        for csv_file, title_file in zip(csv_sorted_files, title_sorted_files):
            try:
                make_dir = '/work/label_data/' + str(i) + '_data'
                if not os.path.exists(make_dir):
                    os.makedirs(make_dir)
            except Exception as e:
                continue            

            with open(csv_file, 'r') as csv_read_file, open(title_file, 'r') as title_read_file:
                reader_csv = csv.reader(csv_read_file)
                rows_csv = list(reader_csv)              
                reader_title = csv.reader(title_read_file)
                rows_title = list(reader_title)

            for row_csv in rows_csv:
                with open('/work/label_data/' + str(i) + '_data/' + row_csv[0] + '.csv', 'a') as csv_write_file:
                    # insert the title
                    for row_title in rows_title:
                        if row_csv[0] == row_title[0] and row_csv[1] == row_title[1] and row_csv[2] == row_title[2] and row_title[8]:
                            row_title[8] = row_title[8].replace('\n\n', '\n').replace('\n', ' ')
                            """ row_titleをさらにsplitしてその数が >= 1なら、タイトルを選択するように"""
                            row_csv[6] = row_title[8]
                    

                    #get the label (0,1,2)
                    label = get_label(row_csv[8])
                    row_csv[7] = label
                        
                    writer = csv.writer(csv_write_file)
                    writer.writerow(row_csv)
                        



                    """
                        漢数字 + 10分が出てきたら適宜出力 
                        それをそのままにするのか or アラビア数字に直すか
                        while True:
                            if re.search('((〇|一|二|三|四|五|六|七|八|九|十|百|千|万)+)|(10分)', row[8]):
                                user_input = input('1: アラビア数字に変更, 0: そのまま')
                                if user_input == '1':
                                    converter(row[8])
                                    break
                                elif user_input == '0':
                                    break
                                else:  
                                    print('無効な入力です')
                    """

                    """
                        matches = re.finditer(regex, text, re.MULTILINE)
                        for match in matches:
                            text = text.replace(match.group(), converter(match.group()))
                    """
                                


if __name__ == "__main__":
    main()
