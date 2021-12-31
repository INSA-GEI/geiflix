#!/usr/bin/python3

import rospy
import jetson.inference
from vision_msgs.msg import Detection2DArray
import jetson.utils
import RPi.GPIO as GPIO
import time
import threading
from threading import Lock
import os
from sensor_msgs import point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField
import numpy as np
import math
from std_msgs.msg import Header

class Detection:
    def __init__(self):
        self.pointCloud = None

    def lidar_pc_callback(self, data):
        points = ros_numpy.point_cloud2.pointcloud2_to_array(data)
        self.pointCloud = np.asarray(points.tolist())

    def camera_detection_callback(self, data)
        if self.pointCloud is not None:
            #Pour chaque objet, on cherche leur distance
            for detection in data.detections:
                center_x = detection.bbox.center.x
                center_y = detection.bbox.center.y
                closest_point = None
                for point in self.pointCLoud:
                    if abs(center_x - point[0]) < 1 and abs(center_y - point[0]) <1:
                        if closest_point is None or point[2] < closest_point:
                            closest_point = point[2]
                print(closest_point)
                #Ajouter cette distance au msg
                #Envoyer tous les msgs
        



beep_on = False
counter_person = 0
watchdog_counter = 0
mutex = Lock()

def chien_de_garde():
    global watchdog_counter
    global counter_person
    global beep_on
    while(True):
        time.sleep(0.5)
        print(watchdog_counter)
        mutex.acquire()
        if (watchdog_counter == 0):
            beep_on = False
            counter_person = 0
        else :
            watchdog_counter = 0
        mutex.release()
           


#Send PWM to the buzzer
def beep(pwm):
    global beep_on
    etat_beep = False
    while (True):
        if ((beep_on != etat_beep) and beep_on):
            pwm.start(50)
            etat_beep = True
        elif (beep_on != etat_beep and (not beep_on)):
            pwm.stop()
            etat_beep = False
    beep_on = False



def callback(data):
    global beep_on
    global counter_person
    global watchdog_counter
    mutex.acquire()
    watchdog_counter = 1
    person_detected = False
    for detection in data.detections:
        if (detection.results[0].id == 1):
            counter_person += 1
            person_detected = True
    print(counter_person)        
    if (not person_detected):
        counter_person = 0
    if (counter_person > 2):
        beep_on = True
        counter_person = 3
    else:
        beep_on = False
    mutex.release()
    
def main():

    # Pin Setup:
    # Board pin-numbering scheme
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    # set pin as an output pin with optional initial state of HIGH
    GPIO.setup(33, GPIO.OUT)
    pwm = GPIO.PWM(33, 2300)

    x = threading.Thread(target=beep, args=(pwm,), daemon=True)
    x.start()

    thread_chien = threading.Thread(target=chien_de_garde, args=(), daemon=True)
    thread_chien.start()

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/detectnet/detections", Detection2DArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    main()
