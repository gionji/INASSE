// Included libraries
#include <Wire.h>
#include <math.h>
#include <OneWire.h> 
#include <DallasTemperature.h>


// Device address
#define I2C_ADDR      0x21

// Pins declaration
#define PYROMETER_PIN        A0
#define TEMP_ONE_WIRE_BUS    4 
#define INTERRUPT_0_PIN      2 // interrupt 0 pin

// I2C registers descriptions
#define EVENT_GET_TEMP_PANEL_1   0x10
#define EVENT_GET_TEMP_PANEL_2   0x11
#define EVENT_GET_TEMP_ENV       0x12
#define EVENT_GET_PYRO           0x13
#define EVENT_GET_WIND           0x14

// Output variables
uint8_t VALUE_TEMP_PANEL_1 = 0;
uint8_t VALUE_TEMP_PANEL_2 = 0;
uint8_t VALUE_TEMP_ENV     = 0;
uint8_t VALUE_WIND         = 0;
uint8_t VALUE_PYRO         = 0;

// Local variables
volatile int int0count =0;
uint8_t EVENT = 0;
OneWire  ds(TEMP_ONE_WIRE_BUS);
DallasTemperature sensors(&ds);
float tempPanel1, tempPanel2, tempEnv;
int wind, pyro;



void setup() { 
  Serial.begin(115200);
  attachInterrupt(0, interrupt0Handler, RISING);
  pinMode(INTERRUPT_0_PIN, INPUT);
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
  // Interrupts reset
  int0count = 0;
  sensors.requestTemperatures();
  //Serial.println(sensors.getTempCByIndex(0));

  tempPanel1    = sensors.getTempCByIndex(0);
  tempPanel2    = sensors.getTempCByIndex(1);
  tempEnv       = sensors.getTempCByIndex(2);

  // counting interrupts
  sei();
  delay(500);
  cli();
  
  wind = int0count;
  pyro = analogRead(PYROMETER_PIN);

  VALUE_TEMP_PANEL_1 = (uint8_t)  (tempPanel1 + 128);
  VALUE_TEMP_PANEL_2 = (uint8_t)  (tempPanel2 + 128);
  VALUE_TEMP_ENV     = (uint8_t)  (tempEnv + 128);
  VALUE_WIND         = (uint8_t)  wind; 
  VALUE_PYRO         = (uint8_t)  pyro >> 2; // guadagno LM358?

/*    
  VALUE_TEMP_PANEL_1 = (uint8_t) 11;
  VALUE_TEMP_PANEL_2 = (uint8_t) 12;
  VALUE_TEMP_ENV     = (uint8_t) 13;
  VALUE_WIND         = (uint8_t) 14;
  VALUE_PYRO         = (uint8_t) 15;
*/

  if(Serial.available() > 0){
    if(Serial.read() == '1'){
      Serial.print(VALUE_TEMP_PANEL_1);
      Serial.print("  ");
      Serial.print(VALUE_TEMP_PANEL_2);
      Serial.print("  ");
      Serial.print(VALUE_TEMP_ENV);
      Serial.print("  ");
      Serial.print(VALUE_WIND);
      Serial.print("  ");
      Serial.print(VALUE_PYRO);
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
    case EVENT_GET_TEMP_PANEL_1: 
      Wire.write(VALUE_TEMP_PANEL_1);
      break;
    case EVENT_GET_TEMP_PANEL_2: 
      Wire.write(VALUE_TEMP_PANEL_2);
      break;
    case EVENT_GET_TEMP_ENV: 
      Wire.write(VALUE_TEMP_ENV);
      break;
    case EVENT_GET_PYRO: 
      Wire.write(VALUE_PYRO);
      break;
    case EVENT_GET_WIND: 
      Wire.write(VALUE_WIND);
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

