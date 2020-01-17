import json
from datetime import datetime, timedelta
import sys
import json
import csv

# Netoyeur de données
# Si une vidéo est supprimé, on garde son nombre de vue avant suppression
def DataClean(data_dict):
    for video in data_dict:
        tmp = 0
        if "cost" in data_dict[video]:
            if data_dict[video]["cost"] == "None":
                data_dict[video]["cost"] = 0
        if "duration" in data_dict[video] or data_dict[video]["duration"] == "None" :
            data_dict[video]["duration"] = 5
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
        data_dict = {}
        for c in data_tuple:
            data_dict[c[0]] = c[1]
    return data_dict

def dictToCSV(data_dict, name):
    with open(name + '.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        row = ["date","cost","views"]
        spamwriter.writerow(row)
        for i in data_dict:
            row = []
            row.append(i)
            for j in data_dict[i]:
                row.append(data_dict[i][j])
            spamwriter.writerow(row)

def nameToRef(data_dict):
    dict_cat = {}
    cat = []
    ano = []
    for video in data_dict:
        for c in data_dict[video]["categories"]:
            if not(c in cat):
               cat.append(c)

    while len(cat) > 0:
        c = cat.pop()
        fin = True
        s = c.split(" ")
        nb = 0
        while fin:
            nb = nb + 1
            r = ""
            for m in s:
                r = r + m[:nb]
            if not(r in ano) :
                ano.append(r)
                dict_cat[c] = r
                fin = False
    return dict_cat

def toNewViewCost(data_dict):
    data_time = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_time):
                data_time[d] = 0
            data_time[d] = data_time[d] + t["views"]
    data_NV = {}
    viewL = 0
    last = 0
    viewC = {}
    for d in data_time:
        if not(d in data_NV):
            data_NV[d] = {}
        if last == 0:
            viewC[d] = 0
        else:
            viewC[d] = data_time[d] - viewL
        duration = int(data_dict[video]["duration"])
        if duration < 10:
            dur = duration
        else:
            dur = 10
        data_NV[d]["cost"] = viewC[d] * dur
        data_NV[d]["views"] = viewC[d]
        viewL = data_time[d]
        last = d
    return data_NV

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

def toDataCategorieCost(data_dict):
    data_cat = {}
    for video in data_dict:
        if "cost" in data_dict[video]:
            for c in data_dict[video]["categories"]:
                if not(c in data_cat):
                    data_cat[c] = 0
                data_cat[c] = data_cat[c] + data_dict[video]["cost"]
    d = sorted(data_cat.items(), reverse=True, key=lambda t: t[0])
    return tupleToDict(d)

# Transforme les données en views par mots
def toDataTitleWords(data_dict):
    data_cat = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_cat):
                data_cat[d] = {}
            for c in data_dict[video]["title"].split(" "):
                c = c.lower()
                if not(c in data_cat[d]):
                    data_cat[d][c] = 0
                data_cat[d][c] = data_cat[d][c] + t["views"]
    for t in data_cat:
        d = sorted(data_cat[t].items(), reverse=True, key=lambda t: t[1])
        data_cat[t] = d
    return tupleToDict(data_cat)

# Transforme les données en views par tags
def toDataTags(data_dict):
    data_cat = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_cat):
                data_cat[d] = {}
            for c in data_dict[video]["tags"]:
                c = c.lower()
                if not(c in data_cat[d]):
                    data_cat[d][c] = 0
                data_cat[d][c] = data_cat[d][c] + t["views"]
    for t in data_cat:
        d = sorted(data_cat[t].items(), reverse=True, key=lambda t: t[1])
        data_cat[t] = d
    return tupleToDict(data_cat)

# Transforme les données en views par tags
def toDataDuration(data_dict):
    data_cat = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_cat):
                data_cat[d] = {}
            c = data_dict[video]["duration"]
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
            data_fluc[d] = viewC[d] - viewC[last]
        viewL = data_time[d]
        last = d
    return data_fluc

