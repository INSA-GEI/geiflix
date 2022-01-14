import time
import datetime
import can
import time
import os
import RPi.GPIO as GPIO
import can
import time
import os

# print("sleeping for 15 s")
# for i in range(30,0,-1):
#     time.sleep(1)
#     print(i)

MCM = 0x010
MS = 0x100
US1 = 0x000
US2 = 0x001
OM1 = 0x101
OM2 = 0x102

led = 22
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,True)

count = 0

print('\n\rCAN Rx test')
print('Bring up CAN0....')

# Bring up can0 interface at 400kbps
os.system("sudo ifconfig can0 down")
os.system("sudo /sbin/ip link set can0 up type can bitrate 400000")
time.sleep(0.1)
print('Press CTL-C to exit')

try:
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
except OSError:
    print('Cannot find PiCAN board.')
    GPIO.output(led,False)
    exit()

lines = []
i = 0
gps_data = []
all_data = []

gps_coor = []
isPath = True
index = 0
mode = 1
with open("./cutecom.log") as file_gps:
    #time.sleep(10)
    while 1:
        where = file_gps.tell()
        line = file_gps.readline()
        if not line:
                time.sleep(1)
                file_gps.seek(where)
        else:
            if(isPath):
                    try:
                        gps_coord_A = can.Message(arbitration_id=0x031,data=[43,34,14,57,1,27,58,83],extended_id=False)
                        bus.send(gps_coord_A)        
                        print("Coordinates A sent")

                        isPath = False  
                  
                    except KeyboardInterrupt:
                        #Catch keyboard interrupt
                        GPIO.output(led,False)
                        os.system("sudo /sbin/ip link set can0 down")
                        print('\n\rKeyboard interrupt: CAN down')
            if i==0:
                #lines.append(line)
                data = line.split(",")
                gps_data.append(data[2])
                gps_data.append(data[3])
                gps_data.append(data[5])
                all_data.append(gps_data)
                gps_data = []
                
            elif i%6==0:
                #lines.append(line)
                data = line.split(",")
                gps_data.append(data[2])
                gps_data.append(data[3])
                gps_data.append(data[5])
                all_data.append(gps_data)
                
                gps_coor.append(data[3].split("."))
                gps_coor.append(data[5].split("."))
                #print(gps_coor)
                
                #longitude
                long_degres = gps_coor[0][0][0:2]
                long_min = gps_coor[0][0][2:]
                long_sec = gps_coor[0][1][0:5]
                
                #latitude
                lat_degres = gps_coor[1][0][0:3]
                lat_min = gps_coor[1][0][3:5]
                lat_sec = gps_coor[1][1][0:5]
                
                #Values of longitude
                val0 = int(long_degres)
                val1 = int(long_min)
                val2 = int(int(long_sec)*10**-5*60)
                val3 = int((int(long_sec)*10**-5*60 - val2)*100)
                
                val_lo_fire = val0 + val1/60 + (int(long_sec)*10**-5*60)/3600
                
                #Values of latitude
                val4 = int(lat_degres)
                val5 = int(lat_min)
                val6 = int(int(lat_sec)*10**-5*60)
                val7 = int((int(lat_sec)*10**-5*60 - val6)*100)
                
                val_la_fire = val4 + val5/60 + (int(lat_sec)*10**-5*60)/3600
        
                if(mode == 0 and index == 0):                #flushinput()
                # Main loop
                    try:                  
                        gps_coord_RT = can.Message(arbitration_id=0x030,data=[val0,val1,val2,val3,val4,val5,val6,val7],extended_id=False)
                        bus.send(gps_coord_RT)        
                        print("ca marche")
                        index = 1
                      
                    except KeyboardInterrupt:
                        #Catch keyboard interrupt
                        GPIO.output(led,False)
                        os.system("sudo /sbin/ip link set can0 down")
                        print('\n\rKeyboard interrupt: CAN down')
                    time.sleep(1)
                    gps_coor = []
                    
                    
                elif(mode == 1):
                    try:
                        parent_conn, child_conn = Pipe()
                        p = Process(target = f, args = (child_conn,))
                        p.start()
                        if parent_conn.recv() == 'true':
                           print('bg')
                           #TODO
                           alist = [val_lo_fire, val_la_fire]
                           f = open('fire_coord.txt', 'w')
                           simplejson.dump(alist, f)
                           f.write("\n")
                           f.close()
                           
                        else:
                            print('nok')
                            #TODO
                        p.join()
                        gps_coord_RT = can.Message(arbitration_id=0x030,data=[val0,val1,val2,val3,val4,val5,val6,val7],extended_id=False)
                        bus.send(gps_coord_RT)        
                        print("ca marche")
                        print([val0, val1, val2, val3, val4, val5, val6, val7])
                        print(gps_coor)
                      
                    except KeyboardInterrupt:
                        #Catch keyboard interrupt
                        GPIO.output(led,False)
                        os.system("sudo /sbin/ip link set can0 down")
                        print('\n\rKeyboard interrupt: CAN down')
                    time.sleep(1)
                    gps_coor = []
                    
                    
                    
                gps_data = []
                
            i=i+1
        #print(all_data)