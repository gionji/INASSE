// Included libraries
#include <Wire.h>
#include <math.h>


// Device address
#define I2C_ADDR      0x21

// Pins declaration
#define XXX_PIN       A0
#define INTERRUPT_0_PIN      2 // interrupt 0 pin
#define INTERRUPT_1_PIN      3 // interrupt 1 pin

// I2C registers descriptions
#define EVENT_XXX     0x10

// Output variables
int VALUE_XXX = 0;

// Local variables
volatile int int0count =0, int0count=0;

// Thresholds



void setup() { 
  Serial.begin(115200);
  attachInterrupt(0, interrupt0Handler, RISING);
  attachInterrupt(1, interrupt1Handler,  RISING);
  pinMode(INTERRUPT_0_PIN, INPUT);
  pinMode(INTERRUPT_1_PIN,  INPUT);
  // Input pins

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

  // counting interrupts
  sei();
  delay(500);
  cli();
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
    case EVENT_XXX: 
      Wire.write(VALUE_XXX);
      //event_s = String(VALUE_XXX, HEX);
      //Serial.println("Request event: " + event_s);
      break;
    default:
      Wire.write(0xFF);
      //event_s = String(0xFF,HEX);
      //Serial.println("Request event: " + event_s);
      break;
    }
  //Serial.println("Request event OUT: " + event_s);
}





void interrupt0Handler(){
  airFreq++;
  }

void interrup1Handler(){
  flowFreq++;
  }
