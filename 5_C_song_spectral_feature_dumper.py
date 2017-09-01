import json
import pandas as pd
import glob
import numpy as np

def json_readup(path):
    with open(path) as data_file:    
        data = json.load(data_file)
    return data

images = glob.glob("./mel_feature_json_dumps/*json")
index = 0
names = ["media_id"] + map(lambda s: "mel_feature_" + str(s), range(1,769))

table = []
print(len(images))

for image in images:
    try:
        row = json_readup(image)["feature"]
        row[0] = int(row[0])
        row[1:len(row)] = map(lambda s: round(s,5), row[1:len(row)])
        index = index + 1
        table = table + [row]
        if index % 20000 == 0:
            print(index)
            table = pd.DataFrame(table, columns = names, index = None)
            table.to_csv("./mel_feature_parts/mel_features" + str(index) + ".csv", index = None, sep = ",")
            table = []
    except:
        pass

table = pd.DataFrame(table, columns = names, index = None)
table.to_csv("./mel_feature_parts/mel_features" + str(index) + ".csv", index = None, sep = ",")
