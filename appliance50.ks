############################################################################
## Kickstart Options
############################################################################

cdrom
firstboot --disable
install
keyboard us
network --bootproto=dhcp --noipv6
lang en_US.UTF-8
repo --cost=1 --name=os --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-19&arch=i386
repo --cost=1 --name=fedora-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=fedora-debug-19&arch=i386
repo --cost=1 --name=updates --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-f19&arch=i386
repo --cost=1 --name=updates-debuginfo --mirrorlist=http://mirrors.fedoraproject.org/metalink?repo=updates-released-debug-f19&arch=i386
rootpw --plaintext crimson
selinux --permissive
timezone --utc America/New_York
xconfig --startxonboot


bootloader --location=mbr --boot-drive=sda
autopart --type=lvm
clearpart --none --initlabel --drives=sda

############################################################################
## Package Selection
############################################################################

%packages

# base
@base-x

# core
@core

# avoids
# Unable to create appliance : Unable to install grub2 bootloader
grub2

# release; cannot be installed by update50 due to grub2 dependencies
generic-logos
generic-release
-fedora-logos
-fedora-release
-fedora-release-notes

# necessary packages for update50
unzip
sed

#prevent "Unable to run ['/usr/bin/firewall-offline-cmd', '--enabled']!" error
firewall-config

%end


############################################################################
## Post-installation Script
############################################################################

%post

# lock root (because doing so in appliance50 RPM alone doesn't work when boxgrinding or kickstarting)
/usr/bin/passwd -l root

# run install50
/bin/curl http://mirror.cs50.net/appliance50/19/source/install50 | /bin/bash

############################################################################
# clean up
############################################################################

# delete yum's cache
/usr/bin/yum clean all
/usr/bin/yum clean metadata
/bin/rm -rf /var/cache/yum/*

# delete temporary files
/bin/rm -f /root/*
/bin/rm -rf /tmp/.[^.]* && /bin/rm -rf /tmp/..?*

# fill disk with 0s, to facilitate disk's compression
/bin/cat /dev/zero > /tmp/zero.fill
/bin/sync
/bin/sleep 1
/bin/sync
/bin/rm -f /tmp/zero.fill


%end
