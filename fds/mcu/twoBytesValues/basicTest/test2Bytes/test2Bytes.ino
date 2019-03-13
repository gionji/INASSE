// Define the ARDUINO station
//#define IS_EXTERNAL 1
//#define IS_INTERNAL 1
//#define IS_HYDRAULIC 1
#define IS_ELECTRIC 1



// Included libraries
#include <Wire.h>
#include <math.h>

#ifdef IS_INTERNAL
#include <DHT.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#endif

#ifdef IS_HYDRAULIC
#include <SoftwareSerial.h>
#include <OneWire.h> 
#include <DallasTemperature.h>
#endif

#ifdef IS_ELECTRIC
#include <EmonLib.h>
#endif


/*
 * Contants
 */
#ifdef IS_ELECTRIC
	#define EMON_CALIB        111.0
	#define EMON_IRMS_CALIB   1480
	#define SCALE_CC          1.0
	#define SCALE_AC1         1.0
	#define SCALE_AC2         1.0
	#define SCALE_AC3         1.0
#endif


/*
 * Define slave I2C
 */
#ifdef IS_EXTERNAL 
	#define I2C_ADDR      0x21 
#elif IS_INTERNAL
	#define I2C_ADDR      0x22 
#elif IS_HYDRAULIC
	#define I2C_ADDR      0x23 
#elif IS_ELECTRIC
	#define I2C_ADDR      0x24 
#endif


/*
 * I2C registers descriptions
 */
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

/*
 * Pin declaration
 */
#ifdef IS_EXTERNAL
	#define PYROMETER_PIN        A0
	#define TEMP_ONE_WIRE_BUS    5 
	#define INTERRUPT_0_PIN      2 
#elif IS_INTERNAL
	#define ONE_WIRE_BUS         5 
	#define DHT11_BUS            6 
	#define FLOOD_PIN            7 
#elif IS_HYDRAULIC
	#define PRESSURE_IN_PIN      A0
	#define PRESSURE_MIDDLE_PIN  A2
	#define PRESSURE_OUT_PIN     A1
	#define UV_PIN               A3
	#define INTERRUPT_0_PIN      2
	#define INTERRUPT_1_PIN      3 
	#define TEMP_ONE_WIRE_BUS    5 
	#define SERIAL_RX_PIN        9
	#define SERIAL_TX_PIN        10
#elif IS_ELECTRIC
	#define CC_OUTPUT_PIN         A0
	#define AC_OUTPUT_1_PIN       A1
	#define AC_OUTPUT_2_PIN       A2
	#define AC_OUTPUT_3_PIN       A3
#endif

/*
 * Output variables
 */
float VALUE_TEMP_PANEL_1       = 0;
float VALUE_TEMP_PANEL_2       = 0;
float VALUE_TEMP_ENV           = 0;
int VALUE_PYRO                 = 0;
int VALUE_WIND                 = 0;

float VALUE_AIR_IN             = 0;
float VALUE_AIR_OUT            = 0;
float VALUE_AIR_INSIDE         = 0;
uint8_t VALUE_FLOODING_STATUS  = 0;
float VALUE_DHT11_AIR          = 0;
float VALUE_DHT11_HUMIDITY     = 0;

float VALUE_PRESSURE_IN        = 0;
float VALUE_PRESSURE_OUT       = 0;
float VALUE_PRESSURE_MIDDLE    = 0;
uint8_t VALUE_UV               = 0;
int   VALUE_FLUX_IN            = 0;
int   VALUE_FLUX_OUT           = 0;
float VALUE_WATER_TEMP         = 0;
int   VALUE_WATER_LEVEL        = 0;

float VALUE_CC                 = 0;
float VALUE_AC1                = 0;
float VALUE_AC2                = 0;
float VALUE_AC3                = 0;

/*
 * Common variables
 */
uint8_t EVENT = 0;


/*
 * Local variables
 */
volatile int int0count = 0, int1count = 0;
 
#ifdef IS_EXTERNAL
	OneWire  ds(TEMP_ONE_WIRE_BUS);
	DallasTemperature sensors(&ds);
	float tempPanel1, tempPanel2, tempEnv;
	int wind, pyro;
 
#elif IS_INTERNAL
	OneWire  ds(ONE_WIRE_BUS);
	DallasTemperature sensors(&ds);
	float airIn, airOut, airInside, dht11air, dht11humidity;
	int isFlooded;
	DHT dht(DHT11_BUS, DHT11);
  
#elif IS_HYDRAULIC
	OneWire  ds(TEMP_ONE_WIRE_BUS);
	DallasTemperature sensors(&ds);
	float waterTemp;
	int pressureIn, pressureOut, pressureMiddle, uv, fluxIn, fluxOut, waterLevel;
	SoftwareSerial DYPSensor(SERIAL_RX_PIN, SERIAL_TX_PIN); // RX, TX
	const int MAX_TRY_SERIAL = 50;
	const int CYCLES = 10;
  
#elif IS_ELECTRIC
	EnergyMonitor acOutput1; 
	EnergyMonitor acOutput2;
	EnergyMonitor acOutput3; 
