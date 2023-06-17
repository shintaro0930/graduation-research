#!/bin/bash

# ディレクトリのパスを指定
directory="/work/csv_data/2021_data"

# 変数の初期化
total_lines=0
file_count=0

# ディレクトリ内のファイルの一覧を取得し、行数を出力および計算
for file in "$directory"/*; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file")
    filename=$(basename "$file")
    echo "$filename: $lines 行"
    total_lines=$((total_lines + lines))
    file_count=$((file_count + 1))
  fi
done

# 平均行数を計算して出力
if [ $file_count -gt 0 ]; then
  average=$((total_lines / file_count))
  echo "平均行数: $average 行"
fi
