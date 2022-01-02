#include "../include/boule_de_cristal/image_node.hpp"
#include <ros/master.h>
#include <ros/network.h>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <sstream>
#include <string>

namespace boule_de_cristal {

ImageNode::ImageNode(std::string image_topic) : it(nh) {
    this->image_topic = image_topic ;
    camera_enabled = false ;
}

ImageNode::~ImageNode() {
  cv::destroyWindow(this->image_topic);
}

void ImageNode::showCamera() {
  image_sub_ = it.subscribe(this->image_topic, 1, &ImageNode::imageCb, this);
  cv::namedWindow(this->image_topic);
  camera_enabled = true ;
  ros::Rate r(10) ;
  while (camera_enabled)
  {
    ros::spinOnce() ;
    r.sleep() ;
  }
}

void ImageNode::hideCamera() {
  camera_enabled = false ;
  image_sub_.shutdown();
  cv::destroyWindow(this->image_topic);
}


void ImageNode::imageCb(const sensor_msgs::ImageConstPtr& msg) {
  cv_bridge::CvImagePtr cv_ptr;
  try {
    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
  } catch (cv_bridge::Exception& e) {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
  }

  // Update GUI Window
  cv::imshow(this->image_topic, cv_ptr->image);
  cv::waitKey(30);
}

};  // namespace boule_de_cristal

