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
import zmq
import pickle

calibrateLowerStepSize = 10
calibrateLowerTotalStepsCount = 20

global_counter = 0
readings = []
distances = []

configuration_file = open('configuration.json',)
configuration_json = json.load(configuration_file)
arduino_port = configuration_json["ARDUINO_PORT"]
port = configuration_json["PORT"]

stepAngle = configuration_json["STEP_ANGLE"]

scanningLowerStepSize = configuration_json["LOWER_STEP_SIZE"]
scanningUpperStepSize = configuration_json["UPPER_STEP_SIZE"]

maxAngleUpper = configuration_json["MAX_ANGLE_UPPER"]
maxStepsOfUpper = maxAngleUpper/(stepAngle*scanningUpperStepSize)

maxAngleLower = configuration_json["MAX_ANGLE_LOWER"]
maxStepsOfLower = maxAngleLower/(stepAngle*scanningLowerStepSize)

state_min = configuration_json["STATE_MIN"]
state_max = configuration_json["STATE_MAX"]
state_counter = state_min

class Motors(Enum):
    LOWER = 'l'
    UPPER = 'u'


class Direction(Enum):
    POSITIVE = 1
    NEGATIVE = -1


radar = Radar()
# radar.setup_radar()
# radar.setup_radar_system_configuration()
# radar.setup_radar_pll_configuration()
# radar.setup_radar_baseband_configuration()

# global_distance = -1
# global_indexes = -1
# global_frame = -1

# radar = Radar()
# radar.setup_radar()

# def get_readings_thread():
    
#     global global_distance, global_indexes, global_frame
#     while(True):
#         # global_frame,global_indexes,global_distance = radar.get_median_distance(1)  
#         frame = radar.get_reading()
#         #print(len(frame))
        
#         # socket.send_string("%d,%s" % (topic, str(global_frame)))
#         #socket.send_multipart([b'status',pickle.dumps(global_frame), pickle.dumps(global_indexes)])
       
#         print("global distance = ",global_distance)

def error_correction(previous,current):
    global state_counter
    if current != -1:
        if(state_counter < state_max):
                state_counter+=1
        
        return current

    else:
        if state_counter == state_min:
            return current
        else:
            state_counter-=1
            return previous


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
    time.sleep(1)
    arduino.readline()


def scanFace(lowerDirection):
    global global_distance
    upperDirection = True
    
    moveU = True
    moveL = True
    uCounter = 0
    lCounter = 0
    count = 0
    count_lower_end = 0
    dResult =[]
    uResult = []
    lResult = []
    while(moveL):
        previous_distance = -1
        while(moveU):
            if(upperDirection):
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.POSITIVE.value)
                uCounter += scanningUpperStepSize
                count+=1
            else:
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.NEGATIVE.value)
                uCounter -= scanningUpperStepSize
                count+=1
            
            distance = global_distance
            distance = error_correction(previous_distance , distance)
            print("######################################")
            print("upperMoter.distance = ",distance)
            print("upperMoter.count = ",count)
            print("upperMoter.uCounter = ",uCounter)
            print("upperMoter.lCounter = ",lCounter)
            print("######################################")
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
            if count == maxStepsOfUpper:
                moveU = False
                count = 0
            previous_distance = distance
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
        lCounter += scanningLowerStepSize
        count_lower_end += 1
        distance = global_distance
        distance = error_correction(previous_distance , distance)
        if (distance != -1):
            dResult.append(distance)
            uResult.append((uCounter * 0.45*np.pi)/180)
            lResult.append((lCounter * 0.45*np.pi)/180)
        if count_lower_end == maxStepsOfLower:
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
        previous_distance = distance
    return dResult,uResult,lResult

def test_function():
    global readings, global_counter
    filereader = open('radar_readings.txt', 'r')
    lines = filereader.readlines()
    line = lines[len(lines)-1]
    filereader.close()
    # print (json.loads(line))
    frame = json.loads(line)
    try:
        index, distance, db_frame = radar.detect_peaks(frame)
        print("step number = ",global_counter," with db value = ", db_frame, " with a distance = ",distance)
        if (db_frame != None):
            distances.append(distance)
            readings.append(db_frame)
        else:
            distances.append(0)
            readings.append(0)
        open('radar_readings.txt', 'w').close()
    except:
        readings.append(0)
def scan2D_lower():
    global global_distance, global_counter
    
    lCounter = 0
    xResult = []
    yResult = []
    previous_distance = -1
    while(lCounter != maxStepsOfLower): 
        global_counter = lCounter
        test_function()
        # distance = global_distance
        # distance = -1
        # print("##############scan2D###############")
        # print("distance = ",distance)
        # print("lCounter = ",lCounter)
        # print("######################################")
        # distance = error_correction(previous_distance,distance)
        # if (distance != -1 and distance != None):
        #     yResult.append(distance)
        #     xResult.append((lCounter * scanningLowerStepSize))
        
        # else:
        #     yResult.append(0)
        #     xResult.append((lCounter * scanningLowerStepSize))

        
        moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.NEGATIVE.value)
        lCounter += 1
        # previous_distance = distance


    moveMotor(Motors.LOWER.value, scanningLowerStepSize * maxStepsOfLower, Direction.POSITIVE.value)
    return xResult,yResult

