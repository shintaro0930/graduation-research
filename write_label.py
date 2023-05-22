import glob
import csv
import re
import os

def main():
    csv_date = '2022-01-17.csv'
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
                    user_input = input("1: 賛成, 0: 反対, 2: どちらでもない, 3: 議題を含む: , 4:ゴミ")
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
