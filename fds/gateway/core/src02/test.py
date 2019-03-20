import FdsChargeController as FdsCC


chargeController = FdsCC.FdsChargeController(FdsCC.MODBUS_ETH, "192.168.0.1")

chargeController.connect()
