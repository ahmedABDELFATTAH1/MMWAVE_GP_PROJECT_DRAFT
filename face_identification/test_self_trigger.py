from object_detection import *
# from communication_Module import *
from radar_configuration import *
import serial
from scipy import stats
import numpy as np
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

ser = serial.Serial()


if __name__=="__main__":
    print ("ahmed ", 5656)
    radar = Radar()
    radar.setup_radar()
    # val = ""
    # frame = []
    # while val != "e":
    #     val = input("Enter your value: ") 
    #     if (val == "t"):
    #         print("getting the reading now")
    for i in range (NUMBER_SAMPLES):
        scan()
    z = np.abs(stats.zscore(np.array(distances)))
    # print(np.where(z > 3))
    # print(z)
    indecies = ~np.logical_or((z>=1), (z<=-1))
    # print(indecies)
    # print(z[indecies])
    distances = np.array(distances)
    print(distances[indecies])
    print (np.average(distances[indecies]))
    print("good bye")

