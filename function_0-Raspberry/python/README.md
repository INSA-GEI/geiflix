# Python architecture

The Python software is launched with `sudo python main.py`.

This program uses the `klunk` packages, dividing the software into multiple modules. It also uses the `xboxdrv` module for the Xbox Controller, the `SocketCAN` module for CAN communication, as well as several native Python modules.

# Ultrasounds

Ultrasounds are handled in the `klunk.ultrasound` module, which contains a thread used to listen to the CAN bus for ultrasounds informations, and stores the last sensors values. The CAN bus is instantiated in the `klunk.car.Car` class in our case.

Each of the six ultrasounds sensors have a corresponding class attribute.

# Lidar

The Jetson Nano handles the lidar, filters its data and extracts obstacle information. It then sends this information using a UDP socket, over the WiFi hospot generated from the Raspberry Pi.

The `klunk.lidar` module contains a thread that creates a UDP server socket, listens to messages, parses the messages to extract the obstacle information, and stores it.

The `klunk.lidar.Lidar` class contrains a list of obstacles, represented by its angle in degrees, distance in cm (both relative to the center of the car) and size in cm.

# `klunk.motors`

This module mostly categorizes the available speed and steer values, and their corresponding CAN values. It also contains some helper functions about theses values.

# Zones

The `klunk.zone` module contains an abstraction of a zone. A zone has two states, occupied or not. As soon as an obstacle is detected in the zone, it becomes occupied. However, there must be no obstacle in the zone for some amount of time for this zone to be considered unoccupied.

The `klunk.zone.Zone` class must be instanciated with a predicate. This predicate defines the requirement for a obstacle to be detected in that zone.

The `klunk.zone` module thus contains every zone predicates.

![zones](https://user-images.githubusercontent.com/34137127/149972813-1d52d532-bf90-49a1-921c-5be0a3edd24b.png)

# Car

The `klunk.car` module contains a `Car` class that abstracts the GEIflix car. It contains the abstractions of the sensors, as well as the current speed, steer, and mode of the car. As soon as the speed and steer of that class are modified, a CAN message is sent to the corresponding motors. Similarly, the mode is synchronised with a text file located in the web server part. The web interfaces polls that text file periodically in order to display the current mode.

# Decision making and avoidance

The decision making part of the software is contained in the `klunk.scheduler` module. Honestly the code is not pretty. It is directed translation of the abstract decision making (if this zone and/or that zone is occupied, then slow/stop the car, or prevent steering, or start avoiding).

The avoidance part is composed of each of the 5 steps, as well as the 6 steering in between. The following structure is repeated :
```
if self.state = given_avoidance_step:
  if dangerous_zones_occupied:
    stop_the_car()
  elif next_step_condition:
    start_the_next_step()
  else:
    do_actions_for_current_step()
```
