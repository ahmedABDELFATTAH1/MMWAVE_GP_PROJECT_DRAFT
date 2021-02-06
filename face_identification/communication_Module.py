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

counter_depth_test_function = 0
max_depth = 10
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
    time.sleep(0.2)
    arduino.readline()


def scanFace(max_db):
    upperDirection = True
    moveU = True
    moveL = True
    uCounter = 0
    lCounter = Direction.NEGATIVE.value * (maxStepsOfLower/2)
    count = 0
    count_lower_end = 0
    dResult =[]
    uResult = []
    lResult = []
    while(moveL):
        previous_distance = -1
        while(moveU):
            index,distance,db_frame = test_function(False, max_db)
            # distance = error_correction(previous_distance , distance)
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
            if(upperDirection):
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.NEGATIVE.value)
                uCounter += scanningUpperStepSize
                count+=1
            else:
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.POSITIVE.value)
                uCounter -= scanningUpperStepSize
                count+=1
            if count >= maxStepsOfUpper:
                moveU = False
                count = 0
            previous_distance = distance
        moveU = True
        upperDirection = not upperDirection
        index,distance,db_frame = test_function(False, max_db)
        # distance = error_correction(previous_distance , distance)
        if (distance != -1):
            dResult.append(distance)
            uResult.append((uCounter * 0.45*np.pi)/180)
            lResult.append((lCounter * 0.45*np.pi)/180)
        moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.POSITIVE.value)
        lCounter += (scanningLowerStepSize*Direction.POSITIVE.value)
        count_lower_end += 1
        if count_lower_end >= maxStepsOfLower:
            moveL = False
        previous_distance = distance
    return dResult,uResult,lResult

def test_function(calibiration_mode, max_db):
    global readings, global_counter, counter_depth_test_function, max_depth
    filereader = open('radar_readings.txt', 'r')
    print ("counter_depth_test_function = ", counter_depth_test_function)
    lines = filereader.readlines()
    while (len(lines) == 0):
        lines = filereader.readlines()
    line = lines[len(lines)-1]
    filereader.close()
    # print (json.loads(line))
    try :
        frame = json.loads(line)
    except:
        open('radar_readings.txt', 'w').close()
        return test_function(calibiration_mode, max_db)
    # try:
    index, distance, db_frame = radar.detect_peaks(frame, calibiration_mode, max_db)
    # index, distance, db_frame = radar.get_max_magnitude_in_range(frame)
    print("step number = ",global_counter," with db value = ", db_frame, " with a distance = ",distance)
    if (db_frame != None):
        distances.append(distance)
        readings.append(db_frame)
        counter_depth_test_function = 0
        open('radar_readings.txt', 'w').close()
        return index, distance, db_frame
    elif counter_depth_test_function < max_depth:
        # distances.append(0)
        # readings.append(0)
        counter_depth_test_function += 1
        return test_function(calibiration_mode, max_db)
    else:
        distances.append(0)
        readings.append(0)
        counter_depth_test_function = 0
        open('radar_readings.txt', 'w').close()
        return -1, -1, -1
    # except:
    #     # readings.append(0)
    #     # distances.append(0)
    #     if counter_depth_test_function < max_depth:
    #         counter_depth_test_function += 1
    #         test_function()
    #     else:
    #         counter_depth_test_function = 0
    #         open('radar_readings.txt', 'w').close()
    #         return None
