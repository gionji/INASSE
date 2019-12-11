/*
 * If defined are also enabled: DHT, FLOOD, WATERLEVEL, 3rd temperature
 */
//#define MAY_COMPLETE_SETUP 1

#define FIRMWARE_VERSION 9

// Included libraries
#include <Wire.h>
#include <math.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#include <EmonLib.h>


/*
 * Contants
 */
#define EMON_CALIB        111.0
#define EMON_IRMS_CALIB   1480
#define SCALE_CC          1.0
#define SCALE_AC1         1.0
#define SCALE_AC2         1.0
#define SCALE_AC3         1.0

/*
 * Define slave I2C
 */
#define I2C_ADDR      0x27 

/*
 * I2C registers descriptions
 */
#define EVENT_GET_FIRMWARE_VERSION          0x90
 
#define EVENT_GET_TEMP_1     0x10
#define EVENT_GET_TEMP_2     0x14
#define EVENT_GET_TEMP_3     0x18

#define EVENT_GET_PRESSURE_IN      0x20
#define EVENT_GET_PRESSURE_OUT     0x24
#define EVENT_GET_PRESSURE_MIDDLE  0x28

#define EVENT_GET_FLUX_IN          0x30
#define EVENT_GET_FLUX_OUT         0x34

#define EVENT_GET_CC_CURRENT       0x40
#define EVENT_GET_AC1_CURRENT      0x44
#define EVENT_GET_AC2_CURRENT      0x48

#define EVENT_GET_DHT11_AIR        0x50
#define EVENT_GET_DHT11_HUMIDITY   0x54

#define EVENT_GET_FLOODING_STATUS  0x60

#define EVENT_GET_WATER_LEVEL      0x70

/*
 * Pin declaration
 */

  #define CC_OUTPUT_PIN         A0
  #define PRESSURE_IN_PIN       A1
  #define PRESSURE_MIDDLE_PIN   A2
  #define PRESSURE_OUT_PIN      A3
  #define AC_OUTPUT_1_PIN       A6
  #define AC_OUTPUT_2_PIN       A7
  #define INTERRUPT_0_PIN       2
  #define INTERRUPT_1_PIN       3 
	#define TEMP_ONE_WIRE_BUS     5 
	#define DHT11_ONEWIRE_BUS     6 
	#define FLOOD_PIN             7 
	#define SERIAL_RX_PIN         9
	#define SERIAL_TX_PIN         10

/*
 * Output variables
 */
uint8_t VALUE_FIRMWARE_VERSION = (uint8_t) FIRMWARE_VERSION;
 
float VALUE_TEMP_1       = 0;
float VALUE_TEMP_2       = 0;
float VALUE_TEMP_3       = 0;

float VALUE_PRESSURE_IN        = 0;
float VALUE_PRESSURE_OUT       = 0;
float VALUE_PRESSURE_MIDDLE    = 0;

int   VALUE_FLUX_IN            = 0;
int   VALUE_FLUX_OUT           = 0;

float VALUE_CC                 = 0;
float VALUE_AC1                = 0;
float VALUE_AC2                = 0;


/*
 * Common variables
 */
uint8_t EVENT = 0;


/*
 * Local variables
 */
volatile int int0count = 0, int1count = 0;

OneWire  ds(TEMP_ONE_WIRE_BUS);
DallasTemperature sensors(&ds);
float temp1, temp2, temp3;
int pressureIn, pressureOut, pressureMiddle, fluxIn, fluxOut, waterLevel;
EnergyMonitor acOutput1; 
EnergyMonitor acOutput2;

/*
 * Setup
 */
void setup() {
	Serial.begin(115200);
	sensors.begin();
	attachInterrupt(0, interrupt0Handler,  RISING);
	attachInterrupt(1, interrupt1Handler,  RISING);
	pinMode(INTERRUPT_0_PIN,  INPUT);
	pinMode(INTERRUPT_1_PIN,  INPUT);
	acOutput1.current(AC_OUTPUT_1_PIN, EMON_CALIB);             
	acOutput2.current(AC_OUTPUT_2_PIN, EMON_CALIB);  
  
	// Output pin muxing
	pinMode(13, OUTPUT);

	// I2c slave mode enabling
	Wire.begin(I2C_ADDR);
	Wire.onRequest(requestEvent); // data request to slave
	Wire.onReceive(receiveEvent); // data slave received

  for(int i=0; i<5; i++){
    digitalWrite(13, HIGH);
    delay(30);
    digitalWrite(13, LOW);
    delay(30);
    }
}



