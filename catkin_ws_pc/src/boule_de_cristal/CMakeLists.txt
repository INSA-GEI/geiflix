##############################################################################
# CMake
##############################################################################

cmake_minimum_required(VERSION 2.8.3)
project(boule_de_cristal)

##############################################################################
# Catkin
##############################################################################

# qt_build provides the qt cmake glue, roscpp the comms for a default talker
find_package(catkin REQUIRED COMPONENTS 
  qt_build 
  roscpp 
  std_msgs 
  cv_bridge
  image_transport
  sensor_msgs)

#include_directories(${catkin_INCLUDE_DIRS})

find_package(OpenCV REQUIRED)
find_package(Qt5Widgets REQUIRED)

QT5_WRAP_CPP(myMOC 
  include/${PROJECT_NAME}/main_window.hpp 
  include/${PROJECT_NAME}/qnode.hpp
  include/${PROJECT_NAME}/image_node.hpp
)
QT5_WRAP_UI(myUIC ui/main_window.ui)

set(SRC_FILES
  src/main.cpp
  src/main_window.cpp
  src/qnode.cpp
  src/image_node.cpp
)




# Use this to define what the package will export (e.g. libs, headers).
# Since the default here is to produce only a binary, we don't worry about
# exporting anything. 
catkin_package(
  CATKIN_DEPENDS qt_build roscpp std_msgs cv_bridge image_transport sensor_msgs
)


link_directories(/usr/local/lib)

## Specify additional locations of header files
## Your package locations should be listed before other locations
include_directories(
  ${catkin_INCLUDE_DIRS}
  ${CMAKE_CURRENT_BINARY_DIR}/..
  ${OpenCV_INCLUDE_DIRS}
  /usr/local/include/yaml-cpp
)


##############################################################################
# Binaries
##############################################################################

#add_executable(boule_de_cristal ${QT_SOURCES} ${QT_RESOURCES_CPP} ${QT_FORMS_HPP} ${QT_MOC_HPP})
add_executable(boule_de_cristal ${SRC_FILES} ${myMOC} ${myUIC})
target_link_libraries(boule_de_cristal ${catkin_LIBRARIES} ${OpenCV_LIBS} Qt5::Widgets yaml-cpp)

#target_link_libraries(boule_de_cristal ${QT_LIBRARIES} ${catkin_LIBRARIES})
#install(TARGETS boule_de_cristal RUNTIME DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION})

