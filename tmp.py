import re

with open("a.txt") as f:
    result = re.sub(r"○(.*)　", "", f.readlines()[0])
    print(result)