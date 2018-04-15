import json

import os

dir = os.path.dirname(os.path.abspath(__file__))

from ScanAPI import ScanAPI

token = "7b34d3ea7b34d3ea7be146e8007b6e989077b347b34d3ea23f7f84ba9d7cdf73eed934c"

start_point = "11106424"

scanner = ScanAPI(token)

followers = scanner.get_followers(start_point, 200)

with open(dir + "\\" + "skeleton.json", 'w', encoding='utf8') as json_file:
    json.dump(followers, json_file, ensure_ascii=False)

print(len(followers))