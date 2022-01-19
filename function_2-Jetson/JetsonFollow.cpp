#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/opencv.hpp>


#include <iostream>

#include <list>
#include <vector>

#include <opencv2/highgui/highgui_c.h>
#include <opencv2/core/ocl.hpp>

#include <chrono>

//include LIDAR
#include <rplidar.h>

//include socket
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <string.h>
#include <string>

//include thread
#include <istream>
#include <sstream>
#include <fstream>
#include <streambuf>
#include <thread>
#include <fcntl.h>
#include <netdb.h>
#include <sys/types.h>


#define PORT 6666
#ifndef _countof
#define _countof(_Array) (int)(sizeof(_Array) / sizeof(_Array[0]))
#endif

using namespace cv;
using namespace rp::standalone::rplidar;
using namespace std;

bool veryLost = false;
int clientSocket;
int listening;

/*
When the robot is lost, the function createServLost() is launched.
This function create a server with a socket and  wait for client to connect.
Once one client is connected the listening socket send the content of
the website.
*/
void createServLost(){
    cout << "Thread server launched" << endl;

    std::string imageBase64;
    std::string line;

    // Encode the last image taken by the camera in base64
    system("base64 imageLost.jpg > image.txt");

    // Open and read image.txt to get the image in base64
    std::ifstream image;
    image.open("image.txt", std::ifstream::in);;
    if (image.good()) {
        imageBase64 += "<img src=\"data:image/gif;base64,";
        while (getline(image,line)) {
            imageBase64 += line;
        }
        imageBase64 += "\" class=\"responsive\" >";
        image.close();
    }
    else cout<< "no Image found"<<endl;

    // Open and read index.html and add the image
    std::string content;
    std::ifstream html;
    int i = 0;
    html.open("index.html", std::ifstream::in);;
    if (html.good()) {
        while (getline(html,line)) {
            i++;
            if (i == 82)
                content += imageBase64;
            else
                content += line;
        }
        html.close();
    }
    else cout<<"html not found" <<endl;

    // Create a socket
    listening = socket(PF_INET, SOCK_STREAM, 0);
    fcntl(listening, F_SETFL, O_NONBLOCK);
    if (listening == -1)
    {
        cerr << "Can't create a socket! Quitting" << endl;
        return;
    }
    else {
	cout << "socket ok" << endl;
    }
 
    // Bind the ip address and port to a socket
    sockaddr_in hint;
    hint.sin_family = AF_INET;
    hint.sin_port = htons(8080);
    inet_pton(AF_INET, "127.0.0.1", &hint.sin_addr);
 
    bind(listening, (sockaddr*)&hint, sizeof(hint));
    listen(listening, SOMAXCONN);
    // Wait for a connection
    sockaddr_in client;
    socklen_t clientSize = sizeof(client);

    // The listening socket loop until a connection or the robot is not lost anymore
    while(veryLost) {
        //cout<<"loop"<<endl;
        clientSocket = accept(listening, (sockaddr*)&client, &clientSize);
        if (clientSocket != -1) {
	    //cout << "something" << endl;
	    break;
	}
    }
 
    if (clientSocket != -1) {
        char host[NI_MAXHOST];
        char service[NI_MAXSERV];

        memset(host, 0, NI_MAXHOST);
        memset(service, 0, NI_MAXSERV);
    
        if (getnameinfo((sockaddr*)&client, sizeof(client), host, NI_MAXHOST, service, NI_MAXSERV, 0) == 0) {
            cout << host << " connected on port " << service << endl;
        }
        else {
            inet_ntop(AF_INET, &client.sin_addr, host, NI_MAXHOST);
            cout << host << " connected on port " << ntohs(client.sin_port) << endl;
        }

        // Write the html back to the client
        std::ostringstream oss;
        oss << "HTTP/1.1 " << 200 << " OK\r\n";
        oss << "Cache-Control: no-cache, private\r\n";
        oss << "Content-Type: text/html\r\n";
        oss << "\r\n";
        oss << content;

        std::string output = oss.str();
        int size = output.size() + 1;

        send(clientSocket, output.c_str(), size, 0);
    }
    else {
        cout << "no connection" << endl;  
    }
    close(listening);

}
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
static double angle(cv::Point pt1, cv::Point pt2, cv::Point pt0)
{
	double dx1 = pt1.x - pt0.x;
	double dy1 = pt1.y - pt0.y;
	double dx2 = pt2.x - pt0.x;
	double dy2 = pt2.y - pt0.y;
	return (dx1 * dx2 + dy1 * dy2) / sqrt((dx1 * dx1 + dy1 * dy1) * (dx2 * dx2 + dy2 * dy2) + 1e-10);
}
int RedTriangle(Mat & m, int& sqX, int& sqY, std::chrono::milliseconds stopDuration)
{
	int tolerance = m.rows/10;
	Mat bgIsolation; //detected orange-red part of the picture
    Mat pinkPart; //detected pink - red part of the picture
	
    // HSV range use for the red detection
	int hl = 0, hh = 20;
	int hl2 = 170, hh2 = 180;
	int sl = 100, sh = 255, vl = 20, vh = 255;

	cvtColor(m, bgIsolation, CV_BGR2HSV); // Convert the image into HSV space
	inRange(bgIsolation, Scalar(hl2, sl, vl), Scalar(hh2, sh, vh), pinkPart); 
	inRange(bgIsolation, Scalar(hl, sl, vl), Scalar(hh, sh, vh), bgIsolation);

	bitwise_or(bgIsolation, pinkPart, bgIsolation); // We add the two picture with an or mask to get a wider range of red colors
    
	morphologyEx(bgIsolation, bgIsolation, MORPH_CLOSE, Mat(), Point(-1, 1), 1, 0, 1); // Clean noise 
	// \HSV

	//CONTOURS
	cv::Mat bw;
	cv::Canny(bgIsolation, bw, 0, 50, 5);
	// Find contours
	std::vector<std::vector<cv::Point> > contours;
	cv::findContours(bw.clone(), contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE); //Apply an edge detection on the picture
	std::vector<cv::Point> approx;

	for (int i = 0; i < contours.size(); i++)
	{
		// Approximate contour with accuracy proportional
		// to the contour perimeter
		cv::approxPolyDP(cv::Mat(contours[i]), approx, cv::arcLength(cv::Mat(contours[i]), true) * 0.02, true);
		// Number of vertices of polygonal curve
		int vtc = approx.size();

		// Skip small or non-convex objects 
		if (std::fabs(cv::contourArea(contours[i])) < 500 || !cv::isContourConvex(approx))
			continue;

		if (vtc == 3)
		{
            cv::Rect r = cv::boundingRect(contours[i]);
			if (abs(r.width - r.height) < 50) { //look for a square bounding box
                if (stopDuration.count() > 3000) { //check if we already have detected a triangle less than 3 seconds ago
                    return 1;
                }
            }
		}
		else if (vtc ==4)
		{		
			// Get the cosines of all corners
			std::vector<double> cos;
			for (int j = 2; j < vtc + 1; j++)
				cos.push_back(angle(approx[j % vtc], approx[j - 2], approx[j - 1]));

			// Sort ascending the cosine values
			std::sort(cos.begin(), cos.end());

			// Get the lowest and the highest cosine
			double mincos = cos.front();
			double maxcos = cos.back();
			
			// Use the degrees obtained above and the number of vertices
			// to determine the shape of the contour
			if (mincos >= -0.1 && maxcos <= 0.3) {

				cv::Rect r = cv::boundingRect(contours[i]);

				if (abs(r.width - r.height) < 50) {
					cv::Point pt(r.x + (r.width / 2), r.y + (r.height / 2)); //get center point of triangle
					sqX = pt.x;
					sqY = pt.y;
					return 2;
				}
			}
		}
	}
	//imshow("dst", bgIsolation);
	return 0;
	//\CONTOURS
}
int WhiteGroupsV2(Mat & m, Mat & edges, int& lX, int& lY, int& tries, int FOV){
	
	cvtColor(m, m, COLOR_BGR2GRAY); //Convert into grayscale

	//Edge detection --------------------------------------------------------------------------------
	adaptiveThreshold(m, edges, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY, 51, 7); 
	morphologyEx(edges, edges, MORPH_GRADIENT, Mat(), Point(-1, 1), 1, 0, 1); //Close detected edges
	bitwise_not(edges, edges); // Invert Edges
		//imshow("Edges", edges); 
	
	//White detection --------------------------------------------------------------------------------
	blur(m, m, Size(11, 11)); //Blur to reduce noises
	threshold(m, m, 120, 255, 0); //Apply threshold to detect white pixels
	morphologyEx(m, m, MORPH_CLOSE, Mat(), Point(-1, 1), 2, 0, 1); //reduce noises again
		//imshow("thresh", m);

	bitwise_and(m, edges, m); //Combine the white detection with the edge detection
	

	//Analyze Group of white pixel on the white + edge picture
	Mat labels, stats, centroids;
	connectedComponentsWithStats(m, labels, stats, centroids, 8);

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
	int lX = 300, lY = 300;
    int sqX = 300, sqY = 300;
	int tries = 0;
	int FOV = 0;
    int theta = 0;

    bool stopped = false;
    bool lost = false;
    bool Obstacle = false;
    //bool veryLost = false;

    int motorEnable = 1;
    auto timerStop = std::chrono::high_resolution_clock::now();//timer since last stop signal
	
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

    printf("Ultra simple LIDAR data grabber for RPLIDAR.\n");

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

    //int thetaSent = theta;

    thread t1; //thread used for the server when the car is lost

	// MAIN LOOP OF THE PROGRAM
	while (1) {
		//-----------------------CAM
		// show the image on the window
		// capture the next frame from the webcam
		camera >> frame;
			//imshow("Webcam", frame);

        auto t2 = std::chrono::high_resolution_clock::now();
		auto int_stopDuration = std::chrono::duration_cast<std::chrono::milliseconds> (t2 - timerStop);
		switch (RedTriangle(frame, sqX, sqY, int_stopDuration)) { // Check signal detection
		case 0:
			break;
		case 1: //Triangle detected
			timerStop = std::chrono::high_resolution_clock::now();
			cout << "SSSSSTTTTOOOOOPPP" << endl;
			stopped = !stopped;
			break;
		case 2: //Square detected
			lX = sqX;
			lY = sqY;
			cout << "SQUAAARE" << endl;
			break;
		default:
			break;
		}
		theta = WhiteGroupsV2(frame, edges, lX, lY, tries, FOV); // White pixel detection


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

			for(int i= -3; i<= 3; i ++){
                int y = ((int)count + index + i)%(int)count;
                double angle = (double) nodes[y].angle_z_q14 * 90.f / (1 << 14);
                int distance = (int) nodes[y].dist_mm_q2/4.0f;

                values.push_back(distance);
            }

            //cout << endl;

            // Here we get the minimal distance among the seven distances that we measured
			int disMin = 0;
            bool hasChanged = false;
            list<int>::iterator it = values.begin();

            for (int i = 0; i < values.size(); i++) {
                //if((*it <disMin && *it != 0) || (!hasChanged && *it != 0)){
                if((*it <disMin && *it >= 1000) || (!hasChanged && *it >= 1000)){
                    disMin = *it;
                    hasChanged =true;
                    index_min = i;
                }
                it++;
            }
            //if(disMin == 0){disMin = disFollow; index_min = values.size()/2;} // If we only have zeros on our values, we will send 2000 as a default value
            if(disMin == 0){
                //disMin = lastDis;
                disMin = 10000; 
                index_min = values.size()/2;
            }
            
	        //shift = index_min-3; //Used to update the angle of the lidar if the camera is not used
            //index = index + shift; //Used to update the angle of the lidar if the camera is not used
            
            
            //theta = index*((float)360/(float)count); // we calculate the angle from the lidar ( used instead of the camera in case there is a bug)
            index = (int)(theta/((float)360/(float)count)) ; //We calculate the angle at which the lidar will read distances according to the image analysis
            //cout << "distance min " << disMin << " at theta " << theta << " and index " << index <<"\n";
            cout << endl;
            //cout << endl;

			if ((disMin - lastDis) >= 1000 || (lastDis - disMin)> 2000){ // avoid a huge difference beetween two consecutive values
                disMin = lastDis;
                cpterr++;

                if (cpterr>5){
                    lost = true; 
                    cpterr++; 

                    if (cpterr>20){ // if we can't detect a valid target for too long the car get in very lost mode
                        if(veryLost == false){
                            veryLost = true;
                            //Encode Image from the camera into base 64
                            camera >> frame;
                            imwrite("imageLost.jpg",frame);
			    // Launch web server in thread
                            t1 = thread(createServLost);
                            cout << "VERY LOST"<<endl;
                        }
                        
                        }
                    }
            }else{
                lastDis = disMin; 
                cpterr = 0; 
                lost = false;

                if(veryLost){
                    cout<<"close serveur"<<endl;
                    close(clientSocket);
                    close(listening);
                    listening = 0;
                    clientSocket = 0;
                    veryLost=false;
                    t1.join();
                }
               
            }


            /* code to invert wheels direction when going backward NOT USED IN THE FINAL VERSION
            if(disMin < disFollow){thetaSent = -theta;}
            else{thetaSent = theta;}
            */
            
            
            // Obstacle avoidance with lidar
            //if (((int) nodes[0].dist_mm_q2/4.0f < 1200) && disMin > disFollow && ((int) nodes[0].dist_mm_q2/4.0f > 300)){
                int av1= (int) nodes[0].dist_mm_q2/4.0f;
                int av2 = (int) nodes[(int)count -1].dist_mm_q2/4.0f;
                int av3 = (int) nodes[1].dist_mm_q2/4.0f;

                int ar1= (int) nodes[(int)count/2].dist_mm_q2/4.0f;
                int ar2 = (int) nodes[(int)count/2 - 1].dist_mm_q2/4.0f;
                int ar3 = (int) nodes[(int)count/2 +1].dist_mm_q2/4.0f;
            if ( ((av1 < 1200 && av1 > 300)||(av2 < 1200 && av2 > 300)||(av3 < 1200 && av3 > 300)) && disMin > disFollow){
                //disMin = disFollow;
                cout << " OBSTACLE" <<endl;
                Obstacle = true;
            }else if ( ((ar1 < 700 && ar1 > 100)||(ar2 < 700 && ar2 > 100)||(ar3 < 700 && ar3 > 100)) && disMin < disFollow){ 
                //disMin = disFollow;
                cout << " OBSTACLE" <<endl;
                Obstacle = true;
            }else {Obstacle = false;}
            
            

            if(stopped || lost || Obstacle){motorEnable = 0;}
            else{motorEnable = 1;}
            if (cpt > 5) { //we wait the 5th value (initial values are wrong) and we send the distance and the angle to the server at each loop
                std::string tmp = std::to_string(disMin) + ":" + std::to_string(theta) + ":" + std::to_string(motorEnable); //we send both values in a string with ":" as a separator
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



