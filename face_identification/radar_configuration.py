import serial
import time
import numpy as np
import json

import matplotlib.pyplot as plt


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
        '''
        define a connection through the serial port
        '''
        self.ser = serial.Serial(port=self.sensor_port, baudrate=self.baudrate,timeout=1)

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

    def configure_radar(self, commands):
        for command in commands:
            self.ser.write((command+"\r\n").encode())
        self.clear_buffer()
        time.sleep(1)
    def generate_commnds1(self):
        #!S11462E82
        #!S11422E82
        configuration = [
            "!F08075300",
            self.configuration_json["RADAR_CONFIGURATION"]["TRIGGER"]["SELF_TRIGGER"],
            self.configuration_json["RADAR_CONFIGURATION"]["AGC"]["DISABLE_AGC"],
            self.configuration_json["RADAR_CONFIGURATION"]["OUTPUT"]["MAGNITUDE_RANGE_ENABLE"],
            self.configuration_json["RADAR_CONFIGURATION"]["OUTPUT"]["CFAR_DISABLE"],
            self.configuration_json["RADAR_CONFIGURATION"]["OUTPUT"]["TARGET_LIST_DISABLE"],
            self.configuration_json["RADAR_CONFIGURATION"]["OUTPUT"]["STATUS_FRAME_DISABLE"],
            self.configuration_json["RADAR_CONFIGURATION"]["OUTPUT"]["ERROR_FRAME_DISABLE"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["ADC_CLK_DIVIDER"]["5"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["NUMBER_OF_SAMPLES"]["512"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["NUMBER_OF_RAMPS"]["8"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["DC_CANCLE"]["ON"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["FIR_FILTER"]["ON"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["DOWNSAMPLING"]["2"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["WINDOWING"]["ON"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["FFT_SIZE"]["1024"],
            self.configuration_json["RADAR_CONFIGURATION"]["BB_PROCESSING"]["AVG_N"]["1"],
            self.configuration_json["RADAR_CONFIGURATION"]["MODE"]["TSV"]
        ]

        '''
        !F08075300
        !BA452C115
        !BA452C0D5
        !BE452C0D5
        !BE452E0D5

        '''
        configuration1 = [               
                "!F08075300",
                "!BA452C115",
                "!S11402F82",
                "!BE452C125",
                "!BA452C0D5",
                "!BE452C0D5",
                "!BE452E0D5",
                "!S11442082" ,                
                "!BA452C125",
                "!S11402F82",
                "!K",
                "!BA452C115",
                "!BA452C095",
                "!BA452E095",
                "!BE452E095",
                "!S11402E82",
                "!S11402E82",
                "!S11402C82",
                "!S11402C82",
                "!S11402882",
                "!S11402882",
                "!S11402082",
                "!S11402082",
                "!S11442082"
                          ]

        configuration2 = ["!F08075300",
                          "!BA452C115",
                          "!S11402F82",
                          "!BE452C125",
                          "!BA452C0D5",
                          "!BE452C0D5",
                          "!BE452E0D5",
                          "!S11442082"                          
                          ]
        #self.configure_radar(configuration2)

    def save_readings (self):
        file = open("radar_readings.txt", "a")
        while 1:
            line = self.ser.readline()  # read a line from the sensor
            newLine = line.decode("utf-8")
            if (newLine[0] == '!' and len(newLine) > 200):
                print (len(newLine))
                file.write(str(newLine)+"\n") 
        file.close()
    def setup_radar(self):
        if(self.is_open()):
            self.close()
            self.start()
        self.clear_buffer()

    def get_median_distance(self, num):  
        frame = self.get_reading()         
        indexes,distance =  self.detect_peaks(frame)  
        if indexes is None:
            return -1        
        return distance

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


    def read_magnitude_waleed(self):
        '''
        this function for reading a frame from  the radar that contains the magintude information
        '''
        filepath = 'radar_readings.txt'
        filehandle = open(filepath, 'r')
        while True:
            line = filehandle.readline()
            print(line)
            splittedLine = line.split("\t")
            
            frame = [int(i) for i in splittedLine[3:len(splittedLine)-1]]  # get the frame

            print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            print(len(frame))
            print(frame)
            yield  frame
            
    def read_magnitude(self):
        '''
        this function for reading a frame from  the radar that contains the magintude information
        '''
        #print(line)
       
        line = self.ser.readline()  # read a line from the sensor
        newLine = line.decode("utf-8")
        # print("111")        
        # !R \t counter \t frame_size \t 109 \t 255 0-->-140 /r/n
        splittedLine = newLine.split("\t")
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
                frame = [int(i)
                         for i in splittedLine[3:index]]  # get the frame

                # print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                #print(len(frame))
                #print(frame)
                if(len(frame) != 1024):
                    return None
                return frame
            except:
                return None
        return None

    def detect_peaks(self,frame):
        """
        Detect peaks with CFAR algorithm.

        num_train: Number of training cells.
        num_guard: Number of guard cells.
        rate_fa: False alarm rate. 
        """
        num_train = self.background_number
        num_guard = self.guard_number

        y= np.array(frame)
        y =y+ np.abs(np.min(y))
        x = np.arange(y.size)*self.bin_resolution     
        num_cells = y.size
        num_train_half = round(num_train / 2)
        num_guard_half = round(num_guard / 2)
        num_side = num_train_half + num_guard_half
        peak_idx = []
        
        alpha = num_train*(self.false_rate**(-1/num_train) - 1) # threshold facto
        # print(alpha)
        for i in range(num_side, num_cells - num_side):
            if i != i-num_side+np.argmax(y[i-num_side:i+num_side+1]):
                continue
            sum1 = np.sum(y[i-num_side:i+num_side+1])
            sum2 = np.sum(y[i-num_guard_half:i+num_guard_half+1])
            p_noise = (sum1 - sum2) / num_train
            # print(p_noise)
            threshold = alpha * p_noise
            if y[i] >threshold and y[i] >80 and x[i]>self.min_distance and x[i]<self.max_distance:
                peak_idx.append(i)
            max_index = 0
            y_max = -1
            for index in peak_idx:
                if y[index] > y_max:
                    max_index = index
                    y_max = y[index]
            if y_max ==-1:
                return None,None
            else:
                return max_index,x[max_index]
       

    
                    
if __name__ == "__main__":
    radar = Radar()
    radar.setup_radar()   
    # radar.save_readings()
    a =  radar.read_magnitude_waleed()
    next(a)
    # while(1):
    #     frame = radar.get_reading()         
    #     indexes,_ =  radar.detect_peaks(frame)  
    #     if indexes is None:
    #         indexes = []
    #     y= np.array(frame)
    #     y =y+ np.abs(np.min(y))
    #     x = np.arange(y.size)*radar.bin_resolution      
    #     plt.plot(x, y)
    #     plt.plot(x[indexes],y[indexes], 'rD')
    #     plt.xlabel('x')
    #     plt.ylabel('y')
    #     plt.show()
