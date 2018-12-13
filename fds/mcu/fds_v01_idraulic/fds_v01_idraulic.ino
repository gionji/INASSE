// Included libraries
#include <Wire.h>
#include <math.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#include <SoftwareSerial.h>

// Device address
#define I2C_ADDR      0x23

// Pins declaration
#define PRESSURE_IN_PIN        A0
#define PRESSURE_MIDDLE_PIN    A3
#define PRESSURE_OUT_PIN       A1
#define UV_PIN                 A2
#define INTERRUPT_0_PIN      2 // interrupt 0 pin
#define INTERRUPT_1_PIN      3 // interrupt 1 pin
#define TEMP_ONE_WIRE_BUS    8 

// I2C registers descriptions
#define EVENT_GET_PRESSURE_IN     0x30
#define EVENT_GET_PRESSURE_OUT    0x31
#define EVENT_GET_UV              0x32
#define EVENT_GET_FLUX_IN         0x33
#define EVENT_GET_FLUX_OUT        0x34
#define EVENT_GET_WATER_TEMP      0x35
#define EVENT_GET_WATER_LEVEL     0x36
#define EVENT_GET_PRESSURE_MIDDLE 0x37

// Output variables
uint8_t VALUE_PRESSURE_IN = 0;
uint8_t VALUE_PRESSURE_OUT = 0;
uint8_t VALUE_PRESSUER_MIDDLE = 0;
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
int pressureIn, pressureOut, pressureMiddle, uv, fluxIn, fluxOut, waterLevel;
SoftwareSerial DYPSensor(9, 10); // RX, TX

// Thresholds
const int MAX_TRY_SERIAL = 50;
const int CYCLES = 10;


void setup() { 
  Serial.begin(115200);
  attachInterrupt(0, interrupt0Handler, RISING);
  attachInterrupt(1, interrupt1Handler,  RISING);
  pinMode(INTERRUPT_0_PIN, INPUT);
  pinMode(INTERRUPT_1_PIN,  INPUT);
  // Input pins
  
  sensors.begin();
  // Output pin muxing
  pinMode(13, OUTPUT);
  // I2c slave mode enabling
  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvent); // data request to slave
  Wire.onReceive(receiveEvent); // data slave received

  DYPSensor.begin(9600);
  
}

void loop() {
  // Interrupts reset
  int0count  = 0;
  int1count  = 0;

  sensors.requestTemperatures();

  uv = analogRead(UV_PIN);
  pressureIn  = analogRead(PRESSURE_IN_PIN);
  pressureOut = analogRead(PRESSURE_OUT_PIN);
  pressureMiddle = analogRead(PRESSURE_MIDDLE_PIN);  
  waterLevel = GetDistance();
  waterTemp = sensors.getTempCByIndex(0);

  Serial.println(waterLevel);

/*
 * 
 * 0xFF: frame start marker byte.
H_DATA: distance data of high eight.
L_DATA: distance data of low 8 bits.
Checksum byte: Value should equal 0xFF + H_DATA + L_DATA  (only lowest 8 bits)
 */



  // counting interrupts
  sei();
  delay(500);
  cli();

  fluxIn  = int0count;
  fluxOut = int1count;


  VALUE_FLUX_IN      = (uint8_t) fluxIn;
  VALUE_FLUX_OUT     = (uint8_t) fluxOut;
  VALUE_UV           = (uint8_t) uv >> 2;
  VALUE_PRESSURE_IN  = (uint8_t) pressureIn  >> 2;
  VALUE_PRESSURE_OUT = (uint8_t) pressureOut >> 2;
  VALUE_WATER_TEMP   = (uint8_t) waterTemp  + 128;
  VALUE_WATER_LEVEL  = (uint8_t) waterLevel;
  VALUE_PRESSURE_MIDDLE = (uint8_t) pressureMiddle >> 2;
/*
  VALUE_PRESSURE_IN  = (uint8_t) 31;
  VALUE_PRESSURE_OUT = (uint8_t) 32;
  VALUE_UV           = (uint8_t) 33;
  VALUE_FLUX_IN      = (uint8_t) 34;
  VALUE_FLUX_OUT     = (uint8_t) 35;
  VALUE_WATER_TEMP   = (uint8_t) 36;
  VALUE_WATER_LEVEL  = (uint8_t) 37;
*/


  if(Serial.available() > 0){
    if(Serial.read() == '1'){
      Serial.print(VALUE_FLUX_IN);
      Serial.print("  ");
      Serial.print(VALUE_FLUX_OUT);
      Serial.print("  ");
      Serial.print(VALUE_UV);
      Serial.print("  ");
      Serial.print(VALUE_PRESSURE_IN);
      Serial.print("  ");
      Serial.print(VALUE_PRESSURE_OUT);
      Serial.print("  ");
      Serial.print(VALUE_PRESSURE_MIDDLE);
      Serial.print("  ");
      Serial.print(VALUE_WATER_TEMP);
      Serial.print("  ");
      Serial.print(VALUE_WATER_LEVEL);

      Serial.println("  ");
    }
  }

  
  digitalWrite(13, HIGH);
  delay(10);
  digitalWrite(13, LOW);
  delay(10);
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
    case EVENT_GET_PRESSURE_MIDDLE:
      Wire.write(VALUE_PRESSURE_MIDDLE);
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



int GetDistance() {
 int mean   = 0;
 int valids = 0;


for(int i=0; i<CYCLES; i++){
 byte msb, lsb, checksum, checkcalc, tries = 0;
 int distance;

// we want a 255 which is the start of the reading (not msb but saving a byte of variable storage)..
 while (msb != 255) {
 // wait for serial..
 while ( not DYPSensor.available() && tries < MAX_TRY_SERIAL ) {
 delay(10);
 tries++;
 }
 if (tries == MAX_TRY_SERIAL) {
 //Serial.println(" TIMED OUT WAITING FOR SERIAL.");
 return -1;
 }
 msb = DYPSensor.read();
 }

// now we collect MSB, LSB, Checksum..
 while ( not DYPSensor.available() ) {
 delay(10);
 }
 msb = DYPSensor.read();

while ( not DYPSensor.available() ) {
 delay(10);
 }
 lsb = DYPSensor.read();

while ( not DYPSensor.available() ) {
 delay(10);
 }
 checksum = DYPSensor.read();

// is the checksum ok?
 checkcalc = 255 + msb + lsb;

if (checksum == checkcalc) {
 distance = msb * 256 + lsb;
 // Round from mm to cm
 distance += 5;
 distance = distance / 10;

 mean += distance;
 valids++;
 } else {
  //Serial.println("bad checksum - ignoring reading.");
  //return -1;
 }

}

return mean/valids;
} // end of GetDistance()  
