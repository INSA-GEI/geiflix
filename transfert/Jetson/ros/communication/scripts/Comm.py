#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import socket

HOST= '192.168.1.10'  #adresse de la jetson
PORT= 1025  #Port (les non-privileged sont >1023

msg = None
test = 1

#conn = None
#s = None

def callback(data):
    global msg

    msg = data.data
    #print(repr(data))
    #msg = data.data.encode("utf8")
    #conn.sendall(msg)



def main():
    #global conn, s

    rospy.init_node('Communication')

    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # create an INET, STREAMing socket
    #s.bind((HOST, PORT))  # bind the socket to the host, and a well-known port
    #s.listen()  # become a server socket
    #print("Listening...")
    #conn, addr = s.accept()  # accept connections from outsid
    #with conn:
        #print('connected by', addr)

    rospy.Subscriber("Motor_commands", String, callback)   
    rospy.spin()


if __name__ == '__main__':
    print ("Starting comm...")
    main()

