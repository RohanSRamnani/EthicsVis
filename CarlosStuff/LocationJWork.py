import json
from collections import defaultdict
def MonthSwitch(s: str)->int:
    if s[0] == "J":
        return 1
    if s[0] == "F":
        return 2
    if s == "Mar":
        return 3
    if s == "Apr":
        return 4
    if s == "May":
        return 5
    if s == "Jun":
        return 6
    if s == "Jul":
        return 7
    if s == "Aug":
        return 8
    if s == "Sep":
        return 9
    if s == "Oct":
        return 10
    if s == "Nov":
        return 11
    if s == "Dec":
        return 12
def FileToJSON()->list:
    file = open('stop_words.txt', 'r')
    stop_words = file.read().split("\n")
    file.close()
    stop_words.append("->")
    file2 = open("Takeout//My Activity//Search//MyActivity.html", encoding="utf8")
    x = file2.read()
    file2.close()
    length = len(x)
    where = 0
    search = ""
    date = ""
    #7
    JSON = []
    while(where + 32 < length):
        if (x[where:where+32] == "https://www.google.com/search?q="):
            where = where + 32
            while(x[where-1] != ">"):
                where = where + 1
            while(x[where:where+8] != "</a><br>"):
                search = search + x[where]
                where = where + 1
            where = where + 8
            date = x[where]
            where = where +1
            while(x[where] != "M"):
                date = date + x[where]
                where = where + 1
            date = date + x[where]
            d2 = []
            for temp in date.split(" "):
                for t2 in temp.split(":"):
                    d2.append(t2.replace(",",""))
            if d2[3] == "12":
                d2[3] = "0"
            if d2[6] == "PM":
                if d2[3] == "0":
                    d2[3] = "12"
                else:
                    d2[3] = str(int(d2[3]) + 12)
            for temp in search.split(" "):
                temp = temp.replace(",","")
                if temp not in stop_words:
                    t = dict()
                    t["word"] = temp
                    t["Month"] = MonthSwitch(d2[0])
                    t["Day"] = d2[1]
                    t["Year"] = d2[2]
                    t["Hour"] = d2[3]
                    t["Min"] = d2[4]
                    JSON.append(t)
            search = ""
            date = ""

        where = where + 1
    return JSON
def refineJSON(d):
    r= dict()
    for t in d:
        if (all(ord(char) < 128 for char in t["word"])):
            if t["Year"] not in r:
                r[t["Year"]]=dict()
            if t["Month"] not in r[t["Year"]]:
                r[t["Year"]][t["Month"]]=dict()
            if t["Day"] not in r[t["Year"]][t["Month"]]:
                r[t["Year"]][t["Month"]][t["Day"]]=dict()
            if t["Hour"] not in r[t["Year"]][t["Month"]][t["Day"]]:
                r[t["Year"]][t["Month"]][t["Day"]][t["Hour"]] = dict()
            if t["Min"] not in r[t["Year"]][t["Month"]][t["Day"]][t["Hour"]]:
                r[t["Year"]][t["Month"]][t["Day"]][t["Hour"]][t["Min"]] = defaultdict(list)
            if t["word"] not in r[t["Year"]][t["Month"]][t["Day"]][t["Hour"]][t["Min"]]:
                r[t["Year"]][t["Month"]][t["Day"]][t["Hour"]][t["Min"]][t["word"]] = 1
    return r
'''and (t["Month"] in loc[t["Year"]].keys()) and (t["Day"] in loc[t["Year"]][t["Month"]].keys()) and (t["Hour"] in loc[t["Year"]][t["Month"]][t["Day"]].keys())'''
def MakeJSON():
    word_dict = FileToJSON()
    word_dict = refineJSON(word_dict)
        
    print("DONE!!!!!!")
    with open("SearchList2.json", 'w') as outfile:
        json.dump(word_dict, outfile)
MakeJSON()
    
