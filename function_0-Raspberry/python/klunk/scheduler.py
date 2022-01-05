import xbox
import time

# Klunk modules
from . import car as kcar
from . import motors
from . import zone

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
    AVOID_AMOUNT_THRESHOLD = 5
    AVOID_UNKNOWN_WAIT_THRESHOLD = 5

    def __init__(self, car):
        self.incremental = False
        self.xbox = xbox.Joystick()
        if isinstance(car, kcar.Car):
            self.car = car
        else:
            raise TypeError("Invalid car or xbox controller")
        self.stop_avoiding()
        self.zoneA = zone.Zone(zone.isAzone, self.car)
        self.zoneB = zone.Zone(zone.isBzone, self.car)
        self.zoneC = zone.Zone(zone.isCzone, self.car)
        self.zoneK = zone.Zone(zone.isKzone, self.car)
        self.zoneL = zone.Zone(zone.isLzone, self.car)
        self.zoneM = zone.Zone(zone.isMzone, self.car)
        self.zoneN = zone.Zone(zone.isNzone, self.car)
        self.zoneS = zone.Zone(zone.isSzone, self.car)
        self.zoneT = zone.Zone(zone.isTzone, self.car)
        self.zoneU = zone.Zone(zone.isUzone, self.car)
        self.zoneV = zone.Zone(zone.isVzone, self.car)
        self.zoneX = zone.Zone(zone.isXzone, self.car)
        self.zoneY = zone.Zone(zone.isYzone, self.car)
        self.zoneZ = zone.Zone(zone.isZzone, self.car)

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
                    self.stop_avoiding()
# AUTO Mode
            elif self.car.mode == self.car.AUTO:

                # Simplified autonomous mode
                speed_order = motors.SPEED_MEDIUM
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
                if not self.isAzone() and self.xbox.A():
                    print("STOP -> AUTO")
                    self.car.mode = self.car.AUTO
                    self.stop_avoiding()
                elif self.xbox.Start():
                    print("STOP -> MANUAL")
                    self.car.mode = self.car.MANUAL
                elif self.xbox.rightThumbstick() and self.xbox.leftThumbstick() and \
                    self.car.is_stopped():
                    print("STOP -> UNSAFE")
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

