from threading import Thread
import time
import os
import struct
import socket
from math import tan,pi
import can
from simple_pid import PID
import csv


# Socket parameters (Ethernet link w/ Jetson)
HOST = ''           # IP address on LAN
PORT = 6666         # Arbitrary non-privileged port

# CAN IDs
CMC = 0x010
SSC = 0x020
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

# Speed limits
MAX_SPEED_FW = 75
MAX_SPEED_BW = 25
SPEED_STOP = 50

# Speed limits
MAX_ANGLE_L = -25
MAX_ANGLE_R = 25

# Car dimension
CAR_LEN_MM = 600

# Desired distance from target
TARGET_DIST_MM = 2000

# PID gains
PID_P = 0.02
PID_I = 0.0002
PID_D = 0

# Main thread
class EthReceiver(Thread):

    # Init
    # Params : Connected ethernet socket object, CAN bus object
    def __init__(self,connSock, canBus):
        Thread.__init__(self)
        self.connSock = connSock
        self.canBus  = canBus
        self.distance = 0
        self.angle = 0
        self.enable_speed = 0
        self.speed_cmd = 0
        self.steering = 0
        # PID object : P,I, and D gain (setpoint to default = 0)
        self.pid = PID(PID_P, PID_I, PID_D)
        self.pid.output_limits = (-25,25)

        # Lists for data logging (in csv file)
        self.listpos = []
        self.listspeed = []
        self.listangle = []
        # Time origin
        self.time0 = time.time()
        self.listtime = []

    # Thread proc (infinite)
    def run(self):
        
        while True :
            
            # Receive data from Jetson (eth)
            fromJetson = self.connSock.recv(1024)
            
            # Parse data from Jetson
            # Format : 'distance:angle:enable'
            fromJetson = fromJetson.decode('utf-8').split(":")
            try:
                rawDist = fromJetson[0]
                if rawDist: self.distance = int(rawDist)
                rawAngle = fromJetson[1]
                if rawAngle: self.angle = int(rawAngle)
                self.enable_speed = int(fromJetson[2])
            except:
                # No data -> socket closed, terminate thread
                break

            # Adjust distance to have it from the front of the car (LiDAR is placed at the back)
            self.distance -= CAR_LEN_MM
            # Compute error from desired distance
            erreur = TARGET_DIST_MM - self.distance

            # Reset PID if asked from Jetson
            if not self.enable_speed:
                self.pid.set_auto_mode(False,last_output=0)
                self.pid.set_auto_mode(True,last_output=0)
                erreur = 0

            # Compute speed command w/ PID
            self.speed_cmd = int(self.pid(erreur)) +50
            # Threshold the speed command
            if (self.speed_cmd > MAX_SPEED_FW): self.speed_cmd = MAX_SPEED_FW
            if (self.speed_cmd < MAX_SPEED_BW): self.speed_cmd = MAX_SPEED_BW

            # Enable/disable speed in motors command
            if self.enable_speed:
                self.speed_cmd |= (1 << 7)
            else:
                self.speed_cmd &= ~(1 << 7)

            # Compute the steering from the angle (-25/25 -> 0/100)
            if self.angle < MAX_ANGLE_L:
                self.steering = 0
            elif self.angle > MAX_ANGLE_R:
                self.steering = 100
            else:
                self.steering = 2*self.angle + 50

            # Enable steering in motors command
            self.steering |= (1 << 7)

            # Compose & send CAN message to Nucleo
            toNucleo = can.Message(arbitration_id=CMC,data=[self.speed_cmd, self.speed_cmd,0,self.steering],extended_id=False)
            self.canBus.send(toNucleo)

            # Log values in the console
            print("d>",self.distance,"/ a>",self.angle,"/ s>",self.speed_cmd & ~(1 << 7),"/ e>",self.enable_speed)

            # Log data
            listpos.append(self.distance)
            listangle.append(self.angle)
            listspeed.append(self.speed_cmd)
            listtime.append(time.time() - time0)

        # Out of while True loop -> connection with Jetson lost
        print("Connexion perdue.")

        # Compose & send CAN message to Nucleo to stop motors
        stopNucleo = can.Message(arbitration_id=CMC,data=[0,0,0,32,0,0,0,0],extended_id=False)
        self.canBus.send(stopNucleo)

        # Close Ethernet socket
        self.connSock.close()

        # Write logged data into csv file liste.csv
        with open('liste.csv','w',newline='') as f: #Write the data into a csv file at the end of the program
            writer=csv.writer(f)
            for i in range(len(listpos)):
                writer.writerow([listpos[i],listangle[i],listspeed[i],listtime[i]])

# Main program
if __name__ == "__main__":

    # Bringing up CAN with Linux command
    print('Démarrage du CAN....')
    os.system("sudo /sbin/ip link set can0 up type can bitrate 500000")
    time.sleep(0.1)

    # Initialising CAN interface object
    try:
        canBus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    except OSError:
        print('Carte PiCAN non trouvée.')
        exit()

    # Initialising connection with Jetson (Ethernet link w/ TCP socket)
    print('Connexion Jetson....')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))
    sock.listen(1)
    (connSock, addr) = sock.accept()
    print('Connecté à l\'adresse {0} sur le port {1}'.format(addr,PORT))

    # Initialising and starting main thread
    recvThread = EthReceiver(connSock, canBus)
    recvThread.start()
    recvThread.join()
