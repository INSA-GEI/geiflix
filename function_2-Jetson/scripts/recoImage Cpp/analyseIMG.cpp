#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/opencv.hpp>


#include <iostream>

#include <list>
#include <vector>

#include <opencv2/highgui/highgui_c.h>
#include <opencv2/core/ocl.hpp>



using namespace cv;
using namespace std;


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

void WhiteGroupsV2(Mat & m, Mat & edges, int& lX, int& lY, int& tries, int FOV){
	
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
	cout << theta << endl;
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

	imshow("RED", ch1);
}

int main() {
	int lX = 300;
	int lY = 300;
	int tries = 0;
	int FOV = 0;
	
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

	while (1) {
		// show the image on the window
		// capture the next frame from the webcam
		camera >> frame;
			//imshow("Webcam", frame);

		// wait (1ms) for a key to be pressed to exit loop
		if (waitKey(1) >= 0)
			break;
			//RedTriangle(frame);
		WhiteGroupsV2(frame, edges, lX, lY, tries, FOV);

	}
	//release memory and end program
	frame.release();
	return 0;
}



