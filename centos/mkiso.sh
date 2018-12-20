#!/bin/bash -x

# https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/installation_guide/sect-simple-install-kickstart

sudo -l
mntdir=$(sudo mktemp -d -p /mnt)
efibootdir=$(sudo mktemp -d -p /mnt)

cleanup1 () {
  if [ -d $mntdir ]; then
    sudo umount $mntdir
    sudo rm -rf $mntdir
  fi
}

cleanup2 () {
  if [ -d $efibootdir ]; then
    sudo umount $efibootdir
    sudo rm -rf $efibootdir
  fi
}

cleanup () {
  cleanup1
  cleanup2
}

trap cleanup EXIT

sudo mount -o loop CentOS-7-x86_64-Minimal-1804.iso $mntdir
sudo rsync -avd $mntdir/ ./centos-install
cleanup1
sudo cp anaconda-ks.cfg ./centos-install
sudo cp isolinux.cfg centos-install/isolinux/isolinux.cfg
sudo cp grub.cfg centos-install/EFI/BOOT/grub.cfg
sudo mount ./centos-install/images/efiboot.img $efibootdir
sudo cp grub.cfg $efibootdir/EFI/BOOT/grub.cfg
cleanup2
# https://www.syslinux.org/wiki/index.php?title=Isohybrid#UEFI
UEFI_ARGS="-eltorito-alt-boot -e images/efiboot.img -no-emul-boot"
sudo mkisofs -J -T -o centos-ks.iso -b isolinux/isolinux.bin -c isolinux/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table $UEFI_ARGS -R -m TRANS.TBL -graft-points -V "CentOS 7 x86_64" ./centos-install
sudo isohybrid --uefi centos-ks.iso
sudo chown $(id -u):$(id -g) centos-ks.iso

