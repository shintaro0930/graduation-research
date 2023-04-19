import xml.etree.ElementTree as ET
from collections import Counter
import glob

def main():
    count_by_speaker = Counter()

    file_paths = glob.glob('./data/2022_data/2022_12_74.xml', recursive=True)
    for file_path in file_paths:
        tree = ET.parse(file_path)
        root = tree.getroot()

        num = int(root[1].text)
        if root.find('nextRecordPosition') is not None:
            for i in range(num):
                count_by_speaker[root[4][i][0][0][6].text] += 1
        else:
            for i in range(num):
                count_by_speaker[root[3][i][0][0][6].text] += 1

    for speaker, count in sorted(count_by_speaker.items(), key=lambda x: -x[1]):
        print(count, speaker, sep='\t')

def get_speech():
    file_paths = glob.glob('./data/2022_data/2022_12_74.xml', recursive=True)
    for file_path in file_paths:
        tree = ET.parse(file_path)
        root = tree.getroot()

    speech_list = []

    for record in root.iter(tag='speechRecord'):
        speaker = record.find('speaker').text
        speaker_yomi = record.find('speakerYomi').text
        speech = record.find('speech').text

        # print(f'{speaker}({speaker_yomi}): {speech}')
        tmp_list = [speaker, speaker_yomi, speech]
        speech_list.append(tmp_list)

    with open('./result.txt', 'w') as f:
        for speech in speech_list:
            speaker = speech[0]
            speaker_yomi = speech[1]
            content = speech[2].replace('\u3000', ' ')
            f.write(f'{speaker}({speaker_yomi}): {content})\n')



if __name__ == "__main__":
    # main()
    get_speech()