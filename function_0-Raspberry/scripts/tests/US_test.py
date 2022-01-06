#!/usr/bin/python3
#
# simple_tx_test.py
#
# This python3 sent CAN messages out, with byte 7 increamenting each time.
# For use with PiCAN boards on the Raspberry Pi
# http://skpang.co.uk/catalog/pican2-canbus-board-for-raspberry-pi-2-p-1475.html
#
# Make sure Python-CAN is installed first http://skpang.co.uk/blog/archives/1220
#
# 01-02-16 SK Pang
#
#
#


import can
import time
import os
import struct


MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

# led = 22
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(led,GPIO.OUT)
# GPIO.output(led,True)

count = 0

print('\n\rCAN Rx test')
print('Bring up CAN0....')

# Bring up can0 interface at 500kbps
os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
time.sleep(0.1)
print('Press CTL-C to exit')

try:
	bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
	print('Cannot find PiCAN board.')
	GPIO.output(led,False)
	exit()

# Main loop
try:
	obstacle=False
	while True:
		msg = bus.recv()
		if (msg.arbitration_id == US1) :
			# ultrason avant droit
			distance = int.from_bytes(msg.data[2:4], byteorder='big')
			# message = "AvD:" + str(distance)+ ";"
			# print(message)
			if (distance > 50):
				obstacle=False
				
			else :
				msg = can.Message(arbitration_id=0x010,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x41,0x19],extended_id=False) # tourner un peu gauche
			    bus.send(msg)
		if (msg.arbitration_id == US2) and (obstacle==False):
			# ultrason avant centre
			distance = int.from_bytes(msg.data[4:6], byteorder='big')
			# message = "AvC:" + str(distance)+ ";"
			# print(message)
			if distance > 50:
			    obstacle=False
			else :
				msg = can.Message(arbitration_id=0x010,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x41,0x4B],extended_id=False) # tourner un peu a droite
			    bus.send(msg)
		if (msg.arbitration_id == US1) and (obstacle==False):
			# ultrason avant gauche
			distance = int.from_bytes(msg.data[0:2], byteorder='big')
			# message = "AvC:" + str(distance)+ ";"
			# print(message)
			if distance > 50:
				obstacle=False
			else :
				msg = can.Message(arbitration_id=0x010,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x41,0x4B],extended_id=False) # tourner un peu a droite
			    bus.send(msg)
    
		if obstacle==False:
			msg = can.Message(arbitration_id=0x010,data=[0xBC,0xBC,0x00, 0x00, 0x00, 0x00,0x00, 0x00],extended_id=False) # juste avance  60 rpm 
			bus.send(msg)
		
		#count +=1
		#time.sleep(0.1)
		# GPIO.output(led,False)
		#time.sleep(0.1)
		#print(count)

except KeyboardInterrupt:
	#Catch keyboard interrupt
	GPIO.output(led,False)
	os.system("shem")
	print('\n\rKeyboard interrtupt')