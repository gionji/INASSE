import pyudev
import psutil
import time
from shutil import copyfile

FILE_NAME = './file.bin'

context = pyudev.Context()
monitor = pyudev.Monitor.from_netlink(context)
monitor.filter_by(subsystem='usb')

def copyDbFileToUsbDrive(src, dst):
    print "Copy file to usb"
    copyfile(src, dst)
    print "unmount"


def main():
	print "Do some jobs!!"
	time.sleep(2)
	print "Agg finito il job!"


	print "Ora controllo le pennette USB ..."


if __name__== "__main__":
	main()
