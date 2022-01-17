#include "../include/boule_de_cristal/image_node.hpp"
#include <ros/master.h>
#include <ros/network.h>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <sstream>
#include <string>

namespace boule_de_cristal {

ImageNode::ImageNode(std::string image_topic, ros::NodeHandle nh) : it(nh) {
    this->image_topic = image_topic ;
    image_sub_ = it.subscribe(this->image_topic, 1, &ImageNode::imageCb, this);
    camera_enabled = false ;
}

ImageNode::~ImageNode() {
  cv::destroyWindow(this->image_topic);
}

void ImageNode::showCamera() {
  cv::namedWindow(this->image_topic);
  camera_enabled = true ;
}

void ImageNode::hideCamera() {
  camera_enabled = false ;
  cv::destroyWindow(this->image_topic);
}


void ImageNode::imageCb(const sensor_msgs::ImageConstPtr& msg) {
  if (camera_enabled == false)
  {
    return ;
  }
  cv_bridge::CvImagePtr cv_ptr;
  try {
    cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
  } catch (cv_bridge::Exception& e) {
    ROS_ERROR("cv_bridge exception: %s", e.what());
    return;
  }

  // Update GUI Window
  cv::imshow(this->image_topic, cv_ptr->image);
  //cv::waitKey(30);
}

};  // namespace boule_de_cristal

