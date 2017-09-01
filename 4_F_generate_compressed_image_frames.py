import numpy as np
import pandas as pd
import json
import sys
import glob

'''
We need to compress further the image features with the autoencoder.
Moreover, we have to save the values from the middle layer.
'''

sys.path.append('/usr/local/lib/python2.7/site-packages')

from keras.models import Model
from keras.models import load_model

def image_list_gen(input_dir):
    
    '''
    input_dir: Path to the images that are scored.
    '''
    
    images = glob.glob(input_dir + "*json")
    return images

def model_read_up(input_line, layer_name):
    
    '''
    input_line: Path to the model file.
    layer_name: Name of the middle layer.
    '''
    
    model = load_model(input_line)
    model.summary()
    model = Model(input = model.input, output = model.get_layer(layer_name).output)
    return model

def readup_image_jsons(input_path):
    
    '''
    input_path: Path to the json files containing values from the middle convolutional layer.
    '''
    
    with open(input_path) as data_file:    
        data = json.load(data_file)
    data_file.close()
    return data
    

def generate_dataframes(name, layer_name):
    
    '''
    name: Name of the autoencoder h5 file.
    layer_name: Name of the middle layer.
    '''
    
    model = model_read_up("./models/" + name + "_compressor.h5", layer_name)    
    images = image_list_gen("./intermediate_jsons/" + name + "/")

    frame = []
    index = 0
    
    for image in images:
        index = index + 1
        features = readup_image_jsons(image)["features"]
        features = np.array(features).reshape(1, 1600)
        ID =  image.split("/")[-1].replace(".json", "")
        y = model.predict(features).tolist()[0]
        y = map(lambda s: round(s, 5), y)
        out = [ID] + y 
        frame = frame + [out]

    frame = pd.DataFrame(frame, index = None)
    frame.columns = [name + "_id"] + map(lambda s: name + "_image_" + str(s), range(0, 30)) 
    frame.to_csv("./raw_dataset/" + name + "_images.csv", sep = ",", index = None)

'''
Generating the frames with the compressed image features.
'''

generate_dataframes("album", "dense_25")    
generate_dataframes("artist", "dense_5")
generate_dataframes("user", "dense_15")
