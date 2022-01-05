import klunk.motors as motors
import klunk.car
import xbox
import time

REFRESH_RATE = 0.1

class Scheduler():
    NOT_AVOIDING = -1
    AVOID_BEFORE_FLEE_STEERING = 0
    AVOID_FLEE = 1
    AVOID_FLEE_CORRECT_STEERING = 2
    AVOID_CORRECT = 3
    AVOID_CORRECT_FORWARD_STEERING = 4
    AVOID_FORWARD = 5
    AVOID_FORWARD_RETURN_STEERING = 6
    AVOID_RETURN = 7
    AVOID_RETURN_END_STEERING = 8
    AVOID_END = 9
    AVOID_AFTER_END_STEERING = 10

    AVOID_STEERING_TIME_THRESHOLD = 2.5
    AVOID_FLEE_TIME_THRESHOLD = 6
    AVOID_CORRECT_TIME_THRESHOLD = AVOID_FLEE_TIME_THRESHOLD

    def __init__(self, car, joy):
        self.incremental = False
        if isinstance(car, klunk.car.Car):
            self.car = car
        if isinstance(joy, xbox.Joystick):
            self.xbox = joy
        self.stop_avoiding()

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
                elif self.xbox.A():
                    print("IDLE -> AUTO")
                    self.car.mode = self.car.AUTO
