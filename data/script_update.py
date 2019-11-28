import requests 
import json
from bs4 import BeautifulSoup
from datetime import datetime
#import time as timeL

with open("data.json", "r") as f:
    data = json.load(f)


time = datetime.timestamp(datetime.now())

#start_time = timeL.time()

for x in data:
    url = "https://fr.pornhub.com" + x
    html = requests.get(url).text
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
#    print(len(data))
#    print("Temps d execution : %s secondes ---" % (timeL.time() - start_time))

