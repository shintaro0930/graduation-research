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
    faf


"""


# 質問なのか、応答なのかの分類
# 正規表現で賛成なのか、反対なのか

def get_label(text) -> int:
    pattern_pro = r"(必要(で|だ)(ある|あり)(と考え|と思))|(賛成(する|すべき|したい|したく))|"    # 引っ掛かれば人手入力
    pattern_con = r"(反対(します|する|して|しようと|だと|で)|(不必要)|信用(しない|されない|できない)|(総理|大臣)に質問します|(総理|大臣)に伺います|(総理|大臣)にお尋ねします|)"    # 引っ掛かれば人手入力
    pattern_others = r"(ありがとうございます|ありがとうございました|終わります)" # 2

    if re.search(pattern_pro, text):
        print(text)
        while True:
            label = 1
            print(f'PCは{label}です')
            user_input = input('修正する場合は 0:反対, 2:なし : ')
            if user_input == '0':
                label = 0
                break                
            elif user_input == '2':
                label = 2
                break
            elif user_input == '':
                break           
            else:
                print('無効な入力です')
    elif re.search(pattern_con, text):
        print(text)
        while True:
            label = 0
            print(f'PCは{label}です')
            user_input = input('修正する場合は 1:賛成, 2:なし : ')
            if user_input == '1':
                label = 1
                break                
            elif user_input == '2':
                label = 2
                break
            elif user_input == '':
                break           
            else:
                print('無効な入力です')
    else:
        label = 2
    return label

# enough or 10 minutes
def enough_or_minutes(text):
    result = text
    return result

# アラビア数字の変換(ラストチャンス)
def pattern_match(text):
    regex = r"((〇|一|二|三|四|五|六|七|八|九)*(・)*(〇|一|二|三|四|五|六|七|八|九|十|千|百|万)+(円|枚|人|名|件|団体|代|店舗|週間|年間|日間|回|波|か月|年度|％|倍|兆|億|月|日|歳|年|時|分|秒|つ|割|社|問|棟|メートル|))"
    matches = re.finditer(regex, text, re.MULTILINE)
    for match in matches:
        text = text.replace(match.group(), converter(match.group()))
    text = text.replace('・', '.')
    return text

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

def get_title(text):
    title = ""
    title_pattern = r'((まず|次に|最後)(.*)について)'
    matches = re.finditer(title_pattern, text, re.MULTILINE)
    if matches:
        print(text)        
        topics = [match[0] or match[1] for match in matches]
        replaced_topic = []
        for j, topic in enumerate(topics):
            topic = topic.replace('について', '').replace('まずは、', '').replace('まずは', '').replace('まず、', '').replace('まず', '').replace('次に、', '').replace('最後に、', '').replace('最後に', '')
            replaced_topic.append({j: topic})
        
            while True:
                for topic in replaced_topic:
                    for key, value in topic.items():
                        print(f"{key}: {value}")

                user_input = input("======タイトルに合う数字を入力してください: =======")
                if user_input == '':
                    return ''
                found = False
                for topic in replaced_topic:
                    for key in topic.keys():
                        if str(key) == user_input:
                            title = topic[key]
                            found = True
                            break
                    if found:
                        break

                if found:
                    break

        return title


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

            count = 0
            for row_csv in rows_csv:
                count += 1
                if count == 1:
                    speaker = row_csv[3]
                
                remove_match = r"(これより|ただいまから)|((.*)の実施について(ご|御)報告(いた|致)します)|(何とぞ(ご|御)理解と(ご|御)協力をお願いいたします)|(順次これを許します)|((ご|御)異議(は)*ありませんか)|(お諮りいたします)|(御異議なしと認めます)|(起立を求めます)|(以上、御報告申し上げます)|(そのように決しました)|(関連質疑の申出があります)|(これにて(.*)の質疑は終了いたしました)|(持ち時間の範囲内でこれを許します)"                
                if not (row_csv[3] == speaker or re.search(remove_match, row_csv[8])):                    
                    with open('/work/label_data/' + str(i) + '_data/' + row_csv[0] + '.csv', 'a') as csv_write_file:
                        for row_title in rows_title:
                            row_title[8].replace('\n\n', '\n').replace('\n', ' ')
                            candidate_title = row_title[8].split()
                            idx = 0
                            if len(candidate_title) == 1 and row_csv[1] == row_title[1] and row_csv[2] == row_title[2]:
                                row_csv[6] = candidate_title[0]
                                idx= 1

                        title_pattern = r'((まず|次に|最後)(.*)について)'
                        matches = re.finditer(title_pattern, row_csv[8])                            
                        count = sum(1 for _ in matches)                        
                        if (idx == 0 and count >= 1):
                            row_csv[6]  = get_title(row_csv[8])

                        
                        # label = get_label(row_csv[8])
                        # row_csv[7] = label
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
                    
                    if row_csv[0] == row_title[0] and row_csv[1] == row_title[1] and row_csv[2] == row_title[2] and row_title[8]:
                        row_title[8] = row_title[8].replace('\n\n', '\n').replace('\n', ' ')
                    
                        row_titleをさらにsplitしてその数が >= 1なら、タイトルを選択するように
                        row_csv[8]の中で (次に)|(次に、)~~~について(主に)|(誰に)伺ってまいります|伺います|伺いたいと思います
                                        ~~~がタイトル
                        その時はspeakerを変更しておく
                        row_csv[6] = row_title[8]   
                    """


if __name__ == "__main__":
    main()
