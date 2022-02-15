echo "What is the new hostname for this system? (be careful upon input)"
OLDHOST=$(hostname)
read NEWHOST

sed -i "s/127.0.1.1 ${OLDHOST}/127.0.1.1 ${NEWHOST}/" /etc/hosts
sed -i "s/${OLDHOST}/${NEWHOST}/" /etc/hostname

yum -y install VirtualBox-6.1
yum -y install xrdp

systemctl enable xrdp
systemctl start xrdp

systemctl status xrdp

reboot