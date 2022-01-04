#!/usr/bin/python3

#from logging import exception
from threading import Thread
import time

from can.interface import Bus

import klunk
import klunk.can
import klunk.car
import klunk.motors
import xbox

class XboxController(Thread):
    def __init__(self,bus,car):
        Thread.__init__(self)
        # Instantiate the controller
        self.joy = xbox.Joystick()
        self.bus = bus
        self.car = car
        self.incremental = False

    def run(self):
        try:
            print("Xbox controller KLUNK testing: Press Back button to exit")
            # Warning: instructions are ordered by priority
            while not self.joy.Back():
                if self.incremental:
                    # Emergency stop
                    if self.joy.B():
                        print("EMERGENCY STOP")
                        self.car.brake()
                    # Turn right
                    elif self.joy.dpadRight():
                        print("RIGHT")
                        # When asked to turn right while turning left: go straight
                        if self.car.steer < klunk.motors.STEER_STRAIGHT:
                            self.car.set_steer(klunk.motors.STEER_STRAIGHT)
                        else:
                            self.car.righter()
                    # Turn left
                    elif self.joy.dpadLeft():
                        print("LEFT")
                        # When asked to turn left while turning right: go straight
                        if self.car.steer > klunk.motors.STEER_STRAIGHT:
                            self.car.set_steer(klunk.motors.STEER_STRAIGHT)
                        else:
                            self.car.lefter()
                    # Speed down
                    elif self.joy.dpadDown() or self.joy.leftBumper():
                        print("DOWN")
                        self.car.slower()
                    # Speed up
                    elif self.joy.dpadUp() or self.joy.rightBumper():
                        print("UP")
                        self.car.faster()
                else:
                    rightTrigger = self.joy.rightTrigger()
                    leftTrigger = self.joy.leftTrigger()

                    if self.joy.B():
                        #print("BRAKE")
                        self.car.brake()
                    elif leftTrigger and not rightTrigger:
                        #print("REVERSE")
                        self.car.set_speed(klunk.motors.SPEED_REVERSE)
                    elif rightTrigger < 0.25 or leftTrigger:
                        #print("NO ACTION -> STOP")
                        self.car.set_speed(klunk.motors.SPEED_STOP)
                    elif rightTrigger < 0.5:
                        #print("SLOW SPEED")
                        self.car.set_speed(klunk.motors.SPEED_SLOW)
                    elif rightTrigger < 0.75:
                        #print("MEDIUM SPEED")
                        self.car.set_speed(klunk.motors.SPEED_MEDIUM)
                    else:
                        #print("FAST SPEED")
                        self.car.set_speed(klunk.motors.SPEED_FAST)

                    joySteer = self.joy.leftX()
                    if joySteer < -0.75:
                        self.car.set_steer(klunk.motors.STEER_LEFT_FAR)
                    elif joySteer < -0.5:
                        self.car.set_steer(klunk.motors.STEER_LEFT_MIDDLE)
                    elif joySteer < -0.25:
                        self.car.set_steer(klunk.motors.STEER_LEFT_CLOSE)
                    elif joySteer < 0.25:
                        self.car.set_steer(klunk.motors.STEER_STRAIGHT)
                    elif joySteer < 0.5:
                        self.car.set_steer(klunk.motors.STEER_RIGHT_CLOSE)
                    elif joySteer < 0.75:
                        self.car.set_steer(klunk.motors.STEER_RIGHT_MIDDLE)
                    else:
                        self.car.set_steer(klunk.motors.STEER_RIGHT_FAR)

                if self.joy.Y():
                    print("CHANGED INCREMENTAL MODE :", self.incremental)
                    self.incremental = not self.incremental

                # Refresh period, must not be too low (eg. < 0.01)
                time.sleep(0.2)
            
            print("BACK")
            # Brake when done
            self.car.brake()
            # Close out when done
            self.joy.close()
        except KeyboardInterrupt:
            self.bus.send(klunk.can.motors_message(klunk.motors.SPEED_STOP, klunk.motors.STEER_STRAIGHT))
