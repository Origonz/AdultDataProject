import json
from datetime import datetime

def toDataCategorie(data_dict):
    data_cat = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_cat):
                data_cat[d] = {}
            for c in data_dict[video]["categories"]:
                if not(c in data_cat[d]):
                    data_cat[d][c] = 0
                data_cat[d][c] = data_cat[d][c] + t["views"]
    return data_cat

with open('data.json') as json_data:
    data_dict = json.load(json_data)
    data_cat = toDataCategorie(data_dict)
    for d in data_cat:
        print(d + " : " + str(data_cat[d]))
        break