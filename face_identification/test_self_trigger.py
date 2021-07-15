from object_detection import *
# from communication_Module import *
from radar_configuration import *
import serial
from scipy import stats
import numpy as np
import open3d as o3d
# import pyvista as pv
NUMBER_SAMPLES = 20

distances = []

def scan():
    frame = []
    data = []
    newLine =[]
    splittedLine = []
    intx = []
    radar.trigger_reading()
    time.sleep(0.1)
    data = radar.clear_buffer()
    newLine = data.decode("utf-8")
    print (newLine)
    splittedLine = newLine.split("!R")
    splittedLine = splittedLine[1].split("\t")
    if (splittedLine[len(splittedLine)-1] == '\r\n'):
        frame = splittedLine[3:len(splittedLine)-1]
        intx = [ int(fr) for fr in frame]
    else:
        print("eeeeeeerrrrrrrrrrooooorrrrrrrrr")
    # print (np.min(np.array(intx)))
    # increase_value = -1*(np.min(np.array(intx))+140)
    # print(increase_value)
    # intx = intx + increase_value
    # print(intx)
    index, distance, db_frame = radar.detect_peaks(intx, True, 0)
    print(" with db value = ", db_frame, " with a distance = ",distance)
    distances.append(distance)

# ser = serial.Serial()


if __name__=="__main__":
    print ("ahmed ")
    folder_indx = 0 
    exp_name = "waleed_14_7_136"
    folder = ["3D_Experements", "flat_Experements"]
    dist = np.loadtxt(folder[folder_indx]+"/"+exp_name+"_x.txt")
    upper_angle = np.loadtxt(folder[folder_indx]+"/"+exp_name+"_y.txt")
    lower_angle = np.loadtxt(folder[folder_indx]+"/"+exp_name+"_z.txt")



    #x , y , z = np.array(dist)*np.cos(uAngel)*np.sin(lAngel) , np.array(dist)*np.cos(uAngel)*np.cos(lAngel) , np.array(dist)*np.sin(uAngel)

    my_sample_x = np.array(dist)*np.cos(upper_angle)*np.sin(lower_angle)
    my_sample_y =  np.array(dist)*np.cos(upper_angle)*np.cos(lower_angle)
    my_sample_z =  np.array(dist)*np.sin(upper_angle)
    my_sample_x = my_sample_x[~np.isnan(my_sample_x)]
    my_sample_y = my_sample_y[~np.isnan(my_sample_y)]
    my_sample_z = my_sample_z[~np.isnan(my_sample_z)]

    # print (type(my_sample_z.tolist()))

    points = np.array([my_sample_x.tolist(), my_sample_y.tolist(), my_sample_z.tolist()])
    print(points.shape)
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[:,:3])
    o3d.visualization.draw_geometries([pcd])
    # radar = Radar()
    # radar.setup_radar()
    # val = ""
    # frame = []
    # while val != "e":
    #     val = input("Enter your value: ") 
    #     if (val == "t"):
    #         print("getting the reading now")
    # for i in range (NUMBER_SAMPLES):
    #     scan()
    # z = np.abs(stats.zscore(np.array(distances)))
    # # print(np.where(z > 3))
    # # print(z)
    # indecies = ~np.logical_or((z>=1), (z<=-1))
    # # print(indecies)
    # # print(z[indecies])
    # distances = np.array(distances)
    # print(distances[indecies])
    # print (np.average(distances[indecies]))
    # print("good bye")

