import json
import csv
def add_pos():
    f = open('data/pos_out.json')
    data = json.load(f)
    ordi = open('data/maskdata.csv','r',newline='')
    datas = csv.reader(ordi)
    out = open('data/maskdata_pos.csv','w',newline='')
    writer = csv.writer(out)
    for i in datas:
        try:
            nxt = data[i[0]]
            arr = i
            arr.append(data[i[0]]['lng'])
            arr.append(data[i[0]]['lat'])
            writer.writerow(arr)
        except:
            pass