import pandas as pd
import json
import numpy as np

def json_readup(path):
    with open(path) as data_file:    
        data = json.load(data_file)
    return data

def dataset_dumper(dataset, i):
    dataset = pd.DataFrame(dataset, index = None)
    
    dataset.columns = ["song_country",
                       "song_registrant",
                       "registry_year",
                       "id_number",
                       "media_readable",
                       "same_country_reg",
                       "song_not_allowed"]
    
    fun_index = i / 20000

    dataset.to_csv("./raw_dataset/combined_chunks/train/part" + str(fun_index) + ".csv", index = None)    

    
train = pd.DataFrame.from_csv("./raw_dataset/train_deduplicated.csv", sep = ",")
target = pd.DataFrame.from_csv("./clean_dataset/target.csv", sep = ",", index_col = None)


user_ids = train["user_id"].tolist()
media_ids = train["media_id"].tolist()

targets = target["train.is_listened"].tolist()
interest, dataset = [], []

for i in range(0, len(user_ids)):
    print(i)
    try:
        media = json_readup("./dumps/media/" + str(media_ids[i]) + ".json")
        user = json_readup("./dumps/user/" + str(user_ids[i]) + ".json")
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
        values = [0]*7
        pass
    dataset = dataset + [values]
    if (i + 1) % 20000 == 0:
        dataset_dumper(dataset, i)
        dataset = []

dataset_dumper(dataset, i)
