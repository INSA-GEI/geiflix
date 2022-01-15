from Fire_Dset import FireSet
from Fire_NN import Fire_Net

import matplotlib.pyplot as plt # for plotting
import numpy as np # for transformation

import torch # PyTorch package
import torch.nn as nn # basic building block for neural neteorks
import cv2
import os
import time

from Jetson_Cam import Get_data
from Jetson_Cam import transform

#Start camera
cap = cv2.VideoCapture(0)

#path to the pretrained nn model
Model_Path = './cifar_net_V3.pth'

# set batch_size
batch_size = 62

# set number of workers
num_workers = 2

#Delay variables to take photos during routine at GPS point
Rot_time=10
Img_Per_Rot=2
Curr_Image=0
Predictions=[]

def Img_Treatment(cam,Rot_time=10,Img_Per_Rot=2,Model_Path = './cifar_net_V3.pth',S_dir="/home/corentin/Desktop/TSFlow",Disp=False) :
    delay=0
    Curr_Img=0
    Predictions=[]
    while Curr_Img < Img_Per_Rot:
        Turn_Start=time.time()

        if delay >= Rot_time/Img_Per_Rot:
            
            #Tuple containing classes name 
            classes = ('Fire', 'No_Fire')
            
            #Capture one image with cam and save it
            Get_data(cam,Display=Disp,index=Curr_Img)
            os.chdir(S_dir)

            #Create dataset and dataloader to feed image taken to the neural network
            testset=FireSet("ImageSet/",transform=transform)
            testloader=torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=True, num_workers=num_workers)

            # create a net object and load pretrained nn
            net=Fire_Net()
            net.load_state_dict(torch.load(Model_Path))

            # get random training images with iter function
            dataiter = iter(testloader)
            images, labels = dataiter.next()

            # run through net to make predictions
            outputs = net(images)

            _, predicted = torch.max(outputs, 1)
            
            Predictions.append(classes[predicted])
            Curr_Img+=1
            delay=0

    return Predictions















if __name__ == "__main__":
    pass
"""     
    delay=0
    while Curr_Image < Img_Per_Rot:
        Turn_Start=time.time()

        if delay >= Rot_time/Img_Per_Rot:

            q=time.time()

            Get_data(cap,Display=False,index=Curr_Image)
            os.chdir("/home/corentin/Desktop/TSFlow")
            print("Photo prise en : ", time.time()-q)


            testset=FireSet("ImageSet/",transform=transform)
            testloader=torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
            # create classes tuple to display answers
            classes = ('Fire', 'No_Fire')
            print("Dataset cree en : ",time.time()-q)
            # create a net object and load pretrained nn
            net=Fire_Net()
            net.load_state_dict(torch.load(Model_Path))


            # get random training images with iter function
            dataiter = iter(testloader)
            images, labels = dataiter.next()

            # run through net to make predictions
            outputs = net(images)

            #Collect net's answers and dislay them
            
            _, predicted = torch.max(outputs, 1)
            print(predicted)
            Predictions.append(classes[predicted])
            Curr_Image+=1
            delay=0
            print("Traitement de l'image en : ", time.time()-q)
        Turn_End=time.time()
        delay+=(time.time()-Turn_Start)

    print(Predictions) """