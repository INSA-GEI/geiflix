import math
from threading import Thread
import socket
import time # TODO: Autre moyen d'enlever les obstacles disparus

EXPIRATION = 0.5 # 500 ms

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
            sock.settimeout(0.5)
            sock.bind(('', 6666))
            print("Lidar socket bound")

            while True:
                try:
                    data, address = sock.recvfrom(1024)
                    if not data:
                        break
                    angle, distance, size = [float(n) for n in data.decode().split(',')]
                    obstacle = (time.time(), -angle, 100*distance, 100*size)
                    self.obstacles.append(obstacle)
                except socket.timeout:
                    pass
                self.removeOldObstacles()
    def removeOldObstacles(self):
        self.obstacles = [obstacle for obstacle in self.obstacles if time.time() - obstacle[0] < EXPIRATION]

    def searchObstacle(self, minAngle, maxAngle, minDistance, maxDistance):
        res = False

        for obstacle in self.obstacles:
            _, angle, distance, size = obstacle

            if  (minDistance <= distance <= maxDistance) and \
                ( (minAngle <= maxAngle and minAngle <= angle <= maxAngle)  \
                    or (minAngle > maxAngle and (angle >= minAngle or angle <= maxAngle)) ):
                res = True

        return res



