import logging
import time
import sys
import json


IS_RUNNING = True
IS_PAUSED = False

BOARD_ID = None

DEFAULT_RESET_GPIO_NEO = 39
DEFAULT_RESET_GPIO_C23 = 149


def dict_factory(cursor, row):
	d = {}
	for idx, col in enumerate(cursor.description):
		d[col[0]] = row[idx]
	return d





def resetMcu(boardType, resetPin):

	if (boardType == "NEO"):
		gpios = [
			"178", "179", "104", "143", "142", "141", "140", "149", "105", "148",
			"146", "147", "100", "102", "102", "106", "106", "107", "180", "181",
			"172", "173", "182", "124",  "25",  "22",  "14",  "15",  "16",  "17",
			"18",   "19",  "20",  "21", "203", "202", "177", "176", "175", "174",
			"119", "124", "127", "116",   "7",   "6",   "5",   "4"]

		gpio = gpios[resetPin]

		try:
			with open("/sys/class/gpio/gpio" + gpio + "/direction", "w") as re:
				re.write("out")
			with open("/sys/class/gpio/gpio" + gpio + "/value", "w") as writes:
				writes.write("0")
				time.sleep(1.0)
				writes.write("1")
				time.sleep(1.0)
		except Exception as e:
				print(e)

	# for C23 we use PWM
	elif boardType == "C23":
		try:
			with open("/sys/class/pwm/pwmchip4/export", "w") as pwm:
				pwm.write("0")
		except Exception as e:
			print(e)

		try:
			with open("/sys/class/pwm/pwmchip4/pwm0/period", "w") as pwm:
				pwm.write("100")
		except Exception as e:
			print(e)

		try:
			with open("/sys/class/pwm/pwmchip4/pwm0/duty_cycle", "w") as pwm:
				pwm.write("100")
		except Exception as e:
			print(e)

		try:
			with open("/sys/class/pwm/pwmchip4/pwm0/enable", "w") as pwm:
				pwm.write("0")
				pwm.flush()
				time.sleep(1.0)
				pwm.write("1")
				pwm.flush()
		except Exception as e:
			print(e)



def printData(name, data):
	if data != None:
		print("\n" + name)
		for key, value in data.items():
			print(str(key) + " : " + str(value))
		print('\n')


def getBoardId():
	try:
		with open("/sys/fsl_otp/HW_OCOTP_CFG0", "r") as reader:
			id0 = reader.read()
		with open("/sys/fsl_otp/HW_OCOTP_CFG1", "r") as reader:
			id1 = reader.read()

		id = "fds-" + str(id1[2:10]) + str(id0[2:10])
	except Exception as e:
		print(e)
		id = "fds-unknown"

	return id



def main():
	print("INASSE OffGridBox Woodbox")

	while IS_RUNNING:

		if not IS_PAUSED:

			meanCycles = 100
			bias = 2100
			scale = 140
			adcs = [0, 0, 0, 0, 0, 0]

			for i in range(0, meanCycles):
				adcs[0] = adcs[0] + int( open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read() )
				adcs[1] = adcs[1] + int( open("/sys/bus/iio/devices/iio:device0/in_voltage1_raw").read() )
				adcs[2] = adcs[2] + int( open("/sys/bus/iio/devices/iio:device0/in_voltage2_raw").read() )
				adcs[3] = adcs[3] + int( open("/sys/bus/iio/devices/iio:device0/in_voltage3_raw").read() )
				adcs[4] = adcs[4] + int( open("/sys/bus/iio/devices/iio:device1/in_voltage0_raw").read() )
				adcs[5] = adcs[5] + int( open("/sys/bus/iio/devices/iio:device1/in_voltage1_raw").read() )

			adcs[0] = ((adcs[0] / meanCycles) - 2100) / scale
			adcs[1] = ((adcs[1] / meanCycles) - 2100) / scale
			adcs[2] = ((adcs[2] / meanCycles) - 2100) / scale
			adcs[3] = ((adcs[3] / meanCycles) - 2100) / scale
			adcs[4] = ((adcs[4] / meanCycles) )
			adcs[5] = ((adcs[5] / meanCycles) )


			print('Array   current:  ' + str(adcs[0]) )
			print('Battery current:  ' + str(adcs[1]) )
			print('Output  current:  ' + str(adcs[2]) )
			print('Pump    current:  ' + str(adcs[3]) + '\n' )


			time.sleep( 0.1 )



if __name__== "__main__":
	main()
