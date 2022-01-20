# CarGate Project

CarGate is an autonomous vehicle intended to help you in transporting goods throughout your warehouse.
The car has been designed and created by the Yankee Doodle Pigeon Group. The name of our company was inspired by the cartoon Dastardly & Muttley in Their Flying Machines, our team took the name of the patriotic American homing pigeon (Yankee Doodle Pigeon). Our team is composed of:
- BURTON Nidishlall (burton@insa-toulouse.fr)
- CHOUIYA Asma  (chouiya@insa-toulouse.fr)
- EL HACHIMI Asmae  (elhachim@insa-toulouse.fr)
- MARTY Axel  (axmarty@insa-toulouse.fr)
- PIQUES Nicolas  (npiques@insa-toulouse.fr)
- RAMIARA Maxime (ramiara@insa-toulouse.fr)

The projects are (or were) surpervised by:
- Pierre-Emmanuel Hladik (pehladik@insa-toulouse.fr)
- Gwendoline Le Corre (lecorre@insa-toulouse.fr)

# Features 
- Gate Detection System
Using a QR-Code Detection Algorithm, the car is able to differentiate between gates. The gate is represented by a pair of QR-Codes. If the pair detected matches the instruction given previously, the program will only focus on that pair.

- Trajectory Calculation
This system was the creation of a merger between the QR-Code Detection Algorithm and a Tracking Algorithm using a Lidar. By using the coordinates created when the right QR-Code is detected, the car is able to direct itself in order to centre itself as close as possible to the middle of the gate. 
In order to stop the car after having successfully crossed the gate, the tracking algorithm will then come into action in order to track the posts of the gate while passing through them. 

- Anti-Blocking System
In any case of emergency, a graphical unit interface (GUI) has been built to override the autonomous control. By the use of this interface, the car can be remotely controlled. An emergency stop button has also been built-in the interface to stop the car when it has been set back on track by a supervisor. 
This GUI is also used to instruct the car about which aisle it should be looking for.


# Requirements
- Linux
- Any C++ compiler
- Python3 (OpenCv)
- Ros 1
- MQTT
- Ethernet
- CAN bus






