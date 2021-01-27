import serial
import time
import numpy as np
import json

class Radar():
    '''
    this is the radar configuration class this will implement all low level communication with the radar sensor
    '''

    def __init__(self):
        configuration_file = open('configuration.json',)
        self.configuration_json = json.load(configuration_file)
        self.sensor_port = self.configuration_json["SENSOR_PORT"]
        self.max_distance = self.configuration_json["RANGE_OF_INTEREST"]["MAX_DISTANCE"]
        self.min_distance = self.configuration_json["RANGE_OF_INTEREST"]["MIN_DISTANCE"]
        self.baudrate = self.configuration_json["BAUD_RATE"]
        self.bin_resolution = self.configuration_json["BIN_RESOLUTION"] 
        '''
        define a connection through the serial port
        '''
        self.ser = serial.Serial(port=self.sensor_port, baudrate=self.baudrate)

    def is_open(self):
        '''
            check if the connection is open
        '''
        return self.ser.is_open

    def start(self):
        '''
            start the connection
        '''
        try:
            self.ser.open()
        except:
            raise Exception('cant open connection')

    def close(self):
        '''
            close the connection 
        '''
        self.ser.close()

    def clear_buffer(self):
        '''
            clear buffer of the pc of the communication
        '''
        self.ser.read_all()

    def store_readings(self, file_name):
        num = self.configuration_json["NUMBER_OF_TRAIN_SET"]
        file = open(file_name,'a')
        for _ in range(num):
            reading = self.get_reading()
            file.write(reading)
    
    def retrive_samples(self,file_name):
        readings = [] 
        file = open(file_name,'r')        
        reading = self.get_reading()
        file.readline()
        readings.append(reading)
        return readings
    


    def setup_radar(self):
        if(self.is_open()):
            self.close()
            self.start()	
        self.clear_buffer()


    def get_median_distance(self,num):
        threashold = self.configuration_json["THRESHOLD"]
        readings = []
        count = 0 
        while(count!=num):
            reading = self.get_reading()
            readings.append(reading)
            count +=1
        distances = []
        for reading in readings:
            distance,magnitude = self.range_face_detection(reading)
            if magnitude > threashold:
                distances.append(distance)
        if(len(distances)==0):
            return -1
        return np.median(distances)

    
    def range_face_detection(self,frame):  
        '''
        a simple function to test object within range 
        '''        
        #print(len(frame))
        range_start = self.min_distance
        range_end= self.max_distance
        bin_resolution = self.bin_resolution
        bin_start=int(range_start/bin_resolution)
        bin_end=int(range_end/bin_resolution)
        face_frame=frame[bin_start:min(bin_end,len(frame))-1]
        max_index=np.argmax(face_frame)
        peak_distance=range_start + bin_resolution*max_index
        print("there is a peak at distance "+str(peak_distance))
        print("with magnitude =  "+str(max(face_frame)))
        return peak_distance,max(face_frame)


    def get_reading(self):   
        '''
        this function will be an opned thread to take readings from the radar
        it will get frames from the radar then produce it in the queue
        '''
        reading = self.read_magnitude()   
        if reading is not None:
            return reading
        else :
            return self.get_reading()


    def read_magnitude(self):
        '''
        this function for reading a frame from  the radar that contains the magintude information
        '''
        line = self.ser.readline()  # read a line from the sensor
        newLine = line.decode("utf-8")
        splittedLine = newLine.split("\t")#!R \t counter \t frame_size \t 109 \t 255 0-->-140 /r/n
        if (splittedLine[0] != '!R'):  # check for start frame
            return None
        index = -1
        try:
            index = splittedLine.index('\r\n')  # seach for the end frame
        except ValueError as e:
            print(e)
            return None
        if (index == -1):
            return None
        else:       
            try:      
                frame = [int(i) for i in splittedLine[3:index]]  # get the frame   
                      
                #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")   
                #print(len(frame))
                if(len(frame) != 1024):
                    return None
                return frame
            except:
                return None
        return None


if __name__ == "__main__":
    radar = Radar()    
    while 1:
        print(radar.read_magnitude())
    #radar.store_readings('negatives.txt')
        
        
