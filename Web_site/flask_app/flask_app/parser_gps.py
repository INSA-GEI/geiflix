import time
import datetime
import can
import os
import RPi.GPIO as GPIO
from receiver import Init_Pican

#This function has one parameter named bus (CAN bus). This function get from a
#file the desired coordinates and send it via CAN frames for the predefined path.
def Path_Init(bus):
    path=[] #List for the coordinates of the predefined path.
    path_point = 0 #Counter for the number of lines on the considered file.
    value = 0 #Variable to store a list of coordinates.
    with open("path_coord.txt", "r") as data_file: #Opening of the file containing coordinates of the fire detected
        #Verification that the file contains at least 5 lines.
        while 1:
            num_lines = sum(1 for line in data_file)
            if num_lines >= 5:
                break
        data_file.close()
        
        #Read the 5 coordinates in the current file and store it in a list.
        while len(path) < 5  and path_point < 5:
            file = open("path_coord.txt", "r")
            line = file.readline()
            while line:
                value = json.loads(line) #Convert a list from a file in real list (Here int list).
                path.append(value)
                path_point += 1
                line = file.readline()
            file.close()
            
        #Convert decimal degrees to DMS (Degres Minutes Seconds)
        A_deg_la = int(path[4][0])
        A_min_la = int((path[4][0]-A_deg_la)*60) 
        A_sec_la = int(((path[4][0]-A_deg_la)*60-A_min_la)*60) 
        A_sec_sec_la = int((((path[4][0]-A_deg_la)*60-A_min_la)*60 - A_sec_la)*60)      
        A_deg_lo = int(path[4][1])
        A_min_lo = int((path[4][1]-A_deg_lo)*60)
        A_sec_lo = int(((path[4][1]-A_deg_lo)*60-A_min_lo)*60)
        A_sec_sec_lo = int((((path[4][1]-A_deg_lo)*60-A_min_lo)*60 - A_sec_lo)*60)

        B_deg_la = int(path[3][0])
        B_min_la = int((path[3][0]-A_deg_la)*60) 
        B_sec_la = int(((path[3][0]-A_deg_la)*60-A_min_la)*60) 
        B_sec_sec_la = int((((path[3][0]-A_deg_la)*60-A_min_la)*60 - A_sec_la)*60)      
        B_deg_lo = int(path[3][1])
        B_min_lo = int((path[3][1]-A_deg_lo)*60)
        B_sec_lo = int(((path[3][1]-A_deg_lo)*60-A_min_lo)*60)
        B_sec_sec_lo = int((((path[3][1]-A_deg_lo)*60-A_min_lo)*60 - A_sec_lo)*60)

        C_deg_la = int(path[2][0])
        C_min_la = int((path[2][0]-A_deg_la)*60) 
        C_sec_la = int(((path[2][0]-A_deg_la)*60-A_min_la)*60) 
        C_sec_sec_la = int((((path[2][0]-A_deg_la)*60-A_min_la)*60 - A_sec_la)*60)      
        C_deg_lo = int(path[2][1])
        C_min_lo = int((path[2][1]-A_deg_lo)*60)
        C_sec_lo = int(((path[2][1]-A_deg_lo)*60-A_min_lo)*60)
        C_sec_sec_lo = int((((path[2][1]-A_deg_lo)*60-A_min_lo)*60 - A_sec_lo)*60)

        D_deg_la = int(path[1][0])
        D_min_la = int((path[1][0]-A_deg_la)*60) 
        D_sec_la = int(((path[1][0]-A_deg_la)*60-A_min_la)*60) 
        D_sec_sec_la = int((((path[1][0]-A_deg_la)*60-A_min_la)*60 - A_sec_la)*60)      
        D_deg_lo = int(path[1][1])
        D_min_lo = int((path[1][1]-A_deg_lo)*60)
        D_sec_lo = int(((path[1][1]-A_deg_lo)*60-A_min_lo)*60)
        D_sec_sec_lo = int((((path[1][1]-A_deg_lo)*60-A_min_lo)*60 - A_sec_lo)*60)

        E_deg_la = int(path[0][0])
        E_min_la = int((path[0][0]-A_deg_la)*60) 
        E_sec_la = int(((path[0][0]-A_deg_la)*60-A_min_la)*60) 
        E_sec_sec_la = int((((path[0][0]-A_deg_la)*60-A_min_la)*60 - A_sec_la)*60)      
        E_deg_lo = int(path[0][1])
        E_min_lo = int((path[0][1]-A_deg_lo)*60)
        E_sec_lo = int(((path[0][1]-A_deg_lo)*60-A_min_lo)*60)
        E_sec_sec_lo = int((((path[0][1]-A_deg_lo)*60-A_min_lo)*60 - A_sec_lo)*60)

        #Send the 5 coordinates via CAN frames.
        try:
            gps_coord_A = can.Message(arbitration_id=0x031,data=[A_deg_la,A_min_la,A_sec_la,A_sec_sec_la,A_deg_lo,A_min_lo,A_sec_lo,A_sec_sec_lo],extended_id=False)
            bus.send(gps_coord_A)        
            print("Coordinates A sent")
            
            time.sleep(2)
            
            gps_coord_B = can.Message(arbitration_id=0x031,data=[B_deg_la,B_min_la,B_sec_la,B_sec_sec_la,B_deg_lo,B_min_lo,B_sec_lo,B_sec_sec_lo],extended_id=False)
            bus.send(gps_coord_B)        
            print("Coordinates B sent")
            
            time.sleep(2)
            
            gps_coord_C = can.Message(arbitration_id=0x031,data=[C_deg_la,C_min_la,C_sec_la,C_sec_sec_la,C_deg_lo,C_min_lo,C_sec_lo,C_sec_sec_lo],extended_id=False)
            bus.send(gps_coord_C)        
            print("Coordinates C sent")
            
            time.sleep(2)
            
            gps_coord_D = can.Message(arbitration_id=0x031,data=[D_deg_la,D_min_la,D_sec_la,D_sec_sec_la,D_deg_lo,D_min_lo,D_sec_lo,D_sec_sec_lo],extended_id=False)
            bus.send(gps_coord_D)        
            print("Coordinates D sent")
            
            time.sleep(2)
            
            gps_coord_E = can.Message(arbitration_id=0x031,data=[E_deg_la,E_min_la,E_sec_la,E_sec_sec_la,E_deg_lo,E_min_lo,E_sec_lo,E_sec_sec_lo],extended_id=False)
            bus.send(gps_coord_E)        
            print("Coordinates E sent")

        except KeyboardInterrupt:
            #Catch keyboard interrupt
            GPIO.output(led,False)
            os.system("sudo /sbin/ip link set can0 down")
            print('\n\rKeyboard interrupt: CAN down')
    
