#!/bin/sh
echo "Launching codes for LIDAR purposes, distances calculation..."
cd ~/Desktop/Travail/QR\ detection/

#echo * # Display documents available in directory

echo "4dminJ3tson*" | sudo -S chmod +x *.py #Setting all python files as exec in QR Detection file

sudo chmod 777 /dev/ttyUSB0 #Setting Lidar as reader, writter and exec

echo "Lauching Lidar GUI"
roslaunch rplidar_ros view_rplidar.launch &
rosrun laser2pc laser2pc.py &
rosrun pc_manip_tracking obj_manipv2.py &
rosrun pc_manip_tracking detect2m.py &
rosrun multi_object_tracking_lidar kf_tracker &
rosrun trajectory Motor_commands.py
