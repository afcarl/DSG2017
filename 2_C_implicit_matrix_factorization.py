import numpy as np
import pandas as pd
import time

from functools import reduce
from implicit.als import AlternatingLeastSquares
from implicit.nearest_neighbours import bm25_weight
from matplotlib import pyplot as plt
from operator import mul
from scipy.sparse import coo_matrix
from sklearn.model_selection import StratifiedKFold

#---------------------------------
#
#---------------------------------

filename = './raw_dataset/train_deduplicated.csv'
train = pd.read_csv(filename)

#---------------------------------
#
#---------------------------------

filename = './raw_dataset/test.csv'
test = pd.read_csv(filename)

#---------------------------------
#
#---------------------------------

whole = pd.concat((train.drop('is_listened', axis = 1), test.drop('sample_id', axis = 1)))

#---------------------------------
#
#---------------------------------

triplets = whole.groupby(['user_id', 'media_id']).size().reset_index()
triplets.columns = ['user', 'track', 'count']

triplets['user'] = triplets['user'].astype('category')
triplets['track'] = triplets['track'].astype('category')

#---------------------------------
#
#---------------------------------

train_triplets = train.groupby(['user_id', 'media_id']).size().reset_index()
train_triplets.columns = ['user', 'track', 'count']

train_triplets['user'] = train_triplets['user'].astype('category')
train_triplets['track'] = train_triplets['track'].astype('category')

#---------------------------------
#
#---------------------------------

test_triplets = test.groupby(['user_id', 'media_id']).size().reset_index()
test_triplets.columns = ['user', 'track', 'count']

test_triplets['user'] = test_triplets['user'].astype('category')
test_triplets['track'] = test_triplets['track'].astype('category')

#---------------------------------
#
#---------------------------------

triplets.head()

plays = coo_matrix((triplets['count'].astype(float),
                   (triplets['track'].cat.codes.copy(),
                    triplets['user'].cat.codes.copy())))
#---------------------------------
#
#---------------------------------

nplays = bm25_weight(plays, K1=100, B=0.5)

#---------------------------------
#
#---------------------------------

nz = (plays.nnz / reduce(mul, plays.shape)) * 100
print("{:.4f}% non-zero entries".format(nz))

#---------------------------------
#
#---------------------------------

als = AlternatingLeastSquares(factors=50)
als.fit(plays)


als.item_factors.shape

als.user_factors.shape

#---------------------------------
#
#---------------------------------

ix = train.user_id.values

train_user_factors = als.user_factors[ix]
train_user_factors.shape

#---------------------------------
#
#---------------------------------

ix = test.user_id.values

test_user_factors = als.user_factors[ix]
test_user_factors.shape

#---------------------------------
#
#---------------------------------

repeats = train_triplets['count'].values
ix = np.repeat(train_triplets.track.cat.codes.values, repeats)

train_media_factors = als.item_factors[ix]
train_media_factors.shape

#---------------------------------
#
#---------------------------------

repeats = test_triplets['count'].values
ix = np.repeat(test_triplets.track.cat.codes.values, repeats)

test_media_factors = als.item_factors[ix]
test_media_factors.shape

#---------------------------------
#
#---------------------------------

train_features = np.hstack((train_user_factors, train_media_factors))
test_features = np.hstack((test_user_factors, test_media_factors))

#---------------------------------
#
#---------------------------------

train_features = pd.DataFrame(train_features, index = None)
test_features = pd.DataFrame(test_features, index = None)

#---------------------------------
#
#---------------------------------

test_features.to_csv('./clean_dataset/test_features.csv', float_format='%.4f', index = None)
train_features.to_csv('./clean_dataset/train_features.csv', float_format='%.4f', index = None)
