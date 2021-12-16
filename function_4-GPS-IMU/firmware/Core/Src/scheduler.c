/*
 * scheduler.c
 *
 *  Created on: Sep 24, 2021
 *      Author: dimercur
 */

#include "stm32l4xx_hal.h"

#include "globalvar.h"
#include "teseo_liv3f.h"
#include "iks01a2.h"
#include "ahrs.h"
#include "can.h"

#include <stdio.h>
#include <string.h>

uint8_t flag_1ms;

/***************************************
 * GPS Data send and variables
 */
float64_t lat = 0;
float64_t lon = 0;
float64_t computing = 0;
uint8_t gps_data[8] = {0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};

/***************************************
 * IMU Data send
 */
int8_t IMU1[8] = {0, 0, 0, 0, 0, 0, 0, 0};
int8_t IMU2[8] = {0, 0, 0, 0, 0, 0, 0, 0};

/*********************************
 * Task task_send_values_GPS
 * Periodic: 2hz (500 ms)
 */
void task_send_values_GPS (void);
uint32_t counter_task_send_values_GPS;
#define PERIOD_TASK_SEND_VALUES_GPS 500

/*********************************
 * Task task_send_values_IMU
 * Periodic: 4hz (250 ms)
 */
void task_send_values_IMU (void);
uint32_t counter_task_send_values_IMU;
#define PERIOD_TASK_SEND_VALUES_IMU 200

/*********************************
 * Task task_get_acceleration
 * Periodic: 12.5hz (80 ms)
 */
void task_get_acceleration (void);
uint32_t counter_task_get_acceleration;
#define PERIOD_TASK_GET_ACCELERATION 80

/*********************************
 * Task task_get_rotation
 * Periodic: 12.5hz (80 ms)
 */
void task_get_rotation (void);
uint32_t counter_task_get_rotation;
#define PERIOD_TASK_GET_ROTATION 80

/*********************************
 * Task task_get_magnetic
 * Periodic: 10hz (100 ms)
 */
void task_get_magnetic (void);
uint32_t counter_task_get_magnetic;
#define PERIOD_TASK_GET_MAGNETIC 100

/*********************************
 * Task task_get_temperature
 * Periodic: 10hz (100 ms)
 */
void task_get_temperature (void);
uint32_t counter_task_get_temperature;
#define PERIOD_TASK_GET_TEMPERATURE 100

/*********************************
 * Task task_get_pressure
 * Periodic: 10hz (100 ms)
 */
void task_get_pressure (void);
uint32_t counter_task_get_pressure;
#define PERIOD_TASK_GET_PRESSURE 100

/*********************************
 * Task task_get_humidity
 * Periodic: 10hz (100 ms)
 */
void task_get_humidity (void);
uint32_t counter_task_get_humidity;
#define PERIOD_TASK_GET_HUMIDITY 100

/*********************************
 * Task task_update_gps
 * Periodic: 20hz (50 ms)
 */
void task_update_gps (void);
uint32_t counter_task_update_gps;
#define PERIOD_TASK_UPDATE_GPS 50

/*********************************
 * Task task_get_gps_coord
 * Periodic: 20hz (50 ms)
 */
void task_get_gps_coord(void);
uint32_t counter_task_get_gps_coord;
#define PERIOD_TASK_GET_GPS_COORD 50

/*********************************
 * Task task_compute_ahrs
 * Periodic: 12.5hz (80 ms)
 */
void task_compute_ahrs(void);
uint32_t counter_task_compute_ahrs;
#define PERIOD_TASK_COMPUTE_AHRS 80

void task_background(void);

/*
 * @brief  Initialize scheduler counters and flags
 *
 */
uint32_t SCHEDULER_Init(void) {
	flag_1ms =0;

	counter_task_send_values_IMU=0;
	counter_task_send_values_GPS=0;
	/* Counter for IMU tasks */
	counter_task_get_acceleration=0;
	counter_task_get_rotation=0;
	counter_task_get_magnetic=0;
	counter_task_get_pressure=0;
	counter_task_get_humidity=0;
	counter_task_get_temperature=0;

	/* Counter for ahrs tasks */
	counter_task_compute_ahrs=0;

	/* Counters for GPS tasks */
	counter_task_update_gps=0;
	counter_task_get_gps_coord=0;

	return 1;
}

/*
 * @brief  execute scheduler
 *
 */
void SCHEDULER_Run(void) {

	while (1)
	{
		if (flag_1ms!=0)
		{
			flag_1ms=0;

			/* increase task counters */
			counter_task_send_values_IMU++;
			counter_task_send_values_GPS++;
			counter_task_get_acceleration++;
			counter_task_get_rotation++;
			counter_task_get_magnetic++;
			counter_task_get_temperature++;
			counter_task_get_humidity++;
			counter_task_get_pressure++;
			counter_task_compute_ahrs++;
			counter_task_update_gps++;
			counter_task_get_gps_coord++;
		}

		if (counter_task_get_acceleration>= PERIOD_TASK_GET_ACCELERATION) {
			counter_task_get_acceleration=0;
			task_get_acceleration();
		}

		if (counter_task_get_rotation>= PERIOD_TASK_GET_ROTATION) {
			counter_task_get_rotation=0;
			task_get_rotation();
		}

		if (counter_task_get_magnetic>= PERIOD_TASK_GET_MAGNETIC) {
			counter_task_get_magnetic=0;
			task_get_magnetic();
		}

		if (counter_task_get_temperature>= PERIOD_TASK_GET_TEMPERATURE) {
			counter_task_get_temperature=0;
			task_get_temperature();
		}

		if (counter_task_get_humidity>= PERIOD_TASK_GET_HUMIDITY) {
			counter_task_get_humidity=0;
			task_get_humidity();
		}

		if (counter_task_get_pressure>= PERIOD_TASK_GET_PRESSURE) {
			counter_task_get_pressure=0;
			task_get_pressure();
		}

		if (counter_task_compute_ahrs>= PERIOD_TASK_COMPUTE_AHRS) {
			counter_task_compute_ahrs=0;
			task_compute_ahrs();
		}

		if (counter_task_update_gps>= PERIOD_TASK_UPDATE_GPS) {
			counter_task_update_gps=0;
			task_update_gps();
		}

		if (counter_task_get_gps_coord>= PERIOD_TASK_GET_GPS_COORD) {
			counter_task_get_gps_coord=0;
			task_get_gps_coord();
		}

		if (counter_task_send_values_IMU>= PERIOD_TASK_SEND_VALUES_IMU) {
			counter_task_send_values_IMU=0;
			task_send_values_IMU();
		}

		if (counter_task_send_values_GPS>= PERIOD_TASK_SEND_VALUES_GPS) {
			counter_task_send_values_GPS=0;
			task_send_values_GPS();
		}

		task_background();
	}
}

