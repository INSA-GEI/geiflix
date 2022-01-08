#!/usr/bin/env python

import rospy
from sensor_msgs.msg import PointCloud2 as pc2
import numpy as np

pub = rospy.Publisher("/XYobject1", pc2, queue_size=10)

def callback(data):

	print "callback"


def control():

	rospy.init_node('XYobjects')

	#rospy.Subscriber("/scan", LaserScan, callback)

	rospy.spin()


if __name__ == '__main__':

	control()







