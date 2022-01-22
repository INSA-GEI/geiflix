# forestfirefighter.github.io
## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)

## General info

**I. Purpose of the project**

A fire outbreak is unpredictable and may happen in remote forest, thus not easily accessible. As firefighters can’t be everywhere all the time, autonomous ways to detect forest fires may reduce intervention time and damages. Here is our solution : The Forest Fire Fighter or F3 for short. An autonomous car that follows a predefined path given by firefighters and alerts them if it recognizes a fire outbreak. If a danger is identified, rescuers and nearby civilians will be alerted and informed of its location through this website.

**II. The Website for our project: Fire Forest Fighter**

To get a good visualization of the future trajectory of the car, we developed a website: **https://ctatger.github.io/forestfirefighter.github.io/**. In this one, we    have some tabs. Bellow the explanations for the different tabs:

- Home: The description of the project and the main purpose.
- Live alerts: An interactive map displaying the predefined path + fire location if applicable.
- Car control: Allow us, after an identification with a usurname and password, to send the predefined path.
- Team: Show the different team members that worked on this project.
- Demonstration: Here there are a few demonstrations from our project with description.
- About: Direct you to our Git repository.

Two tabs concern directly the localization of the path and fire if applicable: **Car control** and **Live alerts**.
First, **Car control** allow us to enter coordinates (You should put 5 coordinates). Then, the coordinates are sended, thanks to PHP code, troughout the network  which the raspberrry Pi is connected to it. Actually, we used a computer connected with SSH protocol to the Rapsberry Pi to send these coordinates. So, the Raspberry Pi received the coordinates printed in a file. A server for the intercative map, appearing in **Live alerts** tab, was developed with the framework Flask using Python language and Folium module.

## Technologies

* We worked with Raspberry Pi OS Lite on a Raspberry Pi 3 (link for OS: https://www.raspberrypi.com/software/operating-systems/).
* We used a GPS during the project, it is the C94-M8P u-blox RTK module. It is composed by a rover module installed into the car and a base module installed in a fixed position.
* We used pip3 for installing packages for Python. Bellow the command to install pip3:

````
$ sudo apt-get install python3-pip
````
* For the connection to PHP and Flask servers, we connect the Raspberry Pi to the same private network than the computer(s) used as clients. We used the SSH communication protocol to connect immidiately to the appropriate IP address and port. For instance, one solution for using two servers at the same time was the folowing: In our project our two servers were open on the same IP address (of the Raspberry Pi) but with a different port number. And in the concerned HTML files, we redirected the page of the concerned tab to the port number chosen of one of the server.

For the development of the website different IT languages were used: HTML, CSS, PHP mainly for the design and Python for the interactive map with Flask and Folium.

Project is created with:
* Python version: 3.7.x
* Flask version: 1.1.1
* Folium version: 0.12.1
	
## Setup
Files of Data:
* cutecom.log: File containing in real time unsorted raw GPS data.
* path_coord.txt: File containing the coordinates points of the predefined path (In the current code it need 5 points).
* degrees_coord.txt: File containing in real time the GPS data in Decimal Degrees format **(There is only one line changed each time)**.
* fire_coord.txt: File containing fire coordinates if applicable in Decimal Degrees format **(There is only one line changed each time)**.

First, you should be sure that the 4 previous files are empty.

Run the folowing command on Linux OS to be sure that each file is really empty:

````
$ > name_file.xx
````
To run this project, install it locally:

A virtual environment for Flask (not mandatory)

````
$ mkdir myproject
$ cd myproject
$ python3 -m venv venv
````
Activate this environment:

````
$ source venv/bin/activate
````
Install Flask and Folium:

```
$ pip install flask
$ pip install folium
````

**You need a GPS module connected to the Rasperry Pi.** 

To verify if the GPS is connected to your Raspberry Pi, launsh the folowwing command and find the reference of your GPS:

```
$ lsusb
```

To launch the writing of the GPS data on a file in real time, you need the folowing command (Don't forget to change the USB module (Here **ttyACM0**) and the path of the file if needed):

```
$ lxterminal -e "cat /dev/ttyACM0 > cutecom.log"
```

To launch the first server corresponding to the Website as such we need the following command:

```
$ php -S ip_address:port
```

Bellow the command to launch the second server Flask for displaying the interactive map (After activating the virtual environment or not. It depends your configuration).

```
$ python3 map_for_path.py
```

**Now enjoy by enter ip_adress:port/index.html in a browser to see the website!!!**

You need to log in in order to enter in Control car tab, the 5 localization and after you can see the predefined path on the map. You can see also a red icon if a fire is detected. You can test by yourself directly by enttering a localization in the fire_coord.txt.

**Connect to the ip_adress:port corresponding to the Flask server to see the interactive map an enjoy yourself :D .**

![image](https://user-images.githubusercontent.com/58248934/150618080-8f934941-b446-4047-9f1b-2ccdb23322ba.png)

After all that, you can run CAN_Comm/parser_gps.py file to send CAN frames with the 5 entered points ans send in real time GPS coordinates via CAN frames too.

More properly, youn should launch global.py (It is the main program connecting all files). In this program, you should call the appropriate method to use it directly.

For a good simulation of all this you need to launch map_for_path.py, paths_gps.py and global.py (Localized in Machine_learning folder) in parallel. For instance, you can read the current Makefile.
