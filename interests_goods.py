import json

import os

dir = os.path.dirname(os.path.abspath(__file__))

from ScanAPI import ScanAPI

token = "7b34d3ea7b34d3ea7be146e8007b6e989077b347b34d3ea23f7f84ba9d7cdf73eed934c"

limit = 2000

with open(dir + "\\" + "skeleton_expanded_cleaned.json", encoding='utf-8') as fh:
    skeleton = json.load(fh)

scanner = ScanAPI(token)

for i in range(len(skeleton)):
    item = skeleton[i]
    print(str(i + 1) + "/" + str(len(skeleton)))
    if "interests" in item:
        continue
    interests = scanner.get_interests_cloud(str(item["id"]))
    item["interests"] = interests
    with open(dir + "\\" + "skeleton_interests.json", 'w', encoding='utf8') as json_file:
        json.dump(skeleton, json_file, ensure_ascii=False)

print(len(skeleton))