import requests 
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time
import re

with open("../data/data.json", "r") as f:
    data = json.load(f)


time = datetime.timestamp(datetime.now())
count = 0

for x in data:
    if "duration" not in data[x] or data[x]['duration'] == "None":
        print("-------")
        print("Champ vide : ", data[x]['duration'])
        url = "https://fr.pornhub.com" + x
        with requests.get(url, stream=True) as r:
            print("Connexion")
            html = r.text
            soup = BeautifulSoup(html, features="lxml")
            print(soup.find_all(class_="original mainPlayerDiv"))
            time_script = soup.find_all(class_="original mainPlayerDiv")[0].find("script")
            print("Parcours scrip")
            pattern = re.compile("\"video_duration\":\"\d+\"") 
            var = pattern.search(time_script.text)
            time = var.group().split("\"")[3]
            print("Valeur récupéré : ", time)

            # except AttributeError:
            #     print("Pub ", count)
            #     time = "None"
            #     count += 1
            data[x]['duration'] = time 

print("Nombre de vidéos sans durée : ", count)


with open("../data/data.json", "w") as f:
    json.dump(data, f)


