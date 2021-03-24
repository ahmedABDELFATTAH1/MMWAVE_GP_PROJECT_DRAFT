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
 
counter_depth_get_dist_mag = 0

global_counter = 0

readings = []
distances = []


configuration_file = open('configuration.json',)
configuration_json = json.load(configuration_file)
arduino_port = configuration_json["ARDUINO_PORT"] #arduino port number
port = configuration_json["PORT"] #radar port number
max_depth = configuration_json["MAX_DEPTH"] #max depth of tries to get readings



motors_delay  = configuration_json["MOTORS_DELAY"] #Delay of each read
stepAngle = configuration_json["STEP_ANGLE"] 

scanningLowerStepSize = configuration_json["LOWER_STEP_SIZE"] #the number of movements the lower motor will move at each step
scanningUpperStepSize = configuration_json["UPPER_STEP_SIZE"] #the number of movements the upper motor will move at each step

maxAngleUpper = configuration_json["MAX_ANGLE_UPPER"]  #the angle that the upper motor will move during the scan
maxStepsOfUpper = maxAngleUpper/(stepAngle*scanningUpperStepSize) #the number of steps that the upper motor will move during the scan

maxAngleLower = configuration_json["MAX_ANGLE_LOWER"] #the angle that the lower motor will move during the scan
maxStepsOfLower = maxAngleLower/(stepAngle*scanningLowerStepSize) #the number of steps that the lower motor will move during the scan

state_min = configuration_json["STATE_MIN"]  
state_max = configuration_json["STATE_MAX"]
state_counter = state_min


class Motors(Enum):
    LOWER = 'l'
    UPPER = 'u'


class Direction(Enum):
    POSITIVE = 1
    NEGATIVE = -1


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
    """
    setting up the arduino baud rate and port
    """
    arduino = serial.Serial()
    arduino.baudrate = 9600
    arduino.port = arduino_port
    arduino.open()
    print(arduino.is_open)
    print(arduino.readline())
    return arduino




def moveMotor(motor: Motors, stepSize, direction: Direction):
    """
    Moves motor in arduino
    input : motor --> can be either 'l' for lower motor 
                  or  'u' for upper motor
        stepSize --> (integer) number of steps that the motor will move (step = 0.45 angle)
        direction -->  either -1 or 1 
    """
    txt = motor + str(direction * stepSize) + "$"
    arduino.write(bytes(txt, 'utf-8'))
    time.sleep(motors_delay)
    arduino.readline()


