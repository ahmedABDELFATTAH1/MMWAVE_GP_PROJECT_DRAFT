##################################################################################################################
########################################### Imports ##############################################################
##################################################################################################################
import json
import matplotlib.pyplot as plt
import json
import numpy as np
import random
from arduino_configuration import *
from radar_configuration import Radar
##########################################
radar = Radar()
arduino = Arduino()
##########################################
##################################################################################################################
########################################### Plot Histogram Parameters ############################################
##################################################################################################################
min_dist = 0
max_dist=800
bin_size = 4
##################################################################################################################
counter_depth_get_dist_mag = 0
global_counter = 0
n_samples = 5
n_readings = 5
readings = []
distances = []
collect_data = False
positive_scane = True
configuration_file = open('configuration.json',)
configuration_json = json.load(configuration_file)
arduino_port = configuration_json["ARDUINO_PORT"] #arduino port number
max_depth = configuration_json["MAX_DEPTH"] #max depth of tries to get readings
##################################################################################################################
########################################### Motor Parameters #####################################################
##################################################################################################################
motors_delay  = configuration_json["MOTORS_DELAY"] #Delay of each read
step_angle = configuration_json["STEP_ANGLE"] 
scanning_lower_step_size = configuration_json["LOWER_STEP_SIZE"] #the number of movements the lower motor will move at each step
scanning_upper_step_size = configuration_json["UPPER_STEP_SIZE"] #the number of movements the upper motor will move at each step
max_angle_upper = configuration_json["MAX_ANGLE_UPPER"]  #the angle that the upper motor will move during the scan
max_steps_of_upper = max_angle_upper/(step_angle*scanning_upper_step_size) #the number of steps that the upper motor will move during the scan
max_angle_lower = configuration_json["MAX_ANGLE_LOWER"] #the angle that the lower motor will move during the scan
max_steps_of_lower = max_angle_lower/(step_angle*scanning_lower_step_size) #the number of steps that the lower motor will move during the scan
##################################################################################################################
def scan_3D_object(max_db):
    """
    3d scanning for the object in front of the radar , radar should be directed to the lower left of the object

    input : max_db --> used as an estimate to the average db of the object , to eliminate noise
    output : d_result[] --> distance between object and the motor of each reading 
            u_result[] --> angle of the upper motor of each reading
            l_result[] --> angle of the lower motor of each reading
    """
    global n_samples,n_readings,collect_data, radar, arduino
    upper_direction = True
    move_u = True
    move_l = True
    u_counter = Direction.NEGATIVE.value * ((max_steps_of_upper*scanning_upper_step_size)/2)
    l_counter = Direction.NEGATIVE.value * ((max_steps_of_lower*scanning_lower_step_size)/2)
    arduino.move_motor(Motors.LOWER.value, ((max_steps_of_lower*scanning_lower_step_size)/2), Direction.NEGATIVE.value)
    arduino.move_motor(Motors.UPPER.value, ((max_steps_of_upper*scanning_upper_step_size)/2), Direction.POSITIVE.value)
    count = 0
    count_lower_end = 0
    d_result =[]
    u_result = []
    l_result = []
    while(move_l): 
        previous_distance = -1
        while(move_u):
            # for classification 
            if collect_data :
                index,distance,db_frame = radar.collect_n_samples(n_samples,n_readings)
            else: 
                index,distance,db_frame = get_dist_mag(False, max_db)

            # for collecting data from single point 
            
            # distance = error_correction(previous_distance , distance)
            print("######################################")
            print("upperMoter.distance = ",distance)
            print("upperMoter.count = ",count)
            print("upperMoter.u_counter = ",u_counter)
            print("upperMoter.l_counter = ",l_counter)
            print("######################################")
            if (distance != -1):  #if there is an object detected
                d_result.append(distance)    #distance between radar and object
                u_result.append((u_counter * 0.45*np.pi)/180) # getting upper angle in radian
                l_result.append((l_counter * 0.45*np.pi)/180) # getting lower angle in radian
            if(upper_direction): # if my direction is upper i will move up 1 step
                arduino.move_motor(Motors.UPPER.value, scanning_upper_step_size,
                          Direction.NEGATIVE.value) 
                u_counter += scanning_upper_step_size
                count+=1
            else: # else I will move down 1 step
                arduino.move_motor(Motors.UPPER.value, scanning_upper_step_size,
                          Direction.POSITIVE.value)
                u_counter -= scanning_upper_step_size
                count+=1
            if count >= max_steps_of_upper: #We have finished scanning 1 column , time to move to the next column
                move_u = False #to exit loop
                count = 0
            previous_distance = distance
        move_u = True  #to enter the next column
        upper_direction = not upper_direction #toggle direction of upper motor
        if collect_data :
            # for collecting data from single point 
            index,distance,db_frame = radar.collect_n_samples(n_samples,n_readings)
        else: 
             # for classification 
            index,distance,db_frame = get_dist_mag(False, max_db)
        # distance = error_correction(previous_distance , distance)
        if (distance != -1):
            d_result.append(distance)
            u_result.append((u_counter * 0.45*np.pi)/180)
            l_result.append((l_counter * 0.45*np.pi)/180)
        arduino.move_motor(Motors.LOWER.value, scanning_lower_step_size, Direction.POSITIVE.value) #moving lower motor 1 step 
        l_counter += (scanning_lower_step_size*Direction.POSITIVE.value)
        count_lower_end += 1
        if count_lower_end > max_steps_of_lower: #quitting scan if we have reached maximum steps of lower motor
            move_l = False 
        previous_distance = distance
    arduino.move_motor(Motors.LOWER.value, ((max_steps_of_lower*scanning_lower_step_size)/2), Direction.NEGATIVE.value)
    if (upper_direction):
        arduino.move_motor(Motors.UPPER.value, ((max_steps_of_upper*scanning_upper_step_size)/2), Direction.NEGATIVE.value)
    else:
        arduino.move_motor(Motors.UPPER.value, ((max_steps_of_upper*scanning_upper_step_size)/2), Direction.POSITIVE.value)
    return d_result,u_result,l_result
    
