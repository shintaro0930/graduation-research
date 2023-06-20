import csv
import glob
import matplotlib.pyplot as plt

path_files = glob.glob('/work/full_data/202*_data/*.csv', recursive=True)
label_counts = [0, 0, 0] 
total_count = 0  # 合計数

for file in path_files:
    with open(file, "r") as csv_file:
        reader_csv = csv.reader(csv_file)
        rows_csv = list(reader_csv)
        for row_csv in rows_csv:
            try:
                label = int(row_csv[7])
                label_counts[label] += 1
                total_count += 1
            except:
                pass

# ラベルの分布を棒グラフで表示
labels = ['Label 0', 'Label 1', 'Label 2']
plt.bar(labels, label_counts)
plt.xlabel('Label')
plt.ylabel('Count')
plt.title('Distribution of Labels')

# 合計数を表示
for i, count in enumerate(label_counts):
    plt.text(i, count + 10, f'Total Count: {count}', ha='center')

plt.savefig('../pictures/result2021.jpg')
#plt.show()

