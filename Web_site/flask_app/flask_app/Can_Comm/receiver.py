import time
import datetime
import can
import time
import os
import RPi.GPIO as GPIO
import pipes


def Init_Pican():
    #Redemarrer le CAN
    os.system("sudo ifconfig can0 down")
    os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
    time.sleep(0.1)
    #Check si c'est bien et ecrire param bus pican
    try:
        bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        GPIO.output(led,False)
        exit()
    
def Can_Read(Pi_can):
    #Creation fichier, un pour stm un pour raspi
    with open("info received.txt","a") as file:
        file.truncate(0)
    with open("fire received.txt","a") as file:
        file.truncate(0)
        
        
    msg=Pi_can.recv(1)
    while (msg == None):
        msg=Pi_can.recv(1)
        time.sleep(1)

    if (msg is not None) & (msg.arbitration_id == 256 | msg.arbitration_id == 256):##message arrived or not

        return msg.arbitration_id,msg.data
    elif  (msg is not None) & (msg.arbitration_id != 256 & msg.arbitration_id != 256):
        return 0,0