def get_dist_mag(calibiration_mode, max_db):
    """
    Processing the last line in "radar_readings.txt" and returning the peak (db) of the reading using cfar (index of the peak , distance value , db)
    if there is no line it will try again until there is a reading with max number of tries = max_depth

    inputs : calibration_mode --> true  --> used when Radar is used in calibration mode
                              --> false --> used when Radar is used in Scanning mode
             max_db  --> used when calibration mode is false , to eliminate noise

    output : (peak_index , distance_value , db_value)
    """
    global readings, global_counter, counter_depth_get_dist_mag, max_depth, radar, arduino
    index, distance, db_frame = radar.access_radar(5)
    print("step number = ",global_counter," with db value = ", db_frame, " with a distance = ",distance)
    if (db_frame != None):  #if a frame is detected
        distances.append(distance) #save distance
        readings.append(db_frame) #save db
        counter_depth_get_dist_mag = 0
        return index, distance, db_frame
    elif counter_depth_get_dist_mag < max_depth:        
        counter_depth_get_dist_mag += 1
        return get_dist_mag(calibiration_mode, max_db) 
    else:  #if I have tried max_depth times and got no readings I will return -1 which indecates that I have no reading
        distances.append(0)
        readings.append(0)
        counter_depth_get_dist_mag = 0
        return -1, -1, -1

def move_with_keyboard ():
    """
    moves the motor with keyboard input
    """
    global arduino
    val = ""
    while val != "e":
        val = input("Enter your value: ") 
        if (val == "d"):
            arduino.move_motor(Motors.LOWER.value, scanning_lower_step_size, Direction.POSITIVE.value)
        elif (val == "a"):
            arduino.move_motor(Motors.LOWER.value, scanning_lower_step_size, Direction.NEGATIVE.value)
        elif (val == "w"):
            arduino.move_motor(Motors.UPPER.value, scanning_upper_step_size, Direction.NEGATIVE.value)
        elif (val == "s"):
            arduino.move_motor(Motors.UPPER.value, scanning_upper_step_size, Direction.POSITIVE.value)

