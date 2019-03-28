import logging
import sqlite3

import FdsChargeController as FdsCC
import FdsSensorUnico      as FdsSS
import FdsDbConstants      as FdsDB



def createDbTables( dbConnection ):
        # get te cursor
        cur = dbConnection.cursor()

	if cur is not None:
		cur.execute(FdsDB.sql_create_charge_controller_table)
		cur.execute(FdsDB.sql_create_relaybox_table)
		cur.execute(FdsDB.sql_create_relay_state_table)
		print("Charge controller tables created!")

		cur.execute(FdsDB.sql_create_mcu_external_table)
		cur.execute(FdsDB.sql_create_mcu_internal_table)
		cur.execute(FdsDB.sql_create_mcu_hydraulic_table)
		cur.execute(FdsDB.sql_create_mcu_electric_table)
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
			cur.execute(FdsDB.insert_rb, data)
		elif data['type'] ==  'chargecontroller':
			cur.execute(FdsDB.insert_cc, data)
                elif data['type'] ==  FdsSS.EXTERNAL:
                	cur.execute(FdsDB.insert_mcu_external, data)
                elif data['type'] ==  FdsSS.INTERNAL:
			cur.execute(FdsDB.insert_mcu_internal, data)
                elif data['type'] ==  FdsSS.HYDRAULIC:
			cur.execute(FdsDB.insert_mcu_hydraulic, data)
                elif data['type'] ==  FdsSS.ELECTRIC:
			cur.execute(FdsDB.insert_mcu_electric, data)

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
		 
		# fetch all or one we'll go for all.
		 
		results = cur1.fetchall()
		 
		# print results

		# generate and save JSON files with the table name for each of the database tables
		with open(outputPath + '/' + table_name['name']+'.json', 'a') as the_file:
			the_file.write(format(results).replace(" u'", "'").replace("'", "\""))

	connection.close()


def syncronizeDb(remoteAddress, machineName):
        exportLocalDbToJson(FdsDB.SQLITE_FILENAME, 'jsons')
        print "Syncronize db. Mo ce provamo"



dbConnection = sqlite3.connect( FdsDB.SQLITE_FILENAME )

## create tables in sqlite DB
createDbTables( dbConnection )

for i in range(0, 3):
	try:
		chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, "192.168.0.1")
		chargeController.connect()
	
		dataCC = chargeController.getChargeControllerData(None)
		dataRB = chargeController.getRelayBoxData(None)
		dataRS = chargeController.getRelayBoxState(None)
		
#		print dataCC
#		print dataRB
#		print dataRS
	except Exception as e:
		print "Error reading Charge controller"
		print e

	try:
		mcuData = dict()

		arduinos = FdsSS.FdsSensor(3)
		
		mcuData[FdsSS.INTERNAL]  = arduinos.getMcuData( FdsSS.EXTERNAL  )
        	mcuData[FdsSS.EXTERNAL]  = arduinos.getMcuData( FdsSS.INTERNAL  )
        	mcuData[FdsSS.HYDRAULIC] = arduinos.getMcuData( FdsSS.HYDRAULIC )
        	mcuData[FdsSS.ELECTRIC]  = arduinos.getMcuData( FdsSS.ELECTRIC  )

		#print mcuData[FdsSS.INTERNAL]
		#print mcuData[FdsSS.EXTERNAL]
		#print mcuData[FdsSS.HYDRAULIC]
		#print mcuData[FdsSS.ELECTRIC]
	except Exception as e:
		print "Reading ARDUINOS: " + str(e)

	print "Data saved " + str(i)
	
	saveDataToDb( dbConnection,
			dataCC, 
			dataRB, 
			dataRS, 
			mcuData[FdsSS.INTERNAL], 
			mcuData[FdsSS.EXTERNAL], 
			mcuData[FdsSS.HYDRAULIC], 
			mcuData[FdsSS.ELECTRIC])

syncronizeDb( FdsDB.SQLITE_FILENAME, "BOARD001" )


