import json
import math

import time

import datetime

import requests


class ScanAPI:
    def __init__(self, token):
        self.token = token

    def get_age(self, date):
        if (int(date.split(".")[2]) < 1971):
            return 2018 - int(date.split(".")[2])
        return math.floor((time.time() - time.mktime(
            datetime.datetime.strptime(date, "%d.%m.%Y").timetuple())) / 60 / 60 / 24 / 365)

    def calculate_score(self, rsp):
        score = 0
        if "bdate" in rsp and len(rsp["bdate"].split(".")) == 3:
            if self.get_age(rsp["bdate"]) < 50 and self.get_age(rsp["bdate"]) > 10:
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

    def calculate_oscore(self, rsp):
        score = 0
        if "bdate" in rsp and len(rsp["bdate"].split(".")) == 3:
            if self.get_age(rsp["bdate"]) < 50 and self.get_age(rsp["bdate"]) > 10:
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

    def get_interests_cloud(self, id):
        answer = requests.get(
            "https://api.vk.com/method/users.getSubscriptions?user_id=" + id + "&v=5.74&count=40&extended=1&access_token=" + self.token)
        if answer.status_code != 200:
            return None
        rsp = json.loads(answer.text)["response"]["items"]
        res = []
        for item in rsp:
            if item["type"] == "page" and "name" in item:
                res.append(item["name"])

        return res

    def analize(self, rsp):
        # looking for basic info
        result = {"female": rsp["sex"] == 1}
        result["name"] = rsp["first_name"]
        result["surname"] = rsp["last_name"]
        if "bdate" in rsp and len(rsp["bdate"].split(".")) == 3:
            result["age"] = self.get_age(rsp["bdate"])

        if "followers_count" in rsp:
            result["popularity"] = round(rsp["followers_count"] / 100)

        result["openmind"] = self.calculate_oscore(rsp)

        if "country" in rsp:
            result["country"] = rsp["country"]

        if "city" in rsp:
            result["city"] = rsp["city"]

        if "site" in rsp:
            result["site"] = rsp["site"]

        result["id"] = rsp["id"]

        return result

    def get_followers(self, id, num):
        fields = "photo_id,verified,sex,bdate,city,country,home_town,has_photo,photo_50,online,domain,has_mobile,contacts," \
                 "site,education,universities,schools,status,last_seen,followers_count,occupation,nickname,relatives," \
                 "relation,personal,connections,exports,wall_comments,activities,interests,music,movies,tv,books,games,about," \
                 "quotes,can_post,can_see_all_posts,can_see_audio,timezone,screen_name,maiden_name,career,military"

        url = "https://api.vk.com/method/users.getFollowers?v=5.74&access_token=" + self.token + "&"

        answer = requests.get(url + "fields=" + fields + "&user_id=" + id + "&count=" + str(num))

        if answer.status_code != 200:
            return None

        result = []

        for item in json.loads(answer.text)["response"]["items"]:
            result.append(self.analize(item))

        return result