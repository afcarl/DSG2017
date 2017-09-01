import pandas as pd
import numpy as np
import xgboost as xgb

train_base = pd.read_csv("./clean_dataset/train.csv", index_col = None)
print("Dataset I. -- Features are loaded.")
train_aux = pd.read_csv("./clean_dataset/train_aux.csv",index_col = None)
print("Dataset II. -- Features obtained from API are loaded.")

train_latent_space = pd.read_csv("./clean_dataset/train_features.csv",index_col = None)
print("Dataset III. -- Matrix factorization features are loaded.")

train_images = pd.read_csv("./clean_dataset/train_aux_image.csv", index_col = None)
print("Dataset IV. -- Image autoencoded features are loaded.")

train_spectral = pd.read_csv("./clean_dataset/mel_features_train.csv",index_col = None)
print("Dataset V. -- Music spectral features.")

train_graph = pd.read_csv("./clean_dataset/train_graph.csv", index_col = None)
print("Dataset VI. -- Graph features.")



#-------------------------------
# Training dataset is obtained.
#-------------------------------

target = pd.read_csv("./clean_dataset/target.csv",index_col = None)
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

shaping = train.shape[0]

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

#-------------------------------------
#
#
#-------------------------------------

dtest = xgb.DMatrix(test)

del test

dtrain = xgb.DMatrix(train, label = target)

del train

#-------------------------------------
#
#
#-------------------------------------

param = {'eta':0.1,
         'alpha':1,
         'lambda':1,
         'silent':1,
         'subsample':0.5,
         'booster':'gblinear',
         'colsample_bytree':0.5,
         'seed': 2017,
         'eval_metric':'auc',
         'nthread':50,
         'objective':'binary:logistic'}
    
watchlist = [ (dtrain,'train')]
    
model = xgb.train(param,
                  dtrain,
                  1500,
                  watchlist)
    
predictions = model.predict(dtest)
    
id_column = range(0, 19918)
    
output = pd.DataFrame()
    
output["sample_id"] = id_column
    
output["is_listened"] = predictions
    
output.to_csv("./predictions/test/linear.csv",sep = ",", index = None)


predictions = model.predict(dtrain)
    
id_column = range(0, shaping)
    
output = pd.DataFrame()
    
output["sample_id"] = id_column
    
output["is_listened"] = predictions
    
output.to_csv("./predictions/train/linear.csv",sep = ",", index = None)
