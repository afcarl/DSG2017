import pandas as pd

with open("./node2vec-master/emb/dsg.emb") as f:
    content = f.readlines()

content = [x.strip().split() for x in content]



dataset = [map(lambda x: float(x), con[0:len(con)])  for con in content[0:len(content)]]

dataset = pd.DataFrame(dataset, index = None)
dataset.columns = ["id"] + map(lambda x: "embed_" + str(x),range(0, len(dataset.columns)-1))
dataset.to_csv("./raw_dataset/node_2_vec.csv", index = None)
