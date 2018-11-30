// Included libraries
#include <Wire.h>
#include <math.h>
#include <OneWire.h> 
#include <DallasTemperature.h>


// Device address
#define I2C_ADDR                   0x22

#define OUT_REG_TYPE uint8_t

// Pins declaration
#define AIR_IN_TEMP_ONE_WIRE_BUS   5 
#define AIR_OUT_TEMP_ONE_WIRE_BUS  5 
#define INSIDE_TEMP_ONE_WIRE_BUS   5 
#define FLOOD_PIN                  8 

// I2C registers descriptions
#define EVENT_GET_AIR_IN           0x20
#define EVENT_GET_AIR_OUT          0x21
#define EVENT_GET_AIR_INSIDE       0x22
#define EVENT_GET_FLOODING_STATUS  0x23

// Output variables
OUT_REG_TYPE VALUE_AIR_IN              = 0;
OUT_REG_TYPE VALUE_AIR_OUT             = 0;
OUT_REG_TYPE VALUE_AIR_INSIDE          = 0;
OUT_REG_TYPE VALUE_FLOODING_STATUS     = 0;

// Local variables
uint8_t EVENT = 0;
OneWire  ds(AIR_IN_TEMP_ONE_WIRE_BUS);
DallasTemperature sensors(&ds);
float airIn, airOut, airInside;
int isFlooded;



void setup() { 
  Serial.begin(115200);
  // Input pins
  sensors.begin();
  // Output pin muxing
  pinMode(13, OUTPUT);

  // I2c slave mode enabling
  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvent); // data request to slave
  Wire.onReceive(receiveEvent); // data slave received
  
}

void loop() {

  discoverOneWireDevices();

  sensors.requestTemperatures();
  //Serial.println(sensors.getTempCByIndex(0));

  airIn     = sensors.getTempCByIndex(0);
  airOut    = sensors.getTempCByIndex(1);
  airInside = sensors.getTempCByIndex(2);
  isFlooded = digitalRead(FLOOD_PIN);
/*  
  VALUE_AIR_IN          = (OUT_REG_TYPE) airIn;
  VALUE_AIR_OUT         = (OUT_REG_TYPE) airOut;
  VALUE_AIR_INSIDE      = (OUT_REG_TYPE) airInside;
  VALUE_FLOODING_STATUS = (OUT_REG_TYPE) isFlooded;
*/
  VALUE_AIR_IN          = (OUT_REG_TYPE) 21;
  VALUE_AIR_OUT         = (OUT_REG_TYPE) 22;
  VALUE_AIR_INSIDE      = (OUT_REG_TYPE) 23;
  VALUE_FLOODING_STATUS = (OUT_REG_TYPE) 24;

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
    case EVENT_GET_AIR_IN: 
      Wire.write(VALUE_AIR_IN);
      break;
    case EVENT_GET_AIR_OUT: 
      Wire.write(VALUE_AIR_OUT);
      break;
    case EVENT_GET_AIR_INSIDE: 
      Wire.write(VALUE_AIR_INSIDE);
      break;
    case EVENT_GET_FLOODING_STATUS: 
      Wire.write(VALUE_FLOODING_STATUS);
      break;
    default:
      Wire.write(0xFF);
      break;
    }
}


void discoverOneWireDevices(void) {
  byte i;
  byte present = 0;
  byte data[12];
  byte addr[8];
  
  Serial.print("Looking for 1-Wire devices...\n\r");
  while(ds.search(addr)) {
    Serial.print("\n\rFound \'1-Wire\' device with address:\n\r");

    for( i = 0; i < 8; i++) {
      Serial.print("0x");
      if (addr[i] < 16) {
        Serial.print('0');
      }
      Serial.print(addr[i], HEX);

      if (i < 7) {
        Serial.print(", ");
      }
    }
    if ( OneWire::crc8( addr, 7) != addr[7]) {
        Serial.print("CRC is not valid!\n");
        return;
    }
  }
  Serial.print("\n\r\n\rThat's it.\r\n");
  ds.reset_search();
  return;
}


