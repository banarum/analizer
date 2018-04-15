import json

import os

dir = os.path.dirname(os.path.abspath(__file__))

with open(dir + "\\" + "skeleton_expanded.json", encoding='utf-8') as fh:
    skeleton = json.load(fh)

print(len(skeleton))

changes = 1
for i in range(len(skeleton)-1, -1, -1):
    for j in range(i-1, -1, -1):
        if skeleton[i]==skeleton[j]:
            del skeleton[j]
            i-=1
            j-=1

for item in skeleton:
    if item["openmind"]<=0:
        skeleton.remove(item)
        continue
    if item["popularity"]<2:
        skeleton.remove(item)
        continue
    if "age" in item and item["age"]<20:
        skeleton.remove(item)
        continue

print(len(skeleton))

with open(dir + "\\" + "skeleton_expanded_cleaned.json", 'w', encoding='utf8') as json_file:
    json.dump(skeleton, json_file, ensure_ascii=False)