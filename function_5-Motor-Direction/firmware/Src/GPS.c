/*
 * GPS.c
 *
 *  Created on: 1 déc. 2021
 *      Author: Amélie MAIER
 */

/* Includes ------------------------------------------------------------------*/

#include "GPS.h"
#include "stdlib.h"
#include "math.h"

/* Private define ------------------------------------------------------------*/
#define PI 3.14159265358979
#define R  6371.160 	// Earth radius in France

extern double latDegPos;
extern double latMinPos;
extern double latSecPos;
extern double latTenPos;
extern double lonDegPos;
extern double lonMinPos;
extern double lonSecPos;
extern double lonTenPos;


extern double latDegDes;
extern double latMinDes;
extern double latSecDes;
extern double latTenDes;
extern double lonDegDes;
extern double lonMinDes;
extern double lonSecDes;
extern double lonTenDes;

/* Programs ------------------------------------------------------------------*/

/* brief	Conversion coordinates from DMS (degrees / minutes / seconds / tenths of a second) to DD (decimal degrees)
 * param	double deg, min, sec, ten 	Angle in DMS
 * retval	double angle_deg 			Angle in degrees decimals
 * */
double dms2dd(double deg, double min, double sec, double ten) {

	  if (ten < 10) {sec = sec + ten/10;}
	  else if (ten < 100) {sec = sec + ten/100;}
	  else if (ten < 1000) {sec = sec + ten/1000;}

	  min = min + sec/60;
	  deg = deg + min/60;

	  return deg;
}

/* brief	Conversion degrees to radians
 * param	double angle_rad 	Angle in radians
 * retval	double angle_deg 	Angle in degrees
 * */
double deg2rad(double angle_rad) {
	return ((2.0*PI) * angle_rad) / 360;
}

/* brief	Determine the distance in meters between two GPS location
 * param	double lat1, lon1, lat2, lon2	GPS decimal coordinates : latitude and longitude of each location
 * retval	double distance	Distance between the two GPS location in meters
 * */

double get_distance(double lat1, double lon1, double lat2, double lon2){

  // degree to radian conversion
  double lat1_r = deg2rad(lat1);
  double lon1_r = deg2rad(lon1);
  double lon2_r = deg2rad(lon2);
  double lat2_r = deg2rad(lat2);

  // distance calcul
  double dist_lat = (lat2_r - lat1_r) / 2.0;
  double dist_lon = (lon2_r - lon1_r) / 2.0;

  double a = ( sinf(dist_lat)*sinf(dist_lat) ) + cosf(lat1) * cosf(lat2) * ( sinf(dist_lon) * sinf(dist_lon) );

  double d = 2.0 * R * atan2f( sqrt(a), sqrt(1.0-a) );

  return (d*1000);
}

/* brief	Determine the angle in degrees compared to the North between two GPS location
 * param	double lat1, lon1, lat2, lon2	GPS decimal coordinates : latitude and longitude of each location
 * retval	double Angle					Angle between the two GPS location in degrees compared to the North
 * */
double get_angle_GPS(double lat1, double lon1, double lat2, double lon2) {

	double lat1_r = deg2rad(lat1);
	double lon1_r = deg2rad(lon1);
	double lon2_r = deg2rad(lon2);
	double lat2_r = deg2rad(lat2);

	// calculation of relatif angle in radian
    double dLon = (lon2_r - lon1_r);
	double y = sinf(dLon) * cosf(lat2_r);
	double x = ( cosf(lat1_r) * sinf(lat2_r) ) - ( sinf(lat1_r) * cosf(lat2_r) * cosf(dLon) ) ;
	double angle_rad = atan2f(y, x);

	//conversion in deg + conversion to have absolute angle compared to the North
	double angle_deg = ( 360 * angle_rad ) / (2*PI);
	angle_deg = fmod((angle_deg + 360.0), 360.0);

    return angle_deg;
}

/* brief	Determine the new latitude of the car according to the distance and the angle traveled from the previous car location
 * param	double latPrev	Previous latitude of the car
 * 			double angle	Angle in degrees traveled from the previous car position compared to the North
 * 			double dist		Distance in meters traveled from the previous car position compared to the North
 * retval	double lat 		New latitude of the car
 * */
double get_new_latitude(double latPrev, double angle, double dist) {

	  double delta = dist/(R*1000);

	  //conversion in radian
	  double latPrev_r = deg2rad(latPrev);
	  double angle_r = deg2rad(angle);

	  // calculate the new latitude in radian
	  double latNew_r = asinf( sinf(latPrev_r) * cosf(delta) + cosf(latPrev_r) * sinf(delta) * cosf(angle_r));

	  //conversion in deg + conversion to have absolute angle compared to the North
	  double latNew = (360 * latNew_r) / (2*PI);
	  latNew = fmod((latNew + 360.0), 360.0);

	  return(latNew);
}

/* brief	Determine the new longitude of the car according to the distance and the angle traveled from the previous car location
 * param	double latPrev, longPrev	Previous coordinates of the car
 * 			double latNew				New latitude of the car
 * 			double angle	Angle in degrees traveled from the previous car position compared to the North
 * 			double dist		Distance in meters traveled from the previous car position compared to the North
 * retval	double lon		New longitude of the car
 * */
double get_new_longitude(double latPrev, double longPrev, double latNew, double angle, double dist) {

	  double delta = dist/(R*1000);

	  //conversion in radian
	  double latPrev_r = deg2rad(latPrev);
	  double longPrev_r = deg2rad(longPrev);
	  double latNew_r = deg2rad(latNew);
	  double angle_r = deg2rad(angle);

	  // calculate the new latitude in radian
	  double longNew_r = longPrev_r + atan2f( sinf(angle_r) * sinf(delta) * cosf(latPrev_r) , cosf(delta) - sinf(latPrev_r)*sinf(latNew_r));

	  //conversion in deg + conversion to have absolute angle compared to the North
	  double longNew = ( 360 * longNew_r) / (2*PI);
	  longNew = fmod((longNew + 360.0), 360.0);

	  return(longNew);
}

/* brief	Set to 0 car coordinates
 * param	None
 * retval	None
 * */
void car_coordinates_to_zero(void) {
	latDegPos = 0;
	latMinPos = 0;
	latSecPos = 0;
	latTenPos = 0;
	lonDegPos = 0;
	lonMinPos = 0;
	lonSecPos = 0;
	lonTenPos = 0;
}

/* brief	Set to 0 destination coordinates
 * param	None
 * retval	None
 * */
void dest_coordinates_to_zero(void) {
	latDegDes = 0;
	latMinDes = 0;
	latSecDes = 0;
	latTenDes = 0;
	lonDegDes = 0;
	lonMinDes = 0;
	lonSecDes = 0;
	lonTenDes = 0;
}

