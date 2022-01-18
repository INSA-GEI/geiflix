# Import socket module
import socket
from control_path_txt import control_path
#import keyboard
import time
def Main():
    # local host IP '127.0.0.1'
    # adress client
    host = '192.168.1.10'

    # Define the port on which you want to connect
    port = 1025

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))

    # message you send to server
    message = "running"
    compteur=0

    while True:

        # message sent to server
        s.send(message.encode('ascii'))


        # messaga received from server
        data = s.recv(1024)
        #fichier=open("lidar_msg.txt","r")
        #lidar_msg=fichier.read()
        #fichier.close()
        #print(lidar_msg)
        # CORRECTION A FAIRE ICI
       # if fichier.read()=="avancer":
        data=str(data.decode('ascii'))

        # print the received message
        data = data.split(' ')

        # here it would be a reverse of sent message
        
       # print('Received from the server :', data)
        if data[1]=='not_gate':
            compteur+=1
            copyIntoTxt=control_path(data,compteur=compteur)
            with open('/home/pi/can_msg.txt','r+') as myfile:
                myfile.read()
                myfile.seek(0)
                myfile.write(copyIntoTxt)
                myfile.truncate()

        #################################
        elif data[1]=='wrong_gate':
            with open('/home/pi/can_msg.txt','r+') as myfile:
                myfile.read()
                myfile.seek(0)
                myfile.write("wrong_gate")
                myfile.truncate()

        else:
            compteur=0

            copyIntoTxt=control_path(data,compteur=compteur)

            with open('can_msg.txt','r+') as myfile:
                myfile.read()
                myfile.seek(0)
                myfile.write(copyIntoTxt)
                myfile.truncate()

       # else:
        #    compteur=0
         #   lidar_command=[50,'straight']
          #  control_path(lidar_command,compteur=compteur)
        #print('Received from the server :', str(data))

        # ask the client whether he wants to continue
        #ans = input('\nDo you want to continue(y/n) :')

 #       if keyboard.is_pressed('q'):
 #           break# if key 'q' is pressed
        #if ans == 'y':
            #continue
        #else:
        #    break
    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
