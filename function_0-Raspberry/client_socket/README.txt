- raspberry.py : client socket -> receives data from jetson.py (data from the camera)

Proportional corrector calculation then messages written into a can_msg.txt 
Those messages will be read by can_mqtt_vtxt.py, our main program. Then, the CAN commands will be send according to the messages transmitted.

WARNING : This script has to be launched in first in the raspberry pi console. It must also be runned in background.

Next program to launch : can_mqtt_vtxt.py , the main program that will switch between automatic mode and manual mode.

- pid_controller.py : library for the pid controller

- control_path : proportional correction applied to camera data