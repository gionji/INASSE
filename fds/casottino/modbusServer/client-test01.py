import pymodbus
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

IP_ADDRESS = '192.168.1.193'

client = ModbusClient(IP_ADDRESS , 5020)
a = client.read_input_registers(0,20)
print( a.registers )
