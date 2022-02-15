#!/usr/bin/env bash
# this script must be run as 'sudo ./setup.sh'

echo "This is a shell setup script"

echo "Regenerating machine ID"
# this stops virtual bridging issues where the same ip is assigned to the clone of the original
# the netplan file also has 'dchp-identifier: mac' added inorder to mitigate the issue straight away after deployed
# this is solely to get it working with multiple cloned virtualboxes however could be of use for virtualisation softwares
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


# this assigns a static ip address for the node which is predetmined according to the design of the network
echo "What is the static ip address needed for this server?"
echo "Refer to the network design for the specific ip address for this node"
echo "10.1.100.XXX - Where the entered XXX is the assigned ending"
read STATIC

sed -i "s/- 10.1.100.149\/24/- 10.1.100.${STATIC}\/24/" /etc/netplan/00-installer-config.yaml

reboot