def scanFace(max_db):
    """
    3d scanning for the object in front of the radar , radar should be directed to the lower left of the object

    input : max_db --> used as an estimate to the average db of the object , to eliminate noise
    output : dResult[] --> distance between object and the motor of each reading 
            uResult[] --> angle of the upper motor of each reading
            lResult[] --> angle of the lower motor of each reading
    """
    upperDirection = True
    moveU = True
    moveL = True
    uCounter = Direction.NEGATIVE.value * ((maxStepsOfUpper*scanningUpperStepSize)/2)
    lCounter = Direction.NEGATIVE.value * ((maxStepsOfLower*scanningLowerStepSize)/2)
    moveMotor(Motors.LOWER.value, ((maxStepsOfLower*scanningLowerStepSize)/2), Direction.NEGATIVE.value)
    moveMotor(Motors.UPPER.value, ((maxStepsOfUpper*scanningUpperStepSize)/2), Direction.POSITIVE.value)
    count = 0
    count_lower_end = 0
    dResult =[]
    uResult = []
    lResult = []
    while(moveL): 
        previous_distance = -1
        while(moveU):
            index,distance,db_frame = get_dist_mag(False, max_db)
            # distance = error_correction(previous_distance , distance)
            print("######################################")
            print("upperMoter.distance = ",distance)
            print("upperMoter.count = ",count)
            print("upperMoter.uCounter = ",uCounter)
            print("upperMoter.lCounter = ",lCounter)
            print("######################################")
            if (distance != -1):  #if there is an object detected
                dResult.append(distance)    #distance between radar and object
                uResult.append((uCounter * 0.45*np.pi)/180) # getting upper angle in radian
                lResult.append((lCounter * 0.45*np.pi)/180) # getting lower angle in radian
            if(upperDirection): # if my direction is upper i will move up 1 step
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.NEGATIVE.value) 
                uCounter += scanningUpperStepSize
                count+=1
            else: # else I will move down 1 step
                moveMotor(Motors.UPPER.value, scanningUpperStepSize,
                          Direction.POSITIVE.value)
                uCounter -= scanningUpperStepSize
                count+=1
            if count >= maxStepsOfUpper: #We have finished scanning 1 column , time to move to the next column
                moveU = False #to exit loop
                count = 0
            previous_distance = distance
        moveU = True  #to enter the next column
        upperDirection = not upperDirection #toggle direction of upper motor
        index,distance,db_frame = get_dist_mag(False, max_db)
        # distance = error_correction(previous_distance , distance)
        if (distance != -1):
            dResult.append(distance)
            uResult.append((uCounter * 0.45*np.pi)/180)
            lResult.append((lCounter * 0.45*np.pi)/180)
        moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.POSITIVE.value) #moving lower motor 1 step 
        lCounter += (scanningLowerStepSize*Direction.POSITIVE.value)
        count_lower_end += 1
        if count_lower_end > maxStepsOfLower: #quitting scan if we have reached maximum steps of lower motor
            moveL = False 
        previous_distance = distance
    moveMotor(Motors.LOWER.value, ((maxStepsOfLower*scanningLowerStepSize)/2), Direction.NEGATIVE.value)
    if (upperDirection):
        moveMotor(Motors.UPPER.value, ((maxStepsOfUpper*scanningUpperStepSize)/2), Direction.NEGATIVE.value)
    else:
        moveMotor(Motors.UPPER.value, ((maxStepsOfUpper*scanningUpperStepSize)/2), Direction.POSITIVE.value)
    return dResult,uResult,lResult
    
def get_reading_message(): 
    context = zmq.Context()
    consumer_receiver = context.socket(zmq.SUB)
    consumer_receiver.setsockopt_string(zmq.SUBSCRIBE, "")    
    consumer_receiver.connect("tcp://127.0.0.1:5558")
    frame = consumer_receiver.recv_json()
    consumer_receiver.close()    
    print(len(frame["FRAME"]))    
    return frame["FRAME"]

    
def get_dist_mag(calibiration_mode, max_db):
    """
    Processing the last line in "radar_readings.txt" and returning the peak (db) of the reading using cfar (index of the peak , distance value , db)
    if there is no line it will try again until there is a reading with max number of tries = max_depth

    inputs : calibration_mode --> true  --> used when Radar is used in calibration mode
                              --> false --> used when Radar is used in Scanning mode
             max_db  --> used when calibration mode is false , to eliminate noise

    output : (peak_index , distance_value , db_value)
    """
    global readings, global_counter, counter_depth_get_dist_mag, max_depth
    frame = get_reading_message()
    index, distance, db_frame = radar.detect_peaks(frame, calibiration_mode, max_db)
    # index, distance, db_frame = radar.get_max_magnitude_in_range(frame)
    print("step number = ",global_counter," with db value = ", db_frame, " with a distance = ",distance)
    if (db_frame != None):  #if a frame is detected
        distances.append(distance) #save distance
        readings.append(db_frame) #save db
        counter_depth_get_dist_mag = 0
        #open('radar_readings.txt', 'w').close()
        return index, distance, db_frame
    elif counter_depth_get_dist_mag < max_depth:        
        counter_depth_get_dist_mag += 1
        return get_dist_mag(calibiration_mode, max_db)
    else:  #if I have tried max_depth times and got no readings I will return -1 which indecates that I have no reading
        distances.append(0)
        readings.append(0)
        counter_depth_get_dist_mag = 0
        #open('radar_readings.txt', 'w').close()
        return -1, -1, -1
    
    
