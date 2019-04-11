import smbus2
import struct



EXTERNAL  =  'mcu_external'
INTERNAL  =  'mcu_internal'
HYDRAULIC =  'mcu_hydraulic'
ELECTRIC  =  'mcu_electric'

# I2C addressed of Arduinos MCU connected
I2C_ADDR_EXTERNAL =   0x21
I2C_ADDR_INTERNAL =   0x22
I2C_ADDR_HYDRAULIC =  0x23
I2C_ADDR_ELECTRIC =   0x24


TEMP_PANEL_1      =  0x10 # DS18D20 ( onewire, D5 )
TEMP_PANEL_2      =  0x14 # DS18D20 ( onewire, D5 )
TEMP_ENV          =  0x18 # DS18D20 ( onewire, D5 )
PYRO              =  0x20 # PYRANOMETER  ( LM358 gain 20, analog, A0  )
WIND              =  0x30 # WINDMETER  ( LM358 gain 5, digital input, D2)

AIR_IN            =  0x10 # DS18D20 ( onewire, D5 )
AIR_OUT           =  0x14 # DS18D20 ( onewire, D5 )
AIR_INSIDE        =  0x18 # DS18D20 ( onewire, D5 )
FLOODING_STATUS   =  0x20 # Flooding sensor ( digital input, D7 )
DHT11_AIR         =  0x30 # DHT11 ( onewire, D6 )
DHT11_HUMIDITY    =  0x34 # DHT11 ( onewire, D6 )

PRESSURE_IN       =  0x20 # PRESSURE (analog, A1)
PRESSURE_OUT      =  0x24 # PRESSURE (analog, A2)
UV                =  0x30 # n.d.
FLUX_IN           =  0x40 # FLUXMETER ( digital input, D2 )
FLUX_OUT          =  0x40 # FLUXMETER ( digital input, D3 )
WATER_TEMP        =  0x10 # DS18D20 ( onewire, D5 )
WATER_LEVEL       =  0x50 # DISTANCE ULTRASOUND SENSOR ( software serial, rxD9 txD10 )
PRESSURE_MIDDLE   =  0x28 # PRESSURE (analog, A3)

CC_CURRENT        =  0x10 # SHUNT  ( LM358 gain 20, analog, A0  )
AC1_CURRENT       =  0x20 # SCT013 (analog in A5)
AC2_CURRENT       =  0x24 # SCT013 (analog in A5)
AC3_CURRENT       =  0x28 # n.c.



SECO_C23_I2C_BUS    = 1
UDOO_NEO_I2C_BUS    = 3

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


