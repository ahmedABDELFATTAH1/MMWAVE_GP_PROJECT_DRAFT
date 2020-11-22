#include <AccelStepper.h>
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

 
  Serial.begin(9600);
 //motors
  H_motor.setMaxSpeed(500);
  H_motor.setAcceleration(50);

  V_motor.setMaxSpeed(500);
  V_motor.setAcceleration(50);

  //assign enable pin for both motors, D8
  H_motor.setEnablePin(8);
  H_motor.setPinsInverted(false, false, true);

  Serial.println("motors ok.");
}

void loop()
{ 
   delay(500);
  H_motor.enableOutputs();
  

  V_motor.setMaxSpeed(200);
  
  V_motor.setAcceleration(200);
 
   int n = 200 ;
   V_motor.moveTo(n);
   V_motor.runToPosition();
  
  
  delay(500000);
}
