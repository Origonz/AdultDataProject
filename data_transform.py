import json
from datetime import datetime, timedelta
import sys

# Netoyeur de données
# si une vidéo est supprimé, on garde son nombre de vue avant suppression
def DataClean(data_dict):
    for video in data_dict:
        tmp = 0
        for t in data_dict[video]["evolution"]:
            if t["percent"] == -1:
                t["views"] = tmp
            else:
                tmp = t["views"]
    return data_dict

# Transforme les tuples en dictionnaire
def tupleToDict(data_tuple):
    data_dict = {}
    for d in data_tuple:
        data_dict[d] = {}
        for c in data_tuple[d]:
            data_dict[d][c[0]] = c[1]
    return data_dict

# Ecrire dans fichier
def dictToFile(data_dict, name):
    fh = open(name + ".json", "w") 
    fh.write(str(data_day).replace("'","\""))
    fh.close()

# Transforme les données en views par categorie
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
    for t in data_cat:
        d = sorted(data_cat[t].items(), reverse=True, key=lambda t: t[1])
        data_cat[t] = d
    return tupleToDict(data_cat)

# compte le nombre de vue pour chaque jour de la semaine
def toDayView(data_dict):
    data_day = {}
    for video in data_dict:
        tmp_date = {}
        for t in data_dict[video]["evolution"]:
            h = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y')
            last = datetime.utcfromtimestamp(t["time"] - 86400).strftime('%d-%m-%Y')
            if last in tmp_date:
                if h in tmp_date:
                    v = t["views"] - tmp_date[h]
                    tmp_date[h] = t["views"]
                else:
                    v = t["views"] - tmp_date[last]
            else:
                v = t["views"]
            tmp_date[h] = t["views"]
            d = datetime.utcfromtimestamp(t["time"]).strftime('%a')
            if not(d in data_day):
                data_day[d] = 0
            data_day[d] = data_day[d] + v
    return data_day

# Compte le nombre de vue en fonction de la date
def toTimeView(data_dict):
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

    data_dict = DataClean(data_dict)

    data_day = toTimeView(data_dict)

    for d in data_day:
        print(d + " : " + str(data_day[d]))