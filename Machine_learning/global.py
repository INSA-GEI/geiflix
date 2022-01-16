from os import name
from Parser import can_iti,Gps_read
from Routine import Img_Treatment
import cv2
from receiver import Can_read
import can

if __name__ == "__main__":
    #initialisation de la camera
    cap = cv2.VideoCapture(0)
    #Variable de contrôle d'avancement dans le chemin et de présence de feu
    Curr_point=0
    Is_fire = False
    # Envoi du chemin par can
    can_iti()
    #Reception d'une premiere trame de reponse
    ID,DW1,DW2=Can_read()

    #Boucle jusqu'à fin du trajet ou presence de feu
    while (Curr_point <5 & Is_fire != True):

        #Boucle d'attente de trame d'arrivee au point
        while (ID != 0x100 & DW1 != 128) :
            ID,DW1,DW2=Can_read()
        #Routine machine learning
        Predictions=Img_Treatment()

        #Presence d'un feu sur plusieures analyses
        if (Predictions.count('fire') > 2):
            Is_fire=True         #Changement de variable pour sortir de la boucle   
            Fire_pos=Gps_read()    #Lecture de la position actuelle de la voiture
            can.message("stop")    #Envoi du message d'arret à la voiture
        else:
            can.message("no fire")  #Envoi de la trame pour reprendre le trajet
        Curr_point+=1

    pass