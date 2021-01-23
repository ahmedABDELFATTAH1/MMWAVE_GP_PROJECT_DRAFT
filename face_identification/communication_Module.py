import serial
import time
from enum import Enum
from object_detection import *


stepAngle = 0.45

maxAngleUpper = 45
maxStepsOfUpper = maxAngleUpper/stepAngle

maxAngleLower = 90
maxStepsOfLower = maxAngleLower/stepAngle

scanningLowerStepSize = 5
scanningUpperStepSize = 5

calibrateLowerStepSize = 10
calibrateLowerTotalStepsCount = 20


configuration_file = open('configuration.json',)
configuration_json = json.load(configuration_file)
sensor_port = configuration_json["SENSOR_PORT"]
max_distance = configuration_json["MAX_DISTANCE"]
min_distance = configuration_json["MIN_DISTANCE"]
arduino_port = configuration_json["ARDUINO_PORT"]


class Motors(Enum):
    LOWER = 'l'
    UPPER = 'u'


class Direction(Enum):
    POSITIVE = 1
    NEGATIVE = -1


global_reading = None
df = Face_Detection()

def get_readings_thread():
    global global_reading
    while(True):
        reading = get_readings(sensor_port)
        if reading is not None:
            global_reading = reading
            df.range_face_detection(reading,bin_resolution=1)
            # print("##########################")
            # print(len(reading))
            # print("##########################")
        # else:
        #     print("IAM  NONE PLZ STOP")

def set_up():
    arduino = serial.Serial()
    arduino.baudrate = 9600
    arduino.port = arduino_port
    arduino.open()
    print(arduino.is_open)
    print(arduino.readline())
    return arduino


"""
if face was found return the direction of the lower motor 
else return none
"""


def calibrateLower():
    df = Face_Detection()
    detect = False
    count = 0
    # looping until face is found or rotated 90 degrees to the right
    while(count < calibrateLowerTotalStepsCount):
        moveMotor(Motors.LOWER.value, calibrateLowerStepSize,
                  Direction.POSITIVE.value)
        count += 1
        distance, max_magnitude = df.range_face_detection(global_reading, 8)
        if distance >= min_distance and distance <= max_distance:
            detect = True
            print(distance)
        if(detect):
            return Direction.POSITIVE.value  # return that a face is found when rotating right
    moveMotor(Motors.LOWER.value, calibrateLowerStepSize *
              calibrateLowerTotalStepsCount, Direction.NEGATIVE.value)
    count = 0
    # looping until face is found or rotated 90 degrees to the left
    while(not detect and count > -1 * calibrateLowerTotalStepsCount):
        moveMotor(Motors.LOWER.value, calibrateLowerStepSize,
                  Direction.NEGATIVE.value)
        count -= 1
        # if (count == -10):
        #     detect = True
        distance, max_magnitude = df.range_face_detection(global_reading, 8)
        if distance >= min_distance and distance <= max_distance:
            detect = True
            print(distance)
        if(detect):
            return Direction.NEGATIVE.value  # return that a face is found when rotating left
    return None


"""
Moves motor in arduino
motor --> can be either 'l' for lower motor 
          or  'u' for upper motor
stepSize --> (integer) number of steps that the motor will move (step = 0.45 angle)
direction -->  either -1 or 1 
"""


def moveMotor(motor: Motors, stepSize, direction: Direction):
    txt = motor + str(direction * stepSize) + "$"
    #arduino.write(bytes(txt, 'utf-8'))
    #arduino.readline()


def scanFace(lowerDirection):
    upperDirection = False
    df = Face_Detection()
    moveU = True
    moveL = True
    uCounter = 0
    lCounter = 0
    dResult =[]
    uResult = []
    lResult = []
    while(moveL):

        while(moveU):
            if(upperDirection):
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.POSITIVE.value)
                uCounter += 1
            else:
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.NEGATIVE.value)
                uCounter -= 1

            distance, max_magnitude = df.range_face_detection(
                global_reading, 8)
            dResult.append(distance)
            uResult.append(uCounter * 0.45)
            lResult.append(lCounter * 0.45)
            # if distance >= min_distance and distance <= max_distance:
            #     detect = True
            #     print(distance)
            #     moveU = True
            # else:
            #     moveU = False
            print(uCounter)
            if uCounter == 50 or uCounter == -50:
                moveU = False
        moveU = True
        uCounter = 0
        upperDirection = not upperDirection
        if(upperDirection):
            moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                      Direction.POSITIVE.value)
            uCounter += 1
        else:
            moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                      Direction.NEGATIVE.value)
            uCounter -= 1

        moveMotor(Motors.LOWER.value, scanningLowerStepSize, lowerDirection)
        lCounter += 1
        distance, max_magnitude = df.range_face_detection(global_reading, 8)
        dResult.append(distance)
        uResult.append(uCounter * 0.45)
        lResult.append(lCounter * 0.45)
        if lCounter == 50:
            moveL = False
        # if distance >= min_distance and distance <= max_distance:
        #     detect = True
        #     print(distance)
        #     moveL = True
        # else:
        #     moveL = False
        #     print("noooooooooooooooooooo")
        #     print(distance)
        #     print("noooooooooooooooooooo")

    return dResult,uResult,lResult


if __name__ == "__main__":
    # setting upp arduino ports
    t1 = Thread(target=get_readings_thread,daemon=False)
    t1.start()
    # arduino = set_up()

    # moves the sensor in lower direction (XY plane) until the face is found
    
    #lowerDirection = calibrateLower()
    # lowerDirection = 1
    # dist = []
    # uAngel =[]
    # lAngel = []
    # if(lowerDirection is None):
    #     moveMotor(Motors.LOWER.value, maxStepsOfLower,
    #               Direction.POSITIVE.value)
    # else:
    #     dist,uAngel,lAngel = scanFace(lowerDirection)
    
    # x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
    # print(x)