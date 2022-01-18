#!/usr/bin/env python

import rospy
from pc_manip_tracking.msg import objects2m, XYobjects
from std_msgs.msg import String
import numpy as np
import socket

#Publication ordre à donner à la voiture sur le topic Motor_commands
pub = rospy.Publisher("Motor_commands", String, queue_size=10)

#Initialisation
gate_detected = False

#Recuperation et traitement des donnees provenant du topic Objects2m
def callback2(data):

    global gate_detected, c01, c02, c03, c04, c05, c12, c13, c14, c15, c23, c24, c25, c34, c35, c45

    #recuperation des donnees du topic
    obj0 = data.Detect2m_obj0
    obj1 = data.Detect2m_obj1
    obj2 = data.Detect2m_obj2
    obj3 = data.Detect2m_obj3
    obj4 = data.Detect2m_obj4
    obj5 = data.Detect2m_obj5

    #conditions 2 objets detectes
    c01 = obj0 and obj1
    c02 = obj0 and obj2
    c03 = obj0 and obj3
    c04 = obj0 and obj4
    c05 = obj0 and obj5
    c12 = obj1 and obj2
    c13 = obj1 and obj3
    c14 = obj1 and obj4
    c15 = obj1 and obj5
    c23 = obj2 and obj3
    c24 = obj2 and obj4
    c25 = obj2 and obj5
    c34 = obj3 and obj4
    c35 = obj3 and obj5
    c45 = obj4 and obj5
    
    #si 1 des conditions valides, portique detecte
    if c01 or c02 or c03 or c04 or c05 or c12 or c13 or c14 or c15 or c23 or c24 or c25 or c34 or c35 or c45 :

            gate_detected = True
                
    else :
   
            gate_detected = False
        
    
#Recuperation et traitement des donnees provenant du topic XYobjects
def callback3(data):
    global gate_detected, c01, c02, c03, c04, c05, c12, c13, c14, c15, c23, c24, c25, c34, c35, c45

    #Initialisation
    Pole1 = 0.0
    Pole2 = 0.0

    #Si portique detecte, recuperer la position Y de chaque objet
    if gate_detected :
    
        if c01 :
            
            Pole1 = data.Yobject0
            Pole2 = data.Yobject1  
        
        elif c02 :
        
            Pole1 = data.Yobject0
            Pole2 = data.Yobject2 
        
        elif c03 :
        
            Pole1 = data.Yobject0
            Pole2 = data.Yobject3 
        
        elif c04 :
        
            Pole1 = data.Yobject0
            Pole2 = data.Yobject4
        
        elif c05 :
        
            Pole1 = data.Yobject0
            Pole2 = data.Yobject5
        
        elif c12 :
        
            Pole1 = data.Yobject1
            Pole2 = data.Yobject2
        
        elif c13 :
        
            Pole1 = data.Yobject1
            Pole2 = data.Yobject3
        
        elif c14 :
        
            Pole1 = data.Yobject1
            Pole2 = data.Yobject4
        
        elif c15 :
        
            Pole1 = data.Yobject1
            Pole2 = data.Yobject5
        
        elif c23 :
        
            Pole1 = data.Yobject2
            Pole2 = data.Yobject3
        
        elif c24 :
        
            Pole1 = data.Yobject2
            Pole2 = data.Yobject4
        
        elif c25 :
        
            Pole1 = data.Yobject2
            Pole2 = data.Yobject5
        
        elif c34 : 
        
            Pole1 = data.Yobject3
            Pole2 = data.Yobject4
        
        elif c35 : 
        
            Pole1 = data.Yobject3
            Pole2 = data.Yobject5
        
        elif c45 :
        
            Pole1 = data.Yobject4
            Pole2 = data.Yobject5

    #Si la position Y est positive et depasse un certain seuil pour les deux objets, alors on a traverse le portique :
    #envoi de la commande stop sinon avancer
    if Pole1 >= 0.5 and Pole2 >= 0.5 :
        pub.publish("stop")
    else :
        pub.publish("avancer")

    #affichage pour tests
    rospy.loginfo('Pole1Y: {}, Pole2Y: {}, gate_detected : {} '.format(Pole1, Pole2, gate_detected))

#Initialisation du node et souscription aux topics Objects2m et XYobjects
def main():

    rospy.init_node('Motor_commands')
    rospy.Subscriber("Objects2m", objects2m, callback2)
    rospy.Subscriber("XYobjects", XYobjects, callback3)
        
    rospy.spin()


if __name__ == '__main__':
    print ("Starting motor_commands...")
    main()

