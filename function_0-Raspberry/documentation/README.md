# Function 0 - Raspberry

Le systeme central est basé sur une raspberry pi 3B, sur laquelle est fixée un "HAT" pican2 de chez [skpang](https://www.skpang.co.uk/collections/hats/products/pican2-can-bus-board-for-raspberry-pi-2-3)

## Creation de la carte SD

Recuperer l'image de la carte SD de base [ici](https://www.raspberrypi.org/software/operating-systems/) et ecrivez là sur une carte SD suffisamment grande et rapide (minimum: 8 GB). Recuperez de preference la version Lite.

- Windows
Utilisez un utilitaire comme celui de la [sd association](https://www.sdcard.org/downloads/formatter_4/eula_windows/) pour ecrire l'image

- Linux
Utilisez [Etcher](https://www.balena.io/etcher) pour ecrire l'image.

## Configuration de base du systeme

Apres le premier demarrage, lancez (*sudo raspi-config*) et configurez les points suivants:

- Interfaces: Activez SSH
- Localisation : Passez le clavier en francais, regler le WIFi sur France, timezone sur Paris

Ensuite, modifiez /etc/hosts et /etc/hostname pour changer le nom *raspberrypi* du systeme en *geicar*

Faites une mise à jour (*sudo apt update && sudo apt full-upgrade -y && sudo apt autoremove -y*)

## Compte et mot de passe

Le seul compte present est celui initialement fourni avec raspberryOS à savoir:
- identifiant: pi
- mot de passe: raspberry

## Configuration de la carte PiCan2

Pour activer la carte, rajoutez à la fin du fichier /boot/config.txt les lignes suivantes:
*dtparam=spi=on*
*dtoverlay=mcp2515-can0,oscillator=16000000,interrupt=25*
*dtoverlay=spi-bcm2835-overlay*

Ensuite copiez le service present dans le depot sous ./systemd-system/pican2.service dans /lib/systemd/system

Activez le service (*sudo systemctl enable pican2*)

Rebootez (*sudo reboot*)

Au reboot, verifiez que le service est demarré (*sudo systemctl status pican2*)

Installez ensuite le support python et cli (*sudo apt install python-can can-utils*)

L'image ainsi créée est telechargeble directement depuis le serveur du GEI [2021-05-07-raspios-buster-armhf-lite-pican2.img.7z] (http://srv-geitp.insa-toulouse.fr/geiflix/rpi-geicar/2021-05-07-raspios-buster-armhf-lite-pican2.img.7z) (RQ: pensez au VPN depuis chez vous)

## Installation de ROS

La version de ROS installée sur la carte SD est Kinetic Kame. Pour l'installer, la procedure suivante a été **scrupuleusement** suivie : [Installing ROS Kinetic on the Raspberry Pi] (http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi)

L'image ainsi créée est telechargeble directement depuis le serveur du GEI [2021-05-07-raspios-buster-armhf-lite-pican2-ros_Kinetic.img.7z] (http://srv-geitp.insa-toulouse.fr/geiflix/rpi-geicar/2021-05-07-raspios-buster-armhf-lite-pican2-ros_Kinetic.img.7z) (RQ: pensez au VPN depuis chez vous)

## Réseau

### Configuration de la raspberry en hotspot Wifi + configuration d'un serveur DHCP

Tutoriel suivi: [Creer un point d'acces Wifi (hostapd)](https://www.framboise314.fr/raspap-creez-votre-hotspot-wifi-avec-un-raspberry-pi-de-facon-express/)

Une fois le script raspAP lancé et la raspberry redemarrée, modifiez les fichiers de config de hostapd et dnsmasq. Les fichiers  se trouve dans le depot sous config/hostapd et config/dnsmasq et doivent etre deposé respectivement dans /etc/hostapd et /etc/dnsmasq.

- Pour Hostapd, les modifications consistent à changer les valeurs des champs ssid (mettez geicar1, par ex) et wpa_passphrase (ici Geicar1234). On peut aussi changer le channel (de 1 à 13)
- Pour dnsmasq, les modifications consistent a rajouter/modifer les configurations des interfaces reseau dans /etc/dnsmasq.d. Les fichiers de configuration peuvent etre trouvés dans /config/dnsmasq.d et permettent de faire du DHCP sur ETH0 et WLAN0, avec des plage d'IP fixes (pour la jetson par ex).

Après installation de hostapd et dnsmasq, un hotspot wifi est fournis par chaque voiture avec les caracteristiques suivantes:

- ssid: geicar(1-4)
- pass: Geicar1234
- Compte d'administration: admin
- Mot de passe d'administration: secret

De plus, dnsmasq fourni les plages d'adresses suivantes:

- eth0: plage DHCP : 192.168.1.50 -> 192.168.1.250
        gateway: 192.168.1.1

        Ip Fixe DHCP: 192.168.1.10 (pour une des jetson, a modifer pour les autres)

- wlan0: plage DHCP : 192.168.0.50 -> 192.168.0.250
         gateway : 192.168.0.1

### SSH

Une fois le hotspot & DHCP configurés, on peut se connecter à la Pi en SSH. Pour cela, il faut d'abord se connecter au hotspot, puis on utilise la commande `ssh` (à activer sur Windows), suivie de l'adresse à laquelle on veut se connecter, à savoir :
```sh
ssh pi@192.168.0.2
```
On renseigne ensuite le mot de passe, et quand la connexion est terminée, on accède au terminal distant.

Si le DHCP & surtout le bail statique pour la Jetson ont été configurés sur `eth0`, on peut également se connecter en SSH sur la Jetson. On procède de la même façon que pour la Pi, en se connectant au hotspot et en utilisant la commande :
```sh
ssh admin-jetson@192.168.1.10
```

##### Perte de connexion

Si la connection est perdue avec l'hôte distant (la Pi ou la Jetson), le terminal SSH ne répond plus, à `CTRL+C` ou `CTRL+D` notamment. Cela peut par exemple arriver si l'alimentation est coupée brutalement, ou lors d'un redémarrage depuis une machine distante (lorsqu'on est connecté en SSH avec `sudo reboot`). Pour éviter d'avoir à fermer & rouvrir le terminal, on peut envoyer la séquence de clôture de connexion suivante :
`Entrée ⏎` + `~` + `.`
Cela termine la session SSH et retourne donc au terminal depuis laquelle elle a été lancée.

### Connexion au réseau WiFi IOT

Pour se connecter au réseau IOT, il faut que la date/heure corresponde à peut près à la date/heure réelle. Cependant, il y a de la dérive naturellement puisque la Raspberry de synchronise pas le temps et n'a pas de RTC pour continuer à garder le temps. Lorsque l'écart devient trop important, la Pi n'arrive plus à se connecter, et il faut donc màj la date/l'heure manuellement, au moyen de la commande `date` :
```sh
date --set='[date]'
```
où `[date]` peut être renseignée dans différents formats, on peut utiliser par exemple :
```
10:00 17 nov
```
On peut ensuite redémarrer la Pi pour appliquer les changements :
```sh
sudo reboot
```

## Installations additionnelles

Le serveur Python tournant sur la Pi a besoin de deux paquets Pythons pour fonctionner, qui nécessitent donc d'être installés.

### `python-can`

C'est le paquet qui fournit le support du bus CAN en Python, et les abstractions qui permettent de communiquer avec (par l'intermédiaire de la carte PiCAN).

#### Installation

```sh
pip install python-can
```

#### Liens

- [Page PyPI du paquet](https://pypi.org/project/python-can/),
- [Documentation](https://python-can.readthedocs.io/en/master/index.html).

### `simple-pid`

C'est le paquet qui fournit l'implémentation en Python d'un PID.

#### Installation

```sh
pip install simple-pid
```

#### Liens

- [Page PyPI du paquet](https://pypi.org/project/simple-pid/),
- [Documentation](https://simple-pid.readthedocs.io/en/latest/).