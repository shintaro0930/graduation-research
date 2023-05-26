import glob
import csv
import re
import os


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
    csv_date = '2022-02-02.csv'
    for i in range(2022, 2023):
        row = []
        # file_paths = glob.glob('/work/csv_data/' + str(i) + '_data/*.csv', recursive=True)
        file_paths = glob.glob('/work/csv_data/' + str(i) + '_data/' + csv_date, recursive=True)

        for file in file_paths:
            with open(file, 'r') as csv_read_file:
                reader = csv.reader(csv_read_file)
                rows = list(reader)
            
            try:
                make_dir = '/work/label_data/' + str(i) + '_data'
                if not os.path.exists(make_dir):
                    os.makedirs(make_dir)
            except Exception as e:
                continue

            for row in rows:
                print(row[8])
                while True:

                    # 質問なのか、応答なのかの分類
                    # 正規表現で賛成なのか、反対なのか
                    # 議題の取得2

                    # 漢数字 + 10分　が出てきたら適宜出力 
                    # それをそのままにするのか or アラビア数字に直すか
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
                                


                    user_input = input("1: 賛成, 0: 反対, 2: どちらでもない, 3: 議題を含む: , 4:ゴミ: ")
                    if user_input in ['0', '1', '2', '3', '4']:
                        print("入力された値:", user_input)
                        row[7] = user_input 
                        with open('/work/label_data/' + str(i) + '_data/' + csv_date, 'a') as csv_write_file:
                            writer = csv.writer(csv_write_file)
                            writer.writerow(row)
                        break
                    else:
                        print("無効な入力です")

if __name__ == "__main__":
    main()
