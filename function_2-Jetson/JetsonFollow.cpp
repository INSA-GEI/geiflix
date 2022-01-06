#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/opencv.hpp>


#include <iostream>

#include <list>
#include <vector>

#include <opencv2/highgui/highgui_c.h>
#include <opencv2/core/ocl.hpp>

//include LIDAR
#include <rplidar.h>

//include socket
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>

#define PORT 6666
#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

using namespace cv;
using namespace rp::standalone::rplidar;
using namespace std;

//-------------------IMAGE RECOGNITION
void DrawCircle(int posx, int posy, Mat & m, bool isMain) { //Draw circles, used for debugging 
	if (isMain){ circle(m, Point(posx, posy), 60, 150, 20); }
	else{ circle(m, Point(posx, posy), 20, 150, 5); }
	circle(m, Point(posx, posy), 12, 70, 2);
	

}
int Distance(int x1, int y1, int x2, int y2) { //calculate distance beetween two points in a 2D space
	return (abs(x2 - x1) + abs(y2 - y1));
}
int calcFOV(Mat &m, int FOVdiag) {
	int diag = sqrt((m.rows * m.rows) + (m.cols * m.cols));
	int FOV = (FOVdiag * m.cols) / diag;
	return FOV;
}
int xToTheta(int x, int width, int FOV) {
	int theta = (FOV/2)*(x-width/2)/(width/2);
	return theta;
}

int WhiteGroupsV2(Mat & m, Mat & edges, int& lX, int& lY, int& tries, int FOV){
	
	cvtColor(m, m, COLOR_BGR2GRAY); //Convert into grayscale

	//Edge detection --------------------------------------------------------------------------------
	adaptiveThreshold(m, edges, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 51, 7); 
	//morphologyEx(edges, edges, MORPH_OPEN, Mat(), Point(-1, 1), 1, 0, 1);
	morphologyEx(edges, edges, MORPH_GRADIENT, Mat(), Point(-1, 1), 1, 0, 1); //Close detected edges
	bitwise_not(edges, edges); // Invert Edges
		//imshow("Edges", edges); 
	
	//White detection --------------------------------------------------------------------------------
	blur(m, m, Size(11, 11)); //Blur to reduce noises
	threshold(m, m, 100, 255, 0); //Apply threshold to detect white pixels
	morphologyEx(m, m, MORPH_CLOSE, Mat(), Point(-1, 1), 2, 0, 1); //reduce noises again
		//imshow("thresh", m);

	bitwise_and(m, edges, m); //Combine the white detection with the edge detection
	

	//Analyze Group of white pixel on the white + edge picture
	Mat labels, stats, centroids;
	connectedComponentsWithStats(m, labels, stats, centroids, 8);

	/*for (int i = 0; i < stats.rows; i++)
	{
		if (stats.at<int>(Point(i, CC_STAT_AREA)) > 0) {
			int x = stats.at<int>(Point(0, i));
			int y = stats.at<int>(Point(1, i));
			int w = stats.at<int>(Point(2, i));
			int h = stats.at<int>(Point(3, i));
			Rect rect(x, y, w, h);
			rectangle(m, rect, 128);
		}	 
	}Draw rectangles on detected groups of white pixels*/

	int mainI = 0, maxChange = m.cols/5, dis = 0, minDist = m.rows*100;
	int x, y;

	for (int i = 1; i < stats.rows; i++) {
		if (stats.at<int>(Point(i, CC_STAT_AREA)) < m.rows*m.cols/6 && stats.at<int>(Point(i, CC_STAT_AREA)) > 0) {
			dis = Distance(lX, lY, centroids.at<double>(i, 0), centroids.at<double>(i, 1));
			if (dis < minDist) {
				minDist = dis;
				mainI = i;
			}
		}
	}
	if (minDist > maxChange) {
		if (tries > 50) { lX = m.cols/2; lY = m.rows/2; } //keep track of the number of time we failed and reset if we failed too many times
		tries++;
	}
	else { 
		tries = 0; 
		lX = centroids.at<double>(mainI, 0);
		lY = centroids.at<double>(mainI, 1);
	}

	//VISUAL PART FOR DEBUG
	//DrawCircle(lX, lY, m, true); //Draw a circle around the followed white object
	//imshow("Final", m); //Show final image

	int theta = xToTheta(lX, m.cols, FOV);
	//cout << theta << endl;
    return theta;
}
int RedTriangle(Mat & m)
{
	Mat ch1;

	vector<Mat> channels(3);
	split(m, channels);
	// get the channels (dont forget they follow BGR order in OpenCV)
	ch1 = channels[1];
	channels[1] = Mat::zeros(m.rows, m.cols, CV_8UC1); // green channel is set to 0
	channels[0] = Mat::zeros(m.rows, m.cols, CV_8UC1);// blue channel is set to 0

	merge(channels, ch1);

	//imshow("RED", ch1);
}
//-------------------LIDAR
bool checkRPLIDARHealth(RPlidarDriver * drv)
{
    u_result     op_result;
    rplidar_response_device_health_t healthinfo;


    op_result = drv->getHealth(healthinfo);
    if (IS_OK(op_result)) { // the macro IS_OK is the preperred way to judge whether the operation is succeed.
        printf("RPLidar health status : %d\n", healthinfo.status);
        if (healthinfo.status == RPLIDAR_STATUS_ERROR) {
            fprintf(stderr, "Error, rplidar internal error detected. Please reboot the device to retry.\n");
            // enable the following code if you want rplidar to be reboot by software
            // drv->reset();
            return false;
        } else {
            return true;
        }

    } else {
        fprintf(stderr, "Error, cannot retrieve the lidar health code: %x\n", op_result);
        return false;
    }
}

