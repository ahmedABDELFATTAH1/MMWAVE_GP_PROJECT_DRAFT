import numpy as np
import plotly.express as px
import pandas as pd
import serial
import time
from enum import Enum
import json
from radar_configuration import Radar
from threading import Thread
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

stepAngle = 0.45

scanningLowerStepSize = 5
scanningUpperStepSize = 5

maxAngleUpper = 22.5
maxStepsOfUpper = maxAngleUpper/(stepAngle*scanningUpperStepSize)

maxAngleLower = 22.5
maxStepsOfLower = maxAngleLower/(stepAngle*scanningLowerStepSize)

calibrateLowerStepSize = 10
calibrateLowerTotalStepsCount = 20



configuration_file = open('configuration.json',)
configuration_json = json.load(configuration_file)
arduino_port = configuration_json["ARDUINO_PORT"]


class Motors(Enum):
    LOWER = 'l'
    UPPER = 'u'


class Direction(Enum):
    POSITIVE = 1
    NEGATIVE = -1



radar = Radar()
global_distance = -1
def get_readings_thread():
    global global_distadnce
    while(True):
        global_distance = radar.get_median_distance(3)
        print("global distance = ",global_distance)


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
    detect = False
    count = 0
    # looping until face is found or rotated 90 degrees to the right
    while(count < calibrateLowerTotalStepsCount):
        moveMotor(Motors.LOWER.value, calibrateLowerStepSize,
                  Direction.POSITIVE.value)
        count += 1
        result = radar.get_median_distance(1) 
        if result != -1:
            detect = True
                 
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
        result = radar.get_median_distance(1) 
        if result != -1:
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


def moveMotor(motor: Motors, stepSize, direction: Direction):
    txt = motor + str(direction * stepSize) + "$"
    arduino.write(bytes(txt, 'utf-8'))
    time.sleep(.1)
    arduino.readline()


def scanFace(lowerDirection):
    global global_distance
    upperDirection = False
    
    moveU = True
    moveL = True
    uCounter = 0
    lCounter = 0
    count = 0
    dResult =[]
    uResult = []
    lResult = []
    while(moveL):

        while(moveU):
            if(upperDirection):
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.POSITIVE.value)
                uCounter += 1
                count+=1
            else:
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.NEGATIVE.value)
                uCounter -= 1
                count+=1
            
            distance = global_distance
#             print("######################################")
#             print("upperMoter.distance = ",distance)
#             print("upperMoter.count = ",count)
#             print("upperMoter.uCounter = ",uCounter)
#             print("upperMoter.lCounter = ",lCounter)
#             print("######################################")
            if (distance != -1):
                dResult.append(distance)
                uResult.append((uCounter * 0.45*np.pi)/180)
                lResult.append((lCounter * 0.45*np.pi)/180)
            # if distance >= min_distance and distance <= max_distance:
            #     detect = True
            #     print(distance)
            #     moveU = True
            # else:
            #     moveU = False
            print("upperMoter.count = ",count)
            if count == maxStepsOfUpper:
                moveU = False
                count = 0
        moveU = True
        upperDirection = not upperDirection
        # if(upperDirection):
        #     moveMotor(Motors.UPPER.value, scanningUpperStepSize,
        #               Direction.POSITIVE.value)
        #     uCounter += 1
        # else:
        #     moveMotor(Motors.UPPER.value, scanningUpperStepSize,
        #               Direction.NEGATIVE.value)
        #     uCounter -= 1

        moveMotor(Motors.LOWER.value, scanningLowerStepSize, lowerDirection)
        lCounter += 1
        distance = global_distance
        if (distance != -1):
            dResult.append(distance)
            uResult.append((uCounter * 0.45*np.pi)/180)
            lResult.append((lCounter * 0.45*np.pi)/180)
        if lCounter == maxStepsOfLower:
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

def move_with_keyboard ():
    global global_distance
    val = ""
    uCounter = 0
    lCounter = 0
    xArr = []
    yArr = []
    zArr = []
    fig = plt.figure()
    ax = fig.add_subplot(111,projection="3d")
    
    while val != "e":
        val = input("Enter your value: ") 
        if (val == "d"):
            moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.POSITIVE.value)
            lCounter += 1
        elif (val == "a"):
            moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.NEGATIVE.value)
            lCounter -= 1
        elif (val == "w"):
            moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.NEGATIVE.value)
            uCounter += 1
        elif (val == "s"):
            moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.POSITIVE.value)
            uCounter -= 1
        dist = global_distance
        uAngel = (uCounter * 0.45*np.pi)/180
        lAngel = (lCounter * 0.45*np.pi)/180
        x , y , z = dist*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
        xArr.append(x)
        yArr.append(y)
        zArr.append(z)
        # fig = plt.figure()
        # ax = fig.add_subplot(111,projection="3d")
        my_sample_x = np.array(xArr)
        my_sample_y = np.array(yArr)
        my_sample_z = np.array(zArr)
        # ax.scatter (my_sample_x,my_sample_y, my_sample_z, s=5, c="r", marker = 'o')
        # ax.set_xlabel("X")
        # ax.set_ylabel("Y")
        # ax.set_zlabel("Z")
        # ax.set_xlim(-300, 300)
        # ax.set_ylim(-300, 300)
        # ax.set_zlim(-300, 300)
        # plt.show()
        
        cat_g = ['setosa']
        sample_cat = [cat_g[np.random.randint(0,1)] for i in range (len(my_sample_z))]

        df = pd.DataFrame(my_sample_x,columns=['sepal_length'])
        df['sepal_width'] = my_sample_y
        df['petal_width'] = my_sample_z
        df['species'] = sample_cat
        df.head()
        fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                color='species',range_x = [-500,500],range_y = [-500,500],range_z=[-500,500])
        fig.show()

if __name__ == "__main__":
    

    arduino = set_up()
    # setting upp arduino ports
    t1 = Thread(target=get_readings_thread,daemon=False)
    t1.start()
    move_with_keyboard ()
   

    # moves the sensor in lower direction (XY plane) until the face is found
    
    # lowerDirection = calibrateLower()
    lowerDirection = 1
    dist = []
    uAngel =[]
    lAngel = []
    if(lowerDirection is None):
        moveMotor(Motors.LOWER.value, maxStepsOfLower,
                  Direction.POSITIVE.value)
    else:
        dist,uAngel,lAngel = scanFace(lowerDirection)
    
        x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
        print(x)
        print(y)
        print(z)

        my_sample_x = np.array(x)
        my_sample_y = np.array(y)
        my_sample_z = np.array(z)
        
        cat_g = ['setosa']
        sample_cat = [cat_g[np.random.randint(0,1)] for i in range (len(my_sample_z))]

        df = pd.DataFrame(my_sample_x,columns=['sepal_length'])
        df['sepal_width'] = my_sample_y
        df['petal_width'] = my_sample_z
        df['species'] = sample_cat
        df.head()
        fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
                color='species',range_x = [-500,500],range_y = [-500,500],range_z=[-500,500])
        fig.show()