import requests 
import json
from bs4 import BeautifulSoup
from datetime import datetime

data = {}
now = datetime.now()
time = datetime.timestamp(now)

for i in range(3, 4):
    url = "https://fr.pornhub.com/video?o=cm&page=" + str(i)
    with requests.get(url, stream=True) as r:
        html = r.text
        soup = BeautifulSoup(html, features="html5lib")
        videos = soup.find_all(class_="thumbnail-info-wrapper clearfix")

        for video in videos:
            link = video.find_all('a')[0].attrs['href']
            title = video.find_all('a')[0].attrs['title']
            
            url2 = "https://fr.pornhub.com" + link

            with requests.get(url2, stream=True) as r2:
                html2 = r2.text
                soup = BeautifulSoup(html2, features="html5lib")
                details = soup.find_all(class_="video-action-tab about-tab active")[0]
                categories = details.find_all(class_='categoriesWrapper')[0].find_all('a')
                auteur = details.find_all(class_='usernameWrap clearfix')[0].find_all('a')[0].text
                production = details.find_all(class_='productionWrapper')[0].find_all('a')[0].text
                listCategories = []
                for i in range(0, len(categories)-1):
                    listCategories.append(categories[i].text)

                views = details.find_all(class_='count')[0].text
                percent = details.find_all(class_='percent')[0].text.split('%')[0]

                evolution = []
                evolution.append({"time": time, "views": views, "percent": percent})    
                data[link] = {"title": title, "categories": listCategories, "auteur": auteur, "type": production, "evolution": evolution}


with open("data.json", "w") as f:
    json.dump(data, f)

