#!/usr/bin/env python

import time
from FdsSensorUnico import FdsSensor

DELAY = 0.1
FLT_MAX = 3

def resetArduino():
	print("Send Arduinos reset signal")


def main():
	## Initialize Arduinos errors counters
	arduinoExtFltCnt = 0
	arduinoIntFltCnt = 0
	arduinoHydFltCnt = 0
	arduinoEleFltCnt = 0

	print("------- FdsSensor class test ----------");
	fds = FdsSensor(1)

	# Start the loop
	while True:
		values = list()

		try:
			values.append( fds.getSolarPanelTemperature1() )
			values.append( fds.getSolarPanelTemperature2() )
			values.append( fds.getEnvironmentalTemperature() )
			values.append( fds.getIrradiation() )
			values.append( fds.getWindSpeed() )
			# reset the error counter
			arduinoExtFltCnt = 0
		except:
			arduinoExtFltCnt = arduinoExtFltCnt + 1
			print("Arduino EXTERNAL not found. Attempt ", arduinoExtFltCnt)


		try:
			values.append( fds.getInternalTemperature() )
			values.append( fds.getIncomingTemperature() )
			values.append( fds.getOutcomingTemperature() )
			values.append( fds.getFloodStatus() )
			values.append( fds.getDHT11Temperature() )
			values.append( fds.getDHT11Humidity() )
			# reset the error counter
			arduinoIntFltCnt = 0
		except:
			arduinoIntFltCnt = arduinoIntFltCnt + 1
			print("Arduino INTERNAL not found. Attempt ", arduinoIntFltCnt)

		try:    
			values.append( fds.getWaterFluxIn() )
			values.append( fds.getWaterFluxOut() )
			values.append( fds.getPressureIn() )
			values.append( fds.getPressureMiddle() )
			values.append( fds.getPressureOut() )
			values.append( fds.getWaterTemperature() )
			values.append( fds.getWaterLevel() )
			# reset the error counter
			arduinoHydFltCnt = 0
		except:
			arduinoHydFltCnt = arduinoHydFltCnt + 1
			print("Arduino HYDRAULIC not found. Attempt ", arduinoHydFltCnt)
			
						
#		try:
#			values.append( fds.getCCCurrent() )
#			values.append( fds.getACCurrent(1) )
#			values.append( fds.getACCurrent(2) )
#			arduinoEleFltCnt = 0
#		except:
#			arduinoEleFltCnt = arduinoEleFltCnt + 1
#			print("Arduino ELECTRIC not found. Attempt ", arduinoEleFltCnt) 


		if arduinoEleFltCnt > FLT_MAX or arduinoIntFltCnt > FLT_MAX or arduinoExtFltCnt > FLT_MAX or arduinoHydIntCnt > FLT_MAX:
			resetArduino()

		time.sleep( DELAY )

		## Print the data collected
		print("---------")

		for v in values:
			print(v)


	## Add values to db



if __name__ == "__main__":
    main()

