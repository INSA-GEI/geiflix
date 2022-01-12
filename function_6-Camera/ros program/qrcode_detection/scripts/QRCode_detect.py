import asyncio
from asyncio import sleep

import numpy as np
import cv2
from cv2 import aruco
from identifyID import identify,identify2
# liste des IDs
products = [10,20,25,30]
#global nb_aruco
#nb_aruco=0
def choice():
    done = False
    while done == False:
        choice=input("What product do you deliver?\n1.Tomatoes\n2.Sneakers\n3.Beer kegs\n4.Wood planks\nEnter the corresponding number:\n")
        if choice.isdigit()== False:
            print("Error, enter one of the 4 numbers.")
            continue
        choice = int(choice)
        if choice != 1 and choice != 2 and choice != 3 and choice != 4:
            print("Error, enter one of the 4 numbers.")
        else:
            done = True
    good_id = products[choice-1]
    print (f"It is therefore necessary to detect the Aruco ID n °{good_id}.")
    return good_id




def capture(choice):
    cap = cv2.VideoCapture(0) #Changer la valeur en fonction de la caméra utilisée
    #Taille du marqueur
    marker_length = 0.056 # [m]
    #Sélection du dictionnaire de marqueurs
    dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_1000)

    #camera_matrix = np.load("mtx.npy")
    #distortion_coeff = np.load("dist.npy")
    #Si vous avez calibré la caméra, utilisez ce qui précède.
    camera_matrix = np.array( [[1.42068235e+03,0.00000000e+00,9.49208512e+02],
    [0.00000000e+00,1.37416685e+03,5.39622051e+02],
    [0.00000000e+00,0.00000000e+00,1.00000000e+00]] )
    distortion_coeff = np.array( [1.69926613e-01,-7.40003491e-01,-7.45655262e-03,-1.79442353e-03, 2.46650225e+00] )

    while True:
        ret, img = cap.read()
        height, width = img.shape[:2]



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
                    D= C-20
                    E= C+20
                    if A in range(D,E):
                        cv2.putText(img,
                                    f'car in the center',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                    elif (A<D):
                        dist= D-A
                        erreur= (dist*100)/ (int(x-x2))
                        cv2.putText(img,
                                    f'car too far to the left, turn right by a distance: {dist}',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        cv2.putText(img,
                                    f' therefore an error of : {erreur}',
                                    (50, 350),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                    elif (A>E):
                        dist2 = A - E
                        erreur2 = (dist2*100) / (int(x-x2))
                        cv2.putText(img,
                                    f'car too far to the right, turn left by a distance: {dist2}',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                        cv2.putText(img,
                                    f' therefore an error of  : {erreur2}',
                                    (50, 350),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
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
                # it's not a gate
                else:
                    cv2.putText(img,
                                f'Aruco codes not identical -> MOVE BACK',
                                (50, 100),
                                font, 0.5,
                                (0, 0, 255),
                                2,
                                cv2.LINE_4)

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
                                f'ID : {goodPair.pairID}',
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
                    D = C - 20
                    E = C + 20

                    if A in range(D, E):
                        cv2.putText(img,
                                    f'car in the center',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                    elif (A < D):
                        dist = D - A
                        cv2.putText(img,
                                    f'car too far to the left, turn right by a distance: {dist}',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)
                    elif (A > E):
                        cv2.putText(img,
                                    f'voiture trop a droite, tournez gauche',
                                    (50, 300),
                                    font, 0.5,
                                    (0, 0, 255),
                                    2,
                                    cv2.LINE_4)


        cv2.imshow('drawDetectedMarkers', img)

        #press q to break the loop and close camera
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    # choix du produit à livrer
    choice = choice()
    #choice=20
    #asyncio.run(main())
    capture(choice)