void loop() {
  int0count  = 0;
  int1count  = 0;
	sensors.requestTemperatures();

	temp1    = sensors.getTempCByIndex(0);
	temp2    = sensors.getTempCByIndex(1);
  temp3    = sensors.getTempCByIndex(2);
  
  pressureIn     = analogRead(PRESSURE_IN_PIN);
  pressureOut    = analogRead(PRESSURE_OUT_PIN);
  pressureMiddle = analogRead(PRESSURE_MIDDLE_PIN);  

	// counting interrupts
	sei();
	delay(500);
	cli();

	fluxIn  = int0count;
	fluxOut = int1count;
  
  int Icc = analogRead(CC_OUTPUT_PIN);
  double Irms1 = acOutput1.calcIrms(1480);  // Calculate Irms only
  double Irms2 = acOutput2.calcIrms(1480);  // Calculate Irms only
  
  VALUE_TEMP_1 = (float)  temp1;
  VALUE_TEMP_2 = (float)  temp2;
  VALUE_TEMP_3 = (float)  temp3;
	VALUE_FLUX_IN      = (int) fluxIn;
	VALUE_FLUX_OUT     = (int) fluxOut;
	VALUE_PRESSURE_IN  = (float) pressureIn;
	VALUE_PRESSURE_OUT = (float) pressureOut;
  VALUE_PRESSURE_MIDDLE = (float) pressureMiddle;
  VALUE_CC  = (float) Icc ;
  VALUE_AC1 = (float)(Irms1 * SCALE_AC1);
  VALUE_AC2 = (float)(Irms2 * SCALE_AC2);

	digitalWrite(13, HIGH);
	delay(10);
	digitalWrite(13, LOW);
	delay(10);

	//delay(100);
}



// I2C management
void receiveEvent(int countToRead) {
  byte x;
  while (0 < Wire.available()) {
    x = Wire.read();
  }
  EVENT = x;
}



uint8_t b = 0;

