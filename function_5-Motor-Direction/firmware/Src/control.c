/*
 * control.c
 *
 *  Created on: 12 nov. 2021
 *      Author: Carole Meyer, Amélie MAIER, Ruiqi HU
 *
 */

/* Includes ------------------------------------------------------------------*/


#include "control.h"

#include "steering.h"
#include "wheels.h"
#include "GPS.h"

#include "gpio.h"


/* Private define ------------------------------------------------------------*/

#define RUN_SPEED 	0.527			// speed in meter/s when speed set at RUN --> init = 0.527
#define JOG_SPEED 	0.17 			// speed in meter/s when speed set at JOG --> init = 0.17
#define RIGHT_ANGLE	8.306741531		// angle in degree traveled in 1 second when angle set at HARD_R
#define LEFT_ANGLE	-8.366477998	// angle in degree traveled in 1 second when angle set a HARD_L


#define DISABLED 	0

// Definition of SPEED MODES
#define STOP 		50
#define REVERSE 	40
#define WALK 		58
#define JOG 		60
#define RUN 		75

// Definition of STEERING MODES
#define STRAIGHT 	50
#define HARD_L 		10
#define MODT_L 		25
#define SOFT_L 		40
#define HARD_R 		90
#define MODT_R 		75
#define SOFT_R 		60

// Definition of differential percentage for back motors
#define DIFF_NONE 	0
#define DIFF_SMALL 	5
#define DIFF_MEDIUM 10
#define DIFF_LARGE 	15

// Definition of azimuth types
#define AZIMUT_FORWARD 	0
#define AZIMUT_LEFT		1
#define AZIMUT_RIGHT	2

// extern variables
extern double dist;
extern double carLatitude;
extern double carLongitude;
extern double angleCar;
extern int pos_OK;
extern int isFire;
int CHANGE_TO_STOP=0;

/* Private variables ---------------------------------------------------------*/

/* Programs ------------------------------------------------------------------*/



/* brief	Control speed and steering commands according to the modeSpeed and modeSteer received by CAN frame SSC 0x020
 * param	int requested_speed		modeSpeed requested between [0;100]
 * 			int requestion_steer	modeSteer requested between [0;100]
 * retval 	None
 * */
