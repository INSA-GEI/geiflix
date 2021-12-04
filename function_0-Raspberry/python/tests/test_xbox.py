#!/usr/bin/python3

#from logging import exception
import can
import time

import klunk as k
import klunk.can
import klunk.car
import klunk.motors
import xbox

bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
car = k.car.Car(bus)
# Instantiate the controller
joy = xbox.Joystick()


try:
    # Remote car control via up & down pad of xbox controller
    print("Xbox controller KLUNK testing: Press Back button to exit")
    while not joy.Back():
        # Emergency stop
        if joy.B():
            print("EMERGENCY STOP")
            car.brake()
        # Speed up
        elif joy.dpadUp() or joy.rightBumper():
            print("UP")
            car.faster()
        # Speed down
        elif joy.dpadDown() or joy.leftBumper():
            print("DOWN")
            car.slower()
        # Turn left
        elif joy.dpadLeft():
            print("LEFT")
            if car.steer > k.motors.STEER_STRAIGHT:
                car.set_steer(k.motors.STEER_STRAIGHT)
            else:
                car.lefter()
        # Turn right
        elif joy.dpadRight():
            print("RIGHT")
            if car.steer < k.motors.STEER_STRAIGHT:
                car.set_steer(k.motors.STEER_STRAIGHT)
            else:
                car.righter()
        # Unsafe mode
        elif joy.rightThumbstick() and joy.leftThumbstick():
            print("UNSAFE MODE ACTIVATED")
            car.brake()

        # Refresh period, must not be too low
        time.sleep(0.2)
    # Brake when done
    car.brake()
    # Close out when done
    joy.close()
except KeyboardInterrupt:
    bus.send(k.can.motors_message(k.motors.SPEED_STOP, k.motors.STEER_STRAIGHT))