#Function for Safety V2
    def isSafe(self, speed_order, steer_order):
        if self.car.mode != self.car.UNSAFE and self.car.mode != self.car.IDLE:
            ZoneA = self.zoneA.isZoneOccupied()
            ZoneB = self.zoneB.isZoneOccupied()
            ZoneC = self.zoneC.isZoneOccupied()
            ZoneK = self.zoneK.isZoneOccupied()
            ZoneL = self.zoneL.isZoneOccupied()
            ZoneM = self.zoneM.isZoneOccupied()
            ZoneN = self.zoneN.isZoneOccupied()
            ZoneS = self.zoneS.isZoneOccupied()
            ZoneT = self.zoneT.isZoneOccupied()
            ZoneU = self.zoneU.isZoneOccupied()
            ZoneV = self.zoneV.isZoneOccupied()
            ZoneX = self.zoneX.isZoneOccupied()
            ZoneY = self.zoneY.isZoneOccupied()
            ZoneZ = self.zoneZ.isZoneOccupied()
            #print("A", ZoneA, "B", ZoneB, "C", ZoneC, "K", ZoneK, "L", ZoneL, "M", ZoneM, "N", ZoneN, \
            #    "S", ZoneS, "T", ZoneT, "U", ZoneU, "V", ZoneV, "X", ZoneX, "Y", ZoneY, "Z", ZoneZ)
            #print(self.car.US)
            #print("#########################")
            #for obstacle in self.car.lidar.obstacles:
            #    print(f"{int(obstacle[0]):03} {int(obstacle[1]):03} {int(obstacle[2]):03}")
            #for i in range(10 - len(self.car.lidar.obstacles)):
            #    print()
            if (self.car.mode == self.car.MANUAL \
                or (self.car.mode == self.car.AUTO and not (self.avoid_right or self.avoid_left or self.avoid_unknown))):

                if ZoneA and (speed_order > motors.SPEED_STOP):
                    speed_order = motors.SPEED_STOP
                    if self.car.mode == self.car.AUTO:
                        self.car.mode = self.car.STOP

                if ZoneB and (speed_order == motors.SPEED_REVERSE):
                    speed_order = motors.SPEED_STOP
                    if self.car.mode == self.car.AUTO:
                        self.car.mode = self.car.STOP

                if ZoneC and (speed_order == motors.SPEED_FAST):
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
                        steer_order = motors.STEER_LEFT_CLOSE

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
                        or (ZoneY and ZoneZ):
                        if speed_order > motors.SPEED_STOP:
                            speed_order = motors.SPEED_STOP
                            self.car.mode = self.car.STOP
                        self.avoid_amount = 0

                    elif ZoneX or ZoneY or ZoneZ:
                        if speed_order > motors.SPEED_STOP:
                            speed_order = motors.SPEED_SLOW
                            if self.avoid_amount < self.AVOID_AMOUNT_THRESHOLD:
                                self.avoid_amount += 1
                            elif ZoneY:
                                self.avoid_right = True
                                steer_order = motors.STEER_RIGHT_FAR
                            elif ZoneZ:
                                self.avoid_left = True
                                steer_order = motors.STEER_LEFT_FAR
                            elif ZoneX:
                                self.avoid_unknown = True
                                self.avoid_unknown_wait = 0
                                speed_order = motors.SPEED_STOP
                            """
                            elif ZoneX:# By default, avoid to the left because left steering is better
                                self.avoid_left = True
                                steer_order = motors.STEER_LEFT_FAR
                            """
                    else:
                        self.avoid_amount = 0
            # Avoidance
            elif (self.car.mode == self.car.AUTO) and self.avoid_unknown:
                speed_order = motors.SPEED_STOP
                if self.avoid_unknown_wait >= self.AVOID_UNKNOWN_WAIT_THRESHOLD:
                    if ZoneA or (ZoneY and ZoneZ):
                        self.car.mode = self.car.STOP
                    elif ZoneY:
                        self.avoid_right = True
                        steer_order = motors.STEER_RIGHT_FAR
                    else: # By default, avoid to the left because left steering is better
                        self.avoid_left = True
                        steer_order = motors.STEER_LEFT_FAR
                    self.avoid_unknown = False
                else:
                    self.avoid_unknown_wait += 1

            elif (self.car.mode == self.car.AUTO) and (self.avoid_left or self.avoid_right):
                speed_order = motors.SPEED_SLOW

                if self.avoid_state == self.NOT_AVOIDING:
                    self.avoid_state = self.AVOID_BEFORE_FLEE_STEERING
                    steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
                    speed_order = motors.SPEED_STOP
                    self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                elif self.avoid_state == self.AVOID_BEFORE_FLEE_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_FLEE
                        steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
                        self.avoid_flee_time = time.time()
                    else:
                        steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_FLEE:
                    if ZoneA or (ZoneS if self.avoid_left else ZoneT):
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_flee_time >= self.AVOID_FLEE_TIME_THRESHOLD \
                        and not (ZoneX or ((ZoneZ or ZoneL or ZoneT) if self.avoid_left else (ZoneY or ZoneS or ZoneK))):
                        self.avoid_state = self.AVOID_FLEE_CORRECT_STEERING
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                        speed_order = motors.SPEED_STOP
                        self.avoid_flee_time = time.time() - self.avoid_flee_time
                        self.avoid_steering_time = time.time() + 2 * self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
                elif self.avoid_state == self.AVOID_FLEE_CORRECT_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_CORRECT
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                        self.avoid_correct_time = time.time()
                    else:
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_CORRECT:
                    if ZoneA or (ZoneT if self.avoid_left else ZoneS):
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_correct_time >= self.AVOID_CORRECT_TIME_THRESHOLD \
                        and not (ZoneX or ZoneY or ZoneZ):
                        self.avoid_state = self.AVOID_CORRECT_FORWARD_STEERING
                        steer_order = motors.STEER_STRAIGHT
                        speed_order = motors.SPEED_STOP
                        self.avoid_correct_time = time.time() - self.avoid_correct_time
                        self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                elif self.avoid_state == self.AVOID_CORRECT_FORWARD_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_FORWARD
                        steer_order = motors.STEER_STRAIGHT
                    else:
                        steer_order = motors.STEER_STRAIGHT
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_FORWARD:
                    if ZoneA:
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif not (ZoneX or ((ZoneZ or ZoneT or ZoneL) if self.avoid_left else (ZoneY or ZoneS or ZoneK))):
                        self.avoid_state = self.AVOID_FORWARD_RETURN_STEERING
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                        speed_order = motors.SPEED_STOP
                        self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_STRAIGHT
                elif self.avoid_state == self.AVOID_FORWARD_RETURN_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_RETURN
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                        self.avoid_return_time = time.time()
                    else:
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_RETURN:
                    if ZoneA or (ZoneT if self.avoid_left else ZoneS):
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_return_time >= self.avoid_correct_time \
                        and not (ZoneX or ((ZoneY or ZoneS or ZoneK) if self.avoid_left else (ZoneZ or ZoneT or ZoneL))):
                        self.avoid_state = self.AVOID_RETURN_END_STEERING
                        steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
                        speed_order = motors.SPEED_STOP
                        self.avoid_steering_time = time.time() + 2 * self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_RIGHT_FAR if self.avoid_left else motors.STEER_LEFT_FAR
                elif self.avoid_state == self.AVOID_RETURN_END_STEERING:
                    if time.time() >= self.avoid_steering_time:
                        self.avoid_state = self.AVOID_END
                        steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
                        self.avoid_end_time = time.time()
                    else:
                        steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
                        speed_order = motors.SPEED_STOP
                elif self.avoid_state == self.AVOID_END:
                    if ZoneA or (ZoneS if self.avoid_left else ZoneT):
                        speed_order = motors.SPEED_STOP
                        self.car.mode = self.car.STOP
                        self.stop_avoiding()
                    elif time.time() - self.avoid_end_time >= self.avoid_flee_time:
                        self.avoid_state = self.AVOID_AFTER_END_STEERING
                        steer_order = motors.STEER_STRAIGHT
                        speed_order = motors.SPEED_STOP
                        self.avoid_steering_time = time.time() + self.AVOID_STEERING_TIME_THRESHOLD
                    else:
                        steer_order = motors.STEER_LEFT_FAR if self.avoid_left else motors.STEER_RIGHT_FAR
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
        self.avoid_unknown = False
        self.avoid_unknown_wait = 0
        self.avoid_amount = 0

    def get_manual_order(self):
        # Warning: instructions are ordered by priority
        speed_order = self.car.speed
        steer_order = self.car.steer
        if self.incremental:
            # Emergency stop
            if self.xbox.B():
                print("EMERGENCY STOP")
                speed_order = motors.SPEED_STOP
            # Turn right
            elif self.xbox.dpadRight():
                print("RIGHT")
                # When asked to turn right while turning left: go straight
                if self.car.steer < motors.STEER_STRAIGHT:
                    steer_order = motors.STEER_STRAIGHT
                else:
                    steer_order = motors.righter(self.car.steer)
            # Turn left
            elif self.xbox.dpadLeft():
                print("LEFT")
                # When asked to turn left while turning right: go straight
                if self.car.steer > motors.STEER_STRAIGHT:
                    steer_order = motors.STEER_STRAIGHT
                else:
                    steer_order = motors.lefter(self.car.steer)
            # Speed down
            elif self.xbox.dpadDown() or self.xbox.leftBumper():
                print("DOWN")
                speed_order = motors.slower(self.car.speed)
            # Speed up
            elif self.xbox.dpadUp() or self.xbox.rightBumper():
                print("UP")
                speed_order = motors.faster(self.car.speed)
        else: # Linear mode
            rightTrigger = self.xbox.rightTrigger()
            leftTrigger = self.xbox.leftTrigger()

            if self.xbox.B():
                #print("BRAKE")
                speed_order = motors.SPEED_STOP
            elif leftTrigger and not rightTrigger:
                #print("REVERSE")
                speed_order = motors.SPEED_REVERSE
            elif rightTrigger < 0.25 or leftTrigger:
                #print("NO ACTION -> STOP")
                speed_order = motors.SPEED_STOP
            elif rightTrigger < 0.5:
                #print("SLOW SPEED")
                speed_order = motors.SPEED_SLOW
            elif rightTrigger < 0.75:
                #print("MEDIUM SPEED")
                speed_order = motors.SPEED_MEDIUM
            else:
                #print("FAST SPEED")
                speed_order = motors.SPEED_FAST

            joySteer = self.xbox.leftX()
            if joySteer < -0.75:
                steer_order = motors.STEER_LEFT_FAR
            elif joySteer < -0.5:
                steer_order = motors.STEER_LEFT_MIDDLE
            elif joySteer < -0.25:
                steer_order = motors.STEER_LEFT_CLOSE
            elif joySteer < 0.25:
                steer_order = motors.STEER_STRAIGHT
            elif joySteer < 0.5:
                steer_order = motors.STEER_RIGHT_CLOSE
            elif joySteer < 0.75:
                steer_order = motors.STEER_RIGHT_MIDDLE
            else:
                steer_order = motors.STEER_RIGHT_FAR

        if self.xbox.Y():
            self.incremental = not self.incremental
            print("MODE", "INCREMENTAL" if self.incremental else "LINEAR", "ACTIVATED")

        return speed_order, steer_order

    def get_auto_order(self):
        order = 0

        return order
