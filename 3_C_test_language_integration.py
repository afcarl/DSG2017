import pandas as pd
import json
import numpy as np

def json_readup(path):
    '''
    '''
    with open(path) as data_file:    
        data = json.load(data_file)
    return data
    
train = pd.DataFrame.from_csv("./raw_dataset/test.csv", sep = ",")


user_ids = train["user_id"].tolist()
media_ids = train["media_id"].tolist()

interest , dataset = [], []

for i in range(0, len(user_ids)):
    print(i)
    try:
        media = json_readup("./dumps/media/" + str(media_ids[i]) + ".json")
        user = json_readup("./user/" + str(user_ids[i]) + ".json")
        isrc = media["isrc"]
        song_country = "".join(list(isrc)[0:2])
        song_registrant = "".join(list(isrc)[2:5])
        song_registry_year = "".join(list(isrc)[5:7])
        id_number = "".join(list(isrc)[7:])
        values = [song_country, song_registrant, int(song_registry_year), int(id_number), media["readable"]]
        
        if song_country == user["country"]:
            values = values + [1]
        else:
            values = values + [0]

        if user["country"] in set(media["available_countries"]):
            values = values + [1]
        else:
            values = values + [0]            
            
    except:
        values = [0, 0, 0, 0, 0, 0, 0]
        pass
    
    dataset = dataset + [values]

dataset = pd.DataFrame(dataset, index = None)

dataset.columns = ["song_country",
                   "song_registrant",
                   "registry_year",
                   "id_number",
                   "media_readable",
                   "same_country_reg",
                   "song_not_allowed"]

dataset.to_csv("./raw_dataset/language_test.csv", index = None)
