#!/usr/bin/env python

import rospy
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Float32
import ros_numpy


import numpy as np

pub01 = rospy.Publisher("Xobject0", Float32, queue_size=10)
pub02 = rospy.Publisher("Yobject0", Float32, queue_size=10)

pub11 = rospy.Publisher("Xobject1", Float32, queue_size=10)
pub12 = rospy.Publisher("Yobject1", Float32, queue_size=10)

pub21 = rospy.Publisher("Xobject2", Float32, queue_size=10)
pub22 = rospy.Publisher("Yobject2", Float32, queue_size=10)

pub31 = rospy.Publisher("Xobject3", Float32, queue_size=10)
pub32 = rospy.Publisher("Yobject3", Float32, queue_size=10)

pub41 = rospy.Publisher("Xobject4", Float32, queue_size=10)
pub42 = rospy.Publisher("Yobject4", Float32, queue_size=10)

pub51 = rospy.Publisher("Xobject5", Float32, queue_size=10)
pub52 = rospy.Publisher("Yobject5", Float32, queue_size=10)

def callback0(data):

	global pub01, pub02
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	data=x
	pub01.publish(data)
	data=y
	pub02.publish(data)

def callback1(data):

	global pub11, pub12
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	data=x
	pub11.publish(data)
	data=y
	pub12.publish(data)

def callback2(data):

	global pub21, pub22
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	data=x
	pub21.publish(data)
	data=y
	pub22.publish(data)

def callback3(data):

	global pub31, pub32
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	data=x
	pub31.publish(data)
	data=y
	pub32.publish(data)

def callback4(data):

	global pub41, pub42
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	data=x
	pub41.publish(data)
	data=y
	pub42.publish(data)

def callback5(data):

	global pub51, pub52
	for coordinates in pc2.read_points(data, field_names = ("x","y","z","intensity"), skip_nans=True):
		x=coordinates[0]
		y=coordinates[1]
	data=x
	pub51.publish(data)
	data=y
	pub52.publish(data)


def main():

	rospy.init_node('Processing')
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


