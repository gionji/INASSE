// Included libraries
#include <Wire.h>
#include <math.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#include <DHT.h>

// Device address
#define I2C_ADDR                   0x22

#define OUT_REG_TYPE uint8_t

// Pins declaration
#define ONE_WIRE_BUS   5 
#define DHT11_BUS      6 
#define FLOOD_PIN      7 

// I2C registers descriptions
#define EVENT_GET_AIR_IN           0x20
#define EVENT_GET_AIR_OUT          0x21
#define EVENT_GET_AIR_INSIDE       0x22
#define EVENT_GET_FLOODING_STATUS  0x23
#define EVENT_GET_DHT11_AIR        0x24
#define EVENT_GET_DHT11_HUMIDITY   0x25

// Output variables
OUT_REG_TYPE VALUE_AIR_IN              = 0;
OUT_REG_TYPE VALUE_AIR_OUT             = 0;
OUT_REG_TYPE VALUE_AIR_INSIDE          = 0;
OUT_REG_TYPE VALUE_FLOODING_STATUS     = 0;
OUT_REG_TYPE VALUE_DHT11_AIR           = 0;
OUT_REG_TYPE VALUE_DHT11_HUMIDITY      = 0;

// Local variables
uint8_t EVENT = 0;
OneWire  ds(ONE_WIRE_BUS);
DallasTemperature sensors(&ds);
float airIn, airOut, airInside, dht11air, dht11humidity;
int isFlooded;
DHT dht(DHT11_BUS, DHT11);


void setup() { 
  Serial.begin(115200);
  // Input pins
  sensors.begin();
  // Output pin muxing
  pinMode(13, OUTPUT);
  dht.begin();

  // I2c slave mode enabling
  Wire.begin(I2C_ADDR);
  Wire.onRequest(requestEvent); // data request to slave
  Wire.onReceive(receiveEvent); // data slave received 
}

void loop() {

  //discoverOneWireDevices();

  sensors.requestTemperatures();

  airIn         = sensors.getTempCByIndex(0);
  airOut        = sensors.getTempCByIndex(1);
  airInside     = sensors.getTempCByIndex(2);
  isFlooded     = digitalRead(FLOOD_PIN);  
  dht11air      = dht.readHumidity();
  dht11humidity = dht.readTemperature();

  VALUE_AIR_IN          = (OUT_REG_TYPE) (airIn + 128);
  VALUE_AIR_OUT         = (OUT_REG_TYPE) (airOut + 128);
  VALUE_AIR_INSIDE      = (OUT_REG_TYPE) (airInside + 128);
  VALUE_FLOODING_STATUS = (OUT_REG_TYPE) isFlooded;
  VALUE_DHT11_AIR       = (OUT_REG_TYPE) (dht11air + 128);
  VALUE_DHT11_HUMIDITY  = (OUT_REG_TYPE) (dht11humidity + 128);

  if(Serial.available() > 0){
    if(Serial.read() == '1'){
      Serial.print(VALUE_AIR_IN);
      Serial.print("  ");
      Serial.print(VALUE_AIR_OUT);
      Serial.print("  ");
      Serial.print(VALUE_AIR_INSIDE);
      Serial.print("  ");
      Serial.print(VALUE_FLOODING_STATUS);
      Serial.print("  ");
      Serial.print(VALUE_DHT11_AIR);
      Serial.print("  ");
      Serial.print(VALUE_DHT11_HUMIDITY);
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
    case EVENT_GET_DHT11_AIR: 
      Wire.write(VALUE_DHT11_AIR);
      break;
    case EVENT_GET_DHT11_HUMIDITY: 
      Wire.write(VALUE_DHT11_HUMIDITY);
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
