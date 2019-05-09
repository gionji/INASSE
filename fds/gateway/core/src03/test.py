import logging
import sqlite3
import time
import sys
import requests
import json
import eventlet
eventlet.monkey_patch()

from argparse import ArgumentParser

sys.dont_write_bytecode = True

import FdsChargeController as FdsCC
import FdsSensorUnico	  as FdsSS
import FdsDbConstants	  as FdsDB

# lo uso per test sul cartone, visto che ora gli schetch sono quelli vecchi a 4 MCU
#import FdsSensorUnico4mcu  as FdsSS4Mcu


############# DEFAULTS ####################################
DEFAULT_MODBUS_IP = '192.168.0.254'
DEFAULT_READ_CYCLES_BEFORE_SYNC = 4
DEFAULT_DELAY_BETWEEN_READINGS = 3.0

DEFAULT_MCU_MAX_ATTEMPTS = 10
DEFAULT_REMOTE_SYNC_TIMEOUT = 5

DEFAULT_RESET_GPIO_NEO = 39
DEFAULT_RESET_GPIO_C23 = 0

DEFAULT_REMOTE_SERVER_IP = 'localhost'
#DEFAULT_REMOTE_SERVER_URL = "http://"+ SERVER_IP +":8888/sync/"




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

		conn = sqlite3.connect( FdsDB.SQLITE_FILENAME )
		conn.row_factory = dict_factory

		cur1 = conn.cursor()
		cur1.execute("SELECT timestamp, synced FROM "+table_name['name']+ " where synced == 0")
		results = cur1.fetchall()

		print(results)



def getDbTablesJson(dbName, outputPath):
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

		conn = sqlite3.connect( FdsDB.SQLITE_FILENAME )
		conn.row_factory = dict_factory

		cur1 = conn.cursor()
		cur1.execute("SELECT * FROM "+table_name['name']+ " where synced == 0")
		results = cur1.fetchall()

		data_json = format(results).replace(" u'", "'").replace("'", "\"")
		#print "Number of records in the table " + table_name['name'] + ": "+ str(len(results))

		## TODO add the board id in the json
		data_json = "{\"boardId\": \""+ BOARD_ID +"\",\"data\": " + data_json + "}"

		tables_jsons[ table_name['name'] ] = data_json

	### generate and save JSON files with the table name for each of the database tables
	# with open(outputPath + '/' + table_name['name']+'.json', 'a') as the_file:
	#	the_file.write(format(results).replace(" u'", "'").replace("'", "\""))

	connection.close()

	return tables_jsons


def markAsSynced(tableName):
		conn = sqlite3.connect( FdsDB.SQLITE_FILENAME )
		cur1 = conn.cursor()
		sync_query = "UPDATE "+ tableName + " SET "+ "synced = 1" # WHERE synced == 0"
		cur1.execute( sync_query )
		print("Tryng to mark as sync : " + sync_query)

		cur1.execute("SELECT timestamp, synced FROM " + tableName + " where synced == 0")
		results = cur1.fetchall()
		print("Unsynced elements: " + str(len(results)))
		conn.commit()
		conn.close()


def syncronizeDb(remoteAddress, machineName, timeout):
		json_tables = getDbTablesJson(FdsDB.SQLITE_FILENAME, 'jsons')

		for table_name, value in json_tables.iteritems():
			print("\nSynching table " + table_name)
			try:
				r = sendRequestToServer(table_name, value, timeout=timeout )
				markAsSynced(table_name)
			except Exception as e:
				print("Error sync DB:" + str( e ))

		print("Syncronize complete")


def resetMcu(boardType, resetPin):

	if boardType == "NEO":

		gpios = [
			"178", "179", "104", "143", "142", "141", "140", "149", "105", "148",
		 	"146", "147", "100", "102", "102", "106", "106", "107", "180", "181",
		 	"172", "173", "182", "124",  "25",  "22",  "14",  "15",  "16",  "17",
			"18",   "19",  "20",  "21", "203", "202", "177", "176", "175", "174",
			"119", "124", "127", "116",   "7",   "6",   "5",   "4"]

		gpio = gpios[resetPin];

	elif boardType == "C23":
		gpio = resetPin
		with open("/sys/class/gpio/export", "w") as create:
			create.write(gpio)
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



def printData(name, data):
	if data != None:
		print("\n" + name)
		for key, value in data.items():
			print(str(key) + " : " + str(value))
		print('\n')



