import json
from datetime import datetime, timedelta
import sys
import json

# Netoyeur de données
# Si une vidéo est supprimé, on garde son nombre de vue avant suppression
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
    with open(name + '.json', 'w', encoding='utf-8') as f:
        json.dump(data_dict, f, ensure_ascii=False, indent=4)

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

# Compte la fluctuation de vue en fonction de la date
def toViewFluctuation(data_dict):
    data_time = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_time):
                data_time[d] = 0
            data_time[d] = data_time[d] + t["views"]
    data_fluc = {}
    viewL = 0
    last = 0
    viewC = {}
    for d in data_time:
        if last == 0:
            viewC[d] = 0
        else:
            viewC[d] = data_time[d] - viewL
            print(d," - ", viewC[d])
            data_fluc[d] = viewC[d] - viewC[last]
        viewL = data_time[d]
        last = d
    print("------")
    return data_fluc

# Compte le nombre de vue pour chaque jour de la semaine
# TODO Changer par rapport au fluctuations
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

# Recupere les videos supprimées
def deletedVideos(data_dict):
    videos = {}
    for video in data_dict:
        tmp = 0
        for t in data_dict[video]["evolution"]:
            if t["percent"] == -1:
                videos[video] = data_dict[video]
                break
    return videos

# Recupere les x pires videos (moins de vue)
def worseVideos(data_dict, x):
    videos = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            if t["percent"] == -1:
                videos[video] = -1
                break
            videos[video] = t["views"]

    clear_v = {}
    for v in videos:
        if videos[v] != -1:
            clear_v[v] = videos[v]

    v = sorted(clear_v.items(), reverse=False, key=lambda t: t[1])
    videos = {}
    del v[x:]
    for d in v:
        videos[d[0]] = data_dict[d[0]]
    return videos

# Recupere les x meilleures videos (nb de vue)
def bestVideos(data_dict, x):
    videos = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            videos[video] = t["views"]
    v = sorted(videos.items(), reverse=True, key=lambda t: t[1])
    videos = {}
    del v[x:]
    for d in v:
        videos[d[0]] = data_dict[d[0]]
    return videos

FILES = False

with open('data/data.json') as json_data:

    data_dict = json.load(json_data)

    if FILES:

        data_clean = DataClean(data_dict)

        deleted = deletedVideos(data_dict)
        dictToFile(deleted, "data/deleted")

        worse = worseVideos(data_dict, 200)
        dictToFile(worse, "data/worse")

        best = bestVideos(data_dict, 200)
        dictToFile(worse, "data/best")

        categories = toDataCategorie(data_clean)
        dictToFile(categories, "data/category")

        days = toDayView(data_clean)
        dictToFile(days, "data/days")

        views = toTimeView(data_clean)
        dictToFile(views, "data/views")

    else:

        data_clean = DataClean(data_dict)
        fluc = toViewFluctuation(data_clean)

        for d in fluc:
            print(d + " : " + str(fluc[d]))