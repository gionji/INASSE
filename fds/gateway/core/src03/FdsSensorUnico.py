import smbus2
import struct
import logging

# I2C addressed of Arduinos MCU connected
I2C_ADDR                  =   0x27

TEMP_1_REGISTER           =  0x10 # DS18D20 ( onewire, D5 )
TEMP_2_REGISTER           =  0x14 # DS18D20 ( onewire, D5 )
TEMP_3_REGISTER           =  0x18 # DS18D20 ( onewire, D5 )
PRESSURE_IN_REGISTER      =  0x20 # PRESSURE (analog, A1)
PRESSURE_OUT_REGISTER     =  0x24 # PRESSURE (analog, A2)
PRESSURE_MIDDLE_REGISTER  =  0x28 # PRESSURE (analog, A3)
FLUX_IN_REGISTER          =  0x30 # FLUXMETER ( digital input, D2 )
FLUX_OUT_REGISTER         =  0x34 # FLUXMETER ( digital input, D3 )
CC_CURRENT_REGISTER       =  0x40 # SHUNT  ( LM358 gain 20, analog, A0  )
AC1_CURRENT_REGISTER      =  0x40 # SCT013 (analog in A5)
AC2_CURRENT_REGISTER      =  0x44 # SCT013 (analog in A5)
DHT11_AIR_REGISTER        =  0x50 # DHT11 ( onewire, D6 )
DHT11_HUMIDITY_REGISTER   =  0x54 # DHT11 ( onewire, D6 )
FLOODING_STATUS_REGISTER  =  0x60 # Flooding sensor ( digital input, D7 )
WATER_LEVEL_REGISTER      =  0x70 # DISTANCE ULTRASOUND SENSOR ( software serial, rxD9 txD10 )


TEMP_1_LABEL           =  'temp1' # DS18D20 ( onewire, D5 )
TEMP_2_LABEL           =  'temp2' # DS18D20 ( onewire, D5 )
TEMP_3_LABEL           =  'temp3' # DS18D20 ( onewire, D5 )
PRESSURE_IN_LABEL      =  'pres1' # PRESSURE (analog, A1)
PRESSURE_OUT_LABEL     =  'pres2' # PRESSURE (analog, A2)
PRESSURE_MIDDLE_LABEL  =  'pres3' # PRESSURE (analog, A3)
FLUX_IN_LABEL          =  'flux1' # FLUXMETER ( digital input, D2 )
FLUX_OUT_LABEL         =  'flux2' # FLUXMETER ( digital input, D3 )
CC_CURRENT_LABEL       =  'cc' # SHUNT  ( LM358 gain 20, analog, A0  )
AC1_CURRENT_LABEL      =  'ac1' # SCT013 (analog in A5)
AC2_CURRENT_LABEL      =  'ac2' # SCT013 (analog in A5)
DHT11_AIR_LABEL        =  'dht_temp'# DHT11 ( onewire, D6 )
DHT11_HUMIDITY_LABEL   =  'dht_hum' # DHT11 ( onewire, D6 )
FLOODING_STATUS_LABEL  =  'flood' # Flooding sensor ( digital input, D7 )
WATER_LEVEL_LABEL      =  'water_lev' # DISTANCE ULTRASOUND SENSOR ( software serial,


# i2c bus number depending on the hardware
SECO_C23_I2C_BUS    = 1
UDOO_NEO_I2C_BUS    = 3

# data sizes
ARDUINO_FLOAT_SIZE  = 4
ARDUINO_INT_SIZE    = 2
ARDUINO_DOUBLE_SIZE = 8


SENSORS_BUS = UDOO_NEO_I2C_BUS


class FdsSensor():
	bus = None

	def __init__(self):
		#print("Called FdsSensor default constructor")
		self.bus = smbus2.SMBus(SENSORS_BUS)

	def __init__(self, busId):
		#print("Called FdsSensor default constructor")
		self.bus = smbus2.SMBus(busId)



	def isConnected(self, arduinoAddress):
		#print("Arduino ", str(arduinoAddress), " isConnected")
		return True



	def read4BytesFloat(self, dev, startReg, nbytes):
		value = [0,0,0,0]

		value[0] = self.bus.read_byte_data(dev, startReg)
		value[1] = self.bus.read_byte_data(dev, startReg+1)
		value[2] = self.bus.read_byte_data(dev, startReg+2)
		value[3] = self.bus.read_byte_data(dev, startReg+3)

		b = struct.pack('4B', * value)
		value = struct.unpack('<f', b)

		return value[0]

	def read2BytesInteger(self, dev, startReg, nbytes):
		value = [0,0]

		value[0] = self.bus.read_byte_data(dev, startReg)
		value[1] = self.bus.read_byte_data(dev, startReg+1)

		b = struct.pack('BB', value[0], value[1])
		value = struct.unpack('<h', b )

		return value[0]

	def read1ByteBoolean(self, dev, startReg):
		value = self.bus.read_byte_data(dev, startReg)
		return value


