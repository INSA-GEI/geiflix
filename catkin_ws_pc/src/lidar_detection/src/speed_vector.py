#!/usr/bin/env python

import rospy
import numpy as np
import ros_numpy
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
import math
from std_msgs.msg import Header, Float32MultiArray, Int16
import time
from geometry_msgs.msg import PoseStamped



pub = rospy.Publisher("speed_vector", Float32MultiArray, queue_size=1)
pub_alert = rospy.Publisher("/alert", Int16, queue_size=1)

pub_fleche = rospy.Publisher("fleche", PoseStamped, queue_size=1)
pub_fleche1 = rospy.Publisher("fleche1", PoseStamped, queue_size=1)
pub_fleche2 = rospy.Publisher("fleche2", PoseStamped, queue_size=1)
pub_fleche3 = rospy.Publisher("fleche3", PoseStamped, queue_size=1)
pub_fleche4 = rospy.Publisher("fleche4", PoseStamped, queue_size=1)
pub_fleche5 = rospy.Publisher("fleche5", PoseStamped, queue_size=1)

data_last=None


def callback(data):
    global pub
    global data_last
    speed_vector=Float32MultiArray()
    fleche = PoseStamped()
    fleche1 = PoseStamped()
    fleche2 = PoseStamped()
    fleche3 = PoseStamped()
    fleche4 = PoseStamped()
    fleche5 = PoseStamped()
    
    alert = Int16()
    alert.data = 1
        
    
    if data_last is None:
    	data_last=np.asarray(data.data)
    	return
    speed_vector.layout=data.layout
    
    #print("Data nouvelle : " + str(data.data) + str(type(data.data)))
    data_list=np.asarray(data.data) #list()
    #print("Data last : " + str(data_last))
    
    speed_vector_calcul=np.array([])
    for i in range(len(data_list)):
    	difference=data_list[i]-data_last[i]
    	if abs(difference)<0.1:
    		difference=0.0
    	speed_vector_calcul=np.append(speed_vector_calcul,difference)
    speed_vector.data=tuple(speed_vector_calcul)  #.tolist()
    #print("Speed Vector : " + str(speed_vector.data) + str(type(speed_vector.data)))
    
    for i in range(6):
    	if speed_vector_calcul[i*3+1]==0:
    		continue
    	b=data_list[i*3]-(speed_vector_calcul[i*3]/speed_vector_calcul[i*3+1])*data_list[i*3+1]
    	print(b)
    	#print(speed_vector_calcul[i*3+1])
    	if b<2 and b>0 and abs(data_list[i*3+1])< abs(data_last[i*3+1]):
    		print("BIIIIIP")
    		pub_alert.publish(alert)
    		#print(i)
    		
    pub.publish(speed_vector)
    
    data_last=data_list
    
    tab_fleches=[fleche,fleche1,fleche2,fleche3,fleche4,fleche5]
    tab_pub_fleches = [pub_fleche,pub_fleche1,pub_fleche2,pub_fleche3,pub_fleche4,pub_fleche5]
    for i in range(6):
    	
    	tab_fleches[i].pose.position.x=data_list[i*3]
    	tab_fleches[i].pose.position.y=data_list[i*3+1]
    	#tab_fleches[i].pose.position.z=data_list[i*3+2]
    	tab_fleches[i].pose.position.z=0
    	
    	tab_fleches[i].pose.orientation.x=speed_vector_calcul[i*3]
    	tab_fleches[i].pose.orientation.y=speed_vector_calcul[i*3+1]
    	#tab_fleches[i].pose.orientation.z=speed_vector_calcul[i*3+2]*100
    	tab_fleches[i].pose.orientation.z=0
    	#tab_fleches[i].pose.orientation.w=1
    	tab_fleches[i].header = Header() 
    	tab_fleches[i].header.frame_id = "map"
    	tab_fleches[i].header.stamp = rospy.Time()
    	
    	if tab_fleches[i].pose.orientation.x==0 and tab_fleches[i].pose.orientation.y==0:
    		continue
    	tab_pub_fleches[i].publish(tab_fleches[i])    	
    	
     

    #rospy.sleep(0.1)
    #(abs(data_list[i*3])-abs(data_last[i*3]))<0

def main():
    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('speed_vector_detection', anonymous=False)
    rospy.Subscriber("/ccs_lowRate", Float32MultiArray, callback)
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
    

if __name__ == '__main__':
    main()


