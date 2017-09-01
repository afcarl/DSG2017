import glob
import pandas as pd
from time import time
import numpy
from gensim.models import Word2Vec
from gensim.models.word2vec import logger, FAST_VERSION
import logging
import os

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
import numpy.distutils.system_info as sysinfo
sysinfo.get_info('atlas')
import scipy; scipy.show_config()
print FAST_VERSION

files = glob.glob("./node2vec-master/src/partial_results/*.csv")

print(files)

index = 0

for file in files:
    index = index + 1
    print("Walk file nr.:")
    print(index)
    if index == 1:
        tab_1 = pd.read_csv(file, index_col = None)
    else:
        tab_2 = pd.read_csv(file, index_col = None)
        tab_1 = pd.concat([tab_1, tab_2])


print("Integration finished")
tab_1 = tab_1.values.tolist()
print("Mapping started.")
tab_1 = [map(str, row) for row in tab_1]
print("Model setup and train.")
model = Word2Vec(tab_1, size = 64, window = 8, min_count = 0, sg = 1, workers = 54, iter = 10)
print("Dumping started.")
model.wv.save_word2vec_format("./node2vec-master/emb/dsg.emb")