# AUTO Mode
            elif self.car.mode == self.car.AUTO:

                # Simplifed autonomous mode
                speed_order = motors.SPEED_FAST
                steer_order = motors.STEER_STRAIGHT

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

            speed_order, steer_order = self.isSafe(speed_order, steer_order)
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
        if self.car.mode != self.car.UNSAFE and self.car.mode != self.car.IDLE:
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
            ZoneV = self.isVzone()
            ZoneX = self.isXzone()
            ZoneY = self.isYzone()
            ZoneZ = self.isZzone()
            if (self.car.mode == self.car.MANUAL \
                or (self.car.mode == self.car.AUTO and not (self.avoid_right or self.avoid_left))):

                if ZoneA and speed_order > motors.SPEED_STOP:
                    speed_order = motors.SPEED_STOP
                    if self.car.mode == self.car.AUTO:
                        self.car.mode = self.car.STOP

                if ((ZoneB and speed_order) == motors.SPEED_REVERSE):
                    speed_order = motors.SPEED_STOP
                    if self.car.mode == self.car.AUTO:
                        self.car.mode = self.car.STOP

                if ZoneC and speed_order == motors.SPEED_FAST:
                    speed_order = motors.SPEED_MEDIUM

                if ZoneK or ZoneM:
                    if speed_order == motors.SPEED_FAST:
                        speed_order = motors.SPEED_MEDIUM

                    if steer_order == motors.STEER_LEFT_FAR:
                        steer_order = motors.STEER_LEFT_MIDDLE

                if ZoneL or ZoneN:
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

                if self.car.mode == self.car.MANUAL:
                    self.stop_avoiding()
                    if ZoneX or ZoneY or ZoneZ:
                        if speed_order > motors.SPEED_SLOW:
                            speed_order = motors.SPEED_SLOW

                        if ZoneY and (steer_order == motors.STEER_LEFT_FAR \
                                   or steer_order == motors.STEER_LEFT_MIDDLE \
                                   or steer_order == motors.STEER_LEFT_CLOSE):
                            steer_order = motors.STEER_STRAIGHT
                        elif ZoneZ and (steer_order == motors.STEER_RIGHT_FAR \
                                     or steer_order == motors.STEER_RIGHT_MIDDLE \
                                     or steer_order == motors.STEER_RIGHT_CLOSE):
                            steer_order = motors.STEER_STRAIGHT

                elif self.car.mode ==  self.car.AUTO:
                    if ((ZoneK or ZoneS) and ZoneZ) \
                        or ((ZoneL or ZoneT) and ZoneY) \
                        or (ZoneY and ZoneZ) \
                        or (ZoneX and ZoneZ) \
                        or (ZoneX and ZoneY):
                        if speed_order > motors.SPEED_STOP:
                            speed_order = motors.SPEED_STOP
                            self.car.mode = self.car.STOP

                    elif ZoneX or ZoneY or ZoneZ:
                        if speed_order > motors.SPEED_SLOW:
                            speed_order = motors.SPEED_SLOW
                            if ZoneY:
                                self.avoid_right = True
                                steer_order = motors.STEER_RIGHT_FAR
                            elif ZoneZ:
                                self.avoid_left = True
                                steer_order = motors.STEER_LEFT_FAR
                            elif ZoneX:
                                obstacle_distance = min(self.car.lidar.dist, self.car.US.front_center)
                                if obstacle_distance < 50 and speed_order > motors.SPEED_STOP:
                                    speed_order = motors.SPEED_STOP
                                    self.car.mode = self.car.STOP
                                elif self.isXZone_Lidar():
                                    if self.car.lidar.angle < 0:
                                        self.avoid_right = True
                                        steer_order = motors.STEER_RIGHT_FAR
                                else: # By default, avoid to the left
                                    self.avoid_left = True
                                    steer_order = motors.STEER_LEFT_FAR
            # Avoidance
            elif self.avoid_right:
                # TODO: avoid au lieu de stop
                speed_order = motors.SPEED_STOP
            elif self.avoid_left:
                speed_order = motors.SPEED_SLOW

                if self.avoid_state == self.NOT_AVOIDING:
                    self.avoid_state = self.AVOID_BEFORE_FLEE_STEERING
                    steer_order = motors.STEER_LEFT_FAR
                    self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                elif self.avoid_state == self.AVOID_BEFORE_FLEE_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_FLEE
                        self.avoid_flee_time = time.time()
                    else:
                        steer_order = motors.STEER_LEFT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_FLEE:
                    if ZoneA or ZoneS:
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_flee_time >= self.AVOID_FLEE_TIME_THRESHOLD \
                        and not (ZoneX or ZoneZ or ZoneL or ZoneT):
                        self.avoid_state = self.AVOID_FLEE_CORRECT_STEERING
                        steer_order = motors.STEER_RIGHT_FAR
                        self.avoid_steering_time = time.time() + 2 * self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_LEFT_FAR
                elif self.avoid_state == self.AVOID_FLEE_CORRECT_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_CORRECT
                        self.avoid_flee_time = time.time() - self.avoid_flee_time
                        self.avoid_correct_time = time.time()
                    else:
                        steer_order = motors.STEER_RIGHT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_CORRECT:
                    if ZoneA or ZoneT:
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_flee_time >= self.AVOID_CORRECT_TIME_THRESHOLD \
                        and not (ZoneX or ZoneY or ZoneZ):
                        self.avoid_state = self.AVOID_CORRECT_FORWARD_STEERING
                        steer_order = motors.STEER_STRAIGHT
                        self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_RIGHT_FAR
                elif self.avoid_state == self.AVOID_CORRECT_FORWARD_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_FORWARD
                        steer_order = motors.STEER_STRAIGHT
                        self.avoid_correct_time = time.time() - self.avoid_correct_time
                    else:
                        steer_order = motors.STEER_STRAIGHT
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_FORWARD:
                    if ZoneA:
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif not (ZoneX or ZoneZ or ZoneT or ZoneL):
                        self.avoid_state = self.AVOID_FORWARD_RETURN_STEERING
                        steer_order = motors.STEER_RIGHT_FAR
                        self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_STRAIGHT
                elif self.avoid_state == self.AVOID_FORWARD_RETURN_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_RETURN
                        steer_order = motors.STEER_RIGHT_FAR
                        self.avoid_return_time = time.time()
                    else:
                        steer_order = motors.STEER_RIGHT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_RETURN:
                    if ZoneA or ZoneT:
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_return_time >= self.avoid_correct_time \
                        and not (ZoneX or ZoneY or ZoneT or ZoneK):
                        self.avoid_state = self.AVOID_RETURN_END_STEERING
                        steer_order = motors.STEER_LEFT_FAR
                        self.avoid_steering_time = time.time() + 2 * self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_RIGHT_FAR
                elif self.avoid_state == self.AVOID_RETURN_END_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_END
                        steer_order = motors.STEER_LEFT_FAR
                        self.avoid_end_time = time.time()
                    else:
                        steer_order = motors.STEER_LEFT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_END:
                    if ZoneA or ZoneS:
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_end_time >= self.avoid_flee_time:
                        self.avoid_state = self.AVOID_AFTER_END_STEERING
                        steer_order = motors.STEER_STRAIGHT
                        self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_LEFT_FAR
                elif self.avoid_state == self.AVOID_AFTER_END_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.stop_avoiding()
                        steer_order = motors.STEER_STRAIGHT
                    else:
                        steer_order = motors.STEER_STRAIGHT
                        speed_order = motors.SPEED_STOP

        return speed_order, steer_order

    def stop_avoiding(self):
        self.avoid_state = self.NOT_AVOIDING
        self.avoid_left = False
        self.avoid_right = False

    def isAzone(self):
        return self.car.US.front_center_obstacle(30) \
            or self.car.US.front_right_obstacle(30) \
            or self.car.US.front_left_obstacle(30) \
            or self.car.lidar.searchObstacle(-45, 45, 40, 80)

    def isBzone(self):
        return self.car.US.rear_center_obstacle(30) \
            or self.car.US.rear_right_obstacle(30) \
            or self.car.US.rear_left_obstacle(30) \
            or self.car.lidar.searchObstacle(-180, -135, 40, 80) \
            or self.car.lidar.searchObstacle(135, 180, 40, 80)

    def isCzone(self):
        US = (self.car.US.front_center_obstacle(100) and not self.car.US.front_center_obstacle(80)) \
            or (self.car.US.front_right_obstacle(100) and not self.car.US.front_right_obstacle(70)) \
            or (self.car.US.front_left_obstacle(100) and not self.car.US.front_left_obstacle(70))

        Lidar = self.car.lidar.searchObstacle(-45, -15, 120, 150) \
            or self.car.lidar.searchObstacle(15, 45, 120, 150) \
            or self.car.lidar.searchObstacle(-15, 15, 130, 150)

        return US or Lidar

    def isKzone(self):
        return self.car.lidar.searchObstacle(-90, -45, 80, 100)

    def isLzone(self):
        return self.car.lidar.searchObstacle(45, 90, 80, 100)

    def isMzone(self):
        return self.car.lidar.searchObstacle(-135, -90, 80, 100)

    def isNzone(self):
        return self.car.lidar.searchObstacle(90, 135, 80, 100)

    def isSzone(self):
        return self.car.lidar.searchObstacle(-90, -45, 0, 80)

    def isTzone(self):
        return self.car.lidar.searchObstacle(45, 90, 0, 80)

    def isUzone(self):
        return self.car.lidar.searchObstacle(-135, -90, 0, 80)

    def isVzone(self):
        return self.car.lidar.searchObstacle(90, 135, 0, 80)

    def isXzone_lidar(self):
        return self.car.lidar.searchObstacle(-15, 15, 30, 80)

    def isXzone_US(self):
        return self.car.US.front_center_obstacle(80) and not self.car.US.front_center_obstacle(30)

    def isXzone(self):
        return self.isXzone_US() or self.isXzone_lidar()

    def isYzone(self):
        return (self.car.US.front_left_obstacle(70) and not self.car.US.front_left_obstacle(30)) or self.car.lidar.searchObstacle(-45, -15, 30, 80)

    def isZzone(self):
        return (self.car.US.front_right_obstacle(70) and not self.car.US.front_right_obstacle(30)) or self.car.lidar.searchObstacle(15, 45, 30, 80)

