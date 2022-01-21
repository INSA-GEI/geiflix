from flask import Flask, render_template
import folium
import os
from folium import IFrame
import base64
import json
import time
from IPython.core.display import display, HTML
from multiprocessing import Process, Pipe
from io import BytesIO
from folium.features import CustomIcon

alist0=[43.57076, 1.46604] #Actual coordiantes of GEI at INSA.
path = [] #List for the coordinates of the predefined path.

app = Flask(__name__) #Name of the application.

#This function solves a few problems of the interactive map of Folium module.
def folium_deepnote_show(m):
    data = m.get_root().render()
    data_fixed_height = data.replace('width: 100%;height: 100%', 'width: 100%').replace('height: 100.0%;', 'height: 609px;', 1)
    display(HTML(data_fixed_height))

@app.route('/')
def home():
    aliste=[] #List of fire coordinates.
    path_point = 0 #Counter for the number of lines on the considered file.
    value = 0 #Variable to store a list of coordinates.
    with open("path_coord.txt", "r") as data_file: #Opening of the file containing coordinates of the predefined path.
        #Verification that the file contains at least 5 lines.
        while 1:
            num_lines = sum(1 for line in data_file)
            if num_lines >= 5:
                break
        data_file.close()
        
        #Read the 5 coordinates in the current file and store it in a list.
        while len(path) < 5  and path_point < 5:
            file = open("path_coord.txt", "r")
            line = file.readline()
            while line:
                value = json.loads(line) #Convert a list from a file in real list (Here int list).
                path.append(value)
                path_point += 1
                line = file.readline()
            file.close()
            
    with open("fire_coord.txt", "r") as data_file: #Opening of the file containing coordinates of the fire detected.
        while 1: 
           where = data_file.tell() #Get the current position of the cursor.
           line = data_file.readline() #Read the current line (next line).
           where = data_file.tell()
           if not line:
               time.sleep(1)
               data_file.seek(0,2) #Go to to the end of the file.
               map = folium.Map(
                        location = path[4],
                        zoom_start = 15
                   )
               #The next lines allows us to dislay each localization with appropriate coordinates.
               #The coordinates are written in the inversal order in the current file. 
               #So we read the first point at the end of the list.
               folium.Marker(
               location = path[4],
               popup="<b>The first point is A</b>",
               tooltip="A",
               icon=folium.Icon(color="purple", icon="leaf")
               ).add_to(map) #Put a marker in the current position.
               folium.Marker(
               location = path[3],
               popup="<b>The second point is B</b>",
               tooltip="B",
               icon=folium.Icon(color="blue", icon="leaf")
               ).add_to(map)
               folium.Marker(
               location = path[2],
               popup="<b>The third point is C</b>",
               tooltip="C",
               icon=folium.Icon(color="green", icon="leaf")
               ).add_to(map)
               folium.Marker(
               location = path[1],
               popup="<b>The fourth point is D</b>",
               tooltip="D",
               icon=folium.Icon(color="orange", icon="leaf")
               ).add_to(map)
               folium.Marker(
               location = path[0],
               popup="<b>The last point is E</b>",
               tooltip="E",
               icon=folium.Icon(color="beige", icon="leaf")
               ).add_to(map)
               return render_template("index.html", map=map._repr_html_())
           else:
               aliste = json.loads(line) #Convert a string format list into a real list.
               
               map = folium.Map(
                    location = path[4],
                    zoom_start = 12
               )                    #Create the base of the map.
               Filename ='images/Feu.png'
               encoded = base64.b64encode(open(Filename, 'rb').read())
               html='<img src="data:image/jpeg;base64,{}">'.format
               resolution, width, height = 75, 50, 5
               iframe = IFrame(html(encoded.decode('UTF-8')), width=(width*resolution) + 20, height=(height*resolution) + 20)
               popup = folium.Popup(iframe, max_width= 50)
               #The previous lines allow the possibility to put an image as a popup.
               
               #The next lines allows us to dislay each localization with appropriate coordinates again + the fire localization.
               #The coordinates are written in the inversal order in the current file. 
               #So we read the first point at the end of the list.
               folium.Marker(
               location = path[4],
               popup="<b>The first point is A</b>",
               tooltip="A",
               icon=folium.Icon(color="purple", icon="leaf")
               ).add_to(map)
               folium.Marker(
               location = path[3],
               popup="<b>The second point is B</b>",
               tooltip="B",
               icon=folium.Icon(color="blue", icon="leaf")
               ).add_to(map)
               folium.Marker(
               location = path[2],
               popup="<b>The third point is C</b>",
               tooltip="C",
               icon=folium.Icon(color="green", icon="leaf")
               ).add_to(map)
               folium.Marker(
               location = path[1],
               popup="<b>The fourth point is D</b>",
               tooltip="D",
               icon=folium.Icon(color="orange", icon="leaf")
               ).add_to(map)
               folium.Marker(
               location = path[0],
               popup="<b>The last point is E</b>",
               tooltip="E",
               icon=folium.Icon(color="beige", icon="leaf")
               ).add_to(map)
               
               #Adding the fire location.
               folium.Marker(
               location = aliste,
               popup=popup,
               tooltip="Fire Alert",
               icon=folium.Icon(color="red", icon="fire")
               ).add_to(map) #Put a marker in the current position.
               folium.Circle(aliste,
                    radius=10 #Add a radius of 10 meters displaying on the map.
                   ).add_to(map)
               return render_template("index.html", map=map._repr_html_()) #Create an internal HTML file which is automatically show in output.
                  

if __name__ == "__main__":
    app.run(debug=True) #Call the current application.

