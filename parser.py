import xml.etree.ElementTree as ET
import glob
import re

def convert_kanji_to_int(string):
    result = string.translate(str.maketrans("〇一二三四五六七八九", "0123456789", ""))
    convert_table = {"十": "0", "百": "00", "千": "000", "万": "0000", "億": "00000000", "兆": "000000000000", "京": "0000000000000000"}
    unit_list:list = "|".join(convert_table.keys())      # unit_list = 十|百|千|...
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

def main(): 
    file_paths = glob.glob('./data/2022_data/2022_12_74.xml', recursive=True)
    for file_path in file_paths:
        tree = ET.parse(file_path)
        root = tree.getroot()

    speech_list = []

    for record in root.iter(tag='speechRecord'):
        speaker = record.find('speaker').text
        speaker_yomi = record.find('speakerYomi').text
        speech = record.find('speech').text

        tmp_list = [speaker, speaker_yomi, speech]
        speech_list.append(tmp_list)

    with open('./tmp_result.txt', 'w') as f:
        for speech in speech_list:
            speaker = speech[0]
            speaker_yomi = speech[1]
            content = speech[2]
            # content = speech[2].replace('\u3000', ' ')
            f.write(f'{speaker}({speaker_yomi}): {content}\n\n')


# speech[2]に漢数字を数字に変換する必要がある。ただしその区別はついていない


if __name__ == "__main__":
    main()