def save_3d_experement(x,y,z,name,folder):
    """
    saves the x , y , z points of an experiment in an external file

    input: x --> x axis points 
           y --> y axis points
           z --> z axis points
           name --> name of the experiment

    """
    #saves x points in "3D_experements" folder with name of "experiment_name+_x.txt"
    file = open(folder+name+"_x.txt", "a")
    np.savetxt(file, x)
    file.close()

    #saves y points in "3D_experements" folder with name of "experiment_name+_y.txt"
    file = open(folder+name+"_y.txt", "a")
    np.savetxt(file, y)
    file.close()

    #saves z points in "3D_experements" folder with name of "experiment_name+_z.txt"
    file = open(folder+name+"_z.txt", "a")
    np.savetxt(file, z)
    file.close()

def _3D_mapping(exp_name, folder):
    """
    Calibrates the system to get max db ,
    then 3d scans the scene infront of the radar ,
    then saves the points in an external file , and draws the experiment 

    input : exp_name --> the name of the experiment , will be used as we save readings in an external file with the same name
    """
    dist,uAngel,lAngel = scan_3D_object(0)
    ## getting the x , y , z axis of the points read by the radar
    x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)
    my_sample_x = np.array(x)
    my_sample_y = np.array(y)
    my_sample_z = np.array(z)
    save_3d_experement(np.array(dist),np.array(uAngel),np.array(lAngel),exp_name, folder)
    return dist,uAngel,lAngel


def _3D_collect_data(exp_name,number_examples,folder):
    dist,uAngel,lAngel = scan_3D_object(0)
    for i in range(number_examples):
        example_distances = []
        for j in range (len(dist)):
            example_distances.append(random.choice(dist[j]))    
        ## getting the x , y , z axis of the points read by the radar
        x , y , z = np.array(example_distances)*np.cos(uAngel)*np.sin(lAngel) , np.array(example_distances)*np.cos(uAngel)*np.cos(lAngel) , np.array(example_distances)*np.sin(uAngel)
        my_sample_x = np.array(x)
        my_sample_y = np.array(y)
        my_sample_z = np.array(z)
        save_3d_experement(np.array(example_distances),np.array(uAngel),np.array(lAngel),exp_name+"_"+str(i),folder)

def plot_hist(y):
    global min_dist,max_dist,bin_size
    n1 = random.randint(0,100)
    n2 = random.randint(0,100)
    my_sample_y = y
    my_sample_y = my_sample_y[~np.isnan(my_sample_y)]
    # Set total number of bins in the histogram
    bins_num = [i for i in range(min_dist,max_dist,bin_size)]#256
    # Get the image histogram
    # plt.figure(n1)
    n = plt.hist(my_sample_y , bins = bins_num, label='Original Histogram') 
    hist = n[0]
    bin_edges = n[1]
    # Calculate centers of bins
    bin_mids = (bin_edges[:-1] + bin_edges[1:]) / 2.
    # Iterate over all thresholds (indices) and get the probabilities w1(t), w2(t)
    weight1 = np.cumsum(hist)
    weight2 = np.cumsum(hist[::-1])[::-1]
    # Get the class means mu0(t)
    mean1 = np.cumsum(hist * bin_mids) / weight1
    # Get the class means mu1(t)
    mean2 = (np.cumsum((hist * bin_mids)[::-1]) / weight2[::-1])[::-1]
    mean1 = np.nan_to_num(mean1)
    mean2 = np.nan_to_num(mean2)
    inter_class_variance = weight1[:-1] * weight2[1:] * (mean1[:-1] - mean2[1:]) ** 2
    # Maximize the inter_class_variance function val
    index_of_max_val = np.argmax(inter_class_variance)
    threshold = bin_mids[:-1][index_of_max_val]
    print("Otsu's algorithm implementation thresholding result: ", threshold)
    plt.title("Original Histogram & Otsu's Threshold") 
    plt.xlabel("Horizontal Distances (mm)")
    plt.ylabel("Bin Value (bin size 4mm)")
    plt.axvline(threshold, color='r', label="Otsu's Threshold")
    plt.legend(loc='upper right')
    # plt.show()
    plt.savefig('assets/UI_folder/original_hist_'+str(n1)+'.png')
    # plt.close()
    # plt.figure(n2)
    plt.clf()
    plt.title("Foreground Histogram & Equalized Foreground Histogram") 
    plt.xlabel("Horizontal Distances (mm)")
    plt.ylabel("Bin Value (bin size 4mm)")
    hist = [ hist[i] if bin_edges[i] < threshold else 0 for i in range(hist.size)]
    my_sample_y = my_sample_y[my_sample_y <= threshold]
    total_value = np.sum(hist)
    hist_prob = hist / total_value
    hist_cumsum = np.cumsum(hist_prob)
    new_hist = hist_cumsum * 800
