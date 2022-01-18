import socket
import time
import Comm.py as Comm


if __name__ == '__main__':

    print(Comm.test)
    #with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        #server.bind((HOST, PORT))
        #server.listen()

        #conn, addr = server.accept()
        #while True:
            #msg = str(int(time.time())).encode('utf-8')
            #conn.send(msg)
            #time.sleep(0.5)