## TODO add try catch raise



	## External MCU
	def getSolarPanelTemperature1(self):
		#print("Requested solar panel temperature 1")
		value = self.read4BytesFloat(I2C_ADDR_EXTERNAL, TEMP_PANEL_1, ARDUINO_FLOAT_SIZE)
		return value

	def getSolarPanelTemperature2(self):
		#print("Requested solar panel temperature 2")
		value = self.read4BytesFloat(I2C_ADDR_EXTERNAL, TEMP_PANEL_2, ARDUINO_FLOAT_SIZE)
		return value

	def getEnvironmentalTemperature(self):
		#print("Requested external temperature")
		value = self.read4BytesFloat(I2C_ADDR_EXTERNAL, TEMP_ENV, ARDUINO_FLOAT_SIZE)
		return value

	def getIrradiation(self):
		#print("Requested solar irradiadion")
		value = self.read2BytesInteger(I2C_ADDR_EXTERNAL, PYRO, ARDUINO_INT_SIZE)
		return value

	def getWindSpeed(self ):
		#print("Requested wind speed")
		value = self.read2BytesInteger(I2C_ADDR_EXTERNAL, WIND, ARDUINO_INT_SIZE)
		return value





	## Internal
	def getInternalTemperature(self):
		#print("Requested internal temperature 1")
		value = self.read4BytesFloat(I2C_ADDR_INTERNAL, AIR_INSIDE, ARDUINO_FLOAT_SIZE)
		return value

	def getIncomingTemperature(self):
		#print("Requested incoming air flow temperature")
		value = self.read4BytesFloat(I2C_ADDR_INTERNAL, AIR_IN, ARDUINO_FLOAT_SIZE)
		return value

	def getOutcomingTemperature(self):
		#print("Requested outcoming air flow temperature")
		value = self.read4BytesFloat(I2C_ADDR_INTERNAL, AIR_OUT, ARDUINO_FLOAT_SIZE)
		return value

	def getFloodStatus(self):
		#print("Requested flooding status")
		value = self.bus.read_byte_data(I2C_ADDR_INTERNAL, FLOODING_STATUS)
		return value

	def getDHT11Temperature(self):
		#print("Requested internal temperature by DHT11")
		value = self.read4BytesFloat(I2C_ADDR_INTERNAL, DHT11_AIR, ARDUINO_FLOAT_SIZE)
		return value

	def getDHT11Humidity(self):
		#print("Requested internal temperature by DHT11")
		value = self.read4BytesFloat(I2C_ADDR_INTERNAL, DHT11_HUMIDITY, ARDUINO_FLOAT_SIZE)
		return value






	## Hydraulic
	def getWaterFluxIn(self):
		#print("Requested water flux in")
		value = self.read2BytesInteger(I2C_ADDR_HYDRAULIC, FLUX_IN, ARDUINO_INT_SIZE)
		return value

	def getWaterFluxOut(self):
		#print("Requested water flux ouy")
		value = self.read2BytesInteger(I2C_ADDR_HYDRAULIC, FLUX_OUT, ARDUINO_INT_SIZE)
		return value

	def getPressureIn(self):
		#print("Requested pressure in input")
		value = self.read4BytesFloat(I2C_ADDR_HYDRAULIC, PRESSURE_IN, ARDUINO_FLOAT_SIZE)
		return value

	def getPressureMiddle(self):
		#print("Requested pressure in middle")
		value = self.read4BytesFloat(I2C_ADDR_HYDRAULIC, PRESSURE_MIDDLE, ARDUINO_FLOAT_SIZE)
		return value

	def getPressureOut(self):
		#print("Requested pressure in output")
		value = self.read4BytesFloat(I2C_ADDR_HYDRAULIC, PRESSURE_OUT, ARDUINO_FLOAT_SIZE)
		return value

	def getWaterTemperature(self):
		#print("Requested water temperature")
		value = self.read4BytesFloat(I2C_ADDR_HYDRAULIC, WATER_TEMP, ARDUINO_FLOAT_SIZE)
		return value

	def getWaterLevel(self):
		#print("Requested tank water level")
		value = self.read2BytesInteger(I2C_ADDR_HYDRAULIC, WATER_LEVEL, ARDUINO_INT_SIZE)
		return value

	def getLampUV(self):
		#print("Requested UV lamp efficency")
		return 1.0



	## Electrical
	def getCcCurrent(self):
		#print("Requested CC current from Shunt")
		value = self.read4BytesFloat(I2C_ADDR_ELECTRIC, CC_CURRENT, ARDUINO_FLOAT_SIZE)
		return value

	def getAcCurrent(self, channel):
		#print("Requested AC current from clamp ", str(channel))

		if channel == 1:
			AC_CURRENT = AC1_CURRENT
		elif channel == 2:
			AC_CURRENT = AC2_CURRENT
		else:
			return -1

		value = self.read4BytesFloat(I2C_ADDR_ELECTRIC, AC_CURRENT, ARDUINO_FLOAT_SIZE)

		return value



	def getMcuData(self, mcuType):
		if mcuType not in (EXTERNAL, INTERNAL, HYDRAULIC, ELECTRIC):
			raise AttributeError("Wrong MCU type ")

		data = {'type': mcuType }

		try:
			if mcuType == EXTERNAL:
				data['ext_temp1']     =   self.getSolarPanelTemperature1()
	                        data['ext_temp2']     =   self.getSolarPanelTemperature2()
	                        data['ext_env']       =   self.getEnvironmentalTemperature( )
	                        data['ext_pyro']      =   self.getIrradiation()
	                        data['ext_wind']      =   self.getWindSpeed()
			elif mcuType == INTERNAL:
	                        data['int_tempIn']    =   self.getIncomingTemperature()
	                        data['int_tempOut']   =   self.getOutcomingTemperature()
	                        data['int_tempInt']   =   self.getInternalTemperature()
	                        data['int_flood']     =   self.getFloodStatus()
	                        data['int_dht11Temp'] =   self.getDHT11Temperature()
	                        data['int_dht11Hum']  =   self.getDHT11Humidity( )
	                elif mcuType == HYDRAULIC:
	                        data['hyd_presIn']    =   self.getPressureIn()
	                        data['hyd_presMid']   =   self.getPressureMiddle( )
	                        data['hyd_presOut']   =   self.getPressureOut()
	                        data['hyd_fluxIn']    =   self.getWaterFluxIn()
				data['hyd_fluxOut']   =   self.getWaterFluxOut()
				data['hyd_waterTemp'] =   self.getWaterTemperature()
				data['hyd_waterLevel']=   self.getWaterLevel()
				data['hyd_uv']        =   self.getLampUV()
	                elif mcuType == ELECTRIC:
				data['ele_cc']        =   self.getCcCurrent()
				data['ele_ac1']       =   self.getAcCurrent(1)
	                        data['ele_ac2']       =   self.getAcCurrent(2)
	                        data['ele_ac3']       =   self.getAcCurrent(3)
		except Exception as e:
			return None
		#	raise IOError('Unable to connect to ' + str(mcuType))


		return data
