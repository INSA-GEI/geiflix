import math
from threading import Thread
import socket
import time # TODO: Autre moyen d'enlever les obstacles disparus

EXPIRATION = 5e+8 # 500 ms

def cart2pol(x, y):
    rho = math.sqrt(x**2 + y**2)
    phi = math.atan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * math.cos(phi)
    y = rho * math.sin(phi)
    return(x, y)


class Lidar(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.obstacles = []

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 6666))
            print("socket bound")

            while True:
                data, address = sock.recvfrom(1024)
                print("Lidar sent:", data)
                if not data:
                    break
                angle, distance, size = [float(n) for n in data.decode().split(',')]
                obstacle = (time.time_ns(), angle, distance, size)
                self.obstacles.append(obstacle)

    def removeOldObstacles(self):
        self.obstacles = [obstacle for obstacle in self.obstacles if time.time_ns() - obstacle[0] < EXPIRATION]

    def searchObstacle(self, minAngle, maxAngle, maxDistance):
        self.removeOldObstacles()
        for obstacle in self.obstacles:
            age, angle, distance, size = obstacle
            if distance > maxDistance:
                continue
            if minAngle <= maxAngle and (minAngle <= angle <= maxAngle):
                return True
            elif minAngle > maxAngle and ((angle >= minAngle) or (angle <= maxAngle)):
                return True



