import pandas as pd
import json

'''
We need the training and test sets.
'''

test = pd.DataFrame.from_csv("./raw_dataset/test.csv", index_col = None)
train = pd.DataFrame.from_csv("./raw_dataset/train.csv", index_col = None)

dummies = {}

'''
We also need columns with the ID variables.
'''

columns = ["user_id", "album_id", "media_id", "genre_id", "artist_id"]

'''
A dictionary is built up and dumped to disk.
'''

for col in columns:
    dummy = list(set(test[col].tolist()).union(set(train[col].tolist())))
    dummies[col] = map(lambda s: int(s), dummy)

with open('keys.json', 'w') as fp:
    json.dump(dummies, fp)
