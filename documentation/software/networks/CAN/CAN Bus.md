# CAN Bus

## Overview
The CAN network provides communication between the various ECUs in the system. The code available is based on a set of pre-defined messages with their own identifier and payload.

![CAN Bus](./figures/hw_archi.jpg)


The CAN bus is configured with a **bitrate of 400 Kbit/s**.

## CAN Configuration for STM32

**Clock Tree:** APB1 frequency = 24 MHz

**CAN configuration with CubeMX:**

* Prescaler = 6 (for 4MhZ)
* Time quantum (tq): tq = 1 / (f_APB1/prescaler) =  250 ns
* Bit Segment 1 (BS1) = 7 tq
* Bit Segment 2 (BS2) = 2 tq
* Synchronization Jump Width (SJW) = 1 tq

baudrate = 1 / [tq * (SJW + BS1 + BS2) ]  = 400 kBits/s

## How to Use the PICAN 2
On the Raspberry Pi the CAN uses the shield **PICAN 2**. This shield is designed by **CopperhillTech**. The procedure to configure the PICAN 2 on a Raspbian is explained on the website of [CopperhillTech](https://copperhilltech.com/pican2-controller-area-network-can-interface-for-raspberry-pi/). Samples of C and python code are available on the web site as well as a set of programs to test the configuration. For example, the traffic on `can0` can be monitored with:

~~~~
./candump can0
~~~~

Main steps to config the Raspbian are :

* Edit the file `/boot/config.txt` by:

~~~~
sudo nano /boot/config.txt
~~~~

* Add these 3 lines to the end of file:

~~~~
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25
dtoverlay=spi-bcm2835-overlay
~~~~

* Reboot the Raspberry Pi:

~~~~
sudo reboot
~~~~

* Initialize the CAN interface by entering:

~~~~
sudo /sbin/ip link set can0 up type can bitrate 400000
~~~~



## Description of the CAN Messages

### Control Motor Commands (CMC)

* **From:** Raspeberry
* **To:** Nucleo
* **Lenght (Bytes):** 4
* **Data field:**

|Byte 0 |Byte 1 | Byte 2| Byte 3|
|:------|:------|:------|:------|
|PWMG_cons | PWMGD_cons | PWMAV_cons | POSAV_cons |

* **PWMG\_cons: Left motor command**
	* Bit 7: Enable bit.
		This bit is used to deactivate the left motor drivers in order to avoid power consumption and save batteries.
		* 0: motor disable
		* 1: motor enable	
	* Bits 6-0: command bits.
		This bit-field is used to control the speed of the left motor. The value 0 is the maximum speed backwards. The value 50 stops the motor. The value 100 is the maximum value forward.
		* value between 0 and 100.

		*Note:* To avoid power problem, the PWM that controls the motor is limited to 40%.

* **PWMD\_cons: Right motor command**
	* Bit 7: Enable bit.
		This bit is used to deactivate the right motor drivers in order to avoid power consumption and save batteries.
		* 0: motor disable
		* 1: motor enable
	* Bits 6-0: command bits.
		This bit-field is used to control the speed of the right motor. The value 0 is the maximum speed backwards. The value 50 stops the motor. The value 100 is the maximum value forward.
		* value between 0 and 100.

		_Note:_ To avoid power problem, the PWM that controls the motor is limited to 60%.

* **PWMAV\_cons: Steering wheel motor command**
	* Bit 7: Enable bit.
		This bit is used to deactivate the steering motor drivers in order to avoid power consumption and save batteries.
		* 0: motor disable
		* 1: motor enable
	* Bits 6-0: command bits.
		This bit-field is used to control the steering  motor. The value 0 turns the wheel to the left with the maximum speed. The value 50 stops the motor. The value 100 turns the wheel to the right with the maximum speed.
		* value between 0 and 100.

		_Note:_ To avoid power problem, the PWM that controls the motor is limited to 40%.

* **POSAV\_cons: Steering wheel motor command (in position)**
	* Bit 7: Enable bit.
		This bit is used to deactivate the steering motor drivers in order to avoid power consumption and save batteries.
		* 0: motor disable
		* 1: motor enable
	* Bits 6-0: command bits.
		This bit-field is used to control the steering motor. The value 0 corresponds to the wheels maximum angle to the left. The value 50 stops the motor. The value 100 corresponds to the wheels maximum angle to the right.
		* value between 0 and 100.

		_Note:_ To avoid power problem, the PWM that controls the motor is limited to 40%.

### Motor Sensors (MS)

* **From:** Nucleo
* **To:** Raspeberry
* **Lenght (Bytes):** 8
* **Data field:**

|Bytes 0-1 |Bytes 2-3| Bytes 4-5| Bytes 6-7 |
|:------|:------|:------|:------|
|Vol_mes | Bat_mes | VMG_mes | VMD_mes |

* **Vol\_mes: Steering Wheel Angle**
	* Bits 15-0: Raw data from the angle sensor on the steering wheel.
* **Bat\_mes: Battery Level**	
	* Bits 15-0: Raw data from the battery sensor. The value is between 0 and 0xFFF. The battery level U (V) can be computed by U = (4095 / Bat\_mes) * (3.3 / 0.2). The nominal operation of the battery has to be between 11 and 14 V. 
* **VMG\_mes: Left Motor Speed**	
	* Bits 15-0: The speed of the left rear motor in *0.01 rpm. The direction of rotation of the motor must be deduced from the command.
* **VMD\_mes: Right Motor Speed**	
	* Bits 15-0: The speed of the right rear motor in *0.01 rpm. The direction of rotation of the motor must be deduced from the command.

### Ultrasonic Sensors 1 (US1)

* **From:** Discovery
* **To:** Raspeberry
* **Lenght (Bytes):** 6
* **Data field:**

|Bytes 0-1 |Bytes 2-3| Bytes 4-5|
|:------|:------|:------|
|US_AVG | US_AVD | US_ARC|

* **US_AVG: Front Left Ultrasonic**
	* bits 15-0: distance in cm measured by the front left ultrasonic sensor.
* **US_AVD: Front Right Ultrasonic**
	* bits 15-0: distance in cm measured by the front right ultrasonic sensor.
* **US_ARC: Central Rear Ultrasonic**
	* bits 15-0: distance in cm measured by the central rear ultrasonic sensor.

### Ultrasonic Sensors 2 (US2)

* **From:** Discovery
* **To:** Raspeberry
* **Lenght (Bytes):** 6
* **Data field:**

|Bytes 0-1 |Bytes 2-3| Bytes 4-5|
|:------|:------|:------|
|US_ARG | US_ARD | US_AVC|

* **US_ARG: Left Rear Ultrasonic**
	* bits 15-0: distance in cm measured by the left rear ultrasonic sensor.
* **US_ARD: Right Rear Ultrasonic**
	* bits 15-0: distance in cm measured by the right rear ultrasonic sensor.
* **US_AVC: Central Front Ultrasonic**
	* bits 15-0: distance in cm measured by the central front ultrasonic sensor.

### Orientation Measures 1 (OM1)

![CAN Bus](./figures/orientation_car.jpg)

* **From:** Discovery
* **To:** Raspeberry
* **Lenght (Bytes):** 8
* **Data field:**

|Bytes 0-3 |Bytes 4-7|
|:------|:------|
|Yaw | Pitch |

* **Yaw: Yaw Angle**
	* bits 31-0: value in float of the yaw angle in degree.
* **Pitch: Pitch Angle**
	* bits 31-0: value in float of the pitch angle in degree.

### Orientation Measures 2 (OM2)
* **From:** Discovery
* **To:** Raspeberry
* **Lenght (Bytes):** 4
* **Data field:**

|Bytes 0-3 |
|:------|
|Roll |

* **Roll: Roll Angle**
	* bits 31-0: value in float of the roll angle in degree.

### Speed & Steering Commands (SSC)

* **From:** Raspeberry
* **To:** NucleoF103
* **Lenght (Bytes):** 2
* **Data field:**

* The SSC mode allows a differential between left and right wheels for more effective turns.

|Byte 0 |Byte 1 |
|:------|:------|
|SpeedMode | SteerMode |

* **SpeedMode: requested speed mode**
	* Bit 7-0: Command bits.
		This bit-field is used to control the speed of the car. The value must be between 0 and 100. 
		The available modes are: 
		* DISABLED 	: 0x00
		* STOP 		: 0x32 //Arret
		* REVERSE 	: 0x28 //Marche arriere
		* WALK 		: 0x3C //Premiere 
		* JOG 		: 0x41 //Seconde
		* RUN 		: 0x4B //Troisieme

		_Note:_ To avoid power problem, the motor's PWM is limited by software.

* **SteerMode: requested steering mode**
	* Bits 15-8: Command bits.
		This bit-field is used to control the steering of the car. The value must be between 0 and 100.The value 0 would be the maximum angle to the left. The value 50 would be going straight forward. The value 100 is the maximum angle to the right.
		The available modes are : 
		* DISABLED 	: 0x00
		* STRAIGHT 	: 0x32 //Roues droites
		* HARD_L	: 0x0A //Hard turn to the left
		* MODT_L	: 0x19 //Moderate turn to the left
		* SOFT_L	: 0x28 //Soft turn to the left
		* HARD_R	: 0x5A //Hard turn to the right
		* MODT_R	: 0x4B //Moderate turn to the right
		* SOFT_R	: 0x3C //soft turn to the right

		_Note:_ The maximum turning radius to the left and right are limited by mechanic.


### GPS Lat&Lon DD (GPS) 

* **From:** NucleoL476
* **To:** Raspberry Pi
* **Lenght (Bytes):** 8
* **Data field:**

* The Latitude and Longitude are transmitted in Decimal Degrees.

|Byte 0 |Byte 1 |Byte 2 |Byte 3 |Byte 4 |Byte 5 |Byte 6 |Byte 7 |
|:------|:------|:------|:------|:------|:------|:------|:------|
| Lat3 | Lat2 | Lat1 | Lat0 | Lon3 | Lon2 | Lon1 | Lon0 |

* **Latitude data**
		The Latitude data in DD (decimal degrees) is decomposed as follows: 
		<Lat3>.<Lat2><Lat1><Lat0>

	* Bit 7-0: Lat3.
		This bit-field corresponds to the integer part of the latitude. This value is usually 43 for our use. 
		
	* Bit 15-8: Lat2.
		This bit-field corresponds to the first and second decimal places of the latitude. 

	* Bit 23-16: Lat1.
		This bit-field corresponds to the third and fourth two decimal places of the latitude. 

	* Bit 31-24: Lat0.
		This bit-field corresponds to the fifth and sixth decimal places of the latitude. 

		_Note:_ The Raspberry must recompose the data as a latitude in decimal degrees.

* **Longitude data**
		The Longitude data in DD (decimal degrees) is decomposed as follows: 
		<Lon3>.<Lon2><Lon1><Lon0>

	* Bit 7-0: Lon3.
		This bit-field corresponds to the integer part of the longitude. This value is usually 1 for our use. 
		
	* Bit 15-8: Lon2.
		This bit-field corresponds to the first and second decimal places of the longitude. 

	* Bit 23-16: Lon1.
		This bit-field corresponds to the third and fourth two decimal places of the longitude. 

	* Bit 31-24: Lon0.
		This bit-field corresponds to the fifth and sixth decimal places of the longitude. 

		_Note:_ The Raspberry must recompose the data as a longitude in decimal degrees.

##IMU Measures 

* **From:** NucleoL476
* **To:** Raspberry Pi
* **Lenght (Bytes):** 8
* **Data field:**

* The Acceleration is transmitted in mg and Yaw is transmitted in mdps.

* IMPORTANT: ALL DATAS IN THIS CAN MESSAGE ARE SIGNED INT.

|Byte 0 |Byte 1 |Byte 2 |Byte 3 |Byte 4 |Byte 5 |Byte 6 |Byte 7 |
|:------|:------|:------|:------|:------|:------|:------|:------|
| AccX  | AccY  |   -   |   -   | Yaw1  | Yaw0  |   -   |   -   |

* **Acceleration data**
		The Acceleration data in mg is decomposed as follows: 
		<Acc_X><Acc_Y>

	* Acc_X.
		This bit-field corresponds to the acceleration on the x axis. It is a signed integer on 8 bits. (Lateral axis) 
		
	* Acc_Y.
		This bit-field corresponds to the acceleration on the y axis. It is a signed integer on 8 bits. (Longitudinal axis = forward/backward axis of the car) 

* **Yaw data**
		The yaw data in mdps is a signed integer decomposed as follows: 
		<Yaw1><Yaw0>

	* Bit 7-0: Yaw1.
		This bit-field corresponds to the 8 most significant bits of the integer part of the Yaw value.  
		
	* Bit 15-8: Yaw0.
		This bit-field corresponds to the 8 least significant bits of the integer part of the Yaw value.
 

## IDs of the CAN Messages

|Name                        |Class ID |SubClass ID|Priority |ID    |
|----------------------------|:-------:|:---------:|:-------:|:----:|
|                            |3bits    |4bits      |4bits    |11bits|
|Control Motor Commands (CMC)|0x0      |0x1        |0x0      |0x010 |
|Motor Sensors (MS)          |0x1      |0x0        |0x0      |0x100 |
|Ultrasonic Sensors 1 (US1)  |0x0      |0x0        |0x0      |0x000 |
|Ultrasonic Sensors 2 (US2)  |0x0      |0x0        |0x1      |0x001 |
|Orientation Measures 1 (OM1)|0x1      |0x0        |0x1      |0x101 |
|Orientation Measures 2 (OM2)|0x1      |0x0        |0x2      |0x102 |
|Speed&Steering Command (SSC)|0x0      |0x2        |0x0      |0x020 |
|GPS Lat&Lon DD (GPS)        |0x2      |0x0        |0x0      |0x200 |
|Acceleration and Yaw (IMU1) |0x2      |0x1        |0x0      |0x200 |