#endif


/*
 * Setup
 */
void setup() {
	Serial.begin(115200);

	#ifdef IS_EXTERNAL
		attachInterrupt(0, interrupt0Handler, RISING);
		pinMode(INTERRUPT_0_PIN, INPUT);
		sensors.begin();
	#elif IS_INTERNAL
		sensors.begin();
		dht.begin();
	#elif IS_HYDRAULIC
		attachInterrupt(0, interrupt0Handler,  RISING);
		attachInterrupt(1, interrupt1Handler,  RISING);
		pinMode(INTERRUPT_0_PIN, INPUT);
		pinMode(INTERRUPT_1_PIN,  INPUT);
		DYPSensor.begin(9600);
	#elif IS_ELECTRIC
		acOutput1.current(AC_OUTPUT_1_PIN, EMON_CALIB);             
		acOutput2.current(AC_OUTPUT_2_PIN, EMON_CALIB);  
		acOutput3.current(AC_OUTPUT_3_PIN, EMON_CALIB);  
	#endif
  
	// Output pin muxing
	pinMode(13, OUTPUT);

	// I2c slave mode enabling
	Wire.begin(I2C_ADDR);
	Wire.onRequest(requestEvent); // data request to slave
	Wire.onReceive(receiveEvent); // data slave received
}



