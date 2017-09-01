import pandas as pd
import numpy as np
import lightgbm as lgb

train_base = pd.read_csv("./clean_dataset/train.csv", index_col = None)
print("Dataset I. -- Features are loaded.")

train_aux = pd.read_csv("./clean_dataset/train_aux.csv", index_col = None)
print("Dataset II. -- Features obtained from API are loaded.")

train_latent_space = pd.read_csv("./clean_dataset/train_features.csv", index_col = None)
print("Dataset III. -- Matrix factorization features are loaded.")

train_images = pd.read_csv("./clean_dataset/train_aux_image.csv", index_col = None)
print("Dataset IV. -- Image autoencoded features are loaded.")

train_spectral = pd.read_csv("./clean_dataset/mel_features_train.csv", index_col = None)
print("Dataset V. -- Music spectral features.")

train_graph = pd.read_csv("./clean_dataset/train_graph.csv", index_col = None)
print("Dataset VI. -- Graph features.")



#-------------------------------
# Training dataset is obtained.
#-------------------------------

target = pd.read_csv("./clean_dataset/target.csv", index_col = None)
target = np.array(target)


#-------------------------------------
#
#
#-------------------------------------


train = np.concatenate((np.array(train_base), np.array(train_aux), np.array(train_latent_space), np.array(train_images), np.array(train_spectral),np.array(train_graph)), axis = 1)

 
#-------------------------------------
#
#
#-------------------------------------

del train_base, train_aux, train_latent_space, train_images, train_spectral, train_graph

#-------------------------------------
#
#
#-------------------------------------

test_base = pd.read_csv("./clean_dataset/test.csv", index_col = None)
test_aux = pd.read_csv("./clean_dataset/test_aux.csv", index_col = None)
test_latent_space = pd.read_csv("./clean_dataset/test_features.csv", index_col = None)
test_images = pd.read_csv("./clean_dataset/test_aux_image.csv", index_col = None)
test_spectral = pd.read_csv("./clean_dataset/mel_features_test.csv", index_col = None)
test_graph = pd.read_csv("./clean_dataset/test_graph.csv", index_col = None)


#-------------------------------------
#
#
#-------------------------------------


test = np.concatenate((np.array(test_base), np.array(test_aux), np.array(test_latent_space), np.array(test_images), np.array(test_spectral), np.array(test_graph)), axis = 1)

#-------------------------------------
#
#
#-------------------------------------


del test_base, test_aux, test_latent_space, test_images, test_spectral, test_graph

train_to_predict = train
train = lgb.Dataset(train, label = map(lambda x: round(x[0]),target.tolist()))

#-------------------------------------
#
#
#-------------------------------------

for i in range(0,30):
    print(i)
    param = {'num_leaves':511,
             'objective':'binary',
             'feature_fraction_seed':i,
             'feature_fraction':0.5,
             'max_depth':9,
             'bagging_seed':i,
             'verbose': 1,
             'num_threads':40,
             'data_random_seed':i}


    param['metric'] = 'auc'
    bst = lgb.train(param, train, 1500)
    predictions = bst.predict(test)
    id_column = range(0, 19918)
    output = pd.DataFrame()
    output["sample_id"] = id_column
    output["is_listened_"+str(i)] = predictions
    output.to_csv("./predictions/test/light_gbm_" + str(i) + ".csv", sep = ",", index = None)
    predictions = bst.predict(train_to_predict)

    id_column = range(0, train_to_predict.shape[0])
    output = pd.DataFrame()
    output["sample_id"] = id_column
    output["is_listened_"+str(i)] = predictions
    output.to_csv("./predictions/train/light_gbm_" + str(i) + ".csv", sep = ",", index = None)

