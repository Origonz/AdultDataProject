import requests 
import json
from bs4 import BeautifulSoup
from datetime import datetime
import time

with open("data.json", "r") as f:
    data = json.load(f)


time = datetime.timestamp(datetime.now())

for x in data:
    url = "https://fr.pornhub.com" + x
    with requests.get(url, stream=True) as r:
        html = r.text
        soup = BeautifulSoup(html, features="html5lib")
        det = soup.find_all(class_="video-action-tab about-tab active")
        if len(det) == 0 :
            view = -1
            percent = -1
        else:
            details = det[0]
            views = int(details.find_all(class_='count')[0].text.replace(" ", ""))
            percent = int(details.find_all(class_='percent')[0].text.split('%')[0])
        
        data[x]['evolution'].append({"time": time, "views": views, "percent": percent})   

        
with open("data.json", "w") as f:
    json.dump(data, f)
