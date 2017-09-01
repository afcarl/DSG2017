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

def generate_arrays_for_train(input_paths, batch_size, seeding):
    
    #-------------------
    # This is ugly
    #-------------------

    index = 0

    while True:
        
        np.random.shuffle(input_paths)
        
        images = []
        y = []
        for i in range(0, len(input_paths) -(len(input_paths) % batch_size)):
            try:
                img = cv2.imread(input_paths[i]).astype(np.float32)
                img = cv2.resize(img, (120, 120))
                img = img.transpose((2, 0, 1))
                images.append(img)
                other  = img.reshape(120,120, 3)
                y.append(np.dot(other[...,:3], [0.299, 0.587, 0.114]))
                index = index + 1
                if index % batch_size == 0:
            	    images = np.array(images, dtype=np.float32)
            	    images = images.reshape(batch_size, 120, 120, 3)
            	    y = np.array(y, dtype = np.float32)

            	    y = y.reshape(batch_size, 120, 120, 1)
                    yield(images, y)
                    y = []
                    images = []

            except:
                pass
            
def generate_arrays_for_validation(input_paths):
    
    #-------------------
    # This is ugly
    #-------------------

    while True:
        for i in range(0, len(input_paths)):
            try:
                img = cv2.imread(input_paths[i]).astype(np.float32)
                img = img.transpose((2, 0, 1))
                img = np.array(img, dtype=np.float32)
                img = img.reshape(1, 120, 120, 3)
                y = img.reshape(120, 120, 3)
                y = np.dot(y[...,:3], [0.299, 0.587, 0.114])
                y = y.reshape(1,120,120, 1)
                yield(img, y)
            except:
                pass


            
def generate_model():
    
    
    nb_filters = 8
    size_conv = 2
    
    model = Sequential()
    
    model.add(Convolution2D(nb_filters, size_conv, size_conv, border_mode = 'valid', input_shape = (120, 120, 3), activation = 'relu'))
    model.add(BatchNormalization())

    model.add(Convolution2D(nb_filters, size_conv, size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.5))


    model.add(Convolution2D(nb_filters*2, size_conv, size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.5))


    model.add(Convolution2D(nb_filters*4, size_conv, size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.5))

    model.add(Convolution2D(nb_filters*8, size_conv, size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(pool_size = (2, 2)))
    model.add(Dropout(0.5))
    
    model.add(Convolution2D(nb_filters*8, size_conv, size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(UpSampling2D((2, 2)))
    model.add(Dropout(0.5))    

    model.add(Convolution2D(nb_filters*4, size_conv, size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(UpSampling2D((2, 2)))
    model.add(Dropout(0.5))    

    model.add(Convolution2D(nb_filters*2, size_conv, size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(UpSampling2D((2, 2)))
    model.add(Dropout(0.5))    

    model.add(Convolution2D(nb_filters, 2*size_conv, 2*size_conv, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(UpSampling2D((2, 2)))    

    model.add(Convolution2D(1, 3, 3, activation = 'relu' ))
    model.add(BatchNormalization())
    model.add(UpSampling2D((2, 2)))
    model.summary()
    return model

def start_training(path, validate, cv_size, batch_size, seeding, naming, epochs):
    
    train = image_list_gen(path)
    
    if validate:
        
        train, test = train_test_split(train, test_size = cv_size, random_state = 56741)
        
        train_sample_size = len(train) - (len(train) % batch_size)
        
        model = generate_model()
        
        model.compile(loss = 'mse', optimizer = Adam(), metrics = ['mse','mae'])
        
        
        model.fit_generator(generate_arrays_for_train(train, batch_size, seeding),
                            samples_per_epoch = train_sample_size,
                            nb_epoch = epochs, 
                            validation_data = generate_arrays_for_validation(test),
                            nb_val_samples = cv_size)

    else:
        
        model = generate_model()
        
        train = image_list_gen(path)   
        
        model = generate_model()
        
        model.compile(loss = 'mse', optimizer = Adam(), metrics = ['mse','mae'])
        
        train_sample_size = len(train) - (len(train) % batch_size)
        
        model.fit_generator(generate_arrays_for_train(train, batch_size, seeding),
                            samples_per_epoch = train_sample_size,
                            nb_epoch = epochs)
        
        model.save("./models/" + naming)

start_training("./image/album/", False, 10000, 32, 2017, "album_model.h5", 40)
start_training("./image/artist/", False, 10000, 32, 2017, "artist_model.h5", 140)        
start_training("./image/user/", False, 2000, 32, 2017, "user_model.h5", 500)
