#!/usr/bin/env python
import rospy
from std_msgs.msg import String

#Initialisation
msg=None

#Recuperation des donnees du commandes moteur et transfert dans le fichier lidar_msg.txt
def callback(data):
	global msg
	msg= data.data
	with open('/home/pi/lidar_msg.txt','r+') as myfile:
		myfile.read()
		myfile.seek(0)
		myfile.write(msg)
		myfile.truncate()

#Initialisation du node et souscription au topic Motor_commands
def listener():
	rospy.init_node('ecriture_txt')
	rospy.Subscriber("Motor_commands",String,callback)
	rospy.spin()

if __name__ == '__main__':
	listener()
