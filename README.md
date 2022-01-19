# 'BOULE DE CRISTAL' PROJECT

![Boule de cristal](https://github.com/INSA-GEI/geiflix/blob/2022_diskdastardly/documentation/Images/Boule_de_cristal.jpg)

## I. GeiBike Project

The GeiBike project is a project carried out by students at [INSA Toulouse](http://www.insa-toulouse.fr/fr/index.html). This project consists in developing the software of a autonomous vehicule, based on a 3-wheels bike, in order to carry out different missions. Several projects are exposed on the [official website](https://sites.google.com/site/projetsecinsa/).

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

## II. Quick User Guide

### 1. Content
In this repository, all our work is located in the [catkin_ws_jetson](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_jetson) and [catkin_ws_pc](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_pc) folders. You can find the documentation for our project in the folder [documentation](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/documentation). It contains the slides for each sprint review and also the poster to summarize our work.

Following each work folder branch, there is an *src* folder in which is located the source code for our project. There is also a file *.catkin_workspace* that is used for setting up a catkin workspace necessary to run a project using ROS (Robot Operating System). ROS is a middleware that allows components of different architectures to automatically communicate between them. Since we are using different sensors (camera & LIDAR) with a GPU (Jetson NANO) and a PC, ROS has been of great help to make them all communicate together.

In **"catkin_ws_jetson/src"**, you will find the source code that is run on the Jetson NANO, which is a Graphical Processing Unit (GPU) we used for the project. The Jetson is used for the camera and the recognition using AI (Artificial Intelligence). 

In **"catkin_ws_pc/src"**, you will find the source code that is run directly on the PC. On the PC, we run the Graphical User Interface (GUI), the LIDAR SDK (Software Design Kit), the camera-LIDAR callibration, the camera-LIDAR detection and the LIDAR objects tracking and trajectory prediction. 

### 2. Installation

#### 2.1. Prerequisites

This project must be run on either the Linux Ubuntu 18.04 or 20.04. 

You will also need to install the corresponding version of ROS: ros melodic or noetic.
* You can follow this tutorial to install ros noetic on Ubuntu 20.04 : [How to install ros noetic on ubuntu 20.04](https://linoxide.com/how-to-install-ros-noetic-on-ubuntu-20-04/).
* You can follow this tutorial to install ros melodic on Ubuntyu 18.04 : [Ubuntu install of ros melodic](http://wiki.ros.org/melodic/Installation/Ubuntu)


#### 2.2. Preliminary installations 

First step, clone this repository and go to the branch *2022_diskdastardly*.

    git clone https://github.com/INSA-GEI/geiflix.git 
    git checkout 2022_diskdastardly 
    git pull
    
You also need to install two external git repositories we reused for our project. You can follow the instructions on their GitHub for installation:
* [Jetson_GPIO](https://github.com/NVIDIA/jetson-gpio)
* [Jetson_Inference](https://github.com/dusty-nv/ros_deep_learning.git)

Once this is done, you are ready to run the project !

#### 2.3. Launch the Jetson:

Go to the Jetson catkin workspace

    roscd catkin_ws_jetson
    
Do not forget to compile before running and every time a source code has been modified

    catkin_make
    
Then you need to launch the *.launch* file in the *camera* folder

    roslaunch camera usb_cam-cam_tricycle.launch


#### 2.4. Launch the PC source code

Go to the PC catkin workspace

    roscd catkin_ws_pc
    
Do not forget to compile before running and every time a source code has been modified

    catkin_make
    
Then you can start the LIDAR by launching the LIDAR SDK

    roslaunch rslidar_sdk start.launch
    
Then you have the choice to either start recognising objects and display their distance from the sensors, or track objects and predict their trajectory. After this, you can launch the GUI if it did not launch by itself.

##### 2.4.1. Object detection, recognition and distance calculus  
    
To start recognising objects and display their distance, you may enter this command in another command window

    roslaunch lidar_detection lidar_transfo.launch
    
##### 2.4.2. Trajectory prediction

To start tracking objects and predict their trajectory, you may enter this command in another command window

    roslaunch lidar_detection lidar_trajectory.launch
    
##### 2.4.3. Start the Graphical User Interface (GUI)

To start the GUI if it did not launch automatically, you can launch in another command window

    rosrun boule_de_cristal boule_de_cristal
    
#### 2.5. Final Words

Now everything should be working fine ! 

Should you have any question or encounter any problem during installation, feel free to contact our tech Pierre CALMETTES at : *pcalmett@insa-toulouse.fr*
