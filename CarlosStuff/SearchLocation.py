import json
def mergeJ():
    l = open("FilteredLocation.json")
    loc = json.load(l)
    s = open("SearchList2.json")
    search = json.load(s)
    r = dict()
    for year in search:
        if year in loc.keys():
            for month in search[year]:
                for day in search[year][month]:
                    for hour in search[year][month][day]:
                        for minute in search[year][month][day][hour]:
                            for w in search[year][month][day][hour][minute]:
                                let = check(loc, year, month, day, hour, minute, 1)
                                if not(let==[]):
                                    r = create(r, year, month, day, hour, minute, w)
                                    r[year][month][day][hour][minute][w] = let
    with open("SearchLocations.json", 'w') as outfile:
        json.dump(r, outfile)
                                

def check(location, year, month, day, hour, minute, num):
    if num >= 120:
        return []
    see = num%2
    temp = (num - (see))/2
    if (see):
        t = str(int(int(minute)-temp))
    else:
        t = str(int(int(minute)+temp))
    try:
        ret = location[year][month][day][hour][t]
        return ret
    except:
        return check(location, year, month, day, hour, minute, num+1)

def create(r, year, month, day, hour, minute, word):
    if year not in r:
        r[year] = dict()
    if month not in r[year]:
        r[year][month] = dict()
    if day not in r[year][month]:
        r[year][month][day] = dict()
    if hour not in r[year][month][day]:
        r[year][month][day][hour]=dict()
    if minute not in r[year][month][day][hour]:
        r[year][month][day][hour][minute] = dict()
    return r
mergeJ()
