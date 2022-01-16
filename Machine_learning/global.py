from os import name
from parser_gps import Path_Init,Gps_Read
from Routine import Img_Treatment
import cv2
from Web_site.flask_app.flask_app.parser_gps import Path_Init
from receiver import Can_read
import can
import time

if __name__ == "__main__":
    #Variable poitant sur un bus can
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    #initialisation de la camera
    cap = cv2.VideoCapture(0)
    #Variable de contrôle d'avancement dans le chemin et de présence de feu
    Curr_point=0
    Is_fire = False
    # Envoi du chemin par can
    Path_Init()
    #Reception d'une premiere trame de reponse
    ID,DW=Can_Read(bus)

    #Boucle jusqu'à fin du trajet ou presence de feu
    while (Curr_point <5 & Is_fire != True):

        #Boucle d'attente de trame d'arrivee au point
        while (ID != 256 & DW != 1) :
            ID,DW=Can_Read()
        
        time.sleep(60)
        """ #Routine machine learning
        Predictions=Img_Treatment()

        #Presence d'un feu sur plusieures analyses
        if (Predictions.count('fire') > 2):
            Is_fire=True         #Changement de variable pour sortir de la boucle   
            Fire_pos=Gps_read()    #Lecture de la position actuelle de la voiture
            can.message("stop")    #Envoi du message d'arret à la voiture
        else:
            can.message("no fire")  #Envoi de la trame pour reprendre le trajet
        Curr_point+=1 """