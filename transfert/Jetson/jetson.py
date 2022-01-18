# import socket programming library
import socket

# import thread module
from _thread import *
import threading
import numpy as np
print_lock = threading.Lock()


#camera libraries
#import keyboard
import cv2
from cv2 import aruco
from identifyID import identify,identify2
# liste des IDs
products = [10,20,25,30]



###################camera init#################
global cap
cap = cv2.VideoCapture(0)  # Changer la valeur en fonction de la caméra utilisée
# Taille du marqueur
marker_length = 0.056  # [m]
# Sélection du dictionnaire de marqueurs
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)

# camera_matrix = np.load("mtx.npy")
# distortion_coeff = np.load("dist.npy")
# Si vous avez calibré la caméra, utilisez ce qui précède.
camera_matrix = np.array([[1.42068235e+03, 0.00000000e+00, 9.49208512e+02],
                          [0.00000000e+00, 1.37416685e+03, 5.39622051e+02],
                          [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]])
distortion_coeff = np.array([1.69926613e-01, -7.40003491e-01, -7.45655262e-03, -1.79442353e-03, 2.46650225e+00])
#########################################################

def send_to_rasp(c,err=0,dir='S'):
    # direction gauche/droite
    if dir == 'R':
        direction = ' turn_right'
        # conversion en string
        data = str(err) + direction
        # encodage utf8
        data = bytes(data, 'UTF-8')
        # data = np.random.randint(1, 10)
        # data=data.to_bytes(2,'big')
        # envoi vers client
        c.send(data)
    elif dir == 'L':
        direction = ' turn_left'
        # conversion en string
        data = str(err) + direction
        # encodage utf8
        data = bytes(data, 'UTF-8')
        # data = np.random.randint(1, 10)
        # data=data.to_bytes(2,'big')
        # envoi vers client
        c.send(data)
    elif dir=='S':
        direction = ' straight'
        # conversion en string
        data = str(err) + direction
        # encodage utf8
        data = bytes(data, 'UTF-8')
        # data = np.random.randint(1, 10)
        # data=data.to_bytes(2,'big')
        # envoi vers client
        c.send(data)
    elif dir =='N':
        direction = ' not_gate'
        # conversion en string
        data = str(err) + direction
        # encodage utf8
        data = bytes(data, 'UTF-8')
        # data = np.random.randint(1, 10)
        # data=data.to_bytes(2,'big')
        # envoi vers client
        c.send(data)
    elif dir =='W':
        direction = ' wrong_gate'
        # conversion en string
        data = str(err) + direction
        # encodage utf8
        data = bytes(data, 'UTF-8')
        # data = np.random.randint(1, 10)
        # data=data.to_bytes(2,'big')
        # envoi vers client
        c.send(data)
    else:
        raise ValueError("Invalid direction")

