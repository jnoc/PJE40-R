fdisk /dev/sdb

umount /dev/sdb1
mkfs.xfs /dev/sdb1 -f
mkdir /mnt/500GB; mount /dev/sdb1 /mnt/500GB; mount | grep /dev/sdb1;

chmod ugo+rwx /mnt/500GB; chmod ugo+rwx /mnt/main;