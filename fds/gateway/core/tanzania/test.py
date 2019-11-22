import logging
import sqlite3
import time
import sys
import requests
import json
import os
import eventlet
#eventlet.monkey_patch()

from argparse import ArgumentParser

sys.dont_write_bytecode = True

import FdsChargeController as FdsCC
import FdsSensorUnico	  as FdsSS
import FdsDbConstants	  as FdsDB

import FdsCommon as fds

from losantmqtt import Device

# lo uso per test sul cartone, visto che ora gli schetch sono quelli vecchi a 4 MCU
#import FdsSensorUnico4mcu  as FdsSS4Mcu
IS_RUNNING = True
IS_PAUSED = False

REMOTE_SERVER_URL = None
DATABASE = None
BOARD_ID = None
REMOTE_SYNC_TIMEOUT = None

############# DEFAULTS ####################################
DEFAULT_MODBUS_IP = '192.168.2.253'
DEFAULT_READ_CYCLES_BEFORE_SYNC = 6
DEFAULT_DELAY_BETWEEN_READINGS  = 10.0

DEFAULT_MCU_MAX_ATTEMPTS        = 10
DEFAULT_REMOTE_SYNC_TIMEOUT     = 60

DEFAULT_RESET_GPIO_NEO          = 39
DEFAULT_RESET_GPIO_C23          = 149

DEFAULT_REMOTE_SERVER_IP = None
DEFAULT_DATABASE_PATH_C23 = '/www/'
DEFAULT_DATABASE_PATH_NEO = './'
DEFAULT_REMOTE_SERVER_URL = 'http://ec2-54-214-112-214.us-west-2.compute.amazonaws.com'


################ LOSANT ####################################

DEVICE_ID     = '5dd3b9ee9285680007ea7a76'
ACCESS_KEY    = '9a517ec4-8ad0-4f55-bd76-251d52aa3c87'
ACCESS_SECRET = '6ea5f8f4ce682619feb8007ec4a6b8ddc679453ceb64642b4acea757fcdd645b'

############################################################



def createDbTables( dbConnection ):
	# get te cursor
	cur = dbConnection.cursor()

	print("Accessing db tables and creating if not exists ...")

	if cur is not None:
		cur.execute(FdsDB.sql_create_charge_controller_table)
		cur.execute(FdsDB.sql_create_relaybox_table)
		cur.execute(FdsDB.sql_create_relay_state_table)
		cur.execute(FdsDB.sql_create_mcu_table)
	else:
		print("DB TABLES CREATION: Error! cannot create the database connection.")



def saveDataToDb(dbConnection, *args):
	# get te cursor
	cur = dbConnection.cursor()

	for count, thing in enumerate(args):
		if thing == None:
			break

		data = dict(thing)
		if data['type'] ==  'relayState':
			cur.execute(FdsDB.insert_relay_state, data)
		elif data['type'] ==  'mcu':
			cur.execute(FdsDB.insert_mcu, data)
		elif data['type'] ==  'relaybox':
			cur.execute(FdsDB.insert_relay_box, data)
		elif data['type'] ==  'chargecontroller':
			cur.execute(FdsDB.insert_charge_controller, data)

	# commit data
	dbConnection.commit()





def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d


def sendRequestToServer(server, table_name, data, timeout):

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	payload = json.dumps(data)

	timer = eventlet.Timeout(timeout, Exception("Timeout exception syncing table " + table_name) )

	try:
		r = requests.post(server + str(table_name),
				data=payload,
				headers=headers)
	finally:
		timer.cancel()

	response = r.content
	# print response

	return r



def printLocalDbTables(dbName):
	# connect to the SQlite databases
	connection = sqlite3.connect( dbName )
	connection.row_factory = dict_factory

	cursor = connection.cursor()

	# select all the tables from the database
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()

	tables_jsons = dict()
	# for each of the bables , select all the records from the table
	for table_name in tables:
		# tablName = table_name[0]['name']
		logging.debug('Exporting ' + str(table_name['name']) + ' to json')

		conn = sqlite3.connect( dbName )
		conn.row_factory = dict_factory

		cur1 = conn.cursor()
		cur1.execute("SELECT timestamp, synced FROM "+table_name['name']+ " where synced == 0")
		results = cur1.fetchall()

		print(results)



