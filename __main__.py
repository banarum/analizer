import datetime
import json
import math
import time

import requests

queue = []

def get_followers(id, token, num):
    fields = "photo_id,verified,sex,bdate,city,country,home_town,has_photo,photo_50,online,domain,has_mobile,contacts," \
             "site,education,universities,schools,status,last_seen,followers_count,occupation,nickname,relatives," \
             "relation,personal,connections,exports,wall_comments,activities,interests,music,movies,tv,books,games,about," \
             "quotes,can_post,can_see_all_posts,can_see_audio,timezone,screen_name,maiden_name,career,military"

    url = "https://api.vk.com/method/users.getFollowers?v=5.74&access_token=" + token + "&"

    answer = requests.get(url + "fields=" + fields + "&user_id=" + id+"&count="+str(num))

    if answer.status_code != 200:
        return None

    result = []

    for item in json.loads(answer.text)["response"]["items"]:
        result.append(analize(item))

    return result

def get_interests_cloud(id, token):
    answer = requests.get(
        "https://api.vk.com/method/users.getSubscriptions?user_id=" + id + "&v=5.74&count=40&extended=1&access_token=" + token)
    if answer.status_code != 200:
        return None

    rsp = json.loads(answer.text)["response"]["items"]

    res = []

    for item in rsp:
        if item["type"] == "page" and "name" in item:
            res.append(item["name"])

    return res


def get_age(date):
        if (int(date.split(".")[2])<1971):
            return 2018-int(date.split(".")[2])
        return math.floor((time.time() - time.mktime(
            datetime.datetime.strptime(date, "%d.%m.%Y").timetuple())) / 60 / 60 / 24 / 365)


def calculate_oscore(rsp):
    score = 0
    if "bdate" in rsp and len(rsp["bdate"].split(".")) == 3:
        if get_age(rsp["bdate"]) < 50 and get_age(rsp["bdate"]) > 10:
            score += 1
    if "has_photo" in rsp and rsp["has_photo"] == 1:
        score += 1
    if "can_post" in rsp and rsp["can_post"] == 1:
        score += 4
    if "can_see_audio" in rsp and rsp["can_see_audio"] == 1:
        score += 3
    if "wall_comments" in rsp and rsp["wall_comments"] == 1:
        score += 3

    return score


def query_one(id, token):
    fields = "photo_id,verified,sex,bdate,city,country,home_town,has_photo,photo_50,online,domain,has_mobile,contacts," \
             "site,education,universities,schools,status,last_seen,followers_count,occupation,nickname,relatives," \
             "relation,personal,connections,exports,wall_comments,activities,interests,music,movies,tv,books,games,about," \
             "quotes,can_post,can_see_all_posts,can_see_audio,timezone,screen_name,maiden_name,career,military"

    url = "https://api.vk.com/method/users.get?v=5.74&access_token=" + token + "&"

    answer = requests.get(url + "fields=" + fields + "&user_id=" + id)

    if answer.status_code != 200:
        return None

    rsp = json.loads(answer.text)["response"][0]

    result = analize(rsp)

    return result


def analize(rsp):
    # looking for basic info
    result = {"female": rsp["sex"] == 1}
    result["name"] = rsp["first_name"]
    result["surname"] = rsp["last_name"]
    if "bdate" in rsp and len(rsp["bdate"].split(".")) == 3:
        result["age"] = get_age(rsp["bdate"])

    if "popularity" in rsp:
        result["popularity"] = round(rsp["followers_count"] / 100)

    result["openmind"] = calculate_oscore(rsp)

    #result["interests"] = get_interests_cloud(rsp["id"], token)

    if "country" in rsp:
        result["country"] = rsp["country"]

    if "city" in rsp:
        result["city"] = rsp["city"]

    if "site" in rsp:
        result["site"] = rsp["site"]

    result["id"] = rsp["id"]

    return result

task = 50

token = "7b34d3ea7b34d3ea7be146e8007b6e989077b347b34d3ea23f7f84ba9d7cdf73eed934c"

import os
import codecs

dir = os.path.dirname(os.path.abspath(__file__))

def update_file():
    with open(dir + "\\" + "users.json", 'w', encoding='utf8') as json_file:
        json.dump(queue, json_file, ensure_ascii=False)


user = "401112366"
user_me = "170751373"

number = 2000

first_queue = get_followers(user_me, token, 300)

with open(dir + "\\" + "users.json", encoding='utf-8') as fh:
    queue = json.load(fh)

for i in range(len(queue)):
    print(i)
    item = queue[i]
    if "interests" in item:
        continue
    data = get_interests_cloud(str(item["id"]), token)
    queue[i]["interests"] = data
    update_file()

update_file()