#     print ("hist_cumsum:: ",hist_cumsum)
    new_hist = np.floor(new_hist).astype(int)
#     print ("new_hist:: ",new_hist)
    new_my_sample_y = np.zeros(len(my_sample_y))
    for idx in range (len(my_sample_y)):
        for i in range(len(bin_edges)):
            if bin_edges[i]> my_sample_y[idx] :
#                 print("my_sample_y",my_sample_y[idx],"bin_edges",bin_edges[i],"i",i,"new_hist" ,new_hist[i-1])
                new_my_sample_y[idx] = new_hist[i-1]
                break
    plt.hist(my_sample_y, bins_num, alpha=0.8, label='Foreground Histogram')
    n = plt.hist(new_my_sample_y, bins_num, alpha=0.8, label='Equalized Foreground Histogram')
    hist_new = n[0]
    bin_edges_new = n[1]
    plt.legend(loc='upper right')
    plt.savefig('assets/UI_folder/modifidied_hist_'+str(n2)+'.png')
    # plt.close()
    plt.clf()
#     pyplot.show()
#     print("oh",hist)
#     print("nh",hist_n)
#     print("oy",bin_edges)
#     print("ny",new_my_sample_y)
    return threshold,hist,bin_edges,hist_new,bin_edges_new,n1,n2

def set_up():
    global radar, arduino
    radar.setup_radar()
    # radar.setup_radar_all_configurations()
    arduino.setup_arduino()

if __name__ == "__main__":
    set_up()
    positive_scane = True if input("is this positive scane ? (y or n, invalide input equal \"negative scane\") \n>>") == 'y' else False
    if positive_scane:
        folder = "3D_Experements/"
        print("positive scaning, saving folder is :: "+folder)
    else:
        folder = "flat_Experements/"
        print("negative scaning, saving folder is :: "+folder)

    file_name = input("enter experment name \n>>")

    collect_data = True if input("please select mode: (1 or 2, invalide input equal \"Scane and detect\") \n 1) Scane and detect \n 2) Collect data \n>>") == '2' else False
    if collect_data :
        print("start collecting data ...")
        _3D_collect_data(file_name,1000,folder)
    else:
        print("start scaning data ...")
        _3D_mapping(file_name, folder)
    
    # radar.setup_radar_system_configuration()
    # radar.setup_radar_pll_configuration()
    # radar.setup_radar_baseband_configuration()
    # move_with_keyboard ()
    # _3D_collect_data(file_name,1000,folder)
    # _mag_dist_mapping(file_name,1,False)






####################################### unwanted_for_now #######################################
# port = configuration_json["PORT"] #radar port number
# context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:%s" % port)
# t1 = Thread(target=get_readings_thread,daemon=True)
# t1.start()
# t1.join()
# """
# if face was found return the direction of the lower motor 
# else return none
# """
# def move_motor(motor: Motors, stepSize, direction: Direction):
#     """
#     Moves motor in arduino
#     input : motor --> can be either 'l' for lower motor 
#                   or  'u' for upper motor
#         stepSize --> (integer) number of steps that the motor will move (step = 0.45 angle)
#         direction -->  either -1 or 1 
#     """
#     txt = motor + str(direction * stepSize) + "$"
#     arduino.write(bytes(txt, 'utf-8'))
#     time.sleep(motors_delay)
#     arduino.readline()
# calibrateLowerStepSize = 10
# calibrateLowerTotalStepsCount = 20
# def calibrateLower():    
#     detect = False
#     count = 0
#     # looping until face is found or rotated 90 degrees to the right
#     while(count < calibrateLowerTotalStepsCount):
#         move_motor(Motors.LOWER.value, calibrateLowerStepSize,
#                   Direction.POSITIVE.value)
#         count += 1
#         result = radar.get_median_distance(1) 
#         if result != -1:
#             detect = True
                 
