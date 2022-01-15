from flask import Flask, render_template
import folium
import os
from folium import IFrame
import base64
import json
import time
from IPython.core.display import display, HTML

alist0=[43.57076, 1.46604] #Actual coordiantes of GEI at INSA.

app = Flask(__name__)

def folium_deepnote_show(m):
    data = m.get_root().render()
    data_fixed_height = data.replace('width: 100%;height: 100%', 'width: 100%').replace('height: 100.0%;', 'height: 609px;', 1)
    display(HTML(data_fixed_height))

@app.route('/')
def home():
    aliste=[]
    with open("fire_coord.txt", "r") as data_file: #Opening of the file containing coordinates of the fire detected
        while 1:
           where = data_file.tell() #Get the current position of the cursor
           line = data_file.readline() #Read the current line (next line)
           where = data_file.tell()
           if not line:
               time.sleep(1)
               data_file.seek(0,2) #Go to to the end of the file     
           else:
               aliste = json.loads(line) #Convert a string format list into a real list
               print(aliste)
               if aliste != alist0: #If a fire is detected.
                   map = folium.Map(
                        location = aliste,
                        zoom_start = 12
                   )                    #Create the base of the map
                   # Filename ='images/fire.jpeg'
                   # encoded = base64.b64encode(open(Filename, 'rb').read())
                   # html='<img src="data:image/jpeg;base64,{}">'.format
                   # resolution, width, height = 75, 50, 5
                   # iframe = IFrame(html(encoded.decode('UTF-8')), width=(width*resolution) + 20, height=(height*resolution) + 20)
                   # popup = folium.Popup(iframe, max_width= 500)
                   
                   #The previous lines allow the possibility to put an image as a popup.

                   folium.Marker(
                   location = aliste,
                   zoom_start = 12,
                   #popup=popup,
                   tooltip="Fire Alert",
                   icon=folium.Icon(color="red", icon="fire")
                   ).add_to(map) #Put an marker in the current position.
                   print(aliste)
               else: #In no fire detected
                   map = folium.Map(
                        location = aliste,
                        zoom_start = 15
                   )
                   folium.Marker(
                   location = aliste,
                   zoom_start = 15,
                   popup="<b>Welcom to Zilly localization. No fire detected</b>",
                   tooltip="No fire detected",
                   icon=folium.Icon(color="green", icon="leaf")
                   ).add_to(map)
                   print(aliste)
               return render_template("index_map.html", map=map._repr_html_()) #Create an internal HTML file which is automatically show in output.
                  

if __name__ == "__main__":
	app.run(host="10.105.1.86", port=8001, debug=True)
