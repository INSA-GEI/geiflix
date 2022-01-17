#!/usr/bin/env python

import rospy
from vision_msgs.msg import Detection2DArray
import time
import os
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import Image, PointCloud2, PointField
import numpy as np
import math
from std_msgs.msg import Header, Int16
import ros_numpy
import cv2
import message_filters
from cv_bridge import CvBridge, CvBridgeError

font                   = cv2.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,500)
fontScale              = 1
fontColor              = (255,255,255)
thickness              = 1
lineType               = 2

pointCloudtest = None

CV_BRIDGE = CvBridge()
class Detection:
    def __init__(self):
        self.pointCloud = None
        self.pubAlerte = rospy.Publisher("/alert", Int16, queue_size=1)

    def lidar_pc_callback(self, data):
        global pointCloudtest
        points = ros_numpy.point_cloud2.pointcloud2_to_array(data)
        pointCloudtest = np.asarray(points.tolist())

    def camera_detection_callback(self, camera_image, data, image_pub):
        global pointCloudtest


        try:
            img = CV_BRIDGE.imgmsg_to_cv2(camera_image, 'bgr8')
        except CvBridgeError as e:
            rospy.logerr(e)
            return

        if pointCloudtest  is not None:
            #Pour chaque objet, on cherche leur distance
            for detection in data.detections:
                center_x = detection.bbox.center.x
                center_y = detection.bbox.center.y
                closest_point = None
                for point in pointCloudtest:
                    if abs(center_x - point[0]) < 150 and abs(center_y - point[1]) <150:
                        if closest_point is None or point[2] < closest_point:
                            closest_point = point[2]

                cv2.putText(img,str(closest_point), (int(center_x),int(center_y)), font,
                            fontScale,
                            fontColor,
                            thickness)

                if (closest_point is not None and closest_point <= 1 and detection.results[0].id == 1):
                    alerte = Int16()
                    alerte.data = 1
                    self.pubAlerte.publish(alerte)


        # Publish the projected points image
        try:
            image_pub.publish(CV_BRIDGE.cv2_to_imgmsg(img, "bgr8"))
        except CvBridgeError as e: 
            rospy.logerr(e)


    
def main():

    rospy.init_node('lidar_camera_detection', anonymous=False)
    image_detection = '/detectnet/overlay'
    data_detection = '/detectnet/detections'

    detection = Detection()
    img_detection_sub = message_filters.Subscriber(image_detection, Image)
    data_detection_sub = message_filters.Subscriber(data_detection, Detection2DArray)


    image_pub = rospy.Publisher("/usb_cam/cam_with_dist", Image, queue_size=1)

    ats =  message_filters.ApproximateTimeSynchronizer(
            [img_detection_sub,data_detection_sub], queue_size=1, slop = 10)

    ats.registerCallback(detection.camera_detection_callback, image_pub)

    rospy.Subscriber("/coordinates_lidar_2d", PointCloud2, detection.lidar_pc_callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    main()
