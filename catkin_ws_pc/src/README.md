## Description

Here is located the source code that is run directly on the PC. On the PC, we run the Graphical User Interface (GUI), the LIDAR SDK (Software Design Kit), the camera-LIDAR callibration and detection, and object tracking and trajectory prediction.

## Content 

* [boule_de_cristal](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc/src/boule_de_cristal): GUI.
* [lidar_camera_calibration](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc/src/lidar_camera_calibration): for running callibration of the LIDAR with the camera, i.e. make sure they "see" the same scene. N.B.: We reused the code from [this GitHub](https://github.com/heethesh/lidar_camera_calibration). We modified it heavily though in order to adapt to our means and resources.
* [lidar_camera_detection](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc/src/lidar_camera_detection): for the display of the LIDAR distances on the camera images.
* [lidar_detection](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc/src/lidar_detection): for the transformation in 2D of LIDAR points.
* [multiple-object-tracking-lidar](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc/src/multiple-object-tracking-lidar): for the object tracking using the LIDAR and ROS. N.B.: this code is from [this GitHub](https://github.com/praveen-palanisamy/multiple-object-tracking-lidar)), we reused and lightly modified it for the most part.
* [rslidar_sdk](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc/src/rslidar_sdk): LIDAR SDK, the base code to start the LIDAR and receive its data. N.B.: this code comes from [this GitHub](https://github.com/RoboSense-LiDAR/rslidar_sdk)).