#         if(detect):
#             return Direction.POSITIVE.value  # return that a face is found when rotating right
#     move_motor(Motors.LOWER.value, calibrateLowerStepSize *
#               calibrateLowerTotalStepsCount, Direction.NEGATIVE.value)
#     count = 0
#     # looping until face is found or rotated 90 degrees to the left
#     while(not detect and count > -1 * calibrateLowerTotalStepsCount):
#         move_motor(Motors.LOWER.value, calibrateLowerStepSize,
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
    
#     u_counter = 0
    
#     xResult = []
#     yResult = []

    
#     while(u_counter < max_steps_of_upper):
#         distance = global_distance
#         print("##############scan2D###############")
#         print("distance = ",distance)
#         print("l_counter = ",u_counter)
#         print("######################################")
#         if (distance != -1 and distance != None):
#             yResult.append(distance)
#             xResult.append((u_counter * scanning_upper_step_size))

#         else:
#             yResult.append(0)
#             xResult.append((u_counter * scanning_upper_step_size))

#         move_motor(Motors.UPPER.value, scanning_upper_step_size, Direction.POSITIVE.value)
#         u_counter += 1

#     move_motor(Motors.UPPER.value, scanning_upper_step_size * max_steps_of_upper, Direction.NEGATIVE.value)
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

# state_min = configuration_json["STATE_MIN"]  
# state_max = configuration_json["STATE_MAX"]
# state_counter = state_min
# def error_correction(previous,current):
#     global state_counter
#     if current != -1:
#         if(state_counter < state_max):
#                 state_counter+=1
        
#         return current

#     else:
#         if state_counter == state_min:
#             return current
#         else:
#             state_counter-=1
#             return previous
# baud_rate = configuration_json["BAUD_RATE"]
# def set_up():
#     """
#     setting up the arduino baud rate and port
#     """
#     arduino = serial.Serial()
#     arduino.baudrate = baud_rate
#     arduino.port = arduino_port
#     arduino.open()
#     print("Arduino is connected :: ",arduino.is_open)
#     print("Arduino state is :: ",arduino.readline())
#     return arduino
# def get_reading_message(): 
#     context = zmq.Context()
#     consumer_receiver = context.socket(zmq.SUB)
#     consumer_receiver.setsockopt_string(zmq.SUBSCRIBE, "")    
#     consumer_receiver.connect("tcp://127.0.0.1:5558")
#     frame = consumer_receiver.recv_json()
#     consumer_receiver.close()    
#     print(len(frame["FRAME"]))    
#     return frame["FRAME"]
#
#def scan2D_lower(calibiration_mode, max_db):
#     """
#     Scanning with lower motor 
#     inputs : calibration_mode --> true  --> used when Radar is used in calibration mode
#                               --> false --> used when Radar is used in Scanning mode
#              max_db  --> used when calibration mode is false , to eliminate noise

#     output : x [] --> x axis points 
#             y [] --> y axis points
#     """ 
#     global global_distance, global_counter, arduino
    
#     l_counter = 0
#     xResult = []
#     yResult = []
#     arduino.move_motor(Motors.LOWER.value, ((max_steps_of_lower*scanning_lower_step_size)/2), Direction.NEGATIVE.value)
#     previous_distance = -1
#     while(l_counter <= max_steps_of_lower): 
#         global_counter = l_counter      
#         get_dist_mag(calibiration_mode, max_db) #getting the reading
#         # distance = global_distance
#         # distance = -1
#         # print("##############scan2D###############")
#         # print("distance = ",distance)
#         # print("l_counter = ",l_counter)
#         # print("######################################")
#         # distance = error_correction(previous_distance,distance)
#         # if (distance != -1 and distance != None):
#         #     yResult.append(distance)
#         #     xResult.append((l_counter * scanning_lower_step_size))
        
#         # else:
#         #     yResult.append(0)
#         #     xResult.append((l_counter * scanning_lower_step_size))        
#         arduino.move_motor(Motors.LOWER.value, scanning_lower_step_size, Direction.POSITIVE.value) #moving 1 step
#         l_counter += 1
#         # previous_distance = distance

#     arduino.move_motor(Motors.LOWER.value, ((max_steps_of_lower*scanning_lower_step_size)/2), Direction.NEGATIVE.value)
#     return xResult,yResult
#
# def calibrate_scene():
#     """
#     getting the max db in the scence by doing a 2d scan

