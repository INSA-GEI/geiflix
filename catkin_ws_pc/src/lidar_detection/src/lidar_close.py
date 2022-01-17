#!/usr/bin/env python

import rospy
import numpy as np
import ros_numpy
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
import math
from std_msgs.msg import Header

pub = rospy.Publisher("coordinates_close", PointCloud2, queue_size=10)

def callback(data):
    global pub


    points3D = ros_numpy.point_cloud2.pointcloud2_to_array(data)
    points3D  = np.asarray(points3D.tolist())

    newPoints = []
    for point_intermediare in points3D:
      for point in point_intermediare:
        if math.sqrt(point[0]*point[0] +
		                         point[1]*point[1] +
		                         point[2]*point[2]) < 2:
          newPoints.append(point)


    fields = [PointField('x', 0, PointField.FLOAT32, 1),
              PointField('y', 4, PointField.FLOAT32, 1),
              PointField('z', 8, PointField.FLOAT32, 1),
              PointField('intensity', 12, PointField.FLOAT32, 1),
              ]

    header = Header() 
    header.frame_id = "map"
    newData = pc2.create_cloud(header, fields, newPoints)
    newData.header.stamp = data.header.stamp
    pub.publish(newData)

def main():
    rospy.init_node('LIDAR_detection', anonymous=False)
    rospy.Subscriber("/rslidar_points", PointCloud2, callback)
   # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    main()


