
from argparse import ArgumentParser


parser = ArgumentParser()

parser.add_argument('--relay',
	'-r',
	action='store',
	default=0,
	dest='relayState',
	type=int,
	help='Set the relay state 1 on 0 off')

parser.add_argument('--relay-pin',
	action='store',
	default=36,
	dest='relayPin',
	type=int,
	help='Set the relay pin. UDOO neo pcb number')

results = parser.parse_args()

STATE = 'high' if (results.relayState != 0) else 'low'
PIN= results.relayPin

RELAY_FILE = '/gpio/pin' + str( PIN ) + '/direction'

with open(RELAY_FILE, 'w+') as f: 
	f.write(STATE) 
