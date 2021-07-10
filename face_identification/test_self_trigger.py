from object_detection import *
# from communication_Module import *
from radar_configuration import *
    
if __name__=="__main__":
    radar = Radar()
    radar.setup_radar()
    val = ""
    while val != "e":
        val = input("Enter your value: ") 
        if (val == "t"):
            print("getting the reading now")
            radar.trigger_reading()
            while(True):
                frame = radar.read_magnitude()
                if frame != None:
                    print(len(frame))
                    print(frame)
                    radar.clear_buffer()
                    break
    print("good bye")

