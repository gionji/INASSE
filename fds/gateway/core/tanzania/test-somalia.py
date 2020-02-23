import time
import sys
import os
import signal


sys.dont_write_bytecode = True



import FdsChargeController as FdsCC
import FdsSensorUnico      as FdsSS
import FdsDbConstants      as FdsDB

import FdsCommon as fds






def main():
    try:
        print('Initializing Charge Controller connection...')
        chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, ipAddress='192.168.2.250' )
        chargeController.connect()
    except Exception as e:
        print(e)


    try:
        cc1 = chargeController.getChargeControllerData( modbusUnit=10 )
        print( cc1 )
    except Exception as e:
        print(e)

    try:
        cc2 = chargeController.getChargeControllerData( modbusUnit=20 )
        print( cc2 )
    except Exception as e:
        print(e)

    try:
        rb = chargeController.getRelayBoxData( modbusUnit=9 )
        print( rb )
    except Exception as e:
        print(e)

    try:
        rs = chargeController.getRelayBoxState( modbusUnit=9 )
        print( rs )
    except Exception as e:
        print(e)


    time.sleep(2)




if __name__== "__main__":
    main()

