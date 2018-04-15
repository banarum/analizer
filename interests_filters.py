import json

import os

dir = os.path.dirname(os.path.abspath(__file__))


with open(dir + "\\" + "skeleton_interests.json", encoding='utf-8') as fh:
    skeleton = json.load(fh)

print(len(skeleton))

for item in skeleton:
    interests = item["interests"]
    if len(interests)<5:
        skeleton.remove(item)
        continue

print(len(skeleton))

with open(dir + "\\" + "skeleton_interests_cleaned.json", 'w', encoding='utf8') as json_file:
    json.dump(skeleton, json_file, ensure_ascii=False)