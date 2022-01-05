import klunk.motors as motors

class Scheduler():
    def __init__(self, car, xbox):
        self.car = car
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
                if not self.car.US.any_obstacle() and self.xbox.A():
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

    def Safety(self):
        ZoneA = self.usCzone() or self.lidarCzone()
        ZoneB = self.usBzone() or self.lidarBzone()
        ZoneC = self.usCzone() or self.lidarCzone()
        ZoneE = self.lidarEzone()
        ZoneF = self.lidarFzone()
        ZoneK = self.usKzone() or self.lidarKzone()
        ZoneL = self.usLzone() or self.lidarLzone()
        ZoneM = self.usMzone() or self.lidarMzone()
    
        if (ZoneA or ZoneB or ZoneC) and self.car_forward():
            self.car.speed = motors.SPEED_STOP

        if (ZoneK or ZoneL or ZoneM) and self.car_backward():
            self.car.speed = motors.SPEED_STOP
        
        if ZoneE or ZoneF:
            if self.car.speed == motors.SPEED_FAST:
                self.car.speed = motors.SPEED_MEDIUM
            if ((self.car.steer == motors.STEER_RIGHT_FAR) or (self.car.steer == motors.STEER_RIGHT_MIDDLE)) and ZoneE:
                self.car.steer = motors.STEER_RIGHT_CLOSE
            if ((self.car.steer == motors.STEER_LEFT_FAR) or (self.car.steer == motors.STEER_LEFT_MIDDLE)) and ZoneF:
                self.car.steer = motors.STEER_LEFT_CLOSE
        

    
    def usAzone(self):
        return self.car.US.front_left_obstacle()
    
    def lidarAzone(self):
        return self.car.lidar.findObstacle(-45, -15, 100)
        return (self.Lidar.angle <= -15) and (self.Lidar.angle >= -45) and (self.Lidar.dist <= 100)
    
    def usBzone(self):
        return self.car.US.front_right_obstacle()
    
    def lidarBzone(self):
        return self.car.lidar.findObstacle(15, 45, 100)
        return (self.Lidar.angle >= 15) and (self.Lidar.angle <= 45) and (self.Lidar.dist <= 100)

    def usCzone(self):
        return self.car.US.front_center_obstacle()
    
    def lidarCzone(self):
        return self.car.lidar.findObstacle(-15, 15, 100)
        return (self.Lidar.angle <= 15) and (self.Lidar.angle >= -15) and (self.Lidar.dist <= 100)
    
    def usKzone(self):
        return self.car.US.rear_left_obstacle()
    
    def lidarKzone(self):
        return self.car.lidar.findObstacle(-165, -135, 100)
        return (self.Lidar.angle <= -165) and (self.Lidar.angle >= -135) and (self.Lidar.dist <= 100)
    
    def usLzone(self):
        return self.car.US.rear_right_obstacle()
    
    def lidarLzone(self):
        return self.car.lidar.findObstacle(135, 165, 100)
        return (self.Lidar.angle <= 165) and (self.Lidar.angle >= 135) and (self.Lidar.dist <= 100)
    
    def usMzone(self):
        return self.car.US.rear_center_obstacle()
    
    def lidarMzone(self):
        return self.car.lidar.findObstacle(165, -165, 100)
        return ((self.Lidar.angle <= -165) or (self.Lidar.angle >= 165)) and (self.Lidar.dist <= 100)
    
    def lidarEzone(self):
        return self.car.lidar.findObstacle(45, 135, 100)
        return (self.Lidar.angle <= 135) and (self.Lidar.angle >= 45)

    def lidarFzone(self):
        return self.car.lidar.findObstacle(-135, -45, 100)
        return (self.Lidar.angle >= -135) and (self.Lidar.angle <= -45)


    def car_forward(self):
        return (self.car.speed == motors.SPEED_FAST) or (self.car.speed == motors.SPEED_MEDIUM) or (self.car.speed == motors.SPEED_SLOW)
    
    def car_backward(self):
        return self.car.speed == motors.SPEED_REVERSE