def scan2D_lower(calibiration_mode, max_db):
    """
    Scanning with lower motor 
    inputs : calibration_mode --> true  --> used when Radar is used in calibration mode
                              --> false --> used when Radar is used in Scanning mode
             max_db  --> used when calibration mode is false , to eliminate noise

    output : x [] --> x axis points 
            y [] --> y axis points
    """ 
    global global_distance, global_counter
    
    lCounter = 0
    xResult = []
    yResult = []
    previous_distance = -1
    while(lCounter != maxStepsOfLower): 
        global_counter = lCounter      
        get_dist_mag(calibiration_mode, max_db) #getting the reading
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
        moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.POSITIVE.value) #moving 1 step
        lCounter += 1
        # previous_distance = distance


    moveMotor(Motors.LOWER.value, scanningLowerStepSize * maxStepsOfLower, Direction.NEGATIVE.value) #returning to the original point
    return xResult,yResult


def move_with_keyboard ():
    """
    moves the motor with keyboard input
    """
    val = ""
    while val != "e":
        val = input("Enter your value: ") 
        if (val == "d"):
            moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.POSITIVE.value)
        elif (val == "a"):
            moveMotor(Motors.LOWER.value, scanningLowerStepSize, Direction.NEGATIVE.value)
        elif (val == "w"):
            moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.NEGATIVE.value)
        elif (val == "s"):
            moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.POSITIVE.value)



def calibrate_scene():
    """
    getting the max db in the scence by doing a 2d scan

    output : maximum db in the scene
    """
    global readings, distances  # list of db(y) , distance(x)
    moveMotor(Motors.LOWER.value, ((maxStepsOfLower*scanningLowerStepSize)/2), Direction.NEGATIVE.value) #move from center of the object to the beginning of the object
    scan2D_lower(True,0) # scan 2d 
    moveMotor(Motors.LOWER.value, ((maxStepsOfLower*scanningLowerStepSize)/2), Direction.POSITIVE.value) #move back to the center
    readings_np = np.array(readings) 
    max_db = np.max(readings_np) # getting max db
    readings = []
    distances = []
    return max_db


def save_3d_experement(x,y,z,name):
    """
    saves the x , y , z points of an experiment in an external file

    input: x --> x axis points 
           y --> y axis points
           z --> z axis points
           name --> name of the experiment

    """
    #saves x points in "3D_experements" folder with name of "experiment_name+_x.txt"
    file = open("3D_Experements/"+name+"_x.txt", "a")
    np.savetxt(file, x)
    file.close()

    #saves y points in "3D_experements" folder with name of "experiment_name+_y.txt"
    file = open("3D_Experements/"+name+"_y.txt", "a")
    np.savetxt(file, y)
    file.close()

    #saves z points in "3D_experements" folder with name of "experiment_name+_z.txt"
    file = open("3D_Experements/"+name+"_z.txt", "a")
    np.savetxt(file, z)
    file.close()



def save_dist_mag_experenemt(mag,dist,name):
    """
    saves the dbs and step number of an experiment in an external file

    input: mag --> dbs values 
           dist --> step number
           name --> name of the experiment

    """
    #saves dbs in "DM_Experements" folder with name of "experiment_name+_mag.txt"
    file = open("DM_Experements/"+name+"_mag.txt", "a")
    np.savetxt(file, mag)
    file.close()

    #saves step numbers in "3D_Experements" folder with name of "experiment_name+_dist.txt"
    file = open("3D_Experements/"+name+"_dist.txt", "a")
    np.savetxt(file, dist)
    file.close()


