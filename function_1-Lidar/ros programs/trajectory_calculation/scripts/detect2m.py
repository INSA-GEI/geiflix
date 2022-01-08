#!/usr/bin/env python

import rospy
from trajectory_calculation.msg import XYobjects, objects2m
from math import *
import ros_numpy


import numpy as np

pub = rospy.Publisher("Objects2m", objects2m, queue_size=10)

msg = objects2m()

def callback(data):

	global pub, msg
	xobject0=data.Xobject0
	yobject0=data.Yobject0

	xobject1=data.Xobject1
	yobject1=data.Yobject1

	xobject2=data.Xobject2
	yobject2=data.Yobject2

	xobject3=data.Xobject3
	yobject3=data.Yobject3

	xobject4=data.Xobject4
	yobject4=data.Yobject4

	xobject5=data.Xobject5
	yobject5=data.Yobject5

	#Detection a 2m objet 0
	msg.Dist_obj0=sqrt(xobject0**2+yobject0**2)
	if msg.Dist_obj0<=2 and msg.Dist_obj0>0.0:
		msg.Detect2m_obj0 = True
	else :
		msg.Detect2m_obj0 = False

	#Detection a 2m objet 1
	msg.Dist_obj1=sqrt(xobject1**2+yobject1**2)
	if msg.Dist_obj1<=2 and msg.Dist_obj1>0.0:
		msg.Detect2m_obj1 = True
	else :
		msg.Detect2m_obj1 = False

	#Detection a 2m objet 2
	msg.Dist_obj2=sqrt(xobject2**2+yobject2**2)
	if msg.Dist_obj2<=2 and msg.Dist_obj2>0.0:
		msg.Detect2m_obj2 = True
	else :
		msg.Detect2m_obj2 = False

	#Detection a 2m objet 3
	msg.Dist_obj3=sqrt(xobject3**2+yobject3**2)
	if msg.Dist_obj3<=2 and msg.Dist_obj3>0.0:
		msg.Detect2m_obj3 = True
	else :
		msg.Detect2m_obj3 = False

	#Detection a 2m objet 4
	msg.Dist_obj4=sqrt(xobject4**2+yobject4**2)
	if msg.Dist_obj4<=2 and msg.Dist_obj4>0.0:
		msg.Detect2m_obj4 = True
	else :
		msg.Detect2m_obj4 = False

	#Detection a 2m objet 5
	msg.Dist_obj5=sqrt(xobject5**2+yobject5**2)
	if msg.Dist_obj5<=2 and msg.Dist_obj5>0.0:
		msg.Detect2m_obj5 = True
	else :
		msg.Detect2m_obj5 = False
	
	pub.publish(msg)



def main():

	rospy.init_node('Detection_2_metres')
	rospy.Subscriber("XYobjects", XYobjects, callback)
	rospy.spin()


if __name__ == '__main__':
	print ("Starting detect2m...")
	main()


