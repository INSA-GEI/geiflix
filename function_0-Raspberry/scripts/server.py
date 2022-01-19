
# coding: utf-8
from threading import Thread
import time
import can
import os
import struct
import socket
from math import tan,pi
from simple_pid import PID
import csv

HOST = ''     # IP address on LAN
PORT = 6666              # Arbitrary non-privileged port

MCM = 0x010
SSC = 0x020
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

MAX_SPEED_FW = 75
MAX_SPEED_BW = 25
SPEED_STOP = 50

CAR_LENGTH = 60
CAR_WIDTH = 40
CAR_LEN_MM = 600

TARGET_DIST_MM = 1700

MAX_ERROR_MM = 2000
MIN_ERROR_MM = -2000

PID_P = 0.02
PID_I = 0.0002
PID_D = 0

#listpos=[]
#listspeed=[]
#listangle=[]
#time0=time.time()
#listtime = []

class EthReceiver(Thread):
    def __init__(self,connSock, canBus):
        Thread.__init__(self)
        self.connSock = connSock
        self.canBus  = can.interface.Bus(channel='can0', bustype='socketcan_native')
        self.distance = 0
        self.angle = 0
        self.speed_cmd = 0
        self.enable_speed = 0
        self.speed_left = 0
        self.speed_right = 0
        self.steering = 0
        # PID object : P,I, and D gain, and setpoint
        self.pid = PID(PID_P, PID_I, PID_D)
        self.pid.output_limits = (-25,25)
        self.prev_sampling = time.time()

    def run(self): 
        self.distance = 0
        self.angle = 0
        self.enable_speed = 0
        self.speed_cmd = 0
        self.speed_left = 0
        self.speed_right = 0
        self.steering = 0
        usAvG,usAvD,usArrC,usArrG,usArrD,usAvC = 0,0,0,0,0,0
        
        while True :
            
            # Receive data from Discovery
            fromDiscov = self.canBus.recv()
            
            # Receive data from Jetson (eth)
            fromJetson = self.connSock.recv(1024)
            

            fromJetson = fromJetson.decode('utf-8').split(":")
            try:
                rawDist = fromJetson[0]
                rawAngle = fromJetson[1]
                self.enable_speed = int(fromJetson[2])
                if rawDist: self.distance = int(rawDist)
                if rawAngle: self.angle = int(rawAngle)
            except:
                print('No data from Jetson')
                break


            
            # Update speed cmd according to the distance ()
            self.distance -= CAR_LEN_MM
            erreur = TARGET_DIST_MM - self.distance

            if not self.enable_speed: # Reset PID
                self.pid.set_auto_mode(False,last_output=0)
                self.pid.set_auto_mode(True,last_output=0)
                erreur = 0

            # Compute speed command w/ PID
            
            self.speed_cmd = int(self.pid(erreur)) +50
            if (self.speed_cmd > MAX_SPEED_FW): self.speed_cmd = MAX_SPEED_FW
            if (self.speed_cmd < MAX_SPEED_BW): self.speed_cmd = MAX_SPEED_BW

            print("d>",self.distance,"/ a>",self.angle,"/ s>",self.speed_cmd,"/ e>",self.enable_speed)

            #get data to write them into a csv
            #listpos.append(self.distance)
            #listangle.append(self.angle)
            #listspeed.append(self.speed_cmd)
            #listtime.append(time.time()-time0)

            # Enable speed bit in motor colistdist.append(self.distance)
            self.speed_cmd |= (1 << 7)

            # Compute differential speed for motors NOT USED IN THE FINAL VERSION
            # self.speed_left = int(((CAR_LENGTH + CAR_WIDTH * tan(2*pi*(self.angle/360)))/CAR_LENGTH) * self.speed_cmd) + 50
            # self.speed_right = int(((CAR_LENGTH - CAR_WIDTH * tan(2*pi*(self.angle/360)))/CAR_LENGTH) * self.speed_cmd) + 50

            # Compute the steering from the angle
            if self.angle < -25: #If we are at less than 25° from the robot, we steer at the maximum in this direction
                self.steering = 0
            elif self.angle > 25: #same thing in the other direction
                self.steering = 100
            else:
                self.steering = 2*(self.angle+25) | (1 << 7)  #Else we interpolate beetween these two points to get the corresponding steering

            # Compose & send CAN message to Nucleo
            toNucleo = can.Message(arbitration_id=MCM,data=[self.speed_cmd, self.speed_cmd,0,self.steering],extended_id=False)
            self.canBus.send(toNucleo)

        print("Connexion perdue")

        stopNucleo = can.Message(arbitration_id=MCM,data=[0,0,0,32,0,0,0,0],extended_id=False)
        self.canBus.send(stopNucleo)

        self.connSock.close()

        #with open('liste.csv','w',newline='') as f: #Write the data into a csv file at the end of the program
            #writer=csv.writer(f)
            #for i in range(len(listpos)):
                #writer.writerow([listpos[i],listangle[i],listspeed[i],listtime[i]])

if __name__ == "__main__":

    print('Bring up CAN0....')
    os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
    time.sleep(0.1)

    try:
        canBus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Cannot find PiCAN board.')
        exit()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    (connSock, addr) = sock.accept()
    print('Connected by ', addr)


    recvThread = EthReceiver(connSock, canBus)
    recvThread.start()
    recvThread.join()
