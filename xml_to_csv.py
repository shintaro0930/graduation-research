import xml.etree.ElementTree as ET
import glob
import csv
import os
import re

"""
xml -> csv

参考リンク
https://qiita.com/Robot-Inventor/items/2264590f392a1a9e8831
"""

import re

def convert_kanji_to_int(string):
    result = string.translate(str.maketrans("〇一二三四五六七八九", "0123456789", ""))
    convert_table = {"十": "0", "百": "00", "千": "000", "万": "0000"}
    unit_list = "|".join(convert_table.keys())

    # 年代
    result = re.sub(r"年代(\D+)(\d+)", lambda x: f"年代{x.group(1)}{int(x.group(2))}", result)
    # 年齢
    result = re.sub(r"(\d+)歳", lambda x: str(int(x.group(1))), result)
    # 金額
    result = re.sub(r"(\d+)円", lambda x: str(int(x.group(1))), result)

    # 年
    result = re.sub(r"(\d+)年", lambda x: str(int(x.group(1))), result)

    while re.search(unit_list, result):
        for unit in convert_table.keys():
            zeros = convert_table[unit]
            for numbers in re.findall(f"(\d+){unit}(\d+)", result):
                result = result.replace(numbers[0] + unit + numbers[1], numbers[0] + zeros[len(numbers[1]):len(zeros)] + numbers[1])
            for number in re.findall(f"(\d+){unit}", result):
                result = result.replace(number + unit, number + zeros)
            for number in re.findall(f"{unit}(\d+)", result):
                result = result.replace(unit + number, "1" + zeros[len(number):len(zeros)] + number)
            result = result.replace(unit, "1" + zeros)
    return result


def count_file(dir_path) -> int:
    count:int = 0
    for file in os.listdir(dir_path):
        file_path = os.path.join(dir_path, file)

        if os.path.isfile(file_path):
            count += 1
    return count

def main():
    # xmlから取ってくる
    # 日付ごとにtsvファイルを分けたい
    # できれば上から順番になるようにしたい

    """rangeの日付は適宜変更"""
    for i in range(2022, 2023):
#    for i in range(1947, 2023):
        file_paths:list = glob.glob('/work/data/' + str(i) + '_data/*.xml', recursive=True)
        for file in file_paths:
            tree = ET.parse(file)
            root = tree.getroot()

            try:
                make_dir = '/work/tmp_data/' + str(i) + '_data'
            #    make_dir = '/work/csv_data/' + str(i) + '_data'
                if not os.path.exists(make_dir):
                    os.makedirs(make_dir)
            except Exception as e:
                continue            

            for record in root.iter(tag='speechRecord'):
                speech_list = []
                speaker = record.find('speaker').text
                speaker_yomi = record.find('speakerYomi').text
                speech = record.find('speech').text
                date = record.find('date').text
                speaker_group = record.find('speakerGroup').text
                name_of_house = record.find('nameOfHouse').text
                name_of_meeting = record.find('nameOfMeeting').text
                
                speech_list.append([
                    date, 
                    name_of_house, 
                    name_of_meeting, 
                    speaker, 
                    speaker_yomi, 
                    speaker_group, 
                    convert_kanji_to_int(speech)
                ])
                with open('/work/tmp_data/' + str(i) + '_data/' + str(date) + '.csv', mode='a') as f:
#                with open('/work/csv_data/' + str(i) + '_data/' + str(date) + '.csv', mode='a') as f:
                    writer = csv.writer(f) 
                    writer.writerows(speech_list)
                print(speech_list)


if __name__ == "__main__":
    main()