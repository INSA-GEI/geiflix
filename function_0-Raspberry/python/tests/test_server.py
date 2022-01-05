#! /usr/bin/env python
import socket

print("C'est parti")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    print("Socket créé")
    server_socket.bind(('', 6666))
    print("Socket bindé")

    while True:
        data, address = server_socket.recvfrom(1024)

        if not data:
            break
        print("Recieved data from IP", address)
        angle, distance, taille = [float(n) for n in data.decode().split(',')]
        print("Angle :", angle)
        print("Distance :", distance)
        print("Taille :", taille)
        print()