def _3D_mapping(exp_name):
    """
    Calibrates the system to get max db ,
    then 3d scans the scene infront of the radar ,
    then saves the points in an external file , and draws the experiment 

    input : exp_name --> the name of the experiment , will be used as we save readings in an external file with the same name
    """
    ##gets the maximum peak of db in the scene to estimate average value of db to eliminate noise
    #radar starts at the middle of the object , and after finishing returns back to the original point (middle of the object)
    max_db = calibrate_scene()  
    print ("MAX_dB = ",max_db)

    ##moving the radar to the left (or right) with number of steps of scanning / 2
    #then make a 3d scan
    #then return back to the center of the object
    dist,uAngel,lAngel = scanFace(max_db)

    ## getting the x , y , z axis of the points read by the radar
    x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
    print("cos ")
    my_sample_x = np.array(x)
    my_sample_y = np.array(y)
    my_sample_z = np.array(z)

    ##saving the x , y ,z points  in an external file
    #save_3d_experement(my_sample_x,my_sample_y,my_sample_z,exp_name)

    save_3d_experement(np.array(dist),np.array(uAngel),np.array(lAngel),exp_name)



 

def _mag_dist_mapping(exp_name,scaning_number = 2 ,increase_upper_angel = False):
    """
    calibrates the scene , then scans 2d using lower motor , then plots changes in db at each step
    input: exp_name --> name of the experiment 
             scanning_number --> number of times to repeat the same experiment
             increase_upper_angel --> true --> move the upper motor 1 step each time I repeat experiment
                                      false --> don`t move upper motor each time I repeat experiment
    """
    max_db = calibrate_scene ()
    print ("MAX_dB = ",max_db)

    fig, ax = plt.subplots(nrows=scaning_number, ncols=2)
    
    if (scaning_number == 1):
        # scan2D_lower(True,0)
        scan2D_lower(False,max_db)
        x = [num*scanningLowerStepSize*stepAngle for num in range(0, len(readings), 1)]
        x_2 = [num*scanningLowerStepSize*stepAngle for num in range(0, len(distances), 1)]
        plt.subplot(211)
        plt.plot(x, readings,marker="o")
        plt.xlabel('Angle in (degree)')
        plt.ylabel('Magnitude in (dB)')
        plt.grid(True)
        plt.subplot(212)
        plt.plot(x_2, distances,marker="o")
        plt.xlabel('Angle in (degree)')
        plt.ylabel('distance in (mm)')
        plt.grid(True)
        plt.suptitle('Beam Pattern', fontsize=25)
    else:
        for i in range(scaning_number):
            # scan2D_lower(False, max_db)
            scan2D_lower(True,0)
            x = [num*scanningLowerStepSize*stepAngle for num in range(0, len(readings), 1)]
            x_2 = [num*scanningLowerStepSize*stepAngle for num in range(0, len(distances), 1)]
            ax[i][0].set_xlabel('Angle in (degree)')
            ax[i][0].set_ylabel('Distance in (mm)')
            ax[i][0].grid(True)
            ax[i][0].plot(x_2, distances,marker="o")
            ax[i][1].set_xlabel('Angle in (degree)')
            ax[i][1].set_ylabel('Magnitude in (dB)')
            ax[i][1].grid(True)
            ax[i][1].plot(x, readings,marker="o")
            save_dist_mag_experenemt(readings,distances,exp_name+"_"+str(i))
            distances = []
            readings = []

            if increase_upper_angel:
                moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.NEGATIVE.value)

    if increase_upper_angel == True:   
        moveMotor(Motors.UPPER.value, scanningUpperStepSize*scaning_number, Direction.POSITIVE.value)
    
    plt.show()  


def Scan3d(file_name):    
    _3D_mapping(file_name)

radar = Radar()
arduino = set_up()

if __name__ == "__main__":

    # radar = Radar()
    # arduino = set_up()
    # radar.setup_radar()
    # radar.setup_radar_system_configuration()
    # radar.setup_radar_pll_configuration()
    # radar.setup_radar_baseband_configuration()
    ##########################
    # context = zmq.Context()
    # socket = context.socket(zmq.PUB)
    # socket.bind("tcp://*:%s" % port)
    # t1 = Thread(target=get_readings_thread,daemon=True)
    # t1.start()
    # t1.join()

    # move_with_keyboard ()
    file_name = input("enter experment name")
    _3D_mapping(file_name)
    #_mag_dist_mapping("corner")






