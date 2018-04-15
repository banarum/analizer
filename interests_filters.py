import json

import os

dir = os.path.dirname(os.path.abspath(__file__))


def filter(arr, filters):
    result = []
    for item in arr:
        interests = item["interests"]
        broken = False
        for obj in interests:
            for filter in filters:
                if filter in obj:
                    result.append(item)
                    arr.remove(item)
                    broken = True
                    break
            if broken:
                break
    return result


with open(dir + "\\" + "skeleton_interests.json", encoding='utf-8') as fh:
    skeleton = json.load(fh)

print(len(skeleton))

for item in skeleton:
    interests = item["interests"]
    if len(interests) < 5:
        skeleton.remove(item)
        continue

filter1 = filter(skeleton, ["бесплатн", "даром", "обмен"])

for item in filter1:
    for obj in skeleton:
        if item["id"]==obj["id"]:
            skeleton.remove(obj)

print(len(skeleton))

result = filter(skeleton, ["инвестиц", "инвест", "вложение"])

print(len(result))

with open(dir + "\\" + "skeleton_interests_cleaned.json", 'w', encoding='utf8') as json_file:
    json.dump(result, json_file, ensure_ascii=False)
