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



## AVAILABLE MODES

**MODE 0 = CALIBRATION** 
1. Use STM32CubeIDE. In main.c, define MODE to 0 (calibration). Build and go to Debug mode. Open calibrate.c and scroll down.
2. Put a break point after power_bootstrap(). Run the code. Start the car. Resume the program. Let the calibration program run for about 10 seconds.
3. Put the wheels in line to roll straight with the buttons from the dashboard. Once the wheels are properly aligned, press the blue button of the NucleoF103RB.
4. Put a breakpoint at the indicated location.
5. Observe the values of capt_when_straight and capt_when_right thanks to right-click then "Add Watch Expression".
6. Switch to Debug view to observe these values in the Expressions tab.
7. Report these values in the #define of the same name in steering.c.
8. In main.c, switch MODE to 2,3,4,5 to resume activity in normal SSC mode.   

*CONGRATULATIONS, you have completed the calibration!*

**MODE 1 = Motor command by CAN frame 0x010 (CMC)**

* Option 1 : Direction using buttons "L" and "R" in the car
* Option 2 : Direction using CAN frame  0x010 (CMC)

**MODE 2 = Motor command by CAN frame 0x020 (SSC)**

* Make sure the car is calibrated (MODE 0) before starting
* Propulsion according to the *speedMode* 
     - STOP    -> 50
     - REVERSE -> 40 
     - WALK    -> 58
     - JOG     -> 60
     - RUN     -> 75
* Direction according to *steerMode*
     - STRAIGHT -> 50
     - HARD_L   -> 10
     - MODT_L   -> 25
     - SOFT_L   -> 40
     - HARD_R   -> 90
     - MODT_R   -> 75
     - SOFT_R   -> 60

**MODE 3 = Autonomous movement to one destination without GPS connection**
* make sure the car is calibrated (MODE 0) before starting
* give coordinates of the car position in *carLatitude* and *carLongitude*
* give coordinates of the destination in *destLatitude* and *destLongitude*
* put the car physically in the direction of the North at the position you just enter in the soft
* start the car, it must join the destination point and send CAN frame with PosOK = 1

**MODE 4 = Autonomous movement to several destination without GPS connection + routine fire detection at each location**
* make sure the car is calibrated (MODE 0) before starting
* give coordinates of the car position in *carLatitude* and *carLongitude*
* enter the number of points in the path in *nbDestCoordinates*
* the coordinates of the different destination are received by the CAN frame DES (0x031)
* put the car physically in the direction of the North at the position you just enter in the soft
* start the car, it must join the first destination and 
   - send CAN frame with PosOK = 1
   - do a 360 degree turn and stop if a CAN frame FIR 0x040 with isFire = 1 is received
   - if isFire stays at 0, the car continues to the next point and execute the exact same routine

**MODE 5 = Autonomous movement to several destination with GPS connection + routine fire detection at each location**

* make sure the car is calibrated (MODE 0) before starting
* enter the number of points in the path in *nbDestCoordinates*
* the coordinates of the different destination are received by the CAN frame DES (0x031)
* the coordinates of the car location are received by the CAN frame POS (0x030) and a mean is done to increase the accuracy
* put the car physically in the direction of the North at the position you just enter in the soft
* start the car, it must join the first destination and 
   - send CAN frame with PosOK = 1
   - do a 360 degree turn and stop if a CAN frame FIR 0x040 with isFire = 1 is received
   - if isFire stays at 0, reception of the car position and the car continues to the next point and execute the exact same routine