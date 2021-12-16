from threading import Thread
from can.interface import Bus

import klunk
import klunk.can
import klunk.car
import klunk.motors
import klunk.xboxController as xC

import xbox



class scheduler(Thread):
    def __init__(self,bus,car):
        Thread.__init__(self)
        self.bus = bus
        self.car = car

    def run(self):
        while True:
            if self.car.mode == 'IDLE':
                print("TBD")
            elif self.car.mode == 'STOP':
                print("TBD")
            elif self.car.mode == 'MANUAL':
                print("TBD")
            elif self.car.mode == 'AUTO':
                print("TBD")
            elif self.car.mode == 'UNSAFE':
                print("TBD")
                
