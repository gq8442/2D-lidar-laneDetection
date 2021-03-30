#include <Wire.h>
#include <Servo.h> 
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Servo servo1;
Servo servo2;

// Select which 'port' M1, M2, M3 or M4. In this case, M1
Adafruit_DCMotor *lidarMotor = AFMS.getMotor(3);
// Adafruit_DCMotor *steermotor = AFMS.getMotor(4);

void setup() {
  // put your setup code here, to run once:
    AFMS.begin();
    lidarMotor->setSpeed(0);
    //servo1.attach(10);
    servo1.write(175);

}

void loop() {
  // put your main code here, to run repeatedly:
  //RFmotor->run(RELEASE);
  //steermotor->run(RELEASE);

}
