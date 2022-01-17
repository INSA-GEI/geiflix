#include "../include/boule_de_cristal/alert_node.hpp"
#include <ros/master.h>
#include <ros/network.h>
#include <ros/ros.h>
#include <std_msgs/String.h>
#include <sstream>
#include <string>
#include <chrono>
#include <ros/package.h>

namespace boule_de_cristal {

AlertNode::AlertNode(std::string alert_topic, ros::NodeHandle nh) {
    this->nh = &nh ;
    this->alert_topic = alert_topic ;
    this->alert_sub = this->nh->subscribe(this->alert_topic, 1, &AlertNode::alertCb,this);
/*
    this->t = new std::thread([](){
        
      ros::Rate r(10);
      while (1)
      {
        ros::spinOnce();
        r.sleep();
        std::cout << "ici" << std::endl ;
      }
      
      ros::AsyncSpinner spinner(4); // Use 4 threads
      spinner.start();
      ros::waitForShutdown();
    });
    this->t->detach();*/
    
}



AlertNode::~AlertNode() {
}


void AlertNode::alertCb(const std_msgs::Int16& msg) {
  std::string path = ros::package::getPath("boule_de_cristal");
  std::string sound = "/resources/banger.ogg";
  std::string cmd = "canberra-gtk-play -f " ;
  std::string sound_cmd = cmd + path + sound ;
  system(sound_cmd.c_str());

  auto start = std::chrono::system_clock::now();
  std::chrono::duration<double> elapsed_seconds = start - start ;
  while (elapsed_seconds.count() < 2)
  {
    auto current_time = std::chrono::system_clock::now();
    elapsed_seconds = current_time - start ;
  }


}

};  // namespace boule_de_cristal