def getDbTablesJson(dbName, boardId):
	# connect to the SQlite databases
	connection = sqlite3.connect( dbName )
	connection.row_factory = dict_factory

	cursor = connection.cursor()

	# select all the tables from the database
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()

	tables_jsons = dict()

	# for each of the bables , select all the records from the table
	for table_name in tables:
		# tableName = table_name[0]['name']

		logging.debug('Exporting ' + str(table_name['name']) + ' to json')

		conn = sqlite3.connect( dbName )
		conn.row_factory = dict_factory

		cur1 = conn.cursor()
		cur1.execute("SELECT * FROM "+table_name['name']+ " where synced == 0")
		results = cur1.fetchall()

		data_json = format(results).replace(" u'", "'").replace("'", "\"")
		#print "Number of records in the table " + table_name['name'] + ": "+ str(len(results))

		## TODO add the board id in the json
		data_json = "{\"boardId\": \""+ boardId +"\",\"data\": " + data_json + "}"

		tables_jsons[ table_name['name'] ] = data_json

	connection.close()

	return tables_jsons


def markAsSynced(dbName, tableName):
		conn = sqlite3.connect( dbName )
		cur1 = conn.cursor()
		sync_query = "UPDATE "+ tableName + " SET "+ "synced = 1" # WHERE synced == 0"
		cur1.execute( sync_query )
		print("Tryng to mark as sync : " + sync_query)

		cur1.execute("SELECT timestamp, synced FROM " + tableName + " where synced == 0")
		results = cur1.fetchall()
		print("Unsynced elements: " + str(len(results)))
		conn.commit()
		conn.close()


def syncronizeDb(remoteServerAddress, dbName, boardId, timeout):
		json_tables = getDbTablesJson(dbName, boardId)

		for tableName, tableData in json_tables.items():
			print("\nSynching table " + tableName)
			try:
				r = sendRequestToServer(remoteServerAddress, tableName, tableData, timeout=timeout )
				markAsSynced(dbName, tableName)
			except Exception as e:
				print("Error sync DB:" + str( e ))

		print("Syncronize complete")


def resetMcu(boardType, resetPin):

	if (boardType == "NEO"):
		gpios = [
			"178", "179", "104", "143", "142", "141", "140", "149", "105", "148",
			"146", "147", "100", "102", "102", "106", "106", "107", "180", "181",
			"172", "173", "182", "124",  "25",  "22",  "14",  "15",  "16",  "17",
			"18",   "19",  "20",  "21", "203", "202", "177", "176", "175", "174",
			"119", "124", "127", "116",   "7",   "6",   "5",   "4"]

		gpio = gpios[resetPin]

		try:
			with open("/sys/class/gpio/gpio" + gpio + "/direction", "w") as re:
				re.write("out")
			with open("/sys/class/gpio/gpio" + gpio + "/value", "w") as writes:
				writes.write("0")
				time.sleep(1.0)
				writes.write("1")
				time.sleep(1.0)
		except Exception as e:
				print(e)

	# for C23 we use PWM
	elif boardType == "C23":
		try:
			with open("/sys/class/pwm/pwmchip4/export", "w") as pwm:
				pwm.write("0")
		except Exception as e:
			print(e)

		try:
			with open("/sys/class/pwm/pwmchip4/pwm0/period", "w") as pwm:
				pwm.write("100")
		except Exception as e:
			print(e)

		try:
			with open("/sys/class/pwm/pwmchip4/pwm0/duty_cycle", "w") as pwm:
				pwm.write("100")
		except Exception as e:
			print(e)

		try:
			with open("/sys/class/pwm/pwmchip4/pwm0/enable", "w") as pwm:
				pwm.write("0")
				pwm.flush()
				time.sleep(1.0)
				pwm.write("1")
				pwm.flush()
		except Exception as e:
			print(e)



