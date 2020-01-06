import json

with open("data.json", "r") as f:
    data = json.load(f)



for x in data:
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