void car_control(int requested_speed, int requested_steer){
	int diff = DIFF_NONE;
	int azimut = AZIMUT_FORWARD;

	// limit the speed command received by the CAN frame between [0; 100] to the max speed
	if (requested_speed > 75){requested_speed = 75;}


	// classify the speed command
	if (requested_speed == DISABLED) {requested_speed = DISABLED;}
	else if (requested_speed <= REVERSE) {requested_speed = REVERSE;}
	else if (requested_speed < WALK) {requested_speed = STOP;}
	else if (requested_speed < JOG) {requested_speed = WALK;}
	else if (requested_speed < RUN) {requested_speed = JOG;}
	else {requested_speed = RUN;}

	// limit the steer command received by the CAN frame between [0; 100] to the max steer
	if (requested_steer > 100){requested_steer = 100;}

	// classify the steer command
	if (requested_steer == DISABLED) {requested_steer = DISABLED;}
	else if (requested_steer <= HARD_L) {requested_steer = HARD_L;}
	else if (requested_steer <= MODT_L) {requested_steer = MODT_L;}
	else if (requested_steer <= SOFT_L) {requested_steer = SOFT_L;}
	else if (requested_steer < SOFT_R) {requested_steer = STRAIGHT;}
	else if (requested_steer < MODT_R) {requested_steer = SOFT_R;}
	else if (requested_steer < HARD_R) {requested_steer = MODT_R;}
	else {requested_steer = HARD_R;}

	// send steering command to the front motor
	switch(requested_steer) {
		case STRAIGHT:
			diff = DIFF_NONE;
			azimut = AZIMUT_FORWARD;
			steering_set_position(GPIO_PIN_SET, STRAIGHT);
			break;
		case HARD_L:
			diff = DIFF_LARGE;
			azimut = AZIMUT_LEFT;
			steering_set_position(GPIO_PIN_SET, HARD_L);
			break;
		case MODT_L:
			diff = DIFF_MEDIUM;
			azimut = AZIMUT_LEFT;
			steering_set_position(GPIO_PIN_SET, MODT_L);
			break;
		case SOFT_L:
			diff = DIFF_SMALL;
			azimut = AZIMUT_LEFT;
			steering_set_position(GPIO_PIN_SET, SOFT_L);
			break;
		case HARD_R:
			diff = DIFF_LARGE;
			azimut = AZIMUT_RIGHT;
			steering_set_position(GPIO_PIN_SET, HARD_R);
			break;
		case MODT_R:
			diff = DIFF_MEDIUM;
			azimut = AZIMUT_RIGHT;
			steering_set_position(GPIO_PIN_SET, MODT_R);
			break;
		case SOFT_R:
			diff = DIFF_SMALL;
			azimut = AZIMUT_RIGHT;
			steering_set_position(GPIO_PIN_SET, SOFT_R);
			break;
		default:
			diff = DIFF_NONE;
			azimut = AZIMUT_FORWARD;
			steering_set_position(GPIO_PIN_RESET, STRAIGHT);
			break;
		}



	// send speed command to back motors
	switch(requested_speed) {
		case STOP:
			wheels_set_speed(GPIO_PIN_RESET, GPIO_PIN_RESET, STOP, STOP);
			break;
		case REVERSE:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (requested_speed*(100-diff))/100, requested_speed);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, requested_speed, (requested_speed*diff)/100);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, requested_speed, requested_speed);}
			break;
		case WALK:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, requested_speed, (requested_speed*(100+diff))/100);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (requested_speed*(100+diff))/100, requested_speed);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, requested_speed, requested_speed);}
			break;
		case JOG:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (requested_speed*(100-diff/3))/100, (requested_speed*(100+(2*diff)/3))/100);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (requested_speed*(100+(2*diff)/3))/100, (requested_speed*(100-diff/3))/100);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, requested_speed, requested_speed);}
			break;
		case RUN:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (requested_speed*(100-diff))/100, requested_speed);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, requested_speed, (requested_speed*(100-diff))/100);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, requested_speed, requested_speed);}
			break;
		default:
			wheels_set_speed(GPIO_PIN_RESET, GPIO_PIN_RESET, STOP, STOP);
			break;
	}

}








/* ********************************************************************************************/
/* *****************	CALCULATE ANGLES NEEDED TO DIRECTED THE CAR		***********************/
/* ********************************************************************************************/


/* brief	Determine the angle between the North and the car
 * param	double carLatitudePre, double carLongitudePre		Previous GPS coordinates of the car
 * 			double carLatitude, double carLongitude				Actual GPS coordinates of the car
 * retval	double angleCar		Angle between the North and the car
 * */
double get_angle_car(double carLatPre, double carLongPre, double carLat, double carLong){
	return get_angle_GPS(carLatPre, carLongPre, carLat, carLong);
}

/* brief	Determine the angle between the North and the destination
 * param	double carLatitude, double carLongitude		Actual GPS coordinates of the car
 * 			double destLatitude, double destLongitude	Actual GPS coordinates of the destination
 * retval	double angleDest	Angle between the North and the destination
 * */
double get_angle_dest(double carLat, double carLong, double destLat, double destLong){
	return get_angle_GPS(carLat, carLong, destLat, destLong);
}


/* brief	Determine the angle we need to turn to join the right location
 * param	double angleCar		Angle between the North and the car
 * 			double angleDest	Angle between the North and the destination
 * retval	double angleToGo	Angle between the car and the destination
 * */
double get_angle_to_go(double angleCar, double angleDest) {
	double angleToGo = angleDest - angleCar;
	return (angleToGo);
}








/* ********************************************************************************************/
/* **********************	CAR MOVEMENT WITHOUT GPS CONNECTED		***************************/
/* ********************************************************************************************/



/* brief	Calculate the movement of the car according to the distance between the car and the location we want to join
 * param	double distance	Distance between the two GPS location in meters
 * retval	None
 * */
double go_straight_without_GPS(double distance){

	//maximum speed while distance less than 2m
	if (distance > 2.0) {
		car_control(RUN, STRAIGHT);
		distance = distance - RUN_SPEED; // each second, the car travels 0,527m at this speed (52,7cm/s)
		HAL_Delay(1000);
	}

	//medium speed between 2m and 25cm
	else if (distance > 0.25) {
		car_control(JOG, STRAIGHT);
		distance = distance - JOG_SPEED;
		HAL_Delay(1000);
	}

	//stop at 25cm
	else {
		car_control(STOP, STRAIGHT);
		pos_OK = 1;
	}

	return distance;
}

