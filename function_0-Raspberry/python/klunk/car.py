import klunk as k
import klunk.can as can
import klunk.motors as motors
import klunk.ultrasound as us
import klunk.lidar as lidar

IDLE   = 0
AUTO   = 1
MANUAL = 2
STOP   = 3
UNSAFE = 4
MODES  = [IDLE, AUTO, MANUAL, STOP, UNSAFE]

class Car:
    def __init__(self, can_bus):
        #init engine
        self.speed = motors.SPEED_STOP
        self.steer = motors.STEER_STRAIGHT
        self.can_bus = can_bus
        self.send_motors_order()
        #init sensors
        self.US = us.Ultrasound()
        self.lidar = lidar.Lidar()
        #init status
        self.mode = 'IDLE'

    def send_motors_order(self):
        self.can_bus.send(can.motors_message(self.speed, self.steer))

#engine commands
    def set_speed(self, speed):
        #safety - to be set in avoidance
        if self.is_safe() or self.mode == UNSAFE:
            self.speed = speed
        else:
            self.speed = motors.SPEED_STOP
        self.send_motors_order()

    def brake(self):
        self.set_speed(motors.SPEED_STOP)

    def faster(self):
        self.set_speed(motors.faster(self.speed))

    def slower(self):
        self.set_speed(motors.slower(self.speed))

    def set_steer(self, steer):
        self.steer = steer
        self.send_motors_order()

    def lefter(self):
        self.set_steer(motors.lefter(self.steer))

    def righter(self):
        self.set_steer(motors.righter(self.steer))

#car status
    def set_mode(self, new_mode):
        self.mode = new_mode

    def get_mode(self):
        return self.mode

    def is_stopped(self):
        return self.speed == motors.SPEED_STOP

    def is_going_forward(self):
        return self.speed > motors.SPEED_STOP

    def is_going_backward(self):
        return self.speed < motors.SPEED_STOP

    def is_going_straight(self):
        return self.steer == motors.STEER_STRAIGHT

    def is_going_left(self):
        return self.steer < motors.STEER_STRAIGHT

    def is_going_right(self):
        return self.steer > motors.STEER_STRAIGHT

#sensor commands
def update_us(self, message):
    self.US.update(message)

##### avoidance old treatment


    def is_safe(self):
        if self.is_going_forward():
            if self.is_going_straight() and self.US.front_obstacle():
                return False
            elif self.is_going_left() and (self.US.front_left_obstacle() or self.US.front_center_obstacle()):
                return False
            elif self.is_going_right() and (self.US.front_right_obstacle() or self.US.front_center_obstacle()):
                return False
        elif self.is_going_backward() and self.US.rear_obstacle():
            return False

        return True