def capture(c,choice,margin):
    while True:

        # frame camera initializaiton
        ret, img = cap.read()
        height, width = img.shape[:2]


        # aruco initialization
        parameters = aruco.DetectorParameters_create()  # Marker detection parameters
        corners, ids, rejectedImgPoints = aruco.detectMarkers(img, dictionary,parameters=parameters)
        aruco.drawDetectedMarkers(img, corners, ids, (0,255,255))

        # trait vertical
        for i in range(height):
            img[i][int(width / 2)] = [255, 0, 0]
        #print(corners)
        # number of aruco markers detected
        nb_aruco= len(corners)
        # describe the type of font to be used.
        font = cv2.FONT_HERSHEY_SIMPLEX
        # display number of aruco markers detected
        cv2.putText(img,
                    f'{nb_aruco} Aruco markers detected.',
                    (50, 50),
                    font, 1,
                    (0, 255, 255),
                    2,
                    cv2.LINE_4)
        #if len(corners)==1:
           # x = (corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]) / 4
            #y = (corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]) / 4
            #cv2.circle(img, (int(x), int(y)), 50, (255, 0, 0), 4)


        if len(corners) > 0:
            #Traiter par marqueur
            for i, corner in enumerate(corners):

                rvec, tvec, _ = aruco.estimatePoseSingleMarkers(corner, marker_length, camera_matrix, distortion_coeff)

                #Supprimer les axes inutiles
                tvec = np.squeeze(tvec)
                rvec = np.squeeze(rvec)
                #Conversion de vecteur de rotation en origines
                rvec_matrix = cv2.Rodrigues(rvec)
                rvec_matrix = rvec_matrix[0] #Extrait de rodorigues
                #Traduction du vecteur translationnel
                transpose_tvec = tvec[np.newaxis, :].T
                #Synthétique
                proj_matrix = np.hstack((rvec_matrix, transpose_tvec))
                #Conversion en angle d'Euler
                euler_angle = cv2.decomposeProjectionMatrix(proj_matrix)[6] # [deg]

                #num_id = ids[i]
                #print("ID : " + str(ids[i]))

                #Visualisation
                draw_pole_length = marker_length/2 #Longueur réelle[m]
                aruco.drawAxis(img, camera_matrix, distortion_coeff, rvec, tvec, draw_pole_length)

            if nb_aruco==2:
                num_id1= ids[0]
                num_id2= ids[1]
                x = (corners[0][0][0][0] + corners[0][0][1][0] + corners[0][0][2][0] + corners[0][0][3][0]) / 4
                y = (corners[0][0][0][1] + corners[0][0][1][1] + corners[0][0][2][1] + corners[0][0][3][1]) / 4
                x2 = (corners[1][0][0][0] + corners[1][0][1][0] + corners[1][0][2][0] + corners[1][0][3][0]) / 4
                y2 = (corners[1][0][0][1] + corners[1][0][1][1] + corners[1][0][2][1] + corners[1][0][3][1]) / 4

                # print(f"Center coordinates : ({int(np.abs(x+x2)/2)}, {int(np.abs(y+y2)/2)})")
                # good gate detected, it's the choice that we've made
                if num_id1==num_id2 and num_id1==choice:

                    cv2.putText(img,
                                'Aruco codes identical -> GOOD GATE DETECTED',
                                (50, 100),
                                font, 0.5,
                                (0, 255, 0),
                                2,
                                cv2.LINE_4)
                    cv2.putText(img,
                                f'ID : {num_id1}',
                                (50, 150),
                                font, 0.5,
                                (0, 255, 0),
                                2,
                                cv2.LINE_4)
                    cv2.putText(img,f"Center coordinates : ({int(np.abs(x+x2)/2)}, {int(np.abs(y+y2)/2)})",
                                (50,200),
                                font,0.5,
                                (0,255,0),
                                2,
                                cv2.LINE_4)
                    cv2.circle(img, (int(np.abs(x + x2) / 2), int(np.abs(y + y2) / 2)), 5, (255, 0, 0), 4)
                    cv2.rectangle(img,(int(x),int(y)),(int(x2),int(y2)),(255,0,0),4)
                    A= int(np.abs(x + x2) / 2)
                    B= int(np.abs(y + y2)/ 2)
                    C=int(width / 2)

                    # margin around the center
                    D= C-margin
                    E= C+margin
                    erreur=0.1*np.abs(x-x2)
                    if A in range(D,E):
                        cv2.putText(img,
                                    f'car in the center',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        send_to_rasp(c,0,'S')
                    elif (A<D):
                        dist = D - A
                        cv2.putText(img,
                                    f'gate too far to the left, turn left by a distance: {dist}',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        cv2.putText(img,
                                    f' éloignement de : {erreur}',
                                    (50, 350),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        send_to_rasp(c, dist, 'L')
                    elif (A>E):
                        dist = A - E
                        cv2.putText(img,
                                    f'gate too far to the right, turn right by a distance: {dist}',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        cv2.putText(img,
                                    f' éloignement de : {erreur}',
                                    (50, 350),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        send_to_rasp(c, dist, 'R')
                # gate detected but not the right one
                elif num_id1==num_id2 and num_id1!=choice:
                    cv2.putText(img,
                                'Aruco codes identical -> WRONG GATE DETECTED',
                                (50, 100),
                                font, 0.5,
                                (0,0 , 255),
                                2,
                                cv2.LINE_4)
                    cv2.putText(img,
                                f'ID : {num_id1}',
                                (50, 150),
                                font, 0.5,
                                (0,0 , 255),
                                2,
                                cv2.LINE_4)
                    send_to_rasp(c, 0,'W')
                # it's not a gate
                else:
                    cv2.putText(img,
                                f'Aruco codes not identical -> MOVE BACK',
                                (50, 100),
                                font, 0.5,
                                (0, 0, 255),
                                2,
                                cv2.LINE_4)
                    send_to_rasp(c, 0, 'N')

            elif nb_aruco>2:
                goodPair=identify2(ids,choice)
                if goodPair.num1 != 99 and goodPair.num2 != 99:
                    index1=goodPair.num1
                    index2=goodPair.num2
                    x = (corners[index1][0][0][0] + corners[index1][0][1][0] + corners[index1][0][2][0] + corners[index1][0][3][0]) / 4
                    y = (corners[index1][0][0][1] + corners[index1][0][1][1] + corners[index1][0][2][1] + corners[index1][0][3][1]) / 4
                    x2 = (corners[index2][0][0][0] + corners[index2][0][1][0] + corners[index2][0][2][0] + corners[index2][0][3][0]) / 4
                    y2 = (corners[index2][0][0][1] + corners[index2][0][1][1] + corners[index2][0][2][1] + corners[index2][0][3][1]) / 4

                    cv2.putText(img,
                                'Aruco codes identical -> GOOD GATE DETECTED',
                                (50, 100),
                                font, 0.5,
                                (0, 255, 0),
                                2,
                                cv2.LINE_4)
                    cv2.putText(img,
                                f'ID : {choice}',
                                (50, 150),
                                font, 0.5,
                                (0, 255, 0),
                                2,
                                cv2.LINE_4)
                    cv2.putText(img, f"Center coordinates : ({int(np.abs(x + x2) / 2)}, {int(np.abs(y + y2) / 2)})",
                                (50, 200),
                                font, 0.5,
                                (0, 255, 0),
                                2,
                                cv2.LINE_4)

                    cv2.circle(img, (int(np.abs(x + x2) / 2), int(np.abs(y + y2) / 2)), 5, (255, 0, 0), 4)
                    cv2.rectangle(img, (int(x), int(y)), (int(x2), int(y2)), (255, 0, 0), 4)
                    A = int(np.abs(x + x2) / 2)
                    B = int(np.abs(y + y2) / 2)
                    C = int(width / 2)

                    # margin around the center
                    D = C - margin
                    E = C + margin

                    if A in range(D, E):
                        cv2.putText(img,
                                    f'car in the center',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        send_to_rasp(c, 0, 'S')
                    elif (A < D):
                        dist = D - A
                        cv2.putText(img,
                                    f'gate too far to the left, turn left by a distance: {dist}',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        send_to_rasp(c, dist, 'L')
                    elif (A > E):
                        dist = A-E
                        cv2.putText(img,
                                    f'gate too far to the right, turn right by a distance : {dist}',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        send_to_rasp(c, dist, 'R')
            elif nb_aruco ==1:
                send_to_rasp(c, 0, 'N')

        else:
            send_to_rasp(c, 0, 'N')
        cv2.imshow('drawDetectedMarkers', img)

        #press q to break the loop and close camera
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()




# thread function
def threaded(c):

    while True:

    # data received from client
        data1 = c.recv(1024)
        #if not data1:
         #   print('Bye')

            #lock released on exit
           # print_lock.release()
            #break



        # reverse the given string from client
        #error=200

 #       if keyboard.is_pressed('q'):
  #          break  # if key 'q' is pressed

        #CALCULATE ERROR HERE
        capture(c,20,20)
        #test=np.random.randint(1,5,1)
        #send_to_rasp(c,200,'S')
        #send_to_rasp(c, 78, 'W')


    # connection closed
    c.close()


def Main():
    #adress JETSON
    host = "192.168.1.10"

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 1025
    # CHANGER TCP TO UDP SI JAMAIS
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")



    # a forever loop until client wants to exit
    while True:
   #     if keyboard.is_pressed('q'):
    #        break# if key 'q' is pressedq
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier

        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':

    Main()