void task_background(void) {

}

void task_send_values_IMU (void) {
	memcpy((void*)&current_compass, (void*)AHRS_GetEulerAngles(),sizeof(AHRS_3AxisValues));


	printf("Acc: x=%4.2f\ty=%4.2f\tz=%4.2f\r\n",
			current_acceleration_mg.x, current_acceleration_mg.y, current_acceleration_mg.z);
	printf("Gyr: x=%4.2f\ty=%4.2f\tz=%4.2f\r\n",
			current_angular_rate_mdps.x, current_angular_rate_mdps.y, current_angular_rate_mdps.z);
	printf("Mag: x=%4.2f\ty=%4.2f\tz=%4.2f\r\n",
			current_magnetic_mG.x, current_magnetic_mG.y, current_magnetic_mG.z);
	printf("T°:%3.2f\r\nPres=%6.2f\r\nHum=%3.2f%%\r\n",
			current_temperature_degC, current_pressure_hPa, current_humidity_perc);
	printf("Lon=%2.5f\tLat=%2.5f\tAlt=%2.2f\r\n", current_coords.lon, current_coords.lat, current_coords.alt);
	printf("Compass: X=%3.2f\r\n         Y=%3.2f\r\n         Z=%3.2f\r\n",
					current_compass.x, current_compass.y, current_compass.z);
	printf("\r\n");
	IMU1[0]= (int)current_acceleration_mg.x & 0xff;
	IMU1[1]= (int)current_acceleration_mg.y & 0xff;
	IMU1[4]= ((int)current_angular_rate_mdps.z & 0xff00)>>8;
	IMU1[5]= ((int)current_angular_rate_mdps.z & 0xff);

	CAN_Send(IMU1, CAN_ID_IMU1);

	IMU2[0]= ((int)current_compass.x & 0xff00)>>8;
	IMU2[1]= ((int)current_compass.x & 0xff);
	IMU2[2]= ((int)current_compass.y & 0xff00)>>8;
	IMU2[3]= ((int)current_compass.y & 0xff);
	IMU2[4]= ((int)current_compass.z & 0xff00)>>8;
	IMU2[5]= ((int)current_compass.z & 0xff);

	CAN_Send(IMU2,CAN_ID_IMU2);
	printf("\r\n");

}

void task_send_values_GPS (void) {

	lat = current_coords.lat;
	lon = current_coords.lon;
	computing = lat;
	int Lat3 = floor(computing);
	computing = 100.0*(computing-(double)Lat3);
	int Lat2 = floor(computing);
	computing = 100.0*(computing-(double)Lat2);
	int Lat1 = floor(computing);
	computing = 100.0*(computing-(double)Lat1);
	int Lat0 = floor(computing);
	computing = lon;
	int Lon3 = floor(computing);
	computing = 100.0*(computing-(double)Lon3);
	int Lon2 = floor(computing);
	computing = 100.0*(computing-(double)Lon2);
	int Lon1 = floor(computing);
	computing = 100.0*(computing-(double)Lon1);
	int Lon0 = floor(computing);
	gps_data[0] = Lat3;
	gps_data[1] = Lat2;
	gps_data[2] = Lat1;
	gps_data[3] = Lat0;
	gps_data[4] = Lon3;
	gps_data[5] = Lon2;
	gps_data[6] = Lon1;
	gps_data[7] = Lon0;
	CAN_Send(gps_data, CAN_ID_GPS);
}

void task_get_acceleration (void) {
	IKS01A2_GetAcceleration(&current_acceleration_mg);
}

void task_get_rotation (void) {
	IKS01A2_GetRotation(&current_angular_rate_mdps);
}

void task_get_magnetic (void) {
	IKS01A2_GetMagnetic(&current_magnetic_mG);
}

void task_get_temperature (void) {
	IKS01A2_GetTemperature(&current_temperature_degC);
}

void task_get_humidity (void) {
	IKS01A2_GetHumidity(&current_humidity_perc);
}

void task_get_pressure (void) {
	IKS01A2_GetPressure(&current_pressure_hPa);
}

void task_compute_ahrs(void) {
	// TODO: AHRS is not working: maybe a problem with values scaling
	AHRS_Update(
			(AHRS_3AxisValues*)&current_acceleration_mg,
			(AHRS_3AxisValues*)&current_angular_rate_mdps,
			(AHRS_3AxisValues*)&current_magnetic_mG);
}

void task_update_gps(void) {
	TESEO_Update();
}

void task_get_gps_coord(void) {
	current_coords=TESEO_GetCoords_DD();
}
