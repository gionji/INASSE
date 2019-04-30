import pyudev
import psutil
import time

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')


for device in iter(monitor.poll, None):

    print str(device.action)

    if device.action == 'bind':
        print('>>>>>>>>>>>>>  {} connected'.format(device))