/* brief	Manage the movement between the car and the destination
 * param	double distance		Distance between the car and the destination
 * 			double angleToGo	Angle in degrees between the car and the destination according to the North
 * 			int first			Set if the routine begins in a new location
 * retval 	double angleCarDiff	Angle in degrees traveled from the last car location
 * */
double direction_speed_management_without_GPS(double distance, double angleToGo, int first){

	int angleCommand = STRAIGHT;
	double angleCarDiff = 0;

	/* When routine starts at the new location, the wheels turns and the car doesn't move */

	if (first == 1) {

		/* Manage the direction of the car according to the angle between the car axis and the GPS location */
		if (angleToGo < 10 || angleToGo >= 350) angleCommand = STRAIGHT;

		else if (angleToGo >= 10 && angleToGo < 180) {
			angleCommand = HARD_R;
			angleCarDiff = RIGHT_ANGLE;
		}
		else if (angleToGo >= 180 || angleToGo < 350) {
			angleCommand = HARD_L;
			angleCarDiff = LEFT_ANGLE;
		}
		/* Apply commands to different motors and stop when we are close to the destination */
		car_control(STOP, angleCommand);

	}
	else {
		/* Manage the direction of the car according to the angle between the car axis and the GPS location */
		if (angleToGo >= 0.0) {
			if (angleToGo < 5.5 || angleToGo >= 354.5) {angleCommand = STRAIGHT;}
			else if (angleToGo < 180) {
				angleCommand = HARD_R;
				angleCarDiff = RIGHT_ANGLE;
			}
			else if (angleToGo >= 180) {
				angleCommand = HARD_L;
				angleCarDiff = LEFT_ANGLE;
			}
		}

		else {
			if (angleToGo > (-5.5) || angleToGo <= (-354.5)) {angleCommand = STRAIGHT;}
			else if (angleToGo < (-180)) {
				angleCommand = HARD_R;
				angleCarDiff = RIGHT_ANGLE;
			}
			else if (angleToGo >= (-180)) {
				angleCommand = HARD_L;
				angleCarDiff = LEFT_ANGLE;
			}
		}

		/* Apply commands to different motors and stop when we are close to the destination */
		if (distance > 0.50) {
			car_control(JOG, angleCommand);
		}
		else {
			car_control(STOP, STRAIGHT);
			pos_OK = 1;
		}
	}

	return(angleCarDiff);

}

/* brief	Manage the movement of the car without GPS connected
 * param	double carLatitudeStart, carLongitudeStart	Car coordinates at the start of the routine
 * 			double destLatitude, destLongitude			Destination coordinates
 * retval 	None
 **/
void movement_without_GPS(double carLatitudeStart, double carLongitudeStart, double destLatitude, double destLongitude) {

	uint32_t startTime = 0;
	uint32_t currentTime = 0;
	double diffTime = 0;

	double angleDiff = 0;
	dist = get_distance(carLatitude, carLongitude, destLatitude, destLongitude);
	double angleDest = get_angle_dest(carLatitudeStart, carLongitudeStart, destLatitude, destLongitude);
	double angleToGo = get_angle_to_go(angleCar, angleDest);

	int first = 1;
	int cnt = 0;

	startTime = HAL_GetTick();

	/* update car coordinates calculated each seconds and movement*/
	while(pos_OK == 0) {

		angleDiff = direction_speed_management_without_GPS(dist, angleToGo, first);

		currentTime = HAL_GetTick();
      	diffTime = currentTime - startTime;

		if (diffTime/1000 > cnt) {

			first = 0;

			dist = get_distance(carLatitude, carLongitude, destLatitude, destLongitude);

			angleCar = angleCar + angleDiff;
			if(angleCar < 0) angleCar = 360+angleCar;

			angleToGo = get_angle_to_go(angleCar, angleDest);

			if(angleDiff < 0) angleDiff = 360+angleDiff;

			carLatitude = get_new_latitude(carLatitudeStart, angleCar, JOG_SPEED*cnt);
			carLongitude = get_new_longitude(carLatitudeStart, carLongitudeStart, carLatitude, angleCar, JOG_SPEED*cnt);
			cnt++;
		}
	}

}