void loop() {

	#ifdef IS_EXTERNAL  // Interrupts reset
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
		VALUE_TEMP_ENV     = (uint8_t)  (tempEnv    + 128);
		VALUE_WIND         = (uint8_t)  wind; 
		VALUE_PYRO         = (uint8_t)  pyro >> 2; // guadagno LM358?
	#elif IS_INTERNAL
		airIn         = sensors.getTempCByIndex(0);
		airOut        = sensors.getTempCByIndex(1);
		airInside     = sensors.getTempCByIndex(2);
		isFlooded     = digitalRead(FLOOD_PIN);  
		dht11air      = dht.readHumidity();
		dht11humidity = dht.readTemperature();

		VALUE_AIR_IN          = (uint8_t) (airIn + 128);
		VALUE_AIR_OUT         = (uint8_t) (airOut + 128);
		VALUE_AIR_INSIDE      = (uint8_t) (airInside + 128);
		VALUE_FLOODING_STATUS = (uint8_t) isFlooded;
		VALUE_DHT11_AIR       = (uint8_t) (dht11air + 128);
		VALUE_DHT11_HUMIDITY  = (uint8_t) (dht11humidity + 128);
	#elif IS_HYDRAULIC  
		int0count  = 0;
		int1count  = 0;

		sensors.requestTemperatures();

		uv = 0;
		pressureIn  = analogRead(PRESSURE_IN_PIN);
		pressureOut = analogRead(PRESSURE_OUT_PIN);
		pressureMiddle = analogRead(PRESSURE_MIDDLE_PIN);  
		waterLevel = GetDistance();
		waterTemp = sensors.getTempCByIndex(0);

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
	#elif IS_ELECTRIC
		int Icc = analogRead(CC_OUTPUT_PIN);
		double Irms1 = acOutput1.calcIrms(1480);  // Calculate Irms only
		double Irms2 = acOutput2.calcIrms(1480);  // Calculate Irms only
		double Irms3 = acOutput3.calcIrms(1480);  // Calculate Irms only

		if (Irms1 > 254.0) Irms1 = 255;
		if (Irms2 > 254.0) Irms2 = 255;
		if (Irms3 > 254.0) Irms3 = 255;
		if (Icc   > 254.0)   Icc = 255;

		VALUE_CC  = (uint8_t)(Icc   * SCALE_CC );
		VALUE_AC1 = (uint8_t)(Irms1 * SCALE_AC1);
		VALUE_AC2 = (uint8_t)(Irms2 * SCALE_AC2);
		VALUE_AC3 = (uint8_t)(Irms3 * SCALE_AC3);
	#endif


	digitalWrite(13, HIGH);
	delay(10);
	digitalWrite(13, LOW);
	delay(10);

	delay(50);
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

    #ifdef IS_EXTERNAL
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

    #elif IS_INTERNAL
    case EVENT_GET_AIR_IN + 0: 
      b = float2Bytes(VALUE_AIR_IN, 0);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_IN + 1: 
      b = float2Bytes(VALUE_AIR_IN, 1);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_IN + 2: 
      b = float2Bytes(VALUE_AIR_IN, 2);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_IN + 3: 
      b = float2Bytes(VALUE_AIR_IN, 3);
      Wire.write( b );
      break;

    case EVENT_GET_AIR_OUT + 0: 
      b = float2Bytes(VALUE_AIR_OUT, 0);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_OUT + 1: 
      b = float2Bytes(VALUE_AIR_OUT, 1);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_OUT + 2: 
      b = float2Bytes(VALUE_AIR_OUT, 2);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_OUT + 3: 
      b = float2Bytes(VALUE_AIR_OUT, 3);
      Wire.write( b );
      break;

    case EVENT_GET_AIR_INSIDE + 0: 
      b = float2Bytes(VALUE_AIR_INSIDE, 0);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_INSIDE + 1: 
      b = float2Bytes(VALUE_AIR_INSIDE, 1);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_INSIDE + 2: 
      b = float2Bytes(VALUE_AIR_INSIDE, 2);
      Wire.write( b );
      break;
    case EVENT_GET_AIR_INSIDE + 3: 
      b = float2Bytes(VALUE_AIR_INSIDE, 3);
      Wire.write( b );
      break;

    case EVENT_GET_FLOODING_STATUS: 
      Wire.write(VALUE_FLOODING_STATUS);
      break;

    case EVENT_GET_DHT11_AIR + 0: 
      b = float2Bytes(VALUE_DHT11_AIR, 0);
      Wire.write( b );
      break;
    case EVENT_GET_DHT11_AIR + 1: 
      b = float2Bytes(VALUE_DHT11_AIR, 1);
      Wire.write( b );
      break;
    case EVENT_GET_DHT11_AIR + 2: 
      b = float2Bytes(VALUE_DHT11_AIR, 2);
      Wire.write( b );
      break;
    case EVENT_GET_DHT11_AIR + 3: 
      b = float2Bytes(VALUE_DHT11_AIR, 3);
      Wire.write( b );
      break;

    case EVENT_GET_DHT11_HUMIDITY + 0: 
      b = float2Bytes(VALUE_DHT11_HUMIDITY, 0);
      Wire.write( b );
      break;
    case EVENT_GET_DHT11_HUMIDITY + 1: 
      b = float2Bytes(VALUE_DHT11_HUMIDITY, 1);
      Wire.write( b );
      break;
    case EVENT_GET_DHT11_HUMIDITY + 2: 
      b = float2Bytes(VALUE_DHT11_HUMIDITY, 2);
      Wire.write( b );
      break;
    case EVENT_GET_DHT11_HUMIDITY + 3: 
      b = float2Bytes(VALUE_DHT11_HUMIDITY, 3);
      Wire.write( b );
      break;

    #elif IS_HYDRAULIC
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

    case EVENT_GET_UV: 
      Wire.write(VALUE_UV);
      break;
     
    case EVENT_GET_FLUX_IN + 0: 
      b = float2Bytes(VALUE_FLUX_IN, 0);
      Wire.write( b );
      break;
    case EVENT_GET_FLUX_IN + 1: 
      b = float2Bytes(VALUE_FLUX_IN, 1);
      Wire.write( b );
      break;
   
    case EVENT_GET_FLUX_OUT + 0: 
      b = float2Bytes(VALUE_FLUX_OUT, 0);
      Wire.write( b );
      break;
    case EVENT_GET_FLUX_OUT + 1: 
      b = float2Bytes(VALUE_FLUX_OUT, 1);
      Wire.write( b );
      break;

    case EVENT_GET_WATER_TEMP + 0: 
      b = float2Bytes(VALUE_WATER_TEMP, 0);
      Wire.write( b );
      break;
    case EVENT_GET_WATER_TEMP + 1: 
      b = float2Bytes(VALUE_WATER_TEMP, 1);
      Wire.write( b );
      break;
    case EVENT_GET_WATER_TEMP + 2: 
      b = float2Bytes(VALUE_WATER_TEMP, 2);
      Wire.write( b );
      break;
    case EVENT_GET_WATER_TEMP + 3: 
      b = float2Bytes(VALUE_WATER_TEMP, 3);
      Wire.write( b );
      break;

    case EVENT_GET_WATER_LEVEL + 0: 
      b = float2Bytes(VALUE_WATER_LEVEL, 0);
      Wire.write( b );
      break;
    case EVENT_GET_WATER_LEVEL + 1: 
      b = float2Bytes(VALUE_WATER_LEVEL, 1);
      Wire.write( b );
      break;

  #elif IS_ELECTRIC
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

    case EVENT_GET_AC3_CURRENT + 0: 
      b = float2Bytes(VALUE_AC3, 0);
      Wire.write( b );
      break;
    case EVENT_GET_AC3_CURRENT + 1: 
      b = float2Bytes(VALUE_AC3, 1);
      Wire.write( b );
      break;
    case EVENT_GET_AC3_CURRENT + 2: 
      b = float2Bytes(VALUE_AC3, 2);
      Wire.write( b );
      break;
    case EVENT_GET_AC3_CURRENT + 3: 
      b = float2Bytes(VALUE_AC3, 3);
      Wire.write( b );
      break;
    #endif  
    
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



void interrupt0Handler(){
	int0count++;
}


#ifdef IS_HYDRAULIC
void interrupt1Handler(){
	int1count++;
}
#endif

#ifndef IS_ELECTRIC
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
#endif

#ifdef IS_HYDRAULIC
int GetDistance() {
	int mean   = 0;
	int valids = 0;

	for(int i=0; i<CYCLES; i++){
		byte msb, lsb, checksum, checkcalc, tries = 0;
		int distance;

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
}  
#endif


