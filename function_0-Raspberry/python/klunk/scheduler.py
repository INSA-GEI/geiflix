import klunk as k
import klunk.car

class scheduler():
    def __init__(self, car):
        self.car = car

    def run(self):
        while True:
            if self.car.mode == self.car.IDLE:
                #wait
                print("TBD")
            elif self.car.mode == self.car.STOP:
                #wait
                print("TBD")
            elif self.car.mode == self.car.UNSAFE:
                #get manual order
                print("TBD")
            elif self.car.mode == self.car.AUTO:
                #get auto order
                print("TBD")
            elif self.car.mode == self.car.MANUAL:
                #get manual order
                print("TBD")
                
