import math
from threading import Thread
import socket

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
        self.scan = {}

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(('', 6666))

            while True:
                data, address = socket.recvfrom(1024)
                if not data:
                    break
                angle, distance = [float(n) for n in data.decode().split(',')]

                self.scan[angle] = distance

