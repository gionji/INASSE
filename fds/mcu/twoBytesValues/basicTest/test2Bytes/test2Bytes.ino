// Included libraries
#include <Wire.h>
#include <math.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#include <EmonLib.h>

//Contants
#define EMON_CALIB      111.0
#define EMON_IRMS_CALIB  1480


// Device address
#define I2C_ADDR      0x30

// I2C registers descriptions
#define EVENT_GET_TEMP_PANEL_1     0x10
#define EVENT_GET_TEMP_PANEL_2     0x14
#define EVENT_GET_TEMP_ENV         0x18
#define EVENT_GET_PYRO             0x20
#define EVENT_GET_WIND             0x30

#define EVENT_GET_AIR_IN           0x10
#define EVENT_GET_AIR_OUT          0x14
#define EVENT_GET_AIR_INSIDE       0x18
#define EVENT_GET_FLOODING_STATUS  0x20
#define EVENT_GET_DHT11_AIR        0x30
#define EVENT_GET_DHT11_HUMIDITY   0x34

#define EVENT_GET_WATER_TEMP       0x10
#define EVENT_GET_PRESSURE_IN      0x20
#define EVENT_GET_PRESSURE_OUT     0x24
#define EVENT_GET_PRESSURE_MIDDLE  0x28
#define EVENT_GET_UV               0x30
#define EVENT_GET_FLUX_IN          0x40
#define EVENT_GET_FLUX_OUT         0x44
#define EVENT_GET_WATER_LEVEL      0x50

#define EVENT_GET_CC_CURRENT       0x10
#define EVENT_GET_AC1_CURRENT      0x20
#define EVENT_GET_AC2_CURRENT      0x24
#define EVENT_GET_AC3_CURRENT      0x28


// Output variables
float VALUE_TEMP_PANEL_1   = 0;
float VALUE_TEMP_PANEL_2   = 0;
float VALUE_TEMP_ENV       = 0;
int VALUE_PYRO             = 0;
int VALUE_WIND             = 0;

float VALUE_AIR_IN              = 0;
float VALUE_AIR_OUT             = 0;
float VALUE_AIR_INSIDE          = 0;
uint8_t VALUE_FLOODING_STATUS   = 0;
float VALUE_DHT11_AIR           = 0;
float VALUE_DHT11_HUMIDITY      = 0;

float VALUE_PRESSURE_IN = 0;
float VALUE_PRESSURE_OUT = 0;
float VALUE_PRESSURE_MIDDLE = 0;
float VALUE_UV = 0;
int VALUE_FLUX_IN = 0;
int VALUE_FLUX_OUT = 0;
float VALUE_WATER_TEMP = 0;
int VALUE_WATER_LEVEL = 0;

float VALUE_CC  = 0;
float VALUE_AC1 = 0;
float VALUE_AC2 = 0;
float VALUE_AC3 = 0;

#define SCALE_CC   1.0
#define SCALE_AC1  1.0
#define SCALE_AC2  1.0
#define SCALE_AC3  1.0



uint8_t EVENT = 0;

void setup() {
  Serial.begin(115200);
  
  // Output pin muxing
  pinMode(13, OUTPUT);

  // I2c slave mode enabling
  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvent); // data request to slave
  Wire.onReceive(receiveEvent); // data slave received
}

void loop() {
  // put your main code here, to run repeatedly:
  VALUE_TEMP_PANEL_1 = (float)  1.23456;
  VALUE_TEMP_PANEL_2 = (float)  123.456;
  VALUE_TEMP_ENV     = (float)  -123.456;
  VALUE_PYRO         = (int)  128; // guadagno LM358?
  VALUE_WIND         = (int)  254; 

  delay(50);
}

// I2C management
void receiveEvent(int countToRead) {
  byte x;
  while (0 < Wire.available()) {
    x = Wire.read();
    //Serial.println(x, HEX);
  }
  String message = "Receive event: ";
  String out = message + x;
  EVENT = x;
}



uint8_t b = 0;

void requestEvent() {
  String event_s = "0xFF";
  switch (EVENT) {
    case EVENT_GET_TEMP_PANEL_1 + 0: 
      b = float2Bytes(VALUE_TEMP_PANEL_1, 0);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_PANEL_1 + 1: 
      b = float2Bytes(VALUE_TEMP_PANEL_1, 1);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_PANEL_1 + 2: 
      b = float2Bytes(VALUE_TEMP_PANEL_1, 2);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_PANEL_1 + 3: 
      b = float2Bytes(VALUE_TEMP_PANEL_1, 3);
      Wire.write( b );
      break;
      
    case EVENT_GET_TEMP_PANEL_2 + 0: 
      b = float2Bytes(VALUE_TEMP_PANEL_2, 0);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_PANEL_2 + 1:  
      b = float2Bytes(VALUE_TEMP_PANEL_2, 1);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_PANEL_2 + 2:  
      b = float2Bytes(VALUE_TEMP_PANEL_2, 2);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_PANEL_2 + 3:  
      b = float2Bytes(VALUE_TEMP_PANEL_2, 3);
      Wire.write( b );
      break;
      
    case EVENT_GET_TEMP_ENV + 0: 
      b = float2Bytes(VALUE_TEMP_ENV, 0);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_ENV + 1:  
      b = float2Bytes(VALUE_TEMP_ENV, 1);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_ENV + 2:  
      b = float2Bytes(VALUE_TEMP_ENV, 2);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_ENV + 3:  
      b = float2Bytes(VALUE_TEMP_ENV, 3);
      Wire.write( b );
      break;
      
    case EVENT_GET_PYRO + 0: 
      b = float2Bytes(VALUE_PYRO, 0);
      Wire.write( b );
      break;      
    case EVENT_GET_PYRO + 1: 
      b = float2Bytes(VALUE_PYRO, 1);
      Wire.write( b );
      break;
      
    case EVENT_GET_WIND + 0: 
      b = float2Bytes(VALUE_WIND, 0);
      Wire.write( b );
      break;
    case EVENT_GET_WIND + 1: 
      b = float2Bytes(VALUE_WIND, 1);
      Wire.write( b );
      break;
      
    default:
      Wire.write(0xFF);
      break;
    }
  //Serial.println("Request event OUT: " + event_s);
}



uint8_t float2Bytes(float floatVal, int id){ 
  uint8_t *b = (uint8_t *)&floatVal;
  return b[id];
}

uint8_t int2Bytes(int intVal, int id){ 
  uint8_t *b = (uint8_t *)&intVal;
  return b[id];
}


