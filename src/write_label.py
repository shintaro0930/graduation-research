import glob
import csv
import re
import os
import unicodedata

def get_label(text) -> int:
    with open('../text_list/pro_list.txt', 'r') as prolist, open('../text_list/con_list.txt', 'r') as conlist, open('../text_list/others_list.txt', 'r') as otherslist:
        pro_expressions:list = prolist.read().replace('。', '').split('\n')
        con_expressions = conlist.read().replace('。', '').split('\n')
        others_expressions = otherslist.read().replace('。', '').split('\n')

    for pro_expression in pro_expressions:
        if pro_expression == '':
            continue
        if re.search(pro_expression, text):
            label = 1
            return label

    for con_expression in con_expressions:
        if con_expression == '':
            continue        
        if re.search(con_expression, text):        
            label = 0
            return label

    for others_expression in others_expressions:
        if others_expression == '':
            continue        
        if re.search(others_expression, text):        
            label = 2
            return label

    print(f'{text}')


    while True:
        try:
            try:
                label = input('==2:other, 1:pro, 0:con :  ')
                if label == '2':
                    reason = input('2の要因: ')  
                    if not reason == '':
                        with open('../text_list/others_list.txt', 'a', encoding='UTF-8') as f:
                            reason = unicodedata.normalize("NFKC", reason)     
                            f.write('\n' + reason) 
                            return label 
                    if reason == '':
                        return label                                       
                elif label == '1':
                    reason = input('賛成表現は: ')
                    if not reason == '':
                        with open('../text_list/pro_list.txt', 'a', encoding='UTF-8') as f:
                            reason = unicodedata.normalize("NFKC", reason) 
                            f.write('\n' + reason)
                            return label
                    if reason == '':
                        return label
                elif label == '0':
                    reason = input('反対表現: ')  
                    if not reason == '':
                        with open('../text_list/con_list.txt', 'a', encoding='UTF-8') as f:
                            reason = unicodedata.normalize("NFKC", reason)     
                            f.write('\n' + reason) 
                            return label
                    if reason == '':
                        return label                        
                elif label == '':
                    return label
            except KeyboardInterrupt:
                print("\nプログラムが終了しました。")  
                return 1
        except:
            print("入力エラーが発生しました。もう一度入力してください。")



def get_title(text):
    with open("../text_list/title_match.txt", "r") as title_match_file:
            title_match_list = title_match_file.read().split('\n')
            title_match_list = [re.sub(r'@(.*?)@', r'(.*)', pattern.replace("、", "").replace("＠", "@")) for pattern in title_match_list if pattern]
            title_match_pattern = '|'.join(title_match_list)
            matches = re.finditer(title_match_pattern, text, re.MULTILINE)
            if matches:
                print(text)
                print('\n\n')
                titles = {i: title.replace("、", "") for i, title in enumerate([title for match in matches for title in match.groups() if title is not None])}
                
                for i, title in titles.items():
                    print(f'{i} : {title}')

                while True:
                    print("=======================")
                    title = ''
                    try:
                        try:
                            if len(titles) == 0:
                                title ==  ''
                                return title
                            user_input = input("タイトルに合う数字を入力してください:")
                            if user_input.isdigit():
                                if int(user_input) in titles:
                                    try:
                                        title = titles[int(user_input)]
                                        with open('../text_list/title_list.txt', 'a', encoding='UTF-8', newline='\n') as f:   
                                            title = unicodedata.normalize("NFKC", title)
                                            f.write(title + '\n')
                                        return title 
                                    except:
                                        print("番号は存在しません")
                                        break
                                else:
                                    print("番号は存在しません")
                                    break
                            elif user_input == '':
                                title = ''
                                return title
                            else:
                                # タイトルを手入力した場合           エラーが発生する
                                with open('../text_list/title_match.txt', 'a', encoding='UTF-8', newline='\n') as f:
                                    user_input = unicodedata.normalize("NFKC", user_input)
                                    f.write(user_input + '\n') 
                                user_input = user_input.replace("＠", "@").replace("@", "")
                                title = user_input
                                return title
                        except KeyboardInterrupt:
                            print("\nプログラムが終了しました。")
                            return 1000
                    except ValueError:
                        print("入力エラーが発生しました。もう一度入力してください。") 
    return 0


#                     name_of_house,
#                    name_of_meeting,
def title():
    return 0



