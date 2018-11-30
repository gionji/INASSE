#!/usr/bin/env python

# Based on Morningstar documentation here
# http://www.morningstarcorp.com/wp-content/uploads/2014/02/TSMPPT.APP_.Modbus.EN_.10.2.pdf

# Copyright un cazzo di nulla! Venite a riprendermi in Spagna o in Germania .. forse! Ciao Stronzi! Vi offro una pizza!!


__version__ = 0.5

import fds_constants as fds


import serial
import time
import random
import sqlite3
import ast
import datetime
import sys
import os
from pymodbus.exceptions import ModbusIOException
from argparse import ArgumentParser
# import the server implementation
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
# configure the client logging
import logging

def showBits(input):
 return bin( input )[::-1][:-2].zfill(8)


def getChargeControllerData(client):
 data = {'type':'chargecontroller'}

 if client != None:
  try:
   # read registers. Start at 0 for convenience
   rr = client.read_holding_registers(0,80, unit=fds.CHARGE_CONTROLLER_UNIT)

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
  except ModbusIOException: 
   print 'Charge Controller: modbusIOException'
   return None
  except: 
   print 'Charge Controller: unpredicted exception'
   return None
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


def getRelayBoxData(client):
 data = {'type':'relaybox'}

 if client != None:
  try:
   # read registers. Start at 0 for convenience
   rr = client.read_holding_registers(0,18, unit=fds.RELAYBOX_UNIT)
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
  except ModbusIOException: 
   print 'RelayBoxRead: modbusIOException'
   return None
  except: 
   print 'RelayBoxRead: unpredicted exception'
   return None
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

def readRelayState(client):
 data = {'type':'relayState'}
 if client != None:
  try:
   rr = client.read_coils(0, 8, unit=9)
   data["relay_1"]   = rr.bits[0]
   data["relay_2"]   = rr.bits[1]
   data["relay_3"]   = rr.bits[2]
   data["relay_4"]   = rr.bits[3]
   data["relay_5"]   = rr.bits[4]
   data["relay_6"]   = rr.bits[5]
   data["relay_7"]   = rr.bits[6]
   data["relay_8"]   = rr.bits[7]
  except ModbusIOException: 
   print 'RelayState: modbusIOException'
   return None
  except: 
   print 'RelayState: unpredicted exception'
   return None
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


def getMCUdata(request_cmd):
 data = {'type':'mcu'}
 ser = serial.Serial('/dev/ttyACM0', timeout=1)  # open serial port
 ser.write(str(request_cmd)) 
 try:
  line = ser.readline()
 except TimeoutError:
  print 'Serial Read Timeout error.'
  ser.close()
  return None
 except: 
  print 'Serial Read unpredicted error.'
  return None
  
 ser.close()
 try:
  mcu_data = dict( ast.literal_eval(line) )
 except:
  print 'MCU message parsing error.' 
  return None
 return mcu_data


def createDBtables(cur):
 print "create tables ..."


 if cur is not None:
  cur.execute(fds.sql_create_charge_controller_table)
  cur.execute(fds.sql_create_relaybox_table)
  cur.execute(fds.sql_create_mcu_table)
  cur.execute(fds.sql_create_relay_state_table)
  print("Tables created!")
 else:
  print("Error! cannot create the database connection.")
# for count, thing in enumerate(args):
#  tab = dict(thing).keys()
  


def addDataToDB(conn, *args):

 cur = conn.cursor()

 for count, thing in enumerate(args):
  if thing == None:
   break
   
  data = dict(thing)
  if data['type'] ==  'relayState':
   cur.execute(fds.insert_relay_state, data)
   sys.stdout.write('r')
  elif data['type'] ==  'mcu':
   cur.execute(fds.insert_mcu, data) 
   sys.stdout.write('m')
  elif data['type'] ==  'relaybox':
   cur.execute(fds.insert_rb, data) 
   sys.stdout.write('b')
  elif data['type'] ==  'chargecontroller':
   cur.execute(fds.insert_cc, data) 
   sys.stdout.write('c')
 conn.commit() 
 sys.stdout.write(' done')



def main():

 hosts = [ fds.CHARGE_CONTROLLER_IP ]

 parser = ArgumentParser()

 parser.add_argument('--dummydata', '-d', action='store_true', default=False,
                    dest='use_dummy_data',
                    help='Use dummy data instead of connect to the modbus or mcu.')
 parser.add_argument('--address','-a', action='store', 
                    dest='charge_controller_ip',
                    help='Set the Modbus IP to connect to the Charge Controller')
 parser.add_argument('--cycles', '-c', action='store', default=1,
                    dest='cycles', type=int,
                    help='Set the number of cycles')
 parser.add_argument('--sampling', '-s', action='store', default=2,
                    dest='sampling_rate', type=int,
                    help='Set the delay in seconds between two readings')
 parser.add_argument('--daemon', '-g', action='store_true', default=False,
                    dest='im_a_daemon',
                    help='The script will be a daemon')
 parser.add_argument('--version', action='version', version='%(prog)s  ' + str(__version__))

 results = parser.parse_args() 
 print 'Parsed arguments ========='
 print "Use dummy data" , results.use_dummy_data
 print "CC IP " , results.charge_controller_ip
 print "Cycles " , results.cycles
 print "Sampling rate " , results.sampling_rate
 print "Im a fuckin deamon " , results.im_a_daemon
 print '=========================='

 SAMPLING_RATE = results.sampling_rate
 MAX_CYCLES  = results.cycles
 DUMMY_DATA  = results.use_dummy_data
 IM_A_DAEMON = results.im_a_daemon

 if results.charge_controller_ip is not None:
  hosts = [results.charge_controller_ip]

 logging.basicConfig()
 log = logging.getLogger('./modbus.error')
 log.setLevel(logging.ERROR)

 client = None

 # connect to modbus hosts
 if not DUMMY_DATA:
  for host in hosts:
    print "Trying to connect to Modbus IP Host %s ..." % host
    client = ModbusClient(host, fds.MODBUS_PORT)
    client.connect()

 sqlite_file = './data/db_fds_offgridbox-'+ str(datetime.datetime.now().strftime('%Y%m%d-%H:%M:%S')) +'.sqlite'

 if os.path.isfile(fds.SQLITE_FILENAME):
  os.rename(fds.SQLITE_FILENAME, sqlite_file)
  print "File backup in : " + sqlite_file


 # Connecting to the database file
 conn = sqlite3.connect(fds.SQLITE_FILENAME)
 cur = conn.cursor()
 createDBtables( cur )

 i = 0
 counter = 0
 while i < MAX_CYCLES: # circa un giorno a 30 al minuto ... forse un po d i piu
  counter = counter + 1
  sys.stdout.write("Reading Modbus " + str(counter) + ' :: ' )
  chargeControllerData = getChargeControllerData(client)
  sys.stdout.write('.')
  relayBoxData         = getRelayBoxData(client)
  sys.stdout.write('.')
  relayStateData       = readRelayState(client)
  sys.stdout.write('. done! - Reading MCU ')
  mcuData              = getMCUdata(fds.MCU_READ_CMD)
  sys.stdout.write('. done! - Adding element to db ' )
  addDataToDB(conn, chargeControllerData , relayBoxData, relayStateData, mcuData )
  print('! ')
  time.sleep(SAMPLING_RATE)
  if not IM_A_DAEMON:
   i = i + 1
 
 cur.execute('SELECT * FROM charge_controller')
 # print(cur.fetchall())

 conn.commit()
 conn.close()

if __name__== "__main__":
 main()

