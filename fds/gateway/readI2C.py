import smbus
import time

bus = smbus.SMBus(3)
addressExternal = 0x21
addressInternal = 0x22
addressIdraulic = 0x23
addressElectric = 0x24

print bus.read_byte_data(addressElectric, 0x40)
print bus.read_byte_data(addressElectric, 0x41)
print bus.read_byte_data(addressElectric, 0x42)
print bus.read_byte_data(addressElectric, 0x43)






