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
import tf2_ros
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from tf.transformations import euler_from_matrix
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.cm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2


CAMERA_MODEL = image_geometry.PinholeCameraModel()
FIRST_TIME = True
TF_BUFFER = None
TF_LISTENER = None

CV_BRIDGE = CvBridge()


def calcul_dist(point):
    return math.sqrt(point[0]*point[0]+point[1]*point[1]+point[2]*point[2])

def point_cloud_transform(pointCloud):
    global TF_BUFFER, TF_LISTENER

    try:
        transform = TF_BUFFER.lookup_transform('world', 'velodyne', rospy.Time())
        pointCloud = do_transform_cloud(pointCloud, transform)
    except tf2_ros.LookupException:
        pass

    return pointCloud


def send_pointcloud(points2D, stamp, publisher):
    fields = [PointField('x', 0, PointField.FLOAT32, 1),
              PointField('y', 4, PointField.FLOAT32, 1),
              PointField('distance', 8, PointField.FLOAT32, 1),
              PointField('intensity',12, PointField.FLOAT32,1),
              ]

    print("ici")

    header = Header()
    header.frame_id = "map"
    newData = pc2.create_cloud(header, fields, points2D)
    newData.header.stamp = stamp
    publisher.publish(newData)




def callback(camera_info, data, camera_image, pub, image_pub):
    global CAMERA_MODEL, FIRST_TIME, TF_BUFFER, TF_LISTENER

    try:
        img = CV_BRIDGE.imgmsg_to_cv2(camera_image, 'bgr8')
    except CvBridgeError as e:
        rospy.logerr(e)
        return

    print("ici")
    if FIRST_TIME:
        FIRST_TIME = False
        CAMERA_MODEL.fromCameraInfo(camera_info)
        TF_BUFFER = tf2_ros.Buffer()
        TF_LISTENER = tf2_ros.TransformListener(TF_BUFFER)

    stamp = data.header.stamp

    data = point_cloud_transform(data)

    points3D = ros_numpy.point_cloud2.pointcloud2_to_array(data)
    points3D = np.asarray(points3D.tolist())



    #FIlter points
    inrange = np.where((points3D[:, 2] > -1) &
                       (points3D[:, 2] < 3) &
                       (np.abs(points3D[:, 0]) < 3) &
                       (np.abs(points3D[:, 1]) < 3))
    max_intensity = np.max(points3D[:, 3])
    points3D = points3D[inrange[0]]



    # Project to 2D and filter points within image boundaries

    points2D = [] 

    for i in range(len(points3D)):
        x_y = CAMERA_MODEL.project3dToPixel(points3D[i, :3])
        points2D.append([x_y[0], x_y[1], calcul_dist(points3D[i, :3]), points3D[i, 3]])


    #points2D = [[CAMERA_MODEL.project3dToPixel(point), calcul_dist(point)] for point in points3D[:, :3]]
    points2D = np.asarray(points2D)

    send_pointcloud(points2D, stamp, pub)
    

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
    
    rospy.init_node('LIDAR_3D_2D', anonymous=False)
    camera_info = '/usb_cam/camera_info'
    lidar_points = '/coordinates_close'
    image = '/usb_cam/image_raw'

    info_sub = message_filters.Subscriber(camera_info, CameraInfo)
    image_sub = message_filters.Subscriber(image, Image)
    lidar_sub = message_filters.Subscriber(lidar_points, PointCloud2)
    
    pub = rospy.Publisher("coordinates_lidar_2d", PointCloud2, queue_size=1)
    image_pub = rospy.Publisher("/usb_cam/camera_lidar", Image, queue_size=5)

    ats = message_filters.ApproximateTimeSynchronizer(
            [info_sub, lidar_sub,image_sub], queue_size=1, slop = 1)
    ats.registerCallback(callback, pub, image_pub)


    rospy.spin()

if __name__ == '__main__':
    main()



















