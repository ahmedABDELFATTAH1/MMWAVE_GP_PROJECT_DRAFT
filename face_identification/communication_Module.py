import serial
import time
from enum import Enum 

stepAngle = 0.45

maxAngleUpper = 45
maxStepsOfUpper = maxAngleUpper/stepAngle

maxAngleLower = 90
maxStepsOfLower = maxAngleLower/stepAngle

scanningLowerStepSize = 5
scanningUpperStepSize = 5

calibrateLowerStepSize = 10
calibrateLowerTotalStepsCount = 20

class Motors(Enum):
    LOWER = 'l'
    UPPER = 'u'

class Direction(Enum):
    POSITIVE = 1 
    NEGATIVE = -1

def set_up():
    arduino = serial.Serial()
    arduino.baudrate = 9600
    arduino.port = 'COM3'
    arduino.open()
    print(arduino.is_open)
    print(arduino.readline())
    return arduino


"""
if face was found return the direction of the lower motor 
else return none
"""
def calibrateLower():
    detect = False
    count = 0
    while(count < calibrateLowerTotalStepsCount):  # looping until face is found or rotated 90 degrees to the right
        moveMotor(Motors.LOWER.value , calibrateLowerStepSize , Direction.POSITIVE.value )
        count += 1
        if(detect):         
            return Direction.POSITIVE.value  # return that a face is found when rotating right
    moveMotor(Motors.LOWER.value , calibrateLowerStepSize * calibrateLowerTotalStepsCount , Direction.NEGATIVE.value )
    count = 0
    # looping until face is found or rotated 90 degrees to the left
    while(not detect and count > -1 * calibrateLowerTotalStepsCount):
        moveMotor(Motors.LOWER.value , calibrateLowerStepSize  , Direction.NEGATIVE.value )
        count -= 1
        if (count == -10): 
            detect = True
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
def moveMotor(motor : Motors , stepSize , direction : Direction) :
    txt = motor + str(direction * stepSize) + "$"
    arduino.write(bytes(txt, 'utf-8'))
    arduino.readline()
                    

def scanFace(lowerDirection) :
    upperDirection = False
    moveU = True
    moveL = True
    uCounter = 0
    lCounter = 0
    while(moveL):
        while(moveU):
            if(upperDirection):
                moveMotor(Motors.UPPER.value , scanningUpperStepSize , Direction.POSITIVE.value )
                uCounter += 1
            else:
                moveMotor(Motors.UPPER.value , scanningUpperStepSize , Direction.NEGATIVE.value )
                uCounter -= 1
            mean =abs(uCounter) # averageOfReadings(NumOfReadings)
            if(mean > 20 and mean < 60):
                moveU = False
        moveU = True
        upperDirection = not upperDirection
        if(upperDirection):
            moveMotor(Motors.UPPER.value , scanningUpperStepSize , Direction.POSITIVE.value )
            uCounter += 1
        else:
            moveMotor(Motors.UPPER.value , scanningUpperStepSize , Direction.NEGATIVE.value )
            uCounter -= 1
        
        moveMotor(Motors.LOWER.value , scanningLowerStepSize , lowerDirection )
        lCounter += 1
        mean = abs(lCounter) #averageOfReadings(NumOfReadings)
        if(mean > 20 and mean < 60):
            moveL = False


#setting upp arduino ports
arduino = set_up()

#moves the sensor in lower direction (XY plane) until the face is found
lowerDirection = calibrateLower()
if(lowerDirection is None):
    moveMotor(Motors.LOWER.value , maxStepsOfLower , Direction.POSITIVE.value)
else: 
    scanFace(lowerDirection)
    