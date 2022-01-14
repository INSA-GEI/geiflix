# Function 5 - Motor & Direction 

The function is build around a evalboard Nucleo-F103 from ST. Firmware code can be found in firmware directory.

RQ: Firmware has been converted to STMCubeIDE v7 since 09/2021. 

## AVAILABLE CAN FRAMES

This function retrieves data from the Raspi through the CAN bus. 

5 types of CAN frames can be used with this function

**Two CAN frames for Motor Commands (either one or the other) :** 
* *Control Motor Command (CMC)* frames, of ID 0x010
    >The CMC mode allows to command PWM directly.
* *Speed & Steering Commands (SSC)* frames, of ID 0x020  
    >The SSC mode allows to command the propulsion and direction directly from a given speed and steering angle. A differential between left and right wheels has been implemented for more effective turns.

**Two CAN frames for GPS coordinates :**
* *GPS coordinates of the car (POS)*, of ID 0x030
* *GPS coordinates of the destination (DES)*, of ID 0x031

**One CAN frame for the fire detection :**
* *Fire detected (FIR)*, of ID 0x040


Further information about the CAN and the content of these frames is available in the Git at geiflix/documentation/software/networks/CAN/Can Bus.md



### HOW-TO FOR THE FIRST USE OF SSC MODE  

1. Use STM32CubeIDE. In main.c, define MODE to 0 (calibration). Build and go to Debug mode. Open calibrate.c and scroll down.
2. Put a break point after power_bootstrap(). Run the code. Start the car. Resume the program. Let the calibration program run for about 10 seconds.
3. Put the wheels in line to roll straight with the buttons from the dashboard. Once the wheels are properly aligned, press the blue button of the NucleoF103RB.
4. Put a breakpoint at the indicated location.
5. Observe the values of capt_when_straight and capt_when_right thanks to right-click then "Add Watch Expression".
6. Switch to Debug view to observe these values in the Expressions tab.
7. Report these values in the #define of the same name in steering.c.
8. In main.c, switch MODE to 2 to resume activity in normal SSC mode.   

*CONGRATULATIONS, you have completed the calibration!*

## AVAILABLE MODES

**MODE 0 = CALIBRATION** 

See explanations on section above

**MODE 1 = Motor command by CAN frame 0x010 (CMC)**

* Direction using button
