#!/usr/bin/env python



# Built-in modules
import time

# External modules
import rospy
import cv2
import numpy as np
import matplotlib.cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ROS modules
PKG = 'lidar_detection'
import roslib; roslib.load_manifest(PKG)
import tf2_ros
import ros_numpy
from tf.transformations import euler_from_matrix
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from sensor_msgs.msg import PointCloud2
from cv_bridge import CvBridge, CvBridgeError


pub = rospy.Publisher("rslidar_points_transfo", PointCloud2, queue_size=1)
CV_BRIDGE = CvBridge()


def project_point_cloud(pointCloud):
    # Transform the point cloud
    
    try:
        transform = TF_BUFFER.lookup_transform('world', 'velodyne', rospy.Time())
        pointCloud = do_transform_cloud(pointCloud, transform)
    except tf2_ros.LookupException:
        pass

    pub.publish(pointCloud)


    



def callback(lidar):
    global TF_BUFFER, TF_LISTENER

    # TF listener
    TF_BUFFER = tf2_ros.Buffer()
    TF_LISTENER = tf2_ros.TransformListener(TF_BUFFER)

    # Projection/display mode
    project_point_cloud(lidar)





def main():

    # Subscribe to topics
    rospy.init_node("Lidar_Transformation", anonymous=False)
    rospy.Subscriber("/coordinates_close", PointCloud2, callback)

    # Keep python from exiting until this node is stopped
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo('Shutting down')



if __name__ == '__main__':
    main()
