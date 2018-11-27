// Included libraries
#include <Wire.h>
#include <math.h>
#include <EmonLib.h>

//Contants
#define EMON_CALIB      111.0
#define EMON_IRMS_CALIB  1480

// Device address
#define I2C_ADDR             0x22

// Pins declaration
#define CC_OUTPUT_PIN         A0
#define AC_OUTPUT_1_PIN       A1
#define AC_OUTPUT_2_PIN       A2
#define AC_OUTPUT_3_PIN       A3

// I2C registers descriptions
#define EVENT_GET_CC_CURRENT      0x10
#define EVENT_GET_AC1_CURRENT     0x11
#define EVENT_GET_AC2_CURRENT     0x12
#define EVENT_GET_AC3_CURRENT     0x13

// Output variables
uint8_t VALUE_CC = 0;
uint8_t VALUE_AC1 = 0;
uint8_t VALUE_AC2 = 0;
uint8_t VALUE_AC3 = 0;

#define SCALE_CC   1.0
#define SCALE_AC1  1.0
#define SCALE_AC2  1.0
#define SCALE_AC3  1.0

uint8_t EVENT = 0;

// Local variables
volatile int int0count =0, int1count=0;
EnergyMonitor acOutput1; 
EnergyMonitor acOutput2;
EnergyMonitor acOutput3; 

// Thresholds



void setup() { 
  Serial.begin(115200);
  // Input pins

  // Output pin muxing

  // I2c slave mode enabling
  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvent); // data request to slave
  Wire.onReceive(receiveEvent); // data slave received

  //Emon cofiguration   
  acOutput1.current(AC_OUTPUT_1_PIN, EMON_CALIB);             // Current: input pin, calibration.
  acOutput2.current(AC_OUTPUT_2_PIN, EMON_CALIB);             // Current: input pin, calibration.
  acOutput3.current(AC_OUTPUT_3_PIN, EMON_CALIB);             // Current: input pin, calibration.       
}

void loop() {
  // read currents
  int Icc = analogRead(CC_OUTPUT_PIN);
  double Irms1 = acOutput1.calcIrms(1480);  // Calculate Irms only
  double Irms2 = acOutput2.calcIrms(1480);  // Calculate Irms only
  double Irms3 = acOutput3.calcIrms(1480);  // Calculate Irms only

  VALUE_CC  = Icc   * SCALE_CC;
  VALUE_AC1 = Irms1 * SCALE_AC1;
  VALUE_AC2 = Irms2 * SCALE_AC2;
  VALUE_AC3 = Irms3 * SCALE_AC3;
}

// I2C management
void receiveEvent(int countToRead) {
  byte x;
  while (0 < Wire.available()) {
    x = Wire.read();
    //Serial.println(x, HEX);
  }
  //String message = "Receive event: ";
  //String out = message + x;
  
  EVENT = x;
}

void requestEvent() {
  String event_s = "0xFF";
  switch (EVENT) {
    case EVENT_GET_CC_CURRENT: 
      Wire.write(VALUE_CC);
      break;
    case EVENT_GET_AC1_CURRENT: 
      Wire.write(VALUE_AC1);
      break;
    case EVENT_GET_AC2_CURRENT: 
      Wire.write(VALUE_AC2);
      break;
    case EVENT_GET_AC3_CURRENT: 
      Wire.write(VALUE_AC3);
      break;
    default:
      Wire.write(0xFF);
      //event_s = String(0xFF,HEX);
      //Serial.println("Request event: " + event_s);
      break;
    }
  //Serial.println("Request event OUT: " + event_s);
}

