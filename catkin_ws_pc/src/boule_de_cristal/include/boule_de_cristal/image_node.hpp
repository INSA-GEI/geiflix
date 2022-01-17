#ifndef boule_de_cristal_IMAGE_NODE_HPP_
#define boule_de_cristal_IMAGE_NODE_HPP_

#ifndef Q_MOC_RUN
#include <ros/ros.h>
#endif
#include <cv_bridge/cv_bridge.h>
#include <image_transport/image_transport.h>
#include <sensor_msgs/image_encodings.h>
#include <QStringListModel>
#include <QThread>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <string>
#include <ros/spinner.h>

namespace boule_de_cristal {

class ImageNode : public QThread {
  Q_OBJECT
 public:
  ImageNode(std::string image_topic, ros::NodeHandle nh);
  virtual ~ImageNode();
  void imageCb(const sensor_msgs::ImageConstPtr &msg);
  void showCamera() ;
  void hideCamera() ;

  image_transport::ImageTransport it ;
  image_transport::Subscriber image_sub_;

  std::string image_topic ;

  bool camera_enabled ;

};

}  // namespace boule_de_cristal

#endif
