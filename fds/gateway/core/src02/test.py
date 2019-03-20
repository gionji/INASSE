import FdsChargeController as FdsCC
import FdsSensorUnico as FdsSS


chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, "192.168.0.1")

arduinos = FdsSS.FdsSensor(3)

chargeController.connect()

dataCC = chargeController.getChargeControllerData(None)
dataRB = chargeController.getRelayBoxData(None)
dataRS = chargeController.getRelayBoxState(None)

arduinos

print dataCC
print dataRB
print dataRS

