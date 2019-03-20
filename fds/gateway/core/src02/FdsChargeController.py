import 

DEBUG = True

MODBUS_RTU = 0x01
MODBUS_ETH = 0x02

CHARGE_CONTROLLER_UNIT  = 0x01
RELAY_BOX_UNIT          = 0x09
MODBUS_PORT             = 502

DEFAULT_CHARGE_CONTROLLER_IP   = '192.168.0.253'
DEFAULT_C23_RS485              = '/dev/ttymxc2' # mxc3 on schematics

# from pymodbus.client.sync import ModbusTcpClient 


class FdsChargeController():
	comunicationType = ""
	serialPort       = ""
	ipAddress        = ""
	modbusClient     = None

	
	def __init__(self, communicationType, port):

		if (communicationType == MODBUS_ETH):
			self.communicationType = communicationType
			self.ipAddress = port
			if(DEBUG): print("FdsChargeController: ETH enabled ", self.communicationType)
		elif (communicationType == MODBUS_RTU):			
			self.communicationType = communicationType
			self.serialPort = port
			if(DEBUG): print("FdsChargeController: RTU enabled ", self.communicationType)
		else:				
			raise ValueError("Unsupported Modbus Communication Type. Choose MODBUS_RTU or MODBUS_ETH.")
	
	
	def connect(self):
		if(DEBUG): print("FdsChargeController: connect called")
		
		if(communicationType == MODBUS_ETH):
				print("-+--")
		elif (communicationType == MODBUS_RTU):
				print("-+--")	
