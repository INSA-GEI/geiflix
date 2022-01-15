from flask import Flask, render_template
import folium
import os
from folium import IFrame
import base64
import json
import time
from IPython.core.display import display, HTML
from multiprocessing import Process, Pipe

alist0=[43.57076, 1.46604] #Actual coordiantes of GEI at INSA.
path = []

# 'red',
#     'blue',
#     'gray',
#     'darkred',
#     'lightred',
#     'orange',
#     'beige',
#     'green',
#     'darkgreen',
#     'lightgreen',
#     'darkblue',
#     'lightblue',
#     'purple',
#     'darkpurple',
#     'pink',
#     'cadetblue',
#     'lightgray',
#     'black

app = Flask(__name__)

def folium_deepnote_show(m):
    data = m.get_root().render()
    data_fixed_height = data.replace('width: 100%;height: 100%', 'width: 100%').replace('height: 100.0%;', 'height: 609px;', 1)
    display(HTML(data_fixed_height))

@app.route('/')
def home():
    aliste=[]
    path_point = 0
    value = 0
    with open("path_coord.txt", "r") as data_file: #Opening of the file containing coordinates of the fire detected
        
        while 1:
            num_lines = sum(1 for line in data_file)
            if num_lines >= 5:
                break
        data_file.close()
            
        while len(path) < 4  and path_point < 5:
            # Ouvrir le fichier en lecture seule
            file = open("path_coord.txt", "r")
            # utilisez readline() pour lire la première ligne
            line = file.readline()
            while line:
                print(line)
                value = json.loads(line)
                path.append(value)
                path_point += 1
                # utilisez readline() pour lire la ligne suivante
                line = file.readline()
            file.close()
            #Montrer le chemin sur la map     
    with open("fire_coord.txt", "r") as data_file: #Opening of the file containing coordinates of the fire detected
        while 1: 
           where = data_file.tell() #Get the current position of the cursor
           line = data_file.readline() #Read the current line (next line)
           where = data_file.tell()
           if not line:
               time.sleep(1)
               data_file.seek(0,2) #Go to to the end of the file
               map = folium.Map(
                        location = path[4],
                        zoom_start = 15
                   )
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
               return render_template("index.html", map=map._repr_html_())
           else:
               aliste = json.loads(line) #Convert a string format list into a real list
               print(aliste)
               #if aliste != alist0: #If a fire is detected.
               map = folium.Map(
                    location = path[4],
                    zoom_start = 12
               )                    #Create the base of the map
               Filename ='images/Feu.png'
               encoded = base64.b64encode(open(Filename, 'rb').read())
               html='<img src="data:image/jpeg;base64,{}">'.format
               resolution, width, height = 75, 50, 5
               iframe = IFrame(html(encoded.decode('UTF-8')), width=(width*resolution) + 20, height=(height*resolution) + 20)
               popup = folium.Popup(iframe, max_width= 50)
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
               
               #The previous lines allow the possibility to put an image as a popup.
               
               folium.Marker(
               location = aliste,
               popup=popup,
               tooltip="Fire Alert",
               icon=folium.Icon(color="red", icon="fire")
               ).add_to(map) #Put an marker in the current position.
               folium.Circle(aliste,
                    radius=10
                   ).add_to(map)
               print(aliste)
#                else: #In no fire detected
#                    map = folium.Map(
#                         location = aliste,
#                         zoom_start = 15
#                    )
#                    folium.Marker(
#                    location = aliste,
#                    zoom_start = 15,
#                    popup="<b>Welcom to Zilly localization. No fire detected</b>",
#                    tooltip="No fire detected",
#                    icon=folium.Icon(color="green", icon="leaf")
#                    ).add_to(map)
#                    print(aliste)
               return render_template("index.html", map=map._repr_html_()) #Create an internal HTML file which is automatically show in output.
                  

if __name__ == "__main__":
    app.run(debug=True)

