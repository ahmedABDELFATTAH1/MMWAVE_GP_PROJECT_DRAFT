import serial
import numpy as np
import matplotlib.pyplot as plt
import cv2
"""
Authored by
ahmed mahmoud
ahmed waleedd
ahmed nassar abdullah ezzat

this is an application to configure the radar , read from it and plot the output in a nice way

library used :
PySerial

useful links :
https://maker.pro/pic/tutorial/introduction-to-python-serial-ports



info about the radar :
uses UART
 TSV output
(Tab Separated Values) 
"""


"""
The following UART settings apply for firmware version 1.4 and later: 1 Mbaud, 8 data bits, 1 start bit, 1 stop bit,
no parity, no flow control.
"""
serialPort = serial.Serial(port = "COM4", baudrate=115200,
                         bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)


#---------------------------------GLOBAL VARIABELS --------------------------------
serialString = ""                           # Used to hold data coming over UART


#---------------------------------Functions ------------------------------------


def trigger():
    trigger_signals=["!M\r\n","!N\r\n","!L\\r\n"]#he said one of thease will trigger the radar to senda ramp





#---------Test----------------------
serialPort.open()
while(1):
    

    # Wait until there is data waiting in the serial buffer
    if(serialPort.in_waiting > 0):

        # Read data out of the buffer until a carraige return / new line is found
        serialString = serialPort.readline()

        # Print the contents of the serial data
        print(serialString.decode('Ascii'))

        # Tell the device connected over the serial port that we recevied the data!
        # The b at the beginning is used to indicate bytes!
        serialPort.write(b"Thank you for sending data \r\n")