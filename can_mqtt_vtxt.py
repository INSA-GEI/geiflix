import can 
import paho.mqtt.client as mqtt 
import socket 
from time import sleep
#from control_path import control_path




###############################INIT SOCKET############################################
#********************************************************
#use MQTT protocol to exchange data between Raspberry pi and GUI
#********************************************************
#initialiser l'interface can
memory_auto=None
memory_manu=None
arret_urgence=False
compteur_lidar=0
wrong_gate=False
bus = can.interface.Bus(channel='can0', bustype='socketcan_native') #activate the CAN bus

# we subscribe to the topic "test/message"
def on_connect(client, userdata,flags, rc):
    client.subscribe("test/message")
'''
verify the info sent by the GUI then send back the command via the CAN bus
 ID :SSC mode
data is composed from [speed mode,steer mode ]

'''

def on_message(client, userdata, msg):
    global compteur
    global compteur_lidar
    global wrong_gate
    #print(str(msg.payload.decode()))
    global memory_auto # activer mode manuelle
    global memory_manu  #activer mode automatique
    global arret_urgence
    if msg.payload.decode() == "MANU" : #on vérifie si l'info sur le buffer est MANU
        memory_manu=True
        memory_auto=False
        arret_urgence=False
        compteur_lidar=0
        wrong_gate=False

    elif msg.payload.decode() == "AUTO" : #on vérifie si l'info sur le buffer est AUTO
        memory_manu=False
        memory_auto=True
        print("auto_reçu")
    
    elif msg.payload.decode()=="Arret_Urgence" :
        arret_urgence=True
        msg = can.Message(arbitration_id=0x020, data=[0x32,0x32], extended_id=False)
        bus.send(msg)
        compteur_lidar=0
        wrong_gate=False
        print("arret urgence")

    if memory_manu and not(arret_urgence):
        print("in Manu")
        if msg.payload.decode() == "avancer":                   
            msg = can.Message(arbitration_id=0x020, data=[0x4B,0x32], extended_id=False)
            bus.send(msg)
        elif msg.payload.decode() == "reculer":
            msg = can.Message(arbitration_id=0x020, data=[0x0A,0x32], extended_id=False)
            bus.send(msg)
        elif msg.payload.decode() == "Arret_Urgence":
            msg = can.Message(arbitration_id=0x020, data=[0x32,0x32], extended_id=False)
            bus.send(msg)
            arret_urgence=True
        #droite a fond
        elif msg.payload.decode() == "droite":
            msg = can.Message(arbitration_id=0x020, data=[0x41,0x5A], extended_id=False)
            bus.send(msg)
        #gauche fond
        elif msg.payload.decode() == "gauche":
            msg = can.Message(arbitration_id=0x020, data=[0x41,0x0A], extended_id=False)
            bus.send(msg)
            #medium gauche
        elif msg.payload.decode() == "avancer_gauche":
            msg = can.Message(arbitration_id=0x020, data=[0x41,0x19], extended_id=False)
            bus.send(msg)
        elif msg.payload.decode() == "avancer_droite":
            msg = can.Message(arbitration_id=0x020, data=[0x41,0x4B], extended_id=False)
            bus.send(msg)
        elif msg.payload.decode() == "reculer_droite":
            msg = can.Message(arbitration_id=0x020, data=[0x28,0x4B], extended_id=False)
            bus.send(msg)
        elif msg.payload.decode() == "reculer_gauche":
            msg = can.Message(arbitration_id=0x020, data=[0x28,0x19], extended_id=False)
            bus.send(msg)
    # AUTOMATIC MODE : read commands into the txt file written by raspberry_vtxt.py
    if memory_auto and not(arret_urgence):
        print("processing auto mode")
        correction_file=open("/home/pi/can_msg.txt")
        correction=correction_file.read()
        correction_file.close()
        # WRONG GATE DETECTED -> the car doesn't move or stop 
        if correction=="wrong_gate":
            print("ONE WRONG GATE")
            wrong_gate=True
            msg = can.Message(arbitration_id=0x020, data=[50,50], extended_id=False)
            bus.send(msg)
            compteur_lidar=0
        # message CAN after correction by proportional corrector
        if correction!='NONE/' and compteur_lidar<1000 and not(wrong_gate) and correction!='NONE':
            correction=correction.split('/')
            speed=int(correction[0])
            steer=int(correction[1])
            # if the car is stopeed -> increment lidar counter
            if [speed,steer]==[50,50]:
                compteur_lidar+=1
            else:
                compteur_lidar=0
            print([speed,steer])
            msg = can.Message(arbitration_id=0x020, data=[speed,steer], extended_id=False)
            bus.send(msg)
        # keep the last command -> avoid little loss of aruco code detection
        elif correction=='NONE/' and compteur_lidar<1000 and not(wrong_gate):
            print("keep the last command")
        # LIDAR MODE -> when the car can't see the aruco codes (the gate) anymore
        elif compteur_lidar>=1000 and compteur_lidar<2000 and not(wrong_gate):
            fichier = open("/home/pi/lidar_msg.txt","r")
            lidar_msg = fichier.read()
            fichier.close()
            if lidar_msg == "avancer":
                msg = can.Message(arbitration_id=0x020, data=[0x4B, 0x32], extended_id=False)
                bus.send(msg)
                print("avancer")
            # Gate behind the car -> STOP THE CAR
            elif lidar_msg == "stop":
                msg = can.Message(arbitration_id=0x020, data=[0x32, 0x32], extended_id=False)
                bus.send(msg)
                print("stop")
                compteur_lidar+=1000
                



client = mqtt.Client()                    #create a mqtt client object
client.on_connect = on_connect            #connect to the broker
client.on_message = on_message            # attach function to callback
client.connect("192.168.0.250",1883,60)   # connect with the address of the publisher
client.loop_forever()                     # the program run indefinitely

