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
  //V_motor.setSpeed(V_speed);
  //H_motor.setSpeed(H_speed);
  
  V_motor.setCurrentPosition(0);
  H_motor.setCurrentPosition(0);

  V_motor.moveTo(max_V_steps/2);
  V_motor.runToPosition();

  H_motor.moveTo(max_H_steps/2);
  H_motor.runToPosition();
  
  H_direction *= -1;
  V_direction *= -1;
  Serial.begin(9600);
 
//  //assign enable pin for both motors, D8
//  H_motor.setEnablePin(8);
//  H_motor.setPinsInverted(false, false, true);
//  //enable motors
//  H_motor.enableOutputs();
}

void loop()
{ 
  home_H();

  //back to origin
  V_motor.moveTo(0);
  V_motor.runToPosition();

  H_motor.moveTo(0);
  H_motor.runToPosition();
  
  delay(500000);
  
}

void home_H() {
  
    //H_motor.setCurrentPosition(0);
    int scaler = 2 * H_direction;   //to increase the step size
    int final_point = max_H_steps * H_direction/2 + scaler ;
    long current_position = H_motor.currentPosition();
    while (current_position != final_point) { // run until it reaches the distance value
     home_V();
     //H_motor.setSpeed(H_direction * H_speed);
     H_motor.moveTo(current_position+scaler);
     //H_motor.runSpeed();
     H_motor.runToPosition();
     current_position = current_position+scaler;
  }
  H_direction *= -1;

}

void home_V() {
//  V_motor.setCurrentPosition(0);
//  int final_point = max_V_steps * V_direction;
  long current_position = V_motor.currentPosition();
//  while (current_position != final_point  ) { // run until it reaches the distance value
//    V_motor.setSpeed(V_direction * V_speed);
//    V_motor.runSpeed();
//    
//  }
  V_motor.moveTo(max_V_steps*V_direction/2);
  V_motor.runToPosition();

  V_direction *= -1;
}
