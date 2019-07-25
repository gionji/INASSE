'''
dbus Server With Callbacks
--------------------------------------------------------------------------

This is an example of adding callbacks to a running modbus server
when a value is written to it. In order for this to work, it needs
a device-mapping file.
'''
# ---------------------------------------------------------------------------#
# import the modbus libraries we need
# ---------------------------------------------------------------------------#
from pymodbus.server.async import StartTcpServer
from pymodbus.datastore import ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from twisted.internet import threads
import psutil

# ---------------------------------------------------------------------------#
# import the python libraries we need
# ---------------------------------------------------------------------------#
from multiprocessing import Queue, Process

# ---------------------------------------------------------------------------#
# configure the service logging
# ---------------------------------------------------------------------------#
import logging

logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)


class Device(object):
    def __init__(self, path, devicetype, callback):
        self.path = path
        self.devicetype = devicetype
        self.callback = callback
        self.value = 0

    def update(self):
        self.value = self.callback(self.path)


def temperatureFromW1File(sensorpath):
    try:
        f = open(sensorpath + "/w1_slave", 'r')
    except IOError as e:
        return -999
    lines = f.readlines()
    f.close()
    crcLine = lines[0]
    tempLine = lines[1]
    result_list = tempLine.split("=")
    temp = float(result_list[-1]) / 1000  # temp in Celcius
    temp = temp + 1  # correction factor
    # if you want to convert to Celcius, comment this line
    temp = (9.0 / 5.0) * temp + 32

    if crcLine.find("NO") > -1:
        temp = -999
    return temp*100


# ---------------------------------------------------------------------------#
def getBatteryVoltage():
    return 14.0

def getBatteryCurrent():
    return 1.0

def getBatteryPower():
    return 20.0

def getBatteryTemperature():
    return 4.0

def getBatterySensing():
    return 0.0


def getArrayVoltage():
    return 1.0

def getArrayCurrent():
    return 2.0

def getArrayPower():
    return 3.0


def getOutputCurrent():
    return 5.0

def getInputPower():
    return 6.0

def getBatteryVoltageDailyMinimum():
    return 7.0

def getBatteryVoltageDailyMaximum():
    return 8.0


def getBatteryTemperatureDailyMinimum():
    return 7.0

def getBatteryTemperatureDailyMaximum():
    return 8.0

def getHeatsinkTemperature():
    return 9.0


def getState():
    return 0

def getDipswitches():
    return 0x01


# ---------------------------------------------------------------------------#
# create your custom data block with callbacks
# ---------------------------------------------------------------------------#
class CallbackDataBlock(ModbusSparseDataBlock):
    ''' A datablock that stores the new value in memory
    and passes the operation to a message queue for further
    processing.
    '''

    def __init__(self, devices):
        self.devices = devices
        self.devices[0xbeef] = len(self.devices)  # the number of devices
        self.get_temperature()
        # values = [k:0 ]
        self.values = {k: 0 for k in self.devices.iterkeys()}
        super(CallbackDataBlock, self).__init__(self.values)

    def get_temperatures(self, devices):
        values = {}
        for device in devices:
            device.update()
            values[device.register] = device.value
            print device.path,device.value
        return values

    def get_temperature(self):
        #print 'getting temperatures'
        temp_sensors = []
        devices_registers = filter(lambda d: d != 0xbeef, self.devices)
        for registers in devices_registers:
            if self.devices[registers].devicetype == 'ds18b20':
                self.devices[registers].register = registers
                temp_sensors.append(self.devices[registers])
        d = threads.deferToThread(self.get_temperatures, temp_sensors)
        d.addCallback(self.update_temperature_values)

    def update_temperature_values(self, values):
        for register in values:
            self.values[register] = values[register]
        self.get_temperature()

    # def getValues(self, address, count=1):
    #     values = [i.value for i in [k for k in self.devices.itervalues()][address:address + count]]
    #
    #     return values


# ---------------------------------------------------------------------------#
# initialize your device map
# ---------------------------------------------------------------------------#
def read_device_map():
    rootpath = '/sys/bus/w1/devices/'
    devices = {
        0x0001: Device('/sys/bus/iio/devices/iio\:device0/in_voltage0_raw', 'acs712', getArrayCurrent      ),
        0x0002: Device('/sys/bus/iio/devices/iio\:device0/in_voltage1_raw', 'acs712', getBatteryCurrent    ),
        0x0003: Device('/sys/bus/iio/devices/iio\:device0/in_voltage2_raw', 'acs712', getOutputCurrent     ),
        0x0004: Device('/sys/bus/iio/devices/iio\:device0/in_voltage3_raw', 'acs712', getArrayVoltage      ),
        0x0005: Device('/sys/bus/iio/devices/iio\:device1/in_voltage0_raw', 'voltmeter', getArrayVoltage   ),
        0x0006: Device('/sys/bus/iio/devices/iio\:device1/in_voltage1_raw', 'voltmeter', getBatteryVoltage ),
        #0x0007: Device('/sys/bus/iio/devices/iio\:device1/in_voltage1_raw', 'ds20b18', getBatteryTemperature  ),
        #0x0008: Device('/sys/bus/iio/devices/iio\:device1/in_voltage1_raw', 'ds20b18', getHeatsinkTemperature  ) 
    }
    return devices


# ---------------------------------------------------------------------------#
# initialize your data store
# ---------------------------------------------------------------------------#
devices = read_device_map()
block = CallbackDataBlock(devices)
store = ModbusSlaveContext(di=None, co=None, hr=None, ir=block)
context = ModbusServerContext(slaves=store, single=True)

# ---------------------------------------------------------------------------#
# run the server you want
# ---------------------------------------------------------------------------#
StartTcpServer(context, address=("0.0.0.0", 5020))