def main():
	print("INASSE OffGridBox v0.2")

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
						required=True,
						nargs=1,
						help='Set the board name')

	parser.add_argument('--server-addr',
						'-s',
						action='store',
						dest='serverIp',
						type=str,
						help='Set the remote server IP address')

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

	parser.add_argument('--i2c-channel',
						'-i',
						action='store',
						dest='i2cChannel',
						type=int,
                                                required=True,
                                                nargs=1,
						help='Set the i2c channel: \n1 SBC-23 \n3 UDOO NEO ')

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

	results = parser.parse_args()

	## Parse the parameters and set the global variables

	BOARD_ID                = str(results.boardname)
	SERVER_IP               = str(results.serverIp)
	DELAY_BETWEEN_READINGS  = results.delay
	READ_CYCLES_BEFORE_SYNC = results.cycles
	IS_MODBUS_IN_DEBUG_MODE = results.modbusDebug
	IS_MCU_IN_DEBUG_MODE	= results.mcuDebug
	BUS_I2C                 = results.i2cChannel[0]
	MCU_MAX_ATTEMPTS        = results.i2cMaxAttempts
	REMOTE_SYNC_TIMEOUT     = results.timeout
	MODBUS_IP               = results.modbusIp

	if BUS_I2C == 1:
		BOARD_TYPE = "C23"
	elif BUS_I2C == 3:
		BOARD_TYPE = "NEO"
		RESET_PIN = DEFAULT_RESET_GPIO_NEO

	if results.resetPin != None:
                RESET_PIN = results.resetPin

#	if MODBUS_IP == None:
#		IS_MODBUS_IN_DEBUG_MODE = True
#	else:
#		IS_MODBUS_IN_DEBUG_MODE = False

	
	REMOTE_SERVER_URL = "http://"+ SERVER_IP +":8888/sync/"


	## Print configuaration parameters
	print("------------------- Configuration parms -------------------------")
	print("BOARD_ID: "  + str(BOARD_ID))

	if SERVER_IP != 'None':
		print("Database sync enabled. Server ip: " + str(SERVER_IP))
		DB_SYNC_ENABLED = True
	else:
		print("Database sync disabled")
		DB_SYNC_ENABLED = False

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

	print("-----------------------------------------------------------------")


	time.sleep(5)


	## connect to the local db: create a new file if doesn't exists
	dbConnection = sqlite3.connect( FdsDB.SQLITE_FILENAME )

	## create tables in sqlite DB if dont exists
	# PAY ATTENTION: if chenged the db structure, it wont recreate the db
	# but the fields will be different
	createDbTables( dbConnection )

	arduino  = None
	# arduinos = None

	try:
		# initialize the MCU object
		arduino = FdsSS.FdsSensor(isDebug = IS_MCU_IN_DEBUG_MODE, busId = BUS_I2C)
	except Exception as e:
		print(e)

	try:
		# ci metto l'indirizzo ma ora se ne fotte, quello che conta e' quello che passo dopo
		# Se passo None va in modalita # DEBUG:
		# TODO: aggiustare questa cosa
		chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, isDebug = IS_MODBUS_IN_DEBUG_MODE )

		# Fa solo finta adesso, non serve a una sega
		chargeController.connect()

	except Exception as e:
		print(e)

	while True:

		print("\n ---------------- Batch")

		## reads N times before to sync the local db with the remote one
		for i in range(0, READ_CYCLES_BEFORE_SYNC):

			print("Sensors reading " + str( i ))

			try:
				## get data from Modbus devices
				dataCC = chargeController.getChargeControllerData()
				dataRB = chargeController.getRelayBoxData()
				dataRS = chargeController.getRelayBoxState()
			except Exception as e:
				dataCC = None
				dataRB = None
				dataRS = None
				print("READING MODBUS ERROR: " + str(e))


			## get Data from MCUs
			for attempt in range(0, MCU_MAX_ATTEMPTS):
				
				# initialize the data structure for MCU da
				mcuData = dict()

				try:
					mcuData  = arduino.getMcuData()
					print("I2C read attempt " + str(attempt) + ": ok")
					break
				except Exception as e:
					mcuData = None
					print("I2C read attempt " + str(attempt) + ": FAIL  " + str(e))
					

			if(mcuData == None):
				print("MCU RESET: MCU i2c probably stuck!")
				resetMcu( BOARD_TYPE, RESET_PIN )
				
			printData("MCU", mcuData)

			## save data to local sqlite db
			saveDataToDb( dbConnection,
					dataCC,
					dataRB,
					dataRS,
					mcuData)

			time.sleep(DELAY_BETWEEN_READINGS)

		## syncronize data
		if DB_SYNC_ENABLED:
			syncronizeDb( REMOTE_SERVER_URL, FdsDB.SQLITE_FILENAME, BOARD_ID, REMOTE_SYNC_TIMEOUT )



if __name__== "__main__":
	main()
