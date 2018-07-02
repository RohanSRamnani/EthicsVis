import json
import datetime
from collections import defaultdict
def JsonFilter():
    with open("Location History.json") as f:
        history = json.load(f)
        d = dict()
        for i in history["locations"]:
            a = int(i["timestampMs"])
            b = a + 1
            if "activity" in i.keys():
                b = int(i["activity"][0]["timestampMs"])
            while(a <= b):
                l = datetime.datetime.fromtimestamp(a/1000.0)
                if l.year not in d.keys():
                    d[l.year] = dict()
                if l.month not in d[l.year].keys():
                    d[l.year][l.month] = dict()
                if l.day not in d[l.year][l.month].keys():
                    d[l.year][l.month][l.day] = dict()
                if l.hour not in d[l.year][l.month][l.day].keys():
                    d[l.year][l.month][l.day][l.hour] = dict()
                d[l.year][l.month][l.day][l.hour][l.minute] = [i["latitudeE7"],i["longitudeE7"]]
                a += 60000
        f.close()
    with open("FilteredLocation.json", 'w') as outfile:
        json.dump(d, outfile)
JsonFilter()
