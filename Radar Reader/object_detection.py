
import json
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers,Sequential,models
import os.path
from radar_configuration import Radar
import ctypes
from threading import Timer
class Object_detection():
    my_model = None
    @staticmethod
    def import_data(file_name):
        all_frames=[]
        with open(file_name, 'r') as f:
            allframes=f.readlines()
            count =0
            for line in allframes:
                count +=1
                splittedLine = line.split("\t")
                if(splittedLine[0] == '\n'):
                    continue
                index = -1
                try:
                    index = splittedLine.index('\n')  # seach for the end frame
                except ValueError as e:
                    print(e)
                if (index == -1):
                    continue
                else:
                    try:
                        frame = [int(i) for i in splittedLine[4:index]]
                        print(len(frame))
                        all_frames.append(frame)
                    except:
                        continue
                    else:
                        continue

        return all_frames



    @staticmethod
    def preprocesseing(data):
        return data
    @staticmethod
    def format_data(positives,negatives,split_per):
        '''
        :param positives: posivies class data
        :param negatives:  negative class data
        :return: X as training data and Y as labels

        takes the positives
        takes the negatives
        add last value as 1 (true) or 0 (false)
        convert them to a numpy arrays
        shuffle them togather
        return X as data[0:-1] and Y as data[-1]
        '''
        for i in range(len(positives)):
            positives[i].append(1)

        for i in range(len(negatives)):
            negatives[i].append(0)

        data_positives = np.array(positives)
        data_negatives = np.array(negatives)

        data = np.concatenate((data_positives,data_negatives),axis=0)

        np.random.shuffle(data)
        train_len=int(data.shape[0]*split_per)
        return data[0:train_len,0:-1],data[0:train_len,-1],data[train_len:,0:-1],data[train_len:,-1]

    @staticmethod
    def modele_naive(X_data_train,Y_data_train,X_data_val,Y_data__val):
        '''
        :param X_data_train:
        :param Y_data_train:
        :param X_data_val:
        :param Y_data__val:
        :return: the trained model
        '''
        if os.path.isfile('model_naive.h5'):
            model = models.load_model('model_naive.h5')
            Object_detection.my_model = model
            return
        shape_input=X_data_train.shape[1]
        model = keras.Sequential()
        model.add(layers.Dense(32,input_dim=shape_input,activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X_data_train, Y_data_train, epochs=100, batch_size=10, validation_data=(X_data_val, Y_data__val))
        model.save('model_naive.h5')
        Object_detection.my_model = model
        return



    @staticmethod
    def make_prediction(model,reading):
        result = model.predict(reading) > .8
        if result[0][0] is False:
            Object_detection.newTimer()


    @staticmethod
    def test_live():
        '''
        this function read a reading from the sensor and make a prediction

        :return: a predicition of true as there is an object or false if there is no object
        '''
        radar = Radar(port='com5')
        if (radar.is_open()):
            radar.close()
        radar.start()
        radar.clear_buffer()
        reading = radar.read_magnitude()
        if reading is not None:
            if len(reading) != 255:
                return None
            y=Object_detection.my_model.predict(np.reshape(reading,(1,len(reading))))>.8
            return y[0][0]

def lock_computer():
    ctypes.windll.user32.LockWorkStation()

last_reading = True
t=Timer(10.0,lock_computer)
if __name__=='__main__':
    positives = Object_detection.import_data(file_name='positives.txt') #read the object on readings
    negatives = Object_detection.import_data(file_name='negatives.txt') #read the object off redings
    X_data_train,Y_data_train,X_data_val,Y_data__val = Object_detection.format_data(positives,negatives,.7) #preprocessing on data
    Object_detection.modele_naive(X_data_train,Y_data_train,X_data_val,Y_data__val) # build and train the model or just return it if already trained
    print(Object_detection.my_model.summary()) #print the summary of the model
    while 1:
        prediction = Object_detection.test_live()
        if prediction is None:
            continue
        elif (prediction == False) and (last_reading == True):
            print('start timer')
            if not t.is_alive():
                t = Timer(10.0, lock_computer)
                t.start()
        elif prediction == True:
            t.cancel()
        last_reading = prediction
        print(prediction)








    
