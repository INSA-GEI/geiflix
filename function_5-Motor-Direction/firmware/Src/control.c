/*
 * control.c
 *
 *  Created on: 12 nov. 2021
 *      Author: Carole Meyer
 */

/* Includes ------------------------------------------------------------------*/


#include "control.h"

#include "steering.h"
#include "wheels.h"
#include "GPS.h"

#include "gpio.h"


/* Private define ------------------------------------------------------------*/

#define MAX_SPEED_CM_S 	0.527	// speed in centimeter/s when speed set at 75 --> init = 0.527
#define MED_SPEED_CM_S 	0.17 	// speed in centimeter/s when speed set at 60


#define DISABLED 	0

//Definition des modes de vitesse :: SPEED MODES
#define STOP 		50
#define REVERSE 	40
#define WALK 		58
#define JOG 		65
#define RUN 		75

//Definition des modes de direction :: STEERING MODES
#define STRAIGHT 	50
#define HARD_L 		10
#define MODT_L 		25
#define SOFT_L 		40
#define HARD_R 		90
#define MODT_R 		75
#define SOFT_R 		60

//Definition des pourcentages de differentiel
#define DIFF_NONE 	0
#define DIFF_SMALL 	5
#define DIFF_MEDIUM 10
#define DIFF_LARGE 	15

//Definition des types d'azimut
#define AZIMUT_FORWARD 	0
#define AZIMUT_LEFT		1
#define AZIMUT_RIGHT	2


extern double alpha;
extern int pos_OK;
int CHANGE_TO_STOP=0;

/* Private variables ---------------------------------------------------------*/

/* Programs ------------------------------------------------------------------*/

/**
*	Controle les MARG, MARD et MAV à partir de modeSpeed et modeSteer recus via le CAN
**/
void car_control(int requested_speed, int requested_steer){
	int diff = DIFF_NONE;
	int azimut = AZIMUT_FORWARD;

	// Limite la commande contenue dans le message CAN dans l'intervalle [0,100]
	if (requested_speed > 75){requested_speed = 75;}

	// Classification de la commande CAN recue
	if (requested_speed == DISABLED) {requested_speed = DISABLED;}
	else if (requested_speed <= REVERSE) {requested_speed = REVERSE;}
	else if (requested_speed < WALK) {requested_speed = STOP;}
	else if (requested_speed < JOG) {requested_speed = WALK;}
	else if (requested_speed < RUN) {requested_speed = JOG;}
	else {requested_speed = RUN;}

	// Limite la commande contenue dans le message CAN dans l'intervalle [0,100]
	if (requested_steer > 100){requested_steer = 100;}

	// Classification de la commande CAN recue
	if (requested_steer == DISABLED) {requested_steer = DISABLED;}
	else if (requested_steer <= HARD_L) {requested_steer = HARD_L;}
	else if (requested_steer <= MODT_L) {requested_steer = MODT_L;}
	else if (requested_steer <= SOFT_L) {requested_steer = SOFT_L;}
	else if (requested_steer < SOFT_R) {requested_steer = STRAIGHT;}
	else if (requested_steer < MODT_R) {requested_steer = SOFT_R;}
	else if (requested_steer < HARD_R) {requested_steer = MODT_R;}
	else {requested_steer = HARD_R;}

	//Actionnement de la commande du moteur de direction
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

	//Actionnement de la commande des moteurs de propulsion
	switch(requested_speed) {
		case STOP:
			wheels_set_speed(GPIO_PIN_RESET, GPIO_PIN_RESET, STOP, STOP);
			break;
		case REVERSE:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (modeSpeed*(100-diff))/100, modeSpeed);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, modeSpeed, (modeSpeed*diff)/100);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, modeSpeed, modeSpeed);}
			break;
		case WALK:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, modeSpeed, (modeSpeed*(100+diff))/100);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (modeSpeed*(100+diff))/100, modeSpeed);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, modeSpeed, modeSpeed);}
			break;
		case JOG:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (modeSpeed*(100-diff/3))/100, (modeSpeed*(100+(2*diff)/3))/100);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (modeSpeed*(100+(2*diff)/3))/100, (modeSpeed*(100-diff/3))/100);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, modeSpeed, modeSpeed);}
			break;
		case RUN:
			if (azimut == AZIMUT_RIGHT){wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (modeSpeed*(100-diff))/100, modeSpeed);}
			else if (azimut == AZIMUT_LEFT) {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, modeSpeed, (modeSpeed*(100-diff))/100);}
			else {wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, modeSpeed, modeSpeed);}
			break;
		default:
			wheels_set_speed(GPIO_PIN_RESET, GPIO_PIN_RESET, STOP, STOP);
			break;
	}

}

/* brief	Calculate the movement of the car according to the distance between the car and the location we want to join
 * param	double distance	Distance between the two GPS location in meters
 * retval	None
 * */

double go_straight_without_GPS(double distance){
	//float start_dist = distance;

	//maximum speed while distance less than 2m
	if (distance > 2.0) {
		wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, 70, 70);
		distance = distance - MAX_SPEED_CM_S; // each second, the car travels 0,527m at this speed (52,7cm/s)
		HAL_Delay(1000);
	}

	//medium speed between 2m and 25cm
	else if (distance > 0.25) {
		wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, 60, 60);
		distance = distance - MED_SPEED_CM_S;
		HAL_Delay(1000);
	}

	//stop at 25cm
	else {
		wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, 50, 50);
		pos_OK = 1;
	}

	return distance;
}

