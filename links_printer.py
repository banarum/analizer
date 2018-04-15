import json

import os

dir = os.path.dirname(os.path.abspath(__file__))

def get_link(obj):
    return "https://vk.com/id"+str(obj["id"])

with open(dir + "\\" + "skeleton_interests_cleaned.json", encoding='utf-8') as fh:
    skeleton = json.load(fh)

for item in skeleton:
    print(get_link(item))