#include <signal.h>
bool ctrl_c_pressed;
void ctrlc(int)
{
    ctrl_c_pressed = true;
}
//-------------------MAIN
int main() {
	//INIT CAM
	int lX = 300;
	int lY = 300;
	int tries = 0;
	int FOV = 0;
    int theta = 0;
	
	Mat frame; // this will contain the image from the webcam
	Mat edges; //contain calculated edges 

	cv::VideoCapture camera(0);
	if (!camera.isOpened()) {
		std::cerr << "ERROR: Could not open camera" << std::endl;
		return 1;
	}
		//namedWindow("Webcam", CV_WINDOW_AUTOSIZE);
	camera >> frame;
	FOV = calcFOV(frame, 60);

	//INIT SOCKET
	int sock = 0, valread;
    struct sockaddr_in serv_addr;
    char const * msg;
    char buffer[1024] = {0};
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }
   
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
       
    // Convert IPv4 and IPv6 addresses from text to binary form
    if(inet_pton(AF_INET, "192.168.1.2", &serv_addr.sin_addr)<=0) 
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }
   
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }
	//INIT LIDAR
	
    const char * opt_com_path = NULL;
    _u32         baudrateArray[2] = {115200, 256000};
    _u32         opt_com_baudrate = 0;
    u_result     op_result;

    bool useArgcBaudrate = false;

    printf("Ultra simple LIDAR data grabber for RPLIDAR.\n" " Version: "RPLIDAR_SDK_VERSION"\n");

    // read serial port from the command line...
    /*if (argc>1) opt_com_path = argv[1]; // or set to a fixed value: e.g. "com3" 

    // read baud rate from the command line if specified...
    if (argc>2)
    {
        opt_com_baudrate = strtoul(argv[2], NULL, 10);
        useArgcBaudrate = true;
    }
	*/
    opt_com_path = "/dev/ttyUSB0";

    // create the driver instance
	RPlidarDriver * drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
    if (!drv) {
        fprintf(stderr, "insufficent memory, exit\n");
        exit(-2);
    }
    
    rplidar_response_device_info_t devinfo;
    bool connectSuccess = false;
    // make connection...
    if(useArgcBaudrate)
    {
        if(!drv)
            drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
        if (IS_OK(drv->connect(opt_com_path, opt_com_baudrate)))
        {
            op_result = drv->getDeviceInfo(devinfo);

            if (IS_OK(op_result)) 
            {
                connectSuccess = true;
            }
            else
            {
                delete drv;
                drv = NULL;
            }
        }
    }
    else
    {
        size_t baudRateArraySize = (sizeof(baudrateArray))/ (sizeof(baudrateArray[0]));
        for(size_t i = 0; i < baudRateArraySize; ++i)
        {
            if(!drv)
                drv = RPlidarDriver::CreateDriver(DRIVER_TYPE_SERIALPORT);
            if(IS_OK(drv->connect(opt_com_path, baudrateArray[i])))
            {
                op_result = drv->getDeviceInfo(devinfo);

                if (IS_OK(op_result)) 
                {
                    connectSuccess = true;
                    break;
                }
                else
                {
                    delete drv;
                    drv = NULL;
                }
            }
        }
    }
    if (!connectSuccess) {
        
        fprintf(stderr, "Error, cannot bind to the specified serial port %s.\n"
            , opt_com_path);
        //goto on_finished;
        RPlidarDriver::DisposeDriver(drv);
        drv = NULL;
        return -1; 
    }

    // print out the device serial number, firmware and hardware version number..
    printf("RPLIDAR S/N: ");
    for (int pos = 0; pos < 16 ;++pos) {
        printf("%02X", devinfo.serialnum[pos]);
    }

    printf("\n"
            "Firmware Ver: %d.%02d\n"
            "Hardware Rev: %d\n"
            , devinfo.firmware_version>>8
            , devinfo.firmware_version & 0xFF
            , (int)devinfo.hardware_version);



    // check health...
    if (!checkRPLIDARHealth(drv)) {
        //goto on_finished;
        RPlidarDriver::DisposeDriver(drv);
        drv = NULL;
        return -1;  
    }

    signal(SIGINT, ctrlc);
    
    drv->startMotor();
    // start scan...
    drv->startScan(0,1);    

    int cpt = 0;
    int index_min = -1;
    int index = 0;
    int shift = 0;
    int disFollow = 2300;
    int lastDis = disFollow;
    int cpterr = 0;

    int thetaSent = theta;

	// MAIN LOOP OF THE PROGRAM
	while (1) {
		//-----------------------CAM
		// show the image on the window
		// capture the next frame from the webcam
		camera >> frame;
			//imshow("Webcam", frame);

			//RedTriangle(frame);
		theta = WhiteGroupsV2(frame, edges, lX, lY, tries, FOV);


		//------------------------LIDAR PART
		rplidar_response_measurement_node_hq_t nodes[8192];
        size_t   count = _countof(nodes);

        op_result = drv->grabScanDataHq(nodes, count);

        //cout << "count :" <<count<< endl;

        if (IS_OK(op_result)) {
            cpt++;
            
            drv->ascendScanData(nodes, count);


            //Here we will take seven values around the angle that we are looking at
            list<int> values;
            //vector<int> distances;

			for(int i= -3; i<= 3; i ++){
                int y = ((int)count + index + i)%(int)count;
                double angle = (double) nodes[y].angle_z_q14 * 90.f / (1 << 14);
                int distance = (int) nodes[y].dist_mm_q2/4.0f;

                values.push_back(distance);
                //distances.push_back((int)distance);

                //cout << "angle " << i << " : " << (double) angle  << " distance: " << (int) distance << endl;
            }

            cout << endl;

            // Here we get the minimal distance among the seven distances that we measured
			int disMin = 0;
            bool hasChanged = false;
            list<int>::iterator it = values.begin();

            for (int i = 0; i < values.size(); i++) {
                if((*it <disMin && *it != 0) || (!hasChanged && *it != 0)){
                    disMin = *it;
                    hasChanged =true;
                    index_min = i;
                }
                it++;
            }
            if(disMin == 0){disMin = disFollow; index_min = values.size()/2;} // If we only have zeros on our values, we will send 2000 as a default value

            
	    shift = index_min-3;
            index = index + shift;
            /*if(index > (int)count){index = index - (int)count;}
            else if(index < 0){index = index + (int)count;}

            cout << "deplacement = " << shift << "\n";
            */
            theta = index*((float)360/(float)count);
            //index = (int)(theta/((float)360/(float)count)) ; //We calculate the angle at which the lidar will read distances according to the image analysis
            cout << "distance min " << disMin << " at theta " << theta << " and index " << index <<"\n";
            cout << endl;
            cout << endl;

			if (abs(disMin - lastDis) >= 1000){ // avoid a huge difference beetween two consecutive values
                disMin = lastDis;
                cpterr++;

                if (cpterr>4){lastDis = disFollow;}
            }else{lastDis = disMin; cpterr = 0;}


            /* code to invert wheels direction when going backward
            if(disMin < disFollow){thetaSent = -theta;}
            else{thetaSent = theta;}
            */
            /*
            // Obstacle avoidance
            if (((int) nodes[0].dist_mm_q2/4.0f < 1200) && disMin > disFollow){
                disMin = disFollow;
                cout << " OBSTACLE" <<endl;
            }else if(((int) nodes[(int)count/2].dist_mm_q2/4.0f < 500) && disMin < disFollow){
                disMin = disFollow;
                cout << " OBSTACLE" <<endl;
            }
            */
            if (cpt > 5) { //we wait the 5th value (initial values are wrong) and we send the distance and the angle to the server at each loop
                std::string tmp = std::to_string(disMin) + ":" + std::to_string(theta); //we send both values in a string with ":" as a separator
                msg = tmp.c_str();

                send(sock , msg , strlen(msg) , 0 );
                //printf("msg sent\n");
            } 
			}

        if (ctrl_c_pressed){ 
            break;
        }
		
	}
	//release memory 
	frame.release();
	
	//Stop lidar
	drv->stop();
    drv->stopMotor();

    RPlidarDriver::DisposeDriver(drv);
    drv = NULL;

	//end program
    return 0;  
}



