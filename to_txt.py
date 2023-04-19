import xml.etree.ElementTree as ET
import glob

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

        # print(f'{speaker}({speaker_yomi}): {speech}')
        tmp_list = [speaker, speaker_yomi, speech]
        speech_list.append(tmp_list)

    with open('./result.txt', 'w') as f:
        for speech in speech_list:
            speaker = speech[0]
            speaker_yomi = speech[1]
            content = speech[2].replace('\u3000', ' ')
            f.write(f'{speaker}({speaker_yomi}): {content}\n\n')



if __name__ == "__main__":
    main()