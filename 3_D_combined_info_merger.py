import pandas as pd

'''
We need to integrate the language related chunks.
These only contain data about 20 thousand rows.
The integrated chunks for the training set are saved as "language_train.csv"
'''

pieces = map(lambda s: "./raw_dataset/combined_chunks/train/part" + str(s) +".csv", range(0,199))
index = 0

for piece in pieces:
    
    if index == 0:
        dataset = pd.DataFrame.from_csv(piece, index_col = None)
        index = index + 1
    else:
        new_dataset = pd.DataFrame.from_csv(piece, index_col = None)
        dataset = pd.concat([dataset, new_dataset])
        
dataset.to_csv("./raw_dataset/language_train.csv", index = None, sep = ",")
