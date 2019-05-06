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
import FdsSensorUnico4mcu  as FdsSS4Mcu

##############################################3
MCU_MAX_ATTEMPTS = 5
REMOTE_SYNC_TIMEOUT = 5


SERVER_IP = 'localhost' # R
READ_CYCLES_BEFORE_SYNC = 4
DELAY_BETWEEN_READINGS  = 1.0

CHARGE_CONTROLLER_MODBUS_IP = '192.168.0.254'
IS_MODBUS_IN_DEBUG_MODE = False
IS_MCU_IN_DEBUG_MODE	= False

BOARD_ID = "fds-neo-lab01"
I2C_BUS = None # If none no real arduino are connected
BOARD_TYPE = None
#######################################################


def createDbTables( dbConnection ):
	# get te cursor
	cur = dbConnection.cursor()

	print "Accessing db tables and creating if not exists ..."

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


def sendRequestToServer(table_name, data, timeout):

	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
	payload = json.dumps(data)
	
	timer = eventlet.Timeout(timeout, Exception("Timeout exception syncing table " + table_name) )

	try:
		r = requests.post("http://"+ SERVER_IP +":8888/sync/" + str(table_name), 
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

		print results



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
		print "Number of records in the table " + table_name['name'] + ": "+ str(len(results))

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
		print "Tryng to mark as sync : " + sync_query

		cur1.execute("SELECT timestamp, synced FROM " + tableName + " where synced == 0")
		results = cur1.fetchall()
		print "Unsynced elements: " + str(len(results))
		conn.commit()
		conn.close()


def syncronizeDb(remoteAddress, machineName, timeout):
		json_tables = getDbTablesJson(FdsDB.SQLITE_FILENAME, 'jsons')

		for table_name, value in json_tables.iteritems():
			print("\nSynching table " + table_name)
			try:
				r = sendRequestToServer(table_name, value, timeout=timeout)
				markAsSynced(table_name)
			except Exception as e:
				print "Error sync DB:" + str( e )

		print "Syncronize completer"


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
	except Exception as e:
		print e
	



def main():
	print "INASSE OffGridBox v0.2"

	parser = ArgumentParser()

	parser.add_argument('--mcu-debug', action='store_true', default=False,
				   dest='mcuDebug',
				   help='Tha Modbus is in debug mode. It provides dummy data without access the Ethernet or RS485. To test in local machines.')
	parser.add_argument('--modbus-debug', action='store_true', default=False,
				   dest='modbusDebug',
				   help='The Arduino is in debug mode. It provides dummy data without access the I2C channel. To test in local machines.')

	parser.add_argument('--board-name', '-b', action='store', default='fds-test-01',
				   dest='boardname', type=str,
				   help='Set the board name')
	parser.add_argument('--server-addr', '-s', action='store', default='localhost',
				   dest='serverIp', type=str,
				   help='Set the remote server IP address')
	parser.add_argument('--delay', '-d', action='store', default=2,
				   dest='delay', type=int,
				   help='Set the delay between sensors readings (seconds) ')
	parser.add_argument('--sync-cycles', '-c', action='store', default=5,
				   dest='cycles', type=int,
				   help='Set the number of cycles after you syncronize the remote database (cycles)')

	parser.add_argument('--i2c-channel', '-i', action='store', 
				   dest='i2cChannel', type=int,
				   help='Set the i2c channel: \n1 SBC-23 \n3 UDOO NEO ')
#	parser.add_argument('--modbus-ip', action='store', default='192.168.0.254',
#				   dest='modbusIp', type=str,
#				   help='Set the Charge Controller IP address')
#	parser.add_argument('--modbus-serial-port', action='store', default='/dev/ttymxc2',
#				   dest='modbusPort', type=str,
#				   help='Set the Charge Controller RS485 Serial port')

	

	results = parser.parse_args()

	## PArse the parameters and set the global variables
	global SERVER_IP, DELAY_BETWEEN_READINGS, READ_CYCLES_BEFORE_SYNC, IS_MODBUS_IN_DEBUG_MODE, IS_MCU_IN_DEBUG_MODE
	global BUS_I2C, BOARD_TYPE

	BOARD_ID = str(results.boardname)
	SERVER_IP = str(results.serverIp)
	DELAY_BETWEEN_READINGS = results.delay
	READ_CYCLES_BEFORE_SYNC = results.cycles
	IS_MODBUS_IN_DEBUG_MODE = results.modbusDebug
	IS_MCU_IN_DEBUG_MODE	= results.mcuDebug
	BUS_I2C = results.i2cChannel
	if BUS_I2C == 1:
		BOARD_TYPE = "C23"
	elif BUS_I2C == 3:
		BOARD_TYPE = "NEO"

	## Print configuaration parameters
	print "------------------- Configuration parms -------------------------"
	print "BOARD_ID: "  + str(BOARD_ID)
	print "server ip: " + str(SERVER_IP)
	print "delay: "     + str(DELAY_BETWEEN_READINGS) + " seconds"
	print "cycles: "    + str(READ_CYCLES_BEFORE_SYNC)
	if IS_MODBUS_IN_DEBUG_MODE == True:
		print "Modbus is in debug mode"
	if IS_MCU_IN_DEBUG_MODE == True:
		print "Arduino is in debug mode"

	print "i2c channel: " + str(BUS_I2C)
	print "board type: " + str(BOARD_TYPE)

	print "-----------------------------------------------------------------"
	

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
		# arduinos = FdsSS4Mcu.FdsSensor(busId = 3)
	except Exception as e:
		print e

	try:
		# ci metto l'indirizzo ma ora se ne fotte, quello che conta e' quello che passo dopo
		# Se passo None va in modalita # DEBUG:
		# TODO: aggiustare questa cosa
		chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, isDebug = IS_MODBUS_IN_DEBUG_MODE )

		# Fa solo finta adesso, non serve a una sega
		chargeController.connect()

	except Exception as e:
		print e

	while True:
		
		print "\n ---------------- Batch"

		## reads N times before to sync the local db with the remote one
		for i in range(0, READ_CYCLES_BEFORE_SYNC):
				
			print "Sensors reading " + str( i )
			
			try:
				# get data from Modbus devices
				### >>>>>> None == DBUG <<<<<<<<<
				dataCC = chargeController.getChargeControllerData(None)
				dataRB = chargeController.getRelayBoxData(None)
				dataRS = chargeController.getRelayBoxState(None)
			except Exception as e:
				print "READING MODBUS ERROR: " + str(e)

			try:
				# initialize the data structure for MCU data
				mcuData = dict()

				## get Data from MCUs
				for attempt in range(0, MCU_MAX_ATTEMPTS):
					mcuData  = arduino.getMcuData()
					if(mcuData == None):
						print("I2C read attempt " + str(attempt) + ": FAIL")
					else:
						print("I2C read attempt " + str(attempt) + ": OK")
						break
				
				if(mcuData == None):	
					print "MCU RESET: MCU i2c probably stuck!"
					resetMcu("NEO", 39) 
						
			except Exception as e:
				print "READING ARDUINOS ERROR: " + str(e)
				print e

			## save data to local sqlite db
			saveDataToDb( dbConnection,
					dataCC,
					dataRB,
					dataRS,
					mcuData)


			time.sleep(DELAY_BETWEEN_READINGS)

		## syncronize data
		syncronizeDb( FdsDB.SQLITE_FILENAME, BOARD_ID, REMOTE_SYNC_TIMEOUT )



if __name__== "__main__":
	main()
