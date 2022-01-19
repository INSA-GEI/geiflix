## Description

Here is located the source code that is run on the Jetson NANO. The Jetson is used for the camera and the object recognition using AI (Artificial Intelligence).

## Content

* [camera](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_jetson/src/camera): contains a ros launch to run an image_view of the camera and the AI detectnet.
* [ros_deep_learning](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_jetson/src/ros_deep_learning): detectnet, the AI (Artificial Intelligence). N.B.: We reused the code that comes from [this Git](https://github.com/dusty-nv/ros_deep_learning).
* [ros_recognition](https://github.com/INSA-GEI/geiflix/tree/2022_diskdastardly/catkin_ws_jetson/src/ros_recognition): contains a script which subscribes to the topics of detectnet and raises an alarm with a GPIO buzzer if a person is detected.
