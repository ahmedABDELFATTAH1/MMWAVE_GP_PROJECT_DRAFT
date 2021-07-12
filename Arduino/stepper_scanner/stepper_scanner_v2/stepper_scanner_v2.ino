#include <AccelStepper.h>
#include <SoftwareSerial.h>
#include <SPI.h>

// The X Stepper pins
#define STEPPER1_DIR_PIN 5
#define STEPPER1_STEP_PIN 2
// The Y stepper pins
#define STEPPER2_DIR_PIN 6
#define STEPPER2_STEP_PIN 3

#define MOTOR_TYPE  1
#define MOTOR_ENABLE 8
// Define some steppers and the pins the will use
AccelStepper lower_motor(MOTOR_TYPE, STEPPER1_STEP_PIN, STEPPER1_DIR_PIN);
AccelStepper upper_motor(MOTOR_TYPE, STEPPER2_STEP_PIN, STEPPER2_DIR_PIN);

int  data;
String dataString;
bool flag = true;
//vertical speed
const float upper_motor_speed = 300;
const float Max_upper_motor_speed = upper_motor_speed + 50;

//horizontal speed 
const float lower_motor_speed = 1000;
const float Max_lower_motor_speed = lower_motor_speed + 50;

void setup()
{

  upper_motor.setMaxSpeed(Max_upper_motor_speed);
  lower_motor.setMaxSpeed(Max_lower_motor_speed);

  upper_motor.setAcceleration(Max_upper_motor_speed);
  lower_motor.setAcceleration(Max_lower_motor_speed);
  
  upper_motor.setCurrentPosition(0);
  lower_motor.setCurrentPosition(0);
  
  pinMode (MOTOR_ENABLE,OUTPUT);
  digitalWrite(MOTOR_ENABLE,LOW);
  
  Serial.begin(1000000);
}

void loop()
{ 
  if (flag)
  {
    Serial.println("ready"); 
    flag = false; 
  }
  
  if (Serial.available())
  {
    dataString = "";
    do{
    data = Serial.read();
    if(data != -1 && data != 10)
      dataString = dataString+(char)data;
    }while(data !=36);
    
    if (dataString[0] == 'l')
    {
      int movement = dataString.substring(1,dataString.length()-1).toInt();
      move_lower_motor(movement);
      send_confirmation(dataString);
    }
    else if  (dataString[0] == 'u')
    {
      int movement = dataString.substring(1,dataString.length()-1).toInt();
      move_upper_motor(movement);
      send_confirmation(dataString);
    }
    else
    {
      Serial.println("Error: invalid command");
    }
  }
}

void move_lower_motor(int number_of_steps) {
    long current_position = lower_motor.currentPosition();
     lower_motor.moveTo(current_position+number_of_steps);
     lower_motor.runToPosition();
}


void move_upper_motor(int number_of_steps) {
    long current_position = upper_motor.currentPosition();
     upper_motor.moveTo(current_position+number_of_steps);
     upper_motor.runToPosition();
}

void send_confirmation(String dataString){
  Serial.println("Confirmation :" + dataString);
}
