import serial
class Arduino_communication():
    def initialize_com(self,com_num):
        self.arduino_con = serial.Serial(com_num)
        self.arduino_con.baudrate = 9600


    def is_open(self):
        return self.arduino_con.is_open
    
    def open_connection(self):
        if(self.is_open()):
            self.arduino_con.close()
        self.arduino_con.open()

    def send_message(self,message:str):
        self.arduino_con.write(bytes(message,'uft-8'))
        

    def read_message(self):
        line = self.arduino_con.readline()
        decoded = line.decode('uft-8')
        return decoded