#This function reads in real time the file with the actual GPS coordinates. Then, an average is made with
#3 coordinates of this file.
def Gps_Read():
    counter = 0
    alist = [] #List to store the 3 coordinates.
    #Verification to get 3 actual coordinates from the GPS coordinates file.
    while counter < 3:
        file = open("degrees_coord.txt", "r")
        line = file.readline()
        value = json.loads(line) #Convert a list from a file in real list (Here int list).
        alist.append(value)
        counter =+ 1
        file.close()
        timer.sleep(3) #Wainting 3 seconds.
    
    average_la = (alist[0][0] + alist[1][0] + alist[2][0])/3 #Average for latitude.
    average_lo = (alist[0][1] + alist[1][1] + alist[2][1])/3 #Average for longitude.
    
    alist1 = [average_la, average_lo]
    f = open('fire_coord.txt', 'w')
    simplejson.dump(alist1, f) #Write the average of coordinates on a file.
    f.write("\n")
    f.close()
                   
if __name__ == "__main__":

    #Constants concerning the motor control.
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
    i = 0 #Index for lines of the file containing the actual GPS coordinates.
    gps_data = [] #Get the actual GPS data from the file.
    all_data = [] #Store all the actual GPS data thanks to gps_data list.
    gps_coor = [] #List containing the actual and current latitude and longitude.
    index = 0 #Lock dor the mode 0 in order to get just one actual GPS coordniates.
    mode = 1 #Mode of sending actual GPS coordinates via CAN frames. 0 for sending only one frame and 1 for sending all frames in real time.
    with open("./cutecom.log") as file_gps:
        #Read in real time the actual GPS coordiantes file.
        while 1:
            where = file_gps.tell()
            line = file_gps.readline()
            if not line:
                    time.sleep(1)
                    file_gps.seek(where)
            else:
                #Get the first actual coordinate.
                if i==0:
                    data = line.split(",")
                    gps_data.append(data[2])
                    gps_data.append(data[3])
                    gps_data.append(data[5])
                    all_data.append(gps_data)
                    gps_data = []
                    
                #Get at each 6 lines the actual coordinates.
                elif i%6==0:
                    data = line.split(",")
                    gps_data.append(data[2])
                    gps_data.append(data[3])
                    gps_data.append(data[5])
                    all_data.append(gps_data)
                    
                    gps_coor.append(data[3].split("."))
                    gps_coor.append(data[5].split("."))
                    
                    #latitude in Degrees Minutes
                    lat_degres = gps_coor[0][0][0:2]
                    lat_min = gps_coor[0][0][2:]
                    lat_sec = gps_coor[0][1][0:5]
                    
                    #longitude in Degrees Minutes
                    long_degres = gps_coor[1][0][0:3]
                    long_min = gps_coor[1][0][3:5]
                    long_sec = gps_coor[1][1][0:5]
                    
                    #Values of latitude in DMS (Degrees Minutes Seconds)
                    val0 = int(lat_degres)
                    val1 = int(lat_min)
                    val2 = int(int(lat_sec)*10**-5*60)
                    val3 = int((int(lat_sec)*10**-5*60 - val2)*100)
                    
                    #Values of latitude in Decimal Degrees
                    val_la = val0 + val1/60 + (int(lat_sec)*10**-5*60)/3600
                    
                    #Values of longitude in DMS (Degrees Minutes Seconds)
                    val4 = int(long_degres)
                    val5 = int(long_min)
                    val6 = int(int(long_sec)*10**-5*60)
                    val7 = int((int(long_sec)*10**-5*60 - val6)*100)
                    
                    #Value of longitude in Decimal Degrees
                    val_lo = val4 + val5/60 + (int(long_sec)*10**-5*60)/3600
                    
                    alist = [val_la, val_lo] #Store coordinates on a list.
                    f = open('degrees_coord.txt', 'w')
                    simplejson.dump(alist, f) #Write coordinates in Decimal Degrees format on the current file.
                    f.write("\n")
                    f.close()
            
                    #In this mode only one actual GPS coordinate in DMS is sent via CAN frames.
                    if(mode == 0 and index == 0):            
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
                        
                    #In this mode the actual GPS coordinate in DMS are sent via CAN frames.
                    elif(mode == 1):
                        try:
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