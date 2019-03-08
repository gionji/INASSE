import smbus
import struct



# I2C addressed of Arduinos MCU connected
I2C_ADDR_EXTERNAL =  0x21
I2C_ADDR_INTERNAL =  0x22
I2C_ADDR_IDRAULIC =  0x23
I2C_ADDR_ELECTRIC =  0x24


TEMP_PANEL_1      =  0x10 # DS18D20 ( onewire, D5 )
TEMP_PANEL_2      =  0x11 # DS18D20 ( onewire, D5 )
TEMP_ENV          =  0x12 # DS18D20 ( onewire, D5 )
PYRO              =  0x13 # PYRANOMETER  ( LM358 gain 20, analog, A0  )
WIND              =  0x14 # WINDMETER  ( LM358 gain 5, digital input, D2)

AIR_IN            =  0x20 # DS18D20 ( onewire, D5 )
AIR_OUT           =  0x21 # DS18D20 ( onewire, D5 )
AIR_INSIDE        =  0x22 # DS18D20 ( onewire, D5 )
FLOODING_STATUS   =  0x23 # Flooding sensor ( digital input, D7 )
DHT11_AIR         =  0x24 # DHT11 ( onewire, D6 )
DHT11_HUMIDITY    =  0x25 # DHT11 ( onewire, D6 )

PRESSURE_IN       =  0x30 # PRESSURE (analog, A1)
PRESSURE_OUT      =  0x31 # PRESSURE (analog, A2)
UV                =  0x32 # n.d.
FLUX_IN           =  0x33 # FLUXMETER ( digital input, D2 )
FLUX_OUT          =  0x34 # FLUXMETER ( digital input, D3 )
WATER_TEMP        =  0x35 # DS18D20 ( onewire, D5 )
WATER_LEVEL       =  0x36 # DISTANCE ULTRASOUND SENSOR ( software serial, rxD9 txD10 )
PRESSURE_MIDDLE   =  0x37 # PRESSURE (analog, A3)

CC_CURRENT        =  0x40 # SHUNT  ( LM358 gain 20, analog, A0  )
AC1_CURRENT       =  0x41 # SCT013 (analog in A5)
AC2_CURRENT       =  0x42 # SCT013 (analog in A5)
AC3_CURRENT       =  0x43 # n.c.


SECO_C23_I2C_BUS = 1
UDOO_NEO_I2C_BUS = 3
ARDUINO_FLOAT_SIZE = 2
ARDUINO_DOUBLE_SIZE = 4


SENSORS_BUS = SECO_C23_I2C_BUS


class FsdSensor:
	bus = None

	def __init__(self):
		print("Called FdsSensor default constructor")
		self.bus = smbus.SMBus(SENSORS_BUS) 
		
		
		
	def isConnected(self, arduinoAddress):
		print("Arduino ", str(arduinoAddress), " isConnected")
		return True
		
		
		
	## External MCU
	def getSolarPanelTemperature1(self):		
		print("Requested solar panel temperature 1")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, TEMP_PANEL_1)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, TEMP_PANEL_1, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) #### ??
		
		return value
		
		
		
	def getSolarPanelTemperature2(self):		
		print("Requested solar panel temperature 2")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, TEMP_PANEL_2)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, TEMP_PANEL_2, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) #### ??
		
		return value
		
		
		
	def getEnvTemperature(self):		
		print("Requested external temperature")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, TEMP_ENV)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, TEMP_ENV, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) #### ??
		
		return value
		
		
		
	def getIrradiation(self):		
		print("Requested solar irradiadion")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, PYRO)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, PYRO, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>i', b) #### ??
		
		return value
		
		
		
		
	def getWindSpeed(self):		
		print("Requested wind speed")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, WIND)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, WIND, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 * 4
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>i', b) 
		
		return value
		
		
		
	
	## Internal
	def getInternalTemperature(self):		
		print("Requested internal temperature 1")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, AIR_INSIDE)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, AIR_INSIDE, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
		
		
	def getIncomingTemperature(self):		
		print("Requested incoming air flow temperature")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, AIR_IN)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, AIR_IN, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
		
		
	def getOutcomingTemperature(self):		
		print("Requested outcoming air flow temperature")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, AIR_OUT)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, AIR_OUT, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
		
		
	def getFloodStatus(self):
		print("Requested flooding status")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, FLOODING_STATUS)
		
		# 1 byte value
		value = value_uint8
		
		return value
		
		
	def getDHT11Temperature(self):		
		print("Requested internal temperature by DHT11")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, DHT11_AIR)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, DHT11_AIR, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
				
		
	def getDHT11Humidity(self):		
		print("Requested internal humidity by DHT11")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, DHT11_HUMIDITY)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, DHT11_HUMIDITY, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
		
		
		
		
	## Hydraulic
	def getWaterFluxIn(self):		
		print("Requested water flux in")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, FLUX_IN)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, FLUX_IN, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>i', b) 
		
		return value
		
		
	def getWaterFluxOut(self):		
		print("Requested pressure in output")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, FLUX_OUT)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, FLUX_OUT, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>i', b) 
		
		return value
			
		
	def getPressureIn(self):		
		print("Requested pressure in input")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, PRESSURE_IN)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, PRESSURE_IN, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 * 4
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
		
	def getPressureMiddle(self):		
		print("Requested pressure in middle")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, PRESSURE_MIDDLE)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, PRESSURE_MIDDLE, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 * 4
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
				
	def getPressureOut(self):		
		print("Requested pressure in output")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, PRESSURE_OUT)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, PRESSURE_OUT, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 * 4
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
			
	def getWaterTemperature(self):		
		print("Requested water temperature")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, WATER_TEMP)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, WATER_TEMP, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8 - 128
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
		
				
	def getWaterLevel(self):		
		print("Requested tank water level")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, WATER_LEVEL)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, WATER_LEVEL, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8
		# 2 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>f', b) 
		
		return value
			
		
	def getLampUV(self):		
		print("Requested UV lamp efficency")
		# get MCU data with smbus
		# scale it (1 or 2 byte version)
		return 1.0
	
	
	
	## Electrical
	def getCCcurrent(self):		
		print("Requested CC current from Shunt")
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, CC_CURRENT)
		value_float16 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, CC_CURRENT, ARDUINO_FLOAT_SIZE)
		
		# 1 byte value
		value = value_uint8
		# 4 bytes float value
		b = struct.pack('2B', * value_float16)
		value = struct.unpack('>i', b) 
		
		return value
		
			
	def getACCurrent(self, channel):		
		print("Requested AC current from clamp ", str(channel))
		
		if channel == 1:
			AC_CURRENT = AC1_CURRENT
		elif channel == 2:
			AC_CURRENT = AC2_CURRENT
		else:
			return -1
		
		# get MCU data with smbus
		value_uint8        = self.bus.read_byte_data(I2C_ADDR_EXTERNAL, AC_CURRENT)
		value_double32 = self.bus.read_i2c_block_data(I2C_ADDR_EXTERNAL, AC_CURRENT, ARDUINO_DOUBLE_SIZE)
		
		# 1 byte value
		value = value_uint8
		# 4 bytes float value
		b = struct.pack('4B', * value_double32)
		value = struct.unpack('>i', b) 
		
		return value
	
	
		
	
	