def printData(name, data):
	if data != None:
		print("\n" + name)
		for key, value in data.items():
			print(str(key) + " : " + str(value))
		print('\n')


def getBoardId():
	try:
		with open("/sys/fsl_otp/HW_OCOTP_CFG0", "r") as reader:
			id0 = reader.read()
		with open("/sys/fsl_otp/HW_OCOTP_CFG1", "r") as reader:
			id1 = reader.read()

		id = "fds-" + str(id1[2:10]) + str(id0[2:10])
	except Exception as e:
		print(e)
		id = "fds-unknown"

	return id


def processCommand(inputFile):
	with open(str(inputFile), 'r+') as file:  # Use file to refer to the file object
		line = file.read()
		file.truncate(0)
		file.flush()

		global IS_RUNNING, IS_PAUSED

		if 'pause' in line:
			IS_PAUSED = True
			print('SYSTEM PAUSED')
		if 'restart' in line:
			IS_PAUSED = False
			print('SYSTEM RESTART')
		if 'quit' in line:
			IS_RUNNING = False
		if 'remote-sync' in line:
			print("Manually request remote sync")
			syncronizeDb( REMOTE_SERVER_URL, DATABASE, BOARD_ID, REMOTE_SYNC_TIMEOUT )




def saveDataToTelemetryFile(path, dataCC, dataRB, dataRS, dataMCU):

	with open(path + 'charge_controller/data', 'w+') as fp:
		json.dump(dataCC, fp)

	with open(path + 'relay_box/data', 'w+') as fp:
		json.dump(dataRB, fp)

	with open(path + 'relay_status/data', 'w+') as fp:
		json.dump(dataRS, fp)

	with open(path + 'mcu/data', 'w+') as fp:
		json.dump(dataMCU, fp)


def saveErrorToTelemetryFile(path, error):
	with open(path + 'errors/data', 'w+') as fp:
		json.dump(error, fp)


def printInit():
	print('Inasse. ....')


def parseParameters():
	print('parse parameters ...')


def sendDeviceStateToLosant( device, json_state ):
	print("Sending Device State")
	device.send_state( json_state )


def main():
	print("INASSE OfGridBox v0.5 - tanzania")

	CWD = os.getcwd()

	DATABASE_PATH      = '/www/'
	TELEMETRY_PATH     = CWD + '/syntetics/'
	COMMAND_INPUT_FILE = CWD + '/fdscmd'

	parser = ArgumentParser()

	parser.add_argument('--mcu-debug',
						action='store_true',
						default=False,
						dest='mcuDebug',
						help='Tha Modbus is in debug mode. It provides dummy data without access the Ethernet or RS485. To test in local machines.')

	parser.add_argument('--modbus-debug',
						action='store_true',
						default=False,
						dest='modbusDebug',
						help='The Arduino is in debug mode. It provides dummy data without access the I2C channel. To test in local machines.')

	parser.add_argument('--board-name',
						'-b',
						action='store',
						dest='boardname',
						type=str,
						default=getBoardId(),
						help='Set the board name')

	parser.add_argument('--remote-sync-disabled',
						'-R',
						action='store_true',
						default=False,
						dest='isRemoteSyncDisabled',
						help='The Arduino is in debug mode. It provides dummy data without access the I2C channel. To test in local machines.')

	parser.add_argument('--delay',
						'-d',
						action='store',
						default=DEFAULT_DELAY_BETWEEN_READINGS,
						dest='delay',
						type=int,
						help='Set the delay between sensors readings (seconds) ')

	parser.add_argument('--sync-cycles',
						'-c',
						action='store',
						default=DEFAULT_READ_CYCLES_BEFORE_SYNC,
						dest='cycles',
						type=int,
						help='Set the number of cycles after you syncronize the remote database (cycles)')

	parser.add_argument('--modbus-ip',
						action='store',
						default=DEFAULT_MODBUS_IP,
						dest='modbusIp',
						type=str,
						help='Set the Charge Controller IP address')

