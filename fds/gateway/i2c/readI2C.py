import smbus
import time
import fds_i2c as mcus

I2C_CHANNEL = 3
bus = smbus.SMBus(I2C_CHANNEL)

print bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.TEMP_PANEL_1)
print bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.TEMP_PANEL_2)
print bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.TEMP_ENV)
print bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.PYRO)
print bus.read_byte_data(mcus.I2C_ADDR_EXTERNAL, mcus.WIND)

print bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.AIR_IN)
print bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.AIR_OUT)
print bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.AIR_INSIDE)
print bus.read_byte_data(mcus.I2C_ADDR_INTERNAL, mcus.FLOODING_STATUS)

print bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.PRESSURE_IN)
print bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.PRESSURE_OUT)
print bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.UV)
print bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.FLUX_IN)
print bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.FLUX_OUT)
print bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.WATER_TEMP)
print bus.read_byte_data(mcus.I2C_ADDR_IDRAULIC, mcus.WATER_LEVEL)

print bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.CC_CURRENT)
print bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.AC1_CURRENT)
print bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.AC2_CURRENT)
print bus.read_byte_data(mcus.I2C_ADDR_ELECTRIC, mcus.AC3_CURRENT)

