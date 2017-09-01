import numpy as np
import json
import sys
import glob

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2

from sklearn.cross_validation import train_test_split
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution2D, UpSampling2D
from keras.optimizers import Adam
from keras.layers import MaxPooling2D
from keras.layers.normalization import BatchNormalization
from keras.layers import Input, Dense
from keras.models import Model
from keras.models import Sequential
from keras.models import load_model


def image_list_gen(input_dir):
    images = glob.glob(input_dir + "*jpg")
    return images

def model_read_up(input_line):
    model = load_model(input_line)
    model.summary()
    intermediate_layer_model = Model(input = model.input,
                                     output = model.get_layer("convolution2d_16").output)
    return intermediate_layer_model

    
def dump_json(file_name, data):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)

def create_predictions(source_of_files, model):
    
    images = image_list_gen(source_of_files)

    index = 0
    for image in images:
        out_dict = {}
        index = index + 1
        print(index)
        try:
            img = cv2.imread(image).astype(np.float32)
            img = img.transpose((2, 0, 1))
            img = img.reshape(1, 120, 120, 3)
            img = np.array(img, dtype=np.float32)
            y = model.predict(img, verbose = 0)[0]
            y = y.reshape(1, y.shape[0]*y.shape[1]*y.shape[2])
            name = image.split("/")[-1].replace(".jpg","")
            folder = image.split("/")[-2]
            out_dict["features"] = y.tolist()[0]
            file_name  = "./" + "intermediate_jsons/" + folder +"/" + name + ".json"

            dump_json(file_name,out_dict)
        except:
            print(index)
            print("Problem")
            pass
    
    
user_model = model_read_up("./models/user_model.h5")
create_predictions("./image/user/",user_model)

album_model = model_read_up("./models/album_model.h5")
create_predictions("./image/album/",album_model)

artist_model = model_read_up("./models/artist_model.h5")
create_predictions("./image/artist/",artist_model)
