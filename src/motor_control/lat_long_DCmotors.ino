#include <Wire.h>
#include <Servo.h> 
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Servo servo1;
Servo servo2;

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *RFmotor = AFMS.getMotor(3);
Adafruit_DCMotor *steermotor = AFMS.getMotor(4);



void setup() {
  // put your setup code here, to run once:
  AFMS.begin();  // create with the default frequency 1.6KHz
  RFmotor->setSpeed(100);
  steermotor->setSpeed(150);
  //servo2.attach(9);
}

void loop() {
  // put your main code here, to run repeatedly:
  RFmotor->run(BACKWARD);
  //steermotor->run(FORWARD);
  delay(1000);
  RFmotor->run(RELEASE);
  //steermotor->run(RELEASE);
  delay(1000);
  RFmotor->run(FORWARD);
  //steermotor->run(BACKWARD);
  delay(1000);
  RFmotor->run(RELEASE);
  //steermotor->run(RELEASE);
  delay(1000);
}