def main():
    """
    params:
        rows_title(list(list)) : その日のタイトルを保持
        rows_csv(list(list)) : その日のcsvファイルを保持
        row_csv(list) : 答弁セグメント
        title_csv(list) : タイトルセグメント
    """

    for i in range(2022, 2023):
        #todayの変更
        #16, 17, 18, 22, 23, 24, 25, 28, 29, 30, 31
        today = input("日付を入力して: ")
        csv_file_paths = glob.glob('/work/csv_data/' + str(i) + '_data/' + today + '.csv', recursive=True)
        title_file_paths = glob.glob('/work/title_data/' + str(i) + '_data/' + today + '.csv', recursive=True)
        csv_sorted_files = sorted(csv_file_paths, key=lambda x: tuple(map(int, re.findall(r'\d+', x))))        
        title_sorted_files = sorted(title_file_paths, key=lambda x: tuple(map(int, re.findall(r'\d+', x))))

        for csv_file, title_file in zip(csv_sorted_files, title_sorted_files):
            try:
                make_dir = '/work/full_data/' + str(i) + '_data'
#                make_dir = '/work/without_title_data/' + str(i) + '_data'
                if not os.path.exists(make_dir):
                    os.makedirs(make_dir)
            except Exception as e:
                continue            

            with open(csv_file, 'r') as csv_read_file, open(title_file, 'r') as title_read_file:
                reader_csv = csv.reader(csv_read_file)
                rows_csv = list(reader_csv)              
                reader_title = csv.reader(title_read_file)
                rows_title = list(reader_title)

            title = ''
            prev_title = ''
            for t, row_csv in enumerate(rows_csv):
                title = prev_title
                # 議長は入れない / 会議が変われば次は議長から
                if t == 0 or ((row_csv[2] != meeting) and (row_csv[1] != party)):
                    party = row_csv[1]          
                    meeting = row_csv[2]        #hoge委員会
                    speaker = row_csv[3]        #fooさん
                
                if not ((row_csv[3] == speaker) and (row_csv[1] == party) and (row_csv[2] == meeting)):
#                     idx = 0
                    with open('/work/full_data/' + str(i) + '_data/' + today + '.csv', 'a', encoding='UTF-8') as csv_write_file:
                        for row_title in rows_title:
                            row_title[8].replace('\n\n', '\n').replace('\n', ' ').replace('、', ' ')
                            candidate_title = row_title[8].split()
                            #row_title[8]が1つしかない場合はそれがタイトルである
                            if len(candidate_title) == 1 and row_csv[1] == row_title[1] and row_csv[2] == row_title[2]:
                                row_csv[6] = candidate_title[0]
                                title = row_csv[6]
                                row_csv[7] = get_label(row_csv[8])
                                if not row_csv[7] == '':
                                    row_csv[8] = row_csv[8].replace('10分', '十分')
                                    writer = csv.writer(csv_write_file)
                                    writer.writerow(row_csv)
                                    continue
                        
                        #先頭話者の場合
                        if title == '':
                            print(row_csv[8])
                            while True:
                                try:
                                    try:
                                        title = input("===先頭なのでタイトルを入力してください: ")
                                        row_csv[6] = title
                                        row_csv[7] = get_label(row_csv[8])
                                        writer = csv.writer(csv_write_file)
                                        writer.writerow(row_csv)
                                        prev_title = title
                                        idx = 1
                                        break                      
                                    except KeyboardInterrupt:
                                        print("\nプログラムが終了しました。")  
                                        return 1                                                     
                                except:
                                    print("入力エラーが発生しました。もう一度入力してください。")                                 
                        if not idx == 1:
                            #row_title[8]が2つ以上の場合
                            with open("../text_list/title_match.txt", "r") as title_match_file:
                                title_match_list = title_match_file.read().replace("、", "").replace("＠", "@").split('\n')
                                for title_match_pattern in title_match_list:
                                    #まず@ウクライナ情勢@について --> まず.*について
                                    title_match_pattern = re.sub(r"@.*@", "(.*)", title_match_pattern)
                                    matches = re.search(title_match_pattern, row_csv[8])
                                    if matches:                                          
                                        title = get_title(row_csv[8])
                                        if title == '':
                                            title = prev_title
                                            break
                                        else:
                                            break
                                    else:
                                        title  = prev_title
                                    
                                row_csv[6] = title.replace("＠", "@").replace("@", "")
                                row_csv[7] = get_label(row_csv[8])
                                if not row_csv[7] == '':
                                    row_csv[8] = row_csv[8].replace('10分', '十分')
                                    writer = csv.writer(csv_write_file)
                                    writer.writerow(row_csv)
                                
                                if not title == '':
                                    prev_title = title

if __name__ == "__main__":
    main()
