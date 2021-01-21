
#import libraries 
import json
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers,Sequential,models
import os.path
from radar_configuration import Radar
from threading import Timer,Thread
import time
import numpy as np
import time
import json



#this function will be opened in a thread for fast reading readings from sensor
def get_readings(com_num):   
    '''
    this function will be an opned thread to take readings from the radar
    it will get frames from the radar then produce it in the queue
    '''
    radar = Radar(port=com_num)
    if(radar.is_open()):
        radar.close()
    radar.start()	
    radar.clear_buffer()
    while 1:             
        reading = radar.read_magnitude()   
        if reading is not None:
            yield reading
        else:
            yield None
           
       
      


class Face_Detection():
    def __init__(self):
        self.model = None

    def make_prediction(self,reading):
        result = self.model.predict(reading) > .8
        return result


    def test_live(self,reading):       
        '''
        this function read a reading from the sensor and make a prediction

        :return: a predicition of true as there is an object or false if there is no object

        [1,2,3,4,5]
        [[1,2,3,4,5],[2,3,4,5,]]

        '''              
        while reading is None:
            #print(reading)       
            return

        var_reading = reading
        y= self.model.predict(np.reshape(var_reading,(1,len(var_reading))))>.8        
        if y is None:            
            return None
        face_exists =  y[0][0]
        print(face_exists)

        if(face_exists):            
            distance, _ = self.range_face_detection(var_reading)
            print(distance)
            return distance
        print('noooo face')
        return None

    def modele_naive(self,X_data_train,Y_data_train,X_data_val,Y_data__val):
        '''
        :param X_data_train:
        :param Y_data_train:
        :param X_data_val:
        :param Y_data__val:
        :return: the trained model
        '''
        if os.path.isfile('model_naive3.h5'):
            model = models.load_model('model_naive3.h5')
            self.model = model
            return
        shape_input=X_data_train.shape[1]
        model = keras.Sequential()
        model.add(layers.Dense(64,input_dim=shape_input,activation='relu'))
        model.add(layers.Dense(32, activation='relu'))
        model.add(layers.Dense(16, activation='relu'))
        model.add(layers.Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X_data_train, Y_data_train, epochs=200, batch_size=32, validation_data=(X_data_val, Y_data__val))
        model.save('model_naive3.h5')
        self.model=model
        return

    def format_data(self,positives,negatives,split_per):
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


    def range_face_detection(self,frame,bin_resolution=8):  
        '''
        a simple function to test object within range 
        '''
        print("1111111111111111111111")
        print(len(frame))
        range_start = 300
        range_end= 2071
        bin_start=int(range_start/bin_resolution)
        bin_end=int(range_end/bin_resolution)
        face_frame=frame[bin_start:min(bin_end,len(frame))-1]
        max_index=np.argmax(face_frame)
        peak_distance=range_start + bin_resolution*max_index
        print("there is a peak at distance "+str(peak_distance))
        print("with magnitude =  "+str(max(face_frame)))
        return peak_distance,max(face_frame)

    def import_data(self,file_path):
        all_frames=[]
        with open(file_path, 'r') as f:
            allframes = f.readlines()
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
                        if len(frame) == 511:
                            all_frames.append(frame)
                    except:
                        continue
                    else:
                        continue

        return all_frames


if __name__=='__main__':
    configuration_file = open('configuration.json',)
    configuration_json = json.load(configuration_file)     
    sensor_port = configuration_json["SENSOR_PORT"]
    df = Face_Detection()
    positives = df.import_data(file_path='data_set\\person_in_range\\positives.txt') #read the object on readings
    negatives = df.import_data(file_path='data_set\\person_in_range\\negatives.txt') #read the object off redings    
    X_data_train,Y_data_train,X_data_val,Y_data__val =df.format_data(positives,negatives,.7) #preprocessing on data
    df.modele_naive(X_data_train,Y_data_train,X_data_val,Y_data__val) # build and train the model or just return it if already trained
    print(df.model.summary()) 
    for reading in get_readings(sensor_port):        
        if reading is None:
            continue
        distance,max_magnitude = df.range_face_detection(reading,8)
        print("the max distance is "+str(distance))
        print("the max magnitude is "+str(max_magnitude))
       








    
