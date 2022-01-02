/**
 * @file /include/boule_de_cristal/main_window.hpp
 *
 * @brief Qt based gui for boule_de_cristal.
 *
 * @date November 2010
 **/
#ifndef boule_de_cristal_MAIN_WINDOW_H
#define boule_de_cristal_MAIN_WINDOW_H

/*****************************************************************************
** Includes
*****************************************************************************/

#include <QMainWindow>
#include "boule_de_cristal/ui_main_window.h"
#include "image_node.hpp"
#include "qnode.hpp"

/*****************************************************************************
** Namespace
*****************************************************************************/

namespace boule_de_cristal {

/*****************************************************************************
** Interface [MainWindow]
*****************************************************************************/
/**
 * @brief Qt central, all operations relating to the view part here.
 */
class MainWindow : public QMainWindow {
  Q_OBJECT

 public:
  MainWindow(int argc, char **argv, QWidget *parent = 0);
  ~MainWindow();

  void ReadSettings();   // Load up qt program settings at startup
  void WriteSettings();  // Save qt program settings when closing

  void closeEvent(QCloseEvent *event);  // Overloaded function
  void showNoMasterMessage();

 public Q_SLOTS:
  /******************************************
  ** Auto-connections (connectSlotsByName())
  *******************************************/
  void on_actionAbout_triggered();
  void on_button_connect_clicked(bool check);
  void on_button_list_clicked(bool check);
  void on_checkbox_use_environment_stateChanged(int state);
  void on_button_image_clicked(bool checked);

  /******************************************
  ** Manual connections
  *******************************************/
  void updateLoggingView();  // no idea why this can't connect automatically

private slots:
  void on_button_cam_with_pts_clicked(bool checked);

private slots:

 private:
  Ui::MainWindowDesign ui;
  QNode qnode;
  ImageNode * imageNode ;
  ImageNode * camLidarNode ;
};

}  // namespace boule_de_cristal

#endif  // boule_de_cristal_MAIN_WINDOW_H