def scan2D_lower(calibiration_mode, max_db):
    global global_distance, global_counter
    
    lCounter = 0
    xResult = []
    yResult = []
    previous_distance = -1
    while(lCounter != maxStepsOfLower): 
        global_counter = lCounter
        test_function(calibiration_mode, max_db)
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

        
        moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.POSITIVE.value)
        lCounter += 1
        # previous_distance = distance


    moveMotor(Motors.LOWER.value, scanningLowerStepSize * maxStepsOfLower, Direction.NEGATIVE.value)
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
def distance_drawing():
    readings = [-94, -94, -98, -100, -103, -102, -103, -102, -103, -99, -103, -99, -99, -100, -100, -100, -95, -100, -97, -97, -99, -99, -93, -93, -93, -97, -93, -89, -87, -85, -86, -85, -84, -91, -97, -99, -96, -96, -93, -93, -96, -96, -89, -83, -75, -74, -77, -84, -93, -96, -87, -83, -81, -80, -80, -81, -86, -87, -75, -64, -57, -50, -45, -43, -42, -40, -39, -38, -36, -34, -31, -28, -25, -22, -21, -19, -19, -18, -16, -11, -7, 0, 4, 6, 8, 9, 9, 8, 5, 2, -8, -11, -24, -29, -29, -20, -19, -13, -11, -12, -13, -16, -19, -20, -21, -20, -21, -24, -27, -33, -40, -44, -47, -47, -46, -47, -48, -53, -67, -72, -72, -69, -68, -68, -70, -74, -87, -81, -66, -75, -72, -70, -60, -79, -77, -85, -85, -90, -88, -91, -96, -96, -92, -91, -91, -90, -91, -90, -93, -91]
    readings_np = np.array(readings)
    distance = [792, 788, 788, 796, 756, 608, 764, 796, 604, 796, 772, 768, 776, 756, 768, 776, 784, 776, 780, 780, 784, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 504, 512, 520, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 772, 780, 792, 796, 796, 796, 796, 796, 764, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 792, 792, 792, 784, 788, 788, 788, 784, 780, 784, 780, 784, 780, 780, 780, 780, 780, 784, 780, 780, 784, 784, 784, 792, 784, 788, 788, 784, 784, 784, 788, 784, 784, 784, 788, 792, 792, 788, 792, 792, 792, 792, 796, 796, 796, 796, 796, 796, 796, 768, 768, 780, 784, 784, 780, 780, 776, 796, 796, 792, 788, 796, 792, 788, 788, 776, 776, 796, 796, 796, 796, 768, 776, 768, 768, 776, 780, 784, 780, 780]
    counter = 0
    flag = 1
    for i in range (len(distance)):  
        angel = ((counter * 0.45*np.pi)/180)
        distance[i] = distance[i] * np.cos(angel)
        if (readings_np[i]/np.max(readings_np)) == 1:
            flag = -1
        counter += flag

    x = [num for num in range(0, len(distance), 1)]
    plt.xlabel('Step')
    plt.ylabel('Distance in (mm)')
    plt.plot(x, distance,marker="o")
    plt.grid(True)
    plt.suptitle('Distance', fontsize=25)
    plt.show()
def beam_pattern ():
    readings_ex1 = [-30, -32, -34, -33, -25, -21, -18, -17, -16, -15, -12, -7, -7, -8, -14, -18, -13, -9, -9, -18, -24, -27, -9, -10, -16, -16, -5, 0, 2, 3, 10, 15, 18, 21, 19, 17, 22, 30, 38, 45, 48, 49, 55, 58, 60, 63, 64, 63, 62, 60, 57, 52, 45, 41, 38, 35, 26, 16, 6, 13, 15, 15, 10, 4, 3, -8, -14, -17, -10, -8, -8, -14, -15, -20, -19, -23, -28, -23, -17, -7, -4, -5, -16, -19, -25, -33, -36, -46, -38, -31, -33, -35, -33, -24, -20, -19, -28, -37, -41, -43]
    readings_ex2 = [-38, -38, -34, -28, -23, -20, -17, -17, -20, -22, -24, -20, -8, -5, -4, 0, 0, 2, 5, 5, 5, 3, 4, 12, 18, 21, 22, 23, 25, 29, 33, 36, 38, 39, 41, 43, 43, 44, 45, 47, 48, 49, 50, 50, 51, 52, 53, 55, 55, 56, 56, 57, 58, 58, 58, 57, 56, 56, 55, 55, 56, 56, 56, 55, 53, 51, 49, 44, 41, 37, 33, 32, 31, 31, 30, 30, 29, 29, 27, 26, 21, 17, 11, 7, 1, -3, -6, -8, -9, -12, -15, -19, -17, -17, -17, -20, -26, -39, -48, -49]
    readings_ex1_np = np.array(readings_ex1)
    readings_ex2_np = np.array(readings_ex2)
    # max_1 = np.argmax(readings_ex1_np)
    # max_2 = np.argmax(readings_ex2_np)
    readings_ex1_np -= np.max(readings_ex1_np)#readings_ex1_np[max_1]
    readings_ex2_np -= np.max(readings_ex2_np)#readings_ex2_np[max_2]
    readings_ex1 = list(readings_ex1_np)
    readings_ex2 = list(readings_ex2_np)
    x = [num for num in range(0, len(readings_ex1), 1)]
    x_2 = [num for num in range(0, len(readings_ex2), 1)]
    plt.xlabel('Angel in (degree)')
    plt.ylabel('Magnitude in (dB)')
    plt.plot(x, readings_ex1,marker="o")
    plt.plot(x_2, readings_ex2,marker="o")
    plt.legend(["2 spacers", "1 spacer"])
    plt.grid(True)
    plt.suptitle('Beam Pattern', fontsize=25)
    plt.show()
