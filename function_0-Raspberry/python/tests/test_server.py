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
        data = data.decode()
        obstacle_amount, data = data.split(',', 1)
        obstacles = []
        for i in range(int(obstacle_amount)):
            angle, distance, size, data = data.split(',', 3)
            obstacles.append((angle, distance, size))

        print(obstacles)