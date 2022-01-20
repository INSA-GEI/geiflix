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


        # messaga received from server : camera data (error and direction) 
        data = s.recv(1024)
        # conversion to correction string -> txt file
        data=str(data.decode('ascii'))

        # print the received message
        data = data.split(' ')

        # fill txt file and incrementing counter that keeps the last command (avoid little loss of aruco gate detection) 
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

    # close the connection
    s.close()


if __name__ == '__main__':
    Main()
