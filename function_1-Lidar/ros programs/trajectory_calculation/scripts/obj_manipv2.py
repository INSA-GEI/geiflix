#!/usr/bin/env python

import rospy
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
from trajectory_calculation.msg import XYobjects
import ros_numpy


import numpy as np

pub = rospy.Publisher("XYobjects", XYobjects, queue_size=10)

msg = XYobjects()

def callback0(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject0 = x
	msg.Yobject0 = y

def callback1(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject1 = x
	msg.Yobject1 = y


def callback2(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject2 = x
	msg.Yobject2 = y

def callback3(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject3 = x
	msg.Yobject3 = y

def callback4(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject4 = x
	msg.Yobject4 = y


def callback5(data):

	global pub, msg
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	msg.Xobject5 = x
	msg.Yobject5 = y
	pub.publish(msg)

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


