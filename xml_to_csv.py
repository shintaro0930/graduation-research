import xml.etree.ElementTree as ET
import glob
import re
import csv
import os

"""
xml -> tsv
"""

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
        file_paths:list = glob.glob('/work/data/' + str(i) + '_data/*.xml', recursive=True)
        for file in file_paths:
            tree = ET.parse(file)
            root = tree.getroot()
            speech_list = []

            for record in root.iter(tag='speechRecord'):
                speaker = record.find('speaker').text
                speaker_yomi = record.find('speakerYomi').text
                speech = record.find('speech').text
                date = record.find('date').text
                speaker_group = record.find('speakerGroup').text
                name_of_house = record.find('nameOfHouse').text
                name_of_meeting = record.find('nameOfMeeting').text

                # tmp_list = [date, speaker, speaker_yomi, speech, speaker_group, name_of_house, name_of_meeting]
                # speech_list.append(tmp_list)
                speech_list.append([
                    date, 
                    name_of_house, 
                    name_of_meeting, 
                    speaker, 
                    speaker_yomi, 
                    speaker_group, 
                    speech
                ])
            
            # ファイル作成


            # ファイル書き込み
            try:
                make_dir = '/work/csv_data/' + str(i) + '_data'
                if not os.path.exists(make_dir):
                    os.makedirs(make_dir)
            except Exception as e:
                continue

            with open('/work/csv_data/' + str(i) + '_data/' + str(date) + '.csv', mode='w') as f:
                writer = csv.writer(f) 
                writer.writerows(speech_list)


if __name__ == "__main__":
    main()