#Function for Safety V1
    def usAzone(self):
        return self.car.US.front_left_obstacle()
    
    def lidarAzone(self):
        return self.car.lidar.searchObstacle(-45, -15, 0, 100)
        return (self.car.lidar.angle <= -15) and (self.car.lidar.angle >= -45) and (self.car.lidar.dist <= 100)
    
    def usBzone(self):
        return self.car.US.front_right_obstacle()
    
    def lidarBzone(self):
        return self.car.lidar.searchObstacle(15, 45, 0, 100)
        return (self.car.lidar.angle >= 15) and (self.car.lidar.angle <= 45) and (self.car.lidar.dist <= 100)

    def usCzone(self):
        return self.car.US.front_center_obstacle()
    
    def lidarCzone(self):
        return self.car.lidar.searchObstacle(-15, 15, 0, 100)
        return (self.car.lidar.angle <= 15) and (self.car.lidar.angle >= -15) and (self.car.lidar.dist <= 100)
    
    def usKzone(self):
        return self.car.US.rear_left_obstacle()
    
    def lidarKzone(self):
        return self.car.lidar.searchObstacle(-165, -135, 0, 100)
        return (self.car.lidar.angle <= -165) and (self.car.lidar.angle >= -135) and (self.car.lidar.dist <= 100)
    
    def usLzone(self):
        return self.car.US.rear_right_obstacle()
    
    def lidarLzone(self):
        return self.car.lidar.searchObstacle(135, 165, 0, 100)
        return (self.car.lidar.angle <= 165) and (self.car.lidar.angle >= 135) and (self.car.lidar.dist <= 100)
    
    def usMzone(self):
        return self.car.US.rear_center_obstacle()
    
    def lidarMzone(self):
        return self.car.lidar.searchObstacle(165, -165, 0, 100)
        return ((self.car.lidar.angle <= -165) or (self.car.lidar.angle >= 165)) and (self.car.lidar.dist <= 100)
    
    def lidarEzone(self):
        return self.car.lidar.searchObstacle(45, 135, 0, 100)
        return (self.car.lidar.angle <= 135) and (self.car.lidar.angle >= 45)

    def lidarFzone(self):
        return self.car.lidar.searchObstacle(-135, -45, 0, 100)
        return (self.car.lidar.angle >= -135) and (self.car.lidar.angle <= -45)

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