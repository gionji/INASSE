#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import json
import logging
import sqlite3
import ast

import FdsRdbConstants as FdsRDB

def initializeDatabase( databaseFilename ):
    ## open the db
    logging.info("Opening DB connection ")
    dbConnection = sqlite3.connect( databaseFilename )
    dbCursor = dbConnection.cursor()

    # queries create
    if dbCursor is not None:
        logging.info("Creating tables if not exists ")
        dbCursor.execute(FdsRDB.remote_sql_create_charge_controller_table)
        dbCursor.execute(FdsRDB.remote_sql_create_relaybox_table)
        dbCursor.execute(FdsRDB.remote_sql_create_relay_state_table)
        dbCursor.execute(FdsRDB.remote_sql_create_mcu_table)
    else:
        logging.error("Error! cannot create the database tables.")
        return False

    #commit
    dbConnection.commit()
    #close connection
    dbConnection.close()

    return True




def addDataToDb(table_name, json_data):
    ## open connection
    dbConnection = sqlite3.connect( FdsRDB.SQLITE_FILENAME )

    # get te cursor
    cur = dbConnection.cursor()

    json_decoded = json.loads(json_data)
    obj_data = ast.literal_eval( json_decoded )

    # get the board ID
    boardId = obj_data['boardId']
    recordsNumber = len(obj_data['data'])
    data = obj_data['data']

    data_for_query = list()

    if table_name == 'mcu':
        for d in data:
            data_for_query.append( tuple([boardId, 
                                          d['temp1'], 
                                          d['temp2'], 
                                          d['pres1'], 
                                          d['pres2'], 
                                          d['pres3'], 
                                          d['flux1'], 
                                          d['flux2'], 
                                          d['cc'], 
                                          d['ac1'], 
                                          d['ac2'],
                                          d['timestamp']
                                          ]))
        query = "INSERT INTO " + table_name + " VALUES (NULL, ?, datetime('now'), ?, ?,   ?, ?, ?, ?, ?,  ?, ?, ?, ?)"

    elif table_name == 'relay_box':
        for d in data:
            data_for_query.append( tuple([boardId, 
                                          d['timestamp'],
                                          d['adc_vb'], 
                                          d['adc_vch_1'], 
                                          d['adc_vch_2'], 
                                          d['adc_vch_3'], 
                                          d['adc_vch_4'], 
                                          d['t_mod'], 
                                          d['global_faults'], 
                                          d['global_alarms'], 
                                          d['hourmeter_HI'], 
                                          d['hourmeter_LO'],
                                          d['ch_faults_1'],
                                          d['ch_faults_2'],
                                          d['ch_faults_3'],
                                          d['ch_faults_4'],
                                          d['ch_alarms_1'],
                                          d['ch_alarms_2'],
                                          d['ch_alarms_3'],
                                          d['ch_alarms_4']
                                          ]))
        query = "INSERT INTO " + table_name + " VALUES (NULL, ?, datetime('now'), ?, ?, ?, ?, ?,  ?, ?, ?, ?, ?,  ?, ?, ?, ?,  ?, ?, ? ,?, ?)"
    elif table_name == 'relay_state': 
        for d in data:
            data_for_query.append( tuple([boardId,
                                          d['timestamp'],
                                          d['relay_1'],                                         
                                          d['relay_2'],
                                          d['relay_3']
                                          ]))
        query = "INSERT INTO " + table_name + " VALUES (NULL, ?, datetime('now'), ?, ?, ?,?)"
    elif table_name == 'charge_controller':         
        for d in data:
            data_for_query.append( tuple([boardId,
                                          d['timestamp'],
                                          d['battsV'],
                                          d['battsSensedV'],
                                          d['battsI'],
                                          d['arrayV'],
                                          d['arrayI'],
                                          d['statenum'],
                                          d['hsTemp'],
                                          d['rtsTemp'],
                                          d['outPower'],
                                          d['inPower'],
                                          d['minVb_daily'],
                                          d['maxVb_daily'],
                                          d['minTb_daily'],
                                          d['maxTb_daily'],
                                          d['dipswitches']                       
                                          ]))
        query = "INSERT INTO " + table_name + " VALUES (NULL, ?, datetime('now'), ?, ?,   ?, ?, ?,?, ?,   ?, ?, ?, ?, ?,  ?, ?, ?, ?)"


    cur.executemany(query, data_for_query)

    # commit
    dbConnection.commit()

    # close connection
    dbConnection.close()

    return None


def saveJsonAsFile():
    return None




define("port", default=8888, help="run on the given port", type=int)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        json_data = self.request.body
        data = json.loads(json_data)

        #print the readed json PRETTY
        print json.dumps(data, indent=2, sort_keys=True)



class McuHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Microcontrollers Handler")

    def post(self):
        json_data = self.request.body
        
        # print json.dumps(data, indent=2, sort_keys=True)
        print "CC Data received: " + str( len(json_data) ) + " bytes."

        addDataToDb('mcu', json_data)
        
        self.write("MCU Sync ok")


class ChargeControllerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ChargeController Handler")

    def post(self):
        json_data = self.request.body
        addDataToDb('charge_controller', json_data)

        print "CC Data received: " + str( len(json_data) ) + " bytes."
        ## print the readed json PRETTY
        #print json.dumps(data, indent=2, sort_keys=True)
        self.write("CC Sync ok")



class RelayBoxHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("RelayBoxHandler Handler")

    def post(self):
        json_data = self.request.body
        addDataToDb('relay_box', json_data)

        print "RB Data received: " + str( len(json_data) ) + " bytes."

        ## print the readed json PRETTY
        # print json.dumps(data, indent=2, sort_keys=True)
        self.write("RB Sync ok")



class RelayStateHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("RelayStateHandler Handler")

    def post(self):
        json_data = self.request.body
        addDataToDb('relay_state', json_data)

        print "RS Data received: " + str( len(json_data) ) + " bytes."

        ## print the readed json PRETTY
        #print json.dumps(data, indent=2, sort_keys=True)
        self.write("RS Sync ok")



def main():

    initializeDatabase( FdsRDB.SQLITE_FILENAME )

    tornado.options.parse_command_line()
    application = tornado.web.Application([
                                           (r"/sync/charge_controller", ChargeControllerHandler),
                                           (r"/sync/relay_box", RelayBoxHandler),
                                           (r"/sync/relay_state", RelayStateHandler),
                                           (r"/sync/mcu", McuHandler),
                                           (r"/", MainHandler)
                                           ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
