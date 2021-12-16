from threading import Thread
import can
import klunk as k
import klunk.motors
import klunk.ultrasound as us

def can_message(can_id, can_data):
    return can.Message(arbitration_id=can_id, data=can_data, is_extended_id=False)

def motors_message(speed, steer):
    if speed not in k.motors.SPEEDS or steer not in k.motors.STEERS:
        raise ValueError("Invalid speed or steer value")

    return can_message(k.motors.CAN_ID, [speed, steer])

def is_message_from_ids(message, ids):
    if isinstance(ids, list):
        return message.arbitration_id in ids
    else:
        return message.arbitration_id == ids


class Can(Thread):
    def __init__(self,bus,car):
        Thread.__init__(self)
        self.bus = bus
        self.car = car

    def run(self):
        while True:
            data = self.bus.recv(1024)

            if klunk.can.is_message_from_ids(data, klunk.ultrasound.CAN_IDS):
                self.car.update_ultrasound(data)

            #if klunk.can.is_message_from_ids(data, klunk.mapping.CAN_IDS):
                #self.car.update_IMU(data)
                #self.car.update_GPS(data)
