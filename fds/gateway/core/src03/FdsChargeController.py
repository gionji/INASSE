from pymodbus.exceptions import ModbusIOException
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

import random
import logging

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
	isDebug          = False

	client = None

	def __init__(self,
		communicationType,
		port=DEFAULT_C23_RS485,
		ipAddress=DEFAULT_CHARGE_CONTROLLER_IP,
		isDebug=False):

		self.isDebug = isDebug

		if (communicationType == MODBUS_ETH):
			self.communicationType = communicationType
			self.ipAddress = ipAddress
			logging.debug("FdsChargeController: ETH enabled ")
		elif (communicationType == MODBUS_RTU):
			self.communicationType = communicationType
			self.serialPort = port
			logging.debug("FdsChargeController: RTU enabled ")
		else:
			raise ValueError("Unsupported Modbus Communication Type. Choose MODBUS_RTU or MODBUS_ETH.")


	def connect(self):
		if(self.communicationType == MODBUS_ETH):
			logging.debug("FdsChargeController: connect EHT called")

			if self.isDebug == False:
			    	print "Trying to connect to Modbus IP Host %s ..." % host
			    	self.client = ModbusClient(self.ipAddress, MODBUS_PORT)
			    	self.client.connect()
		
		elif (self.communicationType == MODBUS_RTU):
                        logging.debug("FdsChargeController: connect RTU called")



	def getChargeControllerData(self):
		data = {'type':'chargecontroller'}

		if self.client != None:
			try:
				# read registers. Start at 0 for convenience
				rr = client.read_holding_registers(0,80, unit=CHARGE_CONTROLLER_UNIT)

				# for all indexes, subtract 1 from what's in the manual
				V_PU_hi = rr.registers[0]
				V_PU_lo = rr.registers[1]
				I_PU_hi = rr.registers[2]
				I_PU_lo = rr.registers[3]

				V_PU = float(V_PU_hi) + float(V_PU_lo)
				I_PU = float(I_PU_hi) + float(I_PU_lo)

				v_scale = V_PU * 2**(-15)
				i_scale = I_PU * 2**(-15)
				p_scale = V_PU * I_PU * 2**(-17)

				# battery sense voltage, filtered
				data["battsV"]       = rr.registers[24] * v_scale
				data["battsSensedV"] = rr.registers[26] * v_scale
				data["battsI"]       = rr.registers[28] * i_scale
				data["arrayV"]       = rr.registers[27] * v_scale
				data["arrayI"]       = rr.registers[29] * i_scale
				data["statenum"]     = rr.registers[50]
				data["hsTemp"]       = rr.registers[35]
				data["rtsTemp"]      = rr.registers[36]
				data["outPower"]     = rr.registers[58] * p_scale
				data["inPower"]      = rr.registers[59] * p_scale
				data["minVb_daily"]  = rr.registers[64] * v_scale
				data["maxVb_daily"]  = rr.registers[65] * v_scale
				data["minTb_daily"]  = rr.registers[71]
				data["maxTb_daily"]  = rr.registers[72]
				data["dipswitches"]  = bin(rr.registers[48])[::-1][:-2].zfill(8)
				#led_state            = rr.registers
			except ModbusIOException as e:
				logging.error('Charge Controller: modbusIOException')
				raise e
			except Exception as e:
				logging.error('Charge Controller: unpredicted exception')
				raise e
		else:
			data["battsV"]       = random.uniform(0, 60)
			data["battsSensedV"] = random.uniform(0, 60)
			data["battsI"]       = random.uniform(0, 60)
			data["arrayV"]       = random.uniform(0, 60)
			data["arrayI"]       = random.uniform(0, 60)
			data["statenum"]     = random.randint(1, 10)
			data["hsTemp"]       = random.uniform(0, 60)
			data["rtsTemp"]      = random.uniform(0, 60)
			data["outPower"]     = random.uniform(0, 60)
			data["inPower"]      = random.uniform(0, 60)
			data["minVb_daily"]  = random.uniform(0, 60)
			data["maxVb_daily"]  = random.uniform(0, 60)
			data["minTb_daily"]  = random.uniform(0, 60)
			data["maxTb_daily"]  = random.uniform(0, 60)
			data["dipswitches"]  = bin(0x02)[::-1][:-2].zfill(8)

		return data



	def getRelayBoxData(self):
		data = {'type':'relaybox'}

		if self.client != None:
			try:
				# read registers. Start at 0 for convenience
				rr = client.read_holding_registers(0,18, unit=RELAYBOX_UNIT)
				v_scale = float(78.421 * 2**(-15))

				data["adc_vb"]        = rr.registers[0] * v_scale
				data["adc_vch_1"]     = rr.registers[1] * v_scale
				data["adc_vch_2"]     = rr.registers[2] * v_scale
				data["adc_vch_3"]     = rr.registers[3] * v_scale
				data["adc_vch_4"]     = rr.registers[4] * v_scale
				data["t_mod"]         = rr.registers[5]
				data["global_faults"] = rr.registers[6]
				data["global_alarms"] = rr.registers[7]
				data["hourmeter_HI"]  = rr.registers[8]
				data["hourmeter_LO"]  = rr.registers[9]
				data["ch_faults_1"]   = rr.registers[10]
				data["ch_faults_2"]   = rr.registers[11]
				data["ch_faults_3"]   = rr.registers[12]
				data["ch_faults_4"]   = rr.registers[13]
				data["ch_alarms_1"]   = rr.registers[14]
				data["ch_alarms_2"]   = rr.registers[15]
				data["ch_alarms_3"]   = rr.registers[16]
				data["ch_alarms_4"]   = rr.registers[17]
			except ModbusIOException as e:
				logging.error('RelayBoxRead: modbusIOException')
				raise e
			except Exception as e:
				logging.error('RelayBoxRead: unpredicted exception')
				raise e

		else:
			data["adc_vb"]        = random.uniform(0, 60)
			data["adc_vch_1"]     = random.uniform(0, 60)
			data["adc_vch_2"]     = random.uniform(0, 60)
			data["adc_vch_3"]     = random.uniform(0, 60)
			data["adc_vch_4"]     = random.uniform(0, 60)
			data["t_mod"]         = random.uniform(0, 60)
			data["global_faults"] = random.randint(0, 60)
			data["global_alarms"] = random.randint(0, 60)
			data["hourmeter_HI"]  = random.uniform(0, 60)
			data["hourmeter_LO"]  = random.uniform(0, 60)
			data["ch_faults_1"]   = random.randint(0, 60)
			data["ch_faults_2"]   = random.randint(0, 60)
			data["ch_faults_3"]   = random.randint(0, 60)
			data["ch_faults_4"]   = random.randint(0, 60)
			data["ch_alarms_1"]   = random.randint(0, 60)
			data["ch_alarms_2"]   = random.randint(0, 60)
			data["ch_alarms_3"]   = random.randint(0, 60)
			data["ch_alarms_4"]   = random.randint(0, 60)
		return data



	def getRelayBoxState(self):
		data = {'type':'relayState'}
		if self.client != None:
			try:
				rr = client.read_coils(0, 8, unit=RELAYBOX_UNIT)
				data["relay_1"]   = rr.bits[0]
				data["relay_2"]   = rr.bits[1]
				data["relay_3"]   = rr.bits[2]
				data["relay_4"]   = rr.bits[3]
				data["relay_5"]   = rr.bits[4]
				data["relay_6"]   = rr.bits[5]
				data["relay_7"]   = rr.bits[6]
				data["relay_8"]   = rr.bits[7]
			except ModbusIOException as e:
				logging.error( 'RelayState: modbusIOException')
				raise e
			except Exception as e:
				logging.error('RelayState: unpredicted exception')
				raise
		else:
			data["relay_1"]   = 0x1
			data["relay_2"]   = 0x1
			data["relay_3"]   = 0x1
			data["relay_4"]   = 0x0
			data["relay_5"]   = 0x0
			data["relay_6"]   = 0x0
			data["relay_7"]   = 0x0
			data["relay_8"]   = 0x0
		return data
