import math
from threading import Thread
import socket

class Lidar(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.obstacles = []

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 6666))
            print("Lidar socket bound")

            while True:
                data, address = sock.recvfrom(1024)
                if not data:
                    break

                data = data.decode()
                obstacle_amount, data = data.split(',', 1)

                new_obstacles = []
                #print("################", int(obstacle_amount), "obstacles detected")
                for i in range(int(obstacle_amount)):
                    angle, distance, size, data = data.split(',', 3)
                    obstacle = (-math.degrees(float(angle)), 100 * float(distance), 100 * float(size))
                    new_obstacles.append(obstacle)
                    #print(f"{int(obstacle[0]):03} {int(obstacle[1]):03} {int(obstacle[2]):03}")
                #for i in range(10 - int(obstacle_amount)):
                    #print()
                self.obstacles = new_obstacles

    def searchObstacle(self, minAngle, maxAngle, minDistance, maxDistance):
        res = False

        for obstacle in self.obstacles:
            angle, distance, size = obstacle

            if  (minDistance <= distance <= maxDistance) and \
                ( (minAngle <= maxAngle and minAngle <= angle <= maxAngle)  \
                    or (minAngle > maxAngle and (angle >= minAngle or angle <= maxAngle)) ):
                res = True

        return res



