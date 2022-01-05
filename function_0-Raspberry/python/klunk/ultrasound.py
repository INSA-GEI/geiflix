
CAN_ID1 = 0x000
CAN_ID2 = 0x001
CAN_IDS = [CAN_ID1, CAN_ID2]

class Ultrasound:

    DEFAULT_THRESHOLD = 50
    
    def __init__(self):
        self.front_left = 0
        self.front_center = 0
        self.front_right = 0
        self.rear_left = 0
        self.rear_center = 0
        self.rear_right = 0
    
    def update(self, message):
        if message.arbitration_id == CAN_ID1:
            self.front_left = int.from_bytes(message.data[0:2], byteorder='big')
            self.front_right = int.from_bytes(message.data[2:4], byteorder='big')
            self.rear_center = int.from_bytes(message.data[4:6], byteorder='big')
        elif message.arbitration_id == CAN_ID2:
            self.rear_left = int.from_bytes(message.data[0:2], byteorder='big')
            self.rear_right = int.from_bytes(message.data[2:4], byteorder='big')
            self.front_center = int.from_bytes(message.data[4:6], byteorder='big')
        #print("rear_right", self.rear_right, "rear_center", self.rear_center, "rear_left", self.rear_left)


    def __str__(self):
        result = f"front [{self.front_left}, {self.front_center}, {self.front_right}]"
        result += '\n'
        result += f"rear  [{self.rear_left}, {self.rear_center}, {self.rear_right}]"
        return result

    def front_left_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.front_left <= threshold

    def front_right_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.front_right <= threshold

    def front_center_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.front_center <= threshold

    def front_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.front_left_obstacle(threshold) \
            or self.front_right_obstacle(threshold) \
            or self.front_center_obstacle(threshold)

    def rear_left_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.rear_left <= threshold

    def rear_right_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.rear_right <= threshold

    def rear_center_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.rear_center <= threshold

    def rear_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.rear_left_obstacle(threshold) \
            or self.rear_right_obstacle(threshold) \
            or self.rear_center_obstacle(threshold)

    def any_obstacle(self, threshold = DEFAULT_THRESHOLD):
        return self.front_obstacle(threshold) \
            or self.rear_obstacle(threshold)
