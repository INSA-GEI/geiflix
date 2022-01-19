#include "../include/boule_de_cristal/alert_node.hpp"
#include <ros/master.h>
#include <ros/network.h>
#include <ros/package.h>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <chrono>
#include <sstream>
#include <string>

namespace boule_de_cristal {

AlertNode::AlertNode(std::string alert_topic, ros::NodeHandle nh) {
  this->nh = &nh;
  this->alert_topic = alert_topic;
  this->alert_sub =
      this->nh->subscribe(this->alert_topic, 1, &AlertNode::alertCb, this);
}

AlertNode::~AlertNode() {}

void AlertNode::alertCb(const std_msgs::Int16& msg) {
  std::string path = ros::package::getPath("boule_de_cristal");
  std::string sound = "/resources/banger+instru.ogg";
  std::string cmd = "canberra-gtk-play -f ";
  std::string sound_cmd = cmd + path + sound;
  system(sound_cmd.c_str());
}

};  // namespace boule_de_cristal