#     output : maximum db in the scene
#     """
#     global readings, distances  # list of db(y) , distance(x)
#     scan2D_lower(True,0) # scan 2d 
#     readings_np = np.array(readings) 
#     max_db = np.max(readings_np) # getting max db
#     readings = []
#     distances = []
#     return max_db
#
# def trigger_get_data():
#     global radar, arduino
#     print("getting the reading now")
#     radar.trigger_reading()
#     while(True):
#         frame = radar.read_magnitude()
        
#         if frame != None:
#             print(len(frame))
#             print(frame)
#             radar.clear_buffer()
#             break
#     return frame

# def save_dist_mag_experenemt(mag,dist,name):
#     """
#     saves the dbs and step number of an experiment in an external file

#     input: mag --> dbs values 
#            dist --> step number
#            name --> name of the experiment

#     """
#     #saves dbs in "DM_Experements" folder with name of "experiment_name+_mag.txt"
#     file = open("DM_Experements/"+name+"_mag.txt", "a")
#     np.savetxt(file, mag)
#     file.close()

#     #saves step numbers in "3D_Experements" folder with name of "experiment_name+_dist.txt"
#     file = open("DM_Experements/"+name+"_dist.txt", "a")
#     np.savetxt(file, dist)
#     file.close()

# def _mag_dist_mapping(exp_name,scaning_number = 2 ,increase_upper_angel = False):
#     """
#     calibrates the scene , then scans 2d using lower motor , then plots changes in db at each step
#     input: exp_name --> name of the experiment 
#              scanning_number --> number of times to repeat the same experiment
#              increase_upper_angel --> true --> move the upper motor 1 step each time I repeat experiment
#                                       false --> don`t move upper motor each time I repeat experiment
#     """

#     global readings, distances, arduino # list of db(y) , distance(x)
#     max_db = calibrate_scene ()
    
#     print ("MAX_dB = ",max_db)

#     fig, ax = plt.subplots(nrows=scaning_number, ncols=2)
    
#     if (scaning_number == 1):
#         # scan2D_lower(True,0)
#         scan2D_lower(False,max_db)
#         x = [num*scanning_lower_step_size*step_angle for num in range(0, len(readings), 1)]
#         x_2 = [num*scanning_lower_step_size*step_angle for num in range(0, len(distances), 1)]
#         plt.subplot(211)
#         plt.plot(x, readings,marker="o")
#         plt.xlabel('Angle in (degree)')
#         plt.ylabel('Magnitude in (dB)')
#         plt.grid(True)
#         plt.subplot(212)
#         plt.plot(x_2, distances,marker="o")
#         plt.xlabel('Angle in (degree)')
#         plt.ylabel('distance in (mm)')
#         plt.grid(True)
#         plt.suptitle('Beam Pattern', fontsize=25)
#         save_dist_mag_experenemt(readings,distances,exp_name)
#     else:
#         for i in range(scaning_number):
#             # scan2D_lower(False, max_db)
#             scan2D_lower(True,0)
#             x = [num*scanning_lower_step_size*step_angle for num in range(0, len(readings), 1)]
#             x_2 = [num*scanning_lower_step_size*step_angle for num in range(0, len(distances), 1)]
#             ax[i][0].set_xlabel('Angle in (degree)')
#             ax[i][0].set_ylabel('Distance in (mm)')
#             ax[i][0].grid(True)
#             ax[i][0].plot(x_2, distances,marker="o")
#             ax[i][1].set_xlabel('Angle in (degree)')
#             ax[i][1].set_ylabel('Magnitude in (dB)')
#             ax[i][1].grid(True)
#             ax[i][1].plot(x, readings,marker="o")
#             save_dist_mag_experenemt(readings,distances,exp_name+"_"+str(i))
#             distances = []
#             readings = []

#             if increase_upper_angel:
#                 arduino.move_motor(Motors.UPPER.value, scanning_upper_step_size, Direction.NEGATIVE.value)

#     if increase_upper_angel == True:   
#         arduino.move_motor(Motors.UPPER.value, scanning_upper_step_size*scaning_number, Direction.POSITIVE.value)
    
#     plt.show()  
#####################################################################################################################