# Compte la fluctuation de vue en fonction de la date et de la moyenne
def toViewFluctuationMoyenne(data_dict):
    data_time = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_time):
                data_time[d] = 0
            data_time[d] = data_time[d] + t["views"]

    data_NV = toNewView(data_dict)
    moyenne = 0
    for i in data_NV:
        moyenne = moyenne + data_NV[i]
    moyenne = round(moyenne / len(data_NV))

    data_flucM = {}
    viewL = 0
    last = 0
    viewC = {}
    for d in data_time:
        if last == 0:
            viewC[d] = 0
        else:
            viewC[d] = data_time[d] - viewL
            data_flucM[d] = viewC[d] - moyenne
        viewL = data_time[d]
        last = d
    data_flucM["Moyenne"] = moyenne
    return data_flucM

# Compte le nombre de nouvelles vues par date
def toNewView(data_dict):
    data_time = {}
    for video in data_dict:
        for t in data_dict[video]["evolution"]:
            d = datetime.utcfromtimestamp(t["time"]).strftime('%d-%m-%Y %H:%M:%S')
            if not(d in data_time):
                data_time[d] = 0
            data_time[d] = data_time[d] + t["views"]
    data_NV = {}
    viewL = 0
    last = 0
    viewC = {}
    for d in data_time:
        if last == 0:
            viewC[d] = 0
        else:
            viewC[d] = data_time[d] - viewL
            data_NV[d] = viewC[d]
        viewL = data_time[d]
        last = d
    return data_NV

# Compte le nombre de vue pour chaque jour de la semaine en utilisant le nombre de vue ajouté par jour
def toDayView(data_dict):
    newView = toNewView(data_dict)
    data_day = {}
    for i in newView:
        datetime_object = datetime.strptime(i, '%d-%m-%Y %H:%M:%S')
        d = datetime_object.strftime('%a')
        if not(d in data_day):
            data_day[d] = 0
        data_day[d] = data_day[d] + newView[i]
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
        dictToFile(best, "data/best")

        categories = toDataCategorie(data_clean)
        dictToFile(categories, "data/category")

        days = toDayView(data_clean)
        dictToFile(days, "data/days")

        views = toTimeView(data_clean)
        dictToFile(views, "data/views")

        NV = toNewView(data_clean)
        dictToFile(NV, "data/newView")

        viewsFM = toViewFluctuationMoyenne(data_clean)
        dictToFile(viewsFM, "data/viewsFM")

        dur = toDataDuration(data_clean)["11-12-2019 09:00:02"] #TODO
        dictToFile(dur, "data/duration")

        tags = toDataTags(data_clean)["11-12-2019 09:00:02"] #TODO
        dictToFile(tags, "data/tags")

        title = toDataTitleWords(data_clean)["11-12-2019 09:00:02"] #TODO
        dictToFile(title, "data/titleWords")

        ntr = nameToRef(data_clean)
        dictToFile(ntr, "data/catAno")

        cq = toDataCategorieCost(data_clean)
        dictToFile(cq, "data/costCat")

    else:

        data_clean = DataClean(data_dict)
        print("DataClean")
        cq = toNewViewCost(data_clean)
        print("DataCost")
        dictToCSV(cq, "data/newView")
        print("File")

        exit()

        fluc = nameToRef(data_clean)
        print(fluc)

        dic = {}

        for d in fluc:
            if not(fluc[d] in dic):
                dic[fluc[d]] = 0
            dic[fluc[d]] = dic[fluc[d]] + 1 

        i = {}

        for d in dic:
            for c in fluc:
                if fluc[c] == d and dic[d] > 1 :
                    if not(d in i):
                        i[d] = []
                    i[d].append(c)
        


        for d in fluc:
            print(d + " : " + str(fluc[d]))

#        for d in fluc:
#            print(d + " : " + str(fluc[d]))