import json
from datetime import datetime

def toDataCategorie(data_dict):
    data_cat = {}
    vid_cat = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_cat):
                data_cat[d] = {}
            for c in data_dict[video]["categories"]:
                if not(c in vid_cat):
                    vid_cat[c] = 0
                if not(c in data_cat[d]):
                    data_cat[d][c] = 0
                vid_cat[c] = vid_cat[c] + 1
                data_cat[d][c] = data_cat[d][c] + t["views"]
    for t in data_cat:
        for c in data_cat[t]:
            data_cat[t][c] = data_cat[t][c] / vid_cat[c]
        d = sorted(data_cat[t].items(), key=lambda t: t[1])
        data_cat[t] = d
    return data_cat

def toDayView(data_dict): #A refaire
    data_day = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%a')
            if not(d in data_day):
                data_day[d] = 0
            data_day[d] = data_day[d] + t["views"]
    return data_day

def toTimeView(data_dict): #A refaire - nb de vue qui diminue
    data_time = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_time):
                data_time[d] = 0
            data_time[d] = data_time[d] + t["views"]
    return data_time

with open('data.json') as json_data:
    data_dict = json.load(json_data)
    
    data_day = toDataCategorie(data_dict)

    for d in data_day:
        print(d + " : " + str(data_day[d]))