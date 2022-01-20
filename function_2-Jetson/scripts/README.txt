- jetson.py main camera script of the jetson

Opens a server socket.
Opens the camera and calculates difference between gate's center and camera's frame center.
Sends that data to the client socket : the raspberry pi.

WARNING : The server socket must be launched first thus it's the first script to launch.