/**
 * @file /include/boule_de_cristal/qnode.hpp
 *
 * @brief Communications central!
 *
 * @date February 2011
 **/
/*****************************************************************************
** Ifdefs
*****************************************************************************/

#ifndef boule_de_cristal_QNODE_HPP_
#define boule_de_cristal_QNODE_HPP_

/*****************************************************************************
** Includes
*****************************************************************************/

// To workaround boost/qt4 problems that won't be bugfixed. Refer to
//    https://bugreports.qt.io/browse/QTBUG-22829
#ifndef Q_MOC_RUN
#include <ros/ros.h>
#endif
#include <QStringListModel>
#include <QThread>
#include <string>

/*****************************************************************************
** Namespaces
*****************************************************************************/

namespace boule_de_cristal {

/*****************************************************************************
** Class
*****************************************************************************/

class QNode : public QThread {
  Q_OBJECT
 public:
  QNode(int argc, char **argv);
  virtual ~QNode();
  bool init();
  bool init(const std::string &master_url, const std::string &host_url);
  void list();

  /*********************
  ** Logging
  **********************/
  enum LogLevel { Debug, Info, Warn, Error, Fatal };

  QStringListModel *loggingModel() { return &logging_model; }
  void log(const LogLevel &level, const std::string &msg);

 Q_SIGNALS:
  void loggingUpdated();

 private:
  int init_argc;
  char **init_argv;
  ros::Publisher chatter_publisher;
  QStringListModel logging_model;
};

}  // namespace boule_de_cristal

#endif /* boule_de_cristal_QNODE_HPP_ */
