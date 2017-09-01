import numpy as np
import json
import sys
import glob

sys.path.append('/usr/local/lib/python2.7/site-packages')

import cv2

from sklearn.cross_validation import train_test_split

from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.models import Sequential

'''
We need to fit an autoencoder to the values from the convolution autoencoder to achieve further compression.
We do this here.
'''


def image_list_gen(input_dir):
    
    '''
    '''    
    
    images = glob.glob(input_dir + "*json")
    return images

def create_model(column_number):
    
    '''
    '''

    model = Sequential()
    
    model.add(Dense(180, activation = 'relu',input_shape = (column_number,)))
    model.add(Dense(120, activation = 'relu' ))     
    model.add(Dense(90, activation = 'relu' ))   
    model.add(Dense(60, activation = 'relu' ))   
    
    model.add(Dense(30, activation = 'relu' ))  
    
    model.add(Dense(60, activation = 'relu' ))   
    model.add(Dense(90, activation = 'relu'))
    model.add(Dense(120, activation = 'relu' ))
    model.add(Dense(180, activation = 'relu' ))

    model.add(Dense(1600, activation = 'relu' ))    
    
    model.compile(loss = 'mse', optimizer = Adam())
    
    return model

def readup_image_jsons(input_path):
    
    '''
    '''
    
    with open(input_path) as data_file:    
        data = json.load(data_file)
    data_file.close()
    
    return data
    
def generate_arrays_for_train(input_paths, batch_size, seeding):
    
    '''
    '''
    
    index = 0

    while True:
        
        np.random.shuffle(input_paths)
        
        images = []
        y = []
        for i in range(0, len(input_paths) -(len(input_paths) % batch_size)):
            try:
                img = readup_image_jsons(input_paths[i])["features"]

                images.append(img)
                y.append(img)
                index = index + 1
                
                if index % batch_size == 0:
            	    images = np.array(images, dtype=np.float32)
            	    images = images.reshape(batch_size, 1600)
            	    y = np.array(y, dtype = np.float32)
            	    y = y.reshape(batch_size, 1600)
                    yield(images, y)
                    y = []
                    images = []

            except:
                pass    
    
 
def generate_arrays_for_validation(input_paths):
    
    '''
    '''

    while True:
        for i in range(0, len(input_paths)):
            try:
                img = readup_image_jsons(input_paths[i])["features"]
                img = img.reshape(1, 1600)
                y = img
                yield(img, y)
            except:
                pass
            
def model_train(cv_size, batch_size, epochs, validate, input_pathing):
    
    '''
    '''
    
    if validate:
        
        model = create_model(1600)
        
        train = image_list_gen(".intermediate_jsons/" + input_pathing + "/")
        
        train, test = train_test_split(train, test_size = cv_size, random_state = 56741)
        
        train_sample_size = len(train) - (len(train) % batch_size)
        
        
        model.fit_generator(generate_arrays_for_train(train, batch_size, 2017),
                            samples_per_epoch = train_sample_size,
                            nb_epoch = epochs,
                            validation_data = generate_arrays_for_validation(test),
                            nb_val_samples = cv_size)
        
    else:
        
        model = create_model(1600)
        
        train = image_list_gen("/./intermediate_jsons/" +input_pathing + "/")
        
        train_sample_size = len(train) - (len(train) % batch_size)
        
        model.fit_generator(generate_arrays_for_train(train, batch_size, 2017),
                            samples_per_epoch = train_sample_size,
                            nb_epoch = epochs)
        
        model.save("./models/" + input_pathing +"_compressor.h5")
      
model_train(200, 32, 20, False, "album")
model_train(200, 32, 12, False, "user")
model_train(200, 32, 20, False, "artist")