/* ********************************************************************************************/
/* *************************	CAR MOVEMENT WITH GPS CONNECTED		***************************/
/* **************************	!!!! NOT OPERATIONNAL YET !!!!	*******************************/
/* ********************************************************************************************/



/* brief	Manage the direction of the car according to the angle between the car axis and the GPS location
 * param	double angleToGo	Angle between the axis of the car and the GPS location in degrees
 * retval	int angleCommand	Command to control the steering of the wheels
 * */
int calculate_direction_command_with_GPS(double angleToGo) {
	int angleCommand = STRAIGHT;

	if (angleToGo < 10 || angleToGo >= 350) {angleCommand = STRAIGHT;}
	else if (angleToGo >= 10 && angleToGo < 45) {angleCommand = MODT_R;}
	else if (angleToGo >= 45 && angleToGo < 180) {angleCommand = HARD_R;}
	else if (angleToGo >= 180 && angleToGo < 315) {angleCommand = HARD_L;}
	else if (angleToGo >= 315 && angleToGo < 350) {angleCommand = MODT_L;}

	return angleCommand;
}


/* brief	Control the speed and the steering of the car in real time according to the distance and the angle between the car and the location we want to join
 * param	double distance		Distance between the two GPS location in meters
 * 			double beta			Angle between the axis of the car and the GPS location in degrees
 * 			double alpha		Angle between the axis of the car and the North
 * retval	None
 * */
void direction_speed_management_with_GPS(double distance, double angleToGo){

	// calculate the angle command according to the angle beta
	int angleCommand = calculate_direction_command_with_GPS(angleToGo);
	// if beta is between 270 and 90 --> the car is in the general right direction -> we manage the speed in normal functioning
	if ((angleToGo <= 90 && angleToGo >= 0) || (angleToGo <= 360 && angleToGo >= 270)) {
		if (distance > 2.0) {
			car_control(RUN, angleCommand);
		}
		else if (distance > 0.25) {
			car_control(WALK, angleCommand);
		}
		else {
		    car_control(STOP, STRAIGHT);
		    pos_OK = 1;
		}
	}
	// if the car is totally in the wrong direction --> the car turns slowly
	else {
	    car_control(WALK, angleCommand);
	}

}

/* brief	Manage the movement between the car and the destination
 * param	double carLatitude, carLongitude			Actual GPS coordinates of the car
 * 			double carLatitudePre, carLongitudePre		Previous GPS coordinates of the car
 * 			double destLatitude, destLongitude			Actual GPS coordinates of the destination
 * retval 	None
 * */
void movement_with_GPS(double carLat, double carLong, double carLatPre, double carLongPre, double destLat, double destLong) {

	double distance = get_distance(carLat, carLong, destLat, destLong);
	double angleDest = get_angle_dest(carLat, carLong, destLat, destLong);

	double angleCar = get_angle_car(carLatPre, carLongPre, carLat, carLong);

	double angleToGo = get_angle_to_go(angleCar, angleDest);

	direction_speed_management_with_GPS(distance, angleToGo);
}







/* ********************************************************************************************/
/* **************************	MOVEMENT FOR FIRE DETECTION 	*******************************/
/* ********************************************************************************************/

/* brief	Make a 360 degrees turn
 * param	None
 * retval	None
 * */
void turn360(void) {

	uint32_t startTime = 0;
	uint32_t currentTime = 0;
	double diffTime = 0;

	int cnt=0;

	startTime = HAL_GetTick();

	while (!CHANGE_TO_STOP && !isFire) {
		currentTime = HAL_GetTick();
		diffTime = currentTime - startTime;

		if (diffTime/1000 > cnt) {
			car_control(JOG, HARD_R);
			if(angleCar > 360) angleCar = angleCar-360;
			angleCar = angleCar + RIGHT_ANGLE;
			cnt++;
		}
	}

	car_control(STOP, STRAIGHT);


}

/* brief	If a fire is detected, wait until the user tell that the car can start again
 * param	None
 * retval	None
 * */
void waiting_while_not_fire(void) {
	while(isFire == 0);
}