####################################### unwanted_for_now #######################################
# """
# if face was found return the direction of the lower motor 
# else return none
# """
# def calibrateLower():    
#     detect = False
#     count = 0
#     # looping until face is found or rotated 90 degrees to the right
#     while(count < calibrateLowerTotalStepsCount):
#         moveMotor(Motors.LOWER.value, calibrateLowerStepSize,
#                   Direction.POSITIVE.value)
#         count += 1
#         result = radar.get_median_distance(1) 
#         if result != -1:
#             detect = True
                 
#         if(detect):
#             return Direction.POSITIVE.value  # return that a face is found when rotating right
#     moveMotor(Motors.LOWER.value, calibrateLowerStepSize *
#               calibrateLowerTotalStepsCount, Direction.NEGATIVE.value)
#     count = 0
#     # looping until face is found or rotated 90 degrees to the left
#     while(not detect and count > -1 * calibrateLowerTotalStepsCount):
#         moveMotor(Motors.LOWER.value, calibrateLowerStepSize,
#                   Direction.NEGATIVE.value)
#         count -= 1
#         result = radar.get_median_distance(1) 
#         if result != -1:
#             detect = True
#         if(detect):
#             return Direction.NEGATIVE.value  # return that a face is found when rotating left
#     return None


# def scan2D_upper():
#     global global_distance
    
#     uCounter = 0
    
#     xResult = []
#     yResult = []

    
#     while(uCounter < maxStepsOfUpper):
#         distance = global_distance
#         print("##############scan2D###############")
#         print("distance = ",distance)
#         print("lCounter = ",uCounter)
#         print("######################################")
#         if (distance != -1 and distance != None):
#             yResult.append(distance)
#             xResult.append((uCounter * scanningUpperStepSize))

#         else:
#             yResult.append(0)
#             xResult.append((uCounter * scanningUpperStepSize))

#         moveMotor(Motors.UPPER.value, scanningUpperStepSize, Direction.POSITIVE.value)
#         uCounter += 1

#     moveMotor(Motors.UPPER.value, scanningUpperStepSize * maxStepsOfUpper, Direction.NEGATIVE.value)
#     return xResult,yResult


# def distance_drawing():
#     readings = [-94, -94, -98, -100, -103, -102, -103, -102, -103, -99, -103, -99, -99, -100, -100, -100, -95, -100, -97, -97, -99, -99, -93, -93, -93, -97, -93, -89, -87, -85, -86, -85, -84, -91, -97, -99, -96, -96, -93, -93, -96, -96, -89, -83, -75, -74, -77, -84, -93, -96, -87, -83, -81, -80, -80, -81, -86, -87, -75, -64, -57, -50, -45, -43, -42, -40, -39, -38, -36, -34, -31, -28, -25, -22, -21, -19, -19, -18, -16, -11, -7, 0, 4, 6, 8, 9, 9, 8, 5, 2, -8, -11, -24, -29, -29, -20, -19, -13, -11, -12, -13, -16, -19, -20, -21, -20, -21, -24, -27, -33, -40, -44, -47, -47, -46, -47, -48, -53, -67, -72, -72, -69, -68, -68, -70, -74, -87, -81, -66, -75, -72, -70, -60, -79, -77, -85, -85, -90, -88, -91, -96, -96, -92, -91, -91, -90, -91, -90, -93, -91]
#     readings_np = np.array(readings)
#     distance = [792, 788, 788, 796, 756, 608, 764, 796, 604, 796, 772, 768, 776, 756, 768, 776, 784, 776, 780, 780, 784, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 504, 512, 520, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 772, 780, 792, 796, 796, 796, 796, 796, 764, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 796, 792, 792, 792, 784, 788, 788, 788, 784, 780, 784, 780, 784, 780, 780, 780, 780, 780, 784, 780, 780, 784, 784, 784, 792, 784, 788, 788, 784, 784, 784, 788, 784, 784, 784, 788, 792, 792, 788, 792, 792, 792, 792, 796, 796, 796, 796, 796, 796, 796, 768, 768, 780, 784, 784, 780, 780, 776, 796, 796, 792, 788, 796, 792, 788, 788, 776, 776, 796, 796, 796, 796, 768, 776, 768, 768, 776, 780, 784, 780, 780]
#     counter = 0
#     flag = 1
#     for i in range (len(distance)):  
#         angel = ((counter * 0.45*np.pi)/180)
#         distance[i] = distance[i] * np.cos(angel)
#         if (readings_np[i]/np.max(readings_np)) == 1:
#             flag = -1
#         counter += flag