/* brief	Determine the angle we need to turn to join the right location
 * param	int requested_speed
 * 			int resquested_angle
 * retval	double alpha_diff	Angle between the North and the axis of the car
 * */
double calculate_alpha(int requested_speed, int requested_steer){
	int alpha_diff = 0;

	switch(requested_steer) {
			case STRAIGHT:
				alpha_diff = 0;
			case HARD_L:
				switch (requested_speed) {
					case WALK :
						alpha_diff = 0;
						break;
					case JOG :
						alpha_diff = 0;
						break;
					case RUN :
						alpha_diff = 0;
						break;
				}
			case MODT_L:
				switch (requested_speed) {
					case WALK :
						alpha_diff = 0;
						break;
					case JOG :
						alpha_diff = 0;
						break;
					case RUN :
						alpha_diff = 0;
						break;
				}
			case SOFT_L:
				switch (requested_speed) {
					case WALK :
						alpha_diff = 0;
						break;
					case JOG :
						alpha_diff = 0;
						break;
					case RUN :
						alpha_diff = 0;
						break;
				}
			case HARD_R:
				switch (requested_speed) {
					case WALK :
						alpha_diff = 0;
						break;
					case JOG :
						alpha_diff = 0;
						break;
					case RUN :
						alpha_diff = 0;
						break;
				}
			case MODT_R:
				switch (requested_speed) {
					case WALK :
						alpha_diff = 0;
						break;
					case JOG :
						alpha_diff = 0;
						break;
					case RUN :
						alpha_diff = 0;
						break;
				}
			case SOFT_R:
				switch (requested_speed) {
					case WALK :
						alpha_diff = 0;
						break;
					case JOG :
						alpha_diff = 0;
						break;
					case RUN :
						alpha_diff = 0;
						break;
				}
	}

			return alpha_diff;
}

/* brief	Determine the angle we need to turn to join the right location
 * param	double teta		Angle between the North and the GPS location we want to join
 * 			double alpha	Angle between the North and the axis of the car
 * retval	double beta		Angle between the axis of the car and the GPS location
 * */
double calculate_beta(double teta) {
	return (teta - alpha);
}


/* brief	Manage the direction of the car according to the angle between the car axis and the GPS location
 * param	double beta			Angle between the axis of the car and the GPS location in degrees
 * retval	int angle_command	Command to control the steering of the wheels
 * */
int direction_management(double beta) {
	int angle_command = 50;

	if (beta < 10 || beta >= 350) {angle_command = STRAIGHT;}
	else if (beta >= 10 && beta < 45) {angle_command = MODT_R;}
	else if (beta >= 45 && beta < 180) {angle_command = HARD_R;}
	else if (beta >= 180 && beta < 315) {angle_command = HARD_L;}
	else if (beta >= 315 && beta < 350) {angle_command = MODT_L;}

	return angle_command;
}


/* brief	Control the speed and the steering of the car in real time according to the distance and the angle between the car and the location we want to join
 * param	double distance		Distance between the two GPS location in meters
 * 			double beta			Angle between the axis of the car and the GPS location in degrees
 * 			double alpha		Angle between the axis of the car and the North
 * retval	None
 * */
void direction_speed(double distance, double beta){

	// calculate the angle command according to the angle beta
	int angle_command = STRAIGHT;//direction_management(beta);

	// if beta is between 270 and 90 --> the car is in the general right direction -> we manage the speed in normal functioning
	if ((beta <= 90 && beta >= 0) || (beta <= 360 && beta >= 270)) {
		if (distance > 2.0) {
			alpha = alpha + calculate_alpha(RUN, angle_command);
			car_control(RUN, angle_command);
		}
		else if (distance > 0.25) {
			alpha = alpha + calculate_alpha(WALK, angle_command);
			car_control(WALK, angle_command);
		}
		else {
			alpha = alpha + calculate_alpha(STOP, STRAIGHT);
		    car_control(STOP, STRAIGHT);
		    pos_OK = 1;
		}
	}

	// if the car is totally in the wrong direction --> the car turns slowly
	else {
		alpha = alpha + calculate_alpha(WALK, angle_command);
	    car_control(WALK, angle_command);
	}

}

/* brief	Manage the movement from 2 GPS coordinates
 * param	double lat1, lon1, lat2, lon2	GPS decimal coordinates : latitude and longitude of each location
 * 			double alpha 					Actual angle between the North and the axis of the car
 * retval	double alpha					Update angle between the North and the axis of the car
 * */
void movement_with_GPS(double lat1, double lon1, double lat2, double lon2) {

	double distance = get_distance(lat1, lon1, lat2, lon2);
	double teta = get_angle_GPS(lat1, lon1, lat2, lon2);

	double beta = calculate_beta(teta);

	direction_speed(distance, beta);

}

/* brief	Make a 360 degrees turn
 * param	None
 * retval	None
 * */
void turn360(void) {
	if (!CHANGE_TO_STOP){
		steering_set_position(GPIO_PIN_SET, HARD_R);
		wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, STOP, RUN);
	}
	else{
		wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, STOP, STOP);
		steering_set_position(GPIO_PIN_SET, STRAIGHT);
	}
	//wheels_set_speed(GPIO_PIN_SET, GPIO_PIN_SET, (60*(100+(2*DIFF_LARGE)/3))/100, (60*(100-DIFF_LARGE/3))/100);
}

