
class scheduler():
    def __init__(self, car, us, xbox):
        self.car = car
        self.US = us
        self.xbox = xbox

    def run(self):
        while True:
# IDLE Mode
            if self.car.mode == self.car.IDLE:

                #wait instructions

                # Switch mode
                if self.xbox.Start():
                    print("IDLE -> MANUAL")
                    self.car.set_mode(self.car.MANUAL)
                elif self.xbox.A():####### and destinatinon input set
                    print("IDLE -> AUTO")
                    self.car.set_mode(self.car.AUTO)
# AUTO Mode
            elif self.car.mode == self.car.AUTO:

                #get auto order (+avoidance)

                # Switch mode
                if self.xbox.Start():
                    print("AUTO -> MANUAL")
                    self.car.set_mode(self.car.MANUAL)
                elif self.xbox.B():####### or unavoidable obstacle
                    print("AUTO -> STOP")
                    self.car.set_mode(self.car.STOP)
                elif False:####### destination reached
                    print("AUTO -> IDLE")
                    self.car.set_mode(self.car.IDLE)
# MANUAL Mode
            elif self.car.mode == self.car.MANUAL:

                #get manual order (+avoidance)

                # Switch mode
                if self.xbox.Back():
                    print("MANUAL -> IDLE")
                    self.car.set_mode(self.car.IDLE)
                elif self.xbox.B():####### or obstacle detected
                    print("MANUAL -> STOP")
                    self.car.set_mode(self.car.STOP)
                elif self.joy.rightThumbstick() and self.joy.leftThumbstick() and \
                    self.car.is_stopped():
                    print("MANUAL -> UNSAFE")
                    self.car.set_mode(self.car.UNSAFE)
# STOP Mode
            elif self.car.mode == self.car.STOP:

                #look around

                # Switch mode
                if not self.US.any_obstacle() and self.xbox.A():
                    print("STOP -> AUTO")
                    self.car.set_mode(self.car.AUTO)
                if True:####### safe movement ordered
                    print("STOP -> MANUAL")
                    self.car.set_mode(self.car.MANUAL)
# UNSAFE Mode
            elif self.car.mode == self.car.UNSAFE:

                #get manual order

                # Switch mode
                if self.xbox.Start():
                    print("UNSAFE -> MANUAL")
                    self.car.set_mode(self.car.MANUAL)