#	parser.add_argument('--modbus-serial-port', action='store', default='/dev/ttymxc2',
#				   dest='modbusPort', type=str,
#				   help='Set the Charge Controller RS485 Serial port')

	parser.add_argument('--timeout',
						'-t',
						action='store',
						default=DEFAULT_REMOTE_SYNC_TIMEOUT,
						dest='timeout',
						type=int,
						help='Set the sync post request timeout  (seconds) ')

	parser.add_argument('--i2c-max-attempts',
						action='store',
						default=DEFAULT_MCU_MAX_ATTEMPTS,
						dest='i2cMaxAttempts',
						type=int,
						help='Set the max number of attempts reading i2c before to send reset signal to mcu ')

	parser.add_argument('--reset-pin',
						action='store',
						dest='resetPin',
						type=int,
						help='Set the reset gpio number ')

	parser.add_argument('--print-data',
						'-p',
						action='store',
						dest='prints',
						type=str,
						default='',
						help='m=MCU, r=RELAY_BOX, s=RELAY_STATE, c=CHARGE CONTROLLER'
						)

	results = parser.parse_args()

	## Parse the parameters and set the global variables
	global REMOTE_SERVER_URL, DATABASE, BOARD_ID, REMOTE_SYNC_TIMEOUT

	BOARD_ID                = str(results.boardname)
	DELAY_BETWEEN_READINGS  = results.delay
	READ_CYCLES_BEFORE_SYNC = results.cycles
	IS_MODBUS_IN_DEBUG_MODE = results.modbusDebug
	IS_MCU_IN_DEBUG_MODE	= results.mcuDebug
	MCU_MAX_ATTEMPTS        = results.i2cMaxAttempts
	REMOTE_SYNC_TIMEOUT     = results.timeout
	MODBUS_IP               = results.modbusIp
	PRINT                   = results.prints
	IS_REMOTE_SYNC_DISABLED = results.isRemoteSyncDisabled

	BUS_I2C = 1
	BOARD_TYPE = "C23"
	RESET_PIN = DEFAULT_RESET_GPIO_C23
	DATABASE_PATH = DEFAULT_DATABASE_PATH_C23

	if results.resetPin != None:
		RESET_PIN = results.resetPin

	DATABASE = DATABASE_PATH + FdsDB.SQLITE_FILENAME

	if IS_REMOTE_SYNC_DISABLED:
		DB_SYNC_ENABLED = False
	else:
		DB_SYNC_ENABLED = True
		REMOTE_SERVER_URL = DEFAULT_REMOTE_SERVER_URL + ":8888/sync/"


	## Print configuaration parameters
	print("------------------- Configuration parms -------------------------")
	print("BOARD_ID: "  + str(BOARD_ID))

	if not DB_SYNC_ENABLED:
		print("Remote database sync disabled!!")
	else:
		print("Server URL is: " + str( REMOTE_SERVER_URL ))


	print("delay: "     + str(DELAY_BETWEEN_READINGS) + " seconds")
	print("cycles: "    + str(READ_CYCLES_BEFORE_SYNC))

	if IS_MODBUS_IN_DEBUG_MODE == True:
		print ("\nModbus disabled\n")
	else:
		print ("Modbus enabled on IP: " + str(MODBUS_IP))

	if IS_MCU_IN_DEBUG_MODE == True:
		print("MCU disabled")

	print("i2c channel: "         + str(BUS_I2C))
	print("board type: "          + str(BOARD_TYPE))

	print("MCU max attempts: "    + str(MCU_MAX_ATTEMPTS))
	print("Remote sync timeout: " + str(REMOTE_SYNC_TIMEOUT))

	print("Reset pin " + str(RESET_PIN))

	print("Database " + str(DATABASE))

	print("-----------------------------------------------------------------")

	if not IS_MCU_IN_DEBUG_MODE:
		print("MCU reset!!")
		resetMcu( BOARD_TYPE, RESET_PIN )


	for i in range(0, 6):
		print('. ', end='', flush=True)
		time.sleep(0.5)


	## connect to the local db: create a new file if doesn't exists
	dbConnection = sqlite3.connect( DATABASE )

	## create tables in sqlite DB if dont exists
	# PAY ATTENTION: if chenged the db structure, it wont recreate the db
	# but the fields will be different
	createDbTables( dbConnection )

	arduino  = None
	# arduinos = None


	## initialize the MCU object
	try:
		arduino = FdsSS.FdsSensor(isDebug = IS_MCU_IN_DEBUG_MODE, busId = BUS_I2C)
	except Exception as e:
		print(e)

	## initialize the ChargeController and Relaybox
	try:
		chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, isDebug = IS_MODBUS_IN_DEBUG_MODE )

		chargeController.connect()

	except Exception as e:
		print(e)


	## initialize Losant dbConnection
	# Construct Losant device

	device = Device(DEVICE_ID, ACCESS_KEY, ACCESS_SECRET)

	try:
		device.connect(blocking=False)
	except Exception as e:
		device = None; print('Error connectiong losant: ' + str(e))

	cycle = 0

	while IS_RUNNING:
		## check if there are commands in cmd file and change local vaiables
		processCommand(COMMAND_INPUT_FILE)

		if not IS_PAUSED:
			print("Sensors reading " + str( cycle ))

			try:
				dataCC = chargeController.getChargeControllerData()
			except Exception as e:
				dataCC = None
				print("READING MODBUS CC: " + str(e))

			try:
				dataRB = chargeController.getRelayBoxData()
			except Exception as e:
				dataRB = None
				print("READING MODBUS RB: " + str(e))

			try:
				dataRS = chargeController.getRelayBoxState()
			except Exception as e:
				dataRS = None
				print("READING MODBUS RS: " + str(e))


			## get Data from MCUs
			for attempt in range(0, MCU_MAX_ATTEMPTS):
				# initialize the data structure for MCU da
				dataMCU = dict()

				try:
					dataMCU  = arduino.getMcuData()
					print("I2C read attempt " + str(attempt) + ": ok")
					break
				except Exception as e:
					dataMCU = None
					print("I2C read attempt " + str(attempt) + ": FAIL  " + str(e))

			## if after all the cycles the mcu is stuck try reset
			if(dataMCU == None):
				print("MCU RESET: MCU i2c probably stuck!")
				resetMcu( BOARD_TYPE, RESET_PIN )

			## print the readed rata
			if 'm' in PRINT:
				printData("MCU", dataMCU)
			if 'c' in PRINT:
				printData("CC", dataCC)
			if 'r' in PRINT:
				printData("RB", dataRB)
			if 's' in PRINT:
				printData("RS", dataRS)

			## Qui in mezzo si possono fare le varie sotto elabrazioni e inviare semmai i dati alla fine

			## creo un dictionary con tutti i valori per passarlo al Device losant
			json_state = dict()
			if dataCC is not None: json_state.update(dataCC)
			if dataRB is not None: json_state.update(dataRB)
			if dataRS is not None: json_state.update(dataRS)
			if dataMCU is not None: json_state.update(dataMCU)

			try:
				sendDeviceStateToLosant(device, json_state)
			except:
				print("Error updating Losant state.")

			## save data to local sqlite db:
			saveDataToDb( dbConnection,
					dataCC,
					dataRB,
					dataRS,
					dataMCU)

			## send data to telemetry
			saveDataToTelemetryFile(TELEMETRY_PATH, dataCC, dataRB, dataRS, dataMCU)

			cycle = cycle + 1
			time.sleep( DELAY_BETWEEN_READINGS )

			## syncronize data
			if cycle == READ_CYCLES_BEFORE_SYNC:
				cycle = 0
				if DB_SYNC_ENABLED:
					syncronizeDb( REMOTE_SERVER_URL, DATABASE, BOARD_ID, REMOTE_SYNC_TIMEOUT )



if __name__== "__main__":
	main()
