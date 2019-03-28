# Devices labels
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
FLUX_IN           =  0x40# FLUXMETER ( digital input, D2 )
FLUX_OUT          =  0x40 # FLUXMETER ( digital input, D3 )
WATER_TEMP        =  0x10 # DS18D20 ( onewire, D5 )
WATER_LEVEL       =  0x50 # DISTANCE ULTRASOUND SENSOR ( software serial, rxD9 txD10 )
PRESSURE_MIDDLE   =  0x28 # PRESSURE (analog, A3)

CC_CURRENT        =  0x10 # SHUNT  ( LM358 gain 20, analog, A0  )
AC1_CURRENT       =  0x20 # SCT013 (analog in A5)
AC2_CURRENT       =  0x24 # SCT013 (analog in A5)
AC3_CURRENT       =  0x28 # n.c.

mcu = dict()

dataTypes = ('INT16': 2, 'FLOAT32': 4 )
INT16   = 2
FLOAT32 = 4

# creare n object apposta ?!?!
class McuData:
	name = ''
	device = ''
	i2cDev = 0x00
	i2cReg = 0x00
`	dataType = ''
	mUnit = 'C'
	dbLabel = '---'

	def __init__(self, name, device, i2cDev, i2cReg, dataType, mUnit, convFormula, dbLabel):
		self.name = name
		self.device = device
		self.i2cDev = i2cDev
		self.i2cReg = i2cReg
		self.dataType = dataType
		self.mUnit = mUnit
		self.convFormula = convFormula
		self.dbLabel = dbLabel


mcu['TEMP_PANEL_1']    = ('Solar panel temperature 1', EXTERNAL, I2C_ADDR_EXTERNAL, TEMP_PANEL_1, INT16, 'C', '1', 'ext_temp1' )
mcu['TEMP_PANEL_2']    = ('Solar panel temperature 2', '', '', '', '', '', '' )
mcu['TEMP_ENV']        = ('', '', '', '', '', '', '' )
mcu['PYRO']            = ('', '', '', '', '', '', '' )
mcu['WIND']            = ('', '', '', '', '', '', '' )

mcu['AIR_IN']          = ('', '', '', '', '', '', '' )
mcu['AIR_OUT']         = ('', '', '', '', '', '', '' )
mcu['AIR_INSIDE']      = ('', '', '', '', '', '', '' )
mcu['FLOODING_STATUS'] = ('', '', '', '', '', '', '' )
mcu['DHT11_AIR']       = ('', '', '', '', '', '', '' )
mcu['DHT11_HUMIDITY']  = ('', '', '', '', '', '', '' )

mcu['PRESSURE_IN']     = ('', '', '', '', '', '', '' )
mcu['PRESSURE_OUT']    = ('', '', '', '', '', '', '' )
mcu['UV']              = ('', '', '', '', '', '', '' )
mcu['FLUX_IN']         = ('', '', '', '', '', '', '' )
mcu['FLUX_OUT']        = ('', '', '', '', '', '', '' )
mcu['WATER_TEMP']      = ('', '', '', '', '', '', '' )
mcu['WATER_LEVEL']     = ('', '', '', '', '', '', '' )
mcu['PRESSURE_MIDDLE'] = ('', '', '', '', '', '', '' )

mcu['CC_CURRENT']      = ('', '', '', '', '', '', '' )
mcu['AC1_CURRENT']     = ('', '', '', '', '', '', '' )
mcu['AC2_CURRENT']     = ('', '', '', '', '', '', '' )
mcu['AC3_CURRENT']     = ('', '', '', '', '', '', '' )

