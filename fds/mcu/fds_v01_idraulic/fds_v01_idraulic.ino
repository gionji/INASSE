// Included libraries
#include <Wire.h>
#include <math.h>
#include <OneWire.h> 
#include <DallasTemperature.h>


// Device address
#define I2C_ADDR      0x24

// Pins declaration
#define PRESSURE_IN_PIN        A0
#define PRESSURE_OUT_PIN       A1
#define UV_PIN                 A2
#define INTERRUPT_0_PIN      2 // interrupt 0 pin
#define INTERRUPT_1_PIN      3 // interrupt 1 pin
#define TEMP_ONE_WIRE_BUS   5 

// I2C registers descriptions
#define EVENT_GET_PRESSURE_IN    0x40
#define EVENT_GET_PRESSURE_OUT    0x41
#define EVENT_GET_UV    0x42
#define EVENT_GET_FLUX_IN    0x43
#define EVENT_GET_FLUX_OUT    0x44
#define EVENT_GET_WATER_TEMP    0x45
#define EVENT_GET_WATER_LEVEL   0x46

// Output variables
uint8_t VALUE_PRESSURE_IN = 0;
uint8_t VALUE_PRESSURE_OUT = 0;
uint8_t VALUE_UV = 0;
uint8_t VALUE_FLUX_IN = 0;
uint8_t VALUE_FLUX_OUT = 0;
uint8_t VALUE_WATER_TEMP = 0;
uint8_t VALUE_WATER_LEVEL = 0;

// Local variables
volatile int int0count = 0, int1count = 0;
uint8_t EVENT = 0;
OneWire  ds(TEMP_ONE_WIRE_BUS);
DallasTemperature sensors(&ds);
float waterTemp;
int pressureIn, pressureOut, uv, fluxIn, fluxOut, waterLevel;

// Thresholds



void setup() { 
  Serial.begin(115200);
  attachInterrupt(0, interrupt0Handler, RISING);
  attachInterrupt(1, interrupt1Handler,  RISING);
  pinMode(INTERRUPT_0_PIN, INPUT);
  pinMode(INTERRUPT_1_PIN,  INPUT);
  // Input pins
  
  sensors.begin();
  // Output pin muxing

  // I2c slave mode enabling
  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvent); // data request to slave
  Wire.onReceive(receiveEvent); // data slave received
  
}

void loop() {
  // Interrupts reset
  int0count = 0;
  int1count  = 0;

  sensors.requestTemperatures();

  uv = analogRead(UV_PIN);
  pressureIn = analogRead(PRESSURE_IN_PIN);
  pressureOut = analogRead(PRESSURE_OUT_PIN);
  waterLevel = 0;
  waterTemp = sensors.getTempCByIndex(0);

  // counting interrupts
  sei();
  delay(500);
  cli();

  fluxIn  = int0count;
  fluxOut = int1count;

  VALUE_FLUX_IN  = (uint8_t) fluxIn;
  VALUE_FLUX_OUT = (uint8_t) fluxOut;
  VALUE_UV = (uint8_t) uv;
  VALUE_PRESSURE_IN  = (uint8_t) pressureIn;
  VALUE_PRESSURE_OUT  = (uint8_t) pressureOut;
  VALUE_WATER_TEMP = (uint8_t) waterTemp;
  VALUE_WATER_LEVEL = (uint8_t) waterLevel;
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

void requestEvent() {
  String event_s = "0xFF";
  switch (EVENT) {
    case EVENT_GET_PRESSURE_IN: 
      Wire.write(VALUE_PRESSURE_IN);
      break;
    case EVENT_GET_PRESSURE_OUT: 
      Wire.write(VALUE_PRESSURE_OUT);
      break;
    case EVENT_GET_UV: 
      Wire.write(VALUE_UV);
      break;
    case EVENT_GET_FLUX_IN: 
      Wire.write(VALUE_FLUX_IN);
      break;
    case EVENT_GET_FLUX_OUT: 
      Wire.write(VALUE_FLUX_OUT);
      break;
    case EVENT_GET_WATER_TEMP: 
      Wire.write(VALUE_WATER_TEMP);
      break;
    case EVENT_GET_WATER_LEVEL: 
      Wire.write(VALUE_WATER_LEVEL);
      break;
    default:
      Wire.write(0xFF);
      break;
    }
  //Serial.println("Request event OUT: " + event_s);
}





void interrupt0Handler(){
  int0count++;
  }

void interrupt1Handler(){
  int1count++;
  }
