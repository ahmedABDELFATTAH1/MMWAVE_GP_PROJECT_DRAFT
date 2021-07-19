from enum import Enum
import json
import serial


class Motors(Enum):
    LOWER = 'l'
    UPPER = 'u'


class Direction(Enum):
    POSITIVE = 1
    NEGATIVE = -1


class Arduino():

    def __init__(self):

        self.configuration_file = open('configuration.json',)
        self.configuration_json = json.load(self.configuration_file)
        self.arduino_port = self.configuration_json["ARDUINO_PORT"] #arduino port number

        self.motors_delay  = self.configuration_json["MOTORS_DELAY"] #Delay of each read
        self.stepAngle = self.configuration_json["STEP_ANGLE"] 
        self.baudrate = self.configuration_json["BAUD_RATE"]

        self.scanningLowerStepSize = self.configuration_json["LOWER_STEP_SIZE"] #the number of movements the lower motor will move at each step
        self.scanningUpperStepSize = self.configuration_json["UPPER_STEP_SIZE"] #the number of movements the upper motor will move at each step

        self.maxAngleUpper = self.configuration_json["MAX_ANGLE_UPPER"]  #the angle that the upper motor will move during the scan
        self.maxStepsOfUpper = self.maxAngleUpper/(self.stepAngle*self.scanningUpperStepSize) #the number of steps that the upper motor will move during the scan

        self.maxAngleLower = self.configuration_json["MAX_ANGLE_LOWER"] #the angle that the lower motor will move during the scan
        self.maxStepsOfLower = self.maxAngleLower/(self.stepAngle*self.scanningLowerStepSize) #the number of steps that the lower motor will move during the scan

        self.ser = serial.Serial()

    def is_open(self):
        '''
            open the connection
        '''
        return self.ser.is_open

    def start(self):
        '''
            start the connection
        '''
        try:
            self.ser.baudrate = self.baudrate
            self.ser.port = self.arduino_port
            # self.ser.timeout = 1
            self.ser.open()
            print("Arduino is connected :: ",self.ser.is_open)
            print("Arduino state is :: ",self.ser.readline().decode("utf-8") )
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

    def setup_arduino(self):
        if(self.is_open()):
            self.close()
            self.start()
        else :
            self.start()

    def moveMotor(self , motor: Motors, stepSize, direction: Direction):
        """
        Moves motor in arduino
        input : motor --> can be either 'l' for lower motor 
                    or  'u' for upper motor
            stepSize --> (integer) number of steps that the motor will move (step = 0.45 angle)
            direction -->  either -1 or 1 
        """
        txt = motor + str(direction * stepSize) + "$"
        self.ser.write(bytes(txt, 'utf-8'))
        self.ser.readline()

        
