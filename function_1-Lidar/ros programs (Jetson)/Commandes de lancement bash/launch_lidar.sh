#!/bin/sh
echo "Setting access rights of the lidar"
sudo chmod 777 /dev/ttyUSB0 #Setting Lidar as reader, writter and exec

echo "Lauching the lidar application"
roslaunch rplidar_ros view_rplidar.launch &
rosrun laser2pc laser2pc.py &
rosrun pc_manip_tracking obj_manipv2.py &
rosrun pc_manip_tracking detect2m.py &
rosrun multi_object_tracking_lidar kf_tracker &
rosrun trajectory Motor_commands.py
