echo "What is the new hostname for this system? (be careful upon input)"
OLDHOST=$(hostname)
read NEWHOST
# update hosts and hostname with new hostname
sed -i "s/127.0.1.1 ${OLDHOST}/127.0.1.1 ${NEWHOST}/" /etc/hosts
sed -i "s/${OLDHOST}/${NEWHOST}/" /etc/hostname
# install packages and check if they are running
yum -y install VirtualBox-6.1
yum -y install xrdp
systemctl enable xrdp
systemctl start xrdp
systemctl status xrdp

# run fdisk to manually wipe then format, mount 
# and make directories for the virtual machines
fdisk /dev/sdb
umount /dev/sdb1
mkfs.xfs /dev/sdb1 -f
mkdir /mnt/500GB; mount /dev/sdb1 /mnt/500GB; mount | grep /dev/sdb1;
chmod ugo+rwx /mnt/500GB; chmod ugo+rwx /mnt/main;

# the final tree look being
# /mnt/
# ├── 500GB
# │   └── node-01
# └── main
#     └── node-02
reboot