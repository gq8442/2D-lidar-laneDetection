#include <Wire.h>
#include <Servo.h> 
#include <Adafruit_MotorShield.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield(); 

Servo servo1;
Servo servo2; // Steering Servo

// Select which 'port' M1, M2, M3 or M4. In this case, M2
Adafruit_DCMotor *lidarMotor = AFMS.getMotor(3);



void setup() {
  // put your setup code here, to run once:
  AFMS.begin();  // create with the default frequency 1.6KHz
  lidarMotor->setSpeed(175);
  servo1.attach(10);
  servo2.attach(9);
}

int i;

void loop() {
  // put your main code here, to run repeatedly:
  lidarMotor->run(BACKWARD);
  for (i=0; i<255; i++) {
    //servo2.write(map(i, 0, 255, 45, 85)); // This is for steering servo motor
    servo1.write(map(i, 0, 255, 175, 150));
    delay(5);
  }
    for (i=0; i<255; i++) {
    //servo2.write(map(i, 0, 255, 85, 45)); // This is for steering servo motor
    servo1.write(map(i, 0, 255, 150, 175));
    delay(5);
  }
}
