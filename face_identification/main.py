from object_detection import *
from communication_Module import *




if __name__=="__main__":
    #setting upp arduino ports
    arduino = set_up()

    #moves the sensor in lower direction (XY plane) until the face is found
    lowerDirection = calibrateLower()
    if(lowerDirection is None):
        moveMotor(Motors.LOWER.value , maxStepsOfLower , Direction.POSITIVE.value)
    else: 
        scanFace(lowerDirection)

