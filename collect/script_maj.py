import requests 
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

with open("data.json", "r") as f:
    data = json.load(f)


time = datetime.timestamp(datetime.now())

for x in data:
    url = "https://fr.pornhub.com" + x
    with requests.get(url, stream=True) as r:
        html = r.text
        soup = BeautifulSoup(html, features="lxml")
        det = soup.find_all(class_="video-action-tab about-tab active")
        if len(det) == 0 :
            view = -1
            percent = -1
            data[x]['tags'] = 'deleted'
            data[x]['duration'] = 'None'
        else:
            details = det[0]
            if "tags" not in data[x]:
                tags = details.find_all(class_='tagsWrapper')[0].find_all('a')
                listTags = []
                for i in range(0, len(tags)-1):
                        listTags.append(tags[i].text)
                data[x]['tags'] = listTags

            if "duration" not in data[x] or data[x]['duration'] is None:
                try:
                    time_script = soup.find_all(class_="original mainPlayerDiv")[0].find("script")
                    pattern = re.compile("\"video_duration\":\"\d+\"") 
                    var = pattern.search(time_script.text)
                    time = var.group().split("\"")[3]
                except AttributeError:
                    time = None
                data[x]['duration'] = time 

            max_view = 0
            for e in data[x]['evolution']:
                if e['views'] > max_view:
                    max_view = e['views']
            try:
                duration = int(data[x]['duration'])
                data[x]['cost'] = (duration * max_view) * 0.25
            except ValueError:
                continue
            except TypeError:
                continue


with open("data.json", "w") as f:
    json.dump(data, f)


