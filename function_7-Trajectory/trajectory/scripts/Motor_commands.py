#!/usr/bin/env python

import rospy
from pc_manip_tracking.msg import objects2m, XYobjects
from std_msgs import String
import numpy as np

pub = rospy.Publisher("Motor_commands", String, queue_size=10)

global etape = 0
global gate_detecte = False

def callback2(data):
    global etape, gate_detecte

    obj0 = data.Detect2m_obj0
    obj1 = data.Detect2m_obj1
    obj2 = data.Detect2m_obj2
    obj3 = data.Detect2m_obj3
    obj4 = data.Detect2m_obj4
    obj5 = data.Detect2m_obj5
    
    if etape == 2 :

        if (obj0 and obj1) or (obj0 and obj2) or (obj0 and obj3) or (obj0 and obj4) or (obj0 and obj5)
        or (obj1 and obj2) or (obj1 and obj3) or (obj1 and obj4) or (obj1 and obj5)
        or (obj2 and obj3) or (obj2 and obj4) or (obj2 and obj5)
        or (obj3 and obj4) or (obj3 and obj5)
        or (obj4 and obj5) :

                gate_detecte = True
        
    

def callback3(data):
    global etape, gate_detecte

    if etape == 2 and gate_detecte :

        

    


def main():

    rospy.init_node('Motor_commands')
    rospy.Subscriber("objects2m", objects2m, callback2)
    rospy.Subscriber("XYobjects", XYobjects, callback3)
        
    rospy.spin()


if __name__ == '__main__':
    print ("Starting motor_commands...")
    main()

