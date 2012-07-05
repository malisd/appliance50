###########################################################################
### CS50 Appliance 17
###
### https://manual.cs50.net/appliance50
###
### David J. Malan
### malan@harvard.edu
############################################################################


############################################################################
## Kickstart Options
############################################################################

autopart
bootloader --append="biosdevname=0 quiet rhgb" --driveorder=sda --location=mbr
cdrom
clearpart --all --initlabel
install
keyboard us
lang en_US.UTF-8
#part biosboot --fstype=biosboot --size=1

# sda2
# http://docs.fedoraproject.org/en-US/Fedora/16/html/Installation_Guide/s2-diskpartrecommend-x86.html
#part swap --ondisk=sda --size=2048

# sda3
#part /boot --fstype=ext4 --ondisk=sda --size=500

# sda4
#part / --fstype=ext4 --grow --ondisk=sda

poweroff
repo --cost=1 --name=os --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-17&arch=i386
repo --cost=1 --name=fedora-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-debug-17&arch=i386
repo --cost=1 --name=updates --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-f17&arch=i386
repo --cost=1 --name=updates-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-debug-f17&arch=i386
repo --cost=2 --name=appliance50 --baseurl=http://mirror.cs50.net/appliance50/17/RPMS/
repo --cost=3 --name=dropbox --baseurl=http://linux.dropbox.com/fedora/17/
repo --cost=3 --name=google-chrome --baseurl=http://dl.google.com/linux/chrome/rpm/stable/i386
repo --cost=3 --name=webmin --mirrorlist=http://download.webmin.com/download/yum/mirrorlist
rootpw --plaintext crimson
selinux --permissive
timezone --utc America/New_York
xconfig --startxonboot


############################################################################
## Package Selection
############################################################################

%packages

# base
@base-x

# kernel
kernel
kernel-devel
kernel-headers

# core
@core
#@fonts

# Xfce
@xfce-desktop

# release
generic-logos
generic-release
-fedora-logos
-fedora-release
-fedora-release-notes

# fonts
#dejavu-fonts-common
#dejavu-sans-fonts
#dejavu-sans-mono-fonts
#dejavu-serif-fonts
#liberation-fonts-common
#liberation-mono-fonts
#liberation-sans-fonts
#liberation-serif-fonts
#liberation-narrow-fonts

# CS50
#appliance50

# unwanted
#-audit
#-gnome-bluetooth-libs
#-java-*-gcj
#-leafpad
#-libgcj
#-libpcap
#-ModemManager
#-mousepad
#-openbox
#-openbox-libs
#-openssh-askpass
#-orage
#-policycoreutils*
#-ppp
#-selinux-*
#-xfce4-appfinder
#-xfce4-power-manager
#-xscreensaver-base

%end


############################################################################
## Post-installation Script
############################################################################

%post

# interferes with biosdevname=0
#/usr/bin/yum -y remove NetworkManager
#/usr/bin/yum -y remove NetworkManager-glib
#/usr/bin/yum -y remove NetworkManager-gnome

## unwanted, but - doesn't suffice above
#/usr/bin/yum -y remove abrt dnsmasq kernel-PAE wpa_supplicant
#
## updates 
#/usr/bin/yum -y update
#
## finish configuration after a boot
#/bin/cat > /etc/rc.d/rc.local << "EOF"
##!/bin/bash
#
## ensure networking has enough time to start
#/bin/sleep 10
#
## re-install appliance's RPM (to configure MySQL)
#/usr/bin/yum -y reinstall cs50-appliance
#
## install VirtualBox Guest Additions or VMware Tools
#declare vmm=$(/bin/grep vmm= /proc/cmdline)
#declare regex='vmm=(\w+)'
#if [[ "$vmm" =~ $regex ]]
#then
#    case ${BASH_REMATCH[1]} in
#    vbox)
#        # download and mount VirtualBox Guest Additions
#        /usr/bin/wget --directory-prefix=/tmp http://download.virtualbox.org/virtualbox/4.1.8/VBoxGuestAdditions_4.1.8.iso
#        /bin/mount -r -o loop -t iso9660 /tmp/VBoxGuestAdditions_4.1.8.iso /mnt
#
#        # install VirtualBox Guest Additions
#        /mnt/VBoxLinuxAdditions.run --nox11
#
#        # tidy up
#        /bin/umount /mnt
#        /bin/rm -f /tmp/VBoxGuestAdditions_4.1.8.iso
#    ;;
#    vmware)
#        # download and mount VMware Tools ISO
#        /usr/bin/wget --directory-prefix=/tmp http://softwareupdate.vmware.com/cds/vmw-desktop/fusion/4.1.1/536016/packages/com.vmware.fusion.tools.linux.zip.tar
#        /bin/tar xf /tmp/com.vmware.fusion.tools.linux.zip.tar -C /tmp
#        /usr/bin/unzip /tmp/com.vmware.fusion.tools.linux.zip -d /tmp
#        /bin/mount -r -o loop -t iso9660 /tmp/payload/linux.iso /mnt
#        /bin/tar xf /mnt/VMwareTools-8.8.1-528969.tar.gz -C /tmp
#        /bin/rm -f /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
#
#        # convince VMware Tools to install within VirtualBox
#        /bin/echo "#!/bin/bash" >> /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
#        /bin/echo "/bin/echo 'good'" >> /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
#        /bin/echo "/bin/true" >> /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
#        /bin/chmod a+x /tmp/vmware-tools-distrib/lib/sbin32/vmware-checkvm
#
#        # install VMware Tools
#        /tmp/vmware-tools-distrib/vmware-install.pl -d
#
#        # tidy up
#        /bin/rm -rf /tmp/vmware-tools-distrib
#        /bin/umount /mnt
#        /bin/rm -rf /tmp/payload
#        /bin/rm -f /tmp/com.vmware.fusion.tools.linux.zip
#        /bin/rm -f /tmp/com.vmware.fusion.tools.linux.zip.tar
#    ;;
#    esac
#fi
#/bin/rm -f /etc/rc.d/rc.local
#/bin/rm -f /root/*
#/usr/bin/poweroff
#EOF
#/bin/chmod 755 /etc/rc.d/rc.local
#
## delete yum's cache
#/usr/bin/yum clean all
#/usr/bin/yum clean metadata
#/bin/rm -rf /var/cache/yum/*


############################################################################
# clean up
############################################################################

## delete yum's cache
#/usr/bin/yum clean all
#/usr/bin/yum clean metadata
#/bin/rm -rf /var/cache/yum/*
#
## delete temporary files
#/bin/rm -f /root/*
#/bin/rm -rf /tmp/.[^.]* && /bin/rm -rf /tmp/..?*
#
## just in case it exists
#/bin/rm -f /etc/udev/rules.d/70-persistent-net.rules
#
## fill disk with 0s, to facilitate VMDK's compression
#/bin/cat /dev/zero > /tmp/zero.fill
#/bin/sync
#/bin/sleep 1
#/bin/sync
#/bin/rm -f /tmp/zero.fill


%end