void requestEvent() {
  String event_s = "0xFF";
  switch (EVENT) {
    case EVENT_GET_FIRMWARE_VERSION: 
      Wire.write( VALUE_FIRMWARE_VERSION );
      break;

    case EVENT_GET_TEMP_1 + 0: 
      b = float2Bytes(VALUE_TEMP_1, 0);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_1 + 1: 
      b = float2Bytes(VALUE_TEMP_1, 1);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_1 + 2: 
      b = float2Bytes(VALUE_TEMP_1, 2);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_1 + 3: 
      b = float2Bytes(VALUE_TEMP_1, 3);
      Wire.write( b );
      break;
      
    case EVENT_GET_TEMP_2 + 0: 
      b = float2Bytes(VALUE_TEMP_2, 0);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_2 + 1:  
      b = float2Bytes(VALUE_TEMP_2, 1);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_2 + 2:  
      b = float2Bytes(VALUE_TEMP_2, 2);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_2 + 3:  
      b = float2Bytes(VALUE_TEMP_2, 3);
      Wire.write( b );
      break;
      
    case EVENT_GET_TEMP_3+ 0: 
      b = float2Bytes(VALUE_TEMP_3, 0);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_3 + 1:  
      b = float2Bytes(VALUE_TEMP_3, 1);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_3 + 2:  
      b = float2Bytes(VALUE_TEMP_3, 2);
      Wire.write( b );
      break;
    case EVENT_GET_TEMP_3 + 3:  
      b = float2Bytes(VALUE_TEMP_3, 3);
      Wire.write( b );
      break;

    case EVENT_GET_PRESSURE_IN + 0: 
      b = float2Bytes(VALUE_PRESSURE_IN, 0);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_IN + 1: 
      b = float2Bytes(VALUE_PRESSURE_IN, 1);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_IN + 2: 
      b = float2Bytes(VALUE_PRESSURE_IN, 2);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_IN + 3: 
      b = float2Bytes(VALUE_PRESSURE_IN, 3);
      Wire.write( b );
      break;

    case EVENT_GET_PRESSURE_OUT + 0: 
      b = float2Bytes(VALUE_PRESSURE_OUT, 0);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_OUT + 1: 
      b = float2Bytes(VALUE_PRESSURE_OUT, 1);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_OUT + 2: 
      b = float2Bytes(VALUE_PRESSURE_OUT, 2);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_OUT + 3: 
      b = float2Bytes(VALUE_PRESSURE_OUT, 3);
      Wire.write( b );
      break;

    case EVENT_GET_PRESSURE_MIDDLE + 0: 
      b = float2Bytes(VALUE_PRESSURE_MIDDLE, 0);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_MIDDLE + 1: 
      b = float2Bytes(VALUE_PRESSURE_MIDDLE, 1);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_MIDDLE + 2: 
      b = float2Bytes(VALUE_PRESSURE_MIDDLE, 2);
      Wire.write( b );
      break;
    case EVENT_GET_PRESSURE_MIDDLE + 3: 
      b = float2Bytes(VALUE_PRESSURE_MIDDLE, 3);
      Wire.write( b );
      break;

    case EVENT_GET_FLUX_IN + 0: 
      b = int2Bytes(VALUE_FLUX_IN, 0);
      Wire.write( b );
      break;
    case EVENT_GET_FLUX_IN + 1: 
      b = int2Bytes(VALUE_FLUX_IN, 1);
      Wire.write( b );
      break;
   
    case EVENT_GET_FLUX_OUT + 0: 
      b = int2Bytes(VALUE_FLUX_OUT, 0);
      Wire.write( b );
      break;
    case EVENT_GET_FLUX_OUT + 1: 
      b = int2Bytes(VALUE_FLUX_OUT, 1);
      Wire.write( b );
      break;


    case EVENT_GET_CC_CURRENT + 0: 
      b = float2Bytes(VALUE_CC, 0);
      Wire.write( b );
      break;
    case EVENT_GET_CC_CURRENT + 1: 
      b = float2Bytes(VALUE_CC, 1);
      Wire.write( b );
      break;
    case EVENT_GET_CC_CURRENT + 2: 
      b = float2Bytes(VALUE_CC, 2);
      Wire.write( b );
      break;
    case EVENT_GET_CC_CURRENT + 3: 
      b = float2Bytes(VALUE_CC, 3);
      Wire.write( b );
      break;

    case EVENT_GET_AC1_CURRENT + 0: 
      b = float2Bytes(VALUE_AC1, 0);
      Wire.write( b );
      break;
    case EVENT_GET_AC1_CURRENT + 1: 
      b = float2Bytes(VALUE_AC1, 1);
      Wire.write( b );
      break;
    case EVENT_GET_AC1_CURRENT + 2: 
      b = float2Bytes(VALUE_AC1, 2);
      Wire.write( b );
      break;
    case EVENT_GET_AC1_CURRENT + 3: 
      b = float2Bytes(VALUE_AC1, 3);
      Wire.write( b );
      break;

    case EVENT_GET_AC2_CURRENT + 0: 
      b = float2Bytes(VALUE_AC2, 0);
      Wire.write( b );
      break;
    case EVENT_GET_AC2_CURRENT + 1: 
      b = float2Bytes(VALUE_AC2, 1);
      Wire.write( b );
      break;
    case EVENT_GET_AC2_CURRENT + 2: 
      b = float2Bytes(VALUE_AC2, 2);
      Wire.write( b );
      break;
    case EVENT_GET_AC2_CURRENT + 3: 
      b = float2Bytes(VALUE_AC2, 3);
      Wire.write( b );
      break;

    
    default:
      Wire.write(0xFF);
      break;
    }
  //Serial.println("Request event OUT: " + event_s);
}



uint8_t float2Bytes(float floatVal, int id){ 
	uint8_t *b = (uint8_t *) &floatVal;
	return b[id];
}

uint8_t int2Bytes(int intVal, int id){ 
	uint8_t *b = (uint8_t *)&intVal;
	return b[id];
}



void interrupt0Handler(){
	int0count++;
}


void interrupt1Handler(){
	int1count++;
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




