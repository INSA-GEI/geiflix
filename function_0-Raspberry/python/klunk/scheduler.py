import klunk.motors as motors
import klunk.car
import xbox
import time

REFRESH_RATE = 0.1

class Scheduler():
    def __init__(self, car, joy):
        self.incremental = False
        if isinstance(car, klunk.car.Car):
            self.car = car
        if isinstance(joy, xbox.Joystick):
            self.xbox = joy

    def run(self):
        while True:
# IDLE Mode
            if self.car.mode == self.car.IDLE:

                speed_order = motors.SPEED_STOP
                steer_order = motors.STEER_STRAIGHT

                # Switch mode
                if self.xbox.Start():
                    print("IDLE -> MANUAL")
                    self.car.mode = self.car.MANUAL
                elif self.xbox.A() and self.car.destination is not None:
                    print("IDLE -> AUTO")
                    self.car.mode = self.car.AUTO
# AUTO Mode
            elif self.car.mode == self.car.AUTO:

                # TODO: get auto order (+avoidance)

                # Switch mode
                if self.xbox.Start():
                    print("AUTO -> MANUAL")
                    self.car.mode = self.car.MANUAL
                elif self.xbox.B():####### or unavoidable obstacle
                    print("AUTO -> STOP")
                    self.car.mode = self.car.STOP
                elif False:####### destination reached
                    print("AUTO -> IDLE")
                    self.car.mode = self.car.IDLE
# MANUAL Mode
            elif self.car.mode == self.car.MANUAL:
                
                speed_order, steer_order = self.get_manual_order()

                # TODO: get manual order (+avoidance)

                # Switch mode
                if self.xbox.Back():
                    print("MANUAL -> IDLE")
                    self.car.mode = self.car.IDLE
                elif self.xbox.B():####### or obstacle detected
                    print("MANUAL -> STOP")
                    self.car.mode = self.car.STOP
                elif self.xbox.rightThumbstick() and self.xbox.leftThumbstick() and \
                    self.car.is_stopped():
                    print("MANUAL -> UNSAFE")
                    self.car.mode = self.car.UNSAFE
# STOP Mode
            elif self.car.mode == self.car.STOP:

                speed_order = motors.SPEED_STOP
                steer_order = motors.STEER_STRAIGHT
                # waiting for instructions safely

                # Switch mode
                if not self.car.US.any_obstacle() and self.xbox.A():
                    print("STOP -> AUTO")
                    self.car.mode = self.car.AUTO
                if True:####### safe movement ordered
                    print("STOP -> MANUAL")
                    self.car.mode = self.car.MANUAL
# UNSAFE Mode
            elif self.car.mode == self.car.UNSAFE:

                speed_order, steer_order = self.get_manual_order()

                # Switch mode
                if self.xbox.Start():
                    print("UNSAFE -> MANUAL")
                    self.car.mode = self.car.MANUAL

            speed_order, steer_order = self.Safety(speed_order, steer_order)
            self.car.speed = speed_order
            self.car.steer = steer_order
            time.sleep(REFRESH_RATE)

    def Safety(self, speed_order, steer_order):
        if self.car.mode == self.car.UNSAFE:
            return speed_order, steer_order
        else:
            ZoneA = self.usCzone() or self.lidarCzone()
            ZoneB = self.usBzone() or self.lidarBzone()
            ZoneC = self.usCzone() or self.lidarCzone()
            ZoneE = self.lidarEzone()
            ZoneF = self.lidarFzone()
            ZoneK = self.usKzone() or self.lidarKzone()
            ZoneL = self.usLzone() or self.lidarLzone()
            ZoneM = self.usMzone() or self.lidarMzone()

            if (ZoneA or ZoneB or ZoneC) and speed_order > motors.SPEED_STOP:
                speed_order = motors.SPEED_STOP
            elif (ZoneK or ZoneL or ZoneM) and speed_order < motors.SPEED_STOP:
                speed_order = motors.SPEED_STOP

            if ZoneE or ZoneF:
                if speed_order == motors.SPEED_FAST:
                    speed_order = motors.SPEED_MEDIUM
                if ((steer_order == motors.STEER_RIGHT_FAR) or (steer_order == motors.STEER_RIGHT_MIDDLE)) and ZoneE:
                    steer_order = motors.STEER_RIGHT_CLOSE
                if ((steer_order == motors.STEER_LEFT_FAR) or (steer_order == motors.STEER_LEFT_MIDDLE)) and ZoneF:
                    steer_order = motors.STEER_LEFT_CLOSE
            
            return speed_order, steer_order
