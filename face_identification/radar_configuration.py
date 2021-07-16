import serial
import time
import numpy as np
import json
import zmq
import matplotlib.pyplot as plt
import json
import numpy as np
from scipy import stats
from tensorflow import keras
from tensorflow.keras import layers,Sequential,models

import os.path

correct_frames = 0
dropped_frames = 0 
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
        self.guard_number = self.configuration_json["CFAR_CONFIG"]["GUART_NUMBER"]
        self.background_number = self.configuration_json["CFAR_CONFIG"]["BACKGROUND_NUMBER"]
        self.false_rate = self.configuration_json["CFAR_CONFIG"]["RATE_FA"]
        self.threashold = self.configuration_json["THRESHOLD"]
        self.frame_size = self.configuration_json["FRAME_SIZE"]
        # self.g_model = models.load_model('model_naive3.h5')
        # self.f_model = models.load_model('face_model.h5')
        '''
        define a connection through the serial port
        '''
        self.ser = serial.Serial()

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
            self.ser.baudrate = self.baudrate
            self.ser.port = self.sensor_port
            # self.ser.timeout = 1
            self.ser.open()
        except serial.SerialException:
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
        return self.ser.read_all()
        # self.ser.reset_input_buffer()
        # self.ser.reset_output_buffer()
    def check_buffer(self):
        '''
            clear buffer of the pc of the communication
        '''
        return self.ser.inWaiting()

    def store_readings(self, file_name):
        num = self.configuration_json["NUMBER_OF_TRAIN_SET"]
        file = open(file_name, 'a')
        for _ in range(num):
            reading = self.get_reading()
            file.write(reading)

    def retrive_samples(self, file_name):
        readings = []
        file = open(file_name, 'r')
        reading = self.get_reading()
        file.readline()
        readings.append(reading)
        return readings

    ####################Configurations_Section#######################

    def configure_radar(self, command):
        self.ser.write((command+"\r\n").encode())

    def trigger_reading(self):
        self.ser.write(("!M\r\n").encode())
    
    def setup_radar_system_configuration(self):
        json_config = self.configuration_json["SYS_CONFIG"]
        config_str = ""
        for key in json_config:
            if key == "ID":
                continue
            config_str = config_str + json_config[key]

        config_str = '%0*X' % ((len(config_str) + 3) // 4, int(config_str, 2))
        config_str = json_config["ID"] + config_str
        self.configure_radar(config_str)

    def setup_radar_front_end_configuration(self):
        json_config = self.configuration_json["RFE_CONFIG"]
        config_str = ""
        for key in json_config:
            if key == "ID":
                continue
            config_str = config_str + json_config[key]

        config_str = '%0*X' % ((len(config_str) + 3) // 4, int(config_str, 2))
        config_str = json_config["ID"] + config_str
        self.configure_radar(config_str)

    def setup_radar_pll_configuration(self):
        json_config = self.configuration_json["PLL_CONFIG"]
        config_str = ""
        for key in json_config:
            if key == "ID":
                continue
            config_str = config_str + json_config[key]

        config_str = '%0*X' % ((len(config_str) + 3) // 4, int(config_str, 2))
        config_str = json_config["ID"] + config_str
        self.configure_radar(config_str)

    def setup_radar_baseband_configuration (self):
        json_config = self.configuration_json["BB_CONFIG"]
        config_str = ""
        for key in json_config:
            if key == "ID":
                continue
            config_str = config_str + json_config[key]

        config_str = '%0*X' % ((len(config_str) + 3) // 4, int(config_str, 2))
        config_str = json_config["ID"] + config_str
        self.configure_radar(config_str)

    def setup_radar_all_configurations(self):
        self.setup_radar_system_configuration()
        self.setup_radar_front_end_configuration()
        self.setup_radar_pll_configuration()
        self.setup_radar_baseband_configuration()

    def setup_radar_set_max_bandwidth (self):
        config_str = "!K00000000"
        self.configure_radar(config_str)


    ##################################################################    
    def save_readings (self):
        while 1:
            file = open("radar_readings.txt", "a")
            line = self.ser.readline()  # read a line from the sensor
            newLine = line.decode("utf-8")
            if (newLine[0] == '!'):
                splittedLine = newLine.split("\t")
                try :
                    frame = [int(i) for i in splittedLine[3:len(splittedLine)-1]]
                    if (len(frame) == 512):
                        # print (len(frame))
                        file.write(str(frame)+"\n") 
                        file.close()
                    else:
                        print ('error in frame size')
                except:
                    print ('can\'t create the frame')    

    def setup_radar(self):
        if(self.is_open()):
            self.close()
            self.start()
        else :
            self.start()


    def get_median_distance(self, num):  
        frame = self.get_reading()         
        indexes,distance =  self.detect_peaks(frame)  
        if indexes is None:
            return frame,-1, -1        
        return frame,indexes,distance

    def range_face_detection(self, frame):
        '''
        a simple function to test object within range 
        '''
        # print(len(frame))
        range_start = self.min_distance
        range_end = self.max_distance
        bin_resolution = self.bin_resolution
        bin_start = int(range_start/bin_resolution)
        bin_end = int(range_end/bin_resolution)
        face_frame = frame[bin_start:min(bin_end, len(frame))-1]
        max_index = np.argmax(face_frame)
        peak_distance = range_start + bin_resolution*max_index
        #print("there is a peak at distance "+str(peak_distance))
        #print("with magnitude =  "+str(max(face_frame)))
        return peak_distance, max(face_frame)

    def get_reading(self):
        '''
        this function will be an opned thread to take readings from the radar
        it will get frames from the radar then produce it in the queue
        '''
        reading = self.read_magnitude()
        if reading is not None:
            return reading
        else:
            return self.get_reading()


    def get_frame(self):
        frame = []
        frame_range = False
        while True:
            try:
                oneByte = self.ser.read(1).decode('utf-8')
            except:
                print("sorry wrong format please convert to tsv mode")
                raise TypeError            
            if frame_range: 
                if oneByte == "\r\n":
                    #end of frame
                    frame_range = False             
                    return frame  
                elif oneByte == "!R":                    
                    frame = []
                else:
                    try:
                        num = int(oneByte)
                        frame.append(num)
                    except ValueError:
                        frame = []
                        frame_range = False                         
            if oneByte == "!R":
                #this means start of the desired frame 
                frame_range = True
            

                

    def read_magnitude(self):
        '''
        this function for reading a frame from  the radar that contains the magintude information
        '''
        global dropped_frames,correct_frames
        correct_frames+=1
        #print(line)
        # self.ser.reset_input_buffer()
        # while self.ser.in_waiting <2600:
        #     print("waiting")
        #     pass
        line = self.ser.readline()  # read a line from the sensor
        # print ("in waiting :: ",self.ser.in_waiting)
        # line =""
        # while len(line) == 0:
        #     line = self.clear_buffer()
        # print(line)
        # print ("wanted length :: ", len(line))

        newLine = line.decode("utf-8")  
        # print (newLine)           
        # !R \t counter \t frame_size \t 109 \t 255 0-->-140 /r/n
        if newLine == "I am Easy\r\n":
            return None
        if newLine == "Front End \x02\r\n":
            return None
    
        # splittedLine = newLine.split("!R")

        # print (splittedLine)
        splittedLine = newLine.split("\t")
        # print(splittedLine[0])
        if (splittedLine[0] != '!R'):  # check for start frame
            print("\'!R\' is missing, frame has been dropped !!!!!")
            dropped_frames+=1
            return None
        if (splittedLine[len(splittedLine)-1] == '\r\n'):
            print ("frame number  :: ",splittedLine[1])
            frame = splittedLine[3:len(splittedLine)-1]
            try:
                intx = [ int(fr) for fr in frame]
            except:
                print("double -ve are detected\"like -20-21\", frame has been dropped !!!!!")
                dropped_frames+=1
                return None
            return intx
        else:
            print("\'\\r\\n\' are missing, frame has been dropped ")
            dropped_frames+=1
        # index = -1
        # try:
        #     # print("here")
        #     index = splittedLine.index('\r\n')  # seach for the end frame
        #     # print(index)
        # except ValueError as e:
        #     #print(e)
        #     return None
        # if (index == -1):
        #     return None
        # else:
            # try:
            #     frame = [int(i)
            #              for i in splittedLine[3:index]]  # get the frame
            #     #print("message",splittedLine[0:4])
            #     if(len(frame) != self.frame_size):
            #         return None
            #     return frame
            # except:
            #     return None
            
        return None

    def get_max_magnitude_in_range(self,frame):
        min_index_range = int(self.min_distance/self.bin_resolution)
        max_index_range = int(self.max_distance/self.bin_resolution)
        max_index = np.argmax(frame[min_index_range:max_index_range])
        max_index = min_index_range + max_index
        max_distance = max_index * self.bin_resolution
        max_magnitude = frame[max_index]
        return max_index,max_distance,max_magnitude


    def make_prediction(self,reading,model):
        result = model.predict(np.reshape(reading,(1,len(reading))))>.3
        return result[0][0]
        
    def detect_peaks(self,frame, calibiration_mode, max_db):        
       
        # face_prediction = self.make_prediction(frame,self.g_model)
        face_body_prediction = True#self.make_prediction(frame,self.f_model)
        """
        Detect peaks with CFAR algorithm.
        num_train: Number of training cells.
        num_guard: Number of guard cells.
        rate_fa: False alarm rate. 
        """
        num_train = self.background_number
        num_guard = self.guard_number
        
        y= np.array(frame)
        # y =y+ np.abs(np.min(y))
        # print("Ahmed")
        # print(np.min(y))
        # print(y)
        x = np.arange(y.size)*self.bin_resolution  
        #print(x)  
        num_cells = y.size
        num_train_half = round(num_train / 2)
        num_guard_half = round(num_guard / 2)
        num_side = num_train_half + num_guard_half
        peak_idx = []
        
        alpha = num_train*(self.false_rate**(-1/num_train) - 1) # threshold facto
        # print(alpha)
        for i in range(len(frame)):
            # if i != i-num_side+np.argmax(y[i-num_side:i+num_side+1]):
            #     continue
            # sum1 = np.sum(y[i-num_side:i+num_side+1])
            # sum2 = np.sum(y[i-num_guard_half:i+num_guard_half+1])
            #p_noise = (sum1 - sum2) / num_train
            # print(p_noise)
            #threshold = alpha * p_noise
            #y[i] >threshold
            if calibiration_mode == True:
                if  (frame[i] >= self.threashold) and x[i]>self.min_distance and x[i]<self.max_distance  and face_body_prediction:
                    peak_idx.append(i)
            else:
                if (frame[i] >= self.threashold) and x[i]>self.min_distance and x[i]<self.max_distance  and face_body_prediction:
                    peak_idx.append(i)
            # print("size of x",len(x))
        max_index = 0
        y_max = -200
        # print("###################################################")
        # print (peak_idx)
        for index in peak_idx:
            # print ("inside peak detect")
            # print ("dis :: " ,x[index] ,"mag :: ",y[index])
            if y[index] > y_max:
                max_index = index
                y_max = y[index]
                
        if y_max == -200:            
            return None,None,None
        else:            
            return max_index,x[max_index],frame[max_index]

    def collect_n_samples(self,n_samples,n_readings):
        distances = []
        db_frames = []
        for i in range (n_samples):
            index, distance, db_frame = self.access_radar(n_readings) 
            distances.append(distance)
            db_frames.append(db_frame)   
        return "error inde is used",distances,db_frames  

    def access_radar(self,num):
        frame_payloads = []
        distances = []
        db_frames = []
        for i in range(num):
            frame_payloads.append(self.get_reading())

        for frame in frame_payloads:
            index, distance, db_frame = self.detect_peaks(frame, True, 0)
            distances.append(distance)
            db_frames.append(db_frame)
        print("before eliminating None values :: ", distances)
        distances = [0 if v is None else v for v in distances]
        print("after eliminating None values :: ", distances)
        z = np.abs(stats.zscore(np.array(distances)))
        # print(np.where(z > 3))
        # print(z)
        indecies = ~np.logical_or((z>=1), (z<=-1))
        # print(indecies)
        # print(z[indecies])
        distances = np.array(distances)
        print(distances[indecies])
        avrg_dis = np.average(distances[indecies])
        
        # print(indecies)
        # print(z[indecies])
        db_frames = np.array(db_frames).astype(float)
        print(db_frames[indecies])
        avrg_db = np.average(db_frames[indecies])
        
        return "error inde is used",avrg_dis,avrg_db
    
if __name__ == "__main__":
    radar = Radar()
    radar.setup_radar() 
    while(1):
        context = zmq.Context()
        zmq_socket = context.socket(zmq.PUB)    
        zmq_socket.bind("tcp://127.0.0.1:5558")
        # count=0
        while True:
            frame_payload = radar.get_reading()
            # print(len(frame_payload))
            # print(count)
            # count+=1
            frame = {
                "FRAME":frame_payload
            }
            zmq_socket.send_json(frame)
            print("#correct frames :: ", correct_frames)
            print("#dropped farmes :: ", dropped_frames)
            # index,distance,magnitude = radar.detect_peaks(frame["FRAME"],True,0)
            # print(distance)



