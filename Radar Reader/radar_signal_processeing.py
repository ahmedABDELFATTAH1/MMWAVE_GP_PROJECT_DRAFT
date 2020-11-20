import numpy as np
import time
def naive_face_detection(frame,bin_resolution=32.3):  
    '''
    a simple function to test object within range
    '''
    range_start=200
    range_end=500
    bin_start=int(range_start/bin_resolution)
    bin_end=int(range_end/bin_resolution)
    if(bin_start<0 or bin_end>len(frame)-1):
        return None,None
    face_frame=frame[bin_start:bin_end]
    max_index=np.argmax(face_frame)
    peak_distance=200+bin_resolution*max_index
    print("there is a peak at distance "+str(peak_distance))
    print("with magnitude =  "+str(max(face_frame)))
    return peak_distance,max(face_frame)
    
    
