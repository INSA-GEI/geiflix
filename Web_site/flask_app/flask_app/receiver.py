import time
import datetime
import can
import time
import os
import RPi.GPIO as GPIO
import pipes


os.system("sudo ifconfig can0 down")
os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
time.sleep(0.1)

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    GPIO.output(led,False)
    exit()
    
with open("info received.txt","a") as file:
    file.truncate(0)
with open("fire received.txt","a") as file:
    file.truncate(0)
    
while True:
    msg=bus.recv(1)
    if msg is None:
        print("NO BUS ACTIVITY")
    if (msg is not None) & (msg.arbitration_id == 256):##message arrived or not
        with open("info received.txt","a") as file:
            data=str(msg.data)
            file.writelines(data +'\n')
        print ("data=",msg.data)
        print ("id=",msg.arbitration_id)
        time.sleep(1)
 #arrived 11 01 33 44 55 66 77 88
 #not arrived 11 00 33 44 55 66 77 88
        
    if (msg is not None) & (msg.arbitration_id == 255):##fire or not
        with open("fire received.txt","a") as file:
            data=str(msg.data)
            file.writelines(data +'\n')
        print ("data=",msg.data)
        print ("id=",msg.arbitration_id)
        time.sleep(1)

 
