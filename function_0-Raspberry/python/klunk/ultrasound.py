import can
import klunk as k
import klunk.can

CAN_ID1 = 0x000
CAN_ID2 = 0x001
CAN_IDS = [CAN_ID1, CAN_ID2]

class Ultrasound:
    # An obstacle is detected if ultrasound value less than this threshold
    OBSTACLE_THRESHOLD = 50
    
    def __init__(self):
        self.values = {
            'front-left'  : 0,
            'front-center': 0,
            'front-right' : 0,
            'rear-left'   : 0,
            'rear-center' : 0,
            'rear-right'  : 0
        }
    
    def update(self, message):
        if message.arbitration_id == CAN_ID1:
            self.values['front-left'] = int.from_bytes(message.data[0:2], byteorder='big')
            self.values['front-right'] = int.from_bytes(message.data[2:4], byteorder='big')
            self.values['rear-center'] = int.from_bytes(message.data[4:6], byteorder='big')
        elif message.arbitration_id == CAN_ID2:
            self.values['rear-left'] = int.from_bytes(message.data[0:2], byteorder='big')
            self.values['rear-right'] = int.from_bytes(message.data[2:4], byteorder='big')
            self.values['front-center'] = int.from_bytes(message.data[4:6], byteorder='big')
        print("front-right", self.values['front-right'], "front-center", self.values['front-center'])


    def __str__(self):
        result = f"front [{self.values['front-left']}, {self.values['front-center']}, {self.values['front-right']}]"
        result += '\n'
        result += f"rear  [{self.values['rear-left']}, {self.values['rear-center']}, {self.values['rear-right']}]"
        return result

    def front_left_obstacle(self):
        return self.values['front-left'] < Ultrasound.OBSTACLE_THRESHOLD

    def front_right_obstacle(self):
        return self.values['front-right'] < Ultrasound.OBSTACLE_THRESHOLD

    def front_center_obstacle(self):
        return self.values['front-center'] < Ultrasound.OBSTACLE_THRESHOLD

    def front_obstacle(self):
        return self.front_left_obstacle() or self.front_right_obstacle() \
                or self.front_center_obstacle()

    def rear_left_obstacle(self):
        return self.values['rear-left'] < Ultrasound.OBSTACLE_THRESHOLD

    def rear_right_obstacle(self):
        return self.values['rear-right'] < Ultrasound.OBSTACLE_THRESHOLD

    def rear_center_obstacle(self):
        return self.values['rear-center'] < Ultrasound.OBSTACLE_THRESHOLD

    def rear_obstacle(self):
        return self.rear_left_obstacle() or self.rear_right_obstacle() \
                or self.rear_center_obstacle()
