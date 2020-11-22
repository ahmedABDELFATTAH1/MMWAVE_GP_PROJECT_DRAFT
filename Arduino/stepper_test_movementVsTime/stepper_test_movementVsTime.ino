#include <AccelStepper.h>
#include "TFMini.h"
#include <SoftwareSerial.h>
#include <SPI.h>

// The X Stepper pins
#define STEPPER1_DIR_PIN 2
#define STEPPER1_STEP_PIN 5
// The Y stepper pins
#define STEPPER2_DIR_PIN 3
#define STEPPER2_STEP_PIN 6

// Define some steppers and the pins the will use
AccelStepper H_motor(AccelStepper::DRIVER, STEPPER1_STEP_PIN, STEPPER1_DIR_PIN);
AccelStepper V_motor(AccelStepper::DRIVER, STEPPER2_STEP_PIN, STEPPER2_DIR_PIN);


/*step for full circle
  classic NEMA 17 and pololu A4988 driver
  full step = 200 steps / 1 step = 1,8°
  1/2 steps = 400 steps / 1 step = 0,9°
  1/4 steps = 800 steps / 1 step = 0,45°

*/

const float step2angle = 0.45;

//range for horizontal
const int max_H_angle = 22.5;

//range for vertical
const int max_V_angle = 45;

//vertical speed
const int V_speed = 300;
const int Max_v_speed = V_speed + 50;

//horizontal speed 
const int H_speed = 1000;
const int Max_h_speed = H_speed + 50;


// max H angle / step2angle = 180/0.45=400 steps
const int max_H_steps = max_H_angle / step2angle;

// max H angle / step2angle = 90/0.45=200 steps
const int max_V_steps = max_V_angle / step2angle;


int V_direction = 1;
int H_direction = 1;

void setup()
{

  V_motor.setMaxSpeed(Max_v_speed);
  H_motor.setMaxSpeed(Max_h_speed);

  V_motor.setAcceleration(Max_v_speed);
  H_motor.setAcceleration(Max_h_speed);
 
  
  Serial.begin(9600);
 

}

void loop()
{ 
   delay(500);
  
  unsigned long s = micros();
  testStepSize(1);
  unsigned long e = micros();
  unsigned long delta = e - s;
  Serial.println("number of steps = 1");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
  
  s = micros();
  testStepSize(2);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 2");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
  
  s = micros();
  testStepSize(4);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 4");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
  
  s = micros();
  testStepSize(8);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 8");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);

  s = micros();
  testStepSize(16);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 16");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
    
  s = micros();
  testStepSize(32);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 32");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
  
  s = micros();
  testStepSize(40);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 40");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
  
  s = micros();
  testStepSize(80);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 80");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
  
  s = micros();
  testStepSize(160);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 160");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);


  s = micros();
  testStepSize(400);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 400");
  Serial.println(delta);
  Serial.println("--------------------------------");
  delay(500);
  
  s = micros();
  testStepSize(800);
  e = micros();
  delta = e - s;
  Serial.println("number of steps = 800");
  Serial.println(delta);
  Serial.println("--------------------------------");
  
  delay(500000);
}

void testStepSize(int steps_number){

  V_motor.setCurrentPosition(0);
  H_motor.setCurrentPosition(0);

 // Call to your function
    int n = 800 ;
    long current_position = H_motor.currentPosition();
    for (int i = 0 ; i< steps_number ; i++ ) { // run until it reaches the distance value
     
     V_motor.moveTo(current_position+n/steps_number);
     //H_motor.runSpeed();
     V_motor.runToPosition();
     current_position = current_position+n/steps_number;
  }

 
}
