# Serveur de la Raspberry Pi

[![forthebadge](https://forthebadge.com/images/badges/its-not-a-lie-if-you-believe-it.svg)](https://forthebadge.com)

## Topologie

La Raspi est connectée en Ethernet à la Jetson, et au bus CAN par l'intermédiaire de la carte PiCAN, qui sert de lien avec les autres cartes (Nucleos & Discovery).

## Fonctionnement

Un serveur python tourne sur la Raspi, qui écoute les données en provenance de la Jetson sur l'Ethernet et commande les moteurs en communiquant sur le CAN.  
Le serveur est contenu intégralement dans le fichier server.py, qu'il suffit de lancer avec la commande :
```sh
python3 server.py
```
lorsque l'on se situe dans le dossier `scripts`. Ne pas oublier de faire auparavant les installations nécessaires, précisées [ici](../documentation/README.md#installations-additionnelles).

## Principe

Le serveur récupère les données envoyées par la Jetson, à savoir :
- Angle de la cible par rapport à l'axe de la voiture
- Distance de la cible à la voiture
- Un bit ON/OFF pour commander directement l'arrêt de la voiture

À partir de ces informations, le serveur fait tourner un PID pour asservir en distance la voiture autour du point défini dans la variable `TARGET_DIST_MM` (par défaut, 2m). Il en tire la commande à appliquer aux moteurs et l'angle à leur donner, qu'il envoie sur le bus CAN.