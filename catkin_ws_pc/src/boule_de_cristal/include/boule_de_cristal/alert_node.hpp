#ifndef boule_de_cristal_ALERT_NODE_HPP_
#define boule_de_cristal_ALERT_NODE_HPP_

#ifndef Q_MOC_RUN
#include <ros/ros.h>
#endif
#include <cv_bridge/cv_bridge.h>
#include <ros/spinner.h>
#include <std_msgs/Int16.h>
#include <QStringListModel>
#include <QThread>
#include <string>
#include <thread>

namespace boule_de_cristal {

class AlertNode : public QThread {
  Q_OBJECT
 public:
  AlertNode(std::string alert_topic, ros::NodeHandle nh);
  virtual ~AlertNode();
  void alertCb(const std_msgs::Int16 &msg);

  ros::NodeHandle *nh;
  ros::Subscriber alert_sub;
  std::string alert_topic;
};

}  // namespace boule_de_cristal

#endif
