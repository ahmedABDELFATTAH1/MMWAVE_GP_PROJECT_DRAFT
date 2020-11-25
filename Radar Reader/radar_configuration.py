import serial
import time
from threading import Timer


class Radar():
    '''
    this is the radar configuration class this will implement all low level communication with the radar sensor
    '''

    def __init__(self, port='com4', baudrate=1000000):
        '''
        define a connection through the serial port
        '''
        self.ser = serial.Serial(port=port, baudrate=baudrate)

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
        line = self.ser.readline()  # read a line from the sensor
        new_line = line.decode("utf-8")
        print(len(new_line))
        print(new_line[0:100])
        f = open(file_name, "a")
        f.write(new_line)
        f.close()


    def read_magnitude(self):
        '''
        this function for reading a frame from  the radar that contains the magintude information
        '''
        line = self.ser.readline()  # read a line from the sensor
        newLine = line.decode("utf-8")
        splittedLine = newLine.split("\t")
        if (splittedLine[0] != '!R'):  # check for start frame
            return None
        index = -1
        try:
            index = splittedLine.index('\r\n')  # seach for the end frame
        except ValueError as e:
            print(e)
        if (index == -1):
            return None
        else:
            counter = splittedLine[1]
            size = splittedLine[2]
            # print('counter value = '+str(counter))
            # print('size value = '+str(size))
            frame = [int(i) for i in splittedLine[4:index]]  # get the frame
            return frame
        return None


if __name__ == "__main__":
    radar = Radar(port='com5')
    if radar.is_open():
        radar.close()
    radar.start()
    radar.clear_buffer()
    while 1:
        radar.store_readings('positives.txt')
