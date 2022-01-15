# 'BOULE DE CRISTAL' PROJECT

## GeiBike Project

The GeiBike project is a project carried out by students at [INSA Toulouse](http://www.insa-toulouse.fr/fr/index.html). This project consists in developing the software of a autonomous vehicule, base on a 3-wheels bike, in order to carry out different missions. Several projects are exposed on the [official website](https://sites.google.com/site/projetsecinsa/).

This repository is intended to provide a basis for students starting a new project on the GeiBike. The present code as well as the documentation is the result of the combination of the various projects carried out by:

* CALMETTES Pierre
* CHOULOT Romain
* MARTIN Gautier
* LIU Yixia
* MIKHIN Nikita
* PIQUERAS Valentin

The platform is (or was) developped and maintained by :

* LOMBARD Emmanuel
* MARTIN José
* BOUBACAR ALZOUMA Abdou Rahamane 
* DI MERCURIO Sébastien


The projects are (or were) surpervised by:

* CHANTHERY Elodie
* AURIOL Guillaume

## Quick User Guide

### Content
In this repository, all our work is located in the [catkin_ws_jetson](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_jetson) and [catkin_ws_pc](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc) folders. 

Following each folder branch, there is an *src* folder in which are located all the source code for our project. There is also a file *.catkin_workspace* that is used for setting up a catkin workspace necessary to run a project using ROS (Robot Operating System). ROS is a middleware that allows components of different architectures to automatically communicate between them. Since we are using different sensors (camera & LIDAR), with a GPU (Jetson NANO) and a PC, ROS was of great help to make them all communicate together.

In "catkin_ws_jetson", you will find the source code that is run on the Jetson NANO, which is a Graphical Processor Unit (GPU) we used for the project. The Jetson is used for the camera and the recognition using AI (Artificial Intelligence). Following this, you will find this :
* *src/camera*: 
* *src/ros_deep_learning*: 
* *src/ros_recognition*: 

In "catkin_ws_pc", you will find the source code that is run directly on the PC. On the PC, we run the Graphical User Interface (GUI), the LIDAR SDK (Software Design Kit), and the camera-LIDAR callibration and detection. Here is the list of the folders and their description : 
* *src/boule_de_cristal*: GUI.
* *src/lidar_camera_calibration*: for running callibration of the LIDAR with the camera, i.e. make sure they "see" the same scene.
* *src/lidar_camera_detection*: ??
* *src/lidar_detection*: ??
* *src/rslidar_sdk*: LIDAR SDK, the base code to start the LIDAR and receive its data.

### Installation

#### Preliminary installations 

You need to use the Linux Ubuntu 20.04 Operating System (OS). You will need to install the corresponding version of ROS: ros noetic.
You can follow this tutorial to install ros noetic on Ubuntu 20.04 : [How to install ros noetic on ubuntu 20.04](https://linoxide.com/how-to-install-ros-noetic-on-ubuntu-20-04/).

First step, clone this repository and go to the branch *2022_diskdastardly*.

    git clone https://github.com/INSA-GEI/geiflix.git 
    git checkout 2022_diskdastardly 
    
You also need to install two external git we reused for our project. You can follow their instructions on their GitHub for installation:
* [Jetson_GPIO](https://github.com/NVIDIA/jetson-gpio)
* [Jetson_Inference](https://github.com/dusty-nv/ros_deep_learning.git)

Once this is done, you are ready to run the project !

#### Launch the Jetson:

Go to the Jetson catkin workspace, and do not forget to compile it:

    roscd catkin_ws_jetson
    catkin_make
    
Then you have to launch the *.launch* file in the *camera* folder

    roslaunch camera ??.launch


#### Launch the PC source code

Go to the PC catkin workspace, and do not forget to compile it:

    roscd catkin_ws_pc
    catkin_make
    
Then you will need to launch the following:

    roslaunch rslidar_sdk start.launch
    roslaunch lidar_detection lidar_transfo.launch

And also start the GUI:

    rosrun boule_de_cristal boule_de_cristal
