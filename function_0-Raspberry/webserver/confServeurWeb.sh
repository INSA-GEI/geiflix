#!/bin/bash

if [ `id -u` != 0 ]; then
	echo "Merci de relancer avec sudo"
	exit 1
fi

activated=`readlink /var/www/html`
if [ "$activated" = "Klunk" ]; then
	RaspAP_Text="Activer RaspAP"
	Klunk_Text="Laisser Klunk"
else
	RaspAP_Text="Laisser RaspAP"
	Klunk_Text="Activer Klunk"
fi

whiptail --title "Configuration du serveur Web"  \
	--yes-button "$RaspAP_Text" --no-button "$Klunk_Text" \
	--yesno "Le serveur Web est actuellement configuré pour $activated.\nQue voulez-vous faire ?" 0 70
result=$?

if [ "$result" = 0 ] && [ "$activated" != "RaspAP" ]; then
	rm /var/www/html
	ln -s RaspAP /var/www/html
	lighty-enable-mod raspap-router > /dev/null
	service lighttpd force-reload > /dev/null
	whiptail --title "Configuration du serveur Web"  \
		--msgbox "RaspAP a bien été activé" 0 70
elif [ "$result" = 1 ] && [ "$activated" != "Klunk" ]; then
	rm /var/www/html
	ln -s Klunk /var/www/html
	lighty-disable-mod raspap-router > /dev/null
	service lighttpd force-reload > /dev/null
	whiptail --title "Configuration du serveur Web"  \
		--msgbox "Klunk a bien été activé" 0 70
else
	whiptail --title "Configuration du serveur Web"  \
		--msgbox "Rien n'a été modifié" 0 70
fi
