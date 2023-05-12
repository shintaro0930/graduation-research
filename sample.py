import re

def find_following_sentence(text):
    # テキストを単語に分割する
    words = text.split()
    print(words)
    # パターンマッチでキーワードを検索する
    pattern = r"本日の会議に付した案件"
    match = re.search(pattern, text)

    result = words[1:]

    result = []
    for i in range(1, len(words)):
        result.append(words[i])
        print(words[i])
    return result

def main():
    print(find_following_sentence("本日の会議に付した案件\n○理事補欠選任の件\n○継続調査要求に関する件\n○委員派遣に関する件"))

if __name__ == "__main__":
    main()