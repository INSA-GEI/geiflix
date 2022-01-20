
import time
import pidcontroller
#import numpy as np
#from car_functions import *
import can



# This script converts error and direction from the camera to a string for CAN commands

# correction with PID -> string for future CAN command
def control_path(data,compteur,coeff=1/4):
    direction = data[1]
    error = int(data[0])
    PIDCar = pidcontroller.PID(coeff, 0.0, 0.0, 0)
    correction = int(PIDCar.Update(error, 1))


    # clamp
    if correction > 40:
        correction = 40
    elif correction < -40:
        correction = -40

    # gate detected in the right part of the camera's frame
    if direction=='turn_right':

        correction_hex=(50+correction)
        response = f"75/{correction_hex}"
    # gate detected in the left part of the camera's frame
    elif direction=='turn_left':


        correction_hex=(50-correction)
        response = f"75/{correction_hex}"
        ################################################################################
    # car and gate already aligned
    elif direction=='straight'
        # conversion hexadécimale
        correction_hex = (50)
        response=f"75/{correction_hex}"
    # keep the last command : in case of not detecting the gate for some milliseconds
    elif compteur<65 and direction=='not_gate':
        #print(compteur)
        response="NONE/"
    # gate not detected 
    else:

        # conversion hexadécimale : exemple
        correction_hex = 50
        response = f"50/{correction_hex}"
    return response
if __name__=="__main__":
    ### TEST#### 
    test1=[320,'turn_right']

    print(control_path(test1,0))

    test=[0,'not_gate']
    print(control_path(test,0))

    #print(int(0x5a))
    #print(int(0x5A))
