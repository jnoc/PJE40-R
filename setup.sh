#!/usr/bin/env bash

echo "This is a shell setup script"

echo "Regenerating machine ID"
rm -f /etc/machine-id
dbus-uuidgen --ensure=/etc/machine-id
rm /var/lib/dbus/machine-id
dbus-uuidgen --ensure
echo "Regen done!"


echo "What is the new hostname for this system? (be careful upon input)"
OLDHOST=$(hostname)
read NEWHOST

sed -i "s/127.0.1.1 ${OLDHOST}/127.0.1.1 ${NEWHOST}/" /etc/hosts
sed -i "s/${OLDHOST}/${NEWHOST}/" /etc/hostname

reboot