from . import car as kcar

class Zone:
    COUNTER_THRESHOLD = 5

    def __init__(self, predicate, car):
        if isinstance(car, kcar.Car):
            self.car = car
        else:
            raise TypeError("invalid car")
        self.state = False
        self.counter = 0
        self.predicate = predicate

    def __repr__(self):
        return f"{self.state} (counter: {self.counter}/{self.COUNTER_THRESHOLD})"

    def isZoneOccupied(self):
        self.update()
        return self.state

    def update(self):
        trigger = self.predicate(self.car)

        if not self.state:
            if trigger:
                self.state = True
                self.counter = 0
        else:
            if not trigger:
                self.counter += 1
                if self.counter >= self.COUNTER_THRESHOLD:
                    self.state = False
            else:
                self.counter = 0

def isAzone(car):
    return car.US.front_center_obstacle(30) \
        or car.US.front_right_obstacle(30) \
        or car.US.front_left_obstacle(30) \
        or car.lidar.searchObstacle(-45, 45, 40, 80)

def isBzone(car):
    return car.US.rear_center_obstacle(30) \
        or car.US.rear_right_obstacle(30) \
        or car.US.rear_left_obstacle(30) \
        or car.lidar.searchObstacle(-180, -135, 40, 80) \
        or car.lidar.searchObstacle(135, 180, 40, 80)

def isCzone(car):
    return car.lidar.searchObstacle(-45, -15, 120, 150) \
        or car.lidar.searchObstacle(15, 45, 120, 150) \
        or car.lidar.searchObstacle(-15, 15, 130, 150)

def isKzone(car):
    return car.lidar.searchObstacle(-90, -45, 80, 100)

def isLzone(car):
    return car.lidar.searchObstacle(45, 90, 80, 100)

def isMzone(car):
    return car.lidar.searchObstacle(-135, -90, 80, 100)

def isNzone(car):
    return car.lidar.searchObstacle(90, 135, 80, 100)

def isSzone(car):
    return car.lidar.searchObstacle(-90, -45, 0, 80)

def isTzone(car):
    return car.lidar.searchObstacle(45, 90, 0, 80)

def isUzone(car):
    return car.lidar.searchObstacle(-135, -90, 0, 80)

def isVzone(car):
    return car.lidar.searchObstacle(90, 135, 0, 80)

def isXzone(car):
    return (car.US.front_center_obstacle(80) and not car.US.front_center_obstacle(30)) \
        or car.lidar.searchObstacle(-15, 15, 80, 130)

def isYzone(car):
    return (car.US.front_left_obstacle(70) and not car.US.front_left_obstacle(30)) \
        or car.lidar.searchObstacle(-45, -15, 80, 120)

def isZzone(car):
    return (car.US.front_right_obstacle(70) and not car.US.front_right_obstacle(30)) \
        or car.lidar.searchObstacle(15, 45, 80, 120)
