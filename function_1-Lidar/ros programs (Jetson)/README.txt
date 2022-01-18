Ces différentes fonctions sur la Jetson permettent grâce au lidar :
- de détecter des objets à 2m 
- en determiner leur position relative par rapport au lidar
- de donner des ordres à la voiture en conséquence (stop si portique detecté à l'arrière du véhicule, avancer sinon)


Dossier Commandes de lancement bash : Rassemble toutes les commandes à effectuer a partir d'un seul fichier bash

Dossier laser2pc : Conversion de messages LaserScan en PointClouds2 (nécessaire pour le tracking)

Dossier multiple-object-tracking-lidar : Tracking de 6 objets (souscription au topic PointCloud2 dans main.cpp)

Dossier pc_manip_tracking : traitement des données du tracking pour en déterminer la position relative des objets et leur détection à 2m ou moins par rapport au capteur

Dossier rplidar_ros : Lancement du lidar (voir https://github.com/Slamtec/rplidar_ros)

Dossier trajectory : Envoi des ordres à la voiture via le topic /Motor_commands connaissant la distance et la position des objets



