import serial
import time

class Radar():
    def __init__(self,port='com4',baudrate = 1000000):
        self.ser=serial.Serial(port=port,baudrate=baudrate)

    def is_open(self):
        return self.ser.is_open
    
    def start(self):
        self.ser.open()

    def close(self):
        self.ser.close()
    
    def read_magnitude(self):        
        line = self.ser.readline() 
        newLine = line.decode("utf-8")        
        splittedLine = newLine.split("\t") 
        if(splittedLine[0]=='!R'):   
            #print(splittedLine[1:min(len(splittedLine),6)])
            pass
        else:
            return None
        index = -1
        try:
            index=splittedLine.index('\r\n')
        except ValueError as e:
            print(e)
            
        if(index==-1):
            return None
        else:
            counter=splittedLine[1]
            size=splittedLine[2]
            #print('counter value = '+str(counter))
            #print('size value = '+str(size))
            return splittedLine[4:index]
        return None      





    
	
        
	