#!/usr/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

import json
import logging
import sqlite3

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
    dbConnection = sqlite3.connect( databaseFilename )

    # get the board ID
    boardId = ''

    # get te cursor
    cur = dbConnection.cursor()

    print ">>>>>> " + table_name
    print json_data + ">>>>>>"

    dbConnection.commit()
    # commit

    # close connection

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
        data = json.loads(json_data)

        print "MCU Data received: " + str( len(data) ) + " bytes."

        ## print the readed json PRETTY
        #print json.dumps(data, indent=2, sort_keys=True)
        self.write("MCU Sync ok")


class ChargeControllerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("ChargeController Handler")

    def post(self):
        json_data = self.request.body
        data = json.loads(json_data)

        print "CC Data received: " + str( len(data) ) + " bytes."
        ## print the readed json PRETTY
        #print json.dumps(data, indent=2, sort_keys=True)
        self.write("CC Sync ok")



class RelayBoxHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("RelayBoxHandler Handler")

    def post(self):
        json_data = self.request.body
        data = json.loads(json_data)

        print "RB Data received: " + str( len(data) ) + " bytes."

        ## print the readed json PRETTY
        # print json.dumps(data, indent=2, sort_keys=True)
        self.write("RB Sync ok")



class RelayStateHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("RelayStateHandler Handler")

    def post(self):
        json_data = self.request.body
        data = json.loads(json_data)

        print "RS Data received: " + str( len(data) ) + " bytes."

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
