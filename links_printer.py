import json

import os

dir = os.path.dirname(os.path.abspath(__file__))

def get_link(obj):
    return "https://vk.com/id"+str(obj["id"])

with open(dir + "\\" + "skeleton_interests_cleaned.json", encoding='utf-8') as fh:
    skeleton = json.load(fh)

cities = {}

for item in skeleton:
    if "city" in item:
        city = item["city"]["title"]
        if not (city in cities):
            cities[city] = []
        cities[city].append(get_link(item))

with open(dir + "\\" + "results_by_cities.json", 'w', encoding='utf8') as json_file:
    json.dump(cities, json_file, ensure_ascii=False)
