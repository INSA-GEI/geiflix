import klunk as k
import klunk.can
import klunk.motors
import klunk.ultrasound

MODES = ['IDLE', 'AUTO', 'MANUAL', 'STOP', 'UNSAFE']

class Car:
    def __init__(self, can_bus):
        self.speed = k.motors.SPEED_STOP
        self.steer = k.motors.STEER_STRAIGHT
        self.can_bus = can_bus
        self.send_motors_order()
        self.ultrasound = klunk.ultrasound.Ultrasound()
        self.unsafe = False
        self.mode = 'IDLE'

    def send_motors_order(self):
        self.can_bus.send(klunk.can.motors_message(self.speed, self.steer))

    def set_speed(self, speed):
        self.speed = speed

        if self.is_safe() or self.unsafe:
            self.send_motors_order()
        else:
            self.brake()

    def is_stopped(self):
        return self.speed == klunk.motors.SPEED_STOP

    def is_going_forward(self):
        return self.speed > klunk.motors.SPEED_STOP

    def is_going_backward(self):
        return self.speed < klunk.motors.SPEED_STOP

    def is_going_straight(self):
        return self.steer == klunk.motors.STEER_STRAIGHT

    def is_going_left(self):
        return self.steer < klunk.motors.STEER_STRAIGHT

    def is_going_right(self):
        return self.steer > klunk.motors.STEER_STRAIGHT

    def brake(self):
        self.set_speed(k.motors.SPEED_STOP)

    def faster(self):
        self.set_speed(k.motors.faster(self.speed))

    def slower(self):
        self.set_speed(k.motors.slower(self.speed))

    def set_steer(self, steer):
        self.steer = steer
        self.send_motors_order()

    def lefter(self):
        self.set_steer(k.motors.lefter(self.steer))

    def righter(self):
        self.set_steer(k.motors.righter(self.steer))

##### avoidance old treatment

    def update_ultrasound(self, message):
        self.ultrasound.update(message)
        if not self.is_safe() and not self.unsafe:
            self.brake()

    def is_safe(self):
        if self.is_going_forward():
            if self.is_going_straight() and self.ultrasound.front_obstacle():
                return False
            elif self.is_going_left() and (self.ultrasound.front_left_obstacle() or self.ultrasound.front_center_obstacle()):
                return False
            elif self.is_going_right() and (self.ultrasound.front_right_obstacle() or self.ultrasound.front_center_obstacle()):
                return False
        elif self.is_going_backward() and self.ultrasound.rear_obstacle():
            return False

        return True
