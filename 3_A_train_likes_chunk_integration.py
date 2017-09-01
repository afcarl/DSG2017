import glob
import pandas as pd


tablets = glob.glob("./raw_dataset/train_pieces/*.csv")
tablets = map(lambda s: int(s.split("_")[3].replace(".csv", "")), tablets)
tablets = sorted(tablets)

index = 0
for tab in tablets:
    index = index + 1
    path = './raw_dataset/train_pieces/train_' + str(tab) + '.csv'
    if index == 1:
        input_tab = pd.DataFrame.from_csv(path, index_col = None)
    else:
        input_tab_aux = pd.DataFrame.from_csv(path, index_col = None)
        input_tab = pd.concat([input_tab, input_tab_aux])
        
input_tab.to_csv('./raw_dataset/train_likes.csv',sep = ",", index = None)