#Function for Safety V2
    def isSafe(self, speed_order, steer_order):
	if self.sar.mode != salf.car.UNSAFE and self.car.mode != self.car.IDLE:
		ZoneA = self.isAzone()
		ZoneB = self.isBzone()
		ZoneC = self.isCzone()
		ZoneK = self.isKzone()
		ZoneL = self.isLzone()
		ZoneM = self.isMzone()
		ZoneN = self.isNzone()
		ZoneS = self.isSzone()
		ZoneT = self.isTzone()
		ZoneU = self.isUzone()
		ZoneX = self.isXzone_US() or self.isXzone_Lidar()
		ZoneY = self.isYzone()
		ZoneZ = self.isZzone()
		if (self.car.mode == self.car.MANUAL or (self.car.mode == self.car.AUTO and not avoid_right and not avoid_left)):
			if ZoneA and speed_order > motors.SPEED_STOP:
				speed_order = motors.SPEED_STOP
			if ((ZoneB and speed_order) == motors.SPEED_REVERSE):
				speed_order = motors.SPEED_STOP
			if ZoneC and speed_order == motors.SPEED_FAST:
				speed_order = motors.SPEED_MEDIUM
			if ZoneK or ZoneM:
				if speed_order == motors.SPEED_FAST:
					speed_order = motors.SPEED_MEDIUM
				if steer_order == motors.STEER_LEFT_FAR:
					steer_order = motors.STEER_LEFT_MIDDLE
			if ZoneL or Zone N:
				if speed_order == motors.SPEED_FAST:
					speed_order = motors.SPEED_MEDIUM
				if steer_order == motors.STEER_RIGHT_FAR:
					steer_order = motors.STEER_RIGHT_MIDDLE
			if ZoneS or ZoneU:
				if speed_order > motors.SPEED_SLOW:
					speed_order = motors.SPEED_SLOW
				if (steer_order == motors.STEER_LEFT_FAR) or (steer_order == motors.STEER_LEFT_MIDDLE):
					speed_order = motors.STEER_LEFT_CLOSE
			if ZoneT or ZoneV:
				if speed_order > motors.SPEED_SLOW:
					speed_order = motors.SPEED_SLOW
				if (steer_order == motors.STEER_RIGHT_FAR) or (steer_order == motors.STEER_RIGHT_MIDDLE):
					steer_order = motors.STEER_RIGHT_CLOSE
			if (self.car.mode == self.car.MANUAL):
				if (ZoneX or ZoneY or ZoneZ):
					if speed_order > motors.SPEED_SLOW:
						speed_order = motors.SPEED_SLOW
					if ZoneY and (steer_order == motors.STEER_LEFT_FAR or steer_order == motors.STEER_LEFT_MIDDLE or steer_order == motors.SPEED_LEFT_CLOSE):
						steer_order = motors.STEER_STRAIGHT
					elif ZoneZ and (steer_order == motors.STEER_RIGHT_FAR or steer_order == STEER_RIGHT_MIDDLE or steer_order == motors.STEER_RIGHT_CLOSE):
						steer_order = motors.STEER_STRAIGHT
			elif (self.car.mode ==  self.car.AUTO):
				if ((ZoneK or ZoneS) and ZoneZ) or ((ZoneL or ZoneT) and Zone Y) or (ZoneY and ZoneZ) or (ZoneX and ZoneZ) or (ZoneX and ZoneY):
					if speed_order > motors.SPEED_STOP:
						speed_order = motors.SPEED_STOP
				elif (ZoneY or ZoneX or ZoneZ):
					if speed_order > motors.SPEED_SLOW:
						speed_order = motors.SPEED_SLOW
						if ZoneY:
							self.avoid_right = true
							steer_order = motors.STEER_RIGHT_FAR
						elif ZoneZ:
							self.avoid_left = true
							steer_order = motors.STEER_LEFT_FAR
						elif ZoneX:
							dist_Obstacle = min (self.Lidar.dist, self.car.US.front_center)
							if dist < 50 and speed_order > motors.SPEED_STOP:
								speed_order = SPEED_STOP
							elif self.isXZone_Lidar():
								if self.Lidar.angle < 0:
									self.avoid_right = true
									steer_order = motors.STEER_RIGHT_FAR
							else:
								self.avoid_left = true
								steer_order = motors.STEER_LEFT_FAR
		elif (avoid_right):
			speed_order = motors.SPEED_STOP
		elif (avoid_left):
			speed_order = motors.SPEED_STOP
	return speed_order, steer_order


    def isAzone(self):
        return (self.car.US.front_center_obstacle(30) or self.car.US.front_right_obstacle(30) or self.car.US.front_left_obstacle(30) or (self.Lidar.searchObstacle(-45, 45, 40, 80))

    def isBzone(self):
	return (self.car.US.rear_center(_obstacle30) or self.car.US.rear_right_obstacle(30) or self.car.US.rear_left_obstacle(30) or self.Lidar.searchObstacle(-180, -135, 80) or self.Lidar.searchObstacle(135, 180, 40, 80))
                
    def isCzone(self):
	US = (self.car.US.front_center_obstacle(100) and not self.car.US.front_center_obstalce(80)) or (self.car.US.front_right_obstacle(100) and not self.car.US.front_right_obstacle(70)) or (self.car.US.front_left_obstacle(100) and not self.car.US.front_left_obstacle(70))
	Lidar = self.Lidar.searchObstacle(-45, -15, 120, 150) or self.Lidar.searchObstacle(15, 45, 120, 150) or self.Lidar.searchObstacle(-15, 15, 130, 150)
	return US or Lidar

    def isKzone(self):
	return self.Lidar.searchObstacle(-90, -45, 80, 100)

    def isLzone(self):
	return self.Lidar.searchObstacle(45, 90, 80, 100)

    def isMzone(self):
	return self.Lidar.searchObstacle(-135, -90, 80, 100)

    def isNzone(self)::
	return self.Lidar.searchObstacle(90, 135, 80, 100)

    def isSzone(self):
	return self.Lidar.searchObstacle(-90, -45, 0, 80)

    def isTzone(self):
	return self.Lidar.searchObstacle(45, 90, 0, 80)

    def isUzone(self):
	return self.Lidar.searchObstacle(-135, -90, 0, 80)

    def isVzone(self):
	return self.Lidar.searchObstacle(90, 135, 0, 80)

    def isXzone_US(self):
	return (self.car.US.front_center_obstacle(80) and not self.car.US.front_center_obstacle(30))

    def isXzone_Lidar(self):
	return self.Lidar.searchObstacle(-15, 15, 30, 80)

    def isYzone(self):
	return (self.car.US.front_left_obstacle(70) and not self.car.US.front_left_obstacle(30)) or self.Lidar.searchObstaacle(-45, -15, 30, 80)

    def izZzone(self):
	return (self.car.US.front_right_obstacle(70) and not self.car.US.front_right_obstacle(30)) or self.Lidar.searchObstacle(15, 45, 30, 80)

#Function for Safety V1
    def usAzone(self):
        return self.car.US.front_left_obstacle()
    
    def lidarAzone(self):
        return self.car.lidar.searchObstacle(-45, -15, 100)
        return (self.Lidar.angle <= -15) and (self.Lidar.angle >= -45) and (self.Lidar.dist <= 100)
    
    def usBzone(self):
        return self.car.US.front_right_obstacle()
    
    def lidarBzone(self):
        return self.car.lidar.searchObstacle(15, 45, 100)
        return (self.Lidar.angle >= 15) and (self.Lidar.angle <= 45) and (self.Lidar.dist <= 100)

    def usCzone(self):
        return self.car.US.front_center_obstacle()
    
    def lidarCzone(self):
        return self.car.lidar.searchObstacle(-15, 15, 100)
        return (self.Lidar.angle <= 15) and (self.Lidar.angle >= -15) and (self.Lidar.dist <= 100)
    
    def usKzone(self):
        return self.car.US.rear_left_obstacle()
    
    def lidarKzone(self):
        return self.car.lidar.searchObstacle(-165, -135, 100)
        return (self.Lidar.angle <= -165) and (self.Lidar.angle >= -135) and (self.Lidar.dist <= 100)
    
    def usLzone(self):
        return self.car.US.rear_right_obstacle()
    
    def lidarLzone(self):
        return self.car.lidar.searchObstacle(135, 165, 100)
        return (self.Lidar.angle <= 165) and (self.Lidar.angle >= 135) and (self.Lidar.dist <= 100)
    
    def usMzone(self):
        return self.car.US.rear_center_obstacle()
    
    def lidarMzone(self):
        return self.car.lidar.searchObstacle(165, -165, 100)
        return ((self.Lidar.angle <= -165) or (self.Lidar.angle >= 165)) and (self.Lidar.dist <= 100)
    
    def lidarEzone(self):
        return self.car.lidar.searchObstacle(45, 135, 100)
        return (self.Lidar.angle <= 135) and (self.Lidar.angle >= 45)

    def lidarFzone(self):
        return self.car.lidar.searchObstacle(-135, -45, 100)
        return (self.Lidar.angle >= -135) and (self.Lidar.angle <= -45)

    def get_manual_order(self):
        # Warning: instructions are ordered by priority
        speed_order = self.car.speed
        steer_order = self.car.steer
        if self.incremental:
            # Emergency stop
            if self.xbox.B():
                print("EMERGENCY STOP")
                speed_order = klunk.motors.SPEED_STOP
            # Turn right
            elif self.xbox.dpadRight():
                print("RIGHT")
                # When asked to turn right while turning left: go straight
                if self.car.steer < klunk.motors.STEER_STRAIGHT:
                    steer_order = klunk.motors.STEER_STRAIGHT
                else:
                    steer_order = klunk.motors.righter(self.car.steer)
            # Turn left
            elif self.xbox.dpadLeft():
                print("LEFT")
                # When asked to turn left while turning right: go straight
                if self.car.steer > klunk.motors.STEER_STRAIGHT:
                    steer_order = klunk.motors.STEER_STRAIGHT
                else:
                    steer_order = klunk.motors.lefter(self.car.steer)
            # Speed down
            elif self.xbox.dpadDown() or self.xbox.leftBumper():
                print("DOWN")
                speed_order = klunk.motors.slower(self.car.speed)
            # Speed up
            elif self.xbox.dpadUp() or self.xbox.rightBumper():
                print("UP")
                speed_order = klunk.motors.faster(self.car.speed)
        else: # Linear mode
            rightTrigger = self.xbox.rightTrigger()
            leftTrigger = self.xbox.leftTrigger()

            if self.xbox.B():
                #print("BRAKE")
                speed_order = klunk.motors.SPEED_STOP
            elif leftTrigger and not rightTrigger:
                #print("REVERSE")
                speed_order = klunk.motors.SPEED_REVERSE
            elif rightTrigger < 0.25 or leftTrigger:
                #print("NO ACTION -> STOP")
                speed_order = klunk.motors.SPEED_STOP
            elif rightTrigger < 0.5:
                #print("SLOW SPEED")
                speed_order = klunk.motors.SPEED_SLOW
            elif rightTrigger < 0.75:
                #print("MEDIUM SPEED")
                speed_order = klunk.motors.SPEED_MEDIUM
            else:
                #print("FAST SPEED")
                speed_order = klunk.motors.SPEED_FAST

            joySteer = self.xbox.leftX()
            if joySteer < -0.75:
                steer_order = klunk.motors.STEER_LEFT_FAR
            elif joySteer < -0.5:
                steer_order = klunk.motors.STEER_LEFT_MIDDLE
            elif joySteer < -0.25:
                steer_order = klunk.motors.STEER_LEFT_CLOSE
            elif joySteer < 0.25:
                steer_order = klunk.motors.STEER_STRAIGHT
            elif joySteer < 0.5:
                steer_order = klunk.motors.STEER_RIGHT_CLOSE
            elif joySteer < 0.75:
                steer_order = klunk.motors.STEER_RIGHT_MIDDLE
            else:
                steer_order = klunk.motors.STEER_RIGHT_FAR

        if self.xbox.Y():
            self.incremental = not self.incremental
            print("MODE", "INCREMENTAL" if self.incremental else "LINEAR", "ACTIVATED")

        return speed_order, steer_order

    def get_auto_order(self):
        order = 0

        return order