def calibiration_seen ():
    global readings, distances
    moveMotor(Motors.LOWER.value, (maxStepsOfLower/2), Direction.NEGATIVE.value)
    scan2D_lower(True,0)
    moveMotor(Motors.LOWER.value, (maxStepsOfLower/2), Direction.POSITIVE.value)
    readings_np = np.array(readings)
    max_db = np.max(readings_np)
    readings = []
    distances = []
    return max_db
i=1
j=1
# if __name__ == "__main__":
#     arduino = set_up()
#     # max_db = calibiration_seen ()
#     # print ("MAX_dB = ",max_db)
#     exp_number=6
#     file = open("Experements.txt", "a")
#     n = 2
#     fig, ax = plt.subplots(nrows=n, ncols=2)
#     if (n == 1):
#         # scan2D_lower(True,0)
#         scan2D_lower(False,max_db)
#         x = [num*scanningLowerStepSize*stepAngle for num in range(0, len(readings), 1)]
#         x_2 = [num*scanningLowerStepSize*stepAngle for num in range(0, len(distances), 1)]
#         plt.subplot(211)
#         plt.plot(x, readings,marker="o")
#         plt.xlabel('Angel in (degree)')
#         plt.ylabel('Magnitude in (dB)')
#         plt.grid(True)
#         plt.subplot(212)
#         plt.plot(x_2, distances,marker="o")
#         plt.xlabel('Angel in (degree)')
#         plt.ylabel('distance in (mm)')
#         plt.grid(True)
#         plt.suptitle('Beam Pattern', fontsize=25)
#     else:
#         for i in range(n):
#             # scan2D_lower(False, max_db)
#             scan2D_lower(True,0)
#             x = [num*scanningLowerStepSize*stepAngle for num in range(0, len(readings), 1)]
#             x_2 = [num*scanningLowerStepSize*stepAngle for num in range(0, len(distances), 1)]
#             ax[i][0].set_xlabel('Angel in (degree)')
#             ax[i][0].set_ylabel('Distance in (mm)')
#             ax[i][0].grid(True)
#             ax[i][0].plot(x_2, distances,marker="o")
#             ax[i][1].set_xlabel('Angel in (degree)')
#             ax[i][1].set_ylabel('Magnitude in (dB)')
#             ax[i][1].grid(True)
#             ax[i][1].plot(x, readings,marker="o")
#             file.write("Experement number ::"+str(i)+"\n") 
#             file.write(str(readings)+"\n") 
#             file.write(str(distances)+"\n")
#             distances = []
#             readings = []
#             #plot1 = plt.figure(1)
#             # moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.NEGATIVE.value)   
#     # moveMotor(Motors.UPPER.value, scanningUpperStepSize*n, Direction.POSITIVE.value)
#     # fig.suptitle('Exp', fontsize=16)
#     plt.show()  
#     file.write("########################################################################################\n")  
#     file.close()

if __name__ == "__main__":
    i = 1
    arduino = set_up()
    file = open("Experements_3D.txt", "a")
    max_db = calibiration_seen ()
    print ("MAX_dB = ",max_db)
    moveMotor(Motors.LOWER.value, (maxStepsOfLower/2), Direction.NEGATIVE.value)
    dist,uAngel,lAngel = scanFace(max_db)
    moveMotor(Motors.LOWER.value, (maxStepsOfLower/2), Direction.POSITIVE.value)
    x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
    my_sample_x = np.array(x)
    my_sample_y = np.array(y)
    my_sample_z = np.array(z)
    file.write("Experement number ::"+str(i)+"\n") 
    file.write(str(my_sample_x)+"\n") 
    file.write(str(my_sample_y)+"\n")
    file.write(str(my_sample_z)+"\n")
    file.write("########################################################################################\n")  
    file.close()
    cat_g = ['setosa']
    sample_cat = [cat_g[np.random.randint(0,1)] for i in range (len(my_sample_z))]
    df = pd.DataFrame(my_sample_x,columns=['X'])
    df['Y'] = my_sample_y
    df['Z'] = my_sample_z
    df['Color'] = sample_cat
    df.head()
    fig = px.scatter_3d(df, x='X', y='Y', z='Z',
            color='Color')
    fig.show()
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