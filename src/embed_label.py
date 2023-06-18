import glob
import csv 
import re
import os
import unicodedata



def get_label(text) -> int:
    with open('../text_list/pro_list.txt', 'r') as prolist, open('../text_list/con_list.txt', 'r') as conlist, open('../text_list/others_list.txt', 'r') as otherslist, open('../text_list/remove_list.txt', 'r') as removelist:
        pro_expressions:list = prolist.read().replace('。', '').split('\n')
        con_expressions = conlist.read().replace('。', '').split('\n')
        others_expressions = otherslist.read().replace('。', '').split('\n')
        remove_expressions = removelist.read().split('\n')

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
        
    for remove_expression in remove_expressions:
        if remove_expression == '':
            continue        
        if re.search(remove_expression, text): 
            return None

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
                label = input('==\'\':other, 0:ゴミ :  ')
                if label == '':
                    label = 0
                    return label
                    reason = input('others要因: ')  
                    if not reason == '':
                        with open('../text_list/others_list.txt', 'a', encoding='UTF-8') as f:
                            reason = unicodedata.normalize("NFKC", reason) 
                            f.write('\n' + reason)
                            return label
                    if reason == '':
                        return label
                elif label == '8':
                    return label
                    reason = input('賛成表現は: ')
                    if not reason == '':
                        with open('../text_list/pro_list.txt', 'a', encoding='UTF-8') as f:
                            reason = unicodedata.normalize("NFKC", reason) 
                            f.write('\n' + reason)
                            return label
                    if reason == '':
                        return label
                elif label == '9':
                    return label                    
                    reason = input('反対表現: ')  
                    if not reason == '':
                        with open('../text_list/con_list.txt', 'a', encoding='UTF-8') as f:
                            reason = unicodedata.normalize("NFKC", reason)     
                            f.write('\n' + reason) 
                            return label
                    if reason == '':
                        return label                        
                elif label == '0':
                    return None
            except KeyboardInterrupt:
                print("\nプログラムが終了しました。")  
                return 1
        except:
            print("入力エラーが発生しました。もう一度入力してください。")



def shape_title(title) -> list:
    return_list = []
    title = title.replace(r',+', ',').replace('\n\n', '\n').replace('\n', '').replace('件', '件@').replace('について', 'について@').replace('調査', '調査@').replace('法律案', '法律案@')
    title = title.replace(r'\（[^)]*\）', '')
    title = ','.join(filter(None, title.split(','))).lstrip(',')
    title_list = title.split('@')
    for text in title_list:
        if not (text == '' or text == '政府参考人の出席要求に関する件'):
            return_list.append(text.replace(',', ''))
    return_title = ",".join(return_list)
    return return_title


def main():
    for i in range(2020, 2021):
        today = '2020-*'
        csv_file_paths = glob.glob('/work/csv_data/' + str(i) + '_data/' + today + '.csv', recursive=True)
        title_file_paths = glob.glob('/work/title_data/' + str(i) + '_data/' + today + '.csv', recursive=True)
        csv_sorted_files = sorted(csv_file_paths, key=lambda x: tuple(map(int, re.findall(r'\d+', x))))        
        title_sorted_files = sorted(title_file_paths, key=lambda x: tuple(map(int, re.findall(r'\d+', x))))

        for csv_file, title_file in zip(csv_sorted_files, title_sorted_files):
            try:
                make_dir = '/work/full_data/' + str(i) + '_data'
                if not os.path.exists(make_dir):
                    os.makedirs(make_dir)
            except Exception :
                continue

            with open(csv_file, 'r') as csv_read_file, open(title_file, 'r') as title_read_file:
                reader_csv = csv.reader(csv_read_file)
                rows_csv = list(reader_csv)              
                reader_title = csv.reader(title_read_file)
                rows_title = list(reader_title)        
            
            for t, row_csv in enumerate(rows_csv):
                if t == 0 or ((row_csv[2] != meeting) and (row_csv[1] != party)):
                    party = row_csv[1]          
                    meeting = row_csv[2]        #hoge委員会
                    speaker = row_csv[3]        #fooさん

                date = row_csv[0]
                if not ((row_csv[3] == speaker) and (row_csv[1] == party) and (row_csv[2] == meeting)):    
                    with open(f'/work/full_data/{str(i)}_data/{date}.csv', 'a', encoding='UTF-8') as csv_write_file: 
                        row_csv[7] = get_label(row_csv[8])
                        if not row_csv[7] == None:
                            for row_title in rows_title:
                                if row_title[0] == row_csv[0] and row_title[1] == row_csv[1] and row_title[2] == row_csv[2]:
                                    # 本当は、件、調査、法律案で分ける、()は消す
                                    row_title[8] = shape_title(row_title[8])
                                    row_csv[6] = row_title[8]
                                    row_csv[8] = row_csv[8].replace('10分', '十分')
                                    if not (row_csv[7] == ''):
                                        writer = csv.writer(csv_write_file)
                                        writer.writerow(row_csv) 
    return 0


if __name__ == "__main__":
    main()