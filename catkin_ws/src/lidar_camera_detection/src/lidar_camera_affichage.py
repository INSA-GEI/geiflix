#!/usr/bin/env python


import rospy
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import Image, CameraInfo, PointCloud2, PointField
import numpy as np
import ros_numpy
import math
from std_msgs.msg import Header
import image_geometry
import message_filters
import cv2
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D



CV_BRIDGE = CvBridge()


def affichage_lidar_camera(lidar_pointsCloud2D, camera_image, image_pub):
    try:
        img = CV_BRIDGE.imgmsg_to_cv2(camera_image, 'bgr8')
    except CvBridgeError as e:
        rospy.logerr(e)
        return

    print("ici")


    points2D = ros_numpy.point_cloud2.pointcloud2_to_array(lidar_pointsCloud2D)
    points2D = np.asarray(points2D.tolist())

    max_intensity = np.max(points2D[:, 3])

    
    # Color map for the points
    cmap = matplotlib.cm.get_cmap('jet')
    colors = cmap(points2D[:, 3] / max_intensity) * 255


 
    inrange = np.where((points2D[:, 0] >= 0) &
                       (points2D[:, 1] >= 0) &
                       (points2D[:, 0] < img.shape[1]) &
                       (points2D[:, 1] < img.shape[0]))
    points2D = points2D[inrange[0]].round().astype('int')
    points2D = points2D.reshape(-1, 2)

    for i in range(len(points2D)):
        cv2.circle(img, tuple(points2D[i]), 2, tuple(colors[i]), -1)

    # Publish the projected points image
    try:
        image_pub.publish(CV_BRIDGE.cv2_to_imgmsg(img, "bgr8"))
    except CvBridgeError as e: 
        rospy.logerr(e)


def main():
    
    rospy.init_node('LIDAR_CAM_AFFICHAGE', anonymous=False)
    lidar_points2D = '/coordinates_lidar_2d'
    image = '/usb_cam/image_color'

    image_sub = message_filters.Subscriber(image, Image)
    lidar_sub = message_filters.Subscriber(lidar_points2D, PointCloud2)
    
    image_pub = rospy.Publisher("/usb_cam/camera_lidar", Image, queue_size=5)


    ats = message_filters.ApproximateTimeSynchronizer(
            [lidar_sub,image_sub], queue_size=5, slop = 0.1)

    ats.registerCallback(affichage_lidar_camera, image_pub)


    rospy.spin()

if __name__ == '__main__':
    main()
