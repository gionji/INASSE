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
import FdsSensorUnico      as FdsSS
import FdsDbConstants      as FdsDB

# lo uso per test sul cartone, visto che ora gli schetch sono quelli vecchi a 4 MCU
import FdsSensorUnico4mcu  as FdsSS4Mcu


######################################################33
SERVER_IP = '192.168.1.150' # R
READ_CYCLES_BEFORE_SYNC = 4
DELAY_BETWEEN_READINGS  = 1.0

IS_MODBUS_IN_DEBUG_MODE = True
IS_MCU_IN_DEBUG_MODE    = True

BOARD_ID = "fds-neo-lab01"
I2C_BUS = None # If none no real arduino are connected
#######################################################


def createDbTables( dbConnection ):
    # get te cursor
    cur = dbConnection.cursor()

    print "Creating new DB file!!!!"

    if cur is not None:
        cur.execute(FdsDB.sql_create_charge_controller_table)
	cur.execute(FdsDB.sql_create_relaybox_table)
	cur.execute(FdsDB.sql_create_relay_state_table)
	logging.info("Charge controller tables created!")
	cur.execute(FdsDB.sql_create_mcu_table)
    else:
	print("Error! cannot create the database connection.")



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

    with eventlet.Timeout( timeout ):
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        payload = json.dumps(data)
        r = requests.post("http://"+ SERVER_IP +":8888/sync/" + str(table_name), data=payload, headers=headers)

        response = r.content
        # print response

        ### if response is ok 200  <Response [200]>
        # empty the db or sign it as synced

        #print("Response " + table_name, r)
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
        # table_name = table_name[0]
        # print table_name['name']

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
        # table_name = table_name[0]
	# print table_name['name']

    	logging.debug('Exporting ' + str(table_name['name']) + ' to json')

    	conn = sqlite3.connect( FdsDB.SQLITE_FILENAME )
    	conn.row_factory = dict_factory

    	cur1 = conn.cursor()
    	cur1.execute("SELECT * FROM "+table_name['name']+ " where synced == 0")
    	results = cur1.fetchall()

    	data_json = format(results).replace(" u'", "'").replace("'", "\"")
    	print "Number of records in the table " + table_name['name'] + ": "+ str(len(results))

<<<<<<< HEAD
    	## TODO add the board id in the json
    	data_json = "{\"boardId\" : \""+ BOARD_ID +"\", \"data\" : " + data_json + "}"
=======
        ## TODO add the board id in the json
        data_json = "{\"boardId\": \""+ BOARD_ID +"\",\"data\": " + data_json + "}"
>>>>>>> 0a28e4184e35f4aa505d9ee6b927f0f219eb0c00

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


def syncronizeDb(remoteAddress, machineName):
        json_tables = getDbTablesJson(FdsDB.SQLITE_FILENAME, 'jsons')

        for table_name, value in json_tables.iteritems():
            print("synching table " + table_name)
            try:
                r = sendRequestToServer(table_name, value, timeout=3)
                markAsSynced(table_name)
            except Exception as e:
                print "Error sync DB:" + str( e )

        print "Syncronize db. Mo ce provamo"



def main():
    print "Let's test"

    parser = ArgumentParser()

    parser.add_argument('--server', '-s', action='store', default='localhost',
                   dest='serverIp', type=str,
                   help='Set the remote server IP address')
    parser.add_argument('--delay', '-d', action='store', default=2,
                   dest='delay', type=int,
                   help='Set the delay between sensors readings (seconds) ')
    parser.add_argument('--synccycles', '-c', action='store', default=5,
                   dest='cycles', type=int,
                   help='Set the number of cycles after you syncronize the remote database (cycles)')

    results = parser.parse_args()

    global SERVER_IP, DELAY_BETWEEN_READINGS, READ_CYCLES_BEFORE_SYNC

    SERVER_IP = str(results.serverIp)
    DELAY_BETWEEN_READINGS = results.delay
    READ_CYCLES_BEFORE_SYNC = results.cycles

    print "server ip: " + str(SERVER_IP)
    print "delay: " + str(DELAY_BETWEEN_READINGS)
    print "cycles: " + str(READ_CYCLES_BEFORE_SYNC)

    ## connect to the local db: create a new file if doesn't exists
    dbConnection = sqlite3.connect( FdsDB.SQLITE_FILENAME )

    ## create tables in sqlite DB if dont exists
    # PAY ATTENTION: if chenged the db structure, it wont recreate the db
    # but the fields will be different
    createDbTables( dbConnection )

    arduino = None
    arduinos = None

    try:
        # initialize the MCU object
<<<<<<< HEAD
        arduino = FdsSS.FdsSensor(isDebug = IS_MCU_IN_DEBUG_MODE)
        # arduinos = FdsSS4Mcu.FdsSensor(busId = 3)
=======
        arduino = FdsSS.FdsSensor(busId = 3)
       # arduinos = FdsSS4Mcu.FdsSensor(busId = 3)
>>>>>>> 0a28e4184e35f4aa505d9ee6b927f0f219eb0c00
    except Exception as e:
        print e

    try:
        # ci metto l'indirizzo ma ora se ne fotte, quello che conta e' quello che passo dopo
        # Se passo None va in modalita # DEBUG:
        # TODO: aggiustare questa cosa
        chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, "192.168.0.1", isDebug = IS_MODBUS_IN_DEBUG_MODE )

        # Fa solo finta adesso, non serve a una sega
        chargeController.connect()
    except Exception as e:
        print e

    while True:
        ## reads N times before to sync the local db with the remote one
        for i in range(0, READ_CYCLES_BEFORE_SYNC):
            try:
                # get data from Modbus devices
        	dataCC = chargeController.getChargeControllerData(None)
        	dataRB = chargeController.getRelayBoxData(None)
        	dataRS = chargeController.getRelayBoxState(None)

            except Exception as e:
                print "Error reading Charge controller"
                print e

            try:
                # initialize the data structure for MCU data
                mcuData = dict()

                # get Data from MCUs
                mcuData  = arduino.getMcuData()

                ## dati dagli arduini effettivamente connessi
                # TODO se c'e' errore ritorna None, non da eccezione
<<<<<<< HEAD
#                with eventlet.Timeout( 3 ):
#                    mcuDataExt = arduinos.getMcuData(mcuType = FdsSS4Mcu.EXTERNAL)
#                    mcuDataInt = arduinos.getMcuData(mcuType = FdsSS4Mcu.INTERNAL)
#                    mcuDataHyd = arduinos.getMcuData(mcuType = FdsSS4Mcu.HYDRAULIC)
=======
                
		#with eventlet.Timeout( 3 ):
                #    mcuDataExt = arduinos.getMcuData(mcuType = FdsSS4Mcu.EXTERNAL)
                #    mcuDataInt = arduinos.getMcuData(mcuType = FdsSS4Mcu.INTERNAL)
                #    mcuDataHyd = arduinos.getMcuData(mcuType = FdsSS4Mcu.HYDRAULIC)
>>>>>>> 0a28e4184e35f4aa505d9ee6b927f0f219eb0c00
            except Exception as e:
                print "ERRRORRRR:   Reading ARDUINOS: " + str(e)

            ## save data to local sqlite db
            saveDataToDb( dbConnection,
                    dataCC,
                    dataRB,
                    dataRS,
                    mcuData)

            print "Data saved. Cycle: " + str(i)

            time.sleep(DELAY_BETWEEN_READINGS)

        ## syncronize data
        syncronizeDb( FdsDB.SQLITE_FILENAME, BOARD_ID )



if __name__== "__main__":
    main()
