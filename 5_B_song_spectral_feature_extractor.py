import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')

import librosa
import json
import glob
import numpy as np
import scipy
from joblib import Parallel, delayed
import multiprocessing

def feature_extractor(current_features, dataset):
    
    '''
    current_features:
    dataset:
    '''
    
    current_features = current_features + np.mean(dataset, axis = 1).tolist()
    current_features = current_features + np.max(dataset, axis = 1).tolist()
    current_features = current_features + np.std(dataset, axis = 1).tolist()
    current_features = current_features + np.median(dataset, axis = 1).tolist()
    current_features = current_features + scipy.stats.skew(dataset, axis = 1).tolist()
    current_features = current_features + scipy.stats.kurtosis(dataset, axis = 1).tolist()
    current_features = map(lambda x: round(x, 5), current_features)
    return current_features        
    
def data_extractor(song):
    
    '''
    song: Path to the mp3 file to be used.
    '''
    
    print(song)
    
    try:
        name = int(song.split("/")[-1].replace(".mp3",""))
        current_features = [name]
        data = librosa.load(song)
    
        dataset = data[0]
        frequency = data[1]
    
        extracted_features = librosa.feature.melspectrogram(y = dataset, sr = frequency)
        extracted_features = librosa.power_to_db(extracted_features,ref=np.max)
        current_features = feature_extractor(current_features, extracted_features)
        current_features[0] = current_features[0]
        data = {}
        data["feature"] =  current_features
        
        with open("./mel_feature_json_dumps/" + str(name) +".json", 'w') as fp:
            json.dump(data, fp)
        with open("./mel_feature_json_dumps/" + str(name) +".json", 'w') as fp:
            json.dump(data, fp)
    except:
        pass
    
files_to_transform = glob.glob("./music/*mp3")
files_that_we_have = glob.glob("./mel_feature_json_dumps/*json")

files_to_transform = set(map(lambda s: s.split("/")[-1].replace(".mp3",""), files_to_transform))
files_that_we_have = set(map(lambda s: s.split("/")[-1].replace(".json",""), files_that_we_have))

files = list(files_to_transform.difference(files_that_we_have))
files = map(lambda s: "./music/" + s + ".mp3", files)

number_of_cores = multiprocessing.cpu_count()

results = Parallel(n_jobs = number_of_cores)(delayed(data_extractor)(song) for song in files)
