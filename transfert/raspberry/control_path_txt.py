
import time
import pidcontroller
#import numpy as np
#from car_functions import *
import can





################# RECUPERER DIRECTION ET ERREUR ########################
def control_path(data,compteur,coeff=1/4):
    # trame data = [direction, error]
    # example : data = [b'right', b'error']
    # little delay
    #time.sleep(0.01)
    direction = data[1]
    error = int(data[0])
    # on ouvre le bus CAN -> décommentez
    ################################################################################
    #bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    ################################################################################
    # PID object, only P corrector at the moment

    # coeff proportionnel -> si caméra = 640 pixels -> maximum error = 320
    # 40/320 = 1/8
    PIDCar = pidcontroller.PID(coeff, 0.0, 0.0, 0)
    correction = int(PIDCar.Update(error, 1))


    # clamp
    if correction > 40:
        correction = 40
    elif correction < -40:
        correction = -40


    if direction=='turn_right':
        #print(f"Error : {error}")
        #print("La voiture tourne à droite.")

        # conversion hexadécimale
        correction_hex=(50+correction)
        #print(correction_hex)
        #print(f"Envoi message CAN : {correction_hex}")
        # décommentez lignes suivantes pour envoi message CAN
        response = f"75/{correction_hex}"
    elif direction=='turn_left':
        #print(f"Error : {error}")
        #print("La voiture tourne à gauche.")

        # conversion hexadécimale
        correction_hex=(50-correction)
        #print(correction_hex)
        #print(f"Envoi message CAN : {correction_hex}")
        # décommentez lignes suivantes pour envoi message CAN
        ################################################################################
        #msg = can.Message(arbitration_id=0x020, data=[0x4b,correction_hex], extended_id=False)
        response = f"75/{correction_hex}"
        #bus.send(msg)
        ################################################################################
    elif direction=='straight':
        #print(f"Error : {error}")
        #print("La voiture va tout droit.")

        # conversion hexadécimale
        correction_hex = (50)
        # print(correction_hex)
        #print(f"Envoi message CAN : {correction_hex}")
        # décommentez lignes suivantes pour envoi message CAN
        ################################################################################
        #msg = can.Message(arbitration_id=0x020, data=[0x4b,correction_hex], extended_id=False)
        #bus.send(msg)
        response=f"75/{correction_hex}"
    elif compteur<65 and direction=='not_gate':
        #print(compteur)
        response="NONE/"
        ################################################################################
   # elif compteur>400 and direction=='not_gate':
     #   msg=can.Message(arbitration_id=0x020,data=[68,50],extended_id=False)
    #    bus.send(msg)
    else:
        #print(f"Error : {error}")
        #print("VOITURE A LARRET, PAS DE GATE OU MAUVAIS GATE")

        # conversion hexadécimale : exemple
        correction_hex = 50
        response = f"50/{correction_hex}"
        # print(correction_hex)
        #print(f"Envoi message CAN : {correction_hex}")
        # décommentez lignes suivantes pour envoi message CAN
        ################################################################################
        #msg = can.Message(arbitration_id=0x020, data=[0x32,correction_hex], extended_id=False)
        #bus.send(msg)
        ################################################################################
    return response
if __name__=="__main__":
    test1=[320,'turn_right']

    print(control_path(test1,0))

    test=[0,'not_gate']
    print(control_path(test,0))

    #print(int(0x5a))
    #print(int(0x5A))
