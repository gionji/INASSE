import pyudev
import psutil
import time

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')


def copyDbFileToUsbDrive():
    print "Copy file to usb"
    print "sync"
    print "unmount"


for device in iter(monitor.poll, None):

    print  str(device.action)

    if device.action == 'bind':
        print('>>>>>>>>>>>>>  {} connected'.format(device))

        removable = [device for device in context.list_devices(subsystem='block', DEVTYPE='disk') if device.attributes.asstring('removable') == "1"]
        for device in removable:
            partitions = [device.device_node for device in context.list_devices(subsystem='block', DEVTYPE='partition', parent=device)]
            print("All removable partitions: {}".format(", ".join(partitions)))
            print("Mounted removable partitions:")
            for p in psutil.disk_partitions():
                if p.device in partitions:
                    print("  {}: {}".format(p.device, p.mountpoint))
					copyDbFileToUsbDrive()
