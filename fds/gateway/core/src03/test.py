import logging
import sqlite3
import time
import sys
import requests
import json

sys.dont_write_bytecode = True

import FdsChargeController as FdsCC
import FdsSensorUnico      as FdsSS
import FdsDbConstants      as FdsDB

# lo uso per test sul cartone, visto che ora gli schetch sono quelli vecchi a 4 MCU
import FdsSensorUnico4mcu  as FdsSS4Mcu


######################################################33
SERVER_IP = '25.46.34.214' # macchina virtuale gionji su asus

READ_CYCLES_BEFORE_SYNC = 5
DELAY_BETWEEN_READINGS  = 2.0

IS_MODBUS_IN_DEBUG_MODE = True
IS_MCU_IN_DEBUG_MODE = True
#######################################################


def createDbTables( dbConnection ):
        # get te cursor
        cur = dbConnection.cursor()

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




def exportLocalDbToJson(dbName, outputPath):
	# connect to the SQlite databases
	connection = sqlite3.connect( dbName )
	connection.row_factory = dict_factory

	cursor = connection.cursor()

	# select all the tables from the database
	cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
	tables = cursor.fetchall()

	# for each of the bables , select all the records from the table
	for table_name in tables:
		# table_name = table_name[0]
		# print table_name['name']

		conn = sqlite3.connect( FdsDB.SQLITE_FILENAME )
		conn.row_factory = dict_factory

		cur1 = conn.cursor()

		cur1.execute("SELECT * FROM "+table_name['name'])

		results = cur1.fetchall()

        	data_json = format(results).replace(" u'", "'").replace("'", "\"")

        	SERVER_IP = '25.46.34.214'
        	headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        	payload = json.dumps(data_json)
        	r = requests.post("http://"+ SERVER_IP +":8888/sync/cc", data=payload, headers=headers)
        	print("Response cc: ", r)

		### generate and save JSON files with the table name for each of the database tables
		# with open(outputPath + '/' + table_name['name']+'.json', 'a') as the_file:
		#	the_file.write(format(results).replace(" u'", "'").replace("'", "\""))

	connection.close()


def syncronizeDb(remoteAddress, machineName):
        exportLocalDbToJson(FdsDB.SQLITE_FILENAME, 'jsons')
        print "Syncronize db. Mo ce provamo"



def main():
    print "Let's test"

    ## connect to the local db: create a new file if doesn't exists
    dbConnection = sqlite3.connect( FdsDB.SQLITE_FILENAME )

    ## create tables in sqlite DB if dont exists
    # PAY ATTENTION: if chenged the db structure, it wont recreate the db
    # but the fields will be different
    createDbTables( dbConnection )


    ## reads N times before to sync the local db with the remote one
    for i in range(0, READ_CYCLES_BEFORE_SYNC):
    	try:
            # ci metto l'indirizzo ma ora se ne fotte, quello che conta e' quello che passo dopo
            # Se passo None va in modalita # DEBUG:
            # TODO: aggiustare questa cosa
            chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, "192.168.0.1", isDebug = IS_MODBUS_IN_DEBUG_MODE )

            # Fa solo finta adesso, non serve a una sega
            chargeController.connect()

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

            # initialize the MCU object
    	    arduino = FdsSS.FdsSensor(busId = 3)
    	    arduinos = FdsSS4Mcu.FdsSensor(busId = 3)

            # get Data from MCUs
    	    mcuData  = arduino.getMcuData(isDebug = IS_MCU_IN_DEBUG_MODE)


            # dati dagli arduini effettivamente connessi
            mcuDataExt = arduinos.getMcuData(mcuType = FdsSS4Mcu.EXTERNAL)
            mcuDataInt = arduinos.getMcuData(mcuType = FdsSS4Mcu.INTERNAL)
            mcuDataHyd = arduinos.getMcuData(mcuType = FdsSS4Mcu.HYDRAULIC)
    	except Exception as e:
    	    print "Reading ARDUINOS: " + str(e)

        ## save data to local sqlite db
        saveDataToDb( dbConnection,
                dataCC,
                dataRB,
                dataRS,
                mcuData)

    	print "Data saved. Cycle: " + str(i)

        time.sleep(DELAY_BETWEEN_READINGS)

    ## syncronize data
    syncronizeDb( FdsDB.SQLITE_FILENAME, "BOARD:001" )

if __name__== "__main__":
    main()
