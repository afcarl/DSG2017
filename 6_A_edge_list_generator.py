import pandas as pd
import  csv

test = pd.DataFrame.from_csv("./raw_dataset/test.csv", index_col = None)
test = test[["media_id", "user_id"]]

train = pd.DataFrame.from_csv("./raw_dataset/train.csv", index_col = None)
train = train[["media_id", "user_id"]]

train = pd.concat([train,test])

media_ids = train["media_id"].tolist()
user_ids = train["user_id"].tolist()

ids = [str(media_ids[i]) + "_" + str(user_ids[i]) for i in range(0, len(media_ids))]
ids = list(set(ids))
ids = map(lambda s: [int(s.split("_")[0]),int(s.split("_")[1])] , ids)

with open("./node2vec-master/graph/out.csv","w") as f:
    wr = csv.writer(f,delimiter = ' ')
    wr.writerows(ids)
