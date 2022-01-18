#!/usr/bin/env python

import rospy
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
from pc_manip_tracking.msg import XYobjects
import ros_numpy
import numpy as np

#publication du topic XYobjects
pub = rospy.Publisher("XYobjects", XYobjects, queue_size=10)

#Initialisation
msg = XYobjects()

#Recuperation de la position XY objet 0
def callback0(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject0 = x
	msg.Yobject0 = y

#Recuperation de la position XY objet 1
def callback1(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject1 = x
	msg.Yobject1 = y

#Recuperation de la position XY objet 2
def callback2(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject2 = x
	msg.Yobject2 = y

#Recuperation de la position XY objet 3
def callback3(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject3 = x
	msg.Yobject3 = y

#Recuperation de la position XY objet 4
def callback4(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject4 = x
	msg.Yobject4 = y

#Recuperation de la position XY objet 5 et publication sur le topic XYobjects
def callback5(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject5 = x
	msg.Yobject5 = y
	pub.publish(msg)

#Initialisation du node et souscription a tous les topics liees aux objets du tracking
def main():

	rospy.init_node('XYobjects_processing')
	rospy.Subscriber("cluster_0", PointCloud2, callback0)
	rospy.Subscriber("cluster_1", PointCloud2, callback1)
	rospy.Subscriber("cluster_2", PointCloud2, callback2)
	rospy.Subscriber("cluster_3", PointCloud2, callback3)
	rospy.Subscriber("cluster_4", PointCloud2, callback4)
	rospy.Subscriber("cluster_5", PointCloud2, callback5)
	rospy.spin()


if __name__ == '__main__':
	print ("Starting obj_manip...")
	main()


