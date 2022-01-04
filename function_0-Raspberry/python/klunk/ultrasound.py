
CAN_ID1 = 0x000
CAN_ID2 = 0x001
CAN_IDS = [CAN_ID1, CAN_ID2]

class Ultrasound:

    DEFAULT_THRESHOLD = 50
    
    def __init__(self):
        self.data = {
            'front-left'  : 0,
            'front-center': 0,
            'front-right' : 0,
            'rear-left'   : 0,
            'rear-center' : 0,
            'rear-right'  : 0
        }
    
    def update(self, message):
        if message.arbitration_id == CAN_ID1:
            self.data['front-left'] = int.from_bytes(message.data[0:2], byteorder='big')
            self.data['front-right'] = int.from_bytes(message.data[2:4], byteorder='big')
            self.data['rear-center'] = int.from_bytes(message.data[4:6], byteorder='big')
        elif message.arbitration_id == CAN_ID2:
            self.data['rear-left'] = int.from_bytes(message.data[0:2], byteorder='big')
            self.data['rear-right'] = int.from_bytes(message.data[2:4], byteorder='big')
            self.data['front-center'] = int.from_bytes(message.data[4:6], byteorder='big')
        print("front-right", self.data['front-right'], "front-center", self.data['front-center'])


    def __str__(self):
        result = f"front [{self.data['front-left']}, {self.data['front-center']}, {self.data['front-right']}]"
        result += '\n'
        result += f"rear  [{self.data['rear-left']}, {self.data['rear-center']}, {self.data['rear-right']}]"
        return result

    def front_left_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.data['front-left'] < threshold

    def front_right_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.data['front-right'] < threshold

    def front_center_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.data['front-center'] < threshold

    def front_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.front_left_obstacle(threshold) \
            or self.front_right_obstacle(threshold) \
            or self.front_center_obstacle(threshold)

    def rear_left_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.data['rear-left'] < threshold

    def rear_right_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.data['rear-right'] < threshold

    def rear_center_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.data['rear-center'] < threshold

    def rear_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.rear_left_obstacle(threshold) \
            or self.rear_right_obstacle(threshold) \
            or self.rear_center_obstacle(threshold)

    def any_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.front_obstacle(threshold) \
            or self.rear_obstacle(threshold)