def scan2D_upper():
    global global_distance
    
    uCounter = 0
    
    xResult = []
    yResult = []

    
    while(uCounter != maxStepsOfUpper):
        distance = global_distance
        print("##############scan2D###############")
        print("distance = ",distance)
        print("lCounter = ",uCounter)
        print("######################################")
        if (distance != -1 and distance != None):
            yResult.append(distance)
            xResult.append((uCounter * scanningUpperStepSize))

        else:
            yResult.append(0)
            xResult.append((uCounter * scanningUpperStepSize))

        moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.POSITIVE.value)
        uCounter += 1

    moveMotor(Motors.UPPER.value, scanningUpperStepSize * maxStepsOfUpper, Direction.NEGATIVE.value)
    return xResult,yResult
    
def move_with_keyboard ():
    val = ""
    while val != "e":
        val = input("Enter your value: ") 
        if (val == "d"):
            moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.POSITIVE.value)
        elif (val == "a"):
            moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.NEGATIVE.value)
        elif (val == "s"):
            moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.NEGATIVE.value)
        elif (val == "w"):
            moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.POSITIVE.value)

i=1
j=1

if __name__ == "__main__":
    arduino = set_up()
    n = 2
    fig, ax = plt.subplots(nrows=n, ncols=2)
    
   

    for i in range(n):
        scan2D_lower()
        x = [i for i in range(0, len(readings), 1)]
        #plt.subplot(211)
        ax[i][0].plot(x, distances,marker="o")
        #plt.subplot(212)
        ax[i][1].plot(x, readings,marker="o")
        distances = []
        readings = []
        
        # plt.plot(x, readings)
        # plt.plot(x, distances)
        #plot1 = plt.figure(1)
        ####################
        
        moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.NEGATIVE.value)
    
    moveMotor(Motors.UPPER.value, scanningUpperStepSize*n, Direction.POSITIVE.value)
    
  
    plt.show()   
    #####################3
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.show()
    # setting upp arduino ports
    # context = zmq.Context()
    # socket = context.socket(zmq.PUB)
    # socket.bind("tcp://*:%s" % port)
    # t1 = Thread(target=get_readings_thread,daemon=True)
    # t1.start()
    # t1.join()
    # move_with_keyboard ()
    #2d scanning
    ####################################################3
    # x , y = scan2D_lower()
    # print(x)
    # print(y)
    # plt.plot(x, y)
    # plt.xlabel('x')
    # plt.ylabel('y')
    # plt.show()
    ########################################################
    #3d scanning 
    ##########################################################################################3
    # lowerDirection = 1
    # dist = []
    # uAngel =[]
    # lAngel = []
    # dist,uAngel,lAngel = scanFace(lowerDirection)
    # x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
    # # print(x)
    # # print(y)
    # # print(z)
    # my_sample_x = np.array(x)
    # my_sample_y = np.array(y)
    # my_sample_z = np.array(z)

    # cat_g = ['setosa']
    # sample_cat = [cat_g[np.random.randint(0,1)] for i in range (len(my_sample_z))]

    # df = pd.DataFrame(my_sample_x,columns=['sepal_length'])
    # df['sepal_width'] = my_sample_y
    # df['petal_width'] = my_sample_z
    # df['species'] = sample_cat
    # df.head()
    # fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
    #         color='species',range_x = [-500,500],range_y = [-500,500],range_z=[-500,500])
    # fig.show()

##################################################################################3333333333




    # moves the sensor in lower direction (XY plane) until the face is found
    
#     # lowerDirection = calibrateLower()
#     lowerDirection = 1
#     dist = []
#     uAngel =[]
#     lAngel = []
#     if(lowerDirection is None):
#         moveMotor(Motors.LOWER.value, maxStepsOfLower,
#                   Direction.POSITIVE.value)
#     else:
#         dist,uAngel,lAngel = scanFace(lowerDirection)
#         # print (dist,uAngel,lAngel)
#         x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
#         # print(x)
#         # print(y)
#         # print(z)

#         my_sample_x = np.array(x)
#         my_sample_y = np.array(y)
#         my_sample_z = np.array(z)
        
#         print ("size of the my_sample_x before drawing :: ",len(my_sample_x))
#         print ("size of the my_sample_y before drawing :: ",len(my_sample_y))
#         print ("size of the my_sample_z before drawing :: ",len(my_sample_z))
# #         fig = plt.figure()
# #         ax = fig.add_subplot(111,projection="3d")
# #         ax.scatter (my_sample_x,my_sample_y, my_sample_z, s=5, c="r", marker = 'o')
# #         ax.set_xlabel("X")
# #         ax.set_ylabel("Y")
# #         ax.set_zlabel("Z")
# # #         ax.set_xlim(-100, 100)
# # #         ax.set_ylim(-100, 100)
# # #         ax.set_zlim(-100, 100)
# #         plt.show()
#         cat_g = ['setosa']
#         sample_cat = [cat_g[np.random.randint(0,1)] for i in range (len(my_sample_z))]

#         df = pd.DataFrame(my_sample_x,columns=['sepal_length'])
#         df['sepal_width'] = my_sample_y
#         df['petal_width'] = my_sample_z
#         df['species'] = sample_cat
#         df.head()
#         fig = px.scatter_3d(df, x='sepal_length', y='sepal_width', z='petal_width',
#                 color='species')
#         fig.show()