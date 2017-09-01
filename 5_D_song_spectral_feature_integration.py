import glob
import pandas as pd

chunks = glob.glob("./mel_feature_parts/*csv")

index = 0
for chunk in chunks:
    print(index)
    if index == 0:
        base_frame = pd.DataFrame.from_csv(chunk, index_col = None)
    else:
        new_frame = pd.DataFrame.from_csv(chunk, index_col = None)
        base_frame = pd.concat([base_frame,new_frame])
    index = index + 1

base_frame.to_csv("./clean_dataset/mel_features.csv", index = None, sep = ",")