#     x = [num for num in range(0, len(distance), 1)]
#     plt.xlabel('Step')
#     plt.ylabel('Distance in (mm)')
#     plt.plot(x, distance,marker="o")
#     plt.grid(True)
#     plt.suptitle('Distance', fontsize=25)
#     plt.show()

# def beam_pattern ():
#     readings_ex1 = [-30, -32, -34, -33, -25, -21, -18, -17, -16, -15, -12, -7, -7, -8, -14, -18, -13, -9, -9, -18, -24, -27, -9, -10, -16, -16, -5, 0, 2, 3, 10, 15, 18, 21, 19, 17, 22, 30, 38, 45, 48, 49, 55, 58, 60, 63, 64, 63, 62, 60, 57, 52, 45, 41, 38, 35, 26, 16, 6, 13, 15, 15, 10, 4, 3, -8, -14, -17, -10, -8, -8, -14, -15, -20, -19, -23, -28, -23, -17, -7, -4, -5, -16, -19, -25, -33, -36, -46, -38, -31, -33, -35, -33, -24, -20, -19, -28, -37, -41, -43]
#     readings_ex2 = [-38, -38, -34, -28, -23, -20, -17, -17, -20, -22, -24, -20, -8, -5, -4, 0, 0, 2, 5, 5, 5, 3, 4, 12, 18, 21, 22, 23, 25, 29, 33, 36, 38, 39, 41, 43, 43, 44, 45, 47, 48, 49, 50, 50, 51, 52, 53, 55, 55, 56, 56, 57, 58, 58, 58, 57, 56, 56, 55, 55, 56, 56, 56, 55, 53, 51, 49, 44, 41, 37, 33, 32, 31, 31, 30, 30, 29, 29, 27, 26, 21, 17, 11, 7, 1, -3, -6, -8, -9, -12, -15, -19, -17, -17, -17, -20, -26, -39, -48, -49]
#     readings_ex1_np = np.array(readings_ex1)
#     readings_ex2_np = np.array(readings_ex2)
#     # max_1 = np.argmax(readings_ex1_np)
#     # max_2 = np.argmax(readings_ex2_np)
#     readings_ex1_np -= np.max(readings_ex1_np)#readings_ex1_np[max_1]
#     readings_ex2_np -= np.max(readings_ex2_np)#readings_ex2_np[max_2]
#     readings_ex1 = list(readings_ex1_np)
#     readings_ex2 = list(readings_ex2_np)
#     x = [num for num in range(0, len(readings_ex1), 1)]
#     x_2 = [num for num in range(0, len(readings_ex2), 1)]
#     plt.xlabel('Angel in (degree)')
#     plt.ylabel('Magnitude in (dB)')
#     plt.plot(x, readings_ex1,marker="o")
#     plt.plot(x_2, readings_ex2,marker="o")
#     plt.legend(["2 spacers", "1 spacer"])
#     plt.grid(True)
#     plt.suptitle('Beam Pattern', fontsize=25)
#     plt.show()
#####################################################################################################################