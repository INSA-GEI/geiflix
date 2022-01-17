/**
 * @file /src/main_window.cpp
 *
 * @brief Implementation for the qt gui.
 *
 * @date February 2011
 **/
/*****************************************************************************
** Includes
*****************************************************************************/

#include "../include/boule_de_cristal/main_window.hpp"
#include <QMainWindow>
#include <QMessageBox>
#include <QSettings>
#include <iostream>

/*****************************************************************************
** Namespaces
*****************************************************************************/

namespace boule_de_cristal {

using namespace Qt;

/*****************************************************************************
** Implementation [MainWindow]
*****************************************************************************/

MainWindow::MainWindow(int argc, char **argv, QWidget *parent)
    : QMainWindow(parent), qnode(argc, argv) {
  ui.setupUi(this);  // Calling this incidentally connects all ui's triggers to
                     // on_...() callbacks in this class.
  QObject::connect(
      ui.actionAbout_Qt, SIGNAL(triggered(bool)), qApp,
      SLOT(aboutQt()));  // qApp is a global variable for the application

  ReadSettings();
  setWindowIcon(QIcon(":/images/icon.png"));
  ui.tab_manager->setCurrentIndex(
      0);  // ensure the first tab is showing - qt-designer should have this
           // already hardwired, but often loses it (settings?).

  /*********************
  ** Logging
  **********************/
  ui.view_logging->setModel(qnode.loggingModel());
  QObject::connect(&qnode, SIGNAL(loggingUpdated()), this,
                   SLOT(updateLoggingView()));

  ui.button_list->setEnabled(false);
  ui.button_image->setEnabled(false);
  ui.button_cam_with_pts->setEnabled(false);

  /*********************
  ** Auto Start
  **********************/
  if (ui.checkbox_remember_settings->isChecked()) {
    on_button_connect_clicked(true);
  }
}

MainWindow::~MainWindow() {}

/*****************************************************************************
** Implementation [Slots]
*****************************************************************************/

void MainWindow::showNoMasterMessage() {
  QMessageBox msgBox;
  msgBox.setText("Couldn't find the ros master.");
  msgBox.exec();
  close();
}

/*
 * These triggers whenever the button is clicked, regardless of whether it
 * is already checked or not.
 */

void MainWindow::on_button_connect_clicked(bool check) {
  if (ui.checkbox_use_environment->isChecked()) {
    if (!qnode.init()) {
      showNoMasterMessage();
      return;
    } else {
      ui.button_connect->setEnabled(false);
      ui.button_list->setEnabled(true);
      ui.button_image->setEnabled(true);
      ui.button_cam_with_pts->setEnabled(true);
    }
  } else {
    if (!qnode.init(ui.line_edit_master->text().toStdString(),
                    ui.line_edit_host->text().toStdString())) {
      showNoMasterMessage();
      return;
    } else {
      ui.button_connect->setEnabled(false);
      ui.button_list->setEnabled(true);
      ui.button_image->setEnabled(true);
      ui.button_cam_with_pts->setEnabled(true);
      ui.line_edit_master->setReadOnly(true);
      ui.line_edit_host->setReadOnly(true);
      ui.line_edit_topic->setReadOnly(true);
    }
  }
  ros::NodeHandle nh;
  imageNode = new ImageNode("/usb_cam/image_raw", nh);
  camLidarNode = new ImageNode("/usb_cam/camera_lidar");
  camLidarIANode = new ImageNode("/usb_cam/cam_with_dist");
  alertNode = new AlertNode("/alert", nh);
  std::thread t([]() {
    ros::AsyncSpinner spinner(4);  // Use 4 threads
    spinner.start();
    ros::waitForShutdown();
  });
  t.detach();
}

void MainWindow::on_button_list_clicked(bool checked) { qnode.list(); }

void MainWindow::on_checkbox_use_environment_stateChanged(int state) {
  bool enabled;
  if (state == 0) {
    enabled = true;
  } else {
    enabled = false;
  }
  ui.line_edit_master->setEnabled(enabled);
  ui.line_edit_host->setEnabled(enabled);
  // ui.line_edit_topic->setEnabled(enabled);
}

/*****************************************************************************
** Implemenation [Slots][manually connected]
*****************************************************************************/

/**
 * This function is signalled by the underlying model. When the model changes,
 * this will drop the cursor down to the last line in the QListview to ensure
 * the user can always see the latest log message.
 */
void MainWindow::updateLoggingView() { ui.view_logging->scrollToBottom(); }

/*****************************************************************************
** Implementation [Menu]
*****************************************************************************/

void MainWindow::on_actionAbout_triggered() {
  QMessageBox::about(
      this, tr("About ..."),
      tr("<h2>PACKAGE_NAME Test Program 0.10</h2><p>"
         "Robot</p><p>This package needs an about description.</p>"));
}

/*****************************************************************************
** Implementation [Configuration]
*****************************************************************************/

void MainWindow::ReadSettings() {
  QSettings settings("Qt-Ros Package", "boule_de_cristal");
  restoreGeometry(settings.value("geometry").toByteArray());
  restoreState(settings.value("windowState").toByteArray());
  QString master_url =
      settings.value("master_url", QString("http://192.168.1.2:11311/"))
          .toString();
  QString host_url =
      settings.value("host_url", QString("192.168.1.3")).toString();
  // QString topic_name = settings.value("topic_name",
  // QString("/chatter")).toString();
  ui.line_edit_master->setText(master_url);
  ui.line_edit_host->setText(host_url);
  // ui.line_edit_topic->setText(topic_name);
  bool remember = settings.value("remember_settings", false).toBool();
  ui.checkbox_remember_settings->setChecked(remember);
  bool checked = settings.value("use_environment_variables", false).toBool();
  ui.checkbox_use_environment->setChecked(checked);
  if (checked) {
    ui.line_edit_master->setEnabled(false);
    ui.line_edit_host->setEnabled(false);
    // ui.line_edit_topic->setEnabled(false);
  }
}

void MainWindow::WriteSettings() {
  QSettings settings("Qt-Ros Package", "boule_de_cristal");
  settings.setValue("master_url", ui.line_edit_master->text());
  settings.setValue("host_url", ui.line_edit_host->text());
  // settings.setValue("topic_name",ui.line_edit_topic->text());
  settings.setValue("use_environment_variables",
                    QVariant(ui.checkbox_use_environment->isChecked()));
  settings.setValue("geometry", saveGeometry());
  settings.setValue("windowState", saveState());
  settings.setValue("remember_settings",
                    QVariant(ui.checkbox_remember_settings->isChecked()));
}

void MainWindow::closeEvent(QCloseEvent *event) {
  WriteSettings();
  QMainWindow::closeEvent(event);
}

void MainWindow::on_button_image_clicked(bool checked) {
  QString button_text = ui.button_image->text();
  if (button_text.compare("Voir camera") == 0) {
    ui.button_image->setText("Fermer camera");
    imageNode->showCamera();
  } else {
    imageNode->hideCamera();
    ui.button_image->setText("Voir camera");
  }
}
void MainWindow::on_button_cam_with_pts_clicked(bool checked) {
  QString button_text = ui.button_cam_with_pts->text();
  if (button_text.compare("Voir camera + pts du lidar") == 0) {
    ui.button_cam_with_pts->setText("Fermer camera + pts du lidar");
    camLidarNode->showCamera();
  } else {
    camLidarNode->hideCamera();
    ui.button_cam_with_pts->setText("Voir camera + pts du lidar");
  }
}

void MainWindow::on_button_cam_with_IA_clicked(bool checked) {
  QString button_text = ui.button_cam_with_IA->text();
  if (button_text.compare("Voir camera + IA + distance") == 0) {
    ui.button_cam_with_IA->setText("Fermer camera + IA + distance");
    camLidarIANode->showCamera();
  } else {
    camLidarIANode->hideCamera();
    ui.button_cam_with_IA->setText("Voir camera + IA + distance");
  }
}

}  // namespace boule_de_cristal