## TODO add try catch raise

	## External MCU
	def getTemperature1(self):
		logging.debug("Requested temperature 1")
		value = self.read4BytesFloat(I2C_ADDR, TEMP_1_REGISTER, ARDUINO_FLOAT_SIZE)
		return value

	## External MCU
	def getTemperature2(self):
		logging.debug("Requested temperature 2")
		value = self.read4BytesFloat(I2C_ADDR, TEMP_2_REGISTER, ARDUINO_FLOAT_SIZE)
		return value

	## External MCU
	def getTemperature3(self):
		logging.debug("Requested temperature 2")
		value = self.read4BytesFloat(I2C_ADDR, TEMP_3_REGISTER, ARDUINO_FLOAT_SIZE)
		return value


	def getPressureIn(self):
		logging.debug("Requested pressure in input")
		value = self.read4BytesFloat(I2C_ADDR, PRESSURE_IN_REGISTER, ARDUINO_FLOAT_SIZE)
		return value

	def getPressureMiddle(self):
		logging.debug("Requested pressure in middle")
		value = self.read4BytesFloat(I2C_ADDR, PRESSURE_MIDDLE_REGISTER, ARDUINO_FLOAT_SIZE)
		return value

	def getPressureOut(self):
		logging.debug("Requested pressure in output")
		value = self.read4BytesFloat(I2C_ADDR, PRESSURE_OUT_REGISTER, ARDUINO_FLOAT_SIZE)
		return value


	def getWaterFluxIn(self):
		logging.debug("Requested water flux in")
		value = self.read2BytesInteger(I2C_ADDR, FLUX_IN_REGISTER, ARDUINO_INT_SIZE)
		return value

	def getWaterFluxOut(self):
		logging.debug("Requested water flux ouy")
		value = self.read2BytesInteger(I2C_ADDR, FLUX_OUT_REGISTER, ARDUINO_INT_SIZE)
		return value


	def getCcCurrent(self):
		logging.debug("Requested CC current from Shunt")
		value = self.read4BytesFloat(I2C_ADDR, CC_CURRENT_REGISTER, ARDUINO_FLOAT_SIZE)
		return value


	def getAcCurrent(self, channel):
		logging.debug("Requested AC current from clamp ", str(channel))

		if channel == 1:
			AC_CURRENT = AC1_CURRENT
		elif channel == 2:
			AC_CURRENT = AC2_CURRENT
		else:
			return -1

		value = self.read4BytesFloat(I2C_ADDR, AC_CURRENT_REGISTER, ARDUINO_FLOAT_SIZE)

		return value


	def getDHT11Temperature(self):
		logging.debug("Requested internal temperature by DHT11")
		value = self.read4BytesFloat(I2C_ADDR, DHT11_AIRT_REGISTER, ARDUINO_FLOAT_SIZE)
		return value

	def getDHT11Humidity(self):
		logging.debug("Requested internal temperature by DHT11")
		value = self.read4BytesFloat(I2C_ADDR, DHT11_HUMIDITY_REGISTER, ARDUINO_FLOAT_SIZE)
		return value


	def getFloodStatus(self):
		logging.debug("Requested flooding status")
		value = self.read1ByteBoolean(I2C_ADDR, FLOODING_STATUS_REGISTER)
		return value

	def getWaterLevel(self):
		logging.debug("Requested tank water level")
		value = self.read2BytesInteger(I2C_ADDR, WATER_LEVEL_REGISTER, ARDUINO_INT_SIZE)
		return value




	def getMcuData(self):
		try:
			data[ TEMP_1_LABEL ]          =   self.getTemperature1()
            data[ TEMP_2_LABEL ]          =   self.getTemperature2()
            data[ PRESSURE_IN_LABEL ]     =   self.getPressureIn()
            data[ PRESSURE_OUT_LABEL ]    =   self.getPressureMiddle()
            data[ PRESSURE_MIDDLE_LABEL ] =   self.getPressureOut()
            data[ FLUX_IN_LABEL ]         =   self.getWaterFluxIn()
			data[ FLUX_OUT_LABEL ]        =   self.getWaterFluxOut()
			data[ CC_LABEL ]              =   self.getCcCurrent()
			data[ AC1_LABEL ]             =   self.getAcCurrent(1)
            data[ AC1_LABEL ]             =   self.getAcCurrent(2)
		except Exception as e:
			return None
		#	raise IOError('Unable to connect to ' + str(mcuType))
		return data
