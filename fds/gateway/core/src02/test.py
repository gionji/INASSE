import FdsChargeController as FdsCC
import FdsSensorUnico      as FdsSS


try:
	chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, "192.168.0.1")
	chargeController.connect()

	dataCC = chargeController.getChargeControllerData(None)
	dataRB = chargeController.getRelayBoxData(None)
	dataRS = chargeController.getRelayBoxState(None)

	print dataCC
	print dataRB
	print dataRS
except Exception as e:
	print "Error reading Charge controller"
	print e


try:
	arduinos = FdsSS.FdsSensor(1)
	print(arduinos.getMcuData(FdsSS.EXTERNAL))
        print(arduinos.getMcuData(FdsSS.INTERNAL))
        print(arduinos.getMcuData(FdsSS.HYDRAULIC))
        print(arduinos.getMcuData(FdsSS.ELECTRIC))
except Exception as e:
	print  e
