import smbus
import time
import fds_i2c as mcus

I2C_CHANNEL = 3
bus = smbus.SMBus(I2C_CHANNEL)

sensorsValues = dict()

sensorsValues['EXTERNAL_TEMP_PANEL_1'] = bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.TEMP_PANEL_1) - 128;
sensorsValues['EXTERNAL_TEMP_PANEL_2'] = bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.TEMP_PANEL_2) - 128;
sensorsValues['EXTERNAL_TEMP_ENV']     = bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.TEMP_ENV) - 128;
sensorsValues['EXTERNAL_PYRO']         = bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.PYRO) * 4;
sensorsValues['EXTERNAL_WIND']         = bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.WIND) 

sensorsValues['INTERNAL_AIR_IN']          = bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.AIR_IN) - 128;
sensorsValues['INTERNAL_AIR_OUT']         = bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.AIR_OUT) - 128;
sensorsValues['INTERNAL_AIR_INSIDE']      = bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.AIR_INSIDE) - 128;
sensorsValues['INTERNAL_FLOODING_STATUS'] = bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.FLOODING_STATUS)

sensorsValues['HYDRAULIC_PRESSURE_IN']  = bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.PRESSURE_IN) * 4
sensorsValues['HYDRAULIC_PRESSURE_OUT'] = bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.PRESSURE_OUT) * 4
sensorsValues['HYDRAULIC_UV']           = bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.UV) * 4
sensorsValues['HYDRAULIC_FLUX_IN']      = bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.FLUX_IN)
sensorsValues['HYDRAULIC_FLUX_OUT']     = bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.FLUX_OUT)
sensorsValues['HYDRAULIC_WATER_TEMP']   = bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.WATER_TEMP) - 128;
sensorsValues['HYDRAULIC_WATER_LEVEL']  = bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.WATER_LEVEL) - 128;

sensorsValues['ELECTIRC_CC_CURRENT']  = bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.CC_CURRENT)
sensorsValues['ELECTIRC_AC1_CURRENT'] = bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.AC1_CURRENT)
sensorsValues['ELECTIRC_AC2_CURRENT'] = bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.AC2_CURRENT)
sensorsValues['ELECTIRC_AC3_CURRENT'] = bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.AC3_CURRENT)


for key, value in sensorValues.items():
	print str(key) + " :  " + str(value)

