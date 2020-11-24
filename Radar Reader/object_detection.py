
import json
import numpy as np
import pandas as pd
from tensorflow import keras
from tensorflow.keras import layers,Sequential,models
import os.path
class Object_detection():
    my_model = None

    @staticmethod
    def import_data(file_name):
        all_frames=[]
        with open(file_name, 'r') as f:
            allframes=f.readlines()
            count =0
            for line in allframes:
                if count == 200:
                    break
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
                    except:
                        continue
                    all_frames.append(frame)
        return all_frames



    @staticmethod
    def preprocesseing(data):
        return data

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
    def modele_naive(shape_input):
        '''
        :param shape_input:
        :param shape_output:
        :return:
        '''
        if os.path.isfile('model_naive.h5'):
            model = models.load_model('model_naive.h5')
            Object_detection.my_model = model
            return
        model = keras.Sequential()
        model.add(layers.Dense(8,input_dim=shape_input,activation='relu'))
        model.add(layers.Dense(4, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X_data_train, Y_data_train, epochs=100, batch_size=10, validation_data=(X_data_val, Y_data__val))
        model.save('model_naive.h5')
        Object_detection.my_model = model
        return
    @staticmethod
    def make_prediction(model,reading):
        return model.predict(reading) > .8

if __name__=='__main__':
    positives = Object_detection.import_data(file_name='positives.txt')
    negatives = Object_detection.import_data(file_name='negatives.txt')
    X_data_train,Y_data_train,X_data_val,Y_data__val = Object_detection.format_data(positives,negatives,.7)
    Object_detection.modele_naive(X_data_train.shape[1])
    print(Object_detection.my_model.summary())
    y=Object_detection.my_model.predict(X_data_val[0:3])
    